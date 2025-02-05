from app.exceptions.codes import *


class BaseServerException(Exception):
    def __init__(
            self,
            message: str,
            code: int = HTTPCodes.INTERNAL_SERVER_ERROR.value,
            error_type: str = HTTPCodes.INTERNAL_SERVER_ERROR.name,
            details: any = None
            ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.error_type = error_type
        self.details = details

    def to_dict(self) -> dict:
        error_response = {
            "status": "error",
            "error": {
                "type": self.error_type,
                "message": self.message,
                "code": self.code,
            }
        }
        if self.details:
            error_response["error"]["details"] = self.details
        return error_response


class FileNotFound(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.FILE_NOT_FOUND.value, error_type=HTTPCodes.NOT_FOUND.name, details=details)


class DuplicatedRecord(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.DB_DUPLICATED_KEY.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)


class NotFound(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.DB_NOT_FOUND.value, error_type=HTTPCodes.NOT_FOUND.name, details=details)


class InvalidToken(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.INVALID_TOKEN.value, error_type=HTTPCodes.UNAUTHORIZED.name, details=details)


class PasswordMismatch(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.PASSWORD_DO_NOT_MATCH.value, error_type=HTTPCodes.FORBIDDEN.name, details=details)


class ExpiredToken(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.EXPIRED_TOKEN.value, error_type=HTTPCodes.FORBIDDEN.name, details=details)


class IncorrectUser(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.INCORRECT_USER.value, error_type=HTTPCodes.UNAUTHORIZED.name, details=details)


class JsonFormatInvalid(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.JSON_FORMAT_INVALID.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)


class JsonNestedFormatInvalid(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.JSON_NESTED_FORMAT_INVALID.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)


class JsonInvalidDataType(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.JSON_INVALID_DATA_TYPE.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)


class JsonMissingParameters(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.JSON_MISSING_PARAMETERS.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)


class RouteNotFound(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.ROUTE_NOT_FOUND.value, error_type=HTTPCodes.NOT_FOUND.name, details=details)


class RouteMethodNotAllowed(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.ROUTE_METHOD_NOT_ALLOWED.value, error_type=HTTPCodes.METHOD_NOT_ALLOWED.name, details=details)


class ServerNotWorking(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.SERVER_NOT_WORKING.value, error_type=HTTPCodes.INTERNAL_SERVER_ERROR.name, details=details)


class ServerDBConnectionError(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.SERVER_DB_CONNECTION_ERROR.value, error_type=HTTPCodes.INTERNAL_SERVER_ERROR.name, details=details)


class ServerUnknownError(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.SERVER_UNKNOWN_ERROR.value, error_type=HTTPCodes.INTERNAL_SERVER_ERROR.name, details=details)


class DataValidationError(BaseServerException):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, code=ErrorCodes.ERROR_DATA_VALIDATION.value, error_type=HTTPCodes.BAD_REQUEST.name, details=details)
