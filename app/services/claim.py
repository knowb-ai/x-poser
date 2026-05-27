"""Input validation and claim extraction (smoke-test version)."""

from __future__ import annotations


def extract_claim(claim_text: str) -> str:
    """Return a cleaned claim string.

    For the smoke test this simply strips whitespace.
    Future versions may use an LLM to split compound claims.
    """
    return claim_text.strip()
