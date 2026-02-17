from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.date_handler import choose_month, choose_trial_days

router = Router()

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