"""
src/api/routers/solar.py
─────────────────────────
Solar-specific endpoints — tính toán kỹ thuật đặc thù cho domain điện mặt trời.
Các endpoint này không dùng LLM mà tính trực tiếp từ công thức vật lý.
"""

from __future__ import annotations

import logging
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── Dữ liệu bức xạ mặt trời theo tỉnh/thành (kWh/m²/ngày, trung bình năm) ──
SOLAR_IRRADIANCE_BY_PROVINCE: dict[str, float] = {
    "hà nội": 3.8, "hải phòng": 3.7, "quảng ninh": 3.6,
    "đà nẵng": 4.9, "thừa thiên huế": 4.5, "quảng nam": 4.8,
    "quảng ngãi": 4.9, "bình định": 5.0, "phú yên": 5.1,
    "khánh hòa": 5.2, "ninh thuận": 5.5, "bình thuận": 5.4,
    "hồ chí minh": 4.9, "bình dương": 4.9, "đồng nai": 4.8,
    "long an": 4.8, "tiền giang": 4.7, "vĩnh long": 4.7,
    "cần thơ": 4.6, "an giang": 4.7, "kiên giang": 4.8,
    "đắk lắk": 5.0, "gia lai": 5.1, "kon tum": 4.9,
    "lâm đồng": 4.7, "đắk nông": 5.0,
}

DEFAULT_IRRADIANCE = 4.5  # Giá trị mặc định nếu không tìm thấy tỉnh


# ─── Request / Response models ────────────────────────────────────────────────

class RoofType(str, Enum):
    TILE = "ngói"
    METAL = "tôn"
    CONCRETE = "bê tông"
    OTHER = "khác"


class SystemCalculateRequest(BaseModel):
    monthly_kwh: float = Field(..., gt=0, le=10_000,
                               description="Lượng điện tiêu thụ hàng tháng (kWh)")
    province: str = Field(..., min_length=2, max_length=50,
                          description="Tỉnh/thành phố lắp đặt")
    roof_type: RoofType = RoofType.TILE
    available_area_m2: float | None = Field(
        None, gt=0, le=2000,
        description="Diện tích mái sẵn có (m²) — để kiểm tra đủ chỗ không",
    )

    @field_validator("province", mode="before")
    @classmethod
    def normalize_province(cls, v: str) -> str:
        return v.strip().lower()


class SystemCalculateResponse(BaseModel):
    province: str
    irradiance_kwh_per_m2_day: float
    recommended_capacity_kwp: float
    estimated_area_m2: float
    area_sufficient: bool | None
    annual_output_kwh: float
    co2_saved_kg_per_year: float
    estimated_cost_vnd_million: float
    payback_years: float
    notes: list[str]


class ROIRequest(BaseModel):
    capacity_kwp: float = Field(..., gt=0, le=1000)
    province: str
    system_cost_million_vnd: float = Field(..., gt=0)
    electricity_price_vnd_per_kwh: float = Field(default=2_000, gt=0)
    annual_degradation_pct: float = Field(default=0.5, ge=0, le=5)

    @field_validator("province", mode="before")
    @classmethod
    def normalize_province(cls, v: str) -> str:
        return v.strip().lower()


class ROIResponse(BaseModel):
    annual_output_kwh: float
    annual_savings_million_vnd: float
    simple_payback_years: float
    irr_20yr_pct: float | None
    lcoe_vnd_per_kwh: float


# ─── Tính toán nội bộ ─────────────────────────────────────────────────────────

def _calc_capacity(monthly_kwh: float, irradiance: float,
                   performance_ratio: float = 0.80) -> float:
    """Công suất cần thiết (kWp) = Tiêu thụ / (bức xạ × PR × 30)."""
    daily_kwh = monthly_kwh / 30
    return round(daily_kwh / (irradiance * performance_ratio), 2)


def _calc_area(capacity_kwp: float, panel_watt: int = 405,
               panel_area_m2: float = 1.92) -> float:
    """Diện tích ước tính = số tấm × diện tích mỗi tấm."""
    panels = capacity_kwp * 1000 / panel_watt
    return round(panels * panel_area_m2, 1)


