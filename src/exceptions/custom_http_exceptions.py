from functools import wraps

from fastapi import HTTPException


class ICustomHttpException(BaseException):
    def to_http_exception(self) -> HTTPException:
        raise NotImplemented("Subclasses must implement this method!")

class QuoteDataNotFound(BaseException):
    def __init__(self, message: str):
        super().__init__(message)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=404, detail=f"Quote not found: {self.message}")

def http_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ICustomHttpException as e:
            raise e.to_http_exception()
    return wrapper