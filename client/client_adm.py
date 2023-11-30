import asyncio
import os
from asyncio import StreamReader, StreamWriter

from auth import register, get_token
from user_depends import UserActiveConnections

token = None


async def tcp_echo_client(reader: StreamReader, writer: StreamWriter):
    try:
        message = input("Your text: ")
        writer.write(message.encode())
        await writer.drain()
        data = await reader.read(256)

        if data.decode() == "test-ping":
            writer.write("SYSTEM INFORMATION ||||".encode())
        await writer.drain()
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


async def main():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)
    while True:
        try:
            await tcp_echo_client(reader, writer)
        except Exception as err:
            break


if __name__ == "__main__":
    asyncio.run(main())
