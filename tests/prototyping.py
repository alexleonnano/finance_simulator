# Load tools
from src.utils.simulators import *

# Split the principal into two accounts and set the investment time and compound frequency
principal = 150000
ratio = 60
time = 40
n = 12

# Setup Accounts
# Account 1
rate_1 = 0.06
monthly_contribution_1 = 0
monthly_withdrawal_1 = 500

# Account 2
rate_2 = 0.04
monthly_contribution_2 = 0
monthly_withdrawal_2 = 500

# Run simulation
simulate_multiple_accounts(principal, ratio, rate_1, rate_2, time, n, monthly_contribution_1, monthly_contribution_2, monthly_withdrawal_1, monthly_withdrawal_2)

#simulate_investment_growth(principal, rate, time, n, monthly_contribution = 0, monthly_withdrawal = 700)