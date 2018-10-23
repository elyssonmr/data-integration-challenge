import json

from tornado.web import RequestHandler

from integration.controllers import ClientController


class ImportClientJsonHandler(RequestHandler):
    async def post(self):
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"message": "Empty Body"})
            return

        data_file = body.get("dataFile")
        if not data_file:
            self.set_status(400)
            self.write({"message": "Empty Data File"})
            return

        controller = ClientController()
        status = await controller.import_clients(data_file)
        if status:
            self.write({"message": "Processed"})
        else:
            self.set_status(400)
            self.write({"message": "Could not import data"})
