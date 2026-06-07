# Passive Income Strategist Report - 2026-06-07

## Status
Status: COMPLETE under graceful-degradation policy.

The scout report was regenerated successfully and contains no failure marker. Stale local inputs were treated as DEGRADED evidence, not a reason to stop. No Telegram message was sent.

## Executive Decision
BUILD: 1
WATCH: 4
PASS: 1

Top recommendation: BUILD `ChargeTrip Fit`, a narrowed version of the 2026-05-31 `ChargeReady Rank` idea. The May version was WATCH because broad charger rankings were too competitive and accuracy-heavy. The June rerun improves the thesis by constraining the product to renter/outlet/trip compatibility reports, which is more defensible and easier to build as a rules engine.

## Evidence Caveats
- `weekly-exploding-topics.md` and `weekly-apis.md` were fresh as of 2026-06-06.
- `weekly-trends.md`, `weekly-google-trends.md`, and TrustMRR files were DEGRADED by age and used only directionally.
- Fresh web checks were bounded to 7 calls through `scripts/web_search.py`.
- TrustMRR revenue figures are directional, self-reported/listed, and not audited.

## Verdict Summary
| Idea | Verdict | Score | Reason |
|---|---|---:|---|
| ChargeTrip Fit | BUILD | 7.5 | Specific compatibility anxiety, fresh EV charger signal, affiliate path, and a narrow rules-engine MVP. |
| BuilderGel Guard | WATCH | 7.0 | Strong beauty demand and fear trigger, but allergy/medical language and overlap with ClaimRisk Cards require caution. |
| MicroAirFit | WATCH | 6.8 | Useful appliance decision engine with affiliate path, but SERP/review competition is heavy. |
| DogEarProof | WATCH | 6.7 | Real pet-owner demand, but medical-adjacent triage and vet disclaimers lower passive autonomy. |
| DocsPulse Lite | WATCH | 6.6 | Revenue-pattern support and agent-readiness angle, but integrations make it consulting-adjacent rather than passive. |
| CeylonCheck | PASS | 5.6 | Strong search volume, but health/safety claims and commodity affiliate competition cap the opportunity. |

## Saturation and Duplicate Filter
| Idea | Filter Result |
|---|---|
| ChargeTrip Fit | Prior 2026-05-31 `ChargeReady Rank` was WATCH, not queued. This is a narrowed promotion, not a duplicate Mission Control task. |
| BuilderGel Guard | Adjacent to `ClaimRisk Cards`, already queued. Keep separate only if it becomes a product/lamp compatibility checker. |
| MicroAirFit | Broad appliance reviews are saturated. Keep as WATCH unless the calculator proves materially better than listicles. |
| DogEarProof | Pet affiliate SEO is crowded. Needs breed/ear-profile and vet-threshold specificity. |
| DocsPulse Lite | Notion analytics and wiki alternatives exist. Best wedge is agent-readiness and stale-grounding risk. |
| CeylonCheck | Wellness affiliate and health-content competition are too high for a build recommendation. |

## Build Blueprint: ChargeTrip Fit

### 1. Opportunity
New EV owners, renters, and road-trip planners are making a high-anxiety purchase under confusing constraints: NACS vs. J1772, NEMA outlet type, amperage, indoor/outdoor use, cable length, adapter needs, and landlord/electrician constraints. Generic charger reviews do not answer "what works for my parking setup?"

### 2. Product
One-page questionnaire plus ranking output:
- Vehicle make/model/year and plug standard.
- Home outlet type or "I do not know."
- Renter/homeowner and parking distance.
- Indoor/outdoor/weather exposure.
- Target use: emergency backup, nightly charging, road trip kit, dryer-outlet sharing.
- Budget and safety preference.

Output:
- 3 ranked charger/adapter recommendations.
- Compatibility warnings and conservative safety caveats.
- "Do not buy if..." section.
- Optional outlet/photo checklist.
- Affiliate links and a $7 downloadable fit report.

