import os
import dotenv
dotenv.load_dotenv()
from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import calendar
import locale

import keyboard.keyboard as kb

locale.setlocale(locale.LC_ALL, 'ru_RU')

router = Router()

MONTHS = [
    "m_1", "m_2", "m_3",
    "m_4", "m_5", "m_6",
    "m_7", "m_8", "m_9",
    "m_10", "m_11", "m_12"
]

DAYS_KEYBOARD = [
    "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "11", "12", "13", "14",
    "15", "16", "17", "18", "19", "20", "21",
    "22", "23", "24", "25", "26", "27", "28",
    "29", "30", "31"
]

TRIAL_DAYS_KEYBOARD = [
    "1d", "3d", "7d", "14d",
    "30d", "60d", "90d", "365d"
]

CHOOSING_MONTH_IMAGE = os.environ.get('CHOOSING_MONTH_IMAGE')
CHOOSING_DAY_IMAGE = os.environ.get('CHOOSING_DAY_IMAGE')
TRIAL_IMAGE = os.getenv('TRIAL_IMAGE')


class AddSubscription(StatesGroup):
    waiting_subscription_day = State()
    waiting_subscription_name = State()
    waiting_subscription_price = State()
    waiting_subscription_new_price = State()

async def choose_month(callback: CallbackQuery):

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=CHOOSING_MONTH_IMAGE,
        caption="Выберите месяц следующего списания средств:",
        reply_markup=await kb.months()
    )

async def choose_trial_days(callback: CallbackQuery):


    await callback.message.delete()

    await callback.message.answer_photo(
        photo=TRIAL_IMAGE,
        caption='Укажите количество дней бесплатного доступа:',
        reply_markup=kb.number_of_days_of_trial_subscription
    )

def get_name_month(number):
    return calendar.month_name[number]


@router.callback_query(F.data.in_(MONTHS))
async def choose_day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choosen_month=callback.data)

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=CHOOSING_DAY_IMAGE,
        caption="Укажите день окончания действия подписки:",
        reply_markup=await kb.days(int(callback.data.split("_")[1]))
    )



@router.callback_query(F.data.in_(DAYS_KEYBOARD))
async def confirmation_of_the_expiration_date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choosen_day=callback.data)
    data = await state.get_data()
    choosen_month = get_name_month(int(str(data.get('choosen_month')).split('_')[1])).lower()
    if choosen_month[-1:] == 'т':
        choosen_month += 'а'
    else:
        choosen_month = choosen_month[:-1] + 'я'
    type_subscription = data.get('type_subscription')

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        text=f"Подписка на {type_subscription} истекает {data.get('choosen_day')} {choosen_month}. Верно?",
        reply_markup=kb.yes_or_not
    )

    await state.set_state(AddSubscription.waiting_subscription_day)