class BaseServerException(Exception):
    
    def __init__(self, message, details=None) -> None:
        super().__init__(message)
        self.message = message
        self.add_note(str(details))

    def to_dict(self) -> dict:
        return {
            "error": self.message,
            "detail": self.__notes__[0]
        }


class FileNotFound(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, details)


class DuplicatedRecord(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, details)


class NotFound(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, details)
