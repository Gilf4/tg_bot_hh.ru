import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types

from config import Bot_Token
from API.get_vacancies import get_vacancies

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=Bot_Token)
dp = Dispatcher()


def format_salary(salary_dict):
    if salary_dict:
        salary_from = salary_dict.get('from', 'Не указана')
        salary_to = salary_dict.get('to', 'Не указана')
        salary_currency = salary_dict.get('currency', '')
        # Преобразование None в "Не указана"
        if salary_from is None:
            salary_from = "Не указана"
        if salary_to is None:
            salary_to = "Не указана"
        if salary_to == "Не указана":
            return f"{salary_from} {salary_currency}"
        else:
            return f"{salary_from} - {salary_to} {salary_currency}"
    else:
        return "Зарплата не указана"


@dp.message()
async def send_vacancies(message: types.Message):
    vacancies = get_vacancies(message.text)
    if vacancies:
        vacancies_text = ''
        for item in vacancies.get('items', []):
            salary_text = format_salary(item.get('salary'))
            vacancies_text += f"Название вакансии: {item['name']}\n"
            vacancies_text += f"Зарплата: {salary_text}\n"
            vacancies_text += f"Компания: {item['employer']['name']}\n"
            vacancies_text += f"Город: {item['area']['name']}\n"
            vacancies_text += f"URL вакансии: {item['alternate_url']}\n\n"
        if vacancies_text:
            await message.answer(vacancies_text)
        else:
            await message.answer("По вашему запросу ничего не найдено.")
    else:
        await message.answer("Ошибка при запросе")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
