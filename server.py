from websockets import ConnectionClosed, ServerConnection, serve

from handlers import handle_connection_welcome


PORT = '8765'

connections = set()


async def handler(websocket: ServerConnection):
    connections.add(websocket)
    print(f'clients connected: {len(connections)}')
    await handle_connection_welcome(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connections:
                if conn != websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients
    except ConnectionClosed as e:
        print("A client just disconnected", e)
    finally:
        print("removed client")
        connections.remove(websocket)


async def start_server():
    # first argument is the handler for each client
    # second argument is the network interfaces where the server can be reached from,
    # "" means all interfaces
    async with serve(handler, "", PORT) as server:
        print(f'WebSocket server started on ws://localhost:{PORT}')
        await server.serve_forever()
