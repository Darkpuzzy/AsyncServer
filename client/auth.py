import asyncio
import json


async def register(user_data: dict):
    try:
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        json_data = json.dumps(user_data)
        msg = "register -u " + json_data
        writer.write(msg.encode())
        await writer.drain()

        data = await reader.read(256)
        # print(f'Received: {data.decode()!r}')
        response = data.decode()
        await add_token(token=response)
        writer.close()
        await writer.wait_closed()
    except Exception as err:
        print(err)


def get_token():
    with open("creds.json", "r") as f:
        data = json.load(f)
        return data["token"]


async def add_token(token: str):
    with open("creds.json", "w") as f:
        data = {"token": token}
        f.write(json.dumps(data))
