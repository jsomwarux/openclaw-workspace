# Passive Income Strategist Report — March 15, 2026

**Run time:** 11:18 AM ET  
**Ideas evaluated:** 6  
**Passed saturation filter:** 6  
**🟢 BUILD THIS:** 5 (FITBRIEF AI, GYMLORE, FANDOMDROP, TRADIECOMMS, CULTUREFIT NUTRITION)  
**🟡 WATCH:** 1 (RECIPE RANKINGS)  
**🔴 PASS:** 0

---

## Saturation Filter Results

| Idea | Saturation Check 1 (passive income lists) | Saturation Check 2 (Reddit 200+ upvote thread) | Result |
|---|---|---|---|
| FITBRIEF AI | No results — concept not in any passive income list | Reddit "personal trainer AI" threads all focus on workout delivery to clients, not trainer business comms | ✅ PASSES |
| GYMLORE | No results — gym ranking directory not suggested as passive income | Reddit threads show only informal "best BJJ gym in [city]" posts with no authoritative resource | ✅ PASSES |
| FANDOMDROP | "AI + POD" is generic but the hyper-niche fandom inside-joke storefront generator is absent | Reddit POD threads discuss generic t-shirts/coloring books, not fandom-specific lore-aware AI design | ✅ PASSES |
| TRADIECOMMS | Generic "AI writing tool" appears in lists; trades-specific post-job comms does not | Reddit r/skilledtrades AI thread focuses on estimating/scheduling, not client follow-up writing | ✅ PASSES |
| CULTUREFIT NUTRITION | "Meal planning app" is in every list; cultural + precision nutrition constraint intersection is absent | Zero Reddit threads on cultural + macro intersection as passive income idea | ✅ PASSES |
| RECIPE RANKINGS | "Recipe blog" and "recipe site" dominate passive income lists; AI curation/ranking angle is absent | Zero high-upvote threads recommending recipe ranking as passive income | ✅ PASSES |

All 6 ideas passed the saturation filter. Full deep analysis below.

---

## FITBRIEF AI

**Verdict:** 🟢 BUILD THIS | Score: **7.5/10**

### 1. The Opportunity
Solo personal trainers are running $50K–$100K+ businesses out of Google Docs and WhatsApp. Every existing platform (Trainerize, PT Distinction, Mindbody) is built to deliver workouts TO clients — none of them solve the business communication overhead that keeps trainers chained to their phones at 9PM drafting check-in messages. FitBrief AI becomes the AI that handles all the written work trainers hate: weekly progress reports, personalized check-in messages, invoice follow-ups, testimonial requests, and social posts celebrating client wins. The trainer sets up each client once; the AI runs the relationship management layer forever. This works in 3–5 years because ~350,000 certified trainers in the US will always need to communicate with clients, and the online coaching market is growing, not shrinking. The AI angle makes per-trainer personalization at scale economically viable for the first time.

