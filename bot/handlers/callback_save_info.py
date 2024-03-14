from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.states_base import StepsBase


async def get_callback_changing_query(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)
