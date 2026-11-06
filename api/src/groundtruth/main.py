"""FastAPI application entry point."""

from typing import Annotated, Literal

from fastapi import Depends, FastAPI, Response, status
from pydantic import BaseModel

from groundtruth.config import Settings, get_settings
from groundtruth.db import check_database

app = FastAPI(title="GroundTruth API", version="0.1.0")


class HealthResponse(BaseModel):
    """Shape of the /health response body."""

    status: Literal["ok", "degraded"]
    database: Literal["up", "down"]
    environment: str


@app.get("/health", response_model=HealthResponse)
def health(
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Report whether the API is running and can reach Postgres.

    Declared with plain `def` (not `async def`) because psycopg's connect call blocks.
    FastAPI runs plain functions in a worker thread so the event loop stays free.
    """
    database_up = check_database(str(settings.database_url))
    if not database_up:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(
        status="ok" if database_up else "degraded",
        database="up" if database_up else "down",
        environment=settings.app_env,
    )
