"""Nebius claim-judge module — calls the Nebius OpenAI-compatible API."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI

from app.config import Config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are X-Poser, a strict claim-checking assistant.
Your job is to assess a claim using only the provided evidence bundle.
Classify the claim as:
VALIDATED:
The evidence strongly supports the claim.
ATTACKED:
The evidence clearly contradicts or undermines the claim.
UNCERTAIN:
The evidence is incomplete, mixed, ambiguous, outdated, or not directly relevant.
Rules:
- Do not invent facts.
- Do not use outside knowledge.
- Mention uncertainty when sources are weak.
- Prefer UNCERTAIN over overclaiming.
- Always cite source numbers from the evidence bundle.
- Return valid JSON only."""

USER_PROMPT_TEMPLATE = """\
Claim:
{claim}

Evidence bundle:
{evidence}

Return JSON with this schema:
{{
  "claim": "...",
  "verdict": "VALIDATED | ATTACKED | UNCERTAIN",
  "confidence": "HIGH | MEDIUM | LOW",
  "summary": "2-4 sentences explaining the judgment.",
  "evidence": [
    {{
      "source_number": 1,
      "stance": "SUPPORTS | CONTRADICTS | CONTEXTUAL",
      "note": "1 sentence explaining why this source matters."
    }}
  ],
  "share_text": "A compact reply suitable for posting under the original X post."
}}"""


def judge_claim(claim: str, stitched_evidence: str) -> dict[str, Any]:
    """Send the evidence bundle to Nebius and return the parsed verdict.

    Raises ``RuntimeError`` on API or parsing failure.
    """
    if not Config.NEBIUS_API_KEY or not Config.NEBIUS_BASE_URL:
        raise RuntimeError("NEBIUS_API_KEY or NEBIUS_BASE_URL is not configured")

    client = OpenAI(
        api_key=Config.NEBIUS_API_KEY,
        base_url=Config.NEBIUS_BASE_URL,
    )

    model = Config.NEBIUS_MODEL or "meta-llama/Meta-Llama-3.1-70B-Instruct"

    user_prompt = USER_PROMPT_TEMPLATE.format(
        claim=claim,
        evidence=stitched_evidence,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
    except Exception as exc:
        logger.exception("Nebius model call failed")
        raise RuntimeError(f"Nebius model call failed: {exc}") from exc

    raw_text = response.choices[0].message.content or ""

    # Strip markdown fences if the model wraps JSON in ```json ... ```
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse Nebius response: %s", raw_text)
        raise RuntimeError(
            f"Nebius returned invalid JSON: {exc}"
        ) from exc
