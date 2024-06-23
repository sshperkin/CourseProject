from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram", url=f'https://t.me/savvapepe'),
            InlineKeyboardButton(text="Vk", url=f'https://vk.com/sshperkin')
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подобрать тур", callback_data="book"),
            InlineKeyboardButton(text="О нас", callback_data="about")
        ],
        [
            InlineKeyboardButton(text="Помощь", callback_data='help'),
            InlineKeyboardButton(text="Поддержка", callback_data="support")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
)

back_to_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)

select_tour = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Забронировать!", callback_data="select")
        ]
    ]
)