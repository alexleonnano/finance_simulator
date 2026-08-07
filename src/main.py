# Simulator for my mom's investment proposal from the asset management company.
from src.simulation import InvestmentAccount, plot_account

# Fund parameters
principal = 30000
time = 5
n = 12
rate = 0.1427

# Create the investment account and plot the growth
account = InvestmentAccount(principal, rate, time, n)
plot_account(account)