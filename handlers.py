from websockets import ConnectionClosedError, ConnectionClosedOK, ServerConnection


def websocket_handler(handler, connections: set[ServerConnection]):
    async def get_handler(websocket):
        try:
            await handler(websocket, connections)
        except ConnectionClosedOK:
            print(f"Client disconnected: {websocket.remote_address}")

        except ConnectionClosedError:
            print(f"Client disconnected abruptly: {websocket.remote_address}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if websocket in connections:
                connections.remove(websocket)
            print(f"Client handler finished: {websocket.remote_address}")
    return get_handler


async def handle_connection_welcome(websocket: ServerConnection):
    welcome_message = "Welcome to the WebSocket server!"
    await websocket.send(welcome_message)


async def handle_client_message(websocket: ServerConnection, cons: set[ServerConnection]):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)
        # for client in cons:
        #     if client != websocket:
        #         await client.send(message)
