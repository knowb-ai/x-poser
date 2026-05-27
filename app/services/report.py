"""Report assembly — merges Nebius output with Tavily source metadata."""

from __future__ import annotations

from typing import Any, Optional

from app.schemas import CheckResponse, EvidenceItem


def assemble_report(
    *,
    tweet_url: Optional[str],
    claim: str,
    nebius_output: dict[str, Any],
    tavily_sources: list[dict[str, Any]],
) -> CheckResponse:
    """Build a ``CheckResponse`` by combining the model verdict with source URLs."""
    evidence_items: list[EvidenceItem] = []

    for ev in nebius_output.get("evidence", []):
        idx = ev.get("source_number", 0) - 1  # 1-indexed → 0-indexed
        if 0 <= idx < len(tavily_sources):
            src = tavily_sources[idx]
            evidence_items.append(
                EvidenceItem(
                    title=src.get("title", ""),
                    url=src.get("url", ""),
                    published_date=src.get("published_date") or None,
                    stance=ev.get("stance", "CONTEXTUAL"),
                    note=ev.get("note", ""),
                )
            )
        else:
            # Source number out of range — still include the note
            evidence_items.append(
                EvidenceItem(
                    title="Unknown source",
                    url="",
                    stance=ev.get("stance", "CONTEXTUAL"),
                    note=ev.get("note", ""),
                )
            )

    return CheckResponse(
        tweet_url=tweet_url or None,
        claim=nebius_output.get("claim", claim),
        verdict=nebius_output.get("verdict", "UNCERTAIN"),
        confidence=nebius_output.get("confidence", "LOW"),
        summary=nebius_output.get("summary", ""),
        evidence=evidence_items,
        share_text=nebius_output.get("share_text", ""),
    )
