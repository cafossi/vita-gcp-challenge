# Vita by Lucernas — Google for Startups AI Agents Challenge

> Track 3: Refactor for Google Cloud Marketplace & Gemini Enterprise
> Team: Carlos Guzmán (Founder & CEO) + Valerie Guzmán (Co-Founder & Head of Science)
> Live: [vita.lucernas.ai](https://vita.lucernas.ai)

---

## What is Vita?

Vita is an AI voice companion that talks to elderly Latino parents every day — in their language, at their pace — while their adult children monitor from the US and Europe.

**The problem:** 43% of adults 60+ report chronic loneliness (WHO) — with health impacts equal to smoking 15 cigarettes per day. 12.3 million diaspora adults in the US and Spain have at least one parent over 65 living alone in Latin America. They call on Sundays. They send money. They worry every day.

**The solution:** Vita speaks neutral Latin American Spanish, remembers mamá's stories in a Libro de Vida, reminds her about medications with warmth (not alarms), and sends her children a daily summary: how she woke up, what she told Vita, what's worrying her, when to call.

Not a nurse. Not a doctor. The presence between your Sunday calls.

---

## Architecture

Built entirely on Google Cloud:

```
┌──────────────────────────────────────────────────────┐
│                  Google Cloud Platform                 │
│                                                       │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ Gemini 3.1  │    │  Google ADK  │    │ Firestore│ │
│  │ Flash Live  │◄──►│  (Agents)    │◄──►│ (15 cols)│ │
│  │ (Voice WS)  │    │  50+ tools   │    │          │ │
│  └──────┬──────┘    └──────┬───────┘    └────┬─────┘ │
│         │                  │                  │       │
│  ┌──────▼──────────────────▼──────────────────▼─────┐│
│  │              Cloud Run (FastAPI)                   ││
│  │  20 API router groups · 125+ endpoints            ││
│  │  4 WebSocket voice endpoints                      ││
│  │  Multi-tenant middleware · Agency isolation        ││
│  └──────────────────────┬────────────────────────────┘│
│                         │                              │
│  ┌──────────────────────▼────────────────────────────┐│
│  │              React 18 SPA (Vite + TS)             ││
│  │  Elder Portal · Caregiver Dashboard · Nurse App   ││
│  │  Agency Admin · Command Center · Demo System      ││
│  └───────────────────────────────────────────────────┘│
│                                                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   GCS   │  │   FCM   │  │ Vision  │  │ Search  │ │
│  │ Storage │  │  Push   │  │ (Gemini)│  │  API    │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│                                                       │
│  ┌───────────────────────────────────────────────────┐│
│  │         Google Cloud Marketplace (Track 3)        ││
│  │  Agency Pro: $49/elder/mo · White-label · MCP     ││
│  └───────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────┘
```

| Component | Technology |
|-----------|-----------|
| Voice Engine | Gemini 3.1 Flash Live (WebSocket, real-time audio) |
| Agent Framework | Google Agent Development Kit (ADK) |
| Text Intelligence | Gemini 3 Flash (memory extraction, summaries) |
| Hosting | Cloud Run (us-central1, auto-scaling 0-10) |
| Database | Firestore (15 collections, 10 data models) |
| Storage | Google Cloud Storage |
| Push | Firebase Cloud Messaging (FCM) |
| Vision | Gemini Vision (mirror mode photo analysis) |
| Search | Google Search API (news, weather for elders) |
| Payments | Stripe |

---

## Three Portals

| Portal | User | Purpose |
|--------|------|---------|
| **Elder App** (El Corazón) | Mamá/Papá (65-85) | Voice companion, medication reminders, Libro de Vida, daily check-in |
| **Caregiver App** (La Tranquilidad) | Adult child (30-50, US/EU) | Daily summary, 3-tier alerts, medication adherence, family coordination |
| **Nurse App** (El Escudo) | Home nurse | QR check-in, vital signs, photo uploads, shift reports |

---

## 50+ Voice Agent Tools

Vita's voice agent runs on Gemini 3.1 Flash Live via WebSocket with 50+ registered tools through Google ADK:

**Health & Safety:** medication reminders with confirmation, mood tracking (1-5), pain logging, sleep journal, hydration tracker, fall risk assessment, medication interaction check, doctor visit debrief, silent caregiver alerts (3 tiers)

**Memory & Stories:** Libro de Vida (life story preservation with era tags), family tree builder, gratitude journal, worry jar, memory extraction from voice sessions

**Daily Life:** today's tasks, weather, bill reminders, visitor log, grocery list, food ordering, recipe search + step-by-step cooking mode

**Family Connection:** call family (phone/WhatsApp/FaceTime), photo sharing with captions, virtual window (describe family member's day in another city)

**Enrichment:** music/video search + playback, read aloud (news, Bible, poems, jokes), cognitive games, guided meditation, UI atmosphere control

---

## Track 3 Refactor: From Consumer to Marketplace

### Before (single-tenant)
- One Firestore prefix per deployment
- Hardcoded branding
- Single billing entity

### After (multi-tenant, Marketplace-ready)
- **Agency organizations** with isolated elder data, configurable branding, per-agency billing
- **Agency Admin Portal** to manage 5-100+ elders, aggregate health metrics, voice persona config
- **Per-elder billing** ($49/elder/month) through Marketplace procurement
- **MCP connectors** for external EHR system integration

See `marketplace/` for the Marketplace listing configuration and `src/` for the multi-tenant refactor code.

---

## Business Impact

| Metric | Value |
|--------|-------|
| TAM | $4.4-5.8B (3.7-4.9M diaspora families) |
| Voice cost | $0.008/min (Gemini 3.1 Flash Live, validated) |
| Infrastructure | ~$10/user/month |
| Gross margins | 63-86% across 4 tiers |
| Pricing | $39-199/month (consumer), $49/elder/month (agency) |

---

## Science Foundation

Vita is grounded in four research areas, led by Valerie Guzmán (Neuroscience & Cognitive Science, University of Connecticut):

1. **Loneliness intervention** — Chronic loneliness = 15 cigarettes/day health impact. Only intervention with evidence: meaningful, repeated contact.
2. **Reminiscence therapy** — Studied since 1963 (Dr. Robert Butler). Measurable effects on depression. Libro de Vida is a structured intervention.
3. **Voice as biomarker** — Voice contains signals of cognitive/emotional wellbeing. Record with consent, observe changes, never diagnose.
4. **Transnational family care** — Love doesn't erase with distance, but presence distorts. Vita is designed for that reality.

---

## The Founders

**Carlos Guzmán** — Founder & CEO. 20+ years: aerospace → AI. MBA UT Dallas. Harvard Business Analytics. His mamá, Doña Teresa, lives alone in Cúcuta, Colombia. Vita was born from wanting someone to be there when he couldn't.

**Valerie Guzmán** — Co-Founder & Head of Science. Neuroscience & Cognitive Science at UConn. Pre-med. Designed Vita's 4-pillar research program. Carlos's daughter, Doña Teresa's granddaughter.

---

## Repository Structure

```
vita-gcp-challenge/
├── README.md                  ← This file
├── docs/
│   ├── SUBMISSION.md          ← Devpost text description
│   ├── FINDINGS.md            ← Technical findings & learnings
│   └── TRACK3_REFACTOR.md     ← Track 3 refactor specification
├── architecture/
│   └── ARCHITECTURE.md        ← Full technical architecture
├── src/
│   ├── routes/                ← Sanitized API route examples
│   ├── services/              ← Sanitized service layer examples
│   ├── models/                ← Data model definitions
│   └── tools/                 ← Voice agent tool definitions
├── frontend-preview/          ← Screenshots of the 3 portals
└── marketplace/               ← GCP Marketplace listing config
```

> **Note:** This is a submission-only repository. The full production codebase is private. Code samples here demonstrate the architecture and Track 3 refactor without exposing operational secrets, persona prompts, or customer data.

---

## Demo

Live: [vita.lucernas.ai](https://vita.lucernas.ai)

Demo video: [YouTube link TBD]

---

## Contact

- Carlos Guzmán — carlos@lucernas.ai
- Valerie Guzmán — valerie@lucernas.ai
- Website — [lucernas.ai](https://lucernas.ai)
