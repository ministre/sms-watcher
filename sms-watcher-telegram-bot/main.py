import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


TOKEN_API = os.environ.get("TOKEN_API", default="")

bot = Bot(token=TOKEN_API)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("test")


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
