"""
src/rag/generator.py
─────────────────────
Sinh câu trả lời từ LLM dựa trên context đã truy xuất.
Hỗ trợ OpenAI, Anthropic, và streaming.
"""

from __future__ import annotations

import logging
from typing import AsyncIterator

from src.core.config import Settings
from src.rag.retriever import RetrievedDoc

logger = logging.getLogger(__name__)

# ─── Prompt builder ───────────────────────────────────────────────────────────

def _build_context(docs: list[RetrievedDoc]) -> str:
    """Ghép tài liệu thành context block cho prompt."""
    if not docs:
        return "Không tìm thấy tài liệu liên quan trong cơ sở tri thức."

    parts = []
    for i, doc in enumerate(docs, 1):
        header = f"[{i}] {doc.title}"
        if doc.source:
            header += f" — {doc.source}"
        if doc.year:
            header += f" ({doc.year})"
        parts.append(f"{header}\n{doc.content}")

    return "\n\n---\n\n".join(parts)


def _build_messages(
    query: str,
    context: str,
    history: list[dict],
    system_prompt: str,
) -> list[dict]:
    """Xây dựng danh sách messages theo OpenAI chat format."""
    messages = [{"role": "system", "content": system_prompt}]

    # Thêm lịch sử hội thoại (tối đa 10 lượt trước)
    messages.extend(history[-10:])

    # Câu hỏi hiện tại kèm context
    user_content = (
        f"**Tài liệu tham khảo:**\n\n{context}\n\n"
        f"---\n\n**Câu hỏi:** {query}"
    )
    messages.append({"role": "user", "content": user_content})

    return messages


# ─── Generator ────────────────────────────────────────────────────────────────

class Generator:
    """
    Sinh câu trả lời từ LLM.

    Args:
        settings: App settings với LLM_PROVIDER, API keys, ...
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = self._init_client()

    def _init_client(self):
        """Khởi tạo LLM client tuỳ theo provider."""
        provider = self.settings.LLM_PROVIDER
        if provider == "openai":
            try:
                from openai import AsyncOpenAI  # noqa: PLC0415
                return AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
            except ImportError:
                logger.warning("openai package không có — dùng mock generator")
                return None

        if provider == "anthropic":
            try:
                from anthropic import AsyncAnthropic  # noqa: PLC0415
                return AsyncAnthropic(api_key=self.settings.ANTHROPIC_API_KEY)
            except ImportError:
                logger.warning("anthropic package không có — dùng mock generator")
                return None

        logger.info("LLM provider='local' — dùng mock generator")
        return None

    async def generate(
        self,
        query: str,
        docs: list[RetrievedDoc],
        history: list[dict] | None = None,
    ) -> str:
        """
        Sinh câu trả lời dựa trên tài liệu đã truy xuất.

        Args:
            query: Câu hỏi của người dùng.
            docs: Danh sách tài liệu liên quan.
            history: Lịch sử hội thoại.

        Returns:
            Câu trả lời dạng string.
        """
        context = _build_context(docs)
        messages = _build_messages(
            query, context, history or [], self.settings.LLM_SYSTEM_PROMPT
        )

        if self._client is None:
            return self._mock_generate(query, docs)

        if self.settings.LLM_PROVIDER == "openai":
            return await self._generate_openai(messages)
        if self.settings.LLM_PROVIDER == "anthropic":
            return await self._generate_anthropic(messages)

        return self._mock_generate(query, docs)

    async def stream(
        self,
        query: str,
        docs: list[RetrievedDoc],
        history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Streaming version — yield từng chunk text."""
        context = _build_context(docs)
        messages = _build_messages(
            query, context, history or [], self.settings.LLM_SYSTEM_PROMPT
        )

        if self._client is None or self.settings.LLM_PROVIDER != "openai":
            # Fallback: yield toàn bộ câu trả lời một lần
            answer = self._mock_generate(query, docs)
            yield answer
            return

        async with self._client.chat.completions.stream(
            model=self.settings.OPENAI_MODEL,
            messages=messages,
            temperature=self.settings.LLM_TEMPERATURE,
            max_tokens=self.settings.LLM_MAX_TOKENS,
        ) as stream:
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    async def _generate_openai(self, messages: list[dict]) -> str:
        response = await self._client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=messages,
            temperature=self.settings.LLM_TEMPERATURE,
            max_tokens=self.settings.LLM_MAX_TOKENS,
        )
        return response.choices[0].message.content or ""

    async def _generate_anthropic(self, messages: list[dict]) -> str:
        # Tách system message khỏi user messages
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        response = await self._client.messages.create(
            model=self.settings.ANTHROPIC_MODEL,
            system=system,
            messages=user_msgs,
            max_tokens=self.settings.LLM_MAX_TOKENS,
        )
        return response.content[0].text if response.content else ""

    def _mock_generate(self, query: str, docs: list[RetrievedDoc]) -> str:
        """Mock response dùng cho testing khi không có LLM API key."""
        if not docs:
            return (
                "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở tri thức. "
                "Vui lòng thử lại với câu hỏi cụ thể hơn về hệ thống điện mặt trời."
            )
        titles = [doc.title for doc in docs[:3]]
        return (
            f"[MOCK] Dựa trên {len(docs)} tài liệu tham khảo "
            f"({', '.join(titles)}), câu trả lời cho '{query[:50]}...' "
            "sẽ được tạo bởi LLM khi có API key hợp lệ."
        )
