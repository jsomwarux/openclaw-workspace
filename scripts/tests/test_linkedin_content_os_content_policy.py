from __future__ import annotations

import unittest

from scripts.linkedin_content_os.content_policy import (
    PUBLIC_SURFACES,
    require_public_copy,
    violations,
)


# One governed example per hard ban in docs/agents/content-rules.md and
# memory/content-voice.md, keyed by the rule identifier the policy must report.
BANNED_EXAMPLES = (
    # content-voice.md "Forbidden Words (zero exceptions across all platforms)".
    ("forbidden_word", "We utilize one review queue."),
    ("forbidden_word", "The synergy shows up in review."),
    ("forbidden_word", "The ecosystem sets the pace."),
    ("forbidden_word", "A scalable review path."),
    ("forbidden_word", "We streamline the review path."),
    ("forbidden_word", "One actionable review step."),
    ("forbidden_word", "The team lacks bandwidth for review."),
    ("forbidden_word", "A holistic review path."),
    ("forbidden_word", "An innovative review path."),
    ("forbidden_word", "A robust review path."),
    ("forbidden_word", "A cutting-edge review path."),
    ("forbidden_word", "A best-in-class review path."),
    ("forbidden_word", "Every thought leader reviews it."),
    ("forbidden_word", "One value-add for review."),
    ("forbidden_word", "A new paradigm for review."),
    ("forbidden_word", "A granular review path."),
    ("forbidden_word", "The deliverable is a review path."),
    ("forbidden_word", "Upskill the review team."),
    ("forbidden_word", "One touchpoint for review."),
    ("forbidden_word", "A disruptive review path."),
    ("forbidden_word", "Implementation excellence starts with review."),
    ("forbidden_word", "A transformative review path."),
    ("forbidden_word", "We leverage the review path."),
    ("forbidden_word", "The solution is one review path."),
    ("forbidden_word", "We optimize the review path."),
    ("forbidden_word", "We strategize the review path."),
    ("forbidden_word", "A proactive review path."),
    ("forbidden_word", "Our learnings from review."),
    ("forbidden_word", "Unpack the review path."),
    ("forbidden_word", "Unlock the review path."),
    ("forbidden_word", "At the end of the day the reviewer decides."),
    ("forbidden_word", "In terms of review, one owner decides."),
    ("forbidden_word", "It is important to note that one owner decides."),
    ("forbidden_word", "That being said, one owner decides."),
    ("forbidden_word", "Log it in order to review it."),
    ("forbidden_word", "Here's the thing about review."),
    # content-voice.md "Never use" punctuation and shapes.
    ("em_dash", "Ship the trail — then review it."),
    ("exclamation", "Review every request!"),
    ("question_marks", "Who owns it?? Nobody knows."),
    ("question_marks", "Who owns it? Who reviews it? Who closes it?"),
    ("tricolon_negation", "No dashboards. No agents. Just a trail."),
    ("prose_colon", "The question that changes every build: what do you prevent?"),
    ("prose_colon", "Three checks: source, owner, and outcome."),
    ("prose_colon", "Three checks: source, owner and outcome."),
    ("prose_colon", "Two checks: source and owner."),
    ("closing_when", "The owner reviewed every row.\n\nThe review worked when the owner signed it."),
    ("hashtag", "One owner reviews the trail. #AIImplementation"),
    # content-voice.md hard-banned hooks (Questions 2, 3, 5, and 7).
    ("banned_hook", "The best first AI project is intake review."),
    ("banned_hook", "Property AI gets useful at intake."),
    ("banned_hook", "Most AI projects do not fail because of models."),
    ("banned_hook", "Most SMBs do not need agents. They need owners."),
    ("banned_hook", "What most people miss is the owner."),
    ("banned_hook", "Here's the system for review."),
    ("banned_hook", "Here's what you need to do next."),
    ("banned_hook", "The results? Faster review."),
    ("banned_hook", "You're a moron if you skip review."),
    ("banned_hook", "This is an INSANE opportunity."),
    ("banned_hook", "DO NOT skip the review."),
    ("banned_hook", "Review EVERYTHING before launch."),
    ("banned_hook", "Take action before someone else does."),
    ("banned_hook", "It gets solved with a hire."),
    ("banned_hook", "Owners do not guess, they review."),
    ("banned_hook", "Would you trust an AI agent with rent?"),
    ("banned_hook", "I would trust it with the trail."),
    ("banned_hook", "Your inbox is probably a margin leak."),
    ("banned_hook", "The useful question is uglier than that."),
    ("banned_hook", "Make stuck work visible before you make replies faster."),
    ("banned_hook", "What did you build in September?"),
    ("noun_stack", "Urgency. Unit history. Vendor route."),
    ("numbered_list", "1. Source record\n2. Owner review"),
    ("slogan_pair", "Agents handle the work. You keep the margin."),
    ("slogan_pair", "Build the process. Buy back the time."),
    ("slogan_pair", "Consultants charge for advice."),
    ("slogan_pair", "Demo proves it's possible. Deploy proves it's real."),
    ("slogan_pair", "Specs live in decks. Systems live in production."),
    # content-rules.md and content-voice.md contrarian-setup bans.
    ("contrast_shape", "The blocker is not the model."),
    ("contrast_shape", "It isn't a model problem."),
    ("contrast_shape", "Owners don't guess."),
    ("contrast_shape", "Not speed but trust."),
    ("contrast_shape", "Review is not just a gate. It is the record."),
    ("contrast_shape", "The owner should be accountable, not the model."),
    ("contrast_shape", "The workflow needs an owner, not a dashboard."),
    ("contrast_shape", "The review should become a record instead of a meeting."),
    ("contrast_shape", "The risk is not the model. The risk is the handoff."),
    ("contrast_shape", "Not look what this tool can do, more like what it records."),
    ("importance_phrase", "Review matters more than people think."),
    ("importance_phrase", "People underestimate the review step."),
    ("importance_phrase", "That part matters."),
    # content-rules.md LinkedIn originality hard blocks.
    ("originality_block", "The least glamorous work is review."),
    ("originality_block", "A handoff everyone checks manually."),
    ("originality_block", "It gets risky when the records live in different places."),
    ("originality_block", "The records live in different places."),
    ("originality_block", "Add an exception layer."),
    ("originality_block", "That is where the risk lives."),
    ("internal_machinery", "Our autonomous content system drafts it."),
    ("internal_machinery", "Keep a state file for every run."),
    ("internal_machinery", "Add a stop condition before sending."),
    # content-rules.md internal-machinery prohibition.
    ("internal_machinery", "Mission Control ranks the queue."),
    ("internal_machinery", "OpenClaw runs the review."),
    ("internal_machinery", "Eve drafts the reply."),
    ("internal_machinery", "The content OS picks the post."),
    ("internal_machinery", "The Growth OS ranks it."),
    ("internal_machinery", "My outreach automation flags it."),
    ("internal_machinery", "The prospecting automation found them."),
    ("internal_machinery", "My job-search automation applied."),
    ("internal_machinery", "The job search pipeline ran."),
    ("internal_machinery", "Proof hygiene cleanup comes first."),
    ("internal_machinery", "The publishing machinery posts it."),
    ("internal_machinery", "The content-generation pipeline wrote it."),
    # content-voice.md Stop Slop delta.
    ("false_agency", "The data tells us to review it."),
    ("false_agency", "The market rewards review."),
    ("false_agency", "The workflow creates trust."),
    ("narrator_distance", "People tend to skip review."),
    ("narrator_distance", "Nobody designed this review path."),
    ("narrator_distance", "This happens because nobody owns review."),
    ("narrator_distance", "This is why review needs an owner."),
    ("vague_declarative", "The stakes are high for review."),
    ("vague_declarative", "The implications are significant."),
    ("vague_declarative", "The reasons are structural."),
    ("vague_declarative", "The consequences are real."),
    ("wh_opener", "What makes this hard is the handoff."),
    ("wh_opener", "Why this matters for owners."),
    ("wh_opener", "How teams should think about review."),
    ("pull_quote_ending", "One owner reviewed every row.\n\nThat's the lesson."),
    ("pull_quote_ending", "One owner reviewed every row.\n\nThat's the tradeoff."),
    ("pull_quote_ending", "Review is the new launch."),
    ("passive_voice", "The reply was generated overnight."),
    ("passive_voice", "Mistakes were made in review."),
    ("possible_secret", "Use token=abc123 for review."),
)

