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

    if await c.init(state) and c.change_query(message.text):
        c.change_is_new_vacancies(False)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await message.answer(text_answer)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_area(message: Message, state: FSMContext):
    text_answer = f'''
        Текущий регион, город... - {message.text}    
    '''

    c = ClientManager()

    if await c.init(state) and c.change_area(message.text):
        c.change_is_new_vacancies(False)
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await message.answer(text_answer)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_salary(message: Message, state: FSMContext):
    text_answer = f'''
            Текущая просматриваемая зарплата: {message.text}    
        '''

    c = ClientManager()

    if await c.init(state) and c.change_salary(message.text):
        c.change_is_new_vacancies(False)
        await c.save()
        await state.set_state(StepsBase.BASE_WORK)
        await message.answer(text_answer)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')


async def save_name_profile(message: Message, state: FSMContext):
    text_answer = f'''
                Ваше новой название профиля: {message.text}
            '''

    c = ClientManager()

    for name in c.get_names_profiles():
        if message.text == name:
            await message.message.answer('Такое имя уже есть. Попробуйте другое')
            return

    if await c.init(state) and c.change_name_profile(message.text):
        await c.save()
        await c.set_state(StepsBase.BASE_WORK)
        await message.answer(text_answer)
    else:
        await message.answer('Что-то пошло не так. Попробуйте ещё раз')
