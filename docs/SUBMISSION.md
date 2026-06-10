# Devpost Submission — Text Description (Track 1)

> Copy this to the Devpost project page text description fields.

---

## Project Name

**Vita by Lucernas — Multimodal Multi-Agent Voice Presence for the Parents Who Raised Us**

## Track

**Track 1: Build (Net-new Agents)**. The Vita agent is a net-new ADK + Gemini Live multi-modal multi-agent system. The `vita.lucernas.ai` marketing site predates the agent; the multi-agent platform this submission is being judged on is the production system that runs behind it.

## Problem to Solve

43% of adults over 60 report chronic loneliness (WHO), with health impact equivalent to smoking 15 cigarettes a day. Millions of diaspora adults aged 30–50 have at least one parent over 65 living alone, sometimes thousands of miles away. They call on Sundays. They send money. They worry every day.

Generic AI assistants (Alexa, Google Home, ChatGPT) do not honor faith routines, do not speak neutral Latin American Spanish, do not remember mamá's stories, and do not watch what she shows the camera. A human in-home companion costs $750–$1,050 per month for daily presence and is out of reach for most families. The void is total.

## Our Solution

Vita is a production multi-modal multi-agent voice presence that talks to elder parents every day, watches what they show the device camera, remembers their stories, observes their health, and bridges the family across borders.

Built net-new on Gemini Enterprise Agent Platform. Three coordinated portals (elder voice, family caregiver dashboard, clinical nurse) share one Firestore back end and one Google ADK multi-agent orchestrator.

### The agent system

A root ADK orchestrator routes intent across 12 specialized sub-agents and 49 production tools (48 custom + Google Search grounding). Each voice turn may require recalling life-story memory, confirming a medication slot, evaluating an emotional dip for tier-2 alert routing, retrieving the latest blood-pressure trend, running Gemini Vision on the camera frame, and selecting the regional voice persona, all inside one Gemini Live socket while the elder is mid-sentence.

The 12 sub-agents: Companion (regional Spanish, register), Medication, Memory (Libro de Vida extraction), Mirror (Gemini Vision camera Q&A), Alert (3-tier escalation), Family messaging, Recipe, Voice cost metering, Session resumption, Persona variant, Clinical handoff, Onboarding.

### Multi-modal capability (voice + vision + text in one socket)

- **Voice:** Gemini 3.1 Flash Live via WebSocket, 6 production persona endpoints
- **Vision:** Gemini Vision Flash for Mirror mode and nurse document parsing
- **Text:** Gemini 3 Flash for memory extraction, summaries, recipe generation

### Three coordinated portals

- **Elder portal:** voice-first daily companion with Mirror mode and Libro de Vida capture
- **Caregiver portal:** daily summary, 3-tier alerts, adherence charts, vital trends, document vault, family coordination
- **Nurse portal:** 4-tier provider taxonomy, QR-coded clock-in, vital signs entry, real-time caregiver sync

## Technologies Used

- **Intelligence:** Gemini 3.1 Flash Live (voice WebSocket, 6 persona endpoints), Gemini 3 Flash (text intelligence), Gemini Vision Flash (Mirror mode + document parsing)
- **Orchestration:** Google ADK — root agent + 12+ sub-agents + 49 production tools, ADK Sessions and Memory Bank, 88-file persona canon validated at boot
- **Infrastructure:** Cloud Run (us-central1, autoscale 0→10), Cloud Build, Firestore (15+ collections + composite-index catalog), Cloud Storage (V4 signed PUT), Secret Manager, Cloud Logging (structured tool-call traces), IAM with service-account federation
- **Grounding and Retrieval:** Google Search via Gemini Live tools, persistent per-elder RAG against 88-file persona canon and 15+ Firestore collections
- **Backend:** Python 3.12 + FastAPI + uvicorn, google-genai SDK, google-adk SDK, Pydantic v2, bcrypt, JWT auth with password-version revocation
- **Frontend:** React 18 + Vite + TypeScript, Liquid Glass design system, ESLint react-hooks rules in pre-deploy gate, ErrorBoundary with server-log integration
- **CI/CD:** Hard-fail pre-deploy gates (lint + Firestore index diff + voice-safety preflight), daily deploy cadence

## Data Sources

- **Per-elder data** (Firestore, 15+ collections): elder profile, medications and adherence log, vital signs time-series, Libro de Vida memory store (categorized story / family / preference / routine / emotion / health), family graph, voice sessions with mood scores and tool-call audit, nurse visits, 3-tier alerts, appointments, routines, activities, documents
- **Knowledge base RAG:** 88-file authored persona canon (voice rules, regional accents, register, refusal patterns, cultural fragments) validated at agent boot
- **Document vault** (Cloud Storage): elder photos, nurse CV uploads, medical documents with 5-category retention schema
- **External real-time:** Google Search via Gemini Live for current events, YouTube Data API v3 for music and video, OpenWeather for localized weather, GNews for regional news

## Findings and Learnings

**Observability comes first.** `logger.info` traces across the multi-agent system were silently dropped because `LOG_LEVEL=INFO` was set in `deploy.sh` but never read by code. Once `basicConfig` and per-logger `setLevel` landed, a 90-minute production bug was diagnosed in 5 minutes from logs.

**Voice config is the fragile surface.** `LiveConnectConfig` drift, `GOOGLE_GENAI_USE_VERTEXAI` ordering, `send_client_content` incompatibility with tool-enabled endpoints, model-name typos: each cost hours. Every voice change is now one-at-a-time with documented preflight.

**Shared budget is not fallback.** Our `google_search` tool shared an 18-second budget across two Gemini models; the slower primary consumed all of it before timing out, so the fallback never ran. Fix: reverse order, bump budget, reserve fallback guard.

**Cultural register is the moat, not the LLM.** Usted vs tú, faith routines, regional Spanish, the silence between turns. Generic LLMs cannot ship this without an authored 88-file persona canon validated at boot. The "would mama say this to her son at 11pm" gate is the actual quality bar.

## Third-Party Integrations

- **Stripe** for subscription billing (test mode during invite phase, production-key rotation pending)
- **YouTube Data API v3** for music and video display with title-rewrite filtering (our API key)
- **OpenWeather API** for localized weather (our key)
- **GNews API** for regional news (our key)
- **Gmail SMTP** for caregiver alert delivery
- **Phosphor Icons** (open-source, MIT license)

All third-party integrations respect provider Terms of Service. No scraped content, no synthetic personas, no fabricated testimonials.

## Live Demo Credentials

Available to judges:

- **Live URL:** [https://vita.lucernas.ai](https://vita.lucernas.ai)
- **Caregiver:** `calagumo@yahoo.com` / `VitaDemo2026!` → `/app/caregiver`
- **Nurse:** `enfermera.vita@lucernas.ai` / `VitaDemo2026!` → `/app/nurse`
- **Seeded elder:** Doña Aurora Aguirre, 73, Bucaramanga, hypertension + diabetes type 2, 45 days of history (medications, nurse visits, voice sessions, memories)
