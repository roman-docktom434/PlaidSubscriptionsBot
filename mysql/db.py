from mysql.connection import get_connection
from datetime import datetime
from dateutil.relativedelta import relativedelta

async def inserting_user_data(username, user_id):
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_insert_users = "INSERT IGNORE INTO users (username, user_id) VALUES (%s, %s)"
        await curs.execute(sql_insert_users, (username, user_id))
        await connection.commit()
    connection.close()


async def inserting_subscription_data(user_id, service, name, price, date):
    current_date = datetime.strptime(date, '%Y-%m-%d')
    next_date = current_date + relativedelta(months=1)
    next_date_str = next_date.strftime('%Y-%m-%d')
    connection = await get_connection()
    if service == 'trial':
        async with connection.cursor() as curs:
            sql_insert_subs = "INSERT INTO subscriptions (user_id, type_subscription, name_subscription, expiration_date, next_billing_date, cost, is_trial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            await curs.execute(sql_insert_subs, (user_id, "Пробный период", name, date, None, price, "1"))
    else:
        async with connection.cursor() as curs:
            sql_insert_subs = "INSERT INTO subscriptions (user_id, type_subscription, name_subscription, expiration_date, next_billing_date, cost, is_trial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            await curs.execute(sql_insert_subs, (user_id, service, name, date, next_date_str, price, "0"))
    await connection.commit()
    connection.close()


async def get_notification_dates():
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_get_notifications = ("SELECT id, user_id, type_subscription, DATE(expiration_date), cost FROM subscriptions WHERE (expiration_date) = DATE_ADD(CURDATE(), INTERVAL 3 DAY) "
                                 "OR (expiration_date) =  DATE_ADD(CURDATE(), INTERVAL 1 DAY)")
        await curs.execute(sql_get_notifications)

        result = await curs.fetchall()
    connection.close()
    return result

async def get_user_data(user_id):
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_user_data = "SELECT id, type_subscription, name_subscription, expiration_date, cost FROM subscriptions WHERE user_id = %s"
        await curs.execute(sql_user_data, (user_id,))

        result = await curs.fetchall()
    connection.close()
    return result

async def deleting_a_subscriptions(id):
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_deleting = "DELETE FROM subscriptions WHERE id = %s"
        await curs.execute(sql_deleting, (id,))

    await connection.commit()
    connection.close()


async def edit_price(id, new_price):
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_edit_price = "UPDATE subscriptions SET cost = %s WHERE id = %s"
        await curs.execute(sql_edit_price, (new_price, id))

    await connection.commit()
    connection.close()


async def get_date(current_date):
    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_get_date = "SELECT next_billing_date FROM subscriptions WHERE expiration_date = %s"
        await curs.execute(sql_get_date, (current_date,))

        result = await curs.fetchall()
    connection.close()
    return result[0][0]

async def update_expiration_date(user_id, id):
    current_date = datetime.now().date()
    new_expiration_date = await get_date(current_date)
    next_date = new_expiration_date + relativedelta(months=1)
    next_date_str = next_date.strftime('%Y-%m-%d')

    connection = await get_connection()
    async with connection.cursor() as curs:
        sql_update_expiration_date = "UPDATE subscriptions SET expiration_date = %s, next_billing_date = %s WHERE user_id = %s AND id = %s"
        await curs.execute(sql_update_expiration_date, (new_expiration_date, next_date_str, user_id, id))

    await connection.commit()