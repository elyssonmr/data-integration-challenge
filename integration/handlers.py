import json

from tornado.web import RequestHandler

from integration.controllers import ClientController


class ImportClientJsonHandler(RequestHandler):
    async def post(self):
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"status": "Empty Body"})
            return

        data_file = body.get("dataFile")
        if not data_file:
            self.set_status(400)
            self.write({"status": "Empty Data File"})
            return

        controller = ClientController()
        status = await controller.import_clients(data_file)
        if status:
            self.write({"status": "processed"})
        else:
            self.set_status(400)
            self.write({"status": "Errors"})
