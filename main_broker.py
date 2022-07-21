import asyncio
import mqttools

HOST = 'test.mosquitto.org'
BROKER_PORT = 1883


async def broker_main():
    """The broker, serving both clients, forever.
    """

    broker = mqttools.Broker((HOST, BROKER_PORT))
    # name = await broker.getsockname()
    # print(name)

async def main():
    await broker_main()


asyncio.run(main())

