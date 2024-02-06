from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# from utils import bot

available_choice = ["Да", "Нет", "На главную"]

router = Router()

class Invoice(StatesGroup):

    discription = State()
    weight = State()
    dimensions = State()
    shipping_address = State()
    receiving_address = State()
    payment_method = State()
    choice = State()


@router.message(StateFilter(None), F.text.lower() == 'накладная')
async def cmd_feedback(message: Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text='Описание груза.', reply_markup=keyboard
    )
    await state.set_state(Invoice.weight)


@router.message(Invoice.weight)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(discription=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="Вес груза.",
        reply_markup=keyboard
    )
    await state.set_state(Invoice.dimensions)


@router.message(Invoice.dimensions)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="Габариты груза.",
        reply_markup=keyboard
    )
    await state.set_state(Invoice.shipping_address)


@router.message(Invoice.shipping_address)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(dimensions=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="Точный адрес отправки.",
        reply_markup=keyboard
    )
    await state.set_state(Invoice.receiving_address)


@router.message(Invoice.receiving_address)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(shipping_address=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="Точный адрес получения.",
        reply_markup=keyboard
    )
    await state.set_state(Invoice.payment_method)


@router.message(Invoice.payment_method)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(receiving_address=message.text)
    kb = [
        [types.KeyboardButton(text="На главную")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        )
    await message.answer(
        text="Способ оплаты.",
        reply_markup=keyboard
    )
    await state.set_state(Invoice.payment_method)


@router.message(Invoice.payment_method)
async def vacancy_add(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    user_data = await state.get_data()
    kb = [
        [
            types.KeyboardButton(text="Да")
        ],
        [
            types.KeyboardButton(text="Нет")
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
        text=f"Описание груза - {user_data['discription']}.\n"
        f"Вес груза - {user_data['weight']}.\n"
        f"Габариты груза - {user_data['dimensions']}.\n"
        f"Точный адрес отправки - {user_data['shipping_address']}.\n"
        f"Точный адрес получения - {user_data['receiving_address']}.\n"
        f"Способ оплаты - {user_data['payment_method']}.\n"
        "Все верно?",
        reply_markup=keyboard
        )
    await state.set_state(Invoice.choice)


# @router.message(Invoice.choice, F.text.in_(available_choice))
# async def cmd_choic(message: Message, state: FSMContext):
#     await state.update_data(choice=message.text)
#     user_data = await state.get_data()
#     if message.text == 'Да':
#         invoice = [
#             ''
#         ]
#         f"Описание груза - {user_data['discription']}.\n"
#         f"Вес груза - {user_data['weight']}.\n"
#         f"Габариты груза - {user_data['dimensions']}.\n"
#         f"Точный адрес отправки - {user_data['shipping_address']}.\n"
#         f"Точный адрес получения - {user_data['receiving_address']}.\n"
#         f"Способ оплаты - {user_data['payment_method']}.\n"
#         await message.answer(text='Спасибо за оставленную вакансию.'
#                              'Мы свяжется с вами в ближайшее время!')
#         await back(message, state)
#     else:
#         await back(message, state)
