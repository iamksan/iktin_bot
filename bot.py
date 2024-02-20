import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import claim, invoice, back, call, call_admin, start


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher() 
    dp.include_routers(
        start.router,
        back.router,
        invoice.router,
        claim.router,    
        call.router,
        call_admin.router
        )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
