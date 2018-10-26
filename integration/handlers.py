import json
import base64

from tornado.web import RequestHandler

from integration.controllers import CompaniesController


class ImportClientJsonHandler(RequestHandler):
    @property
    def db(self):
        return self.settings["db"]

    async def post(self):
        try:
            request_data = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"message": "Malformed JSON"})
            return

        companies_data = request_data.get("data")

        if not companies_data:
            self.set_status(400)
            self.write({"message": "No data to merge"})
            return

        companies_data = base64.b64decode(companies_data.encode()).decode()
        controller = CompaniesController(self.db)
        await controller.merge_companies(companies_data)
        self.write({"message": "Parsed"})
