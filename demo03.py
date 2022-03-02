# To test: python3 -m websockets ws://localhost:8001/
import asyncio
import websockets
import json


connected = set()
logged_in_users = set()

async def send_message_to_clients(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        type = data.get('type')
        if type == 'login':
            logged_in_users.add(data.get('username'))    
            message = {
                'type': 'login',
                'users': list(logged_in_users)
            }
        elif type == 'disconnect':
            print('DISCONNECT', data);
            list(logged_in_users).delete(data.username)
            message = {
                'type': 'disconnect',
                'users': list(logged_in_users)
            }
        elif type == 'chat':
            print('CHAT', data)
            message = data
        else:
            print("Message type not recognized")
        if message:
            await relay_message(message)

async def relay_message(websocket, message):
    await websocket.send(json.dumps(message))
    for sock in connected:
        if sock != websocket:
            await sock.send(json.dumps(message))


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
    # websockets.serve(send_message_to_clients, "", 8001)
    async with websockets.serve(send_message_to_clients, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print('Starting web socket server...')
    asyncio.run(main())