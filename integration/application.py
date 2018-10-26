from tornado.web import Application
from motor.motor_asyncio import AsyncIOMotorClient

from integration import config
from integration.controllers import CompaniesController
from integration.handlers import ImportClientJsonHandler


def config_mongodb():
    client = AsyncIOMotorClient(config.MONGO_URI)["data_challange"]
    return client

async def load_initial_data(db):
    controller = CompaniesController(db)
    companies_data = open("integration/assets/companies_data.csv")
    await controller.import_companies(companies_data.read())


async def make_app():
    handlers = [
        (r"/api/merge", ImportClientJsonHandler)
    ]
    db = config_mongodb()
    settings = {
        "db": db
    }

    await load_initial_data(db)

    app = Application(handlers, **settings)
    app.listen(8000)
