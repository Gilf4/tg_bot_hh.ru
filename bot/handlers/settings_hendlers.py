from aiogram.types import Message
from bot.buttons_markup.inline_markup import settings


async def get_setting(message: Message):
    text_answer = f'''
        Настройки бота:
    '''

    await message.answer(text_answer, reply_markup=settings)
