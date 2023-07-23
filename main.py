import os

import logging
import asyncio
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile
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


@router.message(Command("random_image"))
async def get_random_image(message: Message, command: CommandObject) -> None:
    """
    /random_image 500 600
    /random_image 500 -> Required 2 params but 1 given
    /random_image 500 500 500-> Required 2 params but 3 given
    /random_image -> Required 2 params but 0 given
    :param command:
    :param message:
    :return:
    """
    size = command.args.split()
    if len(size) != 2:
        await message.answer(f'Required 2 params but {len(size)} given')
    else:
        image_from_url = URLInputFile(f"https://random.imagecdn.app/{size[0]}/{size[1]}")
        try:
            await message.answer_photo(image_from_url)
        except TelegramBadRequest:
            await message.answer('Photo invalid dimensions')


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
