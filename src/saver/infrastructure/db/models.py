from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from saver.infrastructure.db.database import Base


class DownloadRecordModel(Base):
    __tablename__ = "download_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    source_url: Mapped[str] = mapped_column(String(length=2048), nullable=False)
    title: Mapped[str] = mapped_column(String(length=512), nullable=False)
    file_path: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
