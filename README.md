# python-websockets-cli
A sample app with Python and Websockets, it can start a server and a client. 

This is a task from the backend [roadmap.sh](https://roadmap.sh). 

Project details can be found here from [Broadcast Server](https://roadmap.sh/projects/broadcast-server)

# Structure
- `main.py`: is where you start, it will bootstrap a command line argument managment using argparse.
- `server.py`: handles creating a websocket server.
- For my experimenation, I made three solution variants for the client: `client_one.py`, `client_two.py` and `client_three.py` (Main solution).

# Setting up
- install `websockets` using `pip install websockets`
- create your env using for example `venv` or your favourite management tool
- using `venv`: `python -m venv .venv`
    -   `./.venv/Scripts/activate` on windows
- Python version used is : `Python 3.12`

# Running the app
- To start the websocket server do:
    - `python main.py broadcast-server start`
- To start a websocket client do:
- `python main.py broadcast-server connect`

Available commands:
- `broadcast-server`: initial command
- `start`: bootstraps the server
- `connect`: bootstraps the client


## Client One (`clinet_one.py`)
This is a basic attempt, I applied a pattern that appearntly is commonly followed when executing multiple concurrent tasks, this uses the `wait` function from `asyncio` to listen when the event completes and then cancel all other events.

## Client Two (`client_two.py`)
I just wanted to experiment on how I could do `client_one.py` differently. Here I simply use `asyncio.gather` to call multiple tasks concurrently, I added a monitoring task that will set a `running` flag to false and stop all tasks.

## Client Three (`client_three.py`)
In here, I experimented with TaskGroup context management, which is in my opinion a more effective solution than the previous two and a step up. I also no longer use a `running` flag to stop the tasks, but use `future` from the running event loop to manage the tasks.





