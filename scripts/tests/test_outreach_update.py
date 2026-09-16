import contextlib
import importlib.util
import io
import json
import subprocess
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "outreach_update.py"
SPEC = importlib.util.spec_from_file_location("outreach_update", SCRIPT)
assert SPEC and SPEC.loader
outreach = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(outreach)


RECEIPT_ID = "pre_send_" + "a" * 20
OWNER_RESULT = {
    "status": "RECORDED",
    "preSendReceiptId": RECEIPT_ID,
    "sentEventId": "suppression_event_" + "b" * 20,
    "ownerRevision": "c" * 64,
    "observedAt": "2026-09-16T12:34:56Z",
}


class ConfirmedSendBoundaryTests(unittest.TestCase):
    def completed(self, *, returncode=0, stdout=None, stderr=""):
        return subprocess.CompletedProcess(
            [], returncode,
            json.dumps(OWNER_RESULT, sort_keys=True) + "\n" if stdout is None else stdout,
            stderr,
        )

    def test_invokes_only_fixed_jt_ops_command_with_opaque_receipt_id(self):
        with mock.patch.object(outreach.subprocess, "run", return_value=self.completed()) as run:
            result = outreach.record_cohort_two_confirmed_send(RECEIPT_ID)

        self.assertEqual(result, OWNER_RESULT)
        run.assert_called_once_with(
            [
                outreach.JT_OPS_PYTHON,
                outreach.JT_OPS_SCRIPT,
                "record-confirmed-send",
                "--pre-send-receipt-id",
                RECEIPT_ID,
            ],
            cwd=outreach.JT_OPS_ROOT,
            env={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0"},
            text=True,
            capture_output=True,
            timeout=outreach.JT_OPS_TIMEOUT_SECONDS,
        )

    def test_rejects_paths_tuples_fingerprints_and_noncanonical_ids_before_spawn(self):
        invalid = (
            "/tmp/receipt.json",
            "pre_send_" + "a" * 19,
            "pre_send_" + "A" * 20,
            "prospect|organization|fingerprint",
            "a" * 64,
            " pre_send_" + "a" * 20,
        )
        with mock.patch.object(outreach.subprocess, "run") as run:
            for value in invalid:
                with self.subTest(value=value), self.assertRaisesRegex(
                    outreach.ConfirmedSendError, "invalid"
                ):
                    outreach.record_cohort_two_confirmed_send(value)
        run.assert_not_called()

    def test_owner_failure_modes_are_generic_and_never_claim_success(self):
        secret = "credential-that-must-not-escape"
        failures = (
            self.completed(returncode=2, stdout=secret, stderr=""),
            self.completed(stderr=secret),
            self.completed(stdout="not-json\n"),
            self.completed(stdout=json.dumps(OWNER_RESULT)),
            self.completed(stdout=json.dumps(OWNER_RESULT) + "\nextra\n"),
            self.completed(stdout=json.dumps({**OWNER_RESULT, "extra": secret}) + "\n"),
            self.completed(stdout=json.dumps({**OWNER_RESULT, "status": "READY"}) + "\n"),
            self.completed(stdout=json.dumps({**OWNER_RESULT, "preSendReceiptId": "pre_send_" + "d" * 20}) + "\n"),
            self.completed(stdout=json.dumps({**OWNER_RESULT, "ownerRevision": "bad"}) + "\n"),
            self.completed(stdout=json.dumps({**OWNER_RESULT, "observedAt": "2026-99-99T99:99:99Z"}) + "\n"),
        )
        for completed in failures:
            with self.subTest(completed=completed), mock.patch.object(
                outreach.subprocess, "run", return_value=completed
            ), self.assertRaises(outreach.ConfirmedSendError) as raised:
                outreach.record_cohort_two_confirmed_send(RECEIPT_ID)
            self.assertEqual(str(raised.exception), "cohort-two confirmed-send owner rejected the receipt")
            self.assertNotIn(secret, str(raised.exception))

        for failure in (
            subprocess.TimeoutExpired([secret], 15, output=secret, stderr=secret),
            OSError(secret),
        ):
            with self.subTest(failure=type(failure).__name__), mock.patch.object(
                outreach.subprocess, "run", side_effect=failure
            ), self.assertRaises(outreach.ConfirmedSendError) as raised:
                outreach.record_cohort_two_confirmed_send(RECEIPT_ID)
            self.assertEqual(str(raised.exception), "cohort-two confirmed-send owner is unavailable")
            self.assertNotIn(secret, str(raised.exception))

    def test_cohort_failure_prevents_all_local_completion_mutations_and_done_claim(self):
        args = [
            "--slug", "example", "--company", "Example Co", "--message", "M1",
            "--channel", "Email", "--date", "2026-09-16",
            "--cohort-two-pre-send-receipt-id", RECEIPT_ID,
        ]
        output, errors = io.StringIO(), io.StringIO()
        with mock.patch.object(
            outreach, "record_cohort_two_confirmed_send",
            side_effect=outreach.ConfirmedSendError("safe failure"),
        ), mock.patch.object(outreach, "load_outreach_draft") as load, mock.patch.object(
            outreach, "update_pipeline_md"
        ) as pipeline, mock.patch.object(outreach, "close_mc_task") as close, mock.patch.object(
            outreach, "create_followup_task"
        ) as followup, contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            status = outreach.main(args)

        self.assertEqual(status, 1)
        load.assert_not_called()
        pipeline.assert_not_called()
        close.assert_not_called()
        followup.assert_not_called()
        self.assertNotIn("Done", output.getvalue())
        self.assertEqual(errors.getvalue().strip(), "ERROR: cohort-two confirmed-send failed")

    def test_present_but_blank_receipt_id_cannot_fall_back_to_legacy_path(self):
        args = [
            "--slug", "example", "--company", "Example Co", "--message", "M1",
            "--channel", "Email", "--date", "2026-09-16",
            "--cohort-two-pre-send-receipt-id", "",
        ]
        with mock.patch.object(
            outreach, "record_cohort_two_confirmed_send",
            side_effect=outreach.ConfirmedSendError("invalid"),
        ) as record, mock.patch.object(
            outreach, "load_outreach_draft"
        ) as load, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            status = outreach.main(args)

        self.assertEqual(status, 1)
        record.assert_called_once_with("")
        load.assert_not_called()

    def test_legacy_send_remains_compatible_and_does_not_spawn_jt_ops(self):
        args = [
            "--slug", "example", "--company", "Example Co", "--message", "M1",
            "--channel", "Email", "--date", "2026-09-16",
        ]
        draft = mock.Mock()
        with mock.patch.object(outreach, "record_cohort_two_confirmed_send") as record, mock.patch.object(
            outreach, "load_outreach_draft", return_value=(draft, "content")
        ), mock.patch.object(outreach, "update_outreach_draft"), mock.patch.object(
            outreach, "update_pipeline_md"
        ), mock.patch.object(outreach, "close_mc_task"), mock.patch.object(
            outreach, "create_followup_task"
        ), contextlib.redirect_stdout(io.StringIO()):
            status = outreach.main(args)

        self.assertEqual(status, 0)
        record.assert_not_called()

    def test_parser_exposes_no_receipt_path_tuple_or_fingerprint_inputs(self):
        options = {
            option
            for action in outreach.build_parser()._actions
            for option in action.option_strings
        }
        self.assertIn("--cohort-two-pre-send-receipt-id", options)
        self.assertFalse(options & {
            "--receipt-path", "--pre-send-receipt-path", "--prospect-id",
            "--organization-fact-id", "--channel-fingerprint",
        })


if __name__ == "__main__":
    unittest.main()
