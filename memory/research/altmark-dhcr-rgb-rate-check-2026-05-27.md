# Altmark DHCR RGB Rate Check — 2026-05-27

## Why This Matters
Altmark's DHCR Lease Renewal Automation needs a configurable rate layer before generating RTP-8 renewal forms. The current kickoff sheet already blocks hardcoded RGB rates; this note pins the official current source for Phase 1 kickoff.

## Verified Source
- NYC Rent Guidelines Board Apartment/Loft Order #57
- URL: https://rentguidelinesboard.cityofnewyork.us/2025-26-apartment-loft-order-57/
- Scope: apartment and loft leases commencing from 2025-10-01 through 2026-09-30
- Apartment renewal adjustments:
  - 1-year lease: 3.0%
  - 2-year lease: 4.5%

## Implementation Notes
- Store RGB rate rows with `effective_start`, `effective_end`, `lease_term`, `rate_percent`, and `source_url`.
- Do not calculate renewals from a single global percentage.
- Route any lease commencement date outside 2025-10-01 through 2026-09-30 to exceptions until the applicable order is configured.
- Keep preferential-rent units excluded from Phase 1 as already scoped.

## Client Prompt
Ask Matt/Yair to confirm whether all Phase 1 legal-rent renewals have commencement dates inside the Order #57 window. If not, collect the applicable windows before build.
