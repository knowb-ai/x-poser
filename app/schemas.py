from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class CheckRequest(BaseModel):
    tweet_url: Optional[str] = None
    claim_text: str = Field(..., min_length=10)


class EvidenceItem(BaseModel):
    title: str
    url: str
    published_date: Optional[str] = None
    stance: str  # SUPPORTS | CONTRADICTS | CONTEXTUAL
    note: str


class CheckResponse(BaseModel):
    tweet_url: Optional[str] = None
    claim: str
    verdict: str  # VALIDATED | ATTACKED | UNCERTAIN
    confidence: str  # HIGH | MEDIUM | LOW
    summary: str
    evidence: list[EvidenceItem]
    share_text: str


class HealthResponse(BaseModel):
    ok: bool
    env: dict[str, bool]


class ErrorResponse(BaseModel):
    error: str
    details: str
