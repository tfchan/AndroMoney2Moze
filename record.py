import datetime
from enum import Enum
from dataclasses import dataclass

import pandas as pd


class RecordType(Enum):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    TRANSFER = 'Transfer'


@dataclass
class Record:
    from_account: str
    to_account: str
    from_amount: int
    to_amount: int
    from_currency: str
    to_currency: str
    categories: list[str]
    date: datetime.date
    time: datetime.time = None
    shop: str = None
    title: str = None
    detail: str = None
    project: str = None

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
