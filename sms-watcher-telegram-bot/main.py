import asyncio
import os
import json

import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

TELEGRAM_TOKEN_API = os.environ.get("TELEGRAM_TOKEN_API", default="")
users_str = os.environ.get("TELEGRAM_USER_WHITELIST")
users = users_str.split(',')
USER_WHITELIST = [int(item) for item in users if item.strip().isdigit()]

bot = Bot(token=TELEGRAM_TOKEN_API)
dp = Dispatcher()
whitelist_error_message = "Я могу отвечать только пользователям из белого списка"

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
        await message.answer(whitelist_error_message)


@dp.message(F.text.startswith("Phone: "))
async def handle_phone(message: types.Message):
    if message.from_user.id in USER_WHITELIST:
        target_phone = message.text[7:]
        for sim_card in sim_cards:
            if sim_card['phone'] == target_phone:
                await message.answer("Test")
                # url = sim_card['url']
                # cookies = {'sysauth': sim_card['sysauth']}
                # name = sim_card['name']
                # response = requests.get(url, cookies=cookies)
                # if response.status_code == 200:
                #     data = json.loads(response.text)
                #     messages = [message["storage"]["content"]["text"] for message in data["result"][name]]
                #     result_messages = ""
                #     for i, result_message in enumerate(messages):
                #         result_messages += f"SMS #{i+1}: \r\n{result_message}\r\n\r\n"
                #     await message.answer(result_messages)
                # else:
                #     await message.answer(f'Error: {response.status_code}')
                break
        else:
            await message.answer("Ошибка")
    else:
        await message.answer(whitelist_error_message)


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
