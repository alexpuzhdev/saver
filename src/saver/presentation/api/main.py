from __future__ import annotations

from fastapi import FastAPI

from saver.presentation.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="Saver API")
    app.include_router(health_router)
    return app


app = create_app()
