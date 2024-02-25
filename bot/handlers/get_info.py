from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import utils
from utils.keys_sort import sort_by_salaries
from utils.formats import format_vacancies


async def get_query(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer(data.get('query'))


async def get_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer(utils.get_format_vacancies(data.get('query')))


async def get_format_skills(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer('Данные собираються...')
    await massage.answer(utils.get_format_skills(data.get('query')))


async def get_boundary_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    vacancies = utils.smarted_get_vacancies(data['query'])
    vacancies = utils.custom_sort_vacancies(vacancies, key_sort=sort_by_salaries)
    vacancies = [vacancies[0], vacancies[-1]]

    await massage.answer(format_vacancies(vacancies))


async def get_count_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    count = utils.get_count_vacancies(data.get('query'), area=None)
    await massage.answer(str(count))
