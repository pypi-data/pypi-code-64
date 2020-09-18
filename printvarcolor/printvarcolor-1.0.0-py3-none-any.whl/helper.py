from termcolor import colored


def make_colorful_text(text: str, color: str = 'white') -> str:
    return colored(text, color)


def cprint(**kwargs) -> None:
    for k, v in kwargs.items():
        key = make_colorful_text(k, 'red')
        value = make_colorful_text(v, 'green')
        print(f"{key}: {value}")
