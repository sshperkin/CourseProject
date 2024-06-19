from aiogram import Bot, Dispatcher
import asyncio
from data import database as db

from handlers import user_commands, bot_messages
from callbacks import callbacks


async def on_startup(_):
    await db.db_start()
    print("Бот успешно запущен")


async def main():
    TOKEN_API = "7126435650:AAHkaUPGPwYAGTTPR4jglOw0CyOwEL4noyA"
    bot = Bot(TOKEN_API)
    dp = Dispatcher()

    dp.include_routers(
        callbacks.router,
        user_commands.router,
        db.router,
        bot_messages.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup)
    await db.db_start()

if __name__ == '__main__':
    asyncio.run(main())
