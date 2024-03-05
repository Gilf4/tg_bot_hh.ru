from aiogram import Bot
from aiogram.types import Message
from bot.commands_buttons.set_commands import set_default_commands


async def start_bot(bot: Bot):
    await set_default_commands(bot)


async def stop_bot(bot: Bot):
    await bot.session.close()


async def started_message(message: Message):
    text_answer = f'''
        Привет {message.from_user.first_name}!
        
        Ты запустил бот для анализа рынка труда на прощадке hh.ru
    '''
    
    await message.answer(text_answer)


async def base_answer(message: Message):
    text_answer = '''
        Для работы нам нужно знать ваш запрос. Чтобы его установать используйте комманду /changing_request.
    '''

    await message.answer(text_answer)
