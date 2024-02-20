from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.back import back
from database import db
from utils import bot

available_choice = ["Да", "Нет", "На главную"]

router = Router()


class Call(StatesGroup):
    user_id = State()
    admin_info = State()
    admin = State()
    status = State()
    call = State()


@router.message(StateFilter(None), F.text.lower() == 'вызов менеджера')
async def cmd_call_user(message: Message,  state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    admin_id = db.get_user_admin(user_id=user_id)
    await state.update_data(admin_id=admin_id[0])
    await state.update_data(status='open')
    user_data = await state.get_data()
    data = tuple(user_data.values())
    db.add_call(data)

    kb = [
        [types.KeyboardButton(text="Завершить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await bot.send_message(chat_id=admin_id[0],
                           text=f"Пользователь {message.from_user.id} ожидает менеджера.")
    await message.answer(text='Менеджер скоро подключится.',
                         reply_markup=keyboard)
    await state.set_state(Call.call)


@router.message(Call.call)
async def cmd_call_admin(message: Message,  state: FSMContext):
    user_id = message.from_user.id
    admin_id = db.get_user_admin(user_id=user_id)
    kb = [
        [types.KeyboardButton(text="Завершить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    if message.text == 'Завершить':
        await bot.send_message(admin_id[0], 'пользователь завершил общение')
        db.del_call(user_id=user_id)
        await back(message, state)
    else:
        await bot.send_message(admin_id[0],
                               message.text,
                               reply_markup=keyboard)
