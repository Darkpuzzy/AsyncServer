import asyncio
import json

from connection_manager.manager import ConnectManager
from src.commands import ServerCommander, commander_maps
from src.config import SECRET_SEED, SERVER_PASS


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

            await ConnectManager.update_info_by_writer(
                writer=writer,
                data=data_info
            )
            print(ConnectManager.active_connections)
            status = "Success"
            break
        except Exception as err:
            print("SERVER ERROR", err)
            status = "Problem on server, sorry bruh"
            break
    return status


async def show_by_id(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        msg: str
) -> None:
    while True:
        try:
            answer: dict = await commander_maps(msg, admin=True)
            obj_json = json.dumps(answer)
            writer.write(obj_json.encode())
            await writer.drain()
            break
        except Exception as err:
            print(err)
            writer.write("test".encode())
            await writer.drain()
            break


async def show_all_gen(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader,
        answer
):
    while True:
        try:
            async for chunk in answer():
                chunk_json = json.dumps(chunk)
                writer.write(chunk_json.encode())
                await writer.drain()
                data = await reader.read(256)
                print("data_finish", data.decode())
            writer.write("all data".encode())
            break
        except StopAsyncIteration as err:
            print("ERROR", err)
            writer.write("--------".encode())
            await writer.drain()
            break

    writer.write("--------------------".encode())
    await writer.drain()


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
