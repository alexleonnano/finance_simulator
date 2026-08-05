# Load tools
from src.utils.simulators import *

# Split the principal into two accounts and set the investment time and compound frequency
principal = 150000
time = 40
n = 12
rate = 0.06

simulate_investment_growth(principal, rate, time, n, monthly_contribution = 100, monthly_withdrawal = 0)