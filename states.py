"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin_state(StatesGroup):
    """
    admin all states
    """
    main_menu = State()
    second_menu = State()
    third_menu = State()
    fourth_menu = State()

    add_new_day = State()
    add_new_media_type = State()
    add_new_media = State()


class User_state(StatesGroup):
    """
    user all states
    """
    main_menu = State()
    second_menu = State()
