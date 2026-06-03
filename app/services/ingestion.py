from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import httpx
import pandas as pd

DATA_PATH = Path("data/java_staple_prices.csv")
DEFAULT_SOURCE_URL = "https://api.data.gov.id/v1/staple-prices/java"


def clean_outliers(df: pd.DataFrame, column: str = "price") -> pd.DataFrame:
    if df.empty:
        return df
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return df
    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)
    return df[(df[column] >= lower) & (df[column] <= upper)].copy()


async def fetch_daily_prices(source_url: str = DEFAULT_SOURCE_URL) -> pd.DataFrame:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(source_url)
        response.raise_for_status()
    payload = response.json()
    records = payload.get("data", payload)
    df = pd.DataFrame(records)

    if "date" not in df.columns:
        df["date"] = date.today().isoformat()
    if "price" not in df.columns:
        raise ValueError("Fetched data does not include a 'price' field")

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    return clean_outliers(df)


def save_prices(df: pd.DataFrame, destination: Path = DATA_PATH) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return destination


def load_local_prices(source: Path = DATA_PATH) -> pd.DataFrame:
    if not source.exists():
        return pd.DataFrame(columns=["date", "price"])
    df = pd.read_csv(source)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.dropna(subset=["price"]).copy()


def get_todays_market_price(df: pd.DataFrame, today: Optional[date] = None) -> float:
    if df.empty:
        return 0.0

    target_date = today or date.today()
    daily = df[df["date"] == target_date]
    if not daily.empty:
        return float(daily["price"].mean())
    return float(df.sort_values("date").iloc[-1]["price"])
