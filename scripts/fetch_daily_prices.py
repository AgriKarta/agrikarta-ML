from __future__ import annotations

import asyncio

from app.services.ingestion import fetch_daily_prices, save_prices


async def run_etl() -> None:
    cleaned = await fetch_daily_prices()
    path = save_prices(cleaned)
    print(f"Saved cleaned Java staple prices to {path}")


if __name__ == "__main__":
    asyncio.run(run_etl())
