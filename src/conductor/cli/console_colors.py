# ANSI escape codes for some colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Resets the color to default


# function that prints a message in red
def print_red(message: str) -> None:
    print(f'{RED}{message}{RESET}')


# function that prints a message in green
def print_green(message: str) -> None:
    print(f'{GREEN}{message}{RESET}')


# function that prints a message in yellow
def print_yellow(message: str) -> None:
    print(f'{YELLOW}{message}{RESET}')


# function that prints a message in blue
def print_blue(message: str) -> None:
    print(f'{BLUE}{message}{RESET}')


# function that prints a message in magenta
def print_magenta(message: str) -> None:
    print(f'{MAGENTA}{message}{RESET}')


# function that prints a message in cyan
def print_cyan(message: str) -> None:
    print(f'{CYAN}{message}{RESET}')
