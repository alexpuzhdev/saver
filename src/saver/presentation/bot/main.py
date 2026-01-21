from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher

from saver.application.use_cases.download_video import DownloadVideoUseCase
from saver.config import SettingsLoader
from saver.infrastructure.downloader.yt_dlp_downloader import YtDlpDownloader
from saver.presentation.bot.handlers import BotContext, router


def build_context() -> BotContext:
    settings = SettingsLoader().load()
    downloader = YtDlpDownloader(
        downloads_dir=settings.app.downloads_dir,
        temp_dir=settings.app.temp_dir,
    )
    use_case = DownloadVideoUseCase(downloader=downloader)
    return BotContext(download_use_case=use_case)


async def main() -> None:
    settings = SettingsLoader().load()
    bot = Bot(token=settings.bot.token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    dispatcher["ctx"] = build_context()

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
