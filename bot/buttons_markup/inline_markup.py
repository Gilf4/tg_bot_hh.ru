from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
    [InlineKeyboardButton(text='Имя профессии', callback_data='query'),
     InlineKeyboardButton(text='Сменить имя профессии', callback_data='change_query')],
    [InlineKeyboardButton(text='Поле поиска', callback_data='search_field'),
     InlineKeyboardButton(text='Сменить поле поиска', callback_data='change_search_field')],
])

search_fields = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='По названию вакансии', callback_data='save_search_field name')],
    [InlineKeyboardButton(text='По названию компании', callback_data='save_search_field company_name')],
    [InlineKeyboardButton(text='По описанию вакансии', callback_data='save_search_field description')],
    [InlineKeyboardButton(text='По требованиям к кандидату', callback_data='save_search_field requirement')]
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать профиль', callback_data='edit_profile')],
    [InlineKeyboardButton(text='Список профилей', callback_data='list_profile')]
])

bot_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сменить название', callback_data='change_name_profile')]
])


def get_list_profile(list_profiles):
    builder = InlineKeyboardBuilder()

    for name in list_profiles:
        builder.add(InlineKeyboardButton(text=name, callback_data=f'change_profile {name}'))

    builder.add(InlineKeyboardButton(text='Добавить новы профиль', callback_data='add_new_profile'))
    builder.adjust(1)
    return builder.as_markup()
