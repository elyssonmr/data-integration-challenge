import base64
import json
from unittest.mock import MagicMock, Mock, patch

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase

from integration.handlers import ImportCompaniesJsonHandler

from tests import setup_future

MERGE_DATA = ("name;addresszip;website\n"
              "tola sales group;78229;http://repsources.com")


class ImportCompaniesJsonHandlerTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.companies = Mock()
        self.db = MagicMock()
        self.db.__getitem__.side_effect = {
            "companies": self.companies}.__getitem__
        super().setUp()

    def get_app(self):
       handlers = [
           (r"/", ImportCompaniesJsonHandler)
       ]

       return Application(handlers, db=self.db)

    def _encode_file(self, file_path):
        with open(file_path, 'rb') as csv_file:
            encoded_bytes = base64.b64encode(csv_file.read())
        return encoded_bytes.decode()

    @patch("integration.handlers.CompaniesController.merge_companies")
    def test_merge_companies(self, _merge_companies):
        _merge_companies.return_value = setup_future()
        encoded_file = self._encode_file("tests/resources/merge_data.csv")
        input_data = {
            "data": encoded_file
        }

        response = self.fetch("/", method="POST", body=json.dumps(input_data))

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertDictEqual(body, {"message": "Parsed"})

    def test_merge_without_data(self):
        input_data = {"data": ""}
        response = self.fetch("/", method="POST", body=json.dumps(input_data))

        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertDictEqual(body, {"message": "No data to merge"})

    def test_merge_malformed_json(self):
        response = self.fetch("/", method="POST", body="")

        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertDictEqual(body, {"message": "Malformed JSON"})
