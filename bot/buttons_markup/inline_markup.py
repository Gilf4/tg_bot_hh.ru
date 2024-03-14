from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фильтры', callback_data='filters'),
     InlineKeyboardButton(text='Сортировка', callback_data='sort')],
    [InlineKeyboardButton(text='Параметры поиска', callback_data='search')]
])

functional = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запрос', callback_data='query'),
     InlineKeyboardButton(text='Изменить запрос', callback_data='changing_query')],
    [InlineKeyboardButton(text='Вакансии', callback_data='vacancies'),
     InlineKeyboardButton(text='Количество вакансии', callback_data='count_vacancies')],
    [InlineKeyboardButton(text='Пограничные вакансии', callback_data='boundary_vacancies')],
    [InlineKeyboardButton(text='Стек технологий', callback_data='skills')]
])

filters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарплата', callback_data='filter_salary')],
    [InlineKeyboardButton(text='Опыт', callback_data='filter_experience')],
    [InlineKeyboardButton(text='Регион, город...', callback_data='filter_areas')],
    [InlineKeyboardButton(text='Только популярные компании', callback_data='filter_popular_companies')]
])

sorting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарплата', callback_data='sort_salary')],
    [InlineKeyboardButton(text='Опыт', callback_data='sort_experience')]
])

search_parameters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поле поиска', callback_data='search_field')],
    [InlineKeyboardButton(text='Что ищем?', callback_data='search_text')]
])
