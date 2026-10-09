"""
src/api/routers/chat.py
────────────────────────
Chat endpoint — giao diện hội thoại chính với AI tư vấn điện mặt trời.
Nhận câu hỏi, chạy RAG pipeline, trả về câu trả lời có trích dẫn nguồn.
"""

from __future__ import annotations

import logging
import time
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.core.dependencies import RAGPipelineDep

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Request / Response models ────────────────────────────────────────────────

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=4096)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(..., min_length=1, max_length=20)
    stream: bool = False
    session_id: str | None = None


class Citation(BaseModel):
    index: int
    title: str
    source: str | None = None
    year: str | None = None
    page: str | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = []
    session_id: str | None = None
    latency_ms: int


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Hỏi đáp AI tư vấn điện mặt trời",
    description=(
        "Nhận câu hỏi tiếng Việt về điện mặt trời, truy xuất tài liệu liên quan "
        "từ vector store, và tạo câu trả lời có trích dẫn nguồn bằng LLM."
    ),
)
async def chat(
    request: ChatRequest,
    pipeline: RAGPipelineDep,
) -> ChatResponse:
    """
    Endpoint hội thoại chính.

    - Lấy câu hỏi mới nhất từ `messages` (role=user)
    - Chạy RAG: embed → retrieve → rerank → generate
    - Trả về câu trả lời + danh sách citations
    """
    # Lấy câu hỏi cuối cùng của user
    user_messages = [m for m in request.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cần có ít nhất một tin nhắn với role='user'",
        )

    query = user_messages[-1].content
    history = [
        {"role": m.role, "content": m.content}
        for m in request.messages[:-1]
    ]

    if request.stream:
        return StreamingResponse(
            _stream_response(pipeline, query, history),
            media_type="text/event-stream",
        )

    t0 = time.monotonic()
    result = await pipeline.run(query=query, history=history)
    latency = int((time.monotonic() - t0) * 1000)

    logger.info("chat: query_len=%d latency_ms=%d citations=%d",
                len(query), latency, len(result.citations))

    return ChatResponse(
        answer=result.answer,
        citations=[
            Citation(
                index=i + 1,
                title=c.get("title", ""),
                source=c.get("source"),
                year=c.get("year"),
                page=c.get("page"),
            )
            for i, c in enumerate(result.citations)
        ],
        session_id=request.session_id,
        latency_ms=latency,
    )


async def _stream_response(
    pipeline, query: str, history: list
) -> AsyncIterator[str]:
    """Server-Sent Events stream cho streaming response."""
    async for chunk in pipeline.stream(query=query, history=history):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"
