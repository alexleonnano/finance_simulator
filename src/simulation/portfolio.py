"""
Compares two InvestmentAccounts split from the same pool of money —
useful for weighing different withdrawal/investment strategies against
each other (e.g. retirement drawdown scenarios).
"""
from .accounts import InvestmentAccount


class Portfolio:
    """
    Splits a single principal into two accounts under a given ratio, each
    with its own rate/contribution/withdrawal, and simulates both.

    :param principal: Total initial amount of money.
    :param ratio: Percentage split between the two accounts (0-100).
        A ratio of 60 means account_1 gets 60% and account_2 gets 40%.
    :param rate_1, rate_2: Annual interest rate for each account (decimal).
    :param time: Investment horizon in years, shared by both accounts.
    :param n: Compounding frequency per year (see InvestmentAccount note).
    :param monthly_contribution_1, monthly_contribution_2: Monthly deposits.
    :param monthly_withdrawal_1, monthly_withdrawal_2: Monthly withdrawals.
    """

    def __init__(self, principal, ratio, rate_1, rate_2, time, n,
                 monthly_contribution_1=0, monthly_contribution_2=0,
                 monthly_withdrawal_1=0, monthly_withdrawal_2=0):
        if not (0 <= ratio <= 100):
            raise ValueError("Ratio must be between 0 and 100.")

        self.principal = principal
        self.ratio = ratio
        self.time = time

        principal_1 = principal * ratio / 100
        principal_2 = principal * (100 - ratio) / 100

        self.account_1 = InvestmentAccount(
            principal_1, rate_1, time, n,
            monthly_contribution_1, monthly_withdrawal_1, label="Cuenta 1")
        self.account_2 = InvestmentAccount(
            principal_2, rate_2, time, n,
            monthly_contribution_2, monthly_withdrawal_2, label="Cuenta 2")

    @property
    def accounts(self):
        return [self.account_1, self.account_2]

    def years_until_depleted(self, with_interest=True):
        """
        Combined portfolio duration: sum of each account's own depletion
        time. Returns None if either account never runs out.
        """
        years = [acc.years_until_depleted(with_interest) for acc in self.accounts]
        if any(y is None for y in years):
            return None
        return sum(years)
