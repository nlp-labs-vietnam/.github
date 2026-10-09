"""
modules/ner/ner.py
───────────────────
Nhận dạng thực thể có tên (NER) đặc thù cho domain Năng lượng Mặt trời Việt Nam.

Các nhãn thực thể được định nghĩa:
  CAPACITY    — Công suất hệ thống (VD: "5 kWp", "10 kW")
  BRAND       — Thương hiệu thiết bị (VD: "Growatt", "SMA", "Jinko")
  PROVINCE    — Tỉnh/thành phố Việt Nam (VD: "Hà Nội", "Đà Nẵng")
  REGULATION  — Văn bản pháp luật (VD: "Quy hoạch Điện VIII", "QĐ 500")
  PRICE       — Giá cả (VD: "15 triệu", "150 triệu đồng")
  ENERGY_TYPE — Loại năng lượng (VD: "điện mặt trời", "năng lượng tái tạo")

Ví dụ:
    extractor = SolarNERExtractor()
    entities = extractor.extract("Lắp 5 kWp Growatt tại Hà Nội giá 80 triệu đồng")
    # → [Entity(text="5 kWp", label="CAPACITY"), Entity(text="Growatt", label="BRAND"), ...]
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Entity:
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0


# ─── Rule-based patterns (fallback khi không có model) ───────────────────────

CAPACITY_PATTERN = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:kWp|kW|MW|MWp|Wp|W)\b",
    re.IGNORECASE,
)

PRICE_PATTERN = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:triệu|nghìn|tỷ)(?:\s+đồng)?\b",
    re.IGNORECASE,
)

SOLAR_BRANDS = {
    "Growatt", "SMA", "Huawei", "Sungrow", "Fronius", "Ginlong", "Solax",
    "Goodwe", "Deye", "Jinko", "Canadian Solar", "LONGi", "JA Solar",
    "Trina Solar", "Risen", "Phono Solar",
}

VIETNAMESE_PROVINCES = {
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "Đắk Lắk", "Khánh Hòa", "Bình Dương", "Đồng Nai", "Lâm Đồng",
    "Gia Lai", "An Giang", "Kiên Giang", "Bình Thuận", "Ninh Thuận",
    "Quảng Ngãi", "Bình Định", "Phú Yên", "Quảng Nam", "Thừa Thiên Huế",
}

REGULATION_PATTERN = re.compile(
    r"(?:Quy hoạch Điện\s+(?:VII|VIII|IX)|QĐ\s+\d+/QĐ-TTg|Nghị định\s+\d+)",
    re.IGNORECASE,
)

ENERGY_TYPE_PATTERN = re.compile(
    r"(?:điện mặt trời|năng lượng tái tạo|điện gió|điện sinh khối|solar|photovoltaic)",
    re.IGNORECASE,
)


class SolarNERExtractor:
    """
    Trích xuất thực thể đặc thù domain Năng lượng Mặt trời.
    Hỗ trợ 2 chế độ:
      - rule_based: dùng regex/dictionary (nhanh, không cần model)
      - model: dùng HuggingFace NER model (chính xác hơn)

    Args:
        config: Dict cấu hình. Các key:
            - mode: "rule_based" | "model"
            - model_name: tên HF model (khi mode="model")
    """

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self.mode = self.config.get("mode", "rule_based")
        self._model_pipeline = None
        if self.mode == "model":
            self._model_pipeline = self._load_model()

    def _load_model(self):
        try:
            from transformers import pipeline
            model_name = self.config.get(
                "model_name", "NlpHUST/ner-vietnamese-electra-base"
            )
            logger.info("Nạp NER model: %s", model_name)
            return pipeline("ner", model=model_name, aggregation_strategy="simple")
        except ImportError:
            logger.warning("transformers không có — fallback sang rule_based")
            self.mode = "rule_based"
            return None

    def extract(self, text: str) -> list[Entity]:
        """Trích xuất tất cả thực thể từ một đoạn văn bản."""
        if not text or not text.strip():
            return []

        if self.mode == "model" and self._model_pipeline:
            return self._extract_with_model(text)
        return self._extract_rule_based(text)

    def _extract_rule_based(self, text: str) -> list[Entity]:
        entities: list[Entity] = []

        # CAPACITY
        for m in CAPACITY_PATTERN.finditer(text):
            entities.append(Entity(m.group(), "CAPACITY", m.start(), m.end()))

        # PRICE
        for m in PRICE_PATTERN.finditer(text):
            entities.append(Entity(m.group(), "PRICE", m.start(), m.end()))

        # BRAND
        for brand in SOLAR_BRANDS:
            idx = text.find(brand)
            if idx != -1:
                entities.append(Entity(brand, "BRAND", idx, idx + len(brand)))

        # PROVINCE
        for province in VIETNAMESE_PROVINCES:
            idx = text.find(province)
            if idx != -1:
                entities.append(Entity(province, "PROVINCE", idx, idx + len(province)))

        # REGULATION
        for m in REGULATION_PATTERN.finditer(text):
            entities.append(Entity(m.group(), "REGULATION", m.start(), m.end()))

        # ENERGY_TYPE
        for m in ENERGY_TYPE_PATTERN.finditer(text):
            entities.append(Entity(m.group(), "ENERGY_TYPE", m.start(), m.end()))

        # Sắp xếp theo vị trí xuất hiện
        entities.sort(key=lambda e: e.start)
        return entities

    def _extract_with_model(self, text: str) -> list[Entity]:
        """Trích xuất sử dụng HuggingFace model."""
        raw = self._model_pipeline(text)
        return [
            Entity(
                text=r["word"],
                label=r["entity_group"],
                start=r["start"],
                end=r["end"],
                confidence=r["score"],
            )
            for r in raw
        ]

    def process_batch(self, input_path: str) -> dict:
        """Entry point cho pipeline runner."""
        if not input_path or not Path(input_path).exists():
            return {"processed": 0, "total_entities": 0}

        with open(input_path, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        all_entities = [e for line in lines for e in self.extract(line)]

        label_counts: dict[str, int] = {}
        for e in all_entities:
            label_counts[e.label] = label_counts.get(e.label, 0) + 1

        return {
            "processed": len(lines),
            "total_entities": len(all_entities),
            "label_distribution": label_counts,
        }