ALLOWED_EXAMPLES = (
    "ServiceNow's September 23 release says, \"INRY deploys ServiceNow EmployeeWorks in six weeks, "
    "replacing its legacy portal with an AI front door to work.\"",
    "I start with one employee request and follow it from intake through outcome.",
    "The review standard is whether one request can be traced from source context to a recorded outcome.",
    "That creates a precise operating question. Can the user trace an explanation to the record, date, "
    "and scope that produced it?",
    "I would keep four checkpoints visible. The source record. The selected metric and date. The generated "
    "explanation separated from source data. The user's review or correction.",
    "That is the trace I would ask a team to preserve before shipping personalized explanations.",
    "PUBLIC-EVIDENCE TEARDOWN",
    "AI PRODUCT CONTROL",
    "JT operator lens · Sep 29, 2026",
    "JT operator lens based on OpenAI release notes",
    "Proposed system based on public information",
    "Everything the reviewer saw stays in the record.",
    "Review starts at 10:30 each morning.",
    "The owner approves or rejects each request.",
    "Source record",
    "Human review",
)


class ContentPolicyTests(unittest.TestCase):
    def test_every_governed_hard_ban_is_rejected_with_its_rule(self) -> None:
        for rule, text in BANNED_EXAMPLES:
            with self.subTest(rule=rule, text=text):
                found = violations(text)
                self.assertIn(rule, {item.split(":", 1)[0] for item in found}, found)
                with self.assertRaisesRegex(ValueError, "prohibited public copy"):
                    require_public_copy(text, "post")

    def test_governed_fixture_copy_and_neutral_text_are_allowed(self) -> None:
        for text in ALLOWED_EXAMPLES:
            with self.subTest(text=text):
                self.assertEqual(violations(text), [])
                self.assertEqual(require_public_copy(text, "post"), text)

    def test_policy_applies_identically_to_every_public_surface(self) -> None:
        self.assertEqual(
            PUBLIC_SURFACES,
            ("post", "eyebrow", "title", "subtitle", "stage", "footer", "attribution", "alt"),
        )
        for surface in PUBLIC_SURFACES:
            for rule, text in BANNED_EXAMPLES:
                with self.subTest(surface=surface, rule=rule):
                    with self.assertRaisesRegex(ValueError, "{} uses prohibited public copy".format(surface)):
                        require_public_copy(text, surface)

    def test_unknown_surfaces_are_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "surface"):
            require_public_copy("Human review", "evidence")


if __name__ == "__main__":
    unittest.main()
