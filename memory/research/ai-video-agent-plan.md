# AI Video Agent — Development Plan
**Created:** 2026-04-07 | **Status:** Research Complete → Ready for Prototype | **Owner:** Eve

---

## 1. What Is This Agent?

An **AI Video Agent** that takes a brand brief (or content goal) and autonomously produces a finished short-form video — avatar talking-head, product demo, social ad, or explainer — with consistent brand voice, visual style, and platform-optimized output.

**Target output:** 30–90 second branded videos, auto-formatted for X/TikTok/LinkedIn/Instagram Reels, generated end-to-end from a text prompt or content input.

**Why it matters for JT:**
- Consulting clients need quick turnaround video content (testimonials, product demos, social ads)
- Nash Satoshi and Glow Index need promotional video content
- Content output velocity without a production team

---

## 2. AI Video Landscape — Current State (April 2026)

### 2.1 Video Generation Models (Scene/Asset Creation)

| Tool | Model | Strength | API? | Est. Cost |
|------|-------|----------|------|-----------|
| **Runway** | Gen-4.5 / Gen-4 Turbo | Cinematic quality, motion control, inpainting | Yes (credits) | $0.01/credit; ~25s free tier |
| **Kling AI** | Kling 2.5 Turbo | Character consistency, camera controls, 1080p | Yes (API) | ~$0.07–0.14/sec |
| **Google Veo 3** | Veo 3 / 3.1 | High-fidelity, near-photorealistic, cinematic terms | Via Google Vids / limited API | Part of Google Workspace |
| **Sora 2** (OpenAI) | sora-2 / sora-2-pro | Script-aware, brand customization | Yes (API) | **⚠️ Deprecated Sept 2026** |
| **Pika Labs** | Pika 2.x | Social-first, quick turnaround | Yes | Free tier + paid |
| **Hailuo AI** | CINE-V | Motion quality, creative scenes | API (via PiAPI) | Affordable |

**Recommendation for Prototype:** Start with **Kling AI API** (best value/quality ratio, strong character consistency) + **Runway API** for premium output.

### 2.2 AI Avatar Platforms (Talking-Head)

| Tool | Strength | API? | Est. Cost |
|------|----------|------|-----------|
| **HeyGen** | Business avatars, brand一致性, script-to-video | Yes | From $24/mo (Creator); API from $5 |
| **Synthesia** | Corporate training, best-in-class pedagogy framework | Yes | From $29/mo (Starter) |
| **D-ID** | Photo-to-video, talking heads, API-first | Yes (API) | From $3 API start; Studio from $4.70/mo |
| **Colossyan** | Enterprise training focus | Yes | Higher tier |

**Recommendation for Prototype:** **HeyGen API** (strongest brand avatar library, unlimited avatar videos on Creator plan, solid API).

### 2.3 Voice & Narration

| Tool | Strength | API? | Est. Cost |
|------|----------|------|-----------|
| **ElevenLabs** | Voice cloning, multilingual, emotional range | Yes (SDK) | Free tier; paid from $5/mo |
| **OpenAI TTS** | Fast, high quality, 6 voices | Yes | $0.015/1K chars |
| **Google Cloud TTS** | WaveNet voices, multilingual | Yes | Pay-per-use |

**Recommendation:** **ElevenLabs** (voice consistency across all videos = brand sonic identity; clone once, use forever).

### 2.4 Video Automation & Templating

| Tool | Role | Notes |
|------|------|-------|
| **Creatomate** | Video API / template engine | Code or no-code; great for product/brand templates |
| **n8n** | Workflow orchestration | Use existing n8n-agent; integrate all above tools |
| **Descript** | Video editing + AI (transcription, overdub) | Strong for post-edit, captioning |
| **CapCut / Canva** | Social-formatted output, captions | Can be automated via API |

### 2.5 Lip-Sync & Dubbing

| Tool | Use Case | API? |
|------|----------|------|
| **HeyGen (Video Translate)** | Dub videos into 70+ languages | Yes (API) |
| **D-ID** | Sync audio to photo avatar | Yes |
| **Rask.ai** | Video dubbing + lip-sync | Yes |

---

## 3. Agent Architecture

```
INPUT LAYER
├── Brand Brief (text prompt)
├── Content Goal (social ad / demo / explainer / testimonial)
└── Platform Target (X / LinkedIn / TikTok / Instagram)

AGENT CORE (n8n workflow + LLM orchestration)
├── Script Generator (LLM → brand-adjusted script + captions)
├── Visual Asset Selector (brand template / product images)
├── Voice Engine (ElevenLabs TTS — brand voice clone)
├── Avatar/Scene Generator (HeyGen API OR Kling/Runway API)
└── Composer (assemble video + captions + music + format)

OUTPUT LAYER
├── Raw MP4 (branded, platform-specific)
├── Captions / Subtitles (burned in)
└── Thumbnail + Caption text (for social post copy)
```

