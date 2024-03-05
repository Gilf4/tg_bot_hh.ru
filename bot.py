import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from bot.config import Bot_Token

from bot.handlers.base_handlers import start_bot, stop_bot, started_message, base_answer
from bot.handlers.save_info import change_query, update_query
from bot.handlers.get_info import (get_query, get_vacancies, get_format_skills, get_boundary_vacancies,
                                   get_count_vacancies)
from bot.states.states_base import StepsBase


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=Bot_Token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(started_message, CommandStart())

    dp.message.register(change_query, Command(commands=['changing_request']))
    dp.message.register(update_query, StepsBase.GET_QUERY)

    dp.message.register(get_query, StepsBase.BASE_WORK, Command(commands=['get_query']))
    dp.message.register(get_vacancies, StepsBase.BASE_WORK, Command(commands=['get_vacancies']))
    dp.message.register(get_format_skills, StepsBase.BASE_WORK, Command(commands=['get_skills']))
    dp.message.register(get_boundary_vacancies, StepsBase.BASE_WORK, Command(commands=['get_boundary_vacancies']))
    dp.message.register(get_count_vacancies, StepsBase.BASE_WORK, Command(commands='get_count_vacancies'))

    dp.message.register(base_answer)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
