from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from saver.application.use_cases.list_downloads import ListDownloadsUseCase
from saver.domain.entities.download_record import DownloadRecord
from saver.infrastructure.db.repositories.download_repository import SqlAlchemyDownloadRepository

router = APIRouter(prefix="/downloads", tags=["downloads"])


@dataclass(slots=True)
class ApiContext:
    sessionmaker: async_sessionmaker[AsyncSession]


def get_context() -> ApiContext:  # placeholder for DI wiring
    raise RuntimeError("ApiContext dependency not configured")


class DownloadRecordResponse(BaseModel):
    user_id: int
    source_url: str
    title: str
    file_path: Path
    created_at: datetime

    @classmethod
    def from_domain(cls, record: DownloadRecord) -> "DownloadRecordResponse":
        return cls(
            user_id=record.user_id,
            source_url=record.source_url,
            title=record.title,
            file_path=record.file_path,
            created_at=record.created_at,
        )


@router.get("", response_model=list[DownloadRecordResponse])
async def list_downloads(
    limit: int = 20, ctx: ApiContext = Depends(get_context)
) -> list[DownloadRecordResponse]:
    async with ctx.sessionmaker() as session:
        repository = SqlAlchemyDownloadRepository(session)
        use_case = ListDownloadsUseCase(repository=repository)
        records = await use_case.execute(limit=limit)
    return [DownloadRecordResponse.from_domain(record) for record in records]
