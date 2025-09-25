from fastapi import HTTPException


class ICustomHttpException(BaseException):
    def to_http_exception(self) -> HTTPException:
        raise NotImplemented("Subclasses must implement this method!")