class BaseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"


class DataBaseOperationError(BaseError):
    """Error Exceptions: DataBase"""

    def __str__(self):
        return f"DB ERROR: {self.message}"