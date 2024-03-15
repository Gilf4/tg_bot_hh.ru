from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils import utils
from utils.keys_sort import sort_by_salaries
from utils.formats import format_vacancies
from utils.managers import ClientManager


async def get_callback_query(call: CallbackQuery, state: FSMContext):
    text = 'Вы еще не ввели запрос. Для этого воспользуйтесь /Changing_request'

    c = ClientManager()
    await c.init(state)

    query = c.get_query()

    if query:
        await call.answer(query)
    else:
        await call.massage.answer(text)


async def get_callback_vacancies(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    await call.message.answer(await utils.get_format_vacancies(c))


async def get_callback_format_skills(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    await call.message.answer('Данные собираються...')
    await call.message.answer(await utils.get_format_skills(c))


async def get_callback_boundary_vacancies(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    vacancies = await utils.smarted_get_vacancies(c)
    vacancies = await utils.custom_sort_vacancies(vacancies, key_sort=sort_by_salaries)  # not canon

    if vacancies:
        vacancies = [vacancies[0], vacancies[-1]]
        await call.message.answer(format_vacancies(vacancies))
    else:
        await call.answer('Вакансии по вашему запросу не найдены')


async def get_callback_count_vacancies(call: CallbackQuery, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    count = await utils.get_count_vacancies(c)
    await call.answer(str(count))
