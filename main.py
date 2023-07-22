import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import html

from aiogram import F

from settings import config

import html

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter


# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message(Command("name"))
async def command_start_handler(message: Message, command: CommandObject) -> None:
    """
    This handler receive messages with `/start` command
    """
    answ = 'NY' if 'a' in command.args and 'o' in command.args \
        else 'LA' if 'o' in command.args \
        else 'LA' if 'a' in command.args \
        else 'IOWA'
    await message.answer(f'Hello {answ}')


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
        input_field_placeholder="Виберіть спосіб подачі",
        # one_time_keyboard=True / False
    )
    await message.answer("Як подавати котлети?", reply_markup=keyboard)


@router.message(F.text)
async def text_handler(message: Message) -> None:
    if message.text == "З пюрешкою":
        await message.answer(f"{message.from_user.full_name}, з пюрешкою завжди смачніше:)")
    elif message.text == "Без пюрешки":
        await message.answer(f"{message.from_user.full_name}, без пюрешки не ситно:(")


@router.message(F.text)
async def text_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    try:
        await message.reply(f'Your text is {len(message.text)} characters long!', parse_mode='HTML')
    except TypeError:
        await message.reply('Not a text!')


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
