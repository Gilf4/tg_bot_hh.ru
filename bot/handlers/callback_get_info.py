from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils import utils
from utils.keys_sort import sort_by_salaries
from utils.formats import format_vacancies
from utils.params_get_vacancies import Params


async def get_callback_query(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = 'Вы еще не ввели запрос. Для этого воспользуйтесь /Changing_request'
    print(data)

    await call.answer(data.get(Params.key_text, text))


async def get_callback_vacancies(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer(await utils.get_format_vacancies(data))


async def get_callback_format_skills(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print('Step 1 ----------------')
    print(data)
    await call.message.answer('Данные собираються...')
    await call.message.answer(await utils.get_format_skills(data))


async def get_callback_boundary_vacancies(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    vacancies = await utils.smarted_get_vacancies(data)
    vacancies = await utils.custom_sort_vacancies(vacancies, key_sort=sort_by_salaries)

    if vacancies:
        vacancies = [vacancies[0], vacancies[-1]]
        await call.message.answer(format_vacancies(vacancies))
    else:
        await call.answer('Вакансии по вашему запросу не найдены')


async def get_callback_count_vacancies(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = await utils.get_count_vacancies(data)
    await call.answer(str(count))
