from __future__ import annotations

from dataclasses import dataclass

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from saver.application.use_cases.download_video import DownloadVideoUseCase
from saver.domain.services.video_downloader import VideoDownloader
from saver.infrastructure.db.repositories.download_repository import SqlAlchemyDownloadRepository

router = Router()


@dataclass(slots=True)
class BotContext:
    downloader: VideoDownloader
    sessionmaker: async_sessionmaker[AsyncSession]


@router.message(F.text == "/start")
async def start_command(message: Message) -> None:
    await message.answer("Отправьте ссылку на видео, и я попробую скачать его.")


@router.message(F.text.regexp(r"https?://"))
async def handle_video_link(message: Message, ctx: BotContext) -> None:
    url = message.text.strip()
    if message.from_user is None:
        await message.answer("Не удалось определить пользователя.")
        return
    await message.answer("Скачиваю видео, подождите...")
    try:
        async with ctx.sessionmaker() as session:
            repository = SqlAlchemyDownloadRepository(session)
            use_case = DownloadVideoUseCase(downloader=ctx.downloader, repository=repository)
            result = await use_case.execute(url, user_id=message.from_user.id)
    except Exception as exc:  # noqa: BLE001
        await message.answer(f"Не удалось скачать видео: {exc}")
        return

    await message.answer_video(video=result.file_path, caption=result.title)
    try:
        result.file_path.unlink()
    except FileNotFoundError:
        pass
