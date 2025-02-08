from functools import wraps
from app.decorators.handle_error import handle_error
from app.exceptions.exceptions import NotFoundException


@handle_error
def injectable_entity(model, only_parse=False, index=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not only_parse:
                entity_id = args[0]
                data = self.session.get(model, entity_id)

                if not data:
                    raise NotFoundException(f"{model.__name__} not found with ID {entity_id}")

                kwargs[model.__name__.lower()] = data
                return func(self, *args, **kwargs)

            else:
                if index is not None and 0 <= index < len(args):
                    new_args = list(args)
                    new_args[index] = model.model_validate(args[index]).model_dump()
                    return func(self, *new_args, **kwargs)

        return wrapper
    return decorator
