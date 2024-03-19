from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.buttons_markup.inline_markup import markup_search, slow_markup_search, experience
from utils.managers import ClientManager
from utils.utils import get_format_vacancies


async def get_callback_search_parameters(call: CallbackQuery):
    text_answer = f'''
        Выберите интересиющий вас параметр поиска:
    '''

    # await call.message.answer(text_answer, reply_markup=)


async def get_callback_show_more(call: CallbackQuery, state: FSMContext):

    c = ClientManager()
    await c.init(state)

    vacancies, is_show_more = await get_format_vacancies(c)

    if is_show_more:
        await call.message.answer(vacancies, reply_markup=markup_search)
        c.change_page(c.get_page() + 1)
        await c.save()
    elif vacancies:
        await call.message.answer(vacancies, reply_markup=slow_markup_search)
    else:
        await call.message.answer('Вакансии не найдены')


async def get_filter_experience(call: CallbackQuery):
    text_answer = f'''
            Выберите категорию опыта:
        '''

    await call.message.answer(text_answer, reply_markup=experience)
