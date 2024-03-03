import hashlib
import os
import shutil
import conductor.cli.commands.add_shortcut.error_codes as err
from collections import namedtuple
from conductor.cli.console_colors import *
from conductor.lib.vdf_file import VdfFile
from conductor.lib.steam_helper import find_steam_user_id
from conductor.lib.constants import STEAM_USERDATA_PATH, \
    STEAM_COMPAT_TOOLS_PATH, \
    STEAM_CONFIG_VDF_PATH

__tuple__ = namedtuple('tuple', 'app_id, error_code')


def register_options(subparsers) -> None:
    add_shortcut_command = subparsers.add_parser('add_shortcut', help='adds an executable shortcut to steam')
    add_shortcut_command.add_argument(
        '--app-name',
        dest='app_name',
        metavar='<name>',
        required=True,
        help='(Required) The name of the shortcut')
    add_shortcut_command.add_argument(
        '--exe-path',
        dest='exe_path',
        metavar='<path/to/executable>',
        required=True,
        help='(Required) The full path to the executable')
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
    add_shortcut_command.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        required=False,
        help='Performs a dry run'
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
        dry_run: bool = False
        ) -> int:
    if dry_run:
        print_yellow('dry run, not actually modifying steam')

    expanded_exe_path = os.path.expanduser(exe_path)

    print_green(f'adding {expanded_exe_path} to steam...')

    if not os.path.isabs(expanded_exe_path):
        print_red(f'path {expanded_exe_path} is not a full path')
        return err.ERROR_PATH_NOT_ABSOLUTE
    user_id = find_steam_user_id()

    if user_id is None:
        print_red('could not find steam user id')
        return err.ERROR_STEAM_USER_NOT_FOUND
    print(f'found steam user id: {user_id}')

    [app_id, error_code] = modify_user_config_vdf(
        user_id=user_id,
        app_name=app_name,
        expanded_exe_path=expanded_exe_path,
        icon=icon,
        launch_options=launch_options,
        dry_run=dry_run
    )

    if error_code != 0:
        return error_code

    result = set_compat_tool(app_id=app_id, compat_tool=compat_tool, dry_run=dry_run)
    if result != 0:
        return result

    result = set_art_work(
        user_id=user_id,
        app_id=app_id,
        hero=hero,
        logo=logo,
        tenfoot=tenfoot,
        boxart=boxart,
        dry_run=dry_run)
    if result != 0:
        return result

    return 0


