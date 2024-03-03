# Conductor

## Description

All in one solution for managing all games within steam.

## Goals of this project

- Enabling batch (un)installation of games with tools such as ansible or plain shell scripts
- Create a tool for managing mods for all steam games
  - This includes downloading, installing, updating and removing mods
  - Letting the user define virtual file systems for mods, much like [Mod Organizer 2](https://www.nexusmods.com/skyrimspecialedition/mods/6194)
  but for linux
- Letting the user define game profiles that specify launch options, environment variables, etc. for official steam games
in an effort to make linux gaming even more accessible

## Development

### Requirements
- [Python 3.10+](https://www.python.org/downloads/)
- [PyCharm (optional, recommended)](https://www.jetbrains.com/pycharm/download/)

### Getting started

Recommended to use virtual environments to avoid conflicts with system packages.

```bash
cd /path/to/conductor/project/root
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
src/conductor/__main__.py --help
```

## How to build conductor-cli

Currently, the project uses pyinstaller to build the binary. This is subject to change.

```bash
cd /path/to/conductor/project/root
./scripts/build.sh
./bin/conductor-cli --help
```

To clean up all build artifacts, run:

```bash
./scripts/clean.sh
```

## Usage
    
```bash
conductor-cli --help

```