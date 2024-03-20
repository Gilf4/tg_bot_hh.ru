import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram import F
from bot.config import Bot_Token

from bot.handlers.base_handlers import start_bot, stop_bot, started_message, base_answer
from bot.handlers.save_info import change_query, save_query, save_area, save_salary
from bot.handlers.get_info import (get_query, get_boundary_vacancies,
                                   get_count_vacancies)
from bot.handlers.menu_handlers import get_filter, get_search, get_sort, get_skills, get_profile
from bot.handlers.callback_handlers import (get_callback_search_parameters, get_callback_show_more,
                                            get_callback_filter_experience, get_callback_average_salary,
                                            get_callback_median_salary, get_callback_change_search_field)
from bot.handlers.callback_get_info import get_callback_query, get_callback_search_field
from bot.handlers.callback_save_info import (get_callback_filter_areas, save_callback_experience,
                                             get_callback_filter_salary, save_callback_sort_salary,
                                             get_callback_sort_ascending_order, get_callback_sort_descending_order,
                                             get_callback_changing_query, save_callback_search_field)
from bot.states.states_base import StepsBase


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=Bot_Token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(started_message, CommandStart())

    # register handlers reply markup
    dp.message.register(get_filter, StepsBase.BASE_WORK, F.text == 'Фильтры')
    dp.message.register(get_search, StepsBase.BASE_WORK, F.text == 'Искать')
    dp.message.register(get_skills, StepsBase.BASE_WORK, F.text == 'Скилы')
    dp.message.register(get_sort, StepsBase.BASE_WORK, F.text == 'Сортировка')
    dp.message.register(get_profile, StepsBase.BASE_WORK, F.text == 'Профиль')

    # register handlers commands
    dp.message.register(get_query, StepsBase.BASE_WORK, Command(commands=['query']))
    dp.message.register(get_search, StepsBase.BASE_WORK, Command(commands=['vacancies']))
    dp.message.register(get_skills, StepsBase.BASE_WORK, Command(commands=['skills']))
    dp.message.register(get_search, StepsBase.BASE_WORK, Command(commands=['vacancies']))
    dp.message.register(get_skills, StepsBase.BASE_WORK, Command(commands=['skills']))
    dp.message.register(get_boundary_vacancies, StepsBase.BASE_WORK, Command(commands=['boundary_vacancies']))
    dp.message.register(get_count_vacancies, StepsBase.BASE_WORK, Command(commands='count_vacancies'))

    # register handlers save and changing info
    dp.message.register(change_query, Command(commands=['changing_request']))
    dp.message.register(save_query, StepsBase.GET_QUERY)

    # register handlers filter
    dp.callback_query.register(get_callback_filter_experience, F.data == 'filter_experience')
    dp.callback_query.register(save_callback_experience, F.data[:10] == 'experience')
    dp.callback_query.register(get_callback_filter_areas, F.data == 'filter_areas')
    dp.callback_query.register(get_callback_filter_salary, F.data == 'filter_salary')
    dp.message.register(save_salary, StepsBase.GET_SALARY)
    dp.message.register(save_area, StepsBase.GET_AREA)

    # register handlers inline buttons
    dp.callback_query.register(get_callback_search_parameters, StepsBase.BASE_WORK, F.data == 'search_parameters')
    dp.callback_query.register(get_callback_show_more, StepsBase.BASE_WORK, F.data == 'show_more')

    # register handlers search parameters
    dp.callback_query.register(get_callback_search_parameters, F.data == 'search_parameters')
    dp.callback_query.register(get_callback_query, F.data == 'query')
    dp.callback_query.register(get_callback_changing_query, F.data == 'change_query')
    dp.callback_query.register(get_callback_search_field, F.data == 'search_field')
    dp.callback_query.register(get_callback_change_search_field, F.data == 'change_search_field')
    dp.callback_query.register(save_callback_search_field, F.data[:17] == 'save_search_field')

    # register handlers inline sort
    dp.callback_query.register(save_callback_sort_salary, F.data == 'sort_salary')
    dp.callback_query.register(get_callback_average_salary, F.data == 'average_salary')
    dp.callback_query.register(get_callback_median_salary, F.data == 'median_salary')
    dp.callback_query.register(get_callback_sort_ascending_order, F.data == 'sort_ascending_order')
    dp.callback_query.register(get_callback_sort_descending_order, F.data == 'sort_descending_order')
    dp.message.register(base_answer)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