### 2. Positioning for Profit
- **Smartest niche**: Solo online coaches (not gym-based trainers) running 10–30 clients remotely. They feel the comms overhead most acutely — no staff, no admin, 100% on them.
- **Defensibility**: Client data (goals, history, personality) entered once becomes the context layer for all future communications. The longer a trainer uses FitBrief, the more personalized the output — creating switching friction over time. Data flywheel: every message sent improves the model's understanding of what "sounds like you" vs. generic AI copy.
- **What beginners get wrong**: They build another full-stack coaching platform. The market doesn't need another Trainerize. It needs a lightweight tool that slots INTO whatever system trainers already use. FitBrief does one thing: drafts professional communications from a client description. No calendars, no payment processing, no workout builder.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Claude API + a single form interface (Next.js, deployed on Vercel). Trainer enters: client name, this week's progress notes, communication goal (check-in / progress report / testimonial request). Claude outputs the copy. That's the MVP.
- **Minimum viable version**: No accounts, no saved client data, no automation — just the copy generator. Charge $39/mo after a 7-day free trial. Add client data storage in Week 3.
- **Key tools**: Claude Sonnet (copy generation, zero marginal cost at JT's usage tier), Next.js + Vercel (frontend), Stripe (billing), Replit for rapid iteration.

### 4. Monetization
- **How first dollar comes in**: Trainer signs up for free trial via a Reddit post in r/personaltraining. Trial ends → Stripe subscription at $39/mo. Target Day 14 as first revenue event.
- **Pricing model**: $39/mo base (unlimited client profiles, all communication types). $79/mo Pro (automated weekly check-in scheduling via email/WhatsApp, milestone email sequences, social post calendar). Annual: $349 (saves 2 months).
- **Path to $3K–$10K/month**: 80 trainers × $39 = $3,120/mo. At 2 new trainers/week from Reddit/Facebook groups + SEO, reach 80 in 10 months. 250 trainers = $9,750/mo + upsell to Pro.

### 5. Automation Stack
- **What to automate first**: The scheduled check-in send. n8n workflow: every Monday at 9AM, pull client list → generate check-in draft per client → deliver to trainer's email for 1-click review + send. This transforms FitBrief from a generator into a system.
- **AI's role**: Claude handles all copy generation with a client-specific context prompt per trainer. No custom ML — just great prompting.
- **How ongoing time approaches zero**: After Month 2, the n8n workflow runs automatically. The trainer reviews drafts in 10 minutes/week (vs. 3+ hours of manual writing). JT's time: zero. The product runs itself.

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Coding agent builds MVP (form → Claude → copy output). Launch in r/personaltraining and 2 fitness Facebook groups. Target 10 paying trainers. Get qualitative feedback. Add client profiles.
- **Days 31–60 (Traction)**: Add automated check-in scheduling (n8n). Add 3 communication types (social post, testimonial request, review nudge). Post weekly value-add content in trainer communities. Target 30 paying trainers ($1,170/mo).
- **Days 61–90 (Scale)**: SEO content ("client check-in templates for personal trainers") starts ranking. Affiliate partnership with trainer directories. Target 80 paying trainers ($3,120/mo). Evaluate upsell Pro tier.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 7 | 8 | 6 | 8 | 8 | 8 |

**Weighted score: 7.5/10**

---

## GYMLORE

**Verdict:** 🟢 BUILD THIS | Score: **7.75/10** ← Top Pick

### 1. The Opportunity
Reddit is flooded with "best BJJ gym in [city]" posts — and every single one is met with scattered anecdotal responses, outdated 3-year-old opinions, or "just try a few." No authoritative gym discovery resource exists that is organized by training discipline (powerlifting, BJJ, muay thai, Olympic lifting, boxing) rather than generic proximity. GymLore fills this gap: AI-curated gym rankings by discipline and city, ingesting Reddit posts, Google Reviews, and community forums weekly. JT built this exact architecture twice already (Nash Satoshi 4-LLM ensemble, Glow Index skincare rankings). This is the third instance — incremental cost is near zero. The directory model works: Nomads.com ($15K/mo), BestPlaces — the formula is proven. In 3–5 years, passionate fitness communities (BJJ alone has 1.1M Reddit members) will still need authoritative local discovery that Google Maps structurally can't provide.

### 2. Positioning for Profit
- **Smartest niche**: Launch with BJJ (1.1M Reddit members, r/bjj, high engagement) and powerlifting (r/powerlifting, 400K+ members). These are the two disciplines where Google's results are worst and community opinion is most valued. Expand to muay thai, boxing, CrossFit after validation.
- **Defensibility**: Data flywheel — every new review, every new Reddit post ingested improves the ranking quality. SEO compounds over time as discipline + city long-tail queries start ranking (e.g., "best powerlifting gym Chicago" — currently zero good results). Gym owners claiming their listings creates a CRM relationship.
- **What beginners get wrong**: Building a "gym review site" that tries to cover everything from yoga studios to commercial gyms. GymLore wins by going deep on a specific discipline, not wide. The BJJ community will promote a definitive BJJ gym resource in a way they'd never promote a generic fitness directory.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Fork Nash Satoshi / Glow Index repo. Replace crypto/skincare data model with gym data model. Seed with 50 BJJ gyms across 10 major cities (NYC, LA, Chicago, Austin, SF, Miami, Boston, Seattle, Denver, Atlanta) from public Google data + Reddit mentions. Claude scores each gym on 5 dimensions (quality of instruction, competitive team, beginner-friendly, facility, value). Launch with a single-discipline (BJJ) focus.
- **Minimum viable version**: Static rankings. No user accounts. No claiming. Just the data — beautifully presented, searchable by city.
- **Key tools**: Nash Satoshi/Glow Index architecture (fork), Claude Sonnet (review synthesis + scoring), n8n (weekly Reddit + Google data ingestion), Next.js + Vercel, Cloudflare Browser Rendering (gym data scraping).

### 4. Monetization
- **How first dollar comes in**: A gym owner finds their listing, wants to update their description and add photos → "Claim your listing" → $29/mo premium listing. First revenue event targeted at Month 3 (after SEO starts bringing organic traffic).
- **Pricing model**: Free (all gym listings, rankings visible). Premium listing: $29/mo per gym (owner control of photos, description, response to reviews, analytics). Affiliate: Gymdesk ($50-100 CPA), Mindbody Gyms ($75-200 CPA), supplement affiliates for gym-adjacent products. Display ads at 50K+ monthly visitors.
- **Path to $3K–$10K/month**: 50 premium listings × $29 = $1,450/mo + $500/mo affiliate at modest traffic = $2K/mo by Month 6. 150 listings + $1,500 affiliate at 30K/mo traffic = $5,850/mo by Month 12.

### 5. Automation Stack
- **What to automate first**: Weekly data ingestion. n8n workflow: every Sunday at 3AM, crawl r/bjj, r/powerlifting, r/gyms for gym mentions by city → Claude scores sentiment and updates gym rankings → push deltas to DB. Zero manual data maintenance.
- **AI's role**: Claude synthesizes review language into structured scoring (1–10 per dimension), generates the "summary take" on each gym (1–2 sentences visible on listing), and flags data quality issues.
- **How ongoing time approaches zero**: Month 2, the ingestion is fully automated. Month 3, gym owners are emailing to claim listings (no active outreach needed). Steady state: 1–2 hours/month reviewing flagged data issues.

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Fork existing architecture. Build gym data model. Seed 200 BJJ gyms across 10 cities. Deploy on Vercel. Post in r/bjj: "I built a resource for finding BJJ gyms by city — roast it." Target 500 organic visitors.
- **Days 31–60 (Traction)**: Add powerlifting discipline. Set up automated weekly data ingestion. Submit site to gym directories and fitness blogs. Target 5K monthly visitors. First gym owner inquiries.
- **Days 61–90 (Scale)**: Add 3 more disciplines (muay thai, boxing, CrossFit). Launch "claim your listing" at $29/mo. Target 10 premium listings ($290/mo). Start affiliate linking to gym management software. Compound SEO from discipline + city queries.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 8 | 9 | 7 | 6 | 8 | 9 |

**Weighted score: 7.75/10**

---

## FANDOMDROP

**Verdict:** 🟢 BUILD THIS | Score: **7.55/10** ⚠️ *IP risk mitigation required — see below*

### 1. The Opportunity
Generic fan merch consistently underperforms. The market has already proven that super-fans will pay for identity-specific products — the problem is no tool exists that actually knows the lore. Existing AI merch tools (imagine.art Merch Maker, Pixelcut, starryai) take a generic prompt and generate a generic design. FandomDrop is different: Claude researches the specific fandom (plot moments, community memes, inside jokes, character relationships, famous quotes) and generates designs that resonate at the community level. Each "fandom store" is a unique shareable URL — fans post it in their Discord, their subreddit, their group chat. The distribution is baked into the product. Printful handles all fulfillment at zero inventory risk. In 3–5 years, new IP (games, anime, shows) launches constantly — the fandom pipeline never dries up. The key constraint is operating only in "fan-inspired" territory, not direct licensed character reproduction.

### 2. Positioning for Profit
- **Smartest niche**: Start with anime micro-fandoms (not mainstream like Demon Slayer — too much licensed merch competition). Target cult classics: Vinland Saga, Mushishi, Kaiba, Casshern Sins. These communities have passionate members, almost no official merch, and no competition for fan-inspired lore-specific designs. Second: obscure 2000s cult TV (The Wire inside jokes, Deadwood quotes, The Shield memes).
- **Defensibility**: The fandom knowledge base builds over time — every store generated adds to the system's understanding of what resonates in each community. The "shareable URL per fandom" creates a link graph that compounds SEO as fans share links.
- **What beginners get wrong**: Using AI image generation directly on licensed characters (Disney, Crunchyroll, etc.) and getting DMCA'd. FandomDrop's designs must be conceptual/symbolic — a "Vinland saga"-inspired minimalist Norse-warrior-with-farming-tools poster is defensible; a direct likeness of Thorfinn is not. Claude generates the brief; the artist stays on the right side of fan art doctrine.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Claude researches fandom lore for 5 seed fandoms → generates 8 design briefs per fandom → feeds briefs into DALL-E 3 or Flux via OpenRouter → outputs images → Printful API connects product listings → shareable store URL generated. That's the full MVP loop.
- **Minimum viable version**: 5 seed fandom stores. Static product catalog per store (no custom orders yet). Manual quality review before publishing. Drive traffic via posting each store URL in the respective community (r/anime, r/theWire, etc.).
- **Key tools**: Claude (lore research + design brief generation), Flux/DALL-E 3 via OpenRouter ($0.04/image at Flux pricing), Printful API (JT has POD knowledge), Next.js + Vercel, Stripe (product checkout via Printful embed or direct).

### 4. Monetization
- **How first dollar comes in**: A fan in r/VinlandSaga sees the store URL posted → clicks → orders a poster. Printful fulfills. First sale targeted at Day 7 (from community share of the seed store).
- **Pricing model**: $8–12 margin per item (t-shirt base $15 Printful → sell at $24; poster base $8 → sell at $18). No subscription. Pure per-transaction.
- **Path to $3K–$10K/month**: 200 active fandom stores × avg 15 sales/month × $10 margin = $30,000/mo at scale. Realistic near-term: 30 active stores × 10 sales/month = $3,000/mo by Month 6 if community seeding works. Volume is the key variable.

### 5. Automation Stack
- **What to automate first**: The fandom store generation pipeline. n8n workflow: fandom name input → Claude lore research → design briefs → image generation → Printful product creation → store URL output. Target: new fandom store live in 10 minutes with zero manual work.
- **AI's role**: Claude is the "lore intelligence layer" — it's what makes FandomDrop's designs feel authentic vs. generic. Without this layer, it's just another AI merch tool. With it, the designs are specific enough that fans share them organically.
- **How ongoing time approaches zero**: After the pipeline is automated, adding a new fandom is a 10-minute job (or fully automated via a community suggestion form). Steady state: moderate traffic to existing stores driving passive sales, new stores added weekly.

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Build pipeline (Claude → Flux → Printful). Launch 10 fandom stores. Post each URL in respective communities (be transparent — "I made fan-inspired merch for [fandom]"). Target 50 sales / $500 in margin.
- **Days 31–60 (Traction)**: Iterate on design quality based on community feedback. Add 20 more fandoms. Build a public "suggest your fandom" form (community-driven product development + word-of-mouth marketing). Target 200 sales / $2,000 margin.
- **Days 61–90 (Scale)**: Automate new fandom pipeline fully. Target 50+ active stores. Launch Pinterest + Reddit content strategy (fandom-specific posts with store links). Target 500 sales / $5,000 margin.

⚠️ **IP Risk Mitigation Required Before Launch**: Designs must be fan-inspired (symbolic, typographic, conceptual references) — not direct character likenesses. Use Claude to explicitly flag any design brief that crosses into licensed IP territory. Stick to anime with no US licensed merch deals (many older/obscure titles), cult TV with expired or limited merch licensing, and video game fandoms where fan merch is tolerated. Do not use character names in product titles for IP-sensitive properties.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 7 | 8 | 6 | 9 | 7 | 9 | 7 |

**Weighted score: 7.55/10**

---

## TRADIECOMMS

**Verdict:** 🟢 BUILD THIS | Score: **7.5/10**

### 1. The Opportunity
There are 7.5 million trade workers in the US — plumbers, HVAC technicians, electricians, landscapers — and their businesses run almost entirely on reputation. Google Reviews are make-or-break (one missed review request is a missed 5-star). Yet the business communication layer for these operators is a disaster: follow-up emails still typed from scratch, Google Review requests sent inconsistently or awkwardly, warranty letters non-existent, care tip follow-ups unheard of. Jobber, Housecall Pro, and ServiceTitan exist — but they're $49–$199/mo platforms built for complex job management. TraidieComms is a single-purpose tool: the tradesperson describes what they did, and Claude produces the professional post-job communication in seconds. No CRM. No scheduling. No complexity. Just the words they need, done. This problem compounds as Google Reviews become more critical for local service discovery and as customers increasingly expect professional follow-up.

### 2. Positioning for Profit
- **Smartest niche**: Solo HVAC technicians and plumbers doing residential service calls. They have high-ticket jobs ($300–$2,000 per call), where a Google Review is worth potentially $5,000 in referred business, but they're the least likely to have admin staff. The ROI argument is immediate and concrete.
- **Defensibility**: The more the tradesperson uses TraidieComms, the more it learns their communication style (voice customization over time). Templates that get edited become the baseline for the next generation. Not a hard moat, but sufficient for $29/mo stickiness.
- **What beginners get wrong**: Building a full CRM with job tracking, invoicing, and scheduling. The trades software market is full of "all-in-one" platforms that overwhelm solo operators. TraidieComms wins by being the simplest possible tool for the highest-ROI problem (getting Google Reviews and maintaining professional follow-up), priced where it's a no-brainer.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Two-input form: (1) "Describe the job you just completed" (free text) + (2) "What do you need?" (dropdown: Google Review Request / Follow-Up Check-In / Warranty Letter / Care Tips Message / Invoice Follow-Up). Claude outputs a professional, personalized message. That's the entire MVP. Deploy on Vercel.
- **Minimum viable version**: No accounts required for first 5 uses (friction-free trial). Email capture at use 3. $29/mo Stripe subscription after trial. Mobile-first design (trades work on phones).
- **Key tools**: Claude Sonnet (copy generation), Next.js + Vercel (frontend), Stripe (billing), optionally: Telegram bot interface as alternative (describe job via Telegram → get copy back instantly — zero frontend needed).

### 4. Monetization
- **How first dollar comes in**: Tradesperson in r/HVAC or r/Plumbing tries it for free → uses it 3 times → subscribes. Or: a trades-focused Facebook group post converts 5 subscribers. Target Day 10 as first revenue event.
- **Pricing model**: $29/mo (solo operator). $49/mo Team (2–3 technicians, shared templates). Annual: $249 (saves ~2 months). One-time usage optional: $4.99 for 10 message credits (for infrequent users — converts the "I don't need it every month" objection).
- **Path to $3K–$10K/month**: 104 users × $29 = $3,016/mo. At 3–4 new subscribers/week (from trades Reddit/Facebook groups + SEO for "HVAC follow-up email template"), reach 100 users in 6–7 months. 350 users = $10,150/mo.

### 5. Automation Stack
- **What to automate first**: A Telegram bot interface. Instead of a web form, the tradesperson texts the bot while still in the driveway: "Just finished an AC tune-up for Mike, super happy customer, wanted to give him a care tip email and a Google review request." Immediate professional copy response. Zero friction, zero app switching.
- **AI's role**: Claude generates all copy. A system prompt specific to the trade type (HVAC vs. plumbing vs. electrical) ensures trade-appropriate vocabulary and references.
- **How ongoing time approaches zero**: Telegram bot requires zero maintenance after setup. Web frontend on Vercel requires zero infrastructure work. Support volume expected low (the product is simple). Steady state: read Stripe reports, occasionally post in trades communities.

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Build MVP (web form + Telegram bot option). Post in r/HVAC, r/Plumbing, r/skilledtrades. Target 15 paying subscribers by Day 30. Collect feedback on most-used communication types.
- **Days 31–60 (Traction)**: Add 5 more communication templates based on feedback. Create SEO content ("best follow-up email for plumbers," "how to ask clients for Google reviews HVAC"). Target 40 subscribers ($1,160/mo).
- **Days 61–90 (Scale)**: Partner with 2–3 trades-specific Facebook groups (10K+ members each) for referral or sponsored posts. Build "before/after" examples gallery (anonymous — "Here's what a typical HVAC follow-up used to look like vs. what TraidieComms generates"). Target 100 subscribers ($2,900/mo).

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 8 | 9 | 5 | 7 | 8 | 7 |

**Weighted score: 7.5/10**

---

## CULTUREFIT NUTRITION

**Verdict:** 🟢 BUILD THIS | Score: **7.2/10** ⚠️ *Window narrowing — build within 60 days or pass*

### 1. The Opportunity
The US is 40% non-white and growing. Every AI meal planning tool defaults to Western/English cuisine. A Nigerian bodybuilder trying to hit 200g protein/day using egusi, suya, and jollof rice gets zero help from MyFitnessPal. A South Asian woman managing gestational diabetes using Indian food has no app. KaibiganGPT recently launched for Filipino meal plans — the window is open but competitors are entering. CultureFit Nutrition is the first AI tool that generates complete weekly meal plans with precise macro tracking using culturally authentic ingredients. The AI angle makes the intersection of "cultural authenticity + exact macro constraints" economically viable for the first time — a human dietitian can't cost-effectively build customized plans per cultural food tradition at scale. This is an intercept moment: diaspora communities with high disposable income are completely unserved by the precision nutrition market.

### 2. Positioning for Profit
- **Smartest niche**: South Asian diaspora first (Indian, Pakistani, Bangladeshi — 5M+ in the US, high disposable income, strong cultural food identity, large fitness-conscious community). Then West African (Nigerian, Ghanaian — 2M+ in US with strong fitness culture and cultural food pride). Filipino is the third (2M+ in US, KaibiganGPT is early but weak on precision macros).
- **Defensibility**: Cultural food database depth is the moat — a detailed, validated nutrition database for Nigerian ingredients (ugwu, ogbono, uda) is not easily replicated by generic AI. First-mover position in South Asian precision nutrition SEO is unclaimed.
- **What beginners get wrong**: Building a generic "supports many cuisines" meal plan tool. Competitors like ai-mealplan.com say they support diverse cuisines but the actual cultural specificity is superficial. CultureFit wins by going absurdly deep on 3 cultures — not barely covering 20.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Claude + a structured form: cultural background (dropdown: South Asian / West African / Filipino / etc.) + fitness/health goal + dietary constraint + macro targets. Claude generates a full 7-day meal plan using that cuisine's actual food vocabulary + a basic macro breakdown. Export to PDF. Charge $19 per plan.
- **Minimum viable version**: South Asian only. No database — Claude handles all cultural food knowledge natively (it's genuinely good at this). No user accounts. Pay-per-plan via Stripe. Simple landing page explaining the gap.
- **Key tools**: Claude Sonnet (meal plan generation — zero database needed at MVP), Stripe (one-time $19 payments), Next.js + Vercel (frontend + PDF generation via react-pdf).

### 4. Monetization
- **How first dollar comes in**: A diaspora fitness community post on Reddit (r/ABCDesis, r/NigerianFitness) or TikTok ("I used AI to build a South Asian meal plan that actually hits my macros — here's what it looks like"). Stripe payment at checkout. First revenue event targeted at Day 5.
- **Pricing model**: $19 per generated meal plan (one-time). $12/mo subscription for monthly updated plans (recurring revenue). Annual: $99. Upsell: $39 "consult-style" plan (includes cultural substitution guide + 3-month progression template).
- **Path to $3K–$10K/month**: $19 plan × 160/month = $3,040 (plus subscription converts). Or 250 subscribers × $12 = $3,000/mo. Mixed model: 100 one-time plans + 100 subs = $1,900 + $1,200 = $3,100/mo. Lower ceiling than the B2B ideas — this tops out around $5–7K/mo realistically. Meaningful as a portfolio asset.

### 5. Automation Stack
- **What to automate first**: SEO content generation. Claude writes 1 article/week targeting cultural-specific macro queries ("how to hit 150g protein on a South Indian vegetarian diet") — auto-posted to the blog via n8n + scheduled Vercel deploy.
- **AI's role**: Claude is the product. Every meal plan is a Claude API call with a heavily engineered system prompt specifying cultural food vocabulary, macro accuracy requirements, and meal structure conventions for that cuisine.
- **How ongoing time approaches zero**: The MVP is nearly fully automated at launch. Month 2: add a community referral system (share your plan, get 20% off next). Month 3: blog content automation running. Steady state: review SEO performance, add new cuisine modules.

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Build South Asian MVP. Post in r/ABCDesis and 2 South Asian fitness Facebook groups. Create 2 TikToks showing actual plan output. Target 30 plans sold ($570).
- **Days 31–60 (Traction)**: Add West African cuisine module. Post in r/Nigeria, Naija fitness Facebook groups. Start subscription option. Target 100 total plans sold + 20 subscribers ($1,900 + $240 = $2,140 cumulative).
- **Days 61–90 (Scale)**: Add Filipino module (compete directly with KaibiganGPT on precision macros). Begin SEO content pipeline. Target $3,000/mo run rate.

⚠️ **Build urgency:** KaibiganGPT launched Filipino meal plans in late 2025 with macro tracking as a paid feature. The window is open but competitors are moving. If not built within 60 days, reassess whether the South Asian niche is still unclaimed.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 7 | 8 | 8 | 7 | 5 | 9 | 6 |

**Weighted score: 7.2/10**

---

## RECIPE RANKINGS

**Verdict:** 🟡 WATCH | Score: **6.2/10**

### Why It Didn't Clear the Bar
The idea is genuinely differentiated — an AI curation/ranking layer on top of existing recipe content is not the same as recipe generation, and the ranking-by-constraint angle is novel. JT's existing architecture (Nash Satoshi/Glow Index) makes it buildable. But two structural problems block a 🟢:

1. **Google AI Overviews are actively eating recipe SEO.** Google launched enhanced AI Overviews for recipe content in late 2025. A traffic-first affiliate model that depends on ranking for "best 30-minute high-protein recipes" is swimming against a Google-shaped current. The SEO moat that makes GymLore or SupplementScore defensible doesn't exist here because the query intent ("best recipe for X") is exactly what Google is trying to answer itself.

2. **Revenue ceiling is too low for the complexity.** At 30K monthly visitors (which would take 6–12 months to build), affiliate revenue from grocery delivery and kitchen tools is realistically $500–$1,500/mo. That's not enough to justify building *and* maintaining a recipe crawling + ranking infrastructure when GymLore (same architecture, same effort) has a direct $29/mo listing fee model.

**What would change this to a 🟢:** A paid subscription angle (e.g., "the algorithm-free recipe discovery service for serious home cooks — $5/mo") that doesn't depend on Google SEO. If JT finds evidence of 50–100 people paying for any premium recipe curation service, revisit.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 6 | 8 | 7 | 5 | 5 | 6 | 5 |

**Weighted score: 6.2/10**

---

## Full Scoring Summary

| Idea | Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition | **Overall** | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| GYMLORE | 8 | 8 | 9 | 7 | 6 | 8 | 9 | **7.75** | 🟢 |
| FANDOMDROP | 7 | 8 | 6 | 9 | 7 | 9 | 7 | **7.55** | 🟢 |
| FITBRIEF AI | 8 | 7 | 8 | 6 | 8 | 8 | 8 | **7.5** | 🟢 |
| TRADIECOMMS | 8 | 8 | 9 | 5 | 7 | 8 | 7 | **7.5** | 🟢 |
| CULTUREFIT NUTRITION | 7 | 8 | 8 | 7 | 5 | 9 | 6 | **7.2** | 🟢 |
| RECIPE RANKINGS | 6 | 8 | 7 | 5 | 5 | 6 | 5 | **6.2** | 🟡 |

---

## Portfolio Commentary

This week's five 🟢 ideas break cleanly into two complementary buckets. **GymLore + FitBrief AI + TraidieComms** extend JT's emerging pattern of B2B operator tools — underserved professionals (trainers, gym owners, tradespeople) who need AI to handle their business communications and discovery. These are the high-defensibility plays, with data flywheels or switching costs that compound over time. **FandomDrop + CultureFit Nutrition** are the more creative bets — lower build risk, higher viral potential, but smaller revenue ceilings. Together, this week's batch would give JT three recurring SaaS tools + two consumer/transactional properties. Alongside Nash Satoshi and Glow Index (both stalled on monetization activation), GymLore is the most strategically coherent next build — it's essentially Glow Index deployed in a vertical JT already understands, with a clearer and faster path to revenue than either of his existing ranking assets.

**Recommended build order if JT builds one:** GymLore (reuses existing architecture, clear revenue model, fastest to first dollar among the 5). **If JT wants maximum revenue ceiling:** FitBrief AI ($19.5K/mo ceiling, clear SaaS model, strong B2B retention).
