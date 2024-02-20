from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from fpdf import FPDF

from handlers.back import back
from database import db


available_choice = ["Да", "Нет", "На главную"]

router = Router()


class Invoice(StatesGroup):
    invoice_number = State()
    user_id = State()
    username = State()
    description = State()
    weight = State()
    dimensions = State()
    sending_address = State()
    receiving_address = State()
    payment_method = State()
    choice = State()
    safe = State()


@router.message(StateFilter(None), F.text.lower() == 'накладная')
async def cmd_ivoice(message: Message, state: FSMContext):
    invoice_number = db.count_invoice() + 1
    await state.update_data(invoice_number=invoice_number)
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
        text='Описание груза.', reply_markup=keyboard
    )
    await state.set_state(Invoice.weight)


@router.message(Invoice.weight)
async def weight(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
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
async def dimensions(message: Message, state: FSMContext):
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
    await state.set_state(Invoice.sending_address)


@router.message(Invoice.sending_address)
async def shipping_address(message: Message, state: FSMContext):
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
async def receiving_address(message: Message, state: FSMContext):
    await state.update_data(sending_address=message.text)
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
async def payment_method(message: Message, state: FSMContext):
    await state.update_data(receiving_address=message.text)
    kb = [
        [
            types.KeyboardButton(text="Наличные"),
            types.KeyboardButton(text="Безналичные")
        ],
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
    await state.set_state(Invoice.choice)


@router.message(Invoice.choice)
async def choice(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    invoice_data = await state.get_data()
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
        text=f"Номер накладной - {invoice_data['invoice_number']}\n"
        f"Описание груза - {invoice_data['description']}.\n"
        f"Вес груза - {invoice_data['weight']}.\n"
        f"Габариты груза - {invoice_data['dimensions']}.\n"
        f"Точный адрес отправки - {invoice_data['sending_address']}.\n"
        f"Точный адрес получения - {invoice_data['receiving_address']}.\n"
        f"Способ оплаты - {invoice_data['payment_method']}.\n"
        "Все верно?",
        reply_markup=keyboard
        )
    await state.set_state(Invoice.safe)


@router.message(Invoice.safe, F.text.in_(available_choice))
async def cmd_safe(message: Message, state: FSMContext):
    invoice_data = await state.get_data()
    if message.text == 'Да':
        text = [f"Номер накладной - {invoice_data['invoice_number']}",
                f"Описание груза - {invoice_data['description']}.",
                f"Вес груза - {invoice_data['weight']}.",
                f"Габариты груза - {invoice_data['dimensions']}.",
                f"Точный адрес отправки - {invoice_data['sending_address']}.",
                f"Точный адрес получения - {invoice_data['receiving_address']}.",
                f"Способ оплаты - {invoice_data['payment_method']}."]
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Roboto",
                     style="",
                     fname="Roboto/Roboto-Regular.ttf",
                     uni=True)
        pdf.set_font("Roboto", "", 10)
        for line in text:
            pdf.cell(0, 10, txt=line, ln=1, new_x="LMARGIN", new_y="NEXT")
        pdf.output(f"invoice/{message.from_user.username}-накладная.pdf")
        file = FSInputFile(F"invoice/{message.from_user.username}-накладная.pdf")
        await message.answer_document(file)
        data = tuple(invoice_data.values())
        db.add_invoice(data)
        await back(message, state)
    else:
        await back(message, state)
