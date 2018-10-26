from csv import DictReader
from io import StringIO


class CompaniesController:
    FIELDSNAME = ["name", "addressZip"]

    def __init__(self, db):
        self._companies_collection = db["companies"]

    def _parse_csv(self, companies_csv):
        # TODO: run in executor due the possibility of high data volume
        companies = []
        reader = DictReader(StringIO(companies_csv), fieldnames=self.FIELDSNAME,
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
        return {
            "name": company['name'].upper(),
            "addressZip": company["addressZip"]
        }

    async def _save_company(self, company):
        # Update to not duplicate
        print(company)
        self._companies_collection.update_one(
            company,
            {"$set": company}, upsert=True)

    async def import_companies(self, companies_csv):
        companies = self._parse_csv(companies_csv)
        for company in companies:
            try:
                self._validate_company(company)
                normalized_company = self._normalize_company(company)
                await self._save_company(normalized_company)
            except ValueError:
                pass
        return True

    async def merge_companies(self, companies_csv):
        pass
