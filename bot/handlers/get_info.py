from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import utils
from utils.keys_sort import sort_by_salaries
from utils.formats import format_vacancies
from utils.params import P
from utils.managers import ClientManager


async def get_query(massage: Message, state: FSMContext):
    text = 'Вы еще не ввели запрос. Для этого воспользуйтесь /Changing_request'

    c = ClientManager()
    await c.init(state)

    query = c.get_query()

    if query:
        await massage.answer(query)
    else:
        await massage.answer(text)


async def get_vacancies(massage: Message, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    await massage.answer(await utils.get_format_vacancies(c))


async def get_format_skills(massage: Message, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    await massage.answer('Данные собираються...')
    await massage.answer(await utils.get_format_skills(c))


async def get_boundary_vacancies(massage: Message, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    vacancies = await utils.smarted_get_vacancies(c)
    vacancies = await utils.custom_sort_vacancies(vacancies, key_sort=sort_by_salaries)  # non canon

    if vacancies:
        vacancies = [vacancies[0], vacancies[-1]]
        await massage.answer(format_vacancies(vacancies))
    else:
        await massage.answer('Вакансии по вашему запросу не найдены')


async def get_count_vacancies(massage: Message, state: FSMContext):
    c = ClientManager()
    await c.init(state)

    count = await utils.get_count_vacancies(c)
    await massage.answer(str(count))
