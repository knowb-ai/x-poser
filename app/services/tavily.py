"""Tavily recency search module."""

from __future__ import annotations

import logging
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any
from openai import OpenAI

from tavily import TavilyClient

from app.config import Config

logger = logging.getLogger(__name__)
_TAVILY_MAX_QUERY_CHARS = 400
_TARGET_QUERY_CHARS = 220

_QUERY_SYSTEM_PROMPT = """\
You rewrite long user claims into a single concise web search query for fact-checking.
Rules:
- Return exactly one line of plain text.
- Keep it under 220 characters.
- Keep named entities, places, numbers, and time references from the claim.
- Do not add quotes, markdown, or explanations.
"""


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate_to_word_boundary(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text

    clipped = text[:max_chars]
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped.strip(" ,.;:-")


def _build_fallback_query(claim: str) -> str:
    cleaned = _normalize_whitespace(re.sub(r"https?://\S+", "", claim))
    if not cleaned:
        return "recent factual verification claim"

    # Keep the leading part of the claim — it's usually where key entities appear.
    return _truncate_to_word_boundary(cleaned, _TARGET_QUERY_CHARS)


def _synthesize_query_with_nebius(claim: str) -> str | None:
    if not Config.NEBIUS_API_KEY or not Config.NEBIUS_BASE_URL:
        return None

    model = Config.NEBIUS_MODEL or "meta-llama/Meta-Llama-3.1-70B-Instruct"
    client = OpenAI(
        api_key=Config.NEBIUS_API_KEY,
        base_url=Config.NEBIUS_BASE_URL,
    )

    claim_for_prompt = _truncate_to_word_boundary(
        _normalize_whitespace(claim), 1200
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _QUERY_SYSTEM_PROMPT},
                {"role": "user", "content": f"Claim: {claim_for_prompt}"},
            ],
            temperature=0.0,
            max_tokens=90,
        )
    except Exception:
        logger.warning(
            "Nebius query synthesis failed; falling back to deterministic query.",
            exc_info=True,
        )
        return None

    content = (response.choices[0].message.content or "").strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
    if content.endswith("```"):
        content = content.rsplit("```", 1)[0]

    content = _normalize_whitespace(content.strip().strip('"').strip("'"))
    if not content:
        return None

    return _truncate_to_word_boundary(content, _TARGET_QUERY_CHARS)


def build_search_query(claim: str) -> str:
    llm_query = _synthesize_query_with_nebius(claim)
    query = llm_query or _build_fallback_query(claim)
    query = _normalize_whitespace(query)
    query = _truncate_to_word_boundary(query, _TAVILY_MAX_QUERY_CHARS)

    if not query:
        query = "recent factual verification claim"

    return query

def _window_ending_today(*, days: int, today: date) -> tuple[str, str]:
    safe_days = max(1, min(days, 365))
    end = today
    start = today - timedelta(days=safe_days)
    return start.isoformat(), end.isoformat()


def _extract_iso_date(text: str) -> date | None:
    match = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", text)
    if not match:
        return None

    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _extract_latest_year(text: str) -> int | None:
    years = [int(y) for y in re.findall(r"\b(20\d{2})\b", text)]
    if not years:
        return None
    return max(years)


def build_recency_window(claim: str) -> tuple[str, str]:
    today = datetime.now(timezone.utc).date()
    lowered = claim.lower()

    explicit_date = _extract_iso_date(lowered)
    if explicit_date:
        start = explicit_date - timedelta(days=3)
        end = min(today, explicit_date + timedelta(days=7))
        if start > end:
            start = end - timedelta(days=1)
        return start.isoformat(), end.isoformat()

    referenced_year = _extract_latest_year(lowered)
    if referenced_year is not None:
        if referenced_year < today.year:
            return date(referenced_year, 1, 1).isoformat(), date(
                referenced_year, 12, 31
            ).isoformat()
        return date(today.year, 1, 1).isoformat(), today.isoformat()

    if any(
        token in lowered
        for token in (
            "today",
            "yesterday",
            "this week",
            "last week",
            "breaking",
            "just now",
            "right now",
            "currently",
        )
    ):
        return _window_ending_today(days=7, today=today)

    if any(
        token in lowered
        for token in ("this month", "last month", "recent weeks", "past month")
    ):
        return _window_ending_today(days=30, today=today)

    if any(token in lowered for token in ("this year", "last year", "past year")):
        return _window_ending_today(days=365, today=today)

    return _window_ending_today(days=14, today=today)


def _normalize_result(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": raw.get("title", ""),
        "url": raw.get("url", ""),
        "content": raw.get("content", ""),
        "published_date": raw.get("published_date") or raw.get("publishedDate") or "",
    }


def search_evidence(claim: str) -> list[dict[str, Any]]:
    """Run a Tavily search for evidence related to *claim*.

    Returns a normalised list of ``{title, url, content, published_date}`` dicts.
    Raises ``RuntimeError`` on API failure.
    """
    if not Config.TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not configured")

    client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    query = build_search_query(claim)
    start_date, end_date = build_recency_window(claim)

    try:
        response = client.search(
            query=query,
            topic="news",
            search_depth="advanced",
            start_date=start_date,
            end_date=end_date,
            max_results=8,
            include_answer=False,
            include_raw_content=False,
        )
    except Exception as exc:
        logger.exception("Tavily search failed")
        raise RuntimeError(f"Tavily search failed: {exc}") from exc

    results = response.get("results", [])
    return [_normalize_result(r) for r in results]
