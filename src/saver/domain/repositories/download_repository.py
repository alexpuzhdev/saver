from __future__ import annotations

from typing import Protocol

from saver.domain.entities.download_record import DownloadRecord


class DownloadRepository(Protocol):
    async def add(self, record: DownloadRecord) -> None:
        raise NotImplementedError

    async def list_recent(self, limit: int) -> list[DownloadRecord]:
        raise NotImplementedError
