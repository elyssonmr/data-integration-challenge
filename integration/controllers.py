from csv import DictReader
from io import StringIO
import logging


class CompaniesController:
    IMPORT_FIELDS = ["name", "addressZip"]
    MERGE_FIELDS = ["name", "addressZip", "website"]


    def __init__(self, db):
        self._companies_collection = db["companies"]

    def _parse_csv(self, companies_csv, fields):
        # TODO: run in executor due the possibility of high data volume
        companies = []
        reader = DictReader(StringIO(companies_csv), fieldnames=fields,
                            delimiter=";")
        for row in reader:
            companies.append(dict(row))
        
        return companies[1:] if len(companies) > 1 else []

    def _validate_company(self, company):
        name = company.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("Field 'name' is a required string")
        
        address_zip = company.get("addressZip")
        if not address_zip or not isinstance(name, str):
            raise ValueError("Field 'addressZip' is a required string")

        if len(address_zip) > 5:
            raise ValueError("Field 'adressZip' should have only 5 characters")

    def _normalize_company(self, company):
        normalized_data = {
            "name": company['name'].upper(),
            "addressZip": company["addressZip"]
        }

        if "website" in company:
            normalized_data["website"] = company["website"].lower()

        return normalized_data

    async def _save_company(self, company, should_insert):
        # Update to not duplicate
        search_filter = {
            "name": company["name"],
            "addressZip": company["addressZip"]
        }
        await self._companies_collection.update_one(
            search_filter,
            {"$set": company}, upsert=should_insert)

    async def _import_csv(self, companies_csv, csv_fields, should_update):
        companies = self._parse_csv(companies_csv, csv_fields)
        for company in companies:
            try:
                self._validate_company(company)
                normalized_company = self._normalize_company(company)
                await self._save_company(normalized_company, should_update)
            except ValueError as ex:
                pass

        return True

    async def import_companies(self, companies_csv):
        return await self._import_csv(companies_csv, self.IMPORT_FIELDS, True)

    async def merge_companies(self, companies_csv):
        return await self._import_csv(companies_csv, self.MERGE_FIELDS, False)

    async def filter_companies(self, name, address_zip):
        search_filter = {}
        if name:
            search_filter["name"] = {
                "$regex": f".*{name.upper()}.*"
            }

        if address_zip:
            search_filter["addressZip"] = address_zip

        companies = await self._companies_collection.find(
            search_filter).to_list(None)

        for company in companies:
            company["id"] = str(company["_id"])
            del company["_id"]

        return companies
