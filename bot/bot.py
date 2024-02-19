import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from config import Bot_Token
from API import handler_api

bot = Bot(token=Bot_Token)
dp = Dispatcher()


@dp.message()
async def get_message(message: types.Message):
    # result = main.get_vacancies(str(message))
    await bot.send_message(
        chat_id=message.chat.id,
        text=main.get_vacancies(str(message))
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
