from aiogram.types import Message


async def start_bot(message: Message):
    text_answer = f'''
        Привет {message.from_user.first_name}!
        
        Ты запустил бот для анализа рынка труда на прощадке hh.ru
    '''

    await message.answer(text_answer)


async def base_answer(message: Message):
    text_answer = '''
        Для работы нам нужно знать ваш запрос.
         
        Чтобы его установать введите комманду "/Changing_request".
        После вы можете вызывать функции: /get_query, /get_vacancies, /get_skills, 
        /get_boundary_vacancies, /get_count_vacancies
    '''

    await message.answer(text_answer)
