from __future__ import annotations

from dataclasses import dataclass

from saver.domain.services.video_downloader import DownloadResult, VideoDownloader


@dataclass(slots=True)
class DownloadVideoUseCase:
    downloader: VideoDownloader

    async def execute(self, url: str) -> DownloadResult:
        return await self.downloader.download(url)
