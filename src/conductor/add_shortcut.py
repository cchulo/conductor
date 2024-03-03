import hashlib
import os
import vdf
import error_codes as err
import constants as const
import shutil
from pathlib import Path


def add_shortcut(
        app_name: str,
        exe_path: str,
        compat_tool: str | None,
        hero: str | None,
        logo: str | None,
        tenfoot: str | None,
        boxart: str | None,
        icon: str | None,
        launch_options: str | None,
        ) -> int:
    expanded_exe_path = os.path.expanduser(exe_path)

    print(f'adding {expanded_exe_path} to steam...')

    if not os.path.isabs(expanded_exe_path):
        print(f'path {expanded_exe_path} is not a full path')
        return err.PATH_NOT_ABSOLUTE
    user_id = find_steam_user_id()

    if user_id is None:
        print('could not find steam user id')
        return err.STEAM_USER_NOT_FOUND
    print(f'found steam user id: {user_id}')

    app_id = modify_user_config_vdf(
        user_id=user_id,
        app_name=app_name,
        expanded_exe_path=expanded_exe_path,
        icon=icon,
        launch_options=launch_options)
    set_compat_tool(app_id=app_id, compat_tool=compat_tool)
    set_art_work(user_id=user_id, app_id=app_id, hero=hero, logo=logo, tenfoot=tenfoot, boxart=boxart)

    pass


def modify_user_config_vdf(
        user_id: str,
        app_name: str,
        expanded_exe_path: str,
        icon: str | None,
        launch_options: str | None) -> str:
    shortcuts_vdf = os.path.expanduser(os.path.join(const.STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))

    if not os.path.exists(shortcuts_vdf):
        Path(shortcuts_vdf).touch()

    with open(shortcuts_vdf, 'rb') as f:
        data = vdf.binary_loads(f.read())

    signed_app_id = generate_shortcut_vdf_app_id(f'{app_name}{expanded_exe_path}')
    unsigned_app_id = str(int(signed_app_id)+2**32)

    print('summary of shortcut to add:')
    print(f'app id: {unsigned_app_id}')
    print(f'app name: {app_name}')
    print(f'exe path: {expanded_exe_path}')

    if 'shortcuts' not in data:
        data['shortcuts'] = {}
    if '0' not in data['shortcuts']:
        data['shortcuts']['0'] = {}
    data['shortcuts']['0'] = {
        'appid': signed_app_id,
        'AppName': app_name,
        'Exe': expanded_exe_path,
        'StartDir': f'"{os.path.dirname(expanded_exe_path)}"',  # wrapped in quotes since this is how steam does it
        'icon': '' if icon is None else icon,
        'ShortcutPath': '',
        'LaunchOptions': launch_options if launch_options is not None else '',
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


def set_art_work(
        user_id: str,
        app_id: str,
        hero: str | None,
        logo: str | None,
        tenfoot: str | None,
        boxart: str | None) -> bool:
    grid_dir = os.path.expanduser(os.path.join(const.STEAM_USERDATA_PATH, user_id, 'config', 'grid'))
    os.makedirs(grid_dir, exist_ok=True)
    success = True
    if hero is not None and not os.path.exists(hero):
        print(f'hero image {hero} does not exist')
        success = False
    if logo is not None and not os.path.exists(logo):
        print(f'logo image {logo} does not exist')
        success = False
    if tenfoot is not None and not os.path.exists(tenfoot):
        print(f'tenfoot image {tenfoot} does not exist')
        success = False
    if boxart is not None and not os.path.exists(boxart):
        print(f'boxart image {boxart} does not exist')
        success = False
    if not success:
        return False

    copy_artwork(app_id, grid_dir, hero, f'{app_id}_hero')
    copy_artwork(app_id, grid_dir, logo, f'{app_id}_logo')
    copy_artwork(app_id, grid_dir, tenfoot, f'{app_id}')
    copy_artwork(app_id, grid_dir, boxart, f'{app_id}p')

    return True


def copy_artwork(app_id: str, grid_dir: str, src: str | None, dest_name: str) -> None:
    if src is None:
        return
    extension = os.path.splitext(src)[1]
    dest = os.path.join(grid_dir, f'{dest_name}{extension}')
    shutil.copy(src, dest)


def generate_shortcut_vdf_app_id(seed_str) -> str:
    seed = hashlib.md5(seed_str.encode()).hexdigest()[:8]
    return f'-{int(seed, 16) % 1000000000}'
