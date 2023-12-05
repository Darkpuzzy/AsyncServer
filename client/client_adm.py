import asyncio
from asyncio import StreamReader, StreamWriter

token = None


async def adm_auth(
        writer: asyncio.StreamWriter,
        reader: asyncio.StreamReader
):
    init_message = "sudo su"
    writer.write(init_message.encode())
    data = await reader.read(600)
    print("---------------------------------------------------------|\n")
    print(data.decode())
    print("---------------------------------------------------------|\n")
    message: str = input("Password: ")
    writer.write(message.encode())
    await writer.drain()
    data = await reader.read(600)
    answer = data.decode()
    print(answer)
    await writer.drain()
    if answer == "success":
        return True
    return False


async def client_tcp_admin(reader: StreamReader, writer: StreamWriter):
    first_auth = await adm_auth(writer=writer, reader=reader)

    if first_auth is False:
        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    await writer.drain()

    while True:
        try:
            message: str = input("Command: ")
            if message == "":
                message = "."

            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(650)
            answer = data.decode()

            print("Server message\n", answer)

            if message == "exit":
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
    try:
        await client_tcp_admin(reader, writer)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    print("Hi, it is admin vm")
    print("enter 'help' to the show a server commands")
    asyncio.run(main())
