from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from bs4 import BeautifulSoup

from aiogram.dispatcher import filters

storage = MemoryStorage()

import sqlite3

bot = Bot(token="5644768745:AAGOrfSr-ZI62Dylu6PXVgp4IBXBDFEf70U")
dp = Dispatcher(bot, storage=storage)

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.3.888 Yowser/2.5 Safari/537.36"
}

url = "https://coddyintensive.com/"
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

kb_main = ReplyKeyboardMarkup()
button1 = KeyboardButton('Курсы')
kb_main.row(button1)

@dp.message_handler(commands=["start"])
async def start(mes: types.Message):
    await mes.answer("Чтобы узнать о курсах нажмите на кнопку Курсы!\n\n", reply_markup=kb_main)

@dp.message_handler(filters.Text(contains=["Курсы"], ignore_case=True))
async def courses(mes: types.Message):
    names = soup.find_all(class_="t-name")
    courses = "Курсы: \n"
    for name in names:
        course = name.find("strong")
        if course != None:
            if course.text != "NEW!":
                courses += course.text + "\n"
    await mes.answer(courses)

executor.start_polling(dp, skip_updates=True)
