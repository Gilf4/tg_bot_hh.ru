from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.states_base import StepsBase
from utils.managers import ClientManager


async def change_query(message: Message, state: FSMContext):
    await message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)


async def save_query(message: Message, state: FSMContext):
    text_answer = f'''
        Текущий запрос - {message.text}    
    '''

    c = ClientManager()

    if await c.init(state) and c.save_query(message.text):
        await message.answer(text_answer)
        await state.set_state(StepsBase.BASE_WORK)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_area(message: Message, state: FSMContext):
    text_answer = f'''
        Текущий регион, город... - {message.text}    
    '''

    c = ClientManager()

    if await c.init(state) and c.save_area(message.text):
        await message.answer(text_answer)
        await state.set_state(StepsBase.BASE_WORK)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_salary(message: Message, state: FSMContext):
    text_answer = f'''
            Текущая просматриваемая зарплата - {message.text}    
        '''

    c = ClientManager()

    if await c.init(state) and c.save_salary(message.text):
        await message.answer(text_answer)
        await state.set_state(StepsBase.BASE_WORK)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')
