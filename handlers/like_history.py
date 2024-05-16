import random
import re
import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database import sql_quaries
from database.a_db import AsyncDatabase
from keyboards.like_dislike import like_dislike_keyboard, history_keyboard
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard_registration
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


@router.callback_query(lambda call: call.data == "history")
async def detect_like_history_call(call: types.CallbackQuery,
                                   db=AsyncDatabase()):
    profiles = await db.execute_query(
        query=sql_quaries.SELECT_LIKED_PROFILES,
        params=(
            call.from_user.id,
        ),
        fetch='all'
    )
    randomizer = random.choice(profiles)
    random_profile = await db.execute_query(
        query=sql_quaries.SELECT_PROFILE_QUERY,
        params=(
            randomizer['OWNER_TELEGRAM_ID'],
        ),
        fetch='one'
    )
    photo = types.FSInputFile(random_profile['PHOTO'])
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=random_profile['NICKNAME'],
            bio=random_profile['BIO'],
            birth_day=random_profile['BIRTH_DAY'],
            gender=random_profile['GENDER']
        ),
        reply_markup=await history_keyboard(tg_id=random_profile['TELEGRAM_ID'])
    )