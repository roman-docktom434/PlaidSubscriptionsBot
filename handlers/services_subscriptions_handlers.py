import os
import dotenv
dotenv.load_dotenv()
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
import asyncio

import keyboard.keyboard as kb
from handlers.date_handler import choose_month, choose_trial_days

router = Router()


# SERVICES_CALLBACKS = [
#     "yaplus", "kinopo", "wink", "sber", "vkmus", "spot",
#     "vpn", "tgprem", "ivi", "okko", "start", "ozonprem",
#     "netflix", "youtprem", "trial", "other"
# ]

SERVICES_CALLBACKS = {
    "Яндекс": "yaplus",
    "Кинопоиск": "kinopo",
    "Wink": "wink",
    "СберПрайм": "sber",
    "VK Музыка": "vkmus",
    "Spotify": "spot",
    "VPN": "vpn",
    "TG Premium": "tgprem",
    "Иви":  "ivi",
    "Okko": "okko",
    "Start": "start",
    "Ozon Premium": "ozonprem",
    "Netflix": "netflix",
    "YT Premium": "youtprem"
}

# Сохранение выбранного сервиса:
@router.callback_query(F.data.in_(SERVICES_CALLBACKS.values()) | (F.data == 'f'))
async def choose_a_service(callback: CallbackQuery, state: FSMContext):
    for key, value in SERVICES_CALLBACKS.items():
        if callback.data == value:
            await state.update_data(type_subscription=key)
    await choose_month(callback)


@router.callback_query(F.data == 'trial')
async def сhoose_the_number_of_days_for_the_trial(callback: CallbackQuery, state: FSMContext):
    await choose_trial_days(callback)
    await state.update_data(type_subscription=callback.data)









# @router.message(F.photo)
# async def get_photo_id(message: Message):
#     # Telegram хранит фото в нескольких размерах.
#     # Последний в списке [-1] — это самое высокое качество.
#     photo_id = message.photo[-1].file_id
#     await message.answer(f"ID твоего фото:\n<code>{photo_id}</code>", parse_mode="HTML")