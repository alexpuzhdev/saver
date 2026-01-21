from __future__ import annotations

from fastapi import FastAPI

from saver.config import SettingsLoader
from saver.infrastructure.db.database import Database
from saver.presentation.api.routes.health import router as health_router
from saver.presentation.api.routes.downloads import ApiContext, get_context, router as downloads_router


def create_app() -> FastAPI:
    settings = SettingsLoader().load()
    database = Database(settings.database.dsn)
    engine = database.create_engine()
    sessionmaker = database.create_sessionmaker(engine)

    def _get_context() -> ApiContext:
        return ApiContext(sessionmaker=sessionmaker)

    app = FastAPI(title="Saver API")
    app.dependency_overrides[get_context] = _get_context
    app.include_router(health_router)
    app.include_router(downloads_router)
    return app


app = create_app()
