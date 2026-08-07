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

    # Currency is constant for a given fund, so it travels as metadata
    # (df.attrs) rather than as a repeated column. Falls back to "EUR" if
    # the provider has no currency_column configured, or the raw file
    # doesn't carry it.
    clean.attrs["currency"] = _extract_currency(df, profile, file_path)

    return clean


def _extract_currency(raw_df, profile, file_path):
    """Reads the fund's ISO currency code from the raw (pre-clean) DataFrame,
    per the provider's currency_column. Returns 'EUR' if unconfigured."""
    if profile.currency_column is None:
        return "EUR"
    if profile.currency_column not in raw_df.columns:
        raise ValueError(
            f"Configured currency_column '{profile.currency_column}' not found in "
            f"{file_path}. Available columns: {list(raw_df.columns)}"
        )
    values = raw_df[profile.currency_column].dropna().unique()
    if len(values) == 0:
        return "EUR"
    if len(values) > 1:
        raise ValueError(
            f"Expected a single currency in {file_path}, found {list(values)} in "
            f"column '{profile.currency_column}'."
        )
    return str(values[0]).strip().upper()