"""
Plotting and info-box formatting, kept separate from the simulation math
so both InvestmentAccount and Portfolio can reuse the same rendering code.
"""
import matplotlib.pyplot as plt


def _format_duration_or_balance(account, with_interest, label):
    years = account.years_until_depleted(with_interest=with_interest)
    if years is not None:
        suffix = "con intereses" if with_interest else "sin intereses"
        return f"Duración de {label} {suffix}: {years} años \n"
    balance = account.final_balance() if with_interest else account.final_savings_balance()
    suffix = "con intereses" if with_interest else "sin intereses"
    return f"Balance final {label} {suffix}: {balance:,.2f} € \n"


def plot_account(account, title=None):
    """Plots a single InvestmentAccount: compound-interest curve vs.
    no-interest savings curve, with an info box summarizing the results."""
    months_years = account.months_axis_years()

    fig, ax1 = plt.subplots()

    ax1.plot(months_years, account.balances, linewidth=2, label='Interés compuesto')
    ax1.yaxis.set_major_formatter('€{x:,.1f}')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)

    ax1.set_title(title or f'Rendimiento de la cuenta durante {account.time} años')
    ax1.set_xlabel('Años')
    ax1.set_ylabel('Monto (€)')
    ax1.grid(True, alpha=0.3)

    info_text = f"Inicial: {account.principal:,.2f} €\n"
    info_text += f"Tasa de interés: {account.rate * 100:.1f}%\n"
    info_text += f"Compuesto: {account.n}x por año\n"
    info_text += f"Interes acumulado: {account.total_interest_earned():,.2f} €\n"
    if account.monthly_contribution > 0:
        info_text += f"Contribución mensual: {account.monthly_contribution:,.2f} €\n"
    if account.monthly_withdrawal > 0:
        info_text += f"Retiro mensual: {account.monthly_withdrawal:,.2f} €\n"
    info_text += _format_duration_or_balance(account, with_interest=True, label="ahorros en inversión")
    info_text += _format_duration_or_balance(account, with_interest=False, label="ahorros sin inversión")

    ax1.text(0.02, 0.35, info_text, transform=ax1.transAxes, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax1.axhline(y=account.principal, color='gray', linestyle='--', alpha=0.5)
    ax1.plot(months_years, account.savings_balance, color='orange', linewidth=2,
              label='Ahorros sin interés')

    ax1.legend()
    plt.show()


def plot_portfolio(portfolio):
    """Plots both accounts in a Portfolio side by side, with a combined
    info box summarizing each account and the portfolio as a whole."""
    acc1, acc2 = portfolio.account_1, portfolio.account_2
    months_years = acc1.months_axis_years()

    fig, ax1 = plt.subplots()

    ax1.plot(months_years, acc1.balances, linewidth=2,
              label=f'Cuenta {portfolio.ratio:.0f}% - Interés compuesto')
    ax1.plot(months_years, acc2.balances, linewidth=2,
              label=f'Cuenta {100 - portfolio.ratio:.0f}% - Interés compuesto')

    ax1.yaxis.set_major_formatter('€{x:,.1f}')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)

    ax1.set_title(f'Rendimiento de las cuentas durante {portfolio.time} años')
    ax1.set_xlabel('Años')
    ax1.set_ylabel('Monto (€)')
    ax1.grid(True, alpha=0.3)

    info_text = f"Rendimiento de las cuentas durante {portfolio.time} años\n"
    info_text += f"Retiros mensuales en cuenta 1: {acc1.monthly_withdrawal:,.2f} €\n"
    info_text += f"Retiros mensuales en cuenta 2: {acc2.monthly_withdrawal:,.2f} €\n"
    info_text += _format_duration_or_balance(acc1, with_interest=True, label="cuenta 1")
    info_text += _format_duration_or_balance(acc1, with_interest=False, label="cuenta 1")
    info_text += _format_duration_or_balance(acc2, with_interest=True, label="cuenta 2")
    info_text += _format_duration_or_balance(acc2, with_interest=False, label="cuenta 2")

    portfolio_years_invested = portfolio.years_until_depleted(with_interest=True)
    portfolio_years_savings = portfolio.years_until_depleted(with_interest=False)
    if portfolio_years_invested is not None:
        info_text += f"Duración del portafolio con inversión: {portfolio_years_invested} años \n"
    if portfolio_years_savings is not None:
        info_text += f"Duración del portafolio sin inversión: {portfolio_years_savings} años \n"

    ax1.text(0.67, 0.9, info_text, transform=ax1.transAxes, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax1.plot(months_years, acc1.savings_balance, color='orange', linewidth=2,
              label=f'Cuenta {portfolio.ratio:.0f}% - Ahorros sin interés')
    ax1.plot(months_years, acc2.savings_balance, color='green', linewidth=2,
              label=f'Cuenta {100 - portfolio.ratio:.0f}% - Ahorros sin interés')

    ax1.axhline(y=acc1.principal, color='gray', linestyle='--', alpha=0.5)
    ax1.axhline(y=acc2.principal, color='gray', linestyle='--', alpha=0.5)

    ax1.legend()
    plt.show()
