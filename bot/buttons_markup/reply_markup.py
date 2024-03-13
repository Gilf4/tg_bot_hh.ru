from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


base_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки'), KeyboardButton(text='Функционал')]
], resize_keyboard=True)
