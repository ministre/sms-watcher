import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart


TOKEN_API = os.environ.get("TOKEN_API", default="")

bot = Bot(token=TOKEN_API)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    kb = [
        [types.KeyboardButton(text="1")],
        [types.KeyboardButton(text="2")],
        [types.KeyboardButton(text="3")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите номер"
    )
    await message.answer("Выберите номер", reply_markup=keyboard)


@dp.message(F.text.lower() == "1")
async def handle_number_1(message: types.Message):
    await message.answer("Выбран номер 1")


@dp.message(F.text.lower() == "2")
async def handle_number_2(message: types.Message):
    await message.answer("Выбран номер 2")


@dp.message(F.text.lower() == "3")
async def handle_number_3(message: types.Message):
    await message.answer("Выбран номер 3")


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
