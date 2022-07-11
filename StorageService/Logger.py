import os

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def success(logger: str, msg) -> None:
    pid_id = os.getpid()
    print(f"{OKGREEN}-- [{pid_id}][success][{logger}] --> {msg}{ENDC}")


def error(logger: str, msg) -> None:
    pid_id = os.getpid()
    print(f"{FAIL}-- [{pid_id}][error][{logger}] --> {msg}{ENDC}")


def warning(logger: str, msg) -> None:
    pid_id = os.getpid()
    print(f"{WARNING}-- [{pid_id}][waring][{logger}] --> {msg}{ENDC}")


def info(logger: str, msg) -> None:
    pid_id = os.getpid()
    print(f"-- [{pid_id}][info][{logger}] --> {msg}")
