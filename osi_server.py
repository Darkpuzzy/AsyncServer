import asyncio
from typing import Tuple
from src.server.commands import commander, loggin, register

active_connections = []


async def forward_msg_to_clients(
        writer: asyncio.StreamWriter,
        addr: Tuple[str],
        msg: str
) -> None:
    for w in active_connections:
        print(w == writer)
        if w != writer:
            msg = f"{addr!r} sent {msg}"
            w.write(msg.encode())


async def handle_echo(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info('peername')
    print('Connection established with {}'.format(addr))
    data = await reader.read(256)
    msg = data.decode()
    # info = writer.get_extra_info("socket")

    # if "set_password" in msg:
    #     msg = msg.split("-p")
    #     password = msg[1].replace(" ", "")
    #     response: str = await setter_pass(password=password)
    #     writer.write("Success".encode())
    #     await writer.drain()
    # else:
    if "register" in msg:
        print(msg)
        user_data = msg.split("-u")[1].replace(" ", "")
        print(user_data)
        response: bool = await register(user_data=user_data)
        if response:
            print("AUTH", user_data)
            token = await loggin(user_data)
            writer.write(token.encode())
        await writer.drain()
    else:
        response: str = await commander(msg=msg)
        writer.write(response.encode())
        await writer.drain()

    if msg == ".quit":
        print("Close the connection")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())

# writers = []
#
#
# def forward(writer, addr, message):
#     for w in writers:
#         print(f"{addr!r}")
#         if w != writer:
#             w.write(f"{addr!r}: {message!r}\n".encode())
#
#
# async def handle(reader, writer):
#     writers.append(writer)
#     addr = writer.get_extra_info('peername')
#     message = f"{addr!r} is connected !!!!"
#     print(message)
#     forward(writer, addr, message)
#     while True:
#         data = await reader.read(100)
#         message = data.decode().strip()
#         forward(writer, addr, message)
#         await writer.drain()
#         if message == "exit":
#             message = f"{addr!r} wants to close the connection."
#             print(message)
#             forward(writer, "Server", message)
#             break
#     writers.remove(writer)
#     writer.close()
#
#
# async def main():
#     server = await asyncio.start_server(
#         handle, '127.0.0.1', 8888)
#     addr = server.sockets[0].getsockname()
#     print(f'Serving on {addr}')
#     async with server:
#         await server.serve_forever()
#
# asyncio.run(main())
