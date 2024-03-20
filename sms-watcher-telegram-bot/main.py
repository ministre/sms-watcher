from services import KroksRouter

import asyncio
import os
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

TELEGRAM_TOKEN_API = os.environ.get("TELEGRAM_TOKEN_API", default="")
users_str = os.environ.get("TELEGRAM_USER_WHITELIST", default="")
if users_str:
    users = users_str.split(',')
    USER_WHITELIST = [int(item) for item in users if item.strip().isdigit()]
else:
    USER_WHITELIST = []

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
                if sim_card['device'] == "kroks":
                    kroks_router = KroksRouter(ip=sim_card['ip'], username=sim_card['username'],
                                               password=sim_card['password'])
                    result = kroks_router.get_sms()
                    if result["status"]:
                        sms_messages = ""
                        for i, sms_message in enumerate(result["messages"]):
                            sms_messages += f"SMS #{i+1}: \r\n{sms_message}\r\n\r\n"
                            await message.answer(sms_messages)
                    else:
                        await message.answer(f'Error: {result["details"]}')
                else:
                    await message.answer("Unsupported device")


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())


# def main():
#     kroks_router = KroksRouter(ip="", username="", password="")
#     result = kroks_router.get_sms()
#     print(result)
#
#
# if __name__ == "__main__":
#     main()
