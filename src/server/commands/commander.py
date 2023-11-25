import json
import os

from passlib.hash import bcrypt

from src.config import SECRET_SEED
from src.services.computer import *
from src.services.users.subservices import UserManager


class ServerCommander:

    @classmethod
    async def ping(cls) -> str:
        return "pong"

    @classmethod
    async def help(cls) -> str:
        return " | ping ---> pong\n | help ---> commands list"

    @classmethod
    async def connection(cls):
        return "CONNECTION"

    @classmethod
    async def add_user_secret_token(cls, username: str, password: str):
        data = {}
        if os.path.exists("server_creds.json"):
            with open("server_creds.json", "r") as file_read:
                check_file = file_read.read()
                if check_file:
                    data = json.loads(check_file)
                    print(data)
                else:
                    data = {}

        with open("server_creds.json", "w") as f:
            print(data)
            token = password
            data[token] = {"ip": username,  # TODO CHANGE TO IP
                           "username": username}
            f.write(json.dumps(data))
        return token
