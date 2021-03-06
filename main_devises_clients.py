import asyncio
import json
import mqttools
import websockets

HOST = 'localhost'
PORT = 1883

WS_HOST = 'localhost'
WS_PORT = 8765


async def start_client():
    client = mqttools.Client(HOST, PORT, connect_delays=[0.1])
    await client.start()

    return client

async def new_client_main():
    client = await start_client()
    await client.subscribe('/new_device')
    message = str(True).encode('ascii')
    while True:
        print(f'client: Publishing {message} on /new_device.')
        client.publish(mqttools.Message('/new_device', message))
        await asyncio.sleep(1)

class device_client:
    def __init__(self):
        self.device_number = 0
        self.greeting = json.dumps({'x': 0, 'y': 0, 's': 0})

    async def listen(self):
        async with websockets.connect('ws://'+ WS_HOST +':' + str(WS_PORT) +'/sub') as websocket:
            while True:
                self.greeting = await websocket.recv()
                print("< {}".format(self.greeting))

    async def start_client(self):
        client = mqttools.Client(HOST, PORT)
        await client.start()

        return client

    async def new_device(self):
        client = await self.start_client()
        await client.subscribe('/new_device')
        message = str(True).encode('ascii')
        while not self.device_number:
            print(f'client: Publishing {message} on /new_device.')
            client.publish(mqttools.Message('/new_device', message))
            await asyncio.sleep(0.01)

    async def set_device_number(self):
        client = await self.start_client()
        while not self.device_number:
            await client.subscribe('/new_device_number')
            message = await client.messages.get()
            print(f'Message: {message.message}')
            self.device_number = int(message.message.decode())
            print(f'Devise number: {self.device_number}')
            await asyncio.sleep(0.01)

    async def message_json(self):
        client = await self.start_client()
        while True:
            if self.device_number:
                topic = '/json_channel/' + str(self.device_number)
                json_msg = self.greeting
                # print(json_msg)
                # message = json.dumps({'x': 0, 'y': 0, 's': 0}).encode('ascii')
                message = self.get_serial()
                message = json_msg.encode('ascii')
                client.publish(mqttools.Message(topic, message))
            await asyncio.sleep(0.01)


    async def client_main(self):
        await asyncio.gather(
            self.listen(),
            self.new_device(),
            self.set_device_number(),
            self.message_json())




device = device_client()
asyncio.run(device.client_main())