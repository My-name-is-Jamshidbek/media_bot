"""
log in
"""
from aiogram.dispatcher import FSMContext as s
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from functions import is_admin, users_main_menu, users_second_menu
from states import *


async def main_menu(m: m, state: s):
    """
    :param m:
    :return:
    """
    if m.text in users_main_menu():
        await m.answer("Malumot turini tanlang:",
                       reply_markup=keyboardbutton(users_second_menu(first_menu=m.text) + ["Chiqish"]))
        await User_state.second_menu.set()
        await state.update_data(main_menu=m.text)
    else:
        await m.answer("Bunday menyu mavjud emas!", reply_markup=keyboardbutton(users_main_menu()))


async def second_menu(m: m, state: s):
    """
    :param state:
    :param m:
    :return:
    """
    database = await state.get_data()
    if m.text in users_second_menu(first_menu=database.get('main_menu')):
        await m.answer('1')
    elif m.text == "Chiqish":
        await m.answer(f"Chiqildi!\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(users_main_menu()))
        await User_state.main_menu.set()
    else:
        await m.answer("Bunday menyu mavjud emas!",
                       reply_markup=keyboardbutton(users_second_menu(first_menu=database.get('main_menu'))))