def _cost_estimate(capacity_kwp: float) -> float:
    """Chi phí ước tính (triệu VND) theo thang bậc công suất."""
    if capacity_kwp <= 5:
        return round(capacity_kwp * 15, 1)
    if capacity_kwp <= 20:
        return round(capacity_kwp * 13.5, 1)
    return round(capacity_kwp * 12, 1)


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/solar/calculate",
    response_model=SystemCalculateResponse,
    summary="Tính toán hệ thống điện mặt trời phù hợp",
)
async def calculate_system(req: SystemCalculateRequest) -> SystemCalculateResponse:
    """
    Tính toán công suất, diện tích, chi phí và thời gian hoàn vốn
    cho hệ thống điện mặt trời dựa trên lượng tiêu thụ và vị trí lắp đặt.
    """
    irradiance = SOLAR_IRRADIANCE_BY_PROVINCE.get(req.province, DEFAULT_IRRADIANCE)
    capacity_kwp = _calc_capacity(req.monthly_kwh, irradiance)
    area_m2 = _calc_area(capacity_kwp)
    annual_output = round(capacity_kwp * irradiance * 0.80 * 365, 0)
    co2_saved = round(annual_output * 0.6, 0)          # 0.6 kg CO₂/kWh (lưới VN)
    cost = _cost_estimate(capacity_kwp)
    electricity_bill_monthly = req.monthly_kwh * 2_200 / 1_000_000  # triệu VND
    annual_savings = electricity_bill_monthly * 12
    payback = round(cost / annual_savings, 1) if annual_savings > 0 else 0

    notes = []
    if req.province not in SOLAR_IRRADIANCE_BY_PROVINCE:
        notes.append(
            f"Chưa có dữ liệu bức xạ chính xác cho '{req.province}' "
            f"— dùng giá trị trung bình quốc gia {DEFAULT_IRRADIANCE} kWh/m²/ngày."
        )
    if capacity_kwp > 100:
        notes.append("Hệ thống lớn hơn 100 kWp cần khảo sát hiện trường và đấu nối lưới chuyên nghiệp.")

    area_sufficient = None
    if req.available_area_m2 is not None:
        area_sufficient = req.available_area_m2 >= area_m2
        if not area_sufficient:
            actual_cap = _calc_capacity(req.monthly_kwh, irradiance) * (req.available_area_m2 / area_m2)
            notes.append(
                f"Diện tích mái {req.available_area_m2} m² chỉ đủ cho ~{actual_cap:.1f} kWp. "
                "Cân nhắc giảm tải hoặc dùng tấm pin hiệu suất cao hơn."
            )

    return SystemCalculateResponse(
        province=req.province,
        irradiance_kwh_per_m2_day=irradiance,
        recommended_capacity_kwp=capacity_kwp,
        estimated_area_m2=area_m2,
        area_sufficient=area_sufficient,
        annual_output_kwh=annual_output,
        co2_saved_kg_per_year=co2_saved,
        estimated_cost_vnd_million=cost,
        payback_years=payback,
        notes=notes,
    )


@router.post(
    "/solar/roi",
    response_model=ROIResponse,
    summary="Tính ROI và LCOE cho hệ thống đã biết công suất",
)
async def calculate_roi(req: ROIRequest) -> ROIResponse:
    """Tính lợi nhuận đầu tư 20 năm cho hệ thống đã biết công suất và chi phí."""
    irradiance = SOLAR_IRRADIANCE_BY_PROVINCE.get(req.province, DEFAULT_IRRADIANCE)
    annual_output = req.capacity_kwp * irradiance * 0.80 * 365

    # Tính NPV đơn giản qua 20 năm (không chiết khấu thời gian)
    total_output_20yr = sum(
        annual_output * ((1 - req.annual_degradation_pct / 100) ** yr)
        for yr in range(20)
    )

    annual_savings = round(annual_output * req.electricity_price_vnd_per_kwh / 1_000_000, 2)
    simple_payback = round(req.system_cost_million_vnd / annual_savings, 1) if annual_savings else 0
    lcoe = round(
        req.system_cost_million_vnd * 1_000_000 / total_output_20yr, 0
    ) if total_output_20yr else 0

    return ROIResponse(
        annual_output_kwh=round(annual_output, 0),
        annual_savings_million_vnd=annual_savings,
        simple_payback_years=simple_payback,
        irr_20yr_pct=None,   # TODO: implement Newton-Raphson IRR
        lcoe_vnd_per_kwh=lcoe,
    )
