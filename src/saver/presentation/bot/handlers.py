from __future__ import annotations

from dataclasses import dataclass

from aiogram import F, Router
from aiogram.types import Message

from saver.application.use_cases.download_video import DownloadVideoUseCase

router = Router()


@dataclass(slots=True)
class BotContext:
    download_use_case: DownloadVideoUseCase


@router.message(F.text == "/start")
async def start_command(message: Message) -> None:
    await message.answer("Отправьте ссылку на видео, и я попробую скачать его.")


@router.message(F.text.regexp(r"https?://"))
async def handle_video_link(message: Message, ctx: BotContext) -> None:
    url = message.text.strip()
    await message.answer("Скачиваю видео, подождите...")
    try:
        result = await ctx.download_use_case.execute(url)
    except Exception as exc:  # noqa: BLE001
        await message.answer(f"Не удалось скачать видео: {exc}")
        return

    await message.answer_video(video=result.file_path, caption=result.title)
