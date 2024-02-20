from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import db
from aiogram.utils.media_group import MediaGroupBuilder

from handlers.back import back
from utils import bot

available_choice = ["Отправить", "На главную"]

router = Router()


class Claim(StatesGroup):
    user_id = State()
    username = State()
    invoice_number = State()
    email = State()
    description = State()
    amount = State()
    photo = State()
    admin_id = State()
    status = State()
    choice = State()
    send = State()


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
        text='Номер накладной', reply_markup=keyboard
    )
    await state.set_state(Claim.email)


@router.message(Claim.email)
async def email(message: Message, state: FSMContext):
    await state.update_data(invoice_number=message.text)
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
    path_file = f"photo/{message.from_user.username}-claim-{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1], destination=path_file)
    await state.update_data(photo=path_file)
    admin_id = db.get_user_admin(user_id=message.from_user.id)
    await state.update_data(admin_id=admin_id)
    await state.update_data(status='open')
    claim_data = await state.get_data()
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
        text=f"Номер накладной - "
        f"E-mail для ответа на претензию - {claim_data['email']}.\n"
        f"описание ситуации - {claim_data['description']}.\n"
        f"требуемая сумма - {claim_data['amount']}.\n"
        "Все верно?",
        reply_markup=keyboard
        )
    album_builder = MediaGroupBuilder()
    album_builder.add(
        type="photo",
        media=FSInputFile(path=claim_data['photo'])
    )
    await message.answer_media_group(
        media=album_builder.build()
    )
    await state.set_state(Claim.send)


@router.message(Claim.send, F.text.in_(available_choice))
async def cmd_safe(message: Message, state: FSMContext):
    claim_data = await state.get_data()
    if message.text == 'Отправить':
        await bot.send_message(
            claim_data['admin_id'][0],
            f"Пользователь {claim_data['username']} создал претензию.")
        data = tuple(claim_data.values())
        db.add_claim(data)
        await back(message, state)
    else:
        await back(message, state)


@router.message(F.text.lower() == 'претензии от клиентов')
async def cmd_claim_admin(message: Message, state: State):
    admin_id = message.from_user.id
    data_claim = db.get_all_claim()
    if 'user' in db.get_user_role(user_id=admin_id):
        await back(message, state)
    elif db.get_open_claim(admin_id=admin_id) != []:
        data_claim = db.get_all_claim()
        for user_id, username, invoice_number, email, description, amount, photo_db, admin_id, status in data_claim:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"USER_ID - {user_id}\n"
                f"USERNAME - {username}\n"
                f"EMAIL - {email}\n"
                f"Описание ситуации - {description},\n"
                f"Сумма - {amount}\n"
            )
            album_builder = MediaGroupBuilder()
            album_builder.add(
                type="photo",
                media=FSInputFile(path=photo_db)
            )
            await bot.send_media_group(
                chat_id=message.from_user.id,
                media=album_builder.build())
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Открытых перетензий нет.')
