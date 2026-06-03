from fastapi import FastAPI

from app.routers.mcp import router as mcp_router

app = FastAPI(title="AGRI-KARTA MCP")
app.include_router(mcp_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
