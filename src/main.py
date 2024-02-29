#!/usr/bin/env python3

import argparse
from add_shortcut import add_shortcut

def main():
    parser = argparse.ArgumentParser(description="All in one steam game manager")
    subparsers = parser.add_subparsers(metavar="[command]", dest="command", help="Available commands")

    add_shortcut_command = subparsers.add_parser('info', help='prints information regarding conductor')

    add_shortcut_command = subparsers.add_parser('add_shortcut', help='adds an executable shortcut to steam')
    add_shortcut_command.add_argument(
        '--path',
        dest='path',
        metavar='<path>',
        help='[required] the full path to the executable')

    args = parser.parse_args()

    if args.command == 'info':
        print('under construction')
    elif args.command == 'add_shortcut':
        add_shortcut(args.path)


if __name__ == '__main__':
    main()
