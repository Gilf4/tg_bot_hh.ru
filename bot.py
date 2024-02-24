import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from bot.config import Bot_Token

from bot.handlers.base_handlers import start_bot, base_answer, changing_query, update_query
from bot.handlers.get_info import get_query, get_vacancies, get_format_skills
from bot.states.states_base import StepsBase


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=Bot_Token, parse_mode='HTML')
    dp = Dispatcher()

    dp.message.register(start_bot, CommandStart())
    dp.message.register(changing_query, Command(commands=['Changing_request']))
    dp.message.register(update_query, StepsBase.GET_QUERY)

    dp.message.register(get_query, StepsBase.BASE_WORK, Command(commands=['get_query']))
    dp.message.register(get_vacancies, StepsBase.BASE_WORK, Command(commands=['get_vacancies']))
    dp.message.register(get_format_skills, StepsBase.BASE_WORK, Command(commands=['get_skills']))
    dp.message.register(base_answer, Command(commands=['get_query', 'get_vacancies', 'get_skills']))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
