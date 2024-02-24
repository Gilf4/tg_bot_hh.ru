from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import utils


async def get_query(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer(data.get('query'))


async def get_vacancies(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer(utils.format_vacancies(data.get('query')))


async def get_format_skills(massage: Message, state: FSMContext):
    data = await state.get_data()
    await massage.answer('Данные собираються...')
    await massage.answer(utils.get_format_skills(data.get('query')))
