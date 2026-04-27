"""Vita Firestore Data Models — Sanitized for submission.

These Pydantic models define the data structures stored in Firestore.
15 collections, 10 core models. All prefixed with `vita_` in production.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class VitaUser(BaseModel):
    """Elder profile — the person Vita talks to every day."""
    uid: str
    name: str
    email: Optional[str] = None
    dob: Optional[str] = None
    gender: str = "female"
    country: str = "Colombia"
    city: str = ""
    timezone: str = "America/Bogota"
    language: str = "es"
    pin_hash: Optional[str] = None
    caregivers: list[str] = Field(default_factory=list)
    onboarding_complete: bool = False
    created_at: Optional[datetime] = None


class Medication(BaseModel):
    """Medication tracked for an elder. Voice reminders + adherence logging."""
    med_id: str
    uid: str
    name: str
    dosage: str = ""
    schedule_times: list[str] = Field(default_factory=list)
    with_food: bool = False
    active: bool = True
    pharmacy: str = ""
    adherence_log: list[dict] = Field(default_factory=list)


class Appointment(BaseModel):
    """Medical appointment tracked for an elder."""
    appointment_id: str
    uid: str
    title: str
    doctor_name: str = ""
    datetime: Optional[datetime] = None
    location: str = ""
    completed: bool = False


class VitaSession(BaseModel):
    """Voice session record — what happened during a conversation."""
    session_id: str
    uid: str
    started_at: Optional[datetime] = None
    duration_seconds: float = 0
    mood_score: Optional[int] = None  # 1-5
    pain_score: Optional[int] = None  # 1-5
    summary: str = ""
    transcript_turns: int = 0


class VitaAlert(BaseModel):
    """Alert sent to caregivers. 3 tiers: 1=urgent, 2=today, 3=weekly."""
    alert_id: str
    uid: str
    tier: int  # 1, 2, or 3
    type: str  # "medication_missed", "mood_low", "fall_risk", etc.
    description: str
    dismissed: bool = False
    notified_caregivers: list[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None


class VitaMemory(BaseModel):
    """Memory extracted from voice sessions — the Libro de Vida."""
    memory_id: str
    uid: str
    fact: str
    category: str  # "family", "health", "preference", "story", "routine", "fear", "joy"
    private: bool = False
    source_session_id: Optional[str] = None
    created_at: Optional[datetime] = None


class VitalReading(BaseModel):
    """Vital sign reading logged by a nurse."""
    reading_id: str
    uid: str
    vital_type: str  # "blood_pressure", "heart_rate", "temperature", "o2_sat", "blood_sugar"
    value: str
    recorded_at: Optional[datetime] = None
    recorded_by: Optional[str] = None  # nurse_id


class VitaNurse(BaseModel):
    """Nurse profile — assigned to elders in the Legado plan."""
    nurse_id: str
    email: str
    name: str
    assigned_elder_uids: list[str] = Field(default_factory=list)


class VoiceBaseline(BaseModel):
    """Voice biomarker baselines — tracked over time for change detection."""
    uid: str
    speech_rate_mean: float = 0
    speech_rate_std: float = 0
    pitch_mean: float = 0
    pitch_std: float = 0
    pause_mean: float = 0
    pause_std: float = 0
    updated_at: Optional[datetime] = None
