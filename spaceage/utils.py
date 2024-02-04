import sys
from enum import Enum

from spaceage.config import SHOW_TOKEN_BREAKS

class Colors(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


def ct(text: str, color: Colors):
    return f"{color.value}{text}{Colors.RESET.value}"


# def print_color(text: str, color: Colors):
#     print(ct(text, color), end='', flush=True)


# def print_color(text: str, color: Colors, show_token_sep: bool = False):
def print_tokens_in_color(text: str, color: Colors, show_token_sep: bool = SHOW_TOKEN_BREAKS):
    sep = ''
    if show_token_sep:
        sep = ct('|', Colors.GREEN)
    print(ct(text, color), end=sep, flush=True)


def color_print(text: str, color: Colors):
    print(ct(text, color))
