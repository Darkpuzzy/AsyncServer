import asyncio


async def tcp_echo_client(message):
    try:
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

        if message == ".quit":
            print('Close the connection')
            writer.close()
            await writer.wait_closed()
    except Exception as err:
        print(err)
        print('Close the connection')
        writer.close()
        await writer.wait_closed()

while True:
    try:
        a = input("TEXT -> ")
        if a == ".quit":
            break
        asyncio.run(tcp_echo_client(a))
    except Exception as err:
        break
