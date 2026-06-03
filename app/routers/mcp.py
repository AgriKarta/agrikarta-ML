from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter

from app.services.factory import get_active_logistics_tracking, get_factory_storage_status
from app.services.ingestion import get_todays_market_price, load_local_prices
from app.services.model import TransformerForecaster

router = APIRouter(prefix="/api/v1", tags=["mcp"])
forecaster = TransformerForecaster.default()


def _extract_price_series(prices_df):
    if "price" not in prices_df.columns:
        return prices_df.assign(price=0.0)["price"]
    return prices_df["price"]


@router.get("/pricing-overview")
async def pricing_overview() -> dict[str, object]:
    prices_df = load_local_prices()
    todays_price = get_todays_market_price(prices_df)
    predictions = forecaster.predict_next_7_days(_extract_price_series(prices_df))

    start = date.today() + timedelta(days=1)
    trend = [
        {
            "date": (start + timedelta(days=offset)).isoformat(),
            "predicted_price": predictions[offset],
        }
        for offset in range(7)
    ]

    return {
        "today_market_price": todays_price,
        "prediction_7_days": trend,
        "factory_storage": get_factory_storage_status(),
        "active_logistics": get_active_logistics_tracking(),
    }
