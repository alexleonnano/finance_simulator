"""
Core simulation unit: a single account earning compound interest, with
optional monthly contributions or withdrawals.
"""


class InvestmentAccount:
    """
    Simulates one account's balance over time, both with compound interest
    and as a plain no-interest savings comparison.

    :param principal: Initial amount of money.
    :param rate: Annual interest rate as a decimal (e.g. 0.05 for 5%).
    :param time: Investment horizon in years.
    :param n: Compounding frequency per year. Currently informational only —
        the simulation compounds monthly regardless of n (see note in _simulate).
    :param monthly_contribution: Amount added each month (default: 0).
    :param monthly_withdrawal: Amount withdrawn each month (default: 0).
    :param label: Human-readable name, used in warnings and plot legends.
    """

    def __init__(self, principal, rate, time, n=12, monthly_contribution=0,
                 monthly_withdrawal=0, label="Cuenta"):
        if monthly_contribution > 0 and monthly_withdrawal > 0:
            print(f"Warning ({label}): Both contribution and withdrawal are set. "
                  "Consider using only one.")

        self.principal = principal
        self.rate = rate
        self.time = time
        self.n = n
        self.monthly_contribution = monthly_contribution
        self.monthly_withdrawal = monthly_withdrawal
        self.label = label

        # Filled in by _simulate()
        self.balances = None
        self.savings_balance = None
        self._simulate()

    @property
    def total_months(self):
        return int(self.time * 12)

    def _simulate(self):
        """Runs both the compound-interest series and the no-interest
        savings series, storing them on self."""
        # NOTE: mirrors the original behavior — always compounds monthly,
        # regardless of self.n. If you want true n-times-per-year compounding
        # this is the place to change it.
        monthly_rate = self.rate / 12
        total_months = self.total_months

        balances = []
        current_balance = self.principal
        for month in range(total_months + 1):
            balances.append(current_balance)
            if month < total_months:
                current_balance *= (1 + monthly_rate)
                if self.monthly_contribution > 0:
                    current_balance += self.monthly_contribution
                if self.monthly_withdrawal > 0:
                    current_balance -= self.monthly_withdrawal
                    if current_balance < 0:
                        current_balance = 0
                        print(f"Warning: {self.label} balance se volvera negativo "
                              f"en el mes {month + 1}. Set to 0.")

        savings_balance = [self.principal]
        for month in range(total_months):
            next_balance = savings_balance[-1]
            if self.monthly_contribution > 0:
                next_balance += self.monthly_contribution
            if self.monthly_withdrawal > 0:
                next_balance -= self.monthly_withdrawal
            if next_balance < 0:
                next_balance = 0
                print(f"Warning: {self.label} savings balance se volvera negativo "
                      f"en el mes {month + 1}. Set to 0.")
            savings_balance.append(next_balance)

        self.balances = balances
        self.savings_balance = savings_balance

    def months_axis_years(self):
        """X-axis values (in years) matching balances/savings_balance."""
        return [month / 12 for month in range(self.total_months + 1)]

    def final_balance(self):
        return self.balances[-1]

    def final_savings_balance(self):
        return self.savings_balance[-1]

    def total_interest_earned(self):
        total_contributions = self.monthly_contribution * self.total_months
        total_withdrawals = self.monthly_withdrawal * self.total_months
        return self.final_balance() - self.principal - total_contributions + total_withdrawals

    def years_until_depleted(self, with_interest=True):
        """
        Returns the number of years until the account balance hits 0,
        or None if it never does within the simulated period.

        :param with_interest: If True, checks the compound-interest series;
            if False, checks the plain no-interest savings series.
        """
        series = self.balances if with_interest else self.savings_balance
        for i, balance in enumerate(series):
            if balance == 0:
                return i / 12
        return None
