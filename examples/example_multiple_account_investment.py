# Load tools
from src.simulation import InvestmentAccount, Portfolio, plot_portfolio

# Setup paramters for the portfolio
principal = 150000
ratio = 60
rate_1 = 0.05
rate_2 = 0.03
monthly_contribution_1 = 100
monthly_withdrawal_2 = 500
time = 40
n = 12

# Create the portfolio and plot the growth
inv = Portfolio(principal, ratio, rate_1, rate_2, time, n, monthly_contribution_1, monthly_withdrawal_2)
plot_portfolio(inv)