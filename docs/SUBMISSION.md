# Devpost Submission — Text Description

> Copy this to the Devpost project page text description field.

---

## Vita by Lucernas — AI Voice Companion for Elderly Latino Families

### Summary

Vita is a production AI voice companion that talks to elderly Latino parents every day — in their language, at their pace — while their adult children monitor from the US and Europe. Built entirely on Google Cloud (Gemini 3.1 Flash Live, Agent Development Kit, Cloud Run, Firestore), Vita combines persistent memory, culturally-specific voice interaction, and a 3-portal family architecture into a platform that no generic AI assistant can replicate.

For this challenge (Track 3), we refactored Vita from a single-tenant consumer product into a multi-tenant, Marketplace-ready platform — enabling home care agencies across Latin America to deploy Vita for their clients through Google Cloud Marketplace.

### The Problem

68 million Hispanics live in the United States. 4.25 million Latin Americans live in Spain. Behind each of them is a parent aging alone in Latin America. 43% of adults 60+ report chronic loneliness (WHO) — with health impacts equal to smoking 15 cigarettes per day.

12.3 million diaspora adults aged 30-50 have at least one parent over 65 living in Latin America. They call on Sundays, send money, and worry every day. Hiring a human companion costs $750-1,050/month. Generic AI doesn't understand "usted" vs "tú," doesn't know about faith routines, and doesn't remember mamá's stories.

The market: 3.7-4.9 million families, $4.4-5.8 billion TAM. Zero products exist that combine voice AI + elder companionship + Latino cultural specificity + diaspora family architecture + neuroscience grounding.

### What Vita Does

**For the elder (65-85):** Daily voice conversations in neutral Latin American Spanish. 50+ voice tools including medication reminders, Libro de Vida (life story preservation), gratitude journal, cognitive games, recipe guidance, fall risk assessment, and family calls. 6 voice modes: companion, cooking, mirror, medications, intro, and caregiver setup. Culturally specific: "usted" formality, regional accents, faith sensitivity.

**For the adult child (30-50, US/Europe):** Daily human summary — how mamá woke up, what she told Vita, what concerns her. 3-tier alerts (urgent/today/weekly). Medication adherence charts. Libro de Vida excerpts. Family coordination across siblings.

**For the nurse (Legado plan):** QR check-in, vital signs entry, photo uploads, real-time sync to caregiver dashboard.

### Technologies Used

- **Gemini 3.1 Flash Live** — Voice engine (WebSocket, real-time audio streaming)
- **Google Agent Development Kit (ADK)** — Agent framework for 50+ voice tools
- **Gemini 3 Flash** — Memory extraction, session summaries, recipe generation
- **Cloud Run** — Hosting (us-central1, auto-scaling 0-10)
- **Firestore** — Database (15 collections, 10 data models)
- **Google Cloud Storage** — Documents, photos, voice recordings
- **Firebase Cloud Messaging** — Push notifications
- **Gemini Vision** — Photo analysis for mirror mode
- **Google Search API** — News, weather, nearby services for elders

### Track 3 Refactor

**Before:** Single-tenant consumer product with one Firestore prefix, hardcoded branding, direct Stripe billing.

**After:** Multi-tenant Marketplace-ready platform with agency organizations, isolated elder data, configurable branding, per-agency billing, Agency Admin Portal (5-100+ elders), and MCP connectors for EHR integration. Any home care agency can deploy Vita through Google Cloud Marketplace at $49/elder/month.

### Business Impact

- **TAM:** $4.4-5.8B (3.7-4.9M diaspora families across US + Spain)
- **Unit economics:** Voice cost $0.008/min (validated). Infrastructure $10/user/month. Margins 63-86%.
- **Revenue path:** 50 founding families → 450 Year 1 → Marketplace distribution Year 2

### Findings & Learnings

1. **Context re-billing is the hidden cost of voice AI.** Gemini Live re-bills all previous turns each turn. Our 2-Session Architecture reduces costs by 49%.

2. **Cultural specificity beats general capability.** Colombian diminutives end in '-ico' (not '-ito'). These invisible details are why elders engage daily with Vita and ignore Alexa.

3. **The buyer and user are different people.** The child in Dallas pays. The mother in Bogotá talks to Vita. Designing for this split is fundamentally different from single-user SaaS.

4. **ADK + Gemini Live is production-ready for voice agents.** 50+ tools via ADK with Gemini 3.1 Flash Live on WebSocket. The combination works at production scale.

5. **Multi-tenant refactoring for Marketplace requires agency-level data isolation** — not just user-level. This was the core Track 3 engineering challenge.
