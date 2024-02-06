import asyncio
import logging

from aiogram import Bot, Dispatcher

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from config import config
from handlers import choose, invoice_user


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(
        choose.router,
        invoice_user.router
        )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
