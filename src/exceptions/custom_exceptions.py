class NoDataInsertedException(BaseException):
    def __init__(self, message: str = "No data was inserted!"):
        super().__init__(message)

class PageLoadException(BaseException):
    def __init__(self, url: str):
        message: str = f"Error in loading page: {url}"
        super().__init__(message)