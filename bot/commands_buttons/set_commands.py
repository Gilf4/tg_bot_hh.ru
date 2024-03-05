from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command='/get_query', description='Получение запроса'),
        BotCommand(command='/changing_request', description='Задание запроса'),
        BotCommand(command='/get_vacancies', description='Полечение вакансий'),
        BotCommand(command='/get_count_vacancies', description='Получение количества вакансий'),
        BotCommand(command='/get_boundary_vacancies', description='Получения максимальной и минимальной вакансии по зарплате'),
        BotCommand(command='/get_skills', description='Получения стека технологий по вакансии'),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
