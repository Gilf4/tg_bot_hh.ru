from aiogram import Bot
from aiogram.types import Message, CallbackQuery


async def get_callback_filter(callback: CallbackQuery):
    text_answer = f'''
        Привет {callback.id}!\r\nТы запустил бот для анализа рынка труда на прощадке hh.ru
    '''

    await callback.answer(text_answer)