### Stack Recommendation
- **Orchestration:** n8n (already running in JT's stack) — python script nodes call APIs
- **LLM:** OpenRouter / Sonnet for script generation + brand voice adaptation
- **Avatar Video:** HeyGen API (primary, consistent brand avatars)
- **Scene Video:** Kling AI API (product demos, b-roll, environments)
- **Voice:** ElevenLabs (brand voice clone — clone JT's voice or a chosen voice once)
- **Composition:** FFmpeg (python script) for final assembly + captions
- **Output:** Auto-upload to Google Drive + notify JT

---

## 4. Prototype Plan

### Phase 1: Foundation (Week 1)
**Goal:** Single workflow — brand avatar video from a text script.

1. Set up accounts: HeyGen API key, ElevenLabs API key
2. Clone or select a brand voice on ElevenLabs (upload 1-min audio sample)
3. Create a HeyGen avatar (or select from their built-in library)
4. Build n8n workflow:
   - **Trigger:** Manual (or Google Sheets row added)
   - **LLM node:** Generate short script from topic (brand-adjusted)
   - **ElevenLabs node:** Convert script → audio MP3
   - **HeyGen node:** Create video from avatar + audio
   - **Output:** Save MP4 to Drive, notify via Telegram
5. Test with 3 variations (consulting intro, app promo, testimonial style)

### Phase 2: Multi-Template Expansion (Week 2)
1. Add 3 brand templates: Talking-Head, Product Demo, Social Ad
2. Add FFmpeg composition: add intro/outro, brand watermark, captions
3. Add platform formatter: LinkedIn (1:1, 30s) / X/TikTok (9:16, 60s) / Instagram (4:5)
4. Add music layer (stock audio via Pixabay API or Epidemic Sound)

### Phase 3: Autonomous Mode (Week 3–4)
1. Content calendar integration: hook into Notion content calendar
2. Auto-generate weekly video batch from scheduled content
3. Auto-post draft to Drive with caption copy ready for JT to publish
4. Add variation generator: 3-5 caption copy variants per video for A/B testing

---

## 5. Tool Cost Estimates (Prototype Phase)

| Tool | Plan | Monthly | Notes |
|------|------|---------|-------|
| HeyGen | Creator | ~$29/mo | Unlimited avatar III videos |
| ElevenLabs | Pro | ~$22/mo | 100K chars/mo, voice cloning |
| Kling AI | Standard | ~$10/mo | 180 video minutes |
| n8n | Cloud Pro | ~$20/mo | Already running |
| **Total** | | **~$60–80/mo** | For a production video agent |

*Note: Runway API credit-based (~$0.01/credit) as backup for premium scenes.*

---

## 6. Brand Video Use Cases for JT

| Use Case | Format | Avatar | Best Tool |
|----------|--------|--------|-----------|
| Consulting service explainer | 60s talking-head | HeyGen brand avatar | HeyGen |
| Client product demo reel | 30–90s product + voiceover | Product footage + ElevenLabs voice | Kling + ElevenLabs |
| Nash Satoshi promo | 15–30s social ad | Animated/scene | Kling + Runway |
| Glow Index launch video | 30s lifestyle | Scene-based | Kling |
| Client testimonial (anonymized) | 45s talking-head | HeyGen avatar on top of real photo | HeyGen + D-ID |

---

## 7. Implementation Checklist

### Must Have (Prototype)
- [ ] HeyGen API account + key added to global.env
- [ ] ElevenLabs API key added to global.env
- [ ] Voice clone created (JT's voice or brand voice)
- [ ] HeyGen avatar selected/created
- [ ] n8n workflow: Script → Audio → HeyGen Video → Drive
- [ ] Test video generated and reviewed
- [ ] FFmpeg captioning + branding overlay added

### Should Have (Phase 2)
- [ ] Kling AI API integrated for product scenes
- [ ] Platform-specific formatting (9:16 / 1:1 / 4:5)
- [ ] Brand watermark + intro/outro template
- [ ] Music layer
- [ ] Notion calendar trigger

### Nice to Have (Phase 3)
- [ ] Multi-language dubbing (HeyGen Video Translate)
- [ ] A/B caption variants
- [ ] Auto-post to social (via Buffer/Hootsuite API)
- [ ] Analytics tracking (views, completion rate)

---

## 8. Key Decisions Needed from JT

1. **Primary brand voice:** Clone JT's voice, or use a professional AI voice from ElevenLabs library?
2. **Brand avatar:** Use HeyGen's built-in avatars, or create a custom digital twin?
3. **Initial use case priority:** Consulting intro video OR app promo first?
4. **Budget comfort:** Is $60–80/mo for the full stack acceptable, or should we start with just HeyGen ($29)?

---

## 9. Risk Factors

| Risk | Mitigation |
|------|-----------|
| HeyGen/Kling API rate limits | Queue system in n8n, retry with backoff |
| Video generation time (1–5 min per video) | Async pattern: queue job → poll → notify when ready |
| Brand avatar consistency across videos | Use same avatar ID + voice ID locked in template |
| Content approval | Agent outputs to Drive draft; JT reviews before publishing |

---

*Next step: JT confirms Phase 1 priority and key decisions above → Eve sets up APIs and builds first n8n workflow.*
