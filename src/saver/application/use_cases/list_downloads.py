from __future__ import annotations

from dataclasses import dataclass

from saver.domain.entities.download_record import DownloadRecord
from saver.domain.repositories.download_repository import DownloadRepository


@dataclass(slots=True)
class ListDownloadsUseCase:
    repository: DownloadRepository

    async def execute(self, limit: int = 20) -> list[DownloadRecord]:
        return await self.repository.list_recent(limit=limit)
