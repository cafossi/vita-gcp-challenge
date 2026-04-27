# Vita API Routes — Overview

> 20 router groups, 125+ endpoints, 4 WebSocket voice endpoints.
> All API routes use `/api/` prefix. SPA catch-all serves React for all other paths.

---

## REST API Routers (mounted in serve.py)

| Prefix | Router | Purpose | Auth |
|--------|--------|---------|------|
| `/api/auth` | auth_routes | Login, registration, PIN verification | Public |
| `/api/users` | user_routes | User profile, preferences, health data | JWT |
| `/api/chat` | chat_routes | Text-based messaging with Vita | JWT |
| `/api/today` | today_routes | Daily tasks, medication schedule, appointments | JWT |
| `/api/care` | care_routes | Care instructions, vitals, medical data | JWT |
| `/api/caregiver` | caregiver_routes | Caregiver dashboard, alerts, summaries, coordination | JWT |
| `/api/more` | more_routes | Miscellaneous features | JWT |
| `/api/entertainment` | entertainment_routes | Music, videos, games, activities | JWT |
| `/api/food` | food_routes | Favorite meals, food orders, recipes | JWT |
| `/api/family` | family_routes | Family members, contacts, birthdays | JWT |
| `/api/settings` | settings_routes | App preferences, notifications, theme, language | JWT |
| `/api/weather` | weather_routes | Weather for elder's location | JWT |
| `/api/billing` | billing_routes | Stripe payments, plans, subscriptions | JWT/Public |
| `/api/agency` | agency_routes | Agency multi-family management portal | Agency JWT |
| `/api/nurse` | nurse_routes | Nurse QR check-in, vitals, photos, visits | Nurse JWT |
| `/api/command` | command_routes | Admin command center (12 tabs) | COMMAND_SECRET |
| `/api/demo` | demo_routes | Demo login, 14 demo codes, rate limiting | Public |
| `/api/waitlist` | waitlist_routes | Waitlist signup, referral tracking | Public |
| `/api/health` | Built-in | Service health check | Public |
| `/api/vision` | Built-in | Photo analysis via Gemini Vision | JWT |

## WebSocket Voice Endpoints

| Path | Page | Persona | Purpose |
|------|------|---------|---------|
| `/ws/voice/{session_id}` | Elder app | Elder companion | Daily voice sessions with mamá |
| `/ws/demo/{ticket}` | Demo page | Demo ambassador | Public 10-min product demo |
| `/ws/dev-voice/{session_id}` | Dev page | Dev engineer | Internal development sessions |
| `/ws/feedback-voice/{session_id}` | Feedback page | Feedback agent | Customer interviews, presentations |

## Marketplace Addition (Track 3)

| Prefix | Router | Purpose |
|--------|--------|---------|
| `/api/agency/admin` | agency_admin_routes | Agency-level elder management, aggregate metrics |
| `/api/agency/billing` | agency_billing_routes | Per-elder billing, invoice aggregation |
| `/api/agency/branding` | agency_branding_routes | White-label configuration per agency |
