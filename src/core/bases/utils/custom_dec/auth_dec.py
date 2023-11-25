import json


def check_user_auth(func):
    async def _wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        print(func)
        msg = kwargs.get("msg").split("-t")
        message = msg[0].replace(" ", "")
        token = msg[1].replace(" ", "")
        with open("server_creds.json", "r") as f:
            fr = f.read()
            if fr:
                data = json.loads(fr)
                data.get(token)
                if data:
                    c = await func(message)
                    print(c)
                    return c
            else:
                raise Exception("NOT TOKEN")
    return _wrapper()


def splited_message_with_token(func):
    async def _wrapper(*args, **kwargs):
        ...

