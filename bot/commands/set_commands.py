from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command='/query', description='Получение запроса'),
        BotCommand(command='/changing_request', description='Задание запроса'),
        BotCommand(command='/vacancies', description='Полечение вакансий'),
        BotCommand(command='/count_vacancies', description='Получение количества вакансий'),
        BotCommand(command='/boundary_vacancies', description='Получения максимальной и минимальной вакансии по зарплате'),
        BotCommand(command='/skills', description='Получения стека технологий по вакансии'),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
