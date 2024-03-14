from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.buttons_markup.inline_markup import filters, sorting, search_parameters


async def get_callback_filter(call: CallbackQuery):
    text_answer = f'''
        Выберите интересиющий вас фильтр:
    '''

    await call.message.answer(text_answer, reply_markup=filters)


async def get_callback_sort(call: CallbackQuery):
    text_answer = f'''
        Выберите параметры сортировки:
    '''

    await call.message.answer(text_answer, reply_markup=sorting)


async def get_callback_search(call: CallbackQuery):
    text_answer = f'''
        Выберите интересиющий вас параметр поиска:
    '''

    await call.message.answer(text_answer, reply_markup=search_parameters)
