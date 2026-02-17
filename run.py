import asyncio
from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.start_handler import router as start_router
from handlers.services_subscriptions_handlers import router as services_subscriptions_router
from handlers.date_handler import router as date_router
from handlers.subscription_name_handler import router as subscription_name_router
from commands.show_subscriptions_command import router as show_subscriptions_command_router
from handlers.management_handler import router as management_handler_router

from mailing.sending_out_informations import sending_out_informations
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(start_router)
    dp.include_router(services_subscriptions_router)
    dp.include_router(date_router)
    dp.include_router(subscription_name_router)
    dp.include_router(show_subscriptions_command_router)
    dp.include_router(management_handler_router)

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(sending_out_informations, trigger='cron', hour=10, minute=0, args=[bot])
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')