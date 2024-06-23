import re
import sqlite3 as sq
from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, FSInputFile, CallbackQuery, InputMediaPhoto, InputFile)

from keyboards import fabrics
from keyboards import inline
from utils.states import Form

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


async def get_tours(state: FSMContext):
    data = await state.get_data()
    cur.execute("""SELECT city_name
                    FROM cities 
                    JOIN countries ON country_id=id
                    WHERE country_name = ? """, (data['country'],))
    cities = cur.fetchall()
    return cities


async def get_city(state: FSMContext):
    data = await state.get_data()
    cur.execute("""SELECT city_name
                        FROM cities 
                        WHERE city_name = ? """, (data['city'],))
    city = cur.fetchall()
    return city


def is_date_valid(text):
    # Регулярное выражение для проверки формата даты
    date_pattern = r'\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}'

    # Проверка соответствия введенной строки регулярному выражению
    if re.match(date_pattern, text):
        return True
    else:
        return False


@router.message(Form.country)
async def choose_dates(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(Form.dates)
    await message.answer("Отличный выбор, введите даты вылета в таком формате ДД.ММ.ГГ - ДД.ММ.ГГ",
                         reply_markup=inline.back_to_main)


@router.message(Form.dates)
async def choose_people(message: Message, state: FSMContext):
    if is_date_valid(message.text):
        await state.update_data(dates=message.text)
        await state.set_state(Form.people_num)
        await message.answer("Отлично, введите количество человек", reply_markup=inline.back_to_main)
    else:
        await message.answer("Некорректная дата, введите дату поездки в формате : ДД.ММ.ГГ - ДД.ММ.ГГ",
                             reply_markup=inline.back_to_main)


@router.message(Form.people_num)
async def finalize(message: Message, state: FSMContext):
    await state.update_data(people_num=message.text)
    data = await state.get_data()
    cur.execute("""SELECT city_name
                FROM cities 
                JOIN countries ON country_id=id
                WHERE country_name = ? """, (data['country'],))
    cities = cur.fetchall()
    if len(cities) != 0:
        await message.answer(f"В стране {data['country']} найдены туры в городах:"
                             f" {", ".join(x[0] for x in cities)}."
                             f"\nВведите желаемый город из предложенных",
                             reply_markup=inline.back_to_main)
        await state.set_state(Form.city)
    else:
        await message.answer("К сожалению в стране, которую вы ввели, не было найдено туров")


@router.message(Form.city)
async def choose_people(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    cur.execute("""SELECT city_name
                    FROM cities 
                    WHERE city_name = ? """, (data['city'],))
    city = cur.fetchall()
    if len(city) != 0:
        await message.answer(f"Вы выбрали город {data['city']}, желаете забронировать тур?",
                             reply_markup=inline.select_tour)
    else:
        await message.answer("Вы ввели город в котором нету туров, пожалуйста попробуйте еще раз")


@router.callback_query(F.data == "select")
async def choose_country(callback: CallbackQuery, state: FSMContext):
    city = await get_city(state)
    photo = FSInputFile(path=f"/Users/savvashperkin/Downloads/{city[0][0]}.jpeg")
    data = await state.get_data()
    await callback.message.answer_photo(photo,
                                        f"Вы выбрали тур в стране {data['country']},{data['city']}\n"
                                        f"Количество персон:{data['people_num']}\nДаты: {data['dates']}")
