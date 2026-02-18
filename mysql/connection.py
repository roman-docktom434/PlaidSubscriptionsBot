from config import HOST, USER, PASSWORD, DB, PORT
import aiomysql

DB_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'db': DB,
    'port': int(PORT)
}


async def get_connection():
    return await aiomysql.connect(**DB_CONFIG)
