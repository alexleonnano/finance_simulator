import pandas as pd

def load_fund_data(csv_path, date_col = "date", nav_column = "nav"):
    """
    Load fund data from a CSV file.

    Parameters:
    csv_path (str): The path to the CSV file.
    date_col (str): The name of the column containing dates.
    nav_column (str): The name of the column containing NAV values.

    Returns:
    pd.DataFrame: The loaded fund data.

    WORK IN PROGRESS
    """
