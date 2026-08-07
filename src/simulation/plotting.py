"""
Plotting and info-box formatting, kept separate from the simulation math
so both InvestmentAccount and Portfolio can reuse the same rendering code.

Amounts are labeled using each account's own `currency` (see
InvestmentAccount/Portfolio) rather than a hardcoded symbol, so a EUR fund
and a USD fund each render with the right symbol without extra plumbing
at the call site.
"""
import matplotlib.pyplot as plt

# ISO currency code -> display symbol. Unknown codes fall back to
# "<CODE> " (e.g. "CHF 1,234.5") so an unmapped currency still renders
# sensibly instead of raising.
CURRENCY_SYMBOLS = {
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
}


def _currency_symbol(currency):
    return CURRENCY_SYMBOLS.get(currency, f"{currency} ")


def _format_amount(value, currency):
    # Mapped symbols (€, $, £) and unmapped codes ("CHF ") both read
    # naturally placed directly before the number.
    return f"{_currency_symbol(currency)}{value:,.2f}"


def _format_duration_or_balance(account, with_interest, label):
    years = account.years_until_depleted(with_interest=with_interest)
    suffix = "con intereses" if with_interest else "sin intereses"
    if years is not None:
        return f"Duración de {label} {suffix}: {years} años \n"
    balance = account.final_balance() if with_interest else account.final_savings_balance()
    return f"Balance final {label} {suffix}: {_format_amount(balance, account.currency)} \n"


def plot_account(account, title=None):
    """Plots a single InvestmentAccount: compound-interest curve vs.
    no-interest savings curve, with an info box summarizing the results.
    Currency symbol/labels follow account.currency (EUR by default)."""
    months_years = account.months_axis_years()
    symbol = _currency_symbol(account.currency)

    fig, ax1 = plt.subplots()

    ax1.plot(months_years, account.balances, linewidth=2, label='Interés compuesto')
    ax1.yaxis.set_major_formatter(f'{symbol}{{x:,.1f}}')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)

    ax1.set_title(title or f'Rendimiento de la cuenta durante {account.time} años')
    ax1.set_xlabel('Años')
    ax1.set_ylabel(f'Monto ({symbol.strip()})')
    ax1.grid(True, alpha=0.3)

    info_text = f"Inicial: {_format_amount(account.principal, account.currency)}\n"
    info_text += f"Tasa de interés: {account.rate * 100:.1f}%\n"
    info_text += f"Compuesto: {account.n}x por año\n"
    info_text += f"Interes acumulado: {_format_amount(account.total_interest_earned(), account.currency)}\n"
    if account.monthly_contribution > 0:
        info_text += f"Contribución mensual: {_format_amount(account.monthly_contribution, account.currency)}\n"
    if account.monthly_withdrawal > 0:
        info_text += f"Retiro mensual: {_format_amount(account.monthly_withdrawal, account.currency)}\n"
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
    info box summarizing each account and the portfolio as a whole.

    Each account keeps its own currency (see InvestmentAccount.currency).
    If both accounts share a currency, the y-axis is labeled with it as
    normal. If they differ (e.g. a EUR fund vs. a USD fund plotted
    together), the axis stays generic — values are plotted in their raw
    native units, not converted — and each line/summary is labeled with
    its own currency instead so the mismatch is obvious rather than
    implying a shared scale."""
    acc1, acc2 = portfolio.account_1, portfolio.account_2
    months_years = acc1.months_axis_years()
    same_currency = acc1.currency == acc2.currency

    fig, ax1 = plt.subplots()

    label1_suffix = "" if same_currency else f" ({acc1.currency})"
    label2_suffix = "" if same_currency else f" ({acc2.currency})"
    ax1.plot(months_years, acc1.balances, linewidth=2,
              label=f'Cuenta {portfolio.ratio:.0f}% - Interés compuesto{label1_suffix}')
    ax1.plot(months_years, acc2.balances, linewidth=2,
              label=f'Cuenta {100 - portfolio.ratio:.0f}% - Interés compuesto{label2_suffix}')

    if same_currency:
        symbol = _currency_symbol(acc1.currency)
        ax1.yaxis.set_major_formatter(f'{symbol}{{x:,.1f}}')
        ax1.set_ylabel(f'Monto ({symbol.strip()})')
    else:
        ax1.yaxis.set_major_formatter('{x:,.1f}')
        ax1.set_ylabel('Monto (moneda nativa de cada cuenta, ver leyenda)')
    ax1.yaxis.set_tick_params(which='major', labelleft=True, labelright=False)

    ax1.set_title(f'Rendimiento de las cuentas durante {portfolio.time} años')
    ax1.set_xlabel('Años')
    ax1.grid(True, alpha=0.3)

    info_text = f"Rendimiento de las cuentas durante {portfolio.time} años\n"
    info_text += f"Retiros mensuales en cuenta 1: {_format_amount(acc1.monthly_withdrawal, acc1.currency)}\n"
    info_text += f"Retiros mensuales en cuenta 2: {_format_amount(acc2.monthly_withdrawal, acc2.currency)}\n"
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
              label=f'Cuenta {portfolio.ratio:.0f}% - Ahorros sin interés{label1_suffix}')
    ax1.plot(months_years, acc2.savings_balance, color='green', linewidth=2,
              label=f'Cuenta {100 - portfolio.ratio:.0f}% - Ahorros sin interés{label2_suffix}')

    ax1.axhline(y=acc1.principal, color='gray', linestyle='--', alpha=0.5)
    ax1.axhline(y=acc2.principal, color='gray', linestyle='--', alpha=0.5)

    ax1.legend()
    plt.show()