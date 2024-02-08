import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import choose, invoice_user, back, claim_user


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        choose.router,
        back.router,
        invoice_user.router,
        claim_user.router
        )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
