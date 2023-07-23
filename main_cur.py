import os

import logging
import asyncio
import sqlite3
import requests

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject, Text
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import html
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from settings import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter

load_dotenv()

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

#
con = sqlite3.connect(config.db_name)
cursor = con.cursor()


def create_table():
    text = """
        CREATE TABLE IF NOT EXISTS currency (
            id integer PRIMARY KEY,
            from_currency TEXT NOT NULL,
            to_currency TEXT NOT NULL,
            value INTEGER,
            created_at TEXT,
            UNIQUE(from_currency,to_currency)
        );
    """
    response = cursor.execute(text)


def clear_table():
    text = "DELETE FROM currency;"
    response = cursor.execute(text)
    con.commit()


def insert_currency(curr_from: str, curr_to: str, value: float):
    text = f"""
        INSERT INTO currency (from_currency, to_currency, value, created_at)
        VALUES ('{curr_from}', '{curr_to}', {value}, datetime('now'));
    """
    response = cursor.execute(text)
    con.commit()


def add_currency_data():
    currencies = ['JPY', 'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'UAH']
    for base_cur in currencies:
        for second_cur in currencies:
            if second_cur == base_cur:
                continue
            request = requests.get('https://api.metalpriceapi.com/v1/latest'
                                   '?api_key=af893cfb035de853c9d9224218125d92'
                                   f'&base={base_cur}'
                                   f'&currencies={second_cur}')
            request = request.json()
            insert_currency(base_cur, second_cur, request["rates"][f'{second_cur}'])


def get_unique_select_from_data() -> list[str]:
    text = "select DISTINCT from_currency from currency;"
    response = cursor.execute(text)
    data = response.fetchall()  # [("USD",), ("EUR",)]
    return [uniq_curr[0] for uniq_curr in data]  # ["USD", "EUR", ...]


def get_all_second_currencies(cur1) -> list[str]:
    text = f"select to_currency from currency where from_currency = '{cur1}';"
    response = cursor.execute(text)
    data = response.fetchall()  # [("USD",), ("EUR",)]
    return [uniq_curr[0] for uniq_curr in data]  # ["USD", "EUR", ...]


def get_currency(cur1, cur2):
    text = f"select value from currency where from_currency = '{cur1}' and to_currency = '{cur2}';"
    response = cursor.execute(text)
    data = response.fetchall()  # [("USD",), ("EUR",)]
    return [uniq_curr[0] for uniq_curr in data]  # ["USD", "EUR", ...]


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    cur_1 = get_unique_select_from_data()
    builder = ReplyKeyboardBuilder()
    for i in cur_1:
        builder.add(types.KeyboardButton(text=i))
    builder.adjust(3)
    await message.answer(
        "Select first currency",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=False))


@router.message(Text('Return'))
async def return_handler(message: types.Message):
    await cmd_start(message)


@router.message(F.text)
async def curs(message: types.Message):
    if '->' in message.text:
        currencies = message.text.split('->')
        currencies[0] = currencies[0].strip()
        currencies[1] = currencies[1].strip()
        value = get_currency(currencies[0], currencies[1])
        if len(value) == 0:
            await message.answer('Unknown currenct')
        else:
            await message.answer(value[0])
    else:
        builder = ReplyKeyboardBuilder()
        from_currency = message.text
        to_currencies = get_all_second_currencies(from_currency)
        if len(to_currencies) == 0:
            await message.answer('Unknown currency')
        else:
            for to_currency in to_currencies:
                builder.add(types.KeyboardButton(text=f'{from_currency} -> {to_currency}'))
            builder.add(types.KeyboardButton(text='Return'))
            builder.adjust(3)
            await message.answer(
                "Here all available currencies",
                reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=False))


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    create_table()
    clear_table()
    add_currency_data()
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
