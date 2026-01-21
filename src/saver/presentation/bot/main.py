from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher

from saver.config import Settings, SettingsLoader
from saver.infrastructure.downloader.yt_dlp_downloader import YtDlpDownloader
from saver.infrastructure.db.database import Base, Database
from saver.presentation.bot.handlers import BotContext, router


def build_context(settings: Settings) -> BotContext:
    downloader = YtDlpDownloader(
        downloads_dir=settings.app.downloads_dir,
        temp_dir=settings.app.temp_dir,
    )
    database = Database(settings.database.dsn)
    engine = database.create_engine()
    sessionmaker = database.create_sessionmaker(engine)
    return BotContext(downloader=downloader, sessionmaker=sessionmaker)


async def init_database(settings: Settings) -> None:
    database = Database(settings.database.dsn)
    engine = database.create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def main() -> None:
    settings = SettingsLoader().load()
    bot = Bot(token=settings.bot.token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await init_database(settings)
    dispatcher["ctx"] = build_context(settings)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
