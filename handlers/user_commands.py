from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

import bot
from keyboards import reply, inline
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'Здравствуйте, приветствуем вас в нашем боте, здесь вы можете забронировать туры',
                         reply_markup=inline.main)
