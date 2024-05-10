import sqlite3

import database
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database.a_db import AsyncDatabase
from database import sql_quaries
from handlers.profile import router
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard_registration

router = Router()


@router.callback_query(lambda call: call.data == "delete_profile")
async def delete_profile(call: types.CallbackQuery,
                         # state: FSMContext,
                         db=AsyncDatabase()):
    await call.message.delete()
    await db.execute_query(
        query=sql_quaries.DELETE_PROFILE_QUERY,
        params=(call.from_user.id,),
        fetch='none'
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text="Your profile has been deleted for some reason ... 😒 "
    )
