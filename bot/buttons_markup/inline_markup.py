from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фильтры', callback_data='filter'),
     InlineKeyboardButton(text='Сортировка', callback_data='sort')],
    [InlineKeyboardButton(text='Параметры поиска', callback_data='search')]
])
