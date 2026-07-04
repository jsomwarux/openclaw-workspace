# July 2026 Clock

## Source Status
1. `references/referral_engine_output.md`: present. Source file is `jt_outbound_v2_jul2026---67d33402-5a04-4cdc-b60d-7fe459f814e8.md`.
2. `references/execution_plan_output.md`: missing. Exact file was not present in inbound media or workspace search as of 2026-07-03 20:51 EDT. Any clock items unique to that absent file are a flagged gap, not reconstructed.
3. `references/eve_mandate_jul2026.md`: present. Used only to add mandate escalation gates that Phase 1 explicitly installed.

## Clock Entries
1. Property sequence, day 1 email M1.
   Condition: launch a property-management prospect sequence.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: confirm-sent required. JT may have executed day-1 sends. No redraft produced.

2. Property sequence, day 2 LinkedIn connection request.
   Condition: day 1 property email has launched.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: queued after day-1 sent confirmation.

3. Property sequence, day 4 LinkedIn DM if connected.
   Condition: LinkedIn connection accepted after property sequence launch.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: gated by connection acceptance.

4. Property sequence, day 5 email M2.
   Condition: property sequence launched and day 5 arrives.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: queued after day-1 sent confirmation.

5. Property sequence, day 10 email M3.
   Condition: property sequence launched and no earlier stop condition has fired.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: queued after day-1 sent confirmation.

6. Property sequence, day 18 breakup email.
   Condition: property sequence launched, no reply, no stop condition.
   Source section: referral_engine_output.md, Section 3, Sequence A.
   Current state: queued after day-1 sent confirmation.

7. Trades sequence, day 1 email M1.
   Condition: launch a trades prospect sequence.
   Source section: referral_engine_output.md, Section 3, Sequence B.
   Current state: confirm-sent required. JT may have executed day-1 sends. No redraft produced.

8. Trades sequence, day 4 phone call.
   Condition: trades day-1 email sent.
   Source section: referral_engine_output.md, Section 3, Sequence B.
   Current state: queued after day-1 sent confirmation.

9. Trades sequence, day 8 email M2.
   Condition: trades sequence launched and no earlier stop condition has fired.
   Source section: referral_engine_output.md, Section 3, Sequence B.
   Current state: queued after day-1 sent confirmation.

10. Trades sequence, day 15 breakup email.
    Condition: trades sequence launched, no reply, no stop condition.
    Source section: referral_engine_output.md, Section 3, Sequence B.
    Current state: queued after day-1 sent confirmation.

11. Stop rule: full sequence with no reply.
    Condition: any prospect completes the full applicable sequence with no reply.
    Source section: referral_engine_output.md, Section 3, Stop rules.
    Current state: active rule, no deletion performed.

12. Stop rule: email bounced plus no connection accept within 7 days.
    Condition: bounced email and no LinkedIn connection acceptance within 7 days.
    Source section: referral_engine_output.md, Section 3, Stop rules.
    Current state: active rule, no deletion performed.

13. Variant-change brake.
    Condition: message testing is underway.
    Source section: referral_engine_output.md, Section 3, Stop rules.
    Current state: active rule. Maximum one message-variant change per week.

14. Proof asset 1: COI Compliance Autopilot proof pack.
    Condition: artifact stack execution begins.
    Source section: referral_engine_output.md, Section 4, Build these three in order.
    Current state: queued first. Do not build extra assets before the three approved assets.

15. Proof asset 2: Job Status Dashboard pack.
    Condition: Asset 1 exists.
    Source section: referral_engine_output.md, Section 4, Build these three in order.
    Current state: queued second and requires Gil permission.

16. Proof asset 3: Arrears Follow-up one-pager.
    Condition: Assets 1 and 2 exist.
    Source section: referral_engine_output.md, Section 4, Build these three in order.
    Current state: queued third. Honest status only: currently deploying at the same Bronx firm.

17. Day-1 send block: baseline and deliverability audit.
    Condition: first 72-hour execution window opens.
    Source section: referral_engine_output.md, Section 8, Immediate Next 72 Hours.
    Current state: confirm-sent or confirm-done required. No redraft produced.

18. Day-1 send block: permission and referral asks.
    Condition: first 72-hour execution window opens.
    Source section: referral_engine_output.md, Section 8, Immediate Next 72 Hours.
    Current state: confirm-sent required for Yair, Gil, Karen, and Sam Foy asks. No redraft produced.

