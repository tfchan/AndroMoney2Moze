import datetime

import pandas as pd


class Record:
    def __init__(self,
                 from_account: str,
                 to_account: str,
                 from_amount: int,
                 to_amount: int,
                 from_currency: str,
                 to_currency: str,
                 categories: list[str],
                 date: datetime.date,
                 time: datetime.time = None,
                 shop: str = None,
                 title: str = None,
                 detail: str = None,
                 project: str = None
                 ) -> None:
        self.from_account = from_account
        self.to_account = to_account
        self.from_amount = from_amount
        self.to_amount = to_amount
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.categories = categories
        self.date = date
        self.time = time
        self.shop = shop
        self.title = title
        self.detail = detail
        self.project = project

    @classmethod
    def from_andromoney(cls, record: pd.Series) -> None:
        return cls(record['Expense(Transfer Out)'],
                   record['Income(Transfer In)'],
                   record['Amount'],
                   record['Amount'],
                   record['Currency'],
                   record['Currency'],
                   [record['Category'], record['Sub-Category']],
                   datetime.datetime.strptime(record['Date'], '%Y%m%d').date,
                   time=datetime.datetime.strptime(record['Time'], '%H%M').time,
                   shop=record['Payee/Payer'],
                   detail=record['Remark'],
                   project=record['Project']
                   )
