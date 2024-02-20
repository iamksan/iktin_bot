from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.back import back
from database import db
from utils import bot

router = Router()

user_for_chat = []


class Call_admin(StatesGroup):
    user_id = State()
    call = State()


@router.message(StateFilter(None), F.text.lower() == 'вызовы клиентов')
async def cmd_call_admin(message: Message,  state: State):
    admin_id = message.from_user.id
    if db.get_calls_admin(admin_id=admin_id) != []:
        call_data = db.get_calls_admin(admin_id=admin_id)
        for user_id, admin_id, status in call_data:
            await bot.send_message(
                chat_id=admin_id,
                text=f'Пользователь {user_id} ожидает вашего ответа.'
            )
        await bot.send_message(
                chat_id=admin_id,
                text='Чтоб ответить пользователь напишите его id.'
            )
    else:
        await bot.send_message(
                chat_id=admin_id,
                text='Клиенты вас не вызывали.'
            )


@router.message(StateFilter(None), F.text.regexp(r'\d+'))
async def cmd_call_for_admin(message: Message,  state: FSMContext):
    user_id = message.text
    user_for_chat.append(user_id)
    await state.update_data(user_id=user_id)
    await message.answer('Вы подключились к чату.')
    await bot.send_message(user_id, 'админ подключился')
    await state.set_state(Call_admin.call)


@router.message(Call_admin.call)
async def cmd_call(message: Message,  state: FSMContext):
    call_data = await state.get_data()
    kb = [
        [types.KeyboardButton(text="Завершить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    if message.text == 'Завершить':
        await bot.send_message(call_data['user_id'], 'админ завершил общение')
        db.del_call(user_id=call_data['user_id'])
        await back(message, state)
    else:
        await bot.send_message(call_data['user_id'],
                               message.text,
                               reply_markup=keyboard)
