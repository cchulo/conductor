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
        metavar='<path>',
        required=True,
        help='The full path to the executable')
    add_shortcut_command.add_argument(
        '--compat-tool',
        dest='compat_tool',
        metavar='<compat_tool>',
        required=False,
        help='The name of the compatability tool to use')

    args = parser.parse_args()

    if args.command == 'add_shortcut':
        add_shortcut(
            app_name=args.name,
            exe_path=args.path,
            compat_tool=args.compat_tool
        )


if __name__ == '__main__':
    main()
