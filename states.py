"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin_state(StatesGroup):
    main_menu = State()
    second_menu = State()


class User_state(StatesGroup):
    main_menu = State()
    second_menu = State()
