from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.buttons_markup.inline_markup import (markup_search, slow_markup_search, experience,
                                              search_parameters, search_fields, profile, get_list_profile,
                                              bot_settings)
from utils.managers import ClientManager
from utils.utils import get_format_vacancies, get_salaries, calculate_average, calculate_median


async def get_callback_show_more(call: CallbackQuery, state: FSMContext):

    c = ClientManager()
    await c.init(state)

    vacancies, is_show_more = await get_format_vacancies(c)

    if is_show_more:
        await call.message.answer(vacancies, reply_markup=markup_search)
        c.change_page(c.get_page() + 1)
        await c.save()
    elif vacancies:
        await call.message.answer(vacancies, reply_markup=slow_markup_search)
    else:
        await call.message.answer('Вакансии не найдены', reply_markup=slow_markup_search)


async def get_callback_filter_experience(call: CallbackQuery):
    text_answer = f'''
            Выберите категорию опыта:
        '''

    await call.message.answer(text_answer, reply_markup=experience)


async def get_callback_average_salary(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    average_salary = await calculate_average(await get_salaries(c))
    await call.message.answer(f'Средняя зарплата по вакансиям - {average_salary}')


async def get_callback_median_salary(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    median_salary = await calculate_median(await get_salaries(c))
    await call.message.answer(f'Медиана зарплаты по вакансиям - {median_salary}')


async def get_callback_search_parameters(call: CallbackQuery):
    text_answer = f'''
                Параметры поиска:
            '''

    await call.message.answer(text_answer, reply_markup=search_parameters)


async def get_callback_change_search_field(call: CallbackQuery):
    text_answer = f'''
                    Выберите параметр поиска:
                '''

    await call.message.answer(text_answer, reply_markup=search_fields)


async def get_callback_edit_profile(call: CallbackQuery):
    text_answer = f'''
                        Настройки бота:
                    '''

    await call.message.answer(text_answer, reply_markup=bot_settings)


async def get_callback_list_profile(call: CallbackQuery, state: FSMContext):
    text_answer = f'''
                        Профили:
                    '''

    c = ClientManager()
    await c.init(state)

    profiles = get_list_profile(c.get_names_profiles())
    await call.message.answer(text_answer, reply_markup=profiles)
