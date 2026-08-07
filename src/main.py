import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.simulation import InvestmentAccount
acc = InvestmentAccount(30000, 0.1427, 5, 12)  # exactly as in main.py, no currency arg
print('currency defaults to:', acc.currency)