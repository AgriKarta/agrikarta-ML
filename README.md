# agrikarta-ML

Python FastAPI-based Master Control Protocol (MCP) service for AGRI-KARTA.

## Components
- `app/routers`: API routers.
- `app/services/ingestion.py`: ETL fetch + outlier cleaning for Java staple prices.
- `app/services/model.py`: Transformer-based 7-day time-series forecaster.
- `app/services/factory.py`: Factory storage and active logistics payload providers.
- `scripts/fetch_daily_prices.py`: Script intended for daily scheduler/cron ETL runs.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /health`
- `GET /api/v1/pricing-overview`
