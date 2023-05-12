"""
log in
"""
from aiogram.dispatcher import FSMContext as s
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from functions import users_main_menu, users_second_menu, read_all_media
from loader import bot
from states import *


async def main_menu(m: m, state: s):
    """
    :param state:
    :param m:
    :return:
    """
    if m.text in users_main_menu():
        await state.update_data(changed_day=m.text)
        await m.answer("Malumot turini tanlang:",
                       reply_markup=keyboardbutton(users_second_menu(first_menu=m.text) + ["Chiqish"]))
        await User_state.second_menu.set()
        await state.update_data(main_menu=m.text)
    else:
        await m.answer("Bunday menyu mavjud emas!", reply_markup=keyboardbutton(users_main_menu()+["Foydalanish "
                                                                                                   "yo'riqnomasi"]))


async def second_menu(m: m, state: s):
    """
    :param state:
    :param m:
    :return:
    """
    database = await state.get_data()
    if m.text in users_second_menu(first_menu=database.get('main_menu')):
        for media_id in read_all_media(media_type=m.text, day=database.get(
                "changed_day")):
            await bot.send_document(chat_id=m.chat.id, document=media_id)
    elif m.text == "Chiqish":
        await m.answer(f"Chiqildi!\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(users_main_menu()+["Foydalanish yo'riqnomasi"]))
        await User_state.main_menu.set()
    else:
        await m.answer("Bunday menyu mavjud emas!",
                       reply_markup=keyboardbutton(users_second_menu(first_menu=database.get('main_menu'))+["Chiqish"]))
