from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from saver.domain.entities.download_record import DownloadRecord
from saver.domain.repositories.download_repository import DownloadRepository
from saver.infrastructure.db.models import DownloadRecordModel


class SqlAlchemyDownloadRepository(DownloadRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, record: DownloadRecord) -> None:
        model = DownloadRecordModel(
            user_id=record.user_id,
            source_url=record.source_url,
            title=record.title,
            file_path=str(record.file_path),
            created_at=record.created_at,
        )
        self._session.add(model)
        await self._session.commit()
