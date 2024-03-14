import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram import F
from bot.config import Bot_Token

from bot.handlers.base_handlers import start_bot, stop_bot, started_message, base_answer
from bot.handlers.save_info import change_query, save_query, save_area
from bot.handlers.get_info import (get_query, get_vacancies, get_format_skills, get_boundary_vacancies,
                                   get_count_vacancies)
from bot.handlers.menu_handlers import get_setting, get_functional
from bot.handlers.callback_handlers import get_callback_filter, get_callback_sort, get_callback_search
from bot.handlers.callback_get_info import (get_callback_query, get_callback_vacancies, get_callback_format_skills,
                                            get_callback_boundary_vacancies, get_callback_count_vacancies)
from bot.handlers.callback_save_info import get_callback_changing_query, get_callback_filter_areas
from bot.states.states_base import StepsBase


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=Bot_Token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(started_message, CommandStart())

    dp.message.register(change_query, Command(commands=['changing_request']))
    dp.message.register(save_query, StepsBase.GET_QUERY)

    dp.message.register(get_query, StepsBase.BASE_WORK, Command(commands=['get_query']))
    dp.message.register(get_vacancies, StepsBase.BASE_WORK, Command(commands=['get_vacancies']))
    dp.message.register(get_format_skills, StepsBase.BASE_WORK, Command(commands=['get_skills']))
    dp.message.register(get_boundary_vacancies, StepsBase.BASE_WORK, Command(commands=['get_boundary_vacancies']))
    dp.message.register(get_count_vacancies, StepsBase.BASE_WORK, Command(commands='get_count_vacancies'))

    dp.message.register(get_setting, F.text == '⚙️Настройки')

    dp.callback_query.register(get_callback_filter, StepsBase.BASE_WORK, F.data == 'filters')

    dp.callback_query.register(get_callback_filter_areas, F.data == 'filter_areas')
    dp.message.register(save_area, StepsBase.GET_AREA)

    dp.callback_query.register(get_callback_sort, StepsBase.BASE_WORK, F.data == 'sort')
    dp.callback_query.register(get_callback_search, StepsBase.BASE_WORK, F.data == 'search')

    dp.message.register(get_functional, F.text == 'Функционал')

    dp.callback_query.register(get_callback_query, StepsBase.BASE_WORK, F.data == 'query')
    dp.callback_query.register(get_callback_changing_query, F.data == 'changing_query')
    dp.callback_query.register(get_callback_vacancies, StepsBase.BASE_WORK, F.data == 'vacancies')
    dp.callback_query.register(get_callback_format_skills, StepsBase.BASE_WORK, F.data == 'skills')
    dp.callback_query.register(get_callback_boundary_vacancies, StepsBase.BASE_WORK, F.data == 'boundary_vacancies')
    dp.callback_query.register(get_callback_count_vacancies, StepsBase.BASE_WORK, F.data == 'count_vacancies')

    dp.message.register(base_answer)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
