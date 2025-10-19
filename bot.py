import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, PARSE_MODE
from database.db import init_db
from handlers import categories
from handlers.client import order_form, products, start
from handlers.admin import manage_products

async def main():
    init_db()  
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=PARSE_MODE))
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры в правильном порядке (админ роутеры первыми)
    dp.include_router(manage_products.router)
    dp.include_router(start.router)
    dp.include_router(categories.router)
    dp.include_router(products.router)
    dp.include_router(order_form.router)

    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
