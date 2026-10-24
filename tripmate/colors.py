from colorama import Fore, init


init(
    autoreset=True
)


def success(
    message: str
):

    print(
        Fore.GREEN
        + message
    )


def warning(
    message: str
):

    print(
        Fore.YELLOW
        + message
    )


def error(
    message: str
):

    print(
        Fore.RED
        + message
    )


def info(
    message: str
):

    print(
        Fore.CYAN
        + message
    )


def ai(
    message: str
):

    print(
        Fore.BLUE
        + message
    )