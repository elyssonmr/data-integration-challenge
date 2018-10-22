import asyncio

from integration.application import make_app



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    make_app()
    print("Server Listening at port 8000")
    loop.run_forever()
