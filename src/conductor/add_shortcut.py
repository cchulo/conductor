import hashlib
import os
import error_codes as err
import constants as const
import shutil
from vdf_file import VdfFile
from steam_helper import find_steam_user_id


def register_options(subparsers) -> None:
    add_shortcut_command = subparsers.add_parser('add_shortcut', help='adds an executable shortcut to steam')
    add_shortcut_command.add_argument(
        '--name',
        dest='name',
        metavar='<name>',
        required=True,
        help='The name of the shortcut')
    add_shortcut_command.add_argument(
        '--path',
        dest='path',
        metavar='<path/to/executable>',
        required=True,
        help='The full path to the executable')
    add_shortcut_command.add_argument(
        '--compat-tool',
        dest='compat_tool',
        metavar='<compat_tool>',
        required=False,
        help='The name of the compatability tool to use')
    add_shortcut_command.add_argument(
        '--hero',
        dest='hero',
        metavar='<path/to/hero/image>',
        required=False,
        help='The path to the hero image'
    )
    add_shortcut_command.add_argument(
        '--logo',
        dest='logo',
        metavar='<path/to/logo/image>',
        required=False,
        help='The path to the logo image'
    )
    add_shortcut_command.add_argument(
        '--tenfoot',
        dest='tenfoot',
        metavar='<path/to/tenfoot/image>',
        required=False,
        help='The path to the tenfoot image'
    )
    add_shortcut_command.add_argument(
        '--boxart',
        dest='boxart',
        metavar='<path/to/boxart/image>',
        required=False,
        help='The path to the boxart image'
    )
    add_shortcut_command.add_argument(
        '--icon',
        dest='icon',
        metavar='<path/to/icon/image>',
        required=False,
        help='The path to the icon image'
    )
    add_shortcut_command.add_argument(
        '--launch-options',
        dest='launch_options',
        metavar='<launch options>',
        required=False,
        help='The launch options for the shortcut'
    )


def command(
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
    shortcuts_vdf_path = os.path.expanduser(os.path.join(const.STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))

    shortcuts_vdf = VdfFile(shortcuts_vdf_path, binary=True, create_if_not_exists=True)

    signed_app_id = generate_shortcut_vdf_app_id(f'{app_name}{expanded_exe_path}')
    unsigned_app_id = str(int(signed_app_id)+2**32)

    print('summary of shortcut to add:')
    print(f'app id: {unsigned_app_id}')
    print(f'app name: {app_name}')
    print(f'exe path: {expanded_exe_path}')

    if 'shortcuts' not in shortcuts_vdf.data:
        shortcuts_vdf.data['shortcuts'] = {}
    if '0' not in shortcuts_vdf.data['shortcuts']:
        shortcuts_vdf.data['shortcuts']['0'] = {}
    shortcuts_vdf.data['shortcuts']['0'] = {
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
    shortcuts_vdf.save()

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

    config_vdf = VdfFile(const.STEAM_CONFIG_VDF_PATH)

    if 'CompatToolMapping' not in config_vdf.data:
        config_vdf.data['CompatToolMapping'] = {}

    if app_id in config_vdf.data['CompatToolMapping']:
        config_vdf.data['CompatToolMapping'].remove_all_for(app_id)

    config_vdf.data['CompatToolMapping'][app_id] = {
        'name': compat_tool
    }
    config_vdf.save()


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
