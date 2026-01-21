from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL

from saver.domain.services.video_downloader import DownloadResult, VideoDownloader


@dataclass(slots=True)
class YtDlpDownloader(VideoDownloader):
    downloads_dir: Path
    temp_dir: Path

    async def download(self, url: str) -> DownloadResult:
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        return await asyncio.to_thread(self._download_sync, url)

    def _download_sync(self, url: str) -> DownloadResult:
        options: dict[str, Any] = {
            "outtmpl": str(self.downloads_dir / "%(title)s.%(ext)s"),
            "paths": {"temp": str(self.temp_dir)},
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            filename = ydl.prepare_filename(info)
        return DownloadResult(file_path=Path(filename), title=title)
