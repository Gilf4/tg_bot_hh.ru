from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


base_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки'), KeyboardButton(text='Функционал')],
    [KeyboardButton(text='Потдержать проект')]
], resize_keyboard=True)
