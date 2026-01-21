from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from saver.domain.entities.download_record import DownloadRecord
from saver.domain.repositories.download_repository import DownloadRepository
from saver.domain.services.video_downloader import DownloadResult, VideoDownloader


@dataclass(slots=True)
class DownloadVideoUseCase:
    downloader: VideoDownloader
    repository: DownloadRepository

    async def execute(self, url: str, user_id: int) -> DownloadResult:
        result = await self.downloader.download(url)
        await self.repository.add(
            DownloadRecord(
                user_id=user_id,
                source_url=url,
                title=result.title,
                file_path=result.file_path,
                created_at=datetime.utcnow(),
            )
        )
        return result
