import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import html
from aiogram.filters import Text
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from settings import config

import html

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter


# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

DATA_LIST = [
    {"currency": ("USD", "UAH"), "val": 45.03},
    {"currency": ("USD", "EUR"), "val": 0.9},
    {"currency": ("USD", "GBP"), "val": 0.8},
    {"currency": ("USD", "ZLT"), "val": 5.7},
    {"currency": ("UAH", "YPI"), "val": 12.0},
]


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    cur_1 = []
    for i in range(len(DATA_LIST)):
        cur_1.append(DATA_LIST[i]['currency'][0])
    cur_1 = set(cur_1)
    builder = ReplyKeyboardBuilder()
    for i in cur_1:
        builder.add(types.KeyboardButton(text=i))
    builder.adjust(3)
    await message.answer(
        "Hi",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True))


@router.message(Text('USD'))
async def usd_cur(message: types.Message):
    builder = ReplyKeyboardBuilder()
    cur_2 = []

    for i in range(len(DATA_LIST)):
        if DATA_LIST[i]['currency'][0] == 'USD':
            cur_2.append('USD -> '+DATA_LIST[i]['currency'][1])

    for i in cur_2:
        builder.add(types.KeyboardButton(text=i))
    builder.adjust(3)
    await message.answer(
        "Here all available currencies",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True))


@router.message(Text('UAH'))
async def usd_cur(message: types.Message):
    builder = ReplyKeyboardBuilder()
    cur_2 = []

    for i in range(len(DATA_LIST)):
        if DATA_LIST[i]['currency'][0] == 'UAH':
            cur_2.append('UAH -> '+DATA_LIST[i]['currency'][1])

    for i in cur_2:
        builder.add(types.KeyboardButton(text=i))
    builder.adjust(3)
    await message.answer(
        "Here all available currencies",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True))


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
