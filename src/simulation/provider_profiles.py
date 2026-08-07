"""
Known fund provider export formats.

Each bank/provider formats their NAV export differently: column names,
delimiter, decimal separator, date format, header row offset, encoding.
FundProviderProfile bundles those settings; PROVIDER_PROFILES holds one
entry per provider we've already figured out.

Add a new provider by adding an entry here once you've inspected its file
— load_fund_prices() can also take these settings ad hoc via keyword
arguments for a provider that isn't listed here yet.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FundProviderProfile:
    """Describes how a specific fund provider formats their NAV exports."""
    name: str
    date_column: str
    nav_column: str
    date_format: str = "%d/%m/%Y"
    header_row: int = 0
    sep: str = ","          # CSV only; ignored for Excel files
    decimal: str = "."
    encoding: str = "utf-8"  # CSV only; ignored for Excel files


PROVIDER_PROFILES = {
    "santalucia": FundProviderProfile(
        name="santalucia",
        date_column="FEC_VALORACION",
        nav_column="VALOR_LIQUIDATIVO",
        date_format="%d/%m/%Y",
        header_row=0,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    ),
    "santander": FundProviderProfile(
        name="santander",
        date_column="Fecha",
        nav_column="Valor liquidativo",
        date_format="%d/%m/%Y",
        header_row=1,  # a title row (fund name + ISIN) precedes the real header
        decimal=",",
    ),
}
