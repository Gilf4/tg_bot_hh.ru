from aiogram.types import Message
from bot.buttons_markup.inline_markup import settings, functional


async def get_setting(message: Message):
    text_answer = f'''
        Настройки бота:
    '''

    await message.answer(text_answer, reply_markup=settings)


async def get_functional(message: Message):
    text_answer = f'''
            Функционал бота:
        '''

    await message.answer(text_answer, reply_markup=functional)
