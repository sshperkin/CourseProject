from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from keyboards import fabrics
from utils.states import Form
router = Router()


def pagination_buttons(current_page, total_pages):
    buttons = []
    if current_page > 1:
        buttons.append(InlineKeyboardButton('◀️ Назад', callback_data='prev'))
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton('Вперед ▶️', callback_data='next'))
    return buttons

