import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO)


def log_message(message: str) -> None:
    logging.info(f"Message: {message}")

async def consumer_header(websocket: websockets.WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)

async def consumer(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    print(websocket_resource_url)
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_header(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consumer('localhost', 4000))
    loop.run_forever()

