import datetime
from enum import Enum
from dataclasses import dataclass, field

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
    record_type: RecordType = field(init=False)

    def __post_init__(self) -> None:
        if self.from_account and not self.to_account:
            self.record_type = RecordType.EXPENSE
        elif self.from_account and self.to_account:
            self.record_type = RecordType.TRANSFER
        elif self.to_account:
            self.record_type = RecordType.INCOME
        else:
            raise ValueError('Invalid record type. '
                             'Both from_account and to_account are None.')

    @classmethod
    def from_andromoney(cls, record: pd.Series) -> None:
        date = pd.to_datetime(record['Date'], '%Y%m%d').date()
        time = (pd.to_datetime(f"{int(record['Time']):04}", '%H%M').time()
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
