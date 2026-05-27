"""RAG stitching — builds a compact evidence bundle for the LLM."""

from __future__ import annotations

from typing import Any

_MAX_SNIPPET_CHARS = 500


def stitch_evidence(claim: str, sources: list[dict[str, Any]]) -> str:
    """Format *claim* and *sources* into a numbered evidence bundle."""
    lines: list[str] = [f"Claim:\n{claim}\n", "Sources:"]

    for i, src in enumerate(sources, start=1):
        snippet = (src.get("content") or "")[:_MAX_SNIPPET_CHARS]
        published = src.get("published_date") or "unknown"
        lines.append(
            f"[{i}] {src.get('title', 'Untitled')}\n"
            f"URL: {src.get('url', '')}\n"
            f"Published: {published}\n"
            f"Snippet: {snippet}"
        )

    return "\n\n".join(lines)
