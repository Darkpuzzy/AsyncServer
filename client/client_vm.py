import asyncio
import json
from asyncio import StreamReader, StreamWriter

from src.view import ManagerVM

vm_example = None


async def update_status(writer: asyncio.StreamWriter, reader: asyncio.StreamReader):
    while True:
        writer.write("admin_pong".encode())
        await writer.drain()
        answer = await received(reader=reader)
        print("ANSWER", answer)
        break


async def connect_vm(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        message: str
):
    writer.write(message.encode())
    await writer.drain()
    data = await reader.read(256)
    print(data.decode())
    msg = input("Get the initial setup of a virtual machine? (y/N): ")
    if msg == "y":
        data_vm: str = json.dumps(await vm_example.get_base_info())
        writer.write(data_vm.encode())
        await writer.drain()
        print(f"SYSTEM: \nYou send VM Data: \n{data_vm}")
        data = await reader.read(256)
        print(data.decode())
    else:
        print("Cancel operation")


async def auth(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    init_message = "connect_vm"
    writer.write(init_message.encode())
    data = await reader.read(256)
    print("---------------------------------------------------------|\n")
    print(data.decode())
    print("---------------------------------------------------------|\n")
    message: str = input("Password: ")
    writer.write(message.encode())
    await writer.drain()
    data = await reader.read(256)
    answer = data.decode()
    print(answer)
    await writer.drain()
    if answer == "success":
        return True
    return False


async def received(reader: asyncio.StreamReader):
    data = await reader.read(256)
    answer = data.decode()
    return answer


async def update_vm(msg: str):
    global vm_example
    try:
        print("---"*80)
        print(msg)
        data = msg.split("-d")
        print(data)
        data_dict: dict = json.loads(data.decode())
        vm_example = ManagerVM(**data_dict)
        print("YOUR DATA IS UPDATED-------------------------")
        print(vm_example.get_full_info())
        return "SUCCESS UPDATED"
    except Exception as err:
        print("CLIENT ERROR\n", err)


async def client_tcp_vm(reader: StreamReader, writer: StreamWriter):
    first_auth = await auth(writer=writer, reader=reader)

    if first_auth is False:
        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    await writer.drain()

    while True:
        try:
            message: str = input("Command: ")
            if message == "":
                continue
            if message == "my_comp":
                print(await vm_example.get_full_info())
            elif message == "connect":
                await connect_vm(writer=writer, reader=reader, message=message)
            else:
                writer.write(message.encode())
                await writer.drain()
                # data = await reader.read(256)
                # await writer.drain()
                # answer = data.decode()
                answer = await received(reader=reader)

                print("Server message\n", answer)
                if "admin_ping" in answer:
                    await update_status(writer=writer, reader=reader)
                await writer.drain()

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
    print("------------------VM INFO------------------")
    print(await vm_example.get_full_info())
    try:
        await client_tcp_vm(reader, writer)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    print("Hi, it is necessary to determine the settings of your virtual machine")
    cpu: int = int(input("CPU: "))
    ram: int = int(input("RAM GB: "))
    disc: int = int(input("CD SIZE GB: "))
    vm_example = ManagerVM(cpu=cpu, ram=ram, disc=disc)
    print("enter 'help' to the show a server commands")
    asyncio.run(main())
