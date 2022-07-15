import asyncio
import json

import mqttools

BROKER_PORT = 1883


class main_client:
    def __init__(self):
        self.json_channel_set = set()

    def bstr_to_intset(self, bstr):
        strset = set(bstr.decode())
        intset = set()
        for i in strset:
            try:
                intset.add(int(i))
            except:
                pass
        return intset

    async def start_client(self):
        client = mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1])
        await client.start()
        return client

    def lv0(self, di, action_limit=0.5):
        action_bool = 0 if di['s'] < action_limit else 1
        return {'x': di['x'], 'y': di['y'], 'action': action_bool}

    async def get_channels(self):
        client = await self.start_client()
        while True:
            await client.subscribe('/open_channels')
            message = await client.messages.get()
            print(f'Message: {message.message}')
            self.json_channel_set = self.bstr_to_intset(message.message)
            print(f'Devise number: {self.json_channel_set}')
            await asyncio.sleep(1)

    async def get_jsons(self):
        print('Get json start')
        client = await self.start_client()
        while True:
            # print(self.json_channels_set)
            for device_number in self.json_channel_set:
                try:
                    print(device_number)
                    self.device_number = max(self.json_channel_set) + 1
                    topic = '/json_channel/' + str(device_number)
                    await client.subscribe(topic)
                    message = await asyncio.wait_for(client.messages.get(), timeout=7.5)
                    msg = json.loads(message.message.decode())
                    print('Message json:')
                    print(msg)
                    print('Lv0')
                    msg_l0 = self.lv0(msg)
                    print(msg_l0)
                except:
                    print(f'remove {device_number}')
                    break
            await asyncio.sleep(1)

    async def client_main(self):
        await asyncio.gather(
            self.get_channels(),
            self.get_jsons(),
        )


if __name__ == '__main__':
    client = main_client()
    asyncio.run(client.client_main())
