from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import fabrics
router = Router()

@router.callback_query(fabrics.Pagination.filter(F.action.in_(["perv","next"])))
async def pagination_handler(call:CallbackQuery, callback_data: fabrics.Pagination):
    page_num = int(callback_data.page)
    page = page_num -1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(tours) - 1) else page_num
