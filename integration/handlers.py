import json

from tornado.web import RequestHandler

from integration.controllers import CompaniesController


class ImportClientJsonHandler(RequestHandler):
    async def post(self):
        # change here
        pass
