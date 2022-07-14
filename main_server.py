import asyncio
import json

import mqttools


# class main_server:
#     def __init__(self, host='localhost', broker_port=10008):
#         self.PORT = broker_port
#         self.next_device_number = 0
#
#     async def start_client(self):
#         client = mqttools.Client('localhost', self.PORT, connect_delays=[0.1])
#         await client.start()
#
#         return client
#
#     async def device_num(self):

BROKER_PORT = 1883


async def start_client():
    client = mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1])
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
        broker = mqttools.Broker(('localhost', BROKER_PORT))
        await broker.serve_forever()

    async def start_client(self):
        client = mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1])
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
            await asyncio.sleep(1)

    async def get_jsons(self):
        print('Get json start')
        client = await self.start_client()
        while True:
            print(self.json_channels_set)
            for device_number in self.json_channels_set:
                print(device_number)
                self.device_number = max(self.json_channels_set) + 1
                topic = '/json_channel/' + str(device_number)
                await client.subscribe(topic)
                message = await client.messages.get()
                msg = json.loads(message.message.decode())
                print('Message json:')
                print(msg)
            await asyncio.sleep(1)

    async def device_main(self):
        await asyncio.gather(
            self.broker_main(),
            self.new_device_register(),
            self.get_jsons())


if __name__ == '__main__':
    server = main_server()
    asyncio.run(server.device_main())


