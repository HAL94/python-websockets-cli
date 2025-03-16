import asyncio
import websockets

PORT = '8765'


running = True

async def receive_messages(websocket):
    """
    Continuously receive and display messages from the server
    """

    global running
    try:
        while running:
            message = await websocket.recv()

            print(f"\nReceived: {message}")

            # Print the prompt again to improve user experience
            print("\nEnter message (or 'exit' to quit): ", end="")

    except websockets.ConnectionClosed:
        print("\nConnection to server closed")
        running = False
    except asyncio.CancelledError:
        print("\nReceive task cancelled")
        running = False
        raise
    except Exception as e:
        print(f"\nError receiving message: {e}")
        running = False


async def send_messages(websocket):
    """
    Send messages from user input to the server
    """
    global running
    while running:
        try:
            # Use asyncio.to_thread in Python 3.9+ or create a custom solution for earlier versions
            # message = await asyncio.get_event_loop().run_in_executor(
            #     None, lambda: input("\nEnter message (or 'exit' to quit): ")
            # )
            message = await asyncio.to_thread(input, "\nEnter message (or 'exit' to quit): ")

            if message.lower() == 'exit':
                running = False
                break

            # Send the message as whatever
            await websocket.send(
                message
            )
        except Exception as e:
            print(f"Error sending message: {e}")
            running = False
            break


async def start_client():
    uri = f"ws://localhost:{PORT}"
    async with websockets.connect(uri) as websocket:
        try:
            try:
                welcome_message = await websocket.recv()
                print(f"Connected to {uri} {welcome_message}")
            except websockets.ConnectionClosedOK:
                return

            # solution 1
            # Wait for either task to complete
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))
            _, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel any pending tasks
            for task in pending:
                task.cancel()

        except websockets.ConnectionClosedOK:
            print("Connection closed by server.")
        except websockets.ConnectionClosedError:
            print("Connection closed abruptly.")
        except asyncio.CancelledError:
            print('All canceled')
            exit(-1)
        except Exception as e:
            print(f"Error receiving messages: {e}")
