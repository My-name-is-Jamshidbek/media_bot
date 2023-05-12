"""
app file
"""
# imports
from aiogram.types import ContentType as ct

from loader import dp
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from functions import is_admin, users_main_menu
from states import *
from apps import user, admin
from database.database import add_user, create_database


# cmd start
async def cmd_start(m: m):
    """
    :param m:
    :return:
    """
    # create_database()
    if is_admin(_id=m.from_user.id):
        await m.answer("Admin botga hush kelibsiz.\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Foydalanuvchi oynasi", "Foydalanuvchilar", "Reklamalar"]))
        await Admin_state.main_menu.set()
    else:
        try:
            username = m.from_user.username
        except Exception as _:
            username = "No username"
        try:
            add_user(user_id=str(m.from_user.id), username=username)
        except Exception as _:
            pass
        await m.answer(f"{m.from_user.full_name} botga hush kelibsiz.\nKerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(users_main_menu()+["Foydalanish yo'riqnomasi"]))
        await User_state.main_menu.set()


dp.register_message_handler(cmd_start, content_types=[ct.TEXT])

"""
USERS APPS
"""

# main_menu

dp.register_message_handler(user.main_menu, content_types=[ct.TEXT], state=User_state.main_menu)

# second_menu

dp.register_message_handler(user.second_menu, content_types=[ct.TEXT], state=User_state.second_menu)


"""
ADMIN APPS
"""

# main_menu

dp.register_message_handler(admin.main_menu, content_types=[ct.TEXT], state=Admin_state.main_menu)

# second_menu

dp.register_message_handler(admin.second_menu, content_types=[ct.TEXT], state=Admin_state.second_menu)

# third_menu

dp.register_message_handler(admin.third_menu, content_types=[ct.TEXT], state=Admin_state.third_menu)

# fourth menu

dp.register_message_handler(admin.fourth_menu, content_types=[ct.TEXT], state=Admin_state.fourth_menu)

# add third menu

dp.register_message_handler(admin.add_new_media_type, content_types=[ct.TEXT], state=Admin_state.add_new_media_type)

# add second menu

dp.register_message_handler(admin.add_new_day, content_types=[ct.TEXT], state=Admin_state.add_new_day)

# add new media

dp.register_message_handler(admin.add_new_media, content_types={ct.TEXT, ct.AUDIO, ct.PHOTO, ct.VIDEO, ct.VOICE,
                                                                ct.DOCUMENT}, state=Admin_state.add_new_media)
