import hashlib
import os
import vdf
import error_codes as err
import constants as const
from pathlib import Path


def add_shortcut(app_name: str, exe_path: str, compat_tool: str | None) -> int:
    expanded_exe_path = os.path.expanduser(exe_path)

    print(f'adding {expanded_exe_path} to steam...')

    if not os.path.isabs(expanded_exe_path):
        print(f'path {expanded_exe_path} is not a full path')
        return err.PATH_NOT_ABSOLUTE
    user_id = find_steam_user_id()

    if user_id is None:
        print('could not find steam user id')
        return err.FILE_DOES_NOT_EXIST
    print(f'found steam user id: {user_id}')

    app_id = modify_user_config_vdf(user_id, app_name, expanded_exe_path)
    set_compat_tool(app_id=app_id, compat_tool=compat_tool)

    pass


def modify_user_config_vdf(user_id: str, app_name: str, exe_path: str) -> str:
    shortcuts_vdf = os.path.expanduser(os.path.join(const.STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))

    if not os.path.exists(shortcuts_vdf):
        Path(shortcuts_vdf).touch()

    with open(shortcuts_vdf, 'rb') as f:
        data = vdf.binary_loads(f.read())

    signed_app_id = generate_shortcut_vdf_app_id(f'{app_name}{exe_path}')
    unsigned_app_id = str(int(signed_app_id)+2**32)

    print('summary of shortcut to add:')
    print(f'app id: {unsigned_app_id}')
    print(f'app name: {app_name}')
    print(f'exe path: {exe_path}')

    if 'shortcuts' not in data:
        data['shortcuts'] = {}
    if '0' not in data['shortcuts']:
        data['shortcuts']['0'] = {}
    data['shortcuts']['0'] = {
        'appid': signed_app_id,
        'AppName': app_name,
        'Exe': exe_path,
        'StartDir': f'"{os.path.dirname(exe_path)}"',  # wrapped in quotes since this is how steam does it
        'icon': '',
        'ShortcutPath': '',
        'LaunchOptions': '',
        'IsHidden': 0,
        'AllowDesktopConfig': 1,
        'AllowOverlay': 1,
        'OpenVR': 0,
        'Devkit': 0,
        'DevkitGameID': '',
        'DevKitOverrideAppID': '',
        'LastPlayTime': 0,
        'FlatpakAppId': '',
        'tags': {}
    }
    b = vdf.binary_dumps(data)
    with open(shortcuts_vdf, 'wb') as f:
        f.write(b)

    # convert to unsigned int since that's what users expect
    return unsigned_app_id


def set_compat_tool(app_id: str, compat_tool: str | None) -> None:
    if compat_tool is None:
        return
    compat_tool_path = os.path.expanduser(os.path.join(const.STEAM_COMPAT_TOOLS_PATH, compat_tool))
    if not os.path.exists(compat_tool_path):
        print(f'compat tool {compat_tool} does not exist')
        return
    print(f'setting compat tool to {compat_tool}')

    with open(const.STEAM_CONFIG_VDF_PATH, 'r') as f:
        config_data = vdf.loads(f.read(), mapper=vdf.VDFDict)
        data = config_data['InstallConfigStore']['Software']['Valve']['Steam']

    if 'CompatToolMapping' not in data:
        data['CompatToolMapping'] = {}

    if app_id in data['CompatToolMapping']:
        data['CompatToolMapping'].remove_all_for(app_id)

    data['CompatToolMapping'][app_id] = {
        'name': compat_tool
    }
    with open(const.STEAM_CONFIG_VDF_PATH, 'w+') as f:
        vdf.dump(config_data, f, pretty=True)


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
    seed = hashlib.md5(seed_str.encode()).hexdigest()[:8]
    return f'-{int(seed, 16) % 1000000000}'
