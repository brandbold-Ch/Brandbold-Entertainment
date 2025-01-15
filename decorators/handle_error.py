import os
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound, DBAPIError
from functools import wraps
from exceptions.exceptions import *


def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound as e:
            raise NotFound("No encontrado", e) from e

        except IntegrityError as e:
            # Error de integridad, como claves duplicadas
            return {"error": "Integrity error: Duplicate or conflicting entry", "details": str(e)}, 400
        except DBAPIError as e:
            # Errores generales de la base de datos
            return {"error": "Database API error: Problem interacting with the database", "details": str(e)}, 500
        except SQLAlchemyError as e:
            # Otros errores generales de SQLAlchemy/SQLModel
            return {"error": "General SQLAlchemy error", "details": str(e)}, 500
        except FileNotFoundError as e:
            # Error al intentar eliminar un archivo inexistente
            return {"error": "File not found: Unable to locate the specified file", "details": str(e)}, 404
        except PermissionError as e:
            # Error de permisos al trabajar con archivos
            return {"error": "Permission error: Insufficient permissions to perform the operation", "details": str(e)}, 403
        except ValueError as e:
            # Error de valor inválido, común en conversiones o validaciones
            return {"error": "Value error: Invalid input provided", "details": str(e)}, 400
        except KeyError as e:
            # Error al intentar acceder a una clave inexistente en un diccionario
            return {"error": "Key error: Missing or invalid key in input", "details": str(e)}, 400
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    return wrapper
