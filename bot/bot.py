import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types

from config import Bot_Token

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=Bot_Token)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
