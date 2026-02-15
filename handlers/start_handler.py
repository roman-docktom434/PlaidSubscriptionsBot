import os
import dotenv
dotenv.load_dotenv()
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

import keyboard.keyboard as kb
from mysql.db import inserting_user_data
START_IMAGE = os.getenv('START_IMAGE')

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    username = message.from_user.first_name
    user_id = message.from_user.id
    await inserting_user_data(username, user_id)
    await message.answer_photo(
        photo=START_IMAGE,
        caption=f"Приветствуем, {username}!\n\nСвоевременный учет подписок — это простой способ сэкономить значительную часть годового бюджета. Я обеспечу прозрачность ваших отношений с цифровыми сервисами и напомню о списании средств за день до платежа.\n\nДля настройки уведомлений выберите соответствующий сервис:",
        reply_markup=kb.choosing_a_service
    )











