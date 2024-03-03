#!/usr/bin/env bash

set -euo pipefail

pip3 install -e .
pyinstaller --onefile --clean --name conductor-cli src/conductor/cli/__main__.py --dist bin
