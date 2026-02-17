from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from mysql.db import get_user_data
from keyboard import keyboard as kb

router = Router()

async def formating_text(user_id, message):
    response = await get_user_data(user_id)
    if not response:
        await message.answer(text="У Вас отсутствуют действующие подписки")
    full_text = "<b>Список Ваших подписок:</b>\n\n"
    total_price = 0
    total_subs = 0

    for subscription in range(0, len(response)):
        service = response[subscription][1]
        name = response[subscription][2]
        date = response[subscription][3].date()
        price = response[subscription][4]


        full_text += (
            f"<b>Сервис</b>: <code>{service}</code>\n"
            f"<b>Название</b>: <code>{"Отсутствует" if name is None else name}</code>\n"
            f"<b>Дата истечения</b>: <code>{date}</code>\n"
            f"<b>Цена</b>: <code>{price} ₽</code>\n"
            "───────────────────\n"
        )
        total_subs += 1
        total_price += float(price)
    full_text += f"\n<b>Количество подписок:</b> <code>{total_subs}</code>\n"
    full_text += f"<b>📊 Общая стоимость:</b> <code>{total_price} ₽</code>"

    return full_text



@router.message(Command("show_subscriptions"))
@router.callback_query(F.data == "back")
async def show_subscriptions(event: Message | CallbackQuery):
    user_id = event.from_user.id
    full_text = await formating_text(user_id, event)
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=full_text, parse_mode="HTML", reply_markup=kb.management)
    else:
        await event.answer(text=full_text, parse_mode="HTML", reply_markup=kb.management)