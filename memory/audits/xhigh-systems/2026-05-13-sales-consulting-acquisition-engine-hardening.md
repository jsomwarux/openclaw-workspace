# XHigh Hardening — Sales / Consulting Acquisition Engine

Date: 2026-05-13
Scope: targeted A+ hardening after `memory/audits/xhigh-systems/2026-05-13-sales-consulting-acquisition-engine.md`.

## Before Grade

**A-.**

The engine was coherent after the first audit, but the next outcome was still split across multiple lanes: Altmark proof/referral gate, property/family-office diagnostic packaging, AI Ops Teardown review/post, Guyana intro ask, and Strategy Jobs Pack first use.

The blocker was not strategy. The blocker was making the best unblocked proof-led move executable enough that JT could act without choosing between five assets.

## After Grade For Internal Controllables

**A.**

Internal controllables are hardened: the next proof-led acquisition move is now a single packet, Drive-backed, MC-prioritized, proof-gated, and tied to the existing diagnostic one-pager.

Still **not A+ overall** because the external outcome gate remains open. A+ requires one real warm/proof-led outcome: Altmark acceptance/proof, Yair referral ask after the gate clears, first diagnostic call, 2+ qualified Guyana intros, or AI Ops Teardown posted with CTA.

## Best Next-Action Packet Created

Created the canonical unblocked acquisition packet:

- Local source: `memory/consulting/proof-led-acquisition-packet-2026-05-13.md`
- Drive copy: https://docs.google.com/document/d/1_cGThUQDgDyfGJnQ1swfA2vO7JAxo0lQkddvQF6mga8/edit

Packet includes:

- recommended LinkedIn AI Ops Teardown post
- CTA comment linking to diagnostic one-pager
- DM/reply script if someone asks what this looks like
- warm-referrer “who is this for?” language
- explicit proof-safe claims allowed/avoided
- JT review checklist before posting
- gate reminder that Yair referral ask waits for Altmark proof/acceptance/payment clarity

Rationale: Yair referrals are correctly blocked until Altmark gates clear. The property insurance expiration teardown is the cleanest unblocked A+ path because it is anonymized, buyer-relevant, and points directly to the diagnostic CTA.

## Files Changed

1. `memory/consulting/proof-led-acquisition-packet-2026-05-13.md`
   - New canonical packet for the proof-led acquisition move.

2. `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`
   - Added proof-safe insurance/COI expiration example.
   - Added source/status block with Drive copy, hidden page, and proof gate.
   - Call-ready Drive copy: https://docs.google.com/document/d/1LLX37Pc5MRUCD-jRKjm48Mj_XbPmnDHAis4VaR4ffhI/edit

3. `memory/consulting/offer-asset-index-2026-05-13.md`
   - Added local and Drive references for the acquisition packet.
   - Added call-ready one-pager Drive copy.
   - Added acquisition packet update and A+ gate.

4. `memory/north-star/consulting-sales-engine.md`
   - Added hardening note: next unblocked JT action is review/post the AI Ops Teardown and log the URL.

5. `memory/north-star/proof-distribution-engine.md`
   - Added proof-led acquisition packet note and guardrail against named Altmark/ROI claims.

## Mission Control Tasks Changed

- **Completed:** `Property/Family Office: package diagnostic as call-ready one-pager`
  - Status set to `done`.
  - Description updated with source path, Drive link, and SHIP-for-JT-review checklist result.

- **Reprioritized/rewrote:** `AI Ops Teardown: review/post property insurance expiration LinkedIn draft`
  - Sort order moved to `3`.
  - Description now points to the packet and Drive copy.
  - Done state now requires posted URL logged and replies routed to diagnostic one-pager.

- **Rewrote:** `Strategy Jobs Pack: pick the first real send/use`
  - Recommendation now clearly says use the proof-led acquisition packet first.
  - Yair referral ask remains blocked until Altmark acceptance/payment/proof clarity.

Preserved existing proof gates:

- `Altmark: lock PC handoff + acceptance/payment clarity` remains high priority at sort `2`.
- `Altmark: ask Yair for 2–3 family-office intros after acceptance` remains blocked/gated.
- `Guyana: ask dad/family network for supplier/operator intros` remains warm-intro validation only.

## Validation

Commands/checks run:

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 scripts/drive_drafts.py --title "Property Family Office AI Operations Diagnostic — Call-Ready One-Pager 2026-05-13" --path "Consulting/Offers/Property Family Office AI Operations Diagnostic" --file memory/consulting/family-office-ai-ops-diagnostic-one-pager.md
python3 scripts/drive_drafts.py --title "Proof-Led Acquisition Packet — Property Family Office AI Ops 2026-05-13" --path "Consulting/Offers/Property Family Office AI Operations Diagnostic" --file memory/consulting/proof-led-acquisition-packet-2026-05-13.md
python3 -m py_compile scripts/drive_drafts.py
curl /api/tasks verification via Python urllib
file existence + explicit key-prefix scan
```

Results:

- Bootstrap sizes at start: AGENTS 27,013; MEMORY 19,019; TOOLS 13,947; HEARTBEAT 15,014.
- Drive uploads succeeded and returned Google Doc links.
- MC task updates returned `{"success":true}`.
- Verified key task states after update:
  - AI Ops Teardown task: `todo`, high, sort `3`.
  - One-pager packaging task: `done`, high.
  - Strategy Jobs Pack task: `todo`, high, sort `4`.
  - Altmark clarity task: `todo`, high, sort `2`.
  - Yair referral task: still gated.
  - Guyana family-network task: still validation-only.
- No explicit secret prefixes (`sk-or-v1`, `sk-ant-`, `Bearer`) found in changed files.
- `scripts/drive_drafts.py` compiles.

## External Blockers

1. **AI Ops Teardown not posted yet.** JT must review/post and log the URL.
2. **Altmark gate not cleared yet.** PC handoff, acceptance/payment clarity, proof capture, and rent-delinquency deposit/data readiness remain prerequisites before Yair intro ask.
3. **Yair referral ask still blocked.** Correctly preserved.
4. **Guyana still validation-only.** Needs real named intros before demo/prospect buildout.
5. **A+ outcome not achieved yet.** Internal execution is ready, but an external proof/warm-path event has to happen.

## Recommendation

Use this order:

1. Lock Altmark handoff/acceptance/payment clarity.
2. Post the property insurance expiration AI Ops Teardown with the diagnostic CTA.
3. Route replies to the Property / Family-Office AI Operations Diagnostic one-pager.
4. Ask Yair for 2–3 qualified intros only after Altmark gates clear.

## Report Path

`/Users/jtsomwaru/.openclaw/workspace/memory/audits/xhigh-systems/2026-05-13-sales-consulting-acquisition-engine-hardening.md`
