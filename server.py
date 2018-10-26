import asyncio
import logging

from integration.application import make_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_app())
    logger.info("Server Listening at port 8000")
    loop.run_forever()
