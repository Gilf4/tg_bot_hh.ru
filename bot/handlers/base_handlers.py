from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.commands.set_commands import set_default_commands
from bot.buttons_markup.reply_markup import base_markup
from bot.handlers.save_info import change_query
from utils.managers import ClientManager


async def start_bot(bot: Bot):
    await set_default_commands(bot)


async def stop_bot(bot: Bot):
    await bot.session.close()


async def started_message(message: Message, state: FSMContext):
    text_answer = f'''
        Привет {message.from_user.first_name}!\r\nТы запустил бот для анализа рынка труда на прощадке hh.ru
    '''

    c = ClientManager()
    await c.init(state)

    await c.save()
    await message.answer(text_answer, reply_markup=base_markup)
    await change_query(message, state)


async def base_answer(message: Message):
    text_answer = '''
        Весь функционал можно посмотреть либо в списке команд, либо в кнопочном меню!\r\nПриятного использования бота!!!
    '''

    await message.answer(text_answer)
