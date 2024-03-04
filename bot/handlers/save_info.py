from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.states_base import StepsBase
from utils.params_get_vacancies import Params


async def change_query(message: Message, state: FSMContext):
    await message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)


async def update_query(message: Message, state: FSMContext):
    text_answer = f'''
        Текущий запрос - {message.text}    
    '''

    await message.answer(text_answer)
    await state.update_data({Params.key_text: message.text})
    await state.set_state(StepsBase.BASE_WORK)
