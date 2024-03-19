from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ⚙️

base_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Фильтры'), KeyboardButton(text='Искать'), KeyboardButton(text='Скилы'),
     KeyboardButton(text='Сортировка')],
    [KeyboardButton(text='Профиль')]
], resize_keyboard=True)
