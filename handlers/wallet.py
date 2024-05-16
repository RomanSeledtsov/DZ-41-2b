import random
import re
import sqlite3

import database
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, CallbackQuery

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database.a_db import AsyncDatabase
from database import sql_quaries
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard_registration
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class SendMoney(StatesGroup):
    id = State()
    amount = State()


@router.callback_query(lambda call: call.data == 'money_')
async def start_state(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id,
                           text='send wallet number')
    await state.set_state(SendMoney.id)


@router.message(SendMoney.id)
async def process_id(m: types.Message,
                     state: FSMContext,
                     db=AsyncDatabase()):
    user = await db.execute_query(query=sql_quaries.SELECT_WALLET_NUMBER,
                                  params=(int(m.text),),
                                  fetch='one')

    if user:
        await state.update_data(id=int(m.text))
        await bot.send_message(
            chat_id=m.from_user.id,
            text='how much do u want to send'
        )
        await state.set_state(SendMoney.amount)
    else:
        await bot.send_message(
            chat_id=m.from_user.id,
            text='User not found'
        )


@router.message(SendMoney.amount)
async def process_money(m: types.Message,
                        state: FSMContext,
                        db=AsyncDatabase()):
    money = int(m.text)
    balance = await db.execute_query(query=sql_quaries.SELECT_BALANCE_QUERY,
                                     params=(m.from_user.id,),
                                     fetch='one')
    balance = balance['COALESCE(BALANCE, 0)']

    if money <= balance:
        await db.execute_query(query=sql_quaries.UPDATE_SENDER_BALANCE_QUERY,
                               params=(money, m.from_user.id),
                               )
        data = await state.get_data()
        await db.execute_query(query=sql_quaries.UPDATE_USER_BALANCE_QUERY_BY_ID,
                               params=(money, data['id']))
        user = await db.execute_query(query=sql_quaries.SELECT_TG_ID_BY_ID,
                                      params=(data['id'],),
                                      fetch='one')
        tg_id = user['TELEGRAM_ID']
        await bot.send_message(chat_id=tg_id,
                               text=f'user{m.from_user.first_name} sent u {money}$')

        await bot.send_message(chat_id=m.from_user.id,
                               text='successfully sent money')
        await db.execute_query(query=sql_quaries.INSERT_WALLET_TRANS,
                               params=(None,
                                       m.from_user.id,
                                       tg_id,
                                       money))
    else:
        await bot.send_message(chat_id=m.from_user.id,
                               text=f'Not enough money\n'
                                    f'Balance -> {balance}')


@router.callback_query(lambda call: call.data == "wallet_")
async def wallet_callback(call: CallbackQuery,
                          db=AsyncDatabase()):
    user = await db.execute_query(query=sql_quaries.SELECT_ID_BY_TG_ID,
                                  params=(call.from_user.id,),
                                  fetch='one')
    id = user['id']
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'ur wallet number is {id}')
