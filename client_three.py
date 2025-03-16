import asyncio
import traceback
from websockets import ConnectionClosedOK, connect

PORT = '8765'

async def receive_messages(websocket, future):
    """
    Continuously receive and display messages from the server
    """
    try:
        while True:
            if future.done():
                return
                
            message = await websocket.recv()

            print(f"\nReceived: {message}")

            # Print the prompt again to improve user experience
            print("\nEnter message (or 'exit' to quit): ", end="")

    except Exception as e:
        print(f"\nError receiving message: {e}")

        if not future.done():
            future.set_result(True)
        return


async def send_messages(websocket, future):
    """
    Send messages from user input to the server
    """

    while True:
        try:
            message_thread = asyncio.to_thread(
                input, "\nEnter message (or 'exit' to quit): ")

            message = await message_thread

            # message = await loop.run_in_executor(None, input, "\nEnter message (or 'exit' to quit): ")

            if message.lower() == 'exit' or future.done():
                if not future.done():
                    future.set_result(True)
                break

            await websocket.send(
                message
            )

        except Exception as e:
            print(f"Error sending message: {e}")
            message_thread.close()

            if not future.done():
                future.set_result(True)
            return


async def monitor_shutdown(future, tasks):
    """
    Monitor the shutdown future and cancel the receive task when it's set
    """
    try:
        await future
        # If we get here, the future was completed
        print('we should cancel all tasks')
        for task in tasks:
            task.cancel()
                
    except asyncio.CancelledError:
        print("\nMonitor task cancelled")
        raise


async def start_client():
    uri = f"ws://localhost:{PORT}"

    loop = asyncio.get_running_loop()
    shutdown_future = loop.create_future()

    async with connect(uri) as websocket:
        try:
            welcome_message = await websocket.recv()
            print(f"Connected to {uri} {welcome_message}")

            async with asyncio.TaskGroup() as tg:
                receive_task = tg.create_task(
                    receive_messages(websocket, shutdown_future))

                send_task = tg.create_task(
                    send_messages(websocket, shutdown_future))

                tg.create_task(monitor_shutdown(
                    shutdown_future, [receive_task, send_task]))
            
            
        except ConnectionClosedOK:
            print("Connection closed by server.")
        except Exception as e:
            traceback.print_exc(e)
