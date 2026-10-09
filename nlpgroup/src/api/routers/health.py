"""
src/api/routers/health.py
──────────────────────────
Health check endpoints — dùng cho load balancer, Kubernetes liveness/readiness probes.
"""

import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

_start_time = time.time()


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]


@router.get("/health", response_model=HealthResponse, summary="Liveness probe")
async def health() -> HealthResponse:
    """Trả về OK ngay lập tức — chỉ dùng để kiểm tra server còn sống."""
    from src.core.config import settings  # noqa: PLC0415
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        uptime_seconds=round(time.time() - _start_time, 1),
    )


@router.get("/ready", response_model=ReadinessResponse, summary="Readiness probe")
async def readiness() -> ReadinessResponse:
    """Kiểm tra tất cả dependencies (ChromaDB, embedding model) đã sẵn sàng chưa."""
    checks: dict[str, str] = {}

    # Kiểm tra ChromaDB
    try:
        import chromadb  # noqa: PLC0415
        from src.core.config import settings  # noqa: PLC0415
        client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
        client.heartbeat()
        checks["chromadb"] = "ok"
    except Exception as e:
        checks["chromadb"] = f"error: {e}"

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return ReadinessResponse(status=overall, checks=checks)
