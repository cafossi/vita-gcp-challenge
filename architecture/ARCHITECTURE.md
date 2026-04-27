# Vita Technical Architecture

> Production system running on Google Cloud Platform

---

## System Overview

```
                    ┌─────────────────┐
                    │   Elder (65-85) │
                    │   Phone/Tablet  │
                    └────────┬────────┘
                             │ WebSocket (voice)
                             │ HTTPS (app)
                    ┌────────▼────────┐
                    │  Cloud Run      │
                    │  vita-advisor   │
                    │  us-central1    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───────┐ ┌───▼────┐ ┌───────▼──────┐
     │ Gemini 3.1     │ │ Google │ │  Firestore   │
     │ Flash Live     │ │  ADK   │ │ 15 collections│
     │ (Voice WS)     │ │ 50+    │ │ 10 models    │
     │                │ │ tools  │ │              │
     └────────────────┘ └────────┘ └──────────────┘
              │                            │
     ┌────────▼───────┐           ┌────────▼──────┐
     │ Gemini Vision  │           │     GCS       │
     │ (Mirror mode)  │           │  (docs/photos)│
     └────────────────┘           └───────────────┘
```

## Voice Pipeline

```
Elder speaks
    │
    ▼
Phone microphone → WebSocket → Cloud Run
    │
    ▼
Gemini 3.1 Flash Live (real-time audio streaming)
    │
    ├─── Audio input ($3.00/1M tokens)
    ├─── Audio output ($12.00/1M tokens)
    ├─── Tool calls via ADK (50+ tools)
    │       ├── read_medications()
    │       ├── confirm_medication_taken()
    │       ├── save_memory()    → Firestore
    │       ├── flag_for_caregiver() → FCM push
    │       ├── search_and_display() → Google Search
    │       └── ... (50+ more)
    │
    ▼
Audio response → WebSocket → Phone speaker
    │
    ▼
Post-session: memory extraction (Gemini Flash text)
    → Libro de Vida entries
    → Session summary for caregiver
    → Mood/pain/adherence metrics
```

## Data Flow

```
Voice Session
    │
    ├──► vita_sessions (transcript, mood, pain, duration)
    ├──► vita_memories (extracted facts, stories, preferences)
    ├──► vita_medications (adherence confirmations)
    ├──► vita_alerts (if flag_for_caregiver triggered)
    │
    ▼
Caregiver Dashboard (React SPA)
    ├── Daily human summary (Gemini-generated)
    ├── Medication adherence chart (7-day)
    ├── Alert feed (3 tiers)
    ├── Libro de Vida excerpts
    └── Family coordination tools
```

## Firestore Schema (15 Collections)

| Collection | Key Fields | Purpose |
|-----------|-----------|---------|
| `{prefix}users` | uid, name, dob, timezone, gender, caregivers[] | Elder profiles |
| `{prefix}medications` | med_id, uid, name, dosage, schedule_times[], adherence_log[] | Medication tracking |
| `{prefix}appointments` | appointment_id, uid, title, doctor, datetime | Calendar |
| `{prefix}sessions` | session_id, uid, transcript[], mood, pain, summary | Voice session records |
| `{prefix}alerts` | alert_id, uid, tier (1/2/3), type, dismissed | Caregiver notifications |
| `{prefix}memories` | memory_id, uid, fact, category, private | Libro de Vida |
| `{prefix}vitals` | reading_id, uid, vital_type, value, recorded_by | Nurse vital signs |
| `{prefix}nurses` | nurse_id, email, name, assigned_elder_uids[] | Nurse profiles |
| `{prefix}voice_baselines` | uid, speech_rate, pitch, pause means/stds | Voice biomarkers |
| `{prefix}subscriptions` | owner_id, plan_id, stripe_id, status, trial_end | Billing |
| `{prefix}voice_costs` | session_id, duration, est_cost, cost_per_min | Cost tracking |
| `{prefix}billing_events` | event_id, type, data | Stripe webhook audit |
| `{prefix}rate_limits` | ip, attempts[], locked_until | Rate limiting |
| `{prefix}waitlist` | email, name, source, created_at | Waitlist signups |
| `{prefix}feedback` | session_id, mode, insights[], complaints[] | User feedback |

`{prefix}` = `vita_` for consumer, `agency_{id}_` for Marketplace agencies.

## Cloud Run Configuration

```yaml
service: vita-advisor
region: us-central1
project: vita-gpd
platform: managed
memory: 4Gi
cpu: 2
cpu-boost: true
min-instances: 0
max-instances: 10
timeout: 300s
allow-unauthenticated: true
```

## Cost Model (Validated April 2026)

| Component | Cost/User/Month |
|-----------|----------------|
| Gemini 3.1 Flash Live (voice) | $4.50-18.00 (varies by plan) |
| Cloud Run | $5.00 |
| Firestore | $2.00 |
| GCS | $1.00 |
| FCM | $0.00 |
| Email (SMTP) | $1.00 |
| Memory extraction (Gemini Flash) | $0.50 |
| Session summary | $0.30 |
| Weekly PDF | $0.20 |
| **Total infrastructure** | **~$10.00** |
| **Validated voice cost** | **$0.008/min** |
