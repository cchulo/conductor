#!/usr/bin/env python3

import sys
import argparse
from commands import info, add_shortcut
import importlib.metadata


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(description="All in one steam game manager")
    parser.add_argument('--version', action='store_true', help='Print the version of conductor')
    subparsers = parser.add_subparsers(metavar="[command]", dest="command", help="Available commands")

    info.register_options(subparsers)
    add_shortcut.register_options(subparsers)

    args = parser.parse_args()

    if args.version:
        print_version()

    match args.command:
        case 'info':
            info.command()
        case 'add_shortcut':
            add_shortcut.command(
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


def print_version():
    version = importlib.metadata.version('conductor')
    print(f'conductor-cli {version}')
    sys.exit(0)


if __name__ == '__main__':
    main()
