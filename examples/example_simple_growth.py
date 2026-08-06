# Load tools
from src.simulation import InvestmentAccount, plot_account

# Fund parameters
principal = 150000
time = 40
n = 12
rate = 0.06

# Create the investment account and plot the growth
account = InvestmentAccount(principal, rate, time, n, monthly_contribution=100)
plot_account(account)