import click
import pandas as pd

import record

DEFAULT_ANDROMONEY_FILE = 'AndroMoney - AndroMoney.csv'
DEFAULT_MOZE_FILE = 'MOZE.csv'


def read_andromoney(filename: click.Path) -> pd.DataFrame:
    return pd.read_csv(filename, skiprows=1)


def fix_account_init_record(andromoney: pd.DataFrame,
                            main_category: str = 'INIT',
                            sub_category: str = 'INIT'
                            ) -> pd.DataFrame:
    andromoney = andromoney.copy()
    is_system_row = andromoney["Category"] == 'SYSTEM'
    andromoney.loc[is_system_row, "Category"] = main_category
    andromoney.loc[is_system_row, "Sub-Category"] = sub_category
    andromoney.loc[is_system_row, "Date"] = pd.NA
    andromoney.loc[is_system_row, "Time"] = 0
    andromoney["Date"] = andromoney["Date"].ffill().bfill()

    return andromoney


def andromoney_to_moze(andromoney: pd.DataFrame) -> pd.DataFrame:
    andromoney = fix_account_init_record(andromoney)
    andromoney = andromoney.sort_values(["Date", "Time"], ignore_index=True)
    records = (andromoney
               .apply(record.Record.from_andromoney, axis=1)
               .map(lambda record: record.to_moze()))
    moze = pd.concat(record for record in records)
    return moze


def write_moze(moze: pd.DataFrame, filename: str):
    moze.to_csv(filename, index=False)


@click.command()
@click.option('-i',
              '--input',
              default=DEFAULT_ANDROMONEY_FILE,
              type=click.Path(exists=True, dir_okay=False),
              show_default=True,
              help='Filename of AndroMoney formated csv')
@click.option('-o',
              '--output',
              default=DEFAULT_MOZE_FILE,
              type=click.Path(dir_okay=False),
              show_default=True,
              help='Filename of Moze formated csv')
def andromoney2moze(input: click.Path, output: click.Path):
    """A tool for converting AndroMoney format into Moze one."""
    andromoney = read_andromoney(input)
    moze = andromoney_to_moze(andromoney)
    write_moze(moze, output)


if __name__ == '__main__':
    andromoney2moze()
