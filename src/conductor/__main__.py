#!/usr/bin/env python3

import sys
import argparse
from add_shortcut import add_shortcut


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(description="All in one steam game manager")
    subparsers = parser.add_subparsers(metavar="[command]", dest="command", help="Available commands")

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

    args = parser.parse_args()

    if args.command == 'add_shortcut':
        add_shortcut(
            app_name=args.name,
            exe_path=args.path,
            compat_tool=args.compat_tool,
            hero=args.hero,
            logo=args.logo,
            tenfoot=args.tenfoot,
            boxart=args.boxart,
            icon=args.icon,
            launch_options=args.launch_options
        )


if __name__ == '__main__':
    main()
