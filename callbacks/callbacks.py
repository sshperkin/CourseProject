from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards import inline, fabrics
router = Router()


@router.callback_query(F.data == "back")
async def BackMainCallback(callback: CallbackQuery):
    await callback.message.answer('вы вернулись в главное меню', reply_markup=inline.main)


@router.callback_query(F.data == "support")
async def support_call(callback: CallbackQuery):
    support_text = """
        Связаться с нами напрямую:
        - Telegram: @savvapepe
        - E-mail: slshperkin@edu.hse.ru 
        """
    await callback.message.answer(text=support_text, reply_markup=inline.links)


@router.callback_query(F.data == "help")
async def help_call(callback: CallbackQuery):
    document = FSInputFile(path="/Users/savvashperkin/Downloads/help.pdf")
    await callback.message.answer(text='Руководство пользователя читайте ниже')
    await callback.message.answer_document(document=document, reply_markup=inline.back_to_main)


@router.callback_query(F.data == "about")
async def about_call(callback: CallbackQuery):
    about_text = """
        BookToursBot - это удобное и простое решение для бронирования и подбора туров прямо в Telegram,
        реализованное с помощью Python и библиотеки aiogram
        """
    await callback.message.answer(text=about_text, reply_markup=inline.back_to_main)


@router.callback_query(F.data == "book")
async def choose_country(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.country)
    await callback.message.answer("Введите страну назначения", reply_markup=inline.back_to_main)



