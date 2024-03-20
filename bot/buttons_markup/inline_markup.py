from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фильтры', callback_data='filters'),
     InlineKeyboardButton(text='Сортировка', callback_data='sort')],
    [InlineKeyboardButton(text='Параметры поиска', callback_data='search')]
])

filters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарплата', callback_data='filter_salary')],
    [InlineKeyboardButton(text='Опыт', callback_data='filter_experience')],
    [InlineKeyboardButton(text='Регион, город...', callback_data='filter_areas')],
    # [InlineKeyboardButton(text='Только популярные компании', callback_data='filter_popular_companies')]
])

sorting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Средняя зарплата', callback_data='average_salary')],
    [InlineKeyboardButton(text='Медиана зарплаты', callback_data='median_salary')],
    [InlineKeyboardButton(text='Сортировка по зарплате', callback_data='sort_salary')],
    [InlineKeyboardButton(text='Сортировка по возрастанию', callback_data='sort_ascending_order')],
    [InlineKeyboardButton(text='Сортировка по убыванию', callback_data='sort_descending_order')]
])

markup_search = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Параметры поиска', callback_data='search_parameters')],
    [InlineKeyboardButton(text='Показать ещё', callback_data='show_more')]
])

slow_markup_search = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Параметры поиска', callback_data='search_parameters')],
])

experience = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Нет опыта', callback_data='experience_Нет опыта')],
    [InlineKeyboardButton(text='От 1 года до 3 лет', callback_data='experience_От 1 года до 3 лет')],
    [InlineKeyboardButton(text='От 3 до 6 лет', callback_data='experience_От 3 до 6 лет')],
    [InlineKeyboardButton(text='Более 6 лет', callback_data='experience_Более 6 лет')],
    [InlineKeyboardButton(text='Любой', callback_data='experience_Любой')],
])

search_parameters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запрос', callback_data='query'),
     InlineKeyboardButton(text='Сменить запрос', callback_data='change_query')],
    [InlineKeyboardButton(text='Поле поиска', callback_data='search_field'),
     InlineKeyboardButton(text='Сменить поле поиска', callback_data='change_search_field')],
])

search_fields = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='По названию вакансии', callback_data='save_search_field name')],
    [InlineKeyboardButton(text='По названию компании', callback_data='save_search_field company_name')],
    [InlineKeyboardButton(text='По описанию вакансии', callback_data='save_search_field description')],
    [InlineKeyboardButton(text='По требованиям к кандидату', callback_data='save_search_field requirement')],
    [InlineKeyboardButton(text='По всем словам', callback_data='save_search_field all_words')],
])
