from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters.command import Command

from database import db
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup


router = Router()


class reg(StatesGroup):
    data = State()


@router.message(Command('start'))
async def cmd_start(message: Message, state=FSMContext):
    user_id = message.from_user.id
    try:
        user_id not in db.get_user_id(user_id=user_id)
        await state.update_data(user_id=user_id)
        await state.update_data(username=message.from_user.username)
        await state.update_data(role='user')
        user_data = await state.get_data()
        data = tuple(user_data.values())
        db.add_user(data)
        await state.clear()
    except:
        if 'user' in db.get_user_role(user_id=user_id):
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
        else:
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
