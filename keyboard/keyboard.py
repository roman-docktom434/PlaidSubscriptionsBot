from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import calendar
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')

async def days(month_number):
    dtn = datetime.now()
    YEAR = int(dtn.strftime("%Y"))
    MONTH = dtn.month
    DAY = int(dtn.strftime("%d"))
    matrix = calendar.monthcalendar(YEAR, month_number)

    month_name = calendar.month_name[month_number]

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=month_name, callback_data="ignore"))

    days = []
    for weeks in matrix:
        for day in weeks:
            if int(day) == 0 or (DAY >= int(day) and MONTH == month_number):
                days.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                days.append(InlineKeyboardButton(text=str(day), callback_data=str(day)))

    builder.row(*days, width=7)
    return builder.as_markup()

async def months():
    dtn = datetime.now()
    YEAR = dtn.strftime("%Y")
    MONTH = dtn.month
    print(MONTH)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=YEAR, callback_data="ignore"))

    if dtn.month == 12:
        next_month_start = datetime(dtn.year + 1, 1, 1)
    else:
        next_month_start = datetime(dtn.year, dtn.month + 1, 1)

    remaining_time = next_month_start - dtn

    months = []
    for month_number in range(1, 13):
        is_expired = month_number < MONTH
        is_closing_soon = (month_number == MONTH and remaining_time.days < 3)
        if is_expired or is_closing_soon:
            months.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        else:
            month = calendar.month_name[month_number]
            months.append(InlineKeyboardButton(text=month, callback_data=f"m_{month_number}"))

    builder.row(*months, width=3)
    return builder.as_markup()



choosing_a_service = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ЯндексПлюс", callback_data="yaplus"), InlineKeyboardButton(text="Кинопоиск", callback_data="kinopo"), InlineKeyboardButton(text="Wink", callback_data="wink"), InlineKeyboardButton(text="СберПрайм", callback_data="sber")],
    [InlineKeyboardButton(text="VK Музыка", callback_data="vkmus"), InlineKeyboardButton(text="Spotify", callback_data="spot"), InlineKeyboardButton(text="VPN сервис", callback_data="vpn"), InlineKeyboardButton(text="TG Premium", callback_data="tgprem")],
    [InlineKeyboardButton(text="Иви", callback_data="ivi"), InlineKeyboardButton(text="Okko", callback_data="okko"), InlineKeyboardButton(text="Start", callback_data="start"), InlineKeyboardButton(text="Ozon", callback_data="ozonprem")],
[InlineKeyboardButton(text="Netflix", callback_data="netflix"), InlineKeyboardButton(text="YT Premium", callback_data="youtprem"), InlineKeyboardButton(text="Тест-период", callback_data="trial"), InlineKeyboardButton(text="Другое", callback_data="other")]
])

number_of_days_of_trial_subscription = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1 дн.", callback_data="1d"), InlineKeyboardButton(text="3 дн.", callback_data="3d"), InlineKeyboardButton(text="7 дн.", callback_data="7d"), InlineKeyboardButton(text="14 дн.", callback_data="14d")],
[InlineKeyboardButton(text="30 дн.", callback_data="30d"), InlineKeyboardButton(text="60 дн.", callback_data="60d"), InlineKeyboardButton(text="90 дн.", callback_data="90d"), InlineKeyboardButton(text="365 дн.", callback_data="365d")]
])

yes_or_not = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="t", style="success"), InlineKeyboardButton(text="Нет", callback_data="f", style="danger")]
])

skip = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пропустить", callback_data="skip")]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])

management = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Управление подписками", callback_data="management")]
])

async def control_selection(page, total, id):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="<-", callback_data=f"page_{page - 1}"),
        InlineKeyboardButton(text=f"{page + 1}/{total}", callback_data="ignore"),
        InlineKeyboardButton(text="->", callback_data=f"page_{page + 1}")
    )

    builder.row(
        InlineKeyboardButton(text="Изменить цену", callback_data=f"editprice_{id}", style="primary"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_{id}", style="danger")
    )

    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="back")
    )

    return builder.as_markup()