import base64
import json
from unittest.mock import Mock, patch

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase

from integration.handlers import ImportClientJsonHandler

from tests import setup_future


class ImportClientJsonHandlerTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.db = Mock()
        super().setUp()

    def _encode_file(self, file_path):
        with open(file_path, 'rb') as csv_file:
            encoded_bytes = base64.b64encode(csv_file.read())
        return encoded_bytes.decode()

    def get_app(self):
        handlers = [
            (r"/", ImportClientJsonHandler)
        ]
        return Application(handlers, db=self.db)

    @patch("integration.handlers.ClientController.import_clients")
    def test_import_json(self, _import_clients):
        _import_clients.return_value = setup_future(True)
        encoded_file = self._encode_file("tests/resources/clients_data.csv")
        body = {
            "dataFile": encoded_file
        }

        response = self.fetch("/", method="POST", body=json.dumps(body))

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual({"message": "Processed"}, body)
        _import_clients.assert_called_once_with(encoded_file)

    def test_import_without_file(self):
        response = self.fetch("/", method="POST", body="{}")

        self.assertEqual(response.code, 400)

    def test_import_empty_body(self):
        response = self.fetch("/", method="POST", body="")

        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertDictEqual({"message": "Empty Body"}, body)

    def test_import_without_data(self):
        body = {
            "dataFile": ""
        }

        response = self.fetch("/", method="POST", body=json.dumps(body))

        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertDictEqual({"message": "Empty Data File"}, body)

    @patch("integration.handlers.ClientController.import_clients")
    def test_import_without_sucess(self, _import_clients):
        _import_clients.return_value = setup_future(False)
        encoded_file = self._encode_file("tests/resources/clients_data.csv")
        body = {
            "dataFile": encoded_file
        }

        response = self.fetch("/", method="POST", body=json.dumps(body))

        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertDictEqual({"message": "Could not import data"}, body)
        _import_clients.assert_called_once_with(encoded_file)
