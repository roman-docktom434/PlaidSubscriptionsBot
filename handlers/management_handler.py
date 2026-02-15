import dotenv
dotenv.load_dotenv()
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.date_handler import AddSubscription
import keyboard.keyboard as kb

from mysql.db import get_user_data, deleting_a_subscriptions, edit_price

router = Router()




@router.callback_query(F.data == "management")
async def management(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    response = await get_user_data(user_id)
    if not response:
        await callback.message.answer(text="У Вас отсутствуют действующие подписки")

    i = 0
    id, service, name, date, price = response[i][0], response[i][1], response[i][2], response[i][3].date(), response[i][4]
    await callback.message.edit_text(text=f"<b>Подписка</b> <code>{i+1}/{len(response)}</code>\n\n"
                               f"<b>Сервис:</b> <code>{service}</code>\n"
                               f"<b>Название:</b> <code>{"Отсутствует" if name is None else name}</code>\n"
                               f"<b>Дата истечения:</b> <code>{date}</code>\n"
                               f"<b>Цена:</b> <code>{price} ₽</code>",
                          reply_markup=await kb.control_selection(i, len(response), id),
                          parse_mode="HTML"
                          )


@router.callback_query(F.data.startswith("page_"))
async def process_pagination(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    response = await get_user_data(user_id)

    if page < 0: page = len(response) - 1
    if page >= len(response): page = 0

    id, service, name, date, price = response[page][0], response[page][1], response[page][2], response[page][3].date(), response[page][4]

    await callback.message.edit_text(text=f"<b>Подписка</b> <code>{page+1}/{len(response)}</code>\n\n"
                               f"<b>Сервис:</b> <code>{service}</code>\n"
                               f"<b>Название:</b> <code>{"Отсутствует" if name is None else name}</code>\n"
                               f"<b>Дата истечения:</b> <code>{date}</code>\n"
                               f"<b>Цена:</b> <code>{price} ₽</code>",
                            reply_markup=await kb.control_selection(page, len(response), id),
                            parse_mode="HTML"
                            )


@router.callback_query(F.data.startswith("delete_"))
async def deleting_a_subscription(callback: CallbackQuery):
    await callback.answer()
    id_subscriptions = int(callback.data.split("_")[1])
    await deleting_a_subscriptions(id_subscriptions)
    await callback.message.edit_text(text="Подписка была успешна удалена!", reply_markup=kb.back)


@router.callback_query(F.data.startswith("editprice_"))
async def price_change(callback: CallbackQuery, state: FSMContext):
    id_subscriptions = int(callback.data.split("_")[1])
    await state.update_data(last_message_id=callback.message.message_id)
    await state.update_data(id_subscriptions=id_subscriptions)
    await callback.message.edit_text(text="Введите новую цену", reply_markup=kb.back)
    await state.set_state(AddSubscription.waiting_subscription_new_price)

@router.message(AddSubscription.waiting_subscription_new_price)
async def accepting_a_modified_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите числовое значение!")
    data = await state.get_data()
    id_subscriptions = data.get("id_subscriptions")
    new_price = int(message.text)
    last_message_id = data.get("last_message_id")
    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)

    await edit_price(id_subscriptions, new_price)
    await message.answer(f"Цена была успешно обновлена! Новая стоимость: <code>{new_price} ₽</code>")
    await state.clear()