from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models import AskRequest, AskResponse, HealthResponse
from app.services.orchestrator import answer_question

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        demo_mode=settings.demo_mode,
    )


@router.post("/ask", response_model=AskResponse, tags=["assistant"])
async def ask(request: AskRequest) -> AskResponse:
    if len(request.location) > settings.max_location_length:
        raise HTTPException(status_code=400, detail="Location is too long.")
    if len(request.question) > settings.max_question_length:
        raise HTTPException(status_code=400, detail="Question is too long.")

    request_id = str(uuid4())
    result = await answer_question(
        location=request.location,
        question=request.question,
        request_id=request_id,
    )
    result.generated_at = datetime.now(timezone.utc)
    return result
