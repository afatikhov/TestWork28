class NoDataInsertedException(BaseException):
    def __init__(self, message: str = "No data was inserted!"):
        super().__init__(message)