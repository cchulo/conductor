import hashlib
import os
import random
import vdf
import error_codes as err
import constants as const
from pathlib import Path


def add_shortcut(path: str) -> int:
    print(f'adding {path} to steam...')
    expanded_path = os.path.expanduser(path)
    if not os.path.isabs(expanded_path):
        print(f'path {path} is not a full path')
        return err.PATH_NOT_ABSOLUTE
    user_id = find_steam_user_id()
    if user_id is None:
        print('could not find steam user id')
        return err.FILE_DOES_NOT_EXIST
    print(f'found steam user id: {user_id}')
    shortcuts_vdf = os.path.expanduser(os.path.join(const.STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))
    with open(shortcuts_vdf, 'rb+') as f:
        data = vdf.binary_loads(f.read(), mapper=vdf.VDFDict)
        app_id_to_add = generate_shortcut_vdf_app_id(path)
        print(f'adding {app_id_to_add} to shortcuts.vdf')
        print(data)
        # data['shortcuts'][app_id_to_add] = {
        #     'AppName': os.path.basename(expanded_path),
        #     'Exe': expanded_path,
        #     'StartDir': os.path.dirname(expanded_path),
        # }
    pass


def find_steam_user_id() -> str | None:
    # steam user id is the name of the directory in the steamapps directory
    # this is the default location for steam library
    userdata_path = os.path.expanduser(const.STEAM_USERDATA_PATH)
    if not os.path.exists(userdata_path):
        print(f'userdata directory does not exist at {userdata_path}')
        return ''
    steam_user_id = os.listdir(userdata_path)
    if len(steam_user_id) == 0:
        print(f'userdata directory {userdata_path} does not contain any accounts')
        return None
    return steam_user_id[0]


def generate_shortcut_vdf_app_id(seed_str) -> str:
    # Seed the random number generator with the MD5 hash of the input string
    random.seed(hashlib.md5(seed_str.encode()).hexdigest()[:8])

    # Generate a random number within the new range
    # Adjusted range to fit between 999,999,999 and 4,294,967,295
    random_number = random.randint(999999999, 2**32 - 1)
    return str(random_number)
