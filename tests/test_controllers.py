import base64
from unittest.mock import MagicMock, Mock

from tornado.testing import AsyncTestCase, gen_test

from integration.controllers import CompaniesController

from tests import setup_future

COMPANIES_DATA = "name;addressZip\ntola sales group;78229"


class CompanyControllerTestCase(AsyncTestCase):
    def setUp(self):
        super().setUp()
        self.db = Mock()
        company = MagicMock()
        company.__getitem__.side_effect = {"companies": self.db}.__getitem__
        self.controller = CompaniesController(company)

    @gen_test
    async def test_import_companies(self):
        resp = await self.controller.import_companies(COMPANIES_DATA)

        self.assertTrue(resp)

    @gen_test
    async def test_validate_company(self):
        company = {"name": "tola sales group", "addressZip": "78229"}

        try:
            self.controller._validate_company(company)
        except ValueError:
            self.fail("Should validate the company")

    @gen_test
    async def test_validate_invalid_name(self):
        # TODO: Test a company with invalid name
        pass

    @gen_test
    async def test_validate_invalid_address_zip(self):
        # TODO: Test a company with invalid adressZip
        pass

    @gen_test
    async def test_validate_invalid_address_zip_len(self):
        # TODO: Test a company with invalid addressZip length
        pass

    def test_normalize_company(self):
        company = {"name": "tola sales group", "addressZip": "78229"}

        normalized_company = self.controller._normalize_company(company)

        self.assertEqual(normalized_company["name"], company["name"].upper())

    @gen_test
    async def test_save_company(self):
        self.db.update_one.return_value = setup_future()
        company = {"name": "tola sales group", "addressZip": "78229"}

        await self.controller._save_company(company)

        self.db.update_one.assert_called_once_with(company, {"$set": company}, upsert=True)

    @gen_test
    async def test_parse_csv(self):
        expected_csv = {
            "name": "tola sales group",
            "addressZip": "78229"
        }

        csv = self.controller._parse_csv(COMPANIES_DATA)

        self.assertListEqual(csv, [expected_csv])
