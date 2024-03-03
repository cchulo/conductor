#!/usr/bin/env python3

import sys
import argparse
import add_shortcut


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(description="All in one steam game manager")
    subparsers = parser.add_subparsers(metavar="[command]", dest="command", help="Available commands")

    add_shortcut.register_options(subparsers)

    args = parser.parse_args()

    if args.command == 'add_shortcut':
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


if __name__ == '__main__':
    main()
