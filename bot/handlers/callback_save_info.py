from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.states_base import StepsBase
from utils.managers import ClientManager
from utils.get_info import get_experience


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
