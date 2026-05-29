"""Report assembly — merges Nebius output with Tavily source metadata."""

from __future__ import annotations

from typing import Any, Optional

from app.schemas import CheckResponse, EvidenceItem
_VERDICT_VALUES = {"VALIDATED", "ATTACKED", "UNCERTAIN"}
_CONFIDENCE_VALUES = {"HIGH", "MEDIUM", "LOW"}
_STANCE_VALUES = {"SUPPORTS", "CONTRADICTS", "CONTEXTUAL"}

_VERDICT_ALIASES = {
    "TRUE": "VALIDATED",
    "SUPPORTED": "VALIDATED",
    "SUPPORTS": "VALIDATED",
    "CONFIRMED": "VALIDATED",
    "FALSE": "ATTACKED",
    "CONTRADICTED": "ATTACKED",
    "CONTRADICTS": "ATTACKED",
    "DEBUNKED": "ATTACKED",
    "REFUTED": "ATTACKED",
    "UNKNOWN": "UNCERTAIN",
}
_CONFIDENCE_ALIASES = {
    "MODERATE": "MEDIUM",
    "MID": "MEDIUM",
    "UNSURE": "LOW",
}
_STANCE_ALIASES = {
    "VALIDATES": "SUPPORTS",
    "VALIDATED": "SUPPORTS",
    "SUPPORT": "SUPPORTS",
    "REFUTES": "CONTRADICTS",
    "REFUTED": "CONTRADICTS",
    "CONTRADICT": "CONTRADICTS",
}


def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _normalize_enum(
    value: Any,
    *,
    allowed: set[str],
    aliases: dict[str, str],
    default: str,
) -> str:
    token = str(value or "").strip().upper().replace("-", "_").replace(" ", "_")
    token = aliases.get(token, token)
    return token if token in allowed else default


def assemble_report(
    *,
    tweet_url: Optional[str],
    claim: str,
    nebius_output: dict[str, Any],
    tavily_sources: list[dict[str, Any]],
) -> CheckResponse:
    """Build a ``CheckResponse`` by combining the model verdict with source URLs."""
    verdict = _normalize_enum(
        nebius_output.get("verdict"),
        allowed=_VERDICT_VALUES,
        aliases=_VERDICT_ALIASES,
        default="UNCERTAIN",
    )
    confidence = _normalize_enum(
        nebius_output.get("confidence"),
        allowed=_CONFIDENCE_VALUES,
        aliases=_CONFIDENCE_ALIASES,
        default="LOW",
    )
    evidence_items: list[EvidenceItem] = []

    for ev in nebius_output.get("evidence", []):
        idx = ev.get("source_number", 0) - 1  # 1-indexed → 0-indexed
        stance = _normalize_enum(
            ev.get("stance"),
            allowed=_STANCE_VALUES,
            aliases=_STANCE_ALIASES,
            default="CONTEXTUAL",
        )
        note = _safe_text(ev.get("note", ""))
        if 0 <= idx < len(tavily_sources):
            src = tavily_sources[idx]
            evidence_items.append(
                EvidenceItem(
                    title=_safe_text(src.get("title", "")),
                    url=str(src.get("url", "")).strip(),
                    published_date=_safe_text(src.get("published_date") or "") or None,
                    stance=stance,
                    note=note,
                )
            )
        else:
            # Source number out of range — still include the note
            evidence_items.append(
                EvidenceItem(
                    title="Unknown source",
                    url="",
                    stance=stance,
                    note=note,
                )
            )

    return CheckResponse(
        tweet_url=str(tweet_url).strip() if tweet_url else None,
        claim=_safe_text(nebius_output.get("claim", claim)),
        verdict=verdict,
        confidence=confidence,
        summary=_safe_text(nebius_output.get("summary", "")),
        evidence=evidence_items,
        share_text=_safe_text(nebius_output.get("share_text", "")),
    )
