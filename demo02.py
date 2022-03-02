# To test: python3 -m websockets ws://localhost:8001/
import asyncio
import websockets
import json


connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    print('A client just connected:', connected, path)
    try:
        async for message in websocket:
            print('received message from client:', message)
            await websocket.send('Pong: ' + message)
            for sock in connected:
                if sock != websocket:
                    await sock.send('Broadcast: ' + message)
    except websockets.ConnectionClosed as e:
        print('A client just disconnected')
        print(e)
    finally:
        connected.remove(websocket)

# start_server = websockets.serve(echo, "localhost", 8001)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
async def main():
    websockets.serve(echo, "", 8001)
    async with websockets.serve(echo, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print('Starting web socket server...')
    asyncio.run(main())