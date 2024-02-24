from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.states_base import StepsBase


async def start_bot(message: Message):
    text_answer = f'''
        Привет {message.from_user.first_name}!
        Ты запустил бот для анализа рынка труда на прощадке hh.ru
    '''

    await message.answer(text_answer)


async def base_answer(message: Message):
    text_answer = f'''
            Для работы нам нужно знать ваш запрос.
            Чтобы его установать введите комманду "/Changing_request"
        '''

    await message.answer(text_answer)


async def changing_query(message: Message, state: FSMContext):
    await message.answer('Введите интересующую вас вакансию')
    await state.set_state(StepsBase.GET_QUERY)


async def update_query(message: Message, state: FSMContext):
    text_answer = f'''
        Текущий запрос - {message.text}    
    '''

    await message.answer(text_answer)
    await state.update_data(query=message.text)
    await state.set_state(StepsBase.BASE_WORK)
