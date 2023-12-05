import asyncio
import json

from connection_manager.manager import ConnectManager

from src.commands import commander_maps, ServerCommander
from src.config import SERVER_PASS, SECRET_SEED


async def setter_client_data(data: dict):
    ...


async def connection(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    writer.write("Send your vm data".encode())
    await writer.drain()
    while True:
        try:
            data = await reader.read(256)
            msg = data.decode()

            data_loads: dict = json.loads(msg)
            print("DATA LOADS", data_loads)
            data_info = await ServerCommander.connection(data=data_loads)
            await ConnectManager.update_info_by_writer(writer=writer, data=data_info)
            print(ConnectManager.active_connections)

            status = "Success"
            break
        except Exception as err:
            print("SERVER ERROR", err)
            status = "Problem on server, sorry bruh"
            break
    return status


async def forward_to_adm(writer, addr, message):
    if ConnectManager.admin_connections != {}:
        for w in ConnectManager.admin_connections:
            w.write(f"{addr!r}: {message}".encode())


async def forward(writer, addr, message):
    if ConnectManager.active_connections != {}:
        for w in ConnectManager.active_connections:
            if w != writer:
                w.write(f"{addr!r}: {message}".encode())


async def broadcast_check():
    for w in ConnectManager.active_connections:
        w.write(f"test-ping".encode())


async def hub_adm(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
) -> None:
    while True:
        addr = writer.get_extra_info('peername')
        data = await reader.read(256)
        msg = data.decode()
        print("Admin", msg)
        if msg == "active-connections":
            result: str = await ConnectManager.show_all_connections()
            writer.write(result.encode())
            await writer.drain()
            continue
        if msg == "update_con":
            await forward(writer=writer, addr=addr, message="admin_ping")
            writer.write("await".encode())
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
            msg_answer = await ConnectManager.update_statuses(writer=writer, reader=reader, answer=msg)
            await forward_to_adm(writer, addr, msg_answer)
            writer.write("success".encode())
            continue
        await writer.drain()
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


async def auth(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        data_pre: str
):
    while True:
        addr = writer.get_extra_info('peername')
        message = f"Enter pass to connect on server"
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(256)
        msg = data.decode()
        await writer.drain()
        print(msg)
        if data_pre == "sudo su":
            if msg == SECRET_SEED:
                msg = "success"
                writer.write(msg.encode())
                await ConnectManager.add_to_adm_con(writer=writer, addr=addr)
                await writer.drain()
                break
        elif msg == SERVER_PASS:
            msg = "success"
            writer.write(msg.encode())
            await ConnectManager.add_to_default_con(writer=writer, addr=addr)
            await writer.drain()
            break
        else:
            writer.write("Wrong Password".encode())
            writer.close()
            break


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

# upd_data: dict = active_connections[writer]["info"].__dict__
#
# print("UP DATA", upd_data, type(upd_data))
# writer.write(f"setter -j -d {upd_data}".encode())
# await writer.drain()
