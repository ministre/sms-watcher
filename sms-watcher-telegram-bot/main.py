import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

TELEGRAM_TOKEN_API = os.environ.get("TELEGRAM_TOKEN_API", default="")
users_str = os.environ.get("TELEGRAM_USER_WHITELIST")
users = users_str.split(',')
USER_WHITELIST = [int(item) for item in users if item.strip().isdigit()]

bot = Bot(token=TELEGRAM_TOKEN_API)
dp = Dispatcher()
access_err_msg = "Я могу отвечать только пользователям из белого списка"

with open('config/config.json', 'r') as file:
    data = json.load(file)

sim_cards = data['sim-cards']


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if message.from_user.id in USER_WHITELIST:
        kb = []
        for sim_card in sim_cards:
            kb.append([types.KeyboardButton(text=f"Phone: {sim_card['phone']}")])
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите номер"
        )
        await message.answer("Выберите номер", reply_markup=keyboard)
    else:
        await message.answer(access_err_msg)


@dp.message(F.text.startswith("Phone: "))
async def handle_phone(message: types.Message):
    if message.from_user.id in USER_WHITELIST:
        target_phone = message.text[7:]
        for sim_card in sim_cards:
            if sim_card['phone'] == target_phone:
                device_ip = sim_card['device_ip']
                await message.answer(device_ip)
                break
        else:
            await message.answer("Ошибка")
    else:
        await message.answer(access_err_msg)


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
