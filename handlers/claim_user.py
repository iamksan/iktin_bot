from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import db

from handlers.back import back
from utils import bot


available_choice = ["Отправить", "На главную"]

router = Router()


class Claim(StatesGroup):
    user_id = State()
    username = State()
    email = State()
    description = State()
    amount = State()
    photo = State()
    close_or_open = State()
    choice = State()


@router.message(StateFilter(None), F.text.lower() == 'претензия')
async def cmd_claim(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(username=message.from_user.username)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text='E-mail для ответа на претензию.', reply_markup=keyboard
    )
    await state.set_state(Claim.description)


@router.message(Claim.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="описание ситуации.",
        reply_markup=keyboard
    )
    await state.set_state(Claim.amount)


@router.message(Claim.amount)
async def amount(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="требуемая сумма.",
        reply_markup=keyboard
    )
    await state.set_state(Claim.photo)


@router.message(Claim.photo)
async def photo(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="фото/сканы.",
        reply_markup=keyboard
    )
    await state.set_state(Claim.choice)


@router.message(Claim.choice)
async def vacancy_add(message: Message, state: FSMContext):
    photo_file = message.text
    photo_info = message.photo[-1].file_id
    await state.update_data(photo=photo_file)
    await state.update_data(close_or_open='open')
    user_data = await state.get_data()
    kb = [
        [
            types.KeyboardButton(text="Отправить")
        ],
        [
            types.KeyboardButton(text="На главную")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text=f"E-mail для ответа на претензию - {user_data['email']}.\n"
        f"описание ситуации - {user_data['description']}.\n"
        f"требуемая сумма - {user_data['amount']}.\n"
        "Все верно?",
        reply_markup=keyboard
        )
    await bot.send_photo(message.from_user.id, photo=photo_info)


@router.message(F.text.in_(available_choice))
async def cmd_safe(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text == 'Отправить':
        text = (f"E-mail для ответа на претензию - {user_data['email']}.\n"
                f"описание ситуации - {user_data['description']}.\n"
                f"требуемая сумма - {user_data['amount']}.\n")
        await bot.send_message(812750445, text=text)
        data = tuple(user_data.values())
        db.add_claim(data)
        await back(message, state)
    else:
        await back(message, state)
