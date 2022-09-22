import click
import pandas as pd

DEFAULT_ANDROMONEY_FILE = 'AndroMoney - AndroMoney.csv'
DEFAULT_MOZE_FILE = 'MOZE.csv'


def read_andromoney(filename: click.Path) -> pd.DataFrame:
    return pd.read_csv(filename, skiprows=1)


def _andromoney2moze(andromoney: pd.DataFrame) -> pd.DataFrame:
    pass


def write_moze(moze: pd.DataFrame):
    pass


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
    moze = _andromoney2moze(andromoney)
    write_moze(moze)


if __name__ == '__main__':
    andromoney2moze()
