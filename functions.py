"""
all personal functions in here
"""
# imports
from config import ADMIN_ID


def is_admin(_id):
    return ADMIN_ID == _id


def users_main_menu():
    return ['14-may', '8-aprel']


def users_second_menu(first_menu):
    return ['Musiqa', 'Rasm', 'kino']
