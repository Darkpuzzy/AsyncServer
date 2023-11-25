import asyncio
import os

from auth import register, get_token
from user_depends import UserActiveConnections

token = None


async def tcp_echo_client(message):
    try:
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        msg_tok = await UserActiveConnections(token, message).msg()
        writer.write(msg_tok.encode())
        await writer.drain()

        data = await reader.read(256)
        # print(f'Received: {data.decode()!r}')
        print(data.decode())
        if message == ".quit":
            print('Close the connection')
            writer.close()
            await writer.wait_closed()
    except Exception as err:
        print(err)
        print('Close the connection')
        writer.close()
        await writer.wait_closed()


def main():
    while True:
        try:
            msg = input()
            if msg == ".quit":
                break
            asyncio.run(tcp_echo_client(msg))
        except Exception as err:
            break


if __name__ == "__main__":
    if os.path.exists("creds.json"):
        token = get_token()
    else:
        print("Not registerd on server")
        username = input("Username ")
        password = input("Password ")
        data = {"username": username,
                "password": password}
        asyncio.run(register(user_data=data))

    main()
