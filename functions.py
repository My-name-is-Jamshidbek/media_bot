"""
all personal functions in here
"""
# imports
from config import ADMIN_ID
from database.database import read_days, read_media_types, read_media, delete_media, delete_media_type


def is_admin(_id):
    """
    :param _id:
    :return:
    """
    return ADMIN_ID == _id


def users_main_menu():
    """
    :return:
    """
    return [i[1] for i in read_days()]


def users_second_menu(first_menu):
    """
    :param first_menu:
    :return:
    """
    _id = -1
    for i in read_days():
        if i[1] == first_menu:
            _id = i[0]
            break
    if _id == -1:
        return []
    else:
        return [i[1] for i in read_media_types(_id)]


def read_all_media(media_type, day):
    """
    :param media_type:
    :param day:
    :return:
    """
    return [i[2] for i in read_media(media_type=media_type, day=day)]


def delete_all_media(media_type, day):
    """
    :param media_type:
    :param day:
    :return:
    """
    medias_ = read_all_media(media_type=media_type, day=day)
    delete_media_type(media_type=media_type, day=day)
    for media_name in medias_:
        delete_media(media_name=media_name)
