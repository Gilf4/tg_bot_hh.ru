from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.states_base import StepsBase
from utils.managers import ClientManager
from utils.get_info import get_experience
from utils.keys_sort import sort_by_salaries
from utils.utils import custom_sort_vacancies


async def get_callback_changing_query(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)


async def get_callback_filter_areas(call: CallbackQuery, state):
    await call.message.answer('Введите регион, город...')
    await state.set_state(StepsBase.GET_AREA)


async def get_callback_filter_salary(call: CallbackQuery, state):
    await call.message.answer('Введите диапозон зарплаты через (пример "10000-50000")')
    await state.set_state(StepsBase.GET_SALARY)


async def save_callback_experience(call: CallbackQuery, state: FSMContext):
    experience = call.data.split('_')[1]

    text_answer = f'''
            Текущая категория: - {experience}    
        '''

    c = ClientManager()
    experience = get_experience().get(experience, None)

    if await c.init(state) and (experience is not None) and c.change_experience(experience):
        c.change_is_new_vacancies(False)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await call.message.answer(text_answer)
    else:
        await call.message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_callback_sort_salary(call: CallbackQuery, state: FSMContext):
    text_answer = f'''
            Текущая сортировка: по цене
        '''

    c = ClientManager()

    if await c.init(state) and c.change_key_sort(sort_by_salaries):
        vacancies = await custom_sort_vacancies(c.get_vacancies(), sort_by_salaries, c.get_revers_sort())
        c.change_vacancies(vacancies)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await call.message.answer(text_answer)
    else:
        await call.message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def get_callback_sort_ascending_order(call: CallbackQuery, state: FSMContext):
    text_answer = f'''
                Сортировка: по возрастанию
            '''

    c = ClientManager()

    if await c.init(state) and c.change_revers_sort(False):
        vacancies = await custom_sort_vacancies(c.get_vacancies(), sort_by_salaries, c.get_revers_sort())
        c.change_vacancies(vacancies)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await call.message.answer(text_answer)
    else:
        await call.message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def get_callback_sort_descending_order(call: CallbackQuery, state: FSMContext):
    text_answer = f'''
                Сортировка: по убыванию
            '''

    c = ClientManager()

    if await c.init(state) and c.change_revers_sort(True):
        vacancies = await custom_sort_vacancies(c.get_vacancies(), sort_by_salaries, c.get_revers_sort())
        c.change_vacancies(vacancies)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await call.message.answer(text_answer)
    else:
        await call.message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_callback_search_field(call: CallbackQuery, state: FSMContext):
    search_field = call.data.split()[-1]

    text_answer = f'''
                Поиск по параметру: {search_field}
            '''

    c = ClientManager()

    if await c.init(state) and c.change_search_field(search_field):
        c.change_is_new_vacancies(False)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await call.message.answer(text_answer)
    else:
        await call.message.answer('Что-то пошло не так. Попробуйте ещё раз')