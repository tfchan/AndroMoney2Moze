import datetime
from enum import Enum

import pandas as pd


class RecordType(Enum):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    TRANSFER = 'Transfer'


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
        date = datetime.datetime.strptime(f"{record['Date']}", '%Y%m%d').date
        time = (datetime.datetime.strptime(f"{int(record['Time']):04}", '%H%M').time
                if pd.notna(record['Time']) else None)
        return cls(record['Expense(Transfer Out)'],
                   record['Income(Transfer In)'],
                   record['Amount'],
                   record['Amount'],
                   record['Currency'],
                   record['Currency'],
                   [record['Category'], record['Sub-Category']],
                   date,
                   time=time,
                   shop=record['Payee/Payer'],
                   detail=record['Remark'],
                   project=record['Project']
                   )
