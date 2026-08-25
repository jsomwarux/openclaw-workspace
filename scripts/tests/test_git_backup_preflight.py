import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.git_backup_preflight import inspect_repository


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


class GitBackupPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.remote = root / "remote.git"
        self.repo = root / "repo"
        self.peer = root / "peer"
        git(root, "init", "--bare", str(self.remote))
        git(root, "clone", str(self.remote), str(self.repo))
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test User")
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "base")
        self.branch = git(self.repo, "branch", "--show-current")
        git(self.repo, "push", "-u", "origin", self.branch)

    def tearDown(self):
        self.temp.cleanup()

    def peer_commit(self):
        git(self.remote.parent, "clone", str(self.remote), str(self.peer))
        git(self.peer, "config", "user.email", "peer@example.com")
        git(self.peer, "config", "user.name", "Peer User")
        (self.peer / "REMOTE.md").write_text("remote\n", encoding="utf-8")
        git(self.peer, "add", "REMOTE.md")
        git(self.peer, "commit", "-m", "remote")
        git(self.peer, "push", "origin", self.branch)

    def test_clean_synced_repository_is_push_safe(self):
        result = inspect_repository(self.repo, self.branch)
        self.assertTrue(result["push_safe"])
        self.assertEqual(result["ahead"], 0)
        self.assertEqual(result["behind"], 0)

    def test_remote_ahead_repository_fails_closed_after_fetch(self):
        self.peer_commit()
        result = inspect_repository(self.repo, self.branch)
        self.assertFalse(result["push_safe"])
        self.assertEqual(result["ahead"], 0)
        self.assertEqual(result["behind"], 1)
        self.assertEqual(result["status"], "REMOTE_AHEAD")

    def test_diverged_repository_fails_closed(self):
        self.peer_commit()
        (self.repo / "LOCAL.md").write_text("local\n", encoding="utf-8")
        git(self.repo, "add", "LOCAL.md")
        git(self.repo, "commit", "-m", "local")
        result = inspect_repository(self.repo, self.branch)
        self.assertFalse(result["push_safe"])
        self.assertEqual(result["ahead"], 1)
        self.assertEqual(result["behind"], 1)
        self.assertEqual(result["status"], "DIVERGED")

    def test_backup_script_uses_preflight_for_all_three_repositories(self):
        script = (Path(__file__).parents[1] / "backup.sh").read_text(encoding="utf-8")
        self.assertIn("backup_git_repo \"$WORKSPACE\" master", script)
        self.assertIn("backup_git_repo \"$HOME/projects/jt-consulting-pipeline\" master", script)
        self.assertIn("backup_git_repo \"$HOME/projects/n8n-agent\" main", script)
        self.assertIn("git_backup_preflight.py", script)


if __name__ == "__main__":
    unittest.main()
