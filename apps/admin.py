"""
log in
"""
from aiogram.dispatcher import FSMContext as s
from aiogram.types import Message as m

from database.database import insert_day, delete_day, insert_media_type, insert_media, get_users_count
from keyboardbutton import keyboardbutton
from functions import users_main_menu, users_second_menu, delete_all_media, read_all_media
from loader import bot
from states import *


async def main_menu(m: m):
    """
    :param m:
    :return:
    """
    textwrap = m.text
    if textwrap == "Foydalanuvchi oynasi":
        await m.answer(f"Foydalanuvchilar menyusi.\nBayram kunlari:",
                       reply_markup=keyboardbutton(users_main_menu() + ["Qo'shish", "Chiqish"]))
        await Admin_state.second_menu.set()
    elif textwrap == "Foydalanuvchilar":
        await m.answer(f"Foydalanuvchilar ummumiy soni: {get_users_count()}")
    elif textwrap == "Reklamalar":
        await m.answer("Ushbu bo'lim vaqtincha ish faoliyatida emas!")


async def second_menu(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    if textwrap in users_main_menu() + ["Qo'shish", "Chiqish"]:
        if textwrap == "Qo'shish":
            await m.answer("Bayram kuni qo'shish.\nBayram kuni nomini kiriting:",
                           reply_markup=keyboardbutton(["Bekor qilish"]))
            await Admin_state.add_new_day.set()
        elif textwrap == "Chiqish":
            await m.answer("Chiqildi")
            await m.answer(f"Kerakli menyuni tanlashingiz mumkin:",
                           reply_markup=keyboardbutton(["Foydalanuvchi oynasi", "Foydalanuvchilar", "Reklamalar"]))
            await Admin_state.main_menu.set()
        else:
            await m.answer(f"{textwrap} uchun media turlari:", reply_markup=keyboardbutton(
                users_second_menu(textwrap) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
            await state.update_data(changed_day=textwrap)
            await Admin_state.third_menu.set()


async def third_menu(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    database = await state.get_data()
    if textwrap in users_second_menu(database.get("changed_day")):
        for media_id in read_all_media(media_type=textwrap, day=database.get("changed_day")):
            await bot.send_document(chat_id=m.chat.id, document=media_id)
        await m.answer("Medi turi uchun menyu:", reply_markup=keyboardbutton(["Media qo'shish", "O'chirish",
                                                                              "Chiqish"]))
        await state.update_data(changed_media_type=textwrap)
        await Admin_state.fourth_menu.set()
    elif textwrap == "Bayram kunini o'chirish":
        delete_day(day=database.get("changed_day"))
        await m.answer(f"{database.get('changed_day')} bayram kuni o'chirildi!")
        await m.answer(f"Foydalanuvchilar menyusi.\nBayram kunlari:",
                       reply_markup=keyboardbutton(users_main_menu() + ["Qo'shish", "Chiqish"]))
        await Admin_state.second_menu.set()
    elif textwrap == "Qo'shish":
        await m.answer(f"{database.get('changed_day')} kuni uchun yangi media turi qo'shish.\n"
                       f"Media turining nomini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.add_new_media_type.set()
    elif textwrap == "Chiqish":
        await m.answer("Chiqildi")
        await m.answer(f"Foydalanuvchilar menyusi.\nBayram kunlari:",
                       reply_markup=keyboardbutton(users_main_menu() + ["Qo'shish", "Chiqish"]))
        await Admin_state.second_menu.set()


async def fourth_menu(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    database = await state.get_data()
    if textwrap == "Chiqish":
        await m.answer(f"{database.get('changed_day')} uchun media turlari:", reply_markup=keyboardbutton(
            users_second_menu(database.get('changed_day')) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
        await Admin_state.third_menu.set()
    elif textwrap == "Media qo'shish":
        await m.answer("Mediani jo'natishingiz mumkin:\nMedia fayl(Document) ko'rinishida jo'nating!",
                       reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.add_new_media.set()
    elif textwrap == "O'chirish":
        delete_all_media(media_type=database.get("changed_media_type"), day=database.get("changed_day"))
        await m.answer("Media turi muvaffaqiyatli o'chirildi.")
        await m.answer(f"{database.get('changed_day')} uchun media turlari:", reply_markup=keyboardbutton(
            users_second_menu(database.get('changed_day')) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
        await Admin_state.third_menu.set()


async def add_new_media(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    try:
        database = await state.get_data()
        if m.document:
            file_id = m.document.file_id
        elif m.text == "Chiqish":
            for media_id in read_all_media(media_type=database.get('changed_media_type'), day=database.get(
                    "changed_day")):
                await bot.send_document(chat_id=m.chat.id, document=media_id)

            await m.answer("Medi turi uchun menyu:", reply_markup=keyboardbutton(["Media qo'shish", "O'chirish",
                                                                                  "Chiqish"]))
            await Admin_state.fourth_menu.set()
            file_id = False
        else:
            await m.answer("Medianing bu turi qo'llab quvvatlanmaydi!")
            file_id = False
        if file_id:
            database = await state.get_data()
            insert_media(media_type=database.get("changed_media_type"), media_id=file_id, day=database.get(
                "changed_day"))
            await m.answer("Medi muvaffaqiyatli qo'shildi.")
            for media_id in read_all_media(media_type=database.get('changed_media_type'), day=database.get(
                    "changed_day")):
                await bot.send_document(chat_id=m.chat.id, document=media_id)

            await m.answer("Medi turi uchun menyu:", reply_markup=keyboardbutton(["Media qo'shish", "O'chirish",
                                                                                  "Chiqish"]))
            await Admin_state.fourth_menu.set()
    except Exception as e:
        print(f"apps.admin.add_new_media -> error {e}")
        await m.answer("Yangi mediani qo'shishni iloji bo'lmadi. Iltimos qayta urinib ko'ring.")
        database = await state.get_data()
        for media_id in read_all_media(media_type=database.get('changed_media_type'), day=database.get(
                "changed_day")):
            await bot.send_document(chat_id=m.chat.id, document=media_id)

        await m.answer("Medi turi uchun menyu:", reply_markup=keyboardbutton(["Media qo'shish", "O'chirish",
                                                                              "Chiqish"]))
        await Admin_state.fourth_menu.set()


async def add_new_media_type(m: m, state: s):
    """
    :param m: 
    :param state:
    :return:
    """
    textwrap = m.text
    database = await state.get_data()
    if textwrap == "Chiqish":
        await m.answer("Chqildi")
        await m.answer(f"{database.get('changed_day')} uchun media turlari:", reply_markup=keyboardbutton(
            users_second_menu(textwrap) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
        await Admin_state.third_menu.set()
    elif textwrap:
        try:
            insert_media_type(name=textwrap, day=database.get("changed_day"))
            await m.answer("Yangi media turi muvaffaqiyatli qo'shildi.")
            await m.answer(f"{database.get('changed_day')} uchun media turlari:", reply_markup=keyboardbutton(
                users_second_menu(database.get('changed_day')) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
            await Admin_state.third_menu.set()
        except Exception as e:
            print(f"apps.admin.add_new_media_type -> error {e}")
            await m.answer("Yangi media turini qo'shishni iloji bo'lmadi. Iltimos qayta urinib ko'ring.")
            await m.answer(f"{database.get('changed_day')} uchun media turlari:", reply_markup=keyboardbutton(
                users_second_menu(textwrap) + ["Qo'shish", "Bayram kunini o'chirish", "Chiqish"]))
            await Admin_state.third_menu.set()


async def add_new_day(m: m):
    """
    :param m:
    :return:
    """
    textwrap = m.text
    if textwrap:
        if textwrap == "Chqish":
            await m.answer("Chiqildi")
            await m.answer(f"Foydalanuvchilar menyusi.\nBayram kunlari:",
                           reply_markup=keyboardbutton(users_main_menu() + ["Qo'shish", "Chiqish"]))
            await Admin_state.second_menu.set()
        elif textwrap in users_main_menu():
            await m.answer("Bunday kun mavjud!\nIltimos yangi kun kiriting:")
        else:
            try:
                insert_day(textwrap)
                await m.answer("Yangi bayram kuni muvaffaqiyatli qo'shildi.\nBayram kunlari:",
                               reply_markup=keyboardbutton(users_main_menu() + ["Qo'shish", "Chiqish"]))
            except Exception as e:
                print(f"apps.admin.add_new_day -> error: {e}")
                await m.answer("Yangi kunni qo'shishni iloji bo'lmadi. Iltimos qayta urinib ko'ring.")
            finally:
                await Admin_state.second_menu.set()