### 3. MVP Scope
Week 1:
- Build static Next.js or Astro site with questionnaire and rules engine.
- Seed 25-40 products: portable Level 1/Level 2 chargers, adapters, extension-safe warnings, smart splitters, cable organizers.
- Create core rule table for NEMA 14-50, 14-30, 6-50, 5-15, J1772, NACS adapters, amperage limits, outdoor rating, and cable length.

Week 2:
- Add affiliate links.
- Add 20 pSEO pages: "best portable EV charger for apartment renters", "NEMA 14-30 EV charger fit", "Tesla renter charging kit", "portable EV charger for road trips", and similar.
- Add $7 report checkout only after free questionnaire works.

### 4. Autonomous Marketing
- Weekly product/spec refresh agent checks charger pages and price changes.
- pSEO pages target outlet/vehicle/use-case combinations.
- Short-form content: "Do not buy a portable EV charger before checking this outlet" and "renter EV charging kit mistakes."
- Agent-readable JSON output can later be exposed as a small API for car-buying or road-trip agents.

### 5. Monetization
- Primary: affiliate revenue on chargers, adapters, splitters, and accessories.
- Secondary: $7 personalized compatibility report.
- Optional: $19/year recall/spec-change watchlist once traffic exists.

### 6. Risks and Guardrails
- Safety risk: every answer must say when to consult an electrician.
- Product liability: do not claim electrical approval; provide compatibility education.
- Data freshness: keep rules simple and auditable.
- Competition: avoid generic "best charger" pages; win on questionnaire utility.

### 7. Scorecard
| Dimension | Score |
|---|---:|
| Demand | 8.0 |
| Urgency | 8.1 |
| Build simplicity | 7.3 |
| Autonomy | 7.2 |
| Monetization | 7.1 |
| Uniqueness | 7.0 |
| Competition resistance | 6.4 |
| JT stack fit | 8.0 |
| Overall | 7.5 |

## Watch Ideas

### BuilderGel Guard - WATCH, 7.0
Strong buyer fear and huge beauty search volume. The correct implementation is a conservative product/lamp compatibility checker with HEMA/acrylate disclaimers, not allergy advice. Watch trigger: `ClaimRisk Cards` gets scoped and this can either merge into it or become a label-safety subtool.

### MicroAirFit - WATCH, 6.8
The compact-kitchen appliance problem is real, and affiliate conversion could work. The issue is competition from review sites. Watch trigger: find 20 high-intent long-tail queries where a calculator beats generic reviews, such as dorm-safe wattage, small counter dimensions, or family-size frozen-food use cases.

### DogEarProof - WATCH, 6.7
Pet owners want maintenance answers, and dog ear cleaner has good signal. The product must stay clear of diagnosing infections. Watch trigger: identify a breed-specific content cluster with low competition and a vet-reviewed disclaimer template.

### DocsPulse Lite - WATCH, 6.6
This has the best B2B logic but the weakest passive-income fit. It may be stronger as consulting proof around AI context quality and stale grounding. Watch trigger: one client or prospect asks how to keep SOPs/knowledge bases agent-ready.

## Pass Idea

### CeylonCheck - PASS, 5.6
Ceylon cinnamon demand is real, but the product is too close to health-content liability and commodity affiliate SEO. Keep as a content idea only if it can be framed as label education without dosage, therapeutic, or safety claims.

## Mission Control Action
Duplicate check: no existing Mission Control task matched `ChargeTrip`, `ChargeFit`, `EVCharge`, `portable EV`, `NEMA`, `Level 2 charger`, or `EV charger` before this report's task creation step.

Action required: create one `[PI]` task for `ChargeTrip Fit` if the board still has no duplicate at task-write time.

## Final Recommendation
Build `ChargeTrip Fit` only as a spec-first passive-income experiment. The first artifact should be a rules table and questionnaire, not a full app. If the rules cannot be made conservative and easy to audit in one sitting, demote it back to WATCH and do not spend build time.
