import asyncio
import traceback
from websockets import ConnectionClosedOK, connect

PORT = '8765'


async def receive_messages(websocket):
    """
    Continuously receive and display messages from the server
    """
    try:
        while True:

            message = await websocket.recv()

            if message:
                print(f"\nReceived: {message}")
            else:
                break

            # Print the prompt again to improve user experience
            print("\nEnter message (or 'exit' to quit): ", end="")

    except Exception as e:
        print(f"\nError receiving message: {e}")
        return
    finally:
        await websocket.close()


async def send_messages(websocket):
    """
    Send messages from user input to the server
    """

    while True:
        try:
            message_thread = asyncio.to_thread(
                input, "\nEnter message (or 'exit' to quit): ")

            message = await message_thread

            if message.lower() == 'exit':
                break

            await websocket.send(
                message
            )

        except Exception as e:
            print(f"Error sending message: {e}")
            message_thread.close()
            return


async def start_client():
    uri = f"ws://localhost:{PORT}"

    async with connect(uri) as websocket:
        try:
            welcome_message = await websocket.recv()
            print(f"Connected to {uri} {welcome_message}")

            receive_task = asyncio.create_task(
                receive_messages(websocket))  # create task
            send_task = asyncio.create_task(
                send_messages(websocket))  # create task

            _, pending = await asyncio.wait([receive_task, send_task], return_when=asyncio.FIRST_COMPLETED)
            
            for task in pending:
                task.cancel()

        except ConnectionClosedOK:
            print("Connection closed by server.")
        except Exception as e:
            traceback.print_exc(e)
