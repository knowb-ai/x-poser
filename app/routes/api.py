"""API routes for the X-Poser Mini smoke test."""

from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import Config
from app.schemas import CheckRequest, CheckResponse, ErrorResponse, HealthResponse
from app.services.claim import extract_claim
from app.services.nebius import judge_claim
from app.services.rag import stitch_evidence
from app.services.report import assemble_report
from app.services.tavily import search_evidence

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        env={
            "tavily": bool(Config.TAVILY_API_KEY),
            "nebius": bool(Config.NEBIUS_API_KEY and Config.NEBIUS_BASE_URL),
        },
    )


async def _run_smoke_pipeline(req: CheckRequest) -> CheckResponse | JSONResponse:
    claim = extract_claim(req.claim_text)

    # --- Tavily search ---
    try:
        sources = search_evidence(claim)
    except RuntimeError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": "Tavily search failed", "details": str(exc)},
        )

    # No sources → shortcut UNCERTAIN
    if not sources:
        return CheckResponse(
            tweet_url=req.tweet_url,
            claim=claim,
            verdict="UNCERTAIN",
            confidence="LOW",
            summary="No useful evidence was found for this claim.",
            evidence=[],
            share_text="I could not verify this claim from available sources.",
        )

    # --- RAG stitch ---
    bundle = stitch_evidence(claim, sources)

    # --- Nebius judge ---
    try:
        verdict = judge_claim(claim, bundle)
    except RuntimeError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": "Nebius model call failed", "details": str(exc)},
        )

    # --- Assemble report ---
    report = assemble_report(
        tweet_url=req.tweet_url,
        claim=claim,
        nebius_output=verdict,
        tavily_sources=sources,
    )
    return report


@router.post("/check", response_model=CheckResponse, responses={500: {"model": ErrorResponse}})
async def check_claim(req: CheckRequest) -> CheckResponse | JSONResponse:
    return await _run_smoke_pipeline(req)


@router.post("/smoke", response_model=CheckResponse, responses={500: {"model": ErrorResponse}})
async def smoke_check(req: CheckRequest) -> CheckResponse | JSONResponse:
    return await _run_smoke_pipeline(req)
