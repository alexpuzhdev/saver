from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class DownloadRecord:
    user_id: int
    source_url: str
    title: str
    file_path: Path
    created_at: datetime
