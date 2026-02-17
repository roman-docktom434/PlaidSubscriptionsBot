from mysql.db import get_notification_dates, update_expiration_date
from datetime import datetime
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

async def sending_out_informations(bot):
    try:
        data_from_db = await get_notification_dates()
    except Exception:
        return

    today = datetime.now().date()
    for subscription in range(0, len(data_from_db)):
        id = data_from_db[subscription][0]
        user_id = data_from_db[subscription][1]
        service = data_from_db[subscription][2]
        date_from_db = data_from_db[subscription][3]
        price = data_from_db[subscription][4]
        try:
            quantity_days = (date_from_db - today).days
            if quantity_days == 1:
                await bot.send_message(user_id, text=f'Ваша подписка на <b>{service}</b> истекает через 1 день.\nСумма оплаты составляет: <code>{price}₽</code>', parse_mode='HTML')
            elif quantity_days == 3:
                await bot.send_message(user_id, text=f'Ваша подписка на <b>{service}</b> истекает через 3 дня.\nСумма оплаты составляет: <code>{price}₽</code>', parse_mode='HTML')
            elif quantity_days == 0:
                await update_expiration_date(user_id, id)
                await bot.send_message(user_id, text=f'Ваша подписка на <b>{service}</b> истекла.')
        except TelegramForbiddenError:
            print("Пользователь заблокировал бота")

        except TelegramRetryAfter:
            print("Слишком быстрая отправка. Флуд")

        except Exception:
            print("Непредвиденная ошибка")
            continue


