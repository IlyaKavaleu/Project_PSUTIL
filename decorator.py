import json


def to_json(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w') as json_file:
                json.dump(result, json_file)
            return result
        return wrapper
    return decorator
