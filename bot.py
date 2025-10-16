import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database.db import init_db
from handlers import categories
from handlers.client import order_form, products, start

async def main():
    init_db()  
    bot = Bot(token=TOKEN, parse_mode="Markdown")
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(categories.router)
    dp.include_router(products.router)
    dp.include_router(order_form.router)

    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
