# Technical Findings & Learnings

> Discoveries from building a production voice AI agent on Google Cloud

---

## 1. Context Re-Billing Is the Hidden Cost of Voice AI

Gemini Live API charges per turn for ALL tokens in the session context window. Past turns accumulate and are re-billed each turn.

```
Turn 1:  billed for turn 1 only         (600 tokens)
Turn 5:  billed for turns 1+2+3+4+5     (3,000 tokens)
Turn 24: billed for all 24 turns         (14,400 tokens)
Turn 48: billed for all 48 turns         (28,800 tokens)
Total for a 24-min session: ~705,600 tokens (triangular sum)
```

**Our solution: 2-Session Architecture.** Two 12-min sessions cost 49% less than one 24-min session (~360K vs ~706K tokens) because context resets between sessions. We position this as "morning check-in + evening check-in."

**Context compression** (trigger: 25k tokens, window: 8k) further reduces re-billing. Validated cost: $0.008/min.

## 2. Cultural Specificity Is an Unfair Advantage

Generic AI fails this population. The details that matter:

| Detail | Generic AI | Vita |
|--------|-----------|------|
| Formality | Uses "tú" with everyone | "Usted" with elders (warmth, not distance) |
| Diminutives | "-ito" (Mexican default) | "-ico" for Colombian elders (regional marker) |
| Pet names | "Mija," "cariño" | NEVER — always the elder's real name |
| Faith | Ignores or generic | Mirrors user: "si Dios quiere," rosary timing |
| Silence | "I didn't understand that" | Waits. Never rushes. Silence is companionship |
| Repeated stories | "You already told me that" | Responds as if first time. Never corrects |

These aren't features — they're cultural competence embedded in the voice model's system instructions. A competitor would need to rebuild this from ethnographic research, not just translate an English prompt.

## 3. The Buyer ≠ The User (Diaspora Split Architecture)

| | Buyer | User |
|---|---|---|
| Who | Adult child (30-50) | Elderly parent (65-85) |
| Where | US, Spain, Chile | Colombia, Mexico, Venezuela, Peru |
| Currency | USD/EUR | Doesn't pay |
| Trigger | Guilt, health scare | Doesn't decide |
| Value | "I know mamá is OK" | "Someone talks to me every day" |

This changes everything about product design:
- **Acquisition** targets the child (guilt + USD income + 5-min demo)
- **Retention** runs through the elder (if mamá loves Vita, no one cancels)
- **The caregiver dashboard** is the paying customer's interface — it must deliver peace of mind, not data
- **The elder app** is the product — it must deliver companionship, not utility

## 4. ADK + Gemini 3.1 Flash Live Is Production-Ready

We run 50+ tools through Google ADK with Gemini 3.1 Flash Live on WebSocket. Key learnings:

- **Latency is acceptable** for natural conversation (~200-400ms tool execution)
- **Narrated actions are essential** — elders can't see loading states. Vita must say "Déjame buscar eso..." before calling any tool
- **Paralinguistic tags work** — [sigh], [pause], [soft laugh] render as actual audio (not spoken text) on Gemini 3.1 Flash Live
- **Context compression** reduces re-billing without losing conversation coherence
- **Tool declarations must match executors exactly** — type mismatches cause silent failures
- **`thinking_config` breaks demo endpoints** but works for production voice. Endpoint-specific config is required.

## 5. Multi-Tenant Refactoring Requires Agency-Level Isolation

User-level isolation (each elder has their own data) was already in place. Marketplace distribution requires a higher-level construct:

- **Agency organization** — groups of elders, caregivers, and nurses under one billing entity
- **Firestore prefix per agency** — `agency_{id}_` prefix for all collections
- **Branding config** — agency logo, colors, voice persona name per organization
- **Billing aggregation** — per-elder charges rolled up to agency invoice
- **Data isolation** — Agency A cannot see Agency B's elders, even if both are on the same Cloud Run instance

## 6. Voice Cost Validation Protocol

Before setting prices, we ran a structured cost validation:

```
Sessions 1-5:   5 min each    → $0.04/session ($0.008/min)
Sessions 6-10:  10 min each   → $0.10/session ($0.010/min)
Sessions 11-15: 15 min each   → $0.18/session ($0.012/min)
Sessions 16-20: Two 12-min    → $0.10+$0.10 ($0.008/min each)
```

Key finding: The 2-session architecture keeps per-minute costs flat at $0.008-0.010. Single long sessions grow super-linearly due to context re-billing.

**Decision rule:** If 10-min session cost < $0.20, ship at current pricing. If $0.20-$0.35, enforce session caps. If > $0.35, raise prices.

Result: Scenario 1 confirmed. All tiers ship as designed.
