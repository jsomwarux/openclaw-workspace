# Built OpenClaw Skill Audit Agent OS Draft

## Draft

I built my OpenClaw workspace around installed skills, so I audited that skill layer today after a ClawHub supply-chain advisory.

That is the layer below the agent conversation.

The review covered:

Two skill directories.
Shell execution patterns.
Network calls.
Credential-touching commands.
Install-on-load behavior.
External execution.

I filtered out vendored dependency noise so the review stayed focused on code the system could actually trust during scheduled work.

Result:

No unexpected SSH access.
No credential-harvesting patterns.
No install-on-load behavior.
No suspicious external-network execution.
No hidden AppleScript or local automation surprise.

This is one of the least glamorous parts of building an AI operating system, but it is the part that makes the rest usable.

If an agent can schedule work, call tools, read client context, or touch production workflows, the trust boundary is bigger than the prompt.

You need to know:

What skills are installed.
Who can change them.
Which tools they can invoke.
What credentials they can reach.
What gets logged when something changes.
What requires human approval before execution.

The goal is not to make AI feel impressive in a demo.

The goal is to make repeated work inspectable, governed, and boring enough to trust.

## Review Notes

- Date: 2026-06-24
- Status: Review
- Lane: Trust/proof
- Proof source: `memory/audits/security/clawhub-skill-supply-chain-audit-2026-06-24.md`
- Intended use: LinkedIn proof/trust post after review.
- Avoid pairing with today's Salesforce/run-control post; this is a separate security and governance angle.
