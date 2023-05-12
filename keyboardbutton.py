"""
buttons reply
"""
from aiogram.types import ReplyKeyboardMarkup


def keyboardbutton(btns, resize_keyboard=True, row=1):
    """
    :param btns:
    :param resize_keyboard:
    :param row:
    :return:
    """
    btns = [btns[i:i + row] for i in range(0, len(btns), row)]
    btns = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=resize_keyboard, row_width=row)
    return btns
