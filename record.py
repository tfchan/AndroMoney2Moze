from typing import Union

import pandas as pd


class Record:
    def __init__(self, record: Union[pd.Series, pd.DataFrame], format: str):
        try:
            init_func = getattr(self, f'__from_{format}')
        except AttributeError:
            raise Exception(f'Importing {format} record is not supported.')
        else:
            init_func(record)

    def __from_andromoney():
        pass
