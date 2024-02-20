from aiogram import Router, F, types

from handlers.start import cmd_start

router = Router()


@router.message(F.text.lower() == "на главную")
async def back(message: types.Message, state):
    await state.clear()
    await cmd_start(message)
