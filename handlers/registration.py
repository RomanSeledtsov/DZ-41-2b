import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database.a_db import AsyncDatabase
from database import sql_quaries
from keyboards.start import start_menu_keyboard_registration

router = Router()


class RegistrationStates(StatesGroup):
    nickname = State()
    bio = State()
    birth_day = State()
    gender = State()
    photo = State()


@router.callback_query(lambda call: call.data == "registration")
async def registration_call(call: types.CallbackQuery,
                            state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Send me your nickname pls!"
    )
    await state.set_state(RegistrationStates.nickname)


@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message,
                           state: FSMContext):
    await state.update_data(nickname=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Tell me about urself"
    )

    await state.set_state(RegistrationStates.bio)


@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message,
                      state: FSMContext):
    await state.update_data(bio=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="tell me ur bithday"
    )
    await state.set_state(RegistrationStates.birth_day)


@router.message(RegistrationStates.birth_day)
async def process_birth(message: types.Message, state: FSMContext):
    await state.update_data(birth_day=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='what is ur gender?'
    )
    await state.set_state(RegistrationStates.gender)


@router.message(RegistrationStates.gender)
async def process_gender(message: types.Message,
                         state: FSMContext):
    gender = message.text.strip().lower()
    if gender not in ['male', 'female', 'other']:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Invalid input. Please choose one of the following: Male, Female, Other."
        )
    else:
        await state.update_data(gender=gender)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Great! Now, could you send ur photo"
        )
        await state.set_state(RegistrationStates.photo)


@router.message(RegistrationStates.photo)
async def process_photo(message: types.Message,
                        state: FSMContext,
                        db=AsyncDatabase()):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    media_final_path = 'media/' + file_path
    await bot.download_file(
        file_path,
        'media/' + file_path
    )
    data = await state.get_data()

    photo = FSInputFile('media/' + file_path)
    try:
        await db.execute_query(
            query=sql_quaries.INSERT_PROFILE_QUERY,
            params=(
                None,
                message.from_user.id,
                data['nickname'],
                data['bio'],
                data['gender'],
                data['birth_day'],
                'media/' + file_path

            ),
            fetch='none'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="U have registered before ??"
        )
        return

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=data['nickname'],
            bio=data['bio'],
            gender=data['gender'],
            birth_day=data['birth_day']
        )
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="U have registered successfully ??"
    )


@router.callback_query(lambda call: call.data == "view_profile")
async def view_profile(call: types.CallbackQuery,
                       db=AsyncDatabase()):
    user_id = call.from_user.id
    user_profile = await db.execute_query(
        query=sql_quaries.SELECT_PROFILE,
        params=(user_id,),
        fetch="all"
    )
    if user_profile:
        user = user_profile[0]
        photo = FSInputFile(user['PHOTO'])
        await bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=f'name:{user['NICKNAME']}\n'
                    f'bio: {user['BIO']}\n'
                    f'gender: {user['GENDER']}\n'
                    f'birth_day: {user['BIRTH_DAY']}\n'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Your profile is not found. Please try again."
        )
