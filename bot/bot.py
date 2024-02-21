import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types

from config import Bot_Token

from utils.utils import format_vacancies, get_list_of_vacancies, calculate_average_salary

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=Bot_Token)
dp = Dispatcher()


@dp.message()
async def send_vacancies(message: types.Message):
    vacancies = get_list_of_vacancies(message.text)
    await message.answer(calculate_average_salary(vacancies))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
