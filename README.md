# Vita by Lucernas — Google for Startups AI Agents Challenge 2026

> **Track 1: Build (Net-new Agents)** · Submitted by Lucernas.AI
> Live: [vita.lucernas.ai](https://vita.lucernas.ai) · Email: [valerie@lucernas.ai](mailto:valerie@lucernas.ai)

---

## What is Vita?

Vita is a production multi-modal multi-agent **voice presence** for the parents who raised us. Not a chatbot. A daily companion that sees, listens, remembers, and stays.

Built net-new on **Google Agent Development Kit + Gemini Live + Cloud Run + Firestore**, Vita coordinates 12+ specialized sub-agents across three portals (elder, family caregiver, clinical nurse) on one Firestore back end. Real elder, caregiver, and nurse sessions live today in production.

**The problem.** 43% of adults over 60 report chronic loneliness (WHO) with health impact equivalent to smoking 15 cigarettes per day. Millions of diaspora adults have a parent over 65 living alone, sometimes thousands of miles away. They call on Sundays. They send money. They worry every day. Generic AI assistants don't remember mamá's stories, don't honor faith routines, don't watch for the medication she missed, and don't tell her son when something feels off.

**The solution.** A multimodal presence that talks to her every day, watches what she shows the camera, remembers her stories, observes her health, and bridges the family across borders. Vita stays so the family can sleep at night.

**Companion, never clinician.** Vita does not make medical or cognitive outcome claims.

---

## Architecture

Built on Google Cloud, end-to-end:

```
                       ┌─────────────────┐
                       │   Elder (65-85) │
                       │  Phone / Tablet │
                       └────────┬────────┘
                                │
                          WebSocket (voice)
                          HTTPS (app)
                                │
                       ┌────────▼────────────┐
                       │  Cloud Run          │
                       │  vita-advisor       │
                       │  us-central1, 0→10  │
                       └────────┬────────────┘
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
┌───────▼─────────┐    ┌────────▼─────────┐    ┌────────▼─────────┐
│  Gemini 3.1     │    │  Google ADK      │    │   Firestore      │
│  Flash Live     │    │  Multi-agent     │    │   15+ collections│
│  (Voice WS,     │    │  Root + 12 sub-  │    │   10+ Pydantic   │
│   6 endpoints)  │    │  agents, 49 tools│    │   models         │
└───────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
        │                       │                        │
┌───────▼─────────┐    ┌────────▼─────────┐    ┌────────▼─────────┐
│  Gemini Vision  │    │  Google Search   │    │   Cloud Storage  │
│  Mirror mode    │    │  grounding tool  │    │   docs / photos  │
│  Doc parsing    │    │                  │    │   V4 signed PUT  │
└─────────────────┘    └──────────────────┘    └──────────────────┘

      Three coordinated portals on one back end:
      Elder voice (React) · Caregiver dashboard · Nurse portal
```

| Layer | Technology |
|---|---|
| Voice intelligence | **Gemini 3.1 Flash Live** (WebSocket, native audio streaming, tool calling in-turn) |
| Multi-agent orchestration | **Google Agent Development Kit (ADK)** — root + 12+ sub-agents |
| Text intelligence | **Gemini 3 Flash** (memory extraction, daily summaries, recipe generation) |
| Vision | **Gemini Vision Flash** (elder Mirror mode, nurse document parsing) |
| Compute | **Cloud Run** us-central1, autoscale 0→10, 4 GiB / 2 vCPU |
| Persistence | **Firestore** — 15+ production collections + composite-index catalog |
| Storage | **Cloud Storage** — V4 signed PUT with content-length-range |
| Build + CI | **Cloud Build** — multi-stage Docker, hard-fail pre-deploy gates |
| Observability | **Cloud Logging** structured tool-call traces per session |
| Secrets | **Secret Manager** + Cloud Run service-identity bindings |
| Grounding | **Google Search via Gemini Live tools** + 88-file persona canon RAG |
| Payments | Stripe |
| Frontend | React 18 + Vite + TypeScript SPA |

---

## Multi-agent topology

The system is multi-agent because no single LLM call can stitch memory + medication + voice cost + cultural register + alert routing + vision + grounding into one coherent conversation while emitting a caregiver-readable audit trail.

**A root ADK orchestrator routes intent across 12 specialized sub-agents:**

| Sub-agent | Owns |
|---|---|
| **Companion** | Daily voice conversation, regional accent, register selection, faith-aware silence |
| **Medication** | Adherence confirmation by voice, schedule reasoning, missed-dose escalation |
| **Memory** (Libro de Vida) | Continuous categorized fact extraction (story / family / preference / routine / emotion / health) |
| **Mirror** | Gemini Vision Q&A on the elder device camera (photos, meds, plants, family albums) |
| **Alert** | 3-tier escalation routing (urgent / today / weekly) with caregiver notification |
| **Family** | Outbound message orchestration to siblings, grandchildren, the diaspora buyer |
| **Recipe** | Culturally grounded meal guidance with familiar regional dishes |
| **Voice cost** | Per-session budget tracking + throttling for cost transparency |
| **Session resumption** | Long-context persistence across multi-day conversations |
| **Persona variant** | Selects accent + register from the 88-file canon based on elder region |
| **Clinical handoff** | Generates redacted health summary for the nurse portal + caregiver |
| **Onboarding** | Caregiver-led elder onboarding with no-form intelligent capture |

The orchestrator stitches their outputs into one voice response in under 2 seconds. See [`architecture/ARCHITECTURE.md`](architecture/ARCHITECTURE.md) for the detailed pipeline.

---

## 49 production agent tools

The voice agent is registered with **48 custom ADK tools + Google Search grounding** (49 total). They are organized into:

- **User context & retrieval** (7 tools): full elder profile, meds, appointments, memories, time
- **Health & safety** (12 tools): mood, pain, hydration, sleep journal, fall-risk, medication-interaction, doctor-visit debrief, silent caregiver alerts
- **Memory & stories** (5 tools): Libro de Vida, family tree, gratitude journal, worry jar, life-story write
- **Daily life** (10 tools): today's tasks, weather, bill reminders, visitor log, grocery list, food order, recipe search + cooking mode
- **Family connection** (3 tools): call family, photo share with captions, virtual window
- **Enrichment** (8 tools): music + video search and playback, read aloud, cognitive games, guided meditation, UI atmosphere control, display cards
- **Search grounding** (1): Google Search via Gemini Live tools

Full catalog: [`src/tools/voice_tools_catalog.md`](src/tools/voice_tools_catalog.md).

---

## Three coordinated portals

| Portal | User | Surface |
|---|---|---|
| **Elder** | The parent (65-85) | Voice companion · Mirror mode camera Q&A · Libro de Vida · medication confirmation · cognitive games |
| **Caregiver** | Adult child (30-50) | Daily human-readable summary · 3-tier alerts · medication adherence charts · vital trends · Libro de Vida excerpts · family coordination · document vault |
| **Nurse** | Clinical home-care provider | 4-tier provider taxonomy · Path A self-signup + Path B invite-code · QR-coded clock-in/out · vital signs entry · photo upload · caregiver real-time sync |

---

## Live demo for judges

| | |
|---|---|
| Live URL | [https://vita.lucernas.ai](https://vita.lucernas.ai) |
| Caregiver login | `calagumo@yahoo.com` / `VitaDemo2026!` → [/app/caregiver](https://vita.lucernas.ai/app/caregiver) |
| Nurse login | `enfermera.vita@lucernas.ai` / `VitaDemo2026!` → [/app/nurse](https://vita.lucernas.ai/app/nurse) |
| Seeded elder | Doña Aurora Aguirre · 73 · Bucaramanga · HTA + Diabetes T2 · 45 days of medication adherence, nurse visits, voice sessions, Libro de Vida memories |

Hard-refresh after first load. The seed accounts are real Firestore docs, not mocks.

---

## Production observability + safety

- **Structured Cloud Logging tool-call traces** per session (`[sid] Tool call: {fc.name}({args})` + `Tool result`)
- **Hard-fail pre-deploy gates** in `deploy.sh`:
  - L2: ESLint `react-hooks/rules-of-hooks` + `no-unsafe-optional-chaining`
  - L4: Firestore composite-index catalog coverage diff
  - Voice-safety preflight (`validate_persona` import-time check, `GOOGLE_GENAI_USE_VERTEXAI=0` ordering, `send_client_content` count check)
- **Paired QA + Performance methodologies** with class-of-bug lesson library that promotes lessons to hard rules after 3 sibling findings
- **Client ErrorBoundary** posts every render crash to `/api/_debug/render_error` for forensic trail
- **88-file persona canon** validated at agent boot

---

## What's in this repo

```
.
├── README.md                          ← This file
├── SECURITY.md                        ← Posture + vulnerability disclosure
├── architecture/
│   └── ARCHITECTURE.md                ← Detailed system + voice pipeline
├── docs/
│   ├── SUBMISSION.md                  ← Devpost-format submission text
│   └── FINDINGS.md                    ← Engineering insights from building this
└── src/
    ├── models/
    │   └── schema.py                  ← Pydantic models (sanitized)
    ├── routes/
    │   └── api_routes_overview.md     ← API surface map
    └── tools/
        └── voice_tools_catalog.md     ← All 49 tools
```

**Not in this repo (intentionally):** the 88-file persona canon (voice rules, regional accent fragments, refusal patterns, faith-aware silence rules); production prompts; secret API keys; demo seed cultural content; competitive analysis; tier internals. The production codebase and canon stay private. This repo shows the architecture and structure that judges need to evaluate, with enough detail to verify the system is real and the multi-agent orchestration is substantive.

---

## Team

**Lucernas.AI** — founder-led pre-seed.

- **Carlos Guzman** (Co-Founder) — engineering and product
- **Valerie Guzman** (Co-Founder, Head of Science) — neuroscience grounding and persona authorship

---

## License

This repository is published under the MIT License for the purposes of the Google for Startups AI Agents Challenge 2026 judging. The production Vita codebase, persona canon, and operational data remain proprietary to Lucernas.AI.

The Vita name, logo, and branding are trademarks of Lucernas.AI.
