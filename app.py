"""
app file
"""
from aiogram.dispatcher import FSMContext as s
# imports
from aiogram.types import ContentType as ct
from loader import dp
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from functions import is_admin, users_main_menu
from states import *
from apps.user import *

# cmd start
async def cmd_start(m: m, state: s):
    if is_admin(_id=m.from_user.id):
        await m.answer("Admin botga hush kelibsiz.\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Foydalanuvchi oynasi", "Foydalanuvchilar", "Reklamalar"]))
        await Admin_state.main_menu.set()
    else:
        await m.answer(f"{m.from_user.full_name} botga hush kelibsiz.\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(users_main_menu()))
        await User_state.main_menu.set()


dp.register_message_handler(cmd_start, content_types=[ct.TEXT])

"""
USERS APPS
"""

# main_menu

dp.register_message_handler(main_menu, content_types=[ct.TEXT], state=User_state.main_menu)
dp.register_message_handler(second_menu, content_types=[ct.TEXT], state=User_state.second_menu)
