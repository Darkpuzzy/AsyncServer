import asyncio
from typing import Tuple

from src.config import SERVER_PASS
from src.server.commands import commander, loggin, register

admin_connections = []

active_connections = []


async def forward(writer, addr, message):
    for w in active_connections:
        if w != writer:
            w.write(f"{addr!r}: {message!r}\n".encode())


async def broadcast_check():
    for w in active_connections:
        w.write(f"test-ping".encode())


async def hub_vm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    while True:
        addr = writer.get_extra_info('peername')
        data = await reader.read(256)
        msg = data.decode()
        print(msg)
        answer = await commander(msg)
        writer.write(answer.encode())
        await writer.drain()
        if msg == "exit":
            message = f"{addr!r} wants to close the connection."
            print(message)
            await forward(writer, "Main", message)
            break
    active_connections.remove(writer)
    writer.close()

async def auth_adm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    ...

async def auth_vm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    while True:
        message = f"Enter pass to connect on server"
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(256)
        msg = data.decode()
        await writer.drain()
        print(msg)
        if msg == SERVER_PASS:
            msg = "sussess"
            writer.write(msg.encode())
            active_connections.append(writer)
            await writer.drain()
            break
        else:
            writer.write("Wrong Password".encode())
            writer.close()
            break


async def handle_echo(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:

    addr = writer.get_extra_info('peername')
    data = await reader.read(256)
    data = data.decode()  # Bags
    await writer.drain()
    if writer not in active_connections and writer not in admin_connections:
        if data == "admin_connect":
            ...
        await auth_vm(writer=writer, reader=reader)

    print(f"{addr!r} is connected !!!!")

    if writer in active_connections:
        await hub_vm(writer=writer, reader=reader)


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