def modify_user_config_vdf(
        user_id: str,
        app_name: str,
        expanded_exe_path: str,
        icon: str | None,
        launch_options: str | None,
        dry_run: bool = False
        ) -> __tuple__:
    shortcuts_vdf_path = os.path.expanduser(os.path.join(STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))

    shortcuts_vdf = VdfFile(shortcuts_vdf_path, binary=True, create_if_not_exists=True)

    signed_app_id = generate_shortcut_vdf_app_id(f'{app_name}{expanded_exe_path}')
    unsigned_app_id = str(int(signed_app_id) + 2**32)

    print_cyan('summary of shortcut to add:')
    print(f'app id: {unsigned_app_id}')
    print(f'app name: {app_name}')
    print(f'exe path: {expanded_exe_path}')
    print(f'icon: {icon}')
    print(f'launch options: {launch_options}')

    if 'shortcuts' not in shortcuts_vdf.data:
        shortcuts_vdf.data['shortcuts'] = {}

    i = 0
    app_ids_found = []
    while True:
        index = str(i)
        if index not in shortcuts_vdf.data['shortcuts']:
            shortcuts_vdf.data['shortcuts'][index] = {}
            break
        if 'appid' in shortcuts_vdf.data['shortcuts'][index]:
            app_ids_found.append(str(shortcuts_vdf.data['shortcuts'][index]['appid']))
        if 'AppId' in shortcuts_vdf.data['shortcuts'][index]:
            app_ids_found.append(str(shortcuts_vdf.data['shortcuts'][index]['AppId']))
        i += 1

    if signed_app_id in app_ids_found:
        print_red(f'app id {signed_app_id} already exists, skipping...')
        return __tuple__(app_id=None, error_code=err.ERROR_APP_ID_ALREADY_EXISTS)

    if index not in shortcuts_vdf.data['shortcuts']:
        shortcuts_vdf.data['shortcuts'][index] = {}

    print_blue('original shortcuts_vdf: ' + str(shortcuts_vdf.data))

    shortcuts_vdf.data['shortcuts'][index] = {
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

    print_cyan('modified shortcuts_vdf.data ' + str(shortcuts_vdf.data))

    if not dry_run:
        shortcuts_vdf.save()
    else:
        print_yellow('dry run, not modifying shortcuts.vdf')

    # convert to unsigned int since that's what users expect
    return __tuple__(app_id=unsigned_app_id, error_code=0)


def set_compat_tool(app_id: str, compat_tool: str | None, dry_run: bool = False) -> int:
    if compat_tool is None:
        print_yellow('no compat tool specified, skipping...')
        return 0

    compat_tool_path = os.path.expanduser(os.path.join(STEAM_COMPAT_TOOLS_PATH, compat_tool))

    if not os.path.exists(compat_tool_path):
        print_red(f'compat tool {compat_tool} does not exist')
        return err.ERROR_COMPAT_TOOL_DOES_NOT_EXIST

    print_cyan(f'setting compat tool to {compat_tool}')
    config_vdf = VdfFile(STEAM_CONFIG_VDF_PATH)

    if 'CompatToolMapping' not in config_vdf.data:
        config_vdf.data['CompatToolMapping'] = {}

    if app_id in config_vdf.data['CompatToolMapping']:
        config_vdf.data['CompatToolMapping'].remove_all_for(app_id)

    config_vdf.data['CompatToolMapping'][app_id] = {
        'name': compat_tool
    }

    if not dry_run:
        config_vdf.save()
    else:
        print_yellow('dry run, not modifying config.vdf')

    return 0


def set_art_work(
        user_id: str,
        app_id: str,
        hero: str | None,
        logo: str | None,
        tenfoot: str | None,
        boxart: str | None,
        dry_run: bool = False,
        ) -> int:
    grid_dir = os.path.expanduser(os.path.join(STEAM_USERDATA_PATH, user_id, 'config', 'grid'))
    os.makedirs(grid_dir, exist_ok=True)
    success = True
    if hero is not None and not os.path.exists(hero):
        print_red(f'hero image {hero} does not exist')
        success = False
    if logo is not None and not os.path.exists(logo):
        print_red(f'logo image {logo} does not exist')
        success = False
    if tenfoot is not None and not os.path.exists(tenfoot):
        print_red(f'tenfoot image {tenfoot} does not exist')
        success = False
    if boxart is not None and not os.path.exists(boxart):
        print_red(f'boxart image {boxart} does not exist')
        success = False
    if not success:
        return err.ERROR_ART_NOT_PROPERLY_SET

    copy_artwork('hero', grid_dir, hero, f'{app_id}_hero', dry_run=dry_run)
    copy_artwork('logo', grid_dir, logo, f'{app_id}_logo', dry_run=dry_run)
    copy_artwork('tenfoot', grid_dir, tenfoot, f'{app_id}', dry_run=dry_run)
    copy_artwork('boxart', grid_dir, boxart, f'{app_id}p', dry_run=dry_run)

    return 0


def copy_artwork(label: str, grid_dir: str, src: str | None, dest_name: str, dry_run: bool = False) -> None:
    if src is None:
        print_yellow(f'no image specified for {label}, skipping...')
        return
    extension = os.path.splitext(src)[1]
    dest = os.path.join(grid_dir, f'{dest_name}{extension}')
    print(f'copying {src} to {dest}')
    if not dry_run:
        shutil.copy(src, dest)
    else:
        print_yellow(f'dry run, not actually copying to {dest}')


def generate_shortcut_vdf_app_id(seed_str) -> str:
    seed = hashlib.md5(seed_str.encode()).hexdigest()[:8]
    return f'-{int(seed, 16) % 1000000000}'
