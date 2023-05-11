"""
log in
"""
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from functions import is_admin
from states import *


async def cmd_start(m: m):
    """
    :param m:
    :return:
    """
    if is_admin(m.chat.id):
        pass