from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.command import Command

router = Router()

admins = [812750445]

@router.message(Command('start'))
async def cmd_start(message: Message):
    if message.from_user.id in admins:
        kb = [
            [types.KeyboardButton(text="Чаты с клиентами")],
            [types.KeyboardButton(text="Претензии от клиентов")],
            [types.KeyboardButton(text="На главную")]
            ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
            )
        await message.answer(
            "Телеграм-бот предназначен для чатов с клиентами и претензий от клиентов.",
            reply_markup=keyboard
            )
    else:
        kb = [
            [
                types.KeyboardButton(text="Накладная"),
                types.KeyboardButton(text="Претензия")
            ],
            [types.KeyboardButton(text="Вызов менеджера")],
            [types.KeyboardButton(text="На главную")]
            ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
            )
        await message.answer(
            "Телеграм-бот предназначен для создания накладных, регистрации претензий, вызоыва менеджера.",
            reply_markup=keyboard
            )
