import asyncio

active_connections = []


async def handle_echo(
        reader,
        writer
):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    info = writer.get_extra_info("socket")
    print(info)
    # addr = writer.get_extra_info('peername')
    # local_addr = writer.get_extra_info('sockname')
    # ssl_context = writer.get_extra_info('sslcontext')
    # is_server_side = writer.get_extra_info('server_side')
    # peer_cert = writer.get_extra_info('peercert')
    print(f"Received {message!r} from {addr!r}")
    active_connections.append(addr)
    print(f"Active connections: {active_connections}")
    print(f"Send: {message!r}")
    print(message)
    writer.write(data)
    if message == "/main":
        writer.write(b"{Hello pidr}")

    await writer.drain()
    if message == ".quit":
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


# import asyncio
#
#
# class EchoServerProtocol(asyncio.Protocol):
#     def __init__(self):
#         self.transport = None
#         self.loop = None
#
#     def connection_made(self, transport):
#         self.transport = transport
#         self.loop = asyncio.get_event_loop()
#         self.loop.create_task(self.send_messages())
#
#     async def send_messages(self):
#         while True:
#             self.transport.write(b'Hello, client!')
#             await self.transport.drain()
#             await asyncio.sleep(1)
#
#
# async def main():
#     server = await asyncio.start_server(
#         lambda: EchoServerProtocol(),
#         '127.0.0.1', 8888
#     )
#     addr = server.sockets[0].getsockname()
#     print(f'Serving on {addr}')
#     async with server:
#         await server.serve_forever()
#
#
# asyncio.run(main())
