import os
from conductor.lib.constants import STEAM_USERDATA_PATH


def find_steam_user_id() -> str | None:
    # steam user id is the name of the directory in the steamapps directory
    # this is the default location for steam library
    userdata_path = os.path.expanduser(STEAM_USERDATA_PATH)
    if not os.path.exists(userdata_path):
        print(f'userdata directory does not exist at {userdata_path}')
        return ''
    steam_user_id = os.listdir(userdata_path)
    if len(steam_user_id) == 0:
        print(f'userdata directory {userdata_path} does not contain any accounts')
        return None
    return steam_user_id[0]
