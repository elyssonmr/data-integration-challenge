from tornado.web import Application
from motor.motor_asyncio import AsyncIOMotorClient

from integration import config


def config_mongodb():
    client = AsyncIOMotorClient(config.MONGO_URI)["data_challange"]
    return client


def make_app():
    handlers = []
    settings = {
        "db": config_mongodb()
    }

    app = Application(handlers, **settings)
    app.listen(8000)
