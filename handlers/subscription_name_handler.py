from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.date_handler import AddSubscription
from mysql.db import inserting_subscription_data
from helpers.math_day import math_day_for_db
import keyboard.keyboard as kb
from handlers.date_handler import TRIAL_DAYS_KEYBOARD

router = Router()


@router.callback_query((F.data == "t") | (F.data.in_(TRIAL_DAYS_KEYBOARD)))
async def subscription_name(callback: CallbackQuery, state: FSMContext):

    if callback.data == "t":
        await callback.message.edit_text(
            text='Укажите название подписки. (Не обязательно)',
            reply_markup=kb.skip
        )
        await state.update_data(last_message_id=callback.message.message_id)

    else:
        await callback.message.delete()
        new_msg = await callback.message.answer(
            text='Укажите название подписки. (Не обязательно)',
            reply_markup=kb.skip
        )
        await state.update_data(days=callback.data)
        await state.update_data(last_message_id=new_msg.message_id)

    await state.set_state(AddSubscription.waiting_subscription_name)


@router.message(AddSubscription.waiting_subscription_name)
async def subscription_price(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)

    new_msg = await message.answer(
        text="Укажите цену подписки:"
    )
    await state.update_data(last_message_id=new_msg.message_id)
    await state.set_state(AddSubscription.waiting_subscription_price)


@router.callback_query(F.data == 'skip')
async def subscription_price_mes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)

    new_msg = await callback.message.answer(
        text="Укажите цену подписки:"
    )

    await state.update_data(last_message_id=new_msg.message_id)
    await state.set_state(AddSubscription.waiting_subscription_price)


@router.message(AddSubscription.waiting_subscription_price)
async def done(message: Message, state: FSMContext):
    if message.text.isdigit() and not message.text.startswith("0"):
        await state.update_data(price=message.text)
        data = await state.get_data()
        last_message_id = data.get('last_message_id')
        await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
        await message.answer(
            text="Подписка успешно добавлена! Просмотреть все подписки можно с помощью команды - /show_subscriptions"
        )
        data = await state.get_data()
        print(data)
        if data.get('type_subscription') == 'trial':
            db_date = {
                'days': data.get('days')
            }
        else:
            db_date = {
                'day': data.get('choosen_day'),
                'month': data.get('choosen_month')
            }
        date = await math_day_for_db(db_date)
        await state.update_data(date=date.isoformat())
        data = await state.get_data()
        db_data = {
            'service': data.get('type_subscription'),
            'name': data.get('name'),
            'price': int(data.get('price')),
            'date': data.get('date')
        }
        print(db_data)
        await inserting_subscription_data(message.from_user.id, db_data['service'], db_data['name'], db_data['price'], db_data['date'])
        await state.clear()
    else:
        await message.answer(text="Ошибка! Похоже Вы не правильно ввели цену, попробуйте еще раз (например, 500):")