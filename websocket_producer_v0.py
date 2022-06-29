import asyncio
import websockets

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        await websocket.send(message)
        await websocket.recv()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce(message='hi', host='localhost', port=4000))