19. Day-1 send block: build the COI proof pack.
    Condition: first 72-hour execution window opens and approved artifact stack is active.
    Source section: referral_engine_output.md, Section 8, Immediate Next 72 Hours.
    Current state: queued. JT records Loom. Agent builds one-pager and page only when directed within approved scope.

20. Day-1 send block: rebuild the list.
    Condition: first 72-hour execution window opens.
    Source section: referral_engine_output.md, Section 8, Immediate Next 72 Hours.
    Current state: queued. Target is 40 NYC PM firms passing binary gates.

21. Day-1 send block: launch week one.
    Condition: list and proof/channel prerequisites are ready.
    Source section: referral_engine_output.md, Section 8, Immediate Next 72 Hours.
    Current state: confirm-sent required for first 15 M1 emails if JT has already executed any. No redraft produced.

22. Weekly Friday review.
    Condition: Friday review slot arrives.
    Source section: referral_engine_output.md, Section 7, Weekly review.
    Current state: active clock. Review sends versus target first, then funnel rates, then one logged change maximum.

23. Variant sample-size gate.
    Condition: reviewing a message variant.
    Source section: referral_engine_output.md, Section 7, Signal thresholds.
    Current state: active rule. Never judge a message variant under 30 sends.

24. Channel sample-size gate.
    Condition: reviewing a channel.
    Source section: referral_engine_output.md, Section 7, Signal thresholds.
    Current state: active rule. Never judge a channel under 100 touches.

25. Healthy views and zero replies diagnostic.
    Condition: 50 sends show healthy views but zero replies.
    Source section: referral_engine_output.md, Section 7, Diagnostics.
    Current state: active trigger. Diagnose offer or CTA problem.

26. Near-zero views diagnostic.
    Condition: artifact views are near zero.
    Source section: referral_engine_output.md, Section 7, Diagnostics.
    Current state: active trigger. Fix visibility plumbing, not copy.

27. Low-reply diagnostic.
    Condition: under 2 percent replies at 100 clean touches.
    Source section: referral_engine_output.md, Section 7, Diagnostics.
    Current state: active trigger. Change offer or ICP, not adjectives.

28. Referral gate opening.
    Condition: Altmark delivery proof is clean enough after acceptance for a specific warm-intro ask.
    Source section: eve_mandate_jul2026.md, Section 6, Escalate immediately.
    Current state: active escalation gate.

29. Altmark day-10 condition.
    Condition: Altmark day-10 condition occurs in the approved July plan.
    Source section: eve_mandate_jul2026.md, Section 6, Escalate immediately.
    Current state: active escalation gate. Specific source details are in missing `execution_plan_output.md`, so exact trigger text is a gap.

30. Altmark day-17 condition.
    Condition: Altmark day-17 condition occurs in the approved July plan.
    Source section: eve_mandate_jul2026.md, Section 6, Escalate immediately.
    Current state: active escalation gate. Specific source details are in missing `execution_plan_output.md`, so exact trigger text is a gap.

31. MSI stall condition.
    Condition: two ignored follow-ups plus 14 days of silence.
    Source section: eve_mandate_jul2026.md, Section 6, Escalate immediately.
    Current state: active escalation gate.

32. Day-15 cash threshold.
    Condition: day-15 cash threshold is reached or missed.
    Source section: eve_mandate_jul2026.md, Section 6, Escalate immediately.
    Current state: active escalation gate. Exact cash threshold amount is a gap unless present in missing `execution_plan_output.md`.

33. Thread stale at 7 or more days.
    Condition: any relevant thread is 7 or more days stale.
    Source section: eve_mandate_jul2026.md, Section 4 and Section 6.
    Current state: active flag.

34. Kill window closing within 48 hours.
    Condition: any registered kill window closes within 48 hours.
    Source section: eve_mandate_jul2026.md, Section 4.
    Current state: active flag.

35. Job brake exceeded twice in one week.
    Condition: any job exceeds its brake twice in one week.
    Source section: eve_mandate_jul2026.md, Section 6.
    Current state: active escalation gate.

## Gaps
1. `references/execution_plan_output.md` is missing, so any dated chase, gate, kill window, or trigger unique to that document cannot be verified.
2. The exact Altmark day-10 and day-17 condition text is not present in the saved reference set.
3. The exact day-15 cash threshold amount is not present in the saved reference set.
4. Current sent status for possible day-1 send-block items is unverified. Each is marked confirm-sent rather than redrafted.
