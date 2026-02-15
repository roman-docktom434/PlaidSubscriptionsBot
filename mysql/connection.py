import os
import dotenv
dotenv.load_dotenv()
import aiomysql
import asyncio

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
PORT = int(os.getenv("PORT"))


DB_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'db': DB,
    'port': PORT
}


async def get_connection():
    return await aiomysql.connect(**DB_CONFIG)