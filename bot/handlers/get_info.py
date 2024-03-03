from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import utils
from utils.keys_sort import sort_by_salaries
from utils.formats import format_vacancies
from utils.params_get_vacancies import Params


async def get_query(massage: Message, state: FSMContext):
    data = await state.get_data()
    text = 'Вы еще не ввели запрос. Для этого воспользуйтесь /Changing_request'
    print(data)

    await massage.answer(data.get(Params.key_text, text))


async def get_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer(await utils.get_format_vacancies(data))


async def get_format_skills(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer('Данные собираються...')
    await massage.answer(await utils.get_format_skills(data))


async def get_boundary_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    vacancies = await utils.smarted_get_vacancies(data)
    vacancies = await utils.custom_sort_vacancies(vacancies, key_sort=sort_by_salaries)

    if vacancies:
        vacancies = [vacancies[0], vacancies[-1]]
        await massage.answer(format_vacancies(vacancies))
    else:
        await massage.answer('Вакансии по вашему запросу не найдены')


async def get_count_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    count = await utils.get_count_vacancies(data)
    await massage.answer(str(count))
