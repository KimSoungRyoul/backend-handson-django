from functools import wraps


def router(path, http_method):
    def decorator_func(func):
        @wraps(func)
        def wrapper_function(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper_function

    return decorator_func
