import asyncio
import argparse

from client_three import start_client
# from client_two import start_client as client_two
# from client_two import start_client as client_one
from server import start_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Broadcast Server Control",
        formatter_class=argparse.RawTextHelpFormatter  # Important for newline formatting
    )

    parser.add_argument(
        "command",
        choices=["broadcast-server"],
        help="Command to execute."
    )

    parser.add_argument(
        "action",
        choices=["start", "connect"],
        help="Action to perform:\n"
             "  * start: Start the broadcast server.\n"
             "  * connect: Connect to the broadcast server."
    )

    args = parser.parse_args()

    if args.command == "broadcast-server":
        if args.action == "start":
            asyncio.run(start_server())
        elif args.action == "connect":
            asyncio.run(start_client())
        else:
            print(f"Invalid action: {args.action}")
