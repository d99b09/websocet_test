import asyncio
import json

import mqttools

HOST = 'localhost'
BROKER_PORT = 1883


async def start_client():
    client = mqttools.Client(HOST, BROKER_PORT)
    await client.start()
    return client

async def server_main():
    client = await start_client()
    print('Client started')
    while True:
        #find new devices
        await client.subscribe('/new_device')
        message = await client.messages.get()
        print(f'Message: {message.message} on {message.topic}')

class main_server:
    def __init__(self):
        self.device_number = 0
        self.json_channels_set = set()

    async def broker_main(self):
        broker = mqttools.Broker((HOST, BROKER_PORT))
        await broker.serve_forever()

    async def start_client(self):
        client = mqttools.Client(HOST, BROKER_PORT, connect_delays=[0.1])
        await client.start()

        return client

    async def new_device_register(self):
        client = await self.start_client()
        print('Client started')
        while True:
            # find new devices
            self.device_number += 1
            await client.subscribe('/new_device')
            message = await client.messages.get()
            self.json_channels_set.add(self.device_number)
            print(f'Message: {message.message.decode()} on {message.topic}')
            client.publish(mqttools.Message('/new_device_number', str(self.device_number).encode('ascii')))
            self.device_number -= 1
            await asyncio.sleep(0.01)

    async def get_jsons(self):
        print('Get json start')
        client = await self.start_client()
        while True:
            # print(self.json_channels_set)
            for device_number in self.json_channels_set:
                try:
                    print(device_number)
                    self.device_number = max(self.json_channels_set) + 1
                    topic = '/json_channel/' + str(device_number)

                    await client.subscribe(topic)
                    message = await asyncio.wait_for(client.messages.get(), timeout=7.5)
                    msg = json.loads(message.message.decode())
                    print('Message json:')
                    print(msg)
                except:
                    print(f'remove {device_number}')
                    self.json_channels_set.remove(device_number)
                    break
            await asyncio.sleep(0.01)

    async def open_channels_publish(self):
        client = await self.start_client()
        while True:
            client.publish(mqttools.Message('/open_channels', str(self.json_channels_set).encode('ascii')))
            await asyncio.sleep(0.01)


    async def server_main(self):
        await asyncio.gather(
            # self.broker_main(),
            self.open_channels_publish(),
            self.new_device_register(),
            self.get_jsons())


if __name__ == '__main__':
    server = main_server()
    asyncio.run(server.server_main())


