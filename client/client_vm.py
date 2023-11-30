import asyncio
import os
from asyncio import StreamReader, StreamWriter

from client_view import ManagerVM

vm_example = None


async def tcp_echo_client(reader: StreamReader, writer: StreamWriter):
    init_message = "connect_vm"
    writer.write(init_message.encode())
    data = await reader.read(256)
    print("---------------------------------------------------------")
    print(data.decode())
    print("---------------------------------------------------------")
    while True:
        try:
            message = input("Command: ")
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(256)
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
    print("------------------VM INFO------------------")
    print(await vm_example.get_full_info())
    try:
        await tcp_echo_client(reader, writer)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    print("Hi, it is necessary to determine the settings of your virtual machine")
    cpu: int = int(input("CPU: "))
    ram: int = int(input("RAM GB: "))
    disk_size: int = int(input("CD SIZE GB: "))
    vm_example = ManagerVM(cpu=cpu, ram=ram, disk_size=disk_size)
    print("enter 'help' to the show a server commands")
    asyncio.run(main())
