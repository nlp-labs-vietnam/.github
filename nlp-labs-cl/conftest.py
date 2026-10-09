"""
conftest.py — Shared pytest fixtures cho toàn bộ nlp-labs-cl
Tự động được nạp bởi pytest trước khi chạy bất kỳ test nào.
"""

import json
import tempfile
from pathlib import Path

import pytest


# ─── Text Fixtures ────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def solar_sentences() -> list[str]:
    """Các câu mẫu về domain năng lượng mặt trời — dùng chung toàn bộ test suite."""
    return [
        "Hệ thống điện mặt trời 5 kWp phù hợp cho hộ gia đình Hà Nội",
        "Inverter Growatt 5kW single phase hiệu suất 97.6%",
        "Quy hoạch Điện VIII mục tiêu 50% năng lượng tái tạo vào 2030",
        "Tấm pin LONGi 405W mono PERC lắp mái nhà Đà Nẵng",
        "Chi phí lắp đặt điện mặt trời khoảng 15 triệu đồng mỗi kWp",
        "Thời gian hoàn vốn trung bình từ 5 đến 7 năm tại miền Nam",
        "Inverter SMA Sunny Boy 3.0 kW xuất xứ Đức bảo hành 5 năm",
        "Bức xạ mặt trời tại Khánh Hòa trung bình 5.2 kWh/m²/ngày",
    ]


@pytest.fixture(scope="session")
def regulatory_sentences() -> list[str]:
    """Các câu về văn bản pháp luật điện lực."""
    return [
        "Theo Quy hoạch Điện VIII ban hành tháng 5/2023",
        "QĐ 500/QĐ-TTg về phê duyệt Quy hoạch điện quốc gia",
        "Nghị định 135 về cơ chế khuyến khích điện mặt trời mái nhà",
    ]


# ─── File Fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_text_file(tmp_path: Path, solar_sentences) -> Path:
    """File .txt tạm chứa solar_sentences — một câu mỗi dòng."""
    p = tmp_path / "solar_input.txt"
    p.write_text("\n".join(solar_sentences), encoding="utf-8")
    return p


@pytest.fixture
def tmp_jsonl_file(tmp_path: Path, solar_sentences) -> Path:
    """File .jsonl tạm với format RAG triplet."""
    p = tmp_path / "solar_pairs.jsonl"
    lines = [
        json.dumps(
            {"query": s, "positive": s + " (bổ sung)", "negative": "Câu không liên quan"},
            ensure_ascii=False,
        )
        for s in solar_sentences
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


@pytest.fixture
def tmp_csv_file(tmp_path: Path, solar_sentences) -> Path:
    """File .csv tạm với cột text và label."""
    p = tmp_path / "solar_data.csv"
    rows = ["text,label"] + [f'"{s}",solar' for s in solar_sentences]
    p.write_text("\n".join(rows), encoding="utf-8")
    return p


# ─── Config Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def base_tokenizer_config() -> dict:
    return {"backend": "whitespace", "keep_punctuation": True, "lowercase": False}


@pytest.fixture
def base_embedder_config() -> dict:
    return {"device": "cpu", "batch_size": 8, "normalize": True}


@pytest.fixture
def base_ner_config() -> dict:
    return {"mode": "rule_based"}
