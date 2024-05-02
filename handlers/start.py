from aiogram import Router, types
from aiogram.filters import Command

from config import bot, ADMIN_ID
from database.a_db import AsyncDatabase
from database import sql_quaries

router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    print(message)
    print(message.from_user.id)
    await db.execute_query(
        query=sql_quaries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        ),
        fetch='none'
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Hello {message.from_user.first_name}'
    )


@router.message(lambda message: message.text == "Admin99")
async def admin_start_menu(message: types.Message,
                           db=AsyncDatabase()):
    print(ADMIN_ID)
    if int(ADMIN_ID) == message.from_user.id:
        users = await db.execute_query(query=sql_quaries.SELECT_USERS, fetch="all")
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Here is your Admin page"
        )
        for user in users:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"{user['FIRST_NAME']}:{user['TELEGRAM_ID']}"
            )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You have not access!!"
        )