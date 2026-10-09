"""
tests/test_solar_router.py
───────────────────────────
Unit tests cho /api/v1/solar/calculate và /api/v1/solar/roi endpoints.
Không cần LLM hay ChromaDB — test tính toán vật lý thuần túy.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestSolarCalculate:
    def test_basic_calculation(self):
        resp = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 300,
            "province": "Hà Nội",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["recommended_capacity_kwp"] > 0
        assert data["estimated_area_m2"] > 0
        assert data["annual_output_kwh"] > 0
        assert data["payback_years"] > 0

    def test_high_irradiance_province(self):
        resp_hn = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 300, "province": "Hà Nội"
        })
        resp_nt = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 300, "province": "Ninh Thuận"
        })
        # Ninh Thuận có bức xạ cao hơn → cần ít kWp hơn
        assert resp_nt.json()["recommended_capacity_kwp"] < resp_hn.json()["recommended_capacity_kwp"]

    def test_unknown_province_uses_default(self):
        resp = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 200, "province": "Tỉnh Không Tồn Tại"
        })
        assert resp.status_code == 200
        notes = resp.json()["notes"]
        assert any("trung bình" in n for n in notes)

    def test_area_check_sufficient(self):
        resp = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 200,
            "province": "Đà Nẵng",
            "available_area_m2": 100,
        })
        data = resp.json()
        assert data["area_sufficient"] is True

    def test_area_check_insufficient(self):
        resp = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": 2000,
            "province": "Đà Nẵng",
            "available_area_m2": 5,
        })
        data = resp.json()
        assert data["area_sufficient"] is False

    def test_invalid_monthly_kwh(self):
        resp = client.post("/api/v1/solar/calculate", json={
            "monthly_kwh": -100, "province": "Hà Nội"
        })
        assert resp.status_code == 422


class TestSolarROI:
    def test_roi_basic(self):
        resp = client.post("/api/v1/solar/roi", json={
            "capacity_kwp": 5.0,
            "province": "Khánh Hòa",
            "system_cost_million_vnd": 75,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["annual_output_kwh"] > 0
        assert data["simple_payback_years"] > 0
        assert data["lcoe_vnd_per_kwh"] > 0

    def test_roi_payback_reasonable(self):
        """Thời gian hoàn vốn điển hình 5–10 năm."""
        resp = client.post("/api/v1/solar/roi", json={
            "capacity_kwp": 5.0,
            "province": "Hồ Chí Minh",
            "system_cost_million_vnd": 75,
            "electricity_price_vnd_per_kwh": 2200,
        })
        data = resp.json()
        assert 3 <= data["simple_payback_years"] <= 15


class TestHealth:
    def test_health_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
