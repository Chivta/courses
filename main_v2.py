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


@router.message(Command("reply_builder"))
async def cmd_reply_builder(message: Message, command: CommandObject):
    num = command.args
    builder = ReplyKeyboardBuilder()
    for i in range(1,int(num)+1):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4,3,2,1)
    await message.answer(
        "done",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="З пюрешкою"),
            types.KeyboardButton(text="Без пюрешки"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Виберіть спосіб подачі",
        # one_time_keyboard=True / False
    )
    await message.answer("Як подавати котлети?", reply_markup=keyboard)


@router.message(Text("З пюрешкою"))
async def text_handler(message: Message) -> None:
    await message.answer(f"{message.from_user.full_name}, з пюрешкою завжди смачніше:)")


@router.message(Text("Без пюрешки"))
async def text_handler(message: Message) -> None:
    await message.answer(f"{message.from_user.full_name}, без пюрешки не ситно:(")


# @router.message(F.text)
# async def text_handler(message: Message) -> None:
#     if message.text == "З пюрешкою":
#         await message.answer(f"{message.from_user.full_name}, з пюрешкою завжди смачніше:)")
#     elif message.text == "Без пюрешки":
#         await message.answer(f"{message.from_user.full_name}, без пюрешки не ситно:(")


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
