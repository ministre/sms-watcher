import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

TELEGRAM_TOKEN_API = os.environ.get("TELEGRAM_TOKEN_API", default="")
users_str = os.environ.get("TELEGRAM_USER_WHITELIST")
users = users_str.split(',')
USER_WHITELIST = [int(item) for item in users if item.strip().isdigit()]

bot = Bot(token=TELEGRAM_TOKEN_API)
dp = Dispatcher()
access_err_msg = "Я могу отвечать только пользователям из белого списка"


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if message.from_user.id in USER_WHITELIST:
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
    else:
        await message.answer(access_err_msg)


@dp.message(F.text.lower() == "1")
async def handle_number_1(message: types.Message):
    if message.from_user.id in USER_WHITELIST:
        await message.answer("Выбран номер 1")
    else:
        await message.answer(access_err_msg)


@dp.message(F.text.lower() == "2")
async def handle_number_2(message: types.Message):
    if message.from_user.id in USER_WHITELIST:
        await message.answer("Выбран номер 2")
    else:
        await message.answer(access_err_msg)


@dp.message(F.text.lower() == "3")
async def handle_number_3(message: types.Message):
    if message.from_user.id in USER_WHITELIST:
        await message.answer("Выбран номер 3")
    else:
        await message.answer(access_err_msg)


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
