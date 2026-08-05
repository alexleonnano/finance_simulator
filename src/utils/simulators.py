# Here are gonna be the main functions used to handle the compound interest calculations and other financial tools.
# Work in progress, more functions will be added in the future.
import matplotlib.pyplot as plt
import numpy as np

def simulate_investment_growth(principal, rate, time, n, monthly_contribution=0, monthly_withdrawal=0):
    """
    Simulate the growth of an investment over time with monthly contributions/withdrawals.

    :param principal: The initial amount of money (the principal).
    :param rate: The annual interest rate (as a decimal, e.g., 0.05 for 5%).
    :param time: The time the money is invested for (in years).
    :param n: The number of times that interest is compounded per year.
    :param monthly_contribution: Amount added to the account each month (default: 0).
    :param monthly_withdrawal: Amount taken from the account each month (default: 0).
    """
    if monthly_contribution > 0 and monthly_withdrawal > 0:
        print("Warning: Both contribution and withdrawal are set. Consider using only one.")
    
    # Calculate monthly rate
    monthly_rate = rate / 12
    
    # Determine number of months
    total_months = int(time * 12)
    
    # Initialize lists
    months = list(range(total_months + 1))
    balances = []
    savings_balance = []  # Start with the initial principal
    
    # Simulate Compound Interest with Contributions and Withdrawals
    current_balance = principal
    
    for month in range(total_months + 1):
        # Add the balance for this month
        balances.append(current_balance)
        
        # Apply interest for this month (only if not the last month)
        if month < total_months:
            # Monthly interest
            current_balance *= (1 + monthly_rate)
            
            # Add monthly contribution
            if monthly_contribution > 0:
                current_balance += monthly_contribution
            
            # Subtract monthly withdrawal
            if monthly_withdrawal > 0:
                current_balance -= monthly_withdrawal
                # Ensure balance doesn't go negative
                if current_balance < 0:
                    current_balance = 0
                    print(f"Warning: El balance se volvera negativo en el mes {month+1}. Set to 0.")

    # Simulate Savings Balance with Contributions and Withdrawals (without interest)
    savings_balance = [principal]
    for month in range(total_months):
        next_balance = savings_balance[-1]

        # Add monthly contribution
        if monthly_contribution > 0:
            next_balance += monthly_contribution

        # Subtract monthly withdrawal
        if monthly_withdrawal > 0:
            next_balance -= monthly_withdrawal

        # Ensure balance doesn't go negative
        if next_balance < 0:
            next_balance = 0
            print(f"Warning: El balance se volvera negativo en el mes {month+1}. Set to 0.")

        savings_balance.append(next_balance)

    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot the investment growth
    ax1.plot([month/12 for month in months], balances, linewidth=2, label='Interés compuesto')
    ax1.yaxis.set_major_formatter('€{x:,.1f}')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)
    
    # Labels and title
    ax1.set_title(f'Rendimiento de la cuenta durante {time} años')
    ax1.set_xlabel('Años')
    ax1.set_ylabel('Monto (€)')
    ax1.grid(True, alpha=0.3)
    
    # Add info box
    info_text = f"Inicial: {principal:,.2f} €\n"
    info_text += f"Tasa de interés: {rate*100:.1f}%\n"
    info_text += f"Compuesto: {n}x por año\n"
    info_text += f"Interes acumulado: {balances[-1] - principal - sum(monthly_contribution for _ in range(total_months)) + sum(monthly_withdrawal for _ in range(total_months)):,.2f} €\n"
    if monthly_contribution > 0:
        info_text += f"Contribución mensual: {monthly_contribution:,.2f} €\n"
    if monthly_withdrawal > 0:
        info_text += f"Retiro mensual: {monthly_withdrawal:,.2f} €\n"
    if balances[-1] == 0:
        info_text += f"Duración de ahorros en inversión: {next((i for i, x in enumerate(balances) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final con intereses: {balances[-1]:,.2f} € \n"
    if savings_balance[-1] == 0:
        info_text += f"Duración de los ahorros sin inversión: {next((i for i, x in enumerate(savings_balance) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final sin intereses: {savings_balance[-1]:,.2f} € \n"

    
    # Place text box in the plot
    ax1.text(0.02, 0.35, info_text, transform=ax1.transAxes, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Add horizontal line at initial investment
    ax1.axhline(y=principal, color='gray', linestyle='--', alpha=0.5)

    # Plot the savings balance
    ax1.plot([month/12 for month in months], savings_balance, color='orange', linewidth=2, label='Ahorros sin interés')

    ax1.legend()
    plt.show()
    
    # Return the final balance for potential further on other calculations.
    return balances[-1]

def query_fund_info(fund_file):
    """
    Query information from a real fund using a CSV file.
    """
    pass

def simulate_fund():
    """
    Simulate a real fund with the given parameters, work in progress.
    """

    pass

def simulate_multiple_accounts(principal, ratio, rate_1, rate_2, time, n, monthly_contribution_1=0, monthly_contribution_2=0, monthly_withdrawal_1=0, monthly_withdrawal_2=0):
    """
    Simulate multiple accounts with different parameters, work in progress.
    """
    if not (0 <= ratio <= 100):
        raise ValueError("Ratio must be between 0 and 100.")

    principal_1 = principal * ratio / 100
    principal_2 = principal * (100 - ratio) / 100

    # Calculate monthly rate for both accounts
    monthly_rate_1 = rate_1 / 12
    monthly_rate_2 = rate_2 / 12

    # Determine number of months
    total_months = int(time * 12)

    # Initialize lists for both accounts
    months = list(range(total_months + 1))

    balances_1 = []
    balances_2 = []

    savings_balance_1 = [principal_1]
    savings_balance_2 = [principal_2]

    # Simulate Compound Interest with Contributions and Withdrawals for both accounts
    current_balance_1 = principal_1
    current_balance_2 = principal_2

    for month in range(total_months + 1):
        # Add the balance for this month
        balances_1.append(current_balance_1)
        balances_2.append(current_balance_2)

        # Apply interest for this month (only if not the last month)
        if month < total_months:
            # Monthly interest
            current_balance_1 *= (1 + monthly_rate_1)
            current_balance_2 *= (1 + monthly_rate_2)

            # Add monthly contribution
            if monthly_contribution_1 > 0:
                current_balance_1 += monthly_contribution_1
            if monthly_contribution_2 > 0:
                current_balance_2 += monthly_contribution_2

            # Subtract monthly withdrawal
            if monthly_withdrawal_1 > 0:
                current_balance_1 -= monthly_withdrawal_1
                # Ensure balance doesn't go negative
                if current_balance_1 < 0:
                    current_balance_1 = 0
                    print(f"Warning: El balance de la cuenta 1 se volvera negativo en el mes {month+1}. Set to 0.")
            if monthly_withdrawal_2 > 0:
                current_balance_2 -= monthly_withdrawal_2
                # Ensure balance doesn't go negative
                if current_balance_2 < 0:
                    current_balance_2 = 0
                    print(f"Warning: El balance de la cuenta 2 se volvera negativo en el mes {month+1}. Set to 0.")

    # Simulate savings balance with contributions and withdrawals (without interest) for both accounts
    for month in range(total_months):
        next_balance_1 = savings_balance_1[-1]
        next_balance_2 = savings_balance_2[-1]

        # Add monthly contribution
        if monthly_contribution_1 > 0:
            next_balance_1 += monthly_contribution_1
        if monthly_contribution_2 > 0:
            next_balance_2 += monthly_contribution_2

        # Subtract monthly withdrawal
        if monthly_withdrawal_1 > 0:
            next_balance_1 -= monthly_withdrawal_1
        if monthly_withdrawal_2 > 0:
            next_balance_2 -= monthly_withdrawal_2

        # Ensure balance doesn't go negative
        if next_balance_1 < 0:
            next_balance_1 = 0
            print(f"Warning: El balance de la cuenta 1 se volvera negativo en el mes {month+1}. Set to 0.")
        if next_balance_2 < 0:
            next_balance_2 = 0
            print(f"Warning: El balance de la cuenta 2 se volvera negativo en el mes {month+1}. Set to 0.")

        savings_balance_1.append(next_balance_1)
        savings_balance_2.append(next_balance_2)

    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot the investment growth for both accounts
    ax1.plot([month/12 for month in months], balances_1, linewidth=2, label=f'Cuenta {principal_1/principal*100:.0f}% - Interés compuesto')
    ax1.plot([month/12 for month in months], balances_2, linewidth=2, label=f'Cuenta {principal_2/principal*100:.0f}% - Interés compuesto')

    # Format y-axis as currency
    ax1.yaxis.set_major_formatter('€{x:,.1f}')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)

    # Labels and title
    ax1.set_title(f'Rendimiento de las cuentas durante {time} años')
    ax1.set_xlabel('Años')
    ax1.set_ylabel('Monto (€)')
    ax1.grid(True, alpha=0.3)

    # Add info box
    info_text = f"Rendimiento de las cuentas durante {time} años\n"
    info_text += f"Retiros mensuales en cuenta 1: {monthly_withdrawal_1:,.2f} €\n"
    info_text += f"Retiros mensuales en cuenta 2: {monthly_withdrawal_2:,.2f} €\n"
    if balances_1[-1] == 0:
        info_text += f"Duración de la cuenta 1 en inversión: {next((i for i, x in enumerate(balances_1) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final cuenta 1 con intereses: {balances_1[-1]:,.2f} € \n"
    if savings_balance_1[-1] == 0:
        info_text += f"Duración de la cuenta 1 sin inversión: {next((i for i, x in enumerate(savings_balance_1) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final cuenta 1 sin intereses: {savings_balance_1[-1]:,.2f} € \n"
    if balances_2[-1] == 0:
        info_text += f"Duración de la cuenta 2 en inversión: {next((i for i, x in enumerate(balances_2) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final cuenta 2 con intereses: {balances_2[-1]:,.2f} € \n"
    if savings_balance_2[-1] == 0:
        info_text += f"Duración de la cuenta 2 sin inversión: {next((i for i, x in enumerate(savings_balance_2) if x == 0))/12} años \n"
    else:
        info_text += f"Balance final cuenta 2 sin intereses: {savings_balance_2[-1]:,.2f} € \n"
    info_text += f"Duración del portafolio con inversión: {next((i for i, x in enumerate(balances_1) if x == 0))/12 + next((i for i, x in enumerate(balances_2) if x == 0))/12} años \n"
    info_text += f"Duración del portafolio sin inversión: {next((i for i, x in enumerate(savings_balance_1) if x == 0))/12 + next((i for i, x in enumerate(savings_balance_2) if x == 0))/12} años \n"

    # Place text box in the plot
    ax1.text(0.67, 0.9, info_text, transform=ax1.transAxes, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Plot the savings balance for both accounts
    ax1.plot([month/12 for month in months], savings_balance_1, color='orange', linewidth=2, label=f'Cuenta {principal_1/principal*100:.0f}% - Ahorros sin interés')
    ax1.plot([month/12 for month in months], savings_balance_2, color='green', linewidth=2, label=f'Cuenta {principal_2/principal*100:.0f}% - Ahorros sin interés')

    # Add horizontal line at initial investment for both accounts
    ax1.axhline(y=principal_1, color='gray', linestyle='--', alpha=0.5)
    ax1.axhline(y=principal_2, color='gray', linestyle='--', alpha=0.5)

    ax1.legend()
    plt.show()

    return balances_1[-1], balances_2[-1]