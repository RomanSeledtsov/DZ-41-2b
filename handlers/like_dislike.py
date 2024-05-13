import re
import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
import random
from database.a_db import AsyncDatabase
from database import sql_quaries
from keyboards.like_dislike import like_dislike_keyboard
from keyboards.start import start_menu_keyboard_registration

router = Router()


@router.callback_query(lambda call: call.data == "view_profiles")
async def random_profiles_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    if call.message.caption.startswith("Nickname"):
        await call.message.delete()
    profiles = await db.execute_query(
        query=sql_quaries.SELECT_ALL_PROFILES,
        params=(
            call.from_user.id,
            call.from_user.id,
        ),
        fetch='all'
    )
    if profiles:
        random_profile = random.choice(profiles)
        print(profiles)
        print(random_profile)
        photo = types.FSInputFile(random_profile['PHOTO'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname=random_profile['NICKNAME'],
                bio=random_profile['BIO'],
                birth_day=random_profile['BIRTH_DAY'],
                gender=random_profile['GENDER'],
            ),
            reply_markup=await like_dislike_keyboard(tg_id=random_profile['TELEGRAM_ID'])
        )
    else:
        # await bot.send_message(
        #     chat_id=call.from_user.id,
        #     text='You\'ve liked all profiles come back later!'
        # )
        return


@router.callback_query(lambda call: "like_" in call.data)
async def like_dislike_call(call: types.CallbackQuery,
                            db=AsyncDatabase()):
    await call.message.delete()
    # print(call.data.replace("like_", ""))
    # print(call.data[5:])
    owner_tg_id = re.sub("like_", "", call.data)

    await db.execute_query(
        query=sql_quaries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            1
        ),
        fetch='none'
    )
    await random_profiles_call(call=call)


@router.callback_query(lambda call: "dislike" in call.data)
async def like_dislike_call(call: types.CallbackQuery,
                            db=AsyncDatabase()):
    await call.message.delete()
    # print(call.data.replace("like_", ""))
    # print(call.data[5:])
    owner_tg_id = re.sub("dislike", "", call.data)

    await db.execute_query(
        query=sql_quaries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            0
        ),
        fetch='none'
    )
    await random_profiles_call(call=call)
