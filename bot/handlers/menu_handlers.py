from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.buttons_markup.inline_markup import filters, sorting, markup_search, slow_markup_search, profile
from utils.managers import ClientManager
from utils.utils import get_format_vacancies, get_format_skills


async def get_filter(message: Message):
    text_answer = f'''
        Выберите интересиющий вас фильтр:
    '''

    await message.answer(text_answer, reply_markup=filters)


async def get_sort(message: Message):
    text_answer = f'''
        Выберите параметры сортировки:
    '''

    await message.answer(text_answer, reply_markup=sorting)


async def get_profile(message: Message):
    text_answer = f'''
                            Профиль:
                        '''

    await message.answer(text_answer, reply_markup=profile)


async def get_skills(massage: Message, state: FSMContext):
    text_answer = f'''
        Данные собираються...
    '''

    c = ClientManager()
    await c.init(state)

    await massage.answer(text_answer)
    await massage.answer(await get_format_skills(c))


async def get_search(message: Message, state: FSMContext):
    text_answer = f'''
                Ваканси по вашим параметрам:
            '''

    c = ClientManager()
    await c.init(state)

    await message.answer(text_answer)

    vacancies, is_show_more = await get_format_vacancies(c)

    if is_show_more:
        await message.answer(vacancies, reply_markup=markup_search)
        c.change_page(c.get_page() + 1)
        await c.save()
    elif vacancies:
        await message.answer(vacancies, reply_markup=slow_markup_search)
    else:
        await message.answer('Вакансии не найдены')
