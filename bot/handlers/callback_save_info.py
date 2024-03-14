from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.states_base import StepsBase


async def get_callback_changing_query(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)


async def get_callback_filter_areas(call: CallbackQuery, state):
    await call.message.answer('Введите регион, город...')
    await state.set_state(StepsBase.GET_AREA)


async def get_callback_filter_salary(call: CallbackQuery, state):
    await call.message.answer('Введите подходящую для вас зарплату')
    await state.set_state(StepsBase.GET_SALARY)
