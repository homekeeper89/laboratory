from functools import wraps

# 파라메터 있는 데코레이터에도 @wraps 붙여주고
def decorator_http_response(status_code: int = 200):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            nonlocal status_code
            result = func(*args, **kwargs)

            if result.get("error", None):
                status_code = result["error"].HTTP_CODE
                result["error"] = result["error"].ERROR
            return result, status_code

        return decorator

    return wrapper
