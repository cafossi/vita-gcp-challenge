# Track 3 Refactor — From Consumer to Google Cloud Marketplace

> Specification for the multi-tenant, Marketplace-ready architecture.

---

## Before (Single-Tenant Consumer)

```
vita_users          ← all users in one collection
vita_medications    ← all meds in one collection
vita_sessions       ← all sessions in one collection
...
Stripe direct       ← one subscription per family
No branding config  ← hardcoded "Vita by Lucernas"
```

Single Firestore prefix (`vita_`). Single Cloud Run service. Single billing entity. Works for 50-500 families. Cannot scale to agencies.

## After (Multi-Tenant Marketplace)

```
agency_{id}_users          ← isolated per agency
agency_{id}_medications    ← isolated per agency
agency_{id}_sessions       ← isolated per agency
...
Marketplace billing        ← per-elder, aggregated per agency invoice
Branding config            ← per agency (logo, colors, voice name)
```

### Agency Organization Model

```python
class Agency(BaseModel):
    agency_id: str
    name: str
    country: str
    contact_email: str
    branding: AgencyBranding
    elder_uids: list[str]
    nurse_uids: list[str]
    plan: str = "agency_pro"
    per_elder_price_cents: int = 4900  # $49/elder/month
    created_at: datetime

class AgencyBranding(BaseModel):
    logo_url: str = ""
    primary_color: str = "#C85A2E"  # default Vita terracotta
    company_name: str = "Vita by Lucernas"
    voice_persona_name: str = "Vita"
```

### Data Isolation

Every Firestore query is scoped by agency prefix:

```python
# Before (single-tenant):
db.collection("vita_users").document(uid)

# After (multi-tenant):
prefix = f"agency_{agency_id}_" if agency_id else "vita_"
db.collection(f"{prefix}users").document(uid)
```

Middleware extracts `agency_id` from JWT claims and injects the correct prefix into every service call. No cross-agency data leakage is possible — queries are structurally isolated.

### Agency Admin Portal

New React page at `/app/agency-admin` with:

- **Elder roster:** Add/remove elders, view aggregate health metrics
- **Nurse management:** Assign nurses to elders, view shift coverage
- **Billing dashboard:** Per-elder costs, monthly invoice, usage breakdown
- **Branding config:** Upload logo, set colors, customize voice persona name
- **Health overview:** Medication adherence across all elders, alert summary

### Marketplace Listing

```yaml
# marketplace/listing.yaml
product:
  name: "Vita Voice Companion for Elder Care"
  provider: "Lucernas.AI"
  category: "Healthcare & Life Sciences"
  pricing:
    model: "per_unit"
    unit: "elder"
    price: "$49/month"
    minimum_units: 5
  deployment:
    type: "managed_service"
    region: "us-central1"
    infrastructure: "Cloud Run"
  requirements:
    - "Google Cloud project with Firestore enabled"
    - "Gemini API access (3.1 Flash Live)"
```

### MCP Connectors (Model Context Protocol)

For agencies that need EHR integration:

```python
# MCP server exposing elder health data to external systems
@mcp_server.tool()
async def get_elder_health_summary(elder_id: str) -> dict:
    """Returns medication adherence, recent vitals, mood trends."""
    # Reads from agency-isolated Firestore
    # Returns FHIR-compatible summary
    pass

@mcp_server.tool()
async def sync_medications_from_ehr(elder_id: str, medications: list) -> dict:
    """Imports medication list from external EHR system."""
    # Validates and creates medication records
    # Triggers voice reminders for new medications
    pass
```

### Migration Path (Consumer → Agency)

Existing consumer families are NOT migrated. They remain on the `vita_` prefix with direct Stripe billing. Agency clients get a fresh `agency_{id}_` prefix. Both coexist on the same Cloud Run instance.

```
Cloud Run (vita-advisor)
├── vita_*          ← consumer families (Stripe direct)
├── agency_abc_*    ← Agency ABC (Marketplace billing)
├── agency_def_*    ← Agency DEF (Marketplace billing)
└── agency_ghi_*    ← Agency GHI (Marketplace billing)
```

---

## Implementation Status

| Component | Status |
|-----------|--------|
| Agency data model | Implemented |
| Firestore prefix isolation | Implemented |
| Agency middleware (JWT extraction) | Implemented |
| Agency Admin Portal (React) | Implemented |
| Branding config (per agency) | Implemented |
| Per-elder billing aggregation | Implemented |
| Marketplace listing YAML | Draft |
| MCP connectors (EHR) | Prototype |
| Documentation | Complete |
