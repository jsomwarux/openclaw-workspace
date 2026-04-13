# Runbook Skill — Handoff
Built: 2026-04-12

## What was built
A diagnostic skill that helps JT (or Eve) debug operational issues quickly using a structured 5-step protocol.

## Files created
- skills/runbook/SKILL.md

## How to use it
Trigger: "debug this", "why is X broken", "how do I fix [error]"
JT can ask mid-session or during a heartbeat.

## What to test
1. Ask "why is Telegram not delivering messages" — should give provider in cooldown diagnosis
2. Ask "why is the gateway unreachable" — should give Convex diagnosis steps
3. Ask "debug this: provider in cooldown" — should walk through 5-step protocol

## v2 ideas
1. Add more patterns based on actual errors that come in
2. Add severity levels (critical/medium/low) with escalation path
3. Add automated checks: when pattern matches, auto-run the investigation command and return results
