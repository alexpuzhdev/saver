from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(slots=True)
class DownloadResult:
    file_path: Path
    title: str


class VideoDownloader(Protocol):
    async def download(self, url: str) -> DownloadResult:
        """Download video by URL and return file path and title."""
        raise NotImplementedError
