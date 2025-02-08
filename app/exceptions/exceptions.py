from app.exceptions.codes import *


class BaseExceptionError(Exception):
    def __init__(
        self,
        message: str,
        error_code: ErrorCodes,
        http_code: HTTPCodes,
        details: any
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = int(error_code.value)
        self.error_name = error_code.name
        self.http_code = int(http_code.value)
        self.http_name = http_code.name
        self.details = details

    def to_dict(self) -> dict:
        error_response = {
            "details": {
                "message": self.message,
                "HttpName": self.http_name,
                "ErrorName": self.error_name,
            },
            "codes": {
                "httpCode": self.http_code,
                "errorCode": self.error_code,
            }
        }
        if self.details:
            error_response["error"]["details"] = self.details
        return error_response


class FileNotFoundException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.FILE_NOT_FOUND, http_code=HTTPCodes.NOT_FOUND, details=details)


class DuplicatedRecordException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.DB_DUPLICATED_KEY, http_code=HTTPCodes.BAD_REQUEST, details=details)


class NotFoundException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.DB_NOT_FOUND, http_code=HTTPCodes.NOT_FOUND, details=details)


class InvalidTokenException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.INVALID_TOKEN, http_code=HTTPCodes.UNAUTHORIZED, details=details)


class PasswordMismatchException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.PASSWORD_DO_NOT_MATCH, http_code=HTTPCodes.FORBIDDEN, details=details)


class ExpiredTokenException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.EXPIRED_TOKEN, http_code=HTTPCodes.FORBIDDEN, details=details)


class IncorrectUserException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.INCORRECT_USER, http_code=HTTPCodes.UNAUTHORIZED, details=details)


class JsonFormatInvalidException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.JSON_FORMAT_INVALID, http_code=HTTPCodes.BAD_REQUEST, details=details)


class JsonNestedFormatInvalidException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.JSON_NESTED_FORMAT_INVALID, http_code=HTTPCodes.BAD_REQUEST, details=details)


class JsonInvalidDataTypeException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.JSON_INVALID_DATA_TYPE, http_code=HTTPCodes.BAD_REQUEST, details=details)


class JsonMissingParametersException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.JSON_MISSING_PARAMETERS, http_code=HTTPCodes.BAD_REQUEST, details=details)


class RouteNotFoundException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.ROUTE_NOT_FOUND, http_code=HTTPCodes.NOT_FOUND, details=details)


class RouteMethodNotAllowedException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.ROUTE_METHOD_NOT_ALLOWED, http_code=HTTPCodes.METHOD_NOT_ALLOWED, details=details)


class ServerNotWorkingException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SERVER_NOT_WORKING, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class ServerDBConnectionException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SERVER_DB_CONNECTION_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class ServerUnknownException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SERVER_UNKNOWN_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class DataValidationException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.ERROR_DATA_VALIDATION, http_code=HTTPCodes.BAD_REQUEST, details=details)


class SQLModelException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SQL_MODEL_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class IntegrityException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SQL_INTEGRITY_ERROR, http_code=HTTPCodes.BAD_REQUEST, details=details)


class DatabaseConnectionException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.DATABASE_CONNECTION_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class ForeignKeyConstraintViolationException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.FOREIGN_KEY_CONSTRAINT_VIOLATION, http_code=HTTPCodes.BAD_REQUEST, details=details)


class UniqueConstraintViolationException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.UNIQUE_CONSTRAINT_VIOLATION, http_code=HTTPCodes.BAD_REQUEST, details=details)


class SQLSyntaxException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.SQL_SYNTAX_ERROR, http_code=HTTPCodes.BAD_REQUEST, details=details)


class TimeoutException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.TIMEOUT_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class NotSupportedException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.NOT_SUPPORTED_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class TransactionException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.TRANSACTION_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class DataTypeMismatchException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.DATA_TYPE_MISMATCH, http_code=HTTPCodes.BAD_REQUEST, details=details)


class NoSuchColumnException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.NO_SUCH_COLUMN, http_code=HTTPCodes.BAD_REQUEST, details=details)


class NoSuchTableException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.NO_SUCH_TABLE, http_code=HTTPCodes.BAD_REQUEST, details=details)


class AuthenticationException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.AUTHENTICATION_ERROR, http_code=HTTPCodes.UNAUTHORIZED, details=details)


class PermissionException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.PERMISSION_ERROR, http_code=HTTPCodes.FORBIDDEN, details=details)


class FilePermissionException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.FILE_PERMISSION_ERROR, http_code=HTTPCodes.FORBIDDEN, details=details)


class AttributeException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.ATTRIBUTE_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class TypeException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.TYPE_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class ValueException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.VALUE_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class IndexException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.INDEX_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class KeyException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.KEY_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class ModuleNotFoundException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.MODULE_NOT_FOUND_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class MultipleResultsException(BaseExceptionError):
    def __init__(self, message="Se encontraron múltiples resultados inesperados", details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.MULTIPLE_RESULTS, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)


class GenericException(BaseExceptionError):
    def __init__(self, message="Ocurrió un error inesperado", details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.GENERIC_ERROR, http_code=HTTPCodes.INTERNAL_SERVER_ERROR, details=details)

class NotFoundTokenException(BaseExceptionError):
    def __init__(self, message, details=None) -> None:
        super().__init__(message, error_code=ErrorCodes.NOT_FOUND_TOKEN, http_code=HTTPCodes.UNAUTHORIZED, details=details)

