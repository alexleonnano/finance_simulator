"""
Loading and cleaning historical fund price data from CSV or Excel exports.

See provider_profiles.py for the known per-provider format settings this
uses.
"""
from dataclasses import replace
from pathlib import Path

import pandas as pd

from src.simulation.provider_profiles import FundProviderProfile, PROVIDER_PROFILES


def load_fund_prices(file_path, provider=None, **overrides):
    """
    Reads a fund's historical NAV data from a CSV or Excel export and
    returns a clean DataFrame with standardized columns: 'date' (datetime64)
    and 'nav' (float), sorted ascending by date, with unrelated columns
    dropped.

    :param file_path: Path to the fund's CSV or XLSX export.
    :param provider: Optional key into PROVIDER_PROFILES (e.g. "santalucia",
        "santander") to use that provider's known format.
    :param overrides: Any FundProviderProfile field (date_column, nav_column,
        date_format, header_row, sep, decimal, encoding) — override the
        chosen provider's values, or supply them all directly if `provider`
        is omitted (e.g. for a provider that isn't profiled yet).
    :return: DataFrame with columns ['date', 'nav'], sorted ascending by date.
    """
    if provider is not None:
        if provider not in PROVIDER_PROFILES:
            raise ValueError(
                f"Unknown provider '{provider}'. Known providers: {list(PROVIDER_PROFILES)}"
            )
        profile = replace(PROVIDER_PROFILES[provider], **overrides)
    else:
        try:
            profile = FundProviderProfile(name="custom", **overrides)
        except TypeError as e:
            raise ValueError(
                "No `provider` given, so date_column and nav_column (at least) "
                f"must be passed directly. {e}"
            ) from e

    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(file_path, sep=profile.sep, decimal=profile.decimal,
                          encoding=profile.encoding, header=profile.header_row)
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(file_path, header=profile.header_row)
    else:
        raise ValueError(f"Unsupported file type '{suffix}'. Expected .csv, .xlsx, or .xls.")

    missing_columns = [c for c in (profile.date_column, profile.nav_column) if c not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Expected column(s) {missing_columns} not found in {file_path}. "
            f"Available columns: {list(df.columns)}"
        )

    clean = df[[profile.date_column, profile.nav_column]].rename(
        columns={profile.date_column: "date", profile.nav_column: "nav"}
    )

    clean["date"] = pd.to_datetime(clean["date"], format=profile.date_format)

    # Excel's read_csv-style `decimal=` option doesn't exist for read_excel,
    # so NAV values from .xlsx files may still be text like "189,97" here.
    if not pd.api.types.is_numeric_dtype(clean["nav"]):
        clean["nav"] = clean["nav"].astype(str).str.replace(profile.decimal, ".", regex=False)
    clean["nav"] = clean["nav"].astype(float)

    clean = clean.dropna(subset=["date", "nav"])
    clean = clean.drop_duplicates(subset="date")
    clean = clean.sort_values("date").reset_index(drop=True)

    return clean
