

class BaseError(Exception):

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def what(self) -> str:
        return self.msg
