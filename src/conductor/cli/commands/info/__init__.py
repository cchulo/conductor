import os

from conductor.lib.constants import STEAM_USERDATA_PATH
from conductor.lib.steam_helper import find_steam_user_id
from conductor.lib.vdf_file import VdfFile


def register_options(subparsers) -> None:
    subparsers.add_parser('info', help='prints information about the current steam installation')


def command() -> int:
    user_id = find_steam_user_id()
    shortcuts_vdf_path = os.path.expanduser(os.path.join(STEAM_USERDATA_PATH, user_id, 'config', 'shortcuts.vdf'))
    shortcuts_vdf = VdfFile(shortcuts_vdf_path, binary=True, create_if_not_exists=True)
    print('Shortcuts added to steam:')
    print(shortcuts_vdf.pretty_print())
    return 0
