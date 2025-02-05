from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError
from functools import wraps

from sqlmodel import Session

from app.exceptions.exceptions import *


def handle_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except IntegrityError as e:
            self.session.rollback()
            raise DuplicatedRecord(e.__repr__())

        except DBAPIError as e:
            raise ServerDBConnectionError(e.__repr__())

        except SQLAlchemyError as e:
            self.session.rollback()
            raise ServerUnknownError(e.__repr__())

        except FileNotFoundError as e:
            raise FileNotFound(e.__repr__())

        except ValueError as e:
            raise DataValidationError(e.__repr__())
    return wrapper
