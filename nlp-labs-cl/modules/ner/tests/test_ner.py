"""
modules/ner/tests/test_ner.py
──────────────────────────────
Unit tests cho SolarNERExtractor (rule-based mode).
Chạy: pytest modules/ner/tests/ -v
"""

import pytest
from modules.ner.ner import Entity, SolarNERExtractor


@pytest.fixture
def extractor():
    return SolarNERExtractor({"mode": "rule_based"})


class TestSolarNERExtractor:
    def test_extract_capacity(self, extractor):
        entities = extractor.extract("Hệ thống 5 kWp lắp tại nhà")
        labels = [e.label for e in entities]
        assert "CAPACITY" in labels
        capacity = next(e for e in entities if e.label == "CAPACITY")
        assert "5" in capacity.text
        assert "kWp" in capacity.text

    def test_extract_multiple_capacities(self, extractor):
        entities = extractor.extract("Hệ thống 3 kWp và 10 kWp")
        capacities = [e for e in entities if e.label == "CAPACITY"]
        assert len(capacities) == 2

    def test_extract_brand(self, extractor):
        entities = extractor.extract("Inverter Growatt 5kW chất lượng cao")
        brands = [e for e in entities if e.label == "BRAND"]
        assert len(brands) >= 1
        assert any("Growatt" in e.text for e in brands)

    def test_extract_province(self, extractor):
        entities = extractor.extract("Lắp đặt điện mặt trời tại Đà Nẵng")
        provinces = [e for e in entities if e.label == "PROVINCE"]
        assert len(provinces) >= 1
        assert any("Đà Nẵng" in e.text for e in provinces)

    def test_extract_price(self, extractor):
        entities = extractor.extract("Chi phí khoảng 80 triệu đồng")
        prices = [e for e in entities if e.label == "PRICE"]
        assert len(prices) >= 1

    def test_extract_regulation(self, extractor):
        entities = extractor.extract("Theo Quy hoạch Điện VIII năm 2023")
        regs = [e for e in entities if e.label == "REGULATION"]
        assert len(regs) >= 1

    def test_extract_energy_type(self, extractor):
        entities = extractor.extract("điện mặt trời ngày càng phổ biến")
        energy = [e for e in entities if e.label == "ENERGY_TYPE"]
        assert len(energy) >= 1

    def test_extract_empty_text(self, extractor):
        assert extractor.extract("") == []
        assert extractor.extract("   ") == []

    def test_entities_sorted_by_position(self, extractor):
        entities = extractor.extract("5 kWp Growatt lắp tại Hà Nội giá 80 triệu")
        for i in range(1, len(entities)):
            assert entities[i].start >= entities[i - 1].start

    def test_full_solar_sentence(self, extractor):
        """Kiểm tra đoạn văn đầy đủ của domain."""
        text = (
            "Lắp hệ thống điện mặt trời 10 kWp dùng tấm pin Jinko "
            "và inverter Growatt tại Khánh Hòa, tổng chi phí khoảng 120 triệu đồng. "
            "Theo Quy hoạch Điện VIII, năng lượng tái tạo sẽ chiếm 50% vào 2030."
        )
        entities = extractor.extract(text)
        found_labels = {e.label for e in entities}
        assert "CAPACITY" in found_labels
        assert "BRAND" in found_labels
        assert "PROVINCE" in found_labels
        assert "PRICE" in found_labels
        assert "REGULATION" in found_labels
        assert "ENERGY_TYPE" in found_labels

    def test_process_batch_nonexistent(self, extractor):
        result = extractor.process_batch("/no/such/file.txt")
        assert result["processed"] == 0
        assert result["total_entities"] == 0
