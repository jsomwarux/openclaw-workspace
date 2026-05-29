# Altmark Rent Delinquency Nonpayment Risk Check — 2026-05-28

Purpose: tighten the rent delinquency workflow test gate around official NYC nonpayment-process facts, without turning the workflow into legal advice or tenant-facing automation.

## Official Source Check

- NY Courts says a NYC nonpayment case is used to collect unpaid rent, and before the case starts the landlord must make a written rent demand warning that nonpayment can lead to eviction. The written demand must be delivered at least 14 days before the court case starts.
- NY Courts' landlord DIY program is limited and explicitly excludes rent-regulated premises outside the right context; Altmark should not rely on generic DIY-form assumptions for regulated/multi-unit property operations.
- NY Courts' eviction guidance separates rent demands, petitions, and notices of eviction. Tenant-facing or legal-status language must stay outside automation unless Altmark counsel/owner explicitly approves wording and timing.
- NY Courts says full payment before the case is heard can stop a nonpayment case from going forward, and payment before actual eviction can affect an issued warrant. The workflow should therefore treat recent payments and payment plans as hard manual-review exceptions.

Sources:
- https://www.nycourts.gov/new-york-city-housing-court/starting-nonpayment-case
- https://www.nycourts.gov/help/diy-forms/landlord-nonpayment-eviction-petition-written-rent-demand-program
- https://www.nycourts.gov/help/homes-evictions/being-evicted
- https://www.nycourts.gov/new-york-city-housing-court/stays-after-entry-judgment-nonpayment-proceeding

## Workflow Implications

1. Keep the workflow framed as an internal exception/review queue, not an eviction or legal-notice generator.
2. Add/verify flags for `written_demand_sent`, `demand_date`, `case_started`, `notice_of_eviction`, and `payment_received_after_report_date` only as internal review context if Altmark provides them.
3. Default any record with legal status, pending case, prior demand, notice of eviction, dispute, payment plan, recent payment, credit/prepayment, or unclear balance to manual review.
4. Do not generate tenant-facing text that references eviction, rent demand, court, warrant, marshal, sheriff, or legal deadlines unless Altmark provides approved language and scope.
5. Acceptance testing should prove that a stale delinquency report cannot push a recently paid or legally sensitive account into a normal outreach queue.

## Test Gate Additions

- Legal/process-sensitive account with prior demand or case status -> manual review, no draft outreach.
- Payment after report date -> manual review or exclusion until Altmark confirms the live balance.
- Notice/court terminology present in input notes -> manual review with reason `legal_process_sensitive`.
- Missing demand/case status fields -> do not block basic exception reporting, but block any tenant-facing draft generation.

## Reusable Pattern

For property-ops automation, the risk is not "can we draft the message?" The risk is whether the source data and legal/process context are current enough to decide that a message should exist at all. The durable implementation pattern is: ledger validation first, legal/process-sensitive exception routing second, owner approval third, tenant-facing output last.
