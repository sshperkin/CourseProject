import sqlite3 as sq
from aiogram import Router
from aiogram.types import Message
from utils.states import Form
from aiogram.fsm.context import FSMContext
from keyboards import inline

router = Router()
db = sq.connect('tgbotdata.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS countries("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "country TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS cities("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "city TEXT, "
                "photo TEXT,"
                "country_id INTEGER)")
    db.commit()
    db.close()


@router.message(Form.country)
async def choose_dates(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(Form.dates)
    await message.answer("Отличный выбор, введите даты вылета в таком формате 17.06.24 - 24.06.24",
                         reply_markup=inline.back_to_main)


@router.message(Form.dates)
async def choose_people(message: Message, state: FSMContext):
    await state.update_data(dates=message.text)
    await state.set_state(Form.people_num)
    await message.answer("Отлично, введите количество человек", reply_markup=inline.back_to_main)


@router.message(Form.people_num)
async def finalize(message: Message, state: FSMContext):
    await state.update_data(people_num=message.text)
    country = "Турция"
    await state.clear()
    cur.execute("""SELECT city_name
                FROM cities 
                JOIN countries ON country_id=id
                WHERE country_name = ? """, (country,))
    cities = cur.fetchall()
    await message.answer(f"В стране {country} найдены туры в городах: {", ".join(x[0] for x in cities)}")
