from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    password: str
