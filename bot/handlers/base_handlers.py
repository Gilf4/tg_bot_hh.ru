from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.commands.set_commands import set_default_commands
from bot.buttons_markup.reply_markup import base_markup
from utils.params import P


async def start_bot(bot: Bot):
    await set_default_commands(bot)


async def stop_bot(bot: Bot):
    await bot.session.close()


async def started_message(message: Message, state: FSMContext):
    text_answer = f'''
        Привет {message.from_user.first_name}!\r\nТы запустил бот для анализа рынка труда на прощадке hh.ru
    '''

    await state.update_data({P.ind_profile: P.base, P.profiles: {P.base: {P.request_parameters: {}, P.filters: [], P.sorts: []}}})
    await message.answer(text_answer, reply_markup=base_markup)


async def base_answer(message: Message):
    text_answer = '''
        Для работы нам нужно знать ваш запрос. Чтобы его установать используйте комманду /changing_request.
    '''

    await message.answer(text_answer)
