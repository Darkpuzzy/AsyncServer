

class UserActiveConnections:

    def __init__(self, token: str, message: str):
        self.token = token
        self.message = message

    async def msg(self) -> str:
        return self.message + " -t " + self.token
