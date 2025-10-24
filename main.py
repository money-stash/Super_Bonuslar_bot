import asyncio
from aiogram import Bot, Dispatcher

from handlers import (
    user_commands,
    open_admin,
    change_link,
    change_post_text,
    change_img,
    change_link_text,
    change_next_post_text,
)

from data.database import initialize_db
from config import TOKEN, DB_PATH


async def main():
    await initialize_db(DB_PATH)

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        open_admin.router,
        change_link.router,
        change_post_text.router,
        change_img.router,
        change_link_text.router,
        change_next_post_text.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
