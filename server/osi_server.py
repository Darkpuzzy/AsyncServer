import asyncio

from connection_manager.manager import ConnectManager
from handle_process import (
    connection,
    action_by_id,
    show_all_gen,
    forward_to_adm,
    forward,
    auth, active_connections_gen)

from src.commands import commander_maps


async def hub_adm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
) -> None:
    while True:
        addr = writer.get_extra_info('peername')

        data = await reader.read(256)
        msg = data.decode()
        print("Admin", msg)

        if msg == ".":
            writer.write(" ".encode())
            await writer.drain()
            continue

        if msg == "active-connections":
            try:
                result = ConnectManager.show_all_connections
                await active_connections_gen(
                    writer=writer,
                    reader=reader,
                    answer=result
                )
                # writer.write(result.encode())
                # await writer.drain()
            except Exception as err:
                writer.write(str(err).encode())
                await writer.drain()
            continue

        if msg == "update_con":
            await forward(
                writer=writer,
                addr=addr,
                message="admin_ping"
            )
            writer.write("await".encode())
            continue

        if "show_obj" in msg or "delete_obj" in msg:
            await action_by_id(
                writer=writer,
                reader=reader,
                msg=msg
            )
            continue

        if msg == "show_all":
            try:
                answer = await commander_maps(msg, admin=True)
                print("ANSWER HUB", answer)
                await show_all_gen(
                    writer=writer,
                    reader=reader,
                    answer=answer
                )
            except Exception as err:
                writer.write(str(err).encode())
                await writer.drain()
            continue

        answer = await commander_maps(msg, admin=True)

        writer.write(answer.encode())
        await writer.drain()

        if msg == "exit":
            message = f"{addr!r} wants to close the connection."
            print(message)
            await forward(writer, "Main", message)
            break

    ConnectManager.active_connections.pop(writer)
    writer.close()


async def hub_vm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
) -> None:
    while True:
        addr = writer.get_extra_info('peername')
        data = await reader.read(256)
        msg = data.decode()
        print(msg)

        if msg == "":
            return

        if msg == "connect":
            msg = await connection(writer, reader)
            writer.write(msg.encode())
            await writer.drain()
            continue

        elif msg == "show_me":
            msg_dict: str = await ConnectManager.show_me(writer=writer)
            writer.write(msg_dict.encode())
            await writer.drain()
            continue

        elif msg == "admin_pong":
            msg_answer = await ConnectManager.update_statuses(
                writer=writer,
                reader=reader,
                answer=msg
            )
            await forward_to_adm(writer, addr, msg_answer)
            writer.write("success".encode())
            continue

        answer = await commander_maps(msg)

        writer.write(answer.encode())
        await writer.drain()

        if msg == "exit":
            message = f"{addr!r} wants to close the connection."
            print(message)
            await forward(writer, "Main", message)
            break

    ConnectManager.active_connections.pop(writer)
    writer.close()


async def handle_tcp(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info('peername')

    data = await reader.read(256)
    data = data.decode()  # Bags

    await writer.drain()
    if writer not in ConnectManager.active_connections and writer not in ConnectManager.admin_connections:
        await auth(writer=writer, reader=reader, data_pre=data)

    print(f"{addr!r} is connected !!!!")
    print(ConnectManager.active_connections)

    if writer in ConnectManager.active_connections:
        await hub_vm(writer=writer, reader=reader)
    elif writer in ConnectManager.admin_connections:
        await hub_adm(writer=writer, reader=reader)


async def main():
    server = await asyncio.start_server(
        handle_tcp, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
