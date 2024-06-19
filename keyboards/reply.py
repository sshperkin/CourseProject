from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



back_to_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)