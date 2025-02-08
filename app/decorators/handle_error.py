from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError, NoResultFound, MultipleResultsFound
from functools import wraps
from app.exceptions.exceptions import *


def handle_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except IntegrityError as e:
            self.session.rollback()
            raise DuplicatedRecordException(e.__repr__())

        except DBAPIError as e:
            raise ServerDBConnectionException(e.__repr__())

        except NoResultFound as e:
            raise NotFoundException(str(e))

        except MultipleResultsFound as e:
            raise MultipleResultsFound(e.__repr__())

        except SQLAlchemyError as e:
            self.session.rollback()
            raise ServerUnknownException(e.__repr__())

        except FileNotFoundError as e:
            raise FileNotFoundException(e.__repr__())

        except ValueError as e:
            raise DataValidationException(e.__repr__())

        except TypeError as e:
            raise TypeException(e.__repr__())

        except KeyError as e:
            raise KeyException(e.__repr__())

        except AttributeError as e:
            raise AttributeException(e.__repr__())

        except PermissionError as e:
            raise PermissionException(e.__repr__())

    return wrapper
