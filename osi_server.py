import asyncio
from typing import Tuple
from src.server.commands import commander

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
    # if writer not in active_connections:
    #     writer.write(b"HELLO USER")
    data = await reader.read(256)
    msg = data.decode()
    addr = writer.get_extra_info('peername')
    info = writer.get_extra_info("socket")
    """
    # print(f"Received {msg!r} from {addr!r}")
    # if writer not in active_connections:
    #     active_connections.append(writer)
    # print(len(active_connections))
    # print(f"Active connections: {active_connections}")
    # # print(f"Send: {msg!r}")
    # # print(msg)
    # await forward_msg_to_clients(writer=writer, addr=addr, msg=data.decode())
    # # writer.write(data)
    # if msg == "/main":
    #     writer.write(b"{Hello pidr}")
    """
    print(msg)
    response: str = await commander(msg=msg)
    print(response)
    writer.write(response.encode())
    await writer.drain()

    if msg == ".quit":
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    # addr = writer.get_extra_info('peername')
    # local_addr = writer.get_extra_info('sockname')
    # ssl_context = writer.get_extra_info('sslcontext')
    # is_server_side = writer.get_extra_info('server_side')
    # peer_cert = writer.get_extra_info('peercert')


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
