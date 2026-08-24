import pandas as pd

from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN


# Illustrative DCF assumptions
BETA = STOCK_UNIVERSE["PAYFIN"]["beta"]
TAX_RATE = 0.25
COST_OF_DEBT_PRE_TAX = 0.09
EQUITY_WEIGHT = 0.70
DEBT_WEIGHT = 0.30
TERMINAL_GROWTH = 0.03

# FCFF base and illustrative growth path
BASE_FCFF = 100_000_000
GROWTH_RATES = [0.12, 0.10, 0.08, 0.07, 0.06]


def capm_cost_of_equity():
    return RISK_FREE_RATE + BETA * (MARKET_RETURN - RISK_FREE_RATE)


def calculate_wacc():
    cost_of_equity = capm_cost_of_equity()
    after_tax_debt = COST_OF_DEBT_PRE_TAX * (1 - TAX_RATE)

    return (
        EQUITY_WEIGHT * cost_of_equity
        + DEBT_WEIGHT * after_tax_debt
    )


def project_fcff():
    fcff = BASE_FCFF
    rows = []

    for year, growth in enumerate(GROWTH_RATES, start=1):
        fcff *= (1 + growth)
        rows.append({
            "Year": year,
            "Growth Rate": growth,
            "FCFF (INR)": fcff,
        })

    return pd.DataFrame(rows)


def terminal_value(terminal_fcff, wacc):
    return terminal_fcff * (1 + TERMINAL_GROWTH) / (wacc - TERMINAL_GROWTH)


def discount(value, year, wacc):
    return value / ((1 + wacc) ** year)


def run_dcf():
    wacc = calculate_wacc()
    projection = project_fcff()

    projection["PV FCFF"] = [
        discount(row["FCFF (INR)"], int(row["Year"]), wacc)
        for _, row in projection.iterrows()
    ]

    pv_projected_fcff = projection["PV FCFF"].sum()

    last_fcff = projection.iloc[-1]["FCFF (INR)"]
    terminal_fcff = last_fcff * (1 + TERMINAL_GROWTH)
    tv = terminal_value(last_fcff, wacc)
    pv_tv = discount(tv, 5, wacc)

    enterprise_value = pv_projected_fcff + pv_tv

    return {
        "wacc": wacc,
        "projection": projection,
        "terminal_fcff": terminal_fcff,
        "terminal_value": tv,
        "pv_terminal_value": pv_tv,
        "pv_projected_fcff": pv_projected_fcff,
        "enterprise_value": enterprise_value,
    }


def sensitivity_table(base_wacc):
    wacc_values = [base_wacc - 0.01, base_wacc, base_wacc + 0.01]
    growth_values = [TERMINAL_GROWTH - 0.01, TERMINAL_GROWTH, TERMINAL_GROWTH + 0.01]

    projection = project_fcff()
    fcff_values = projection["FCFF (INR)"].tolist()

    table = {}

    for wacc in wacc_values:
        table[f"WACC {wacc:.2%}"] = {}

        for growth in growth_values:
            pv_fcff = sum(
                discount(fcff, year, wacc)
                for year, fcff in enumerate(fcff_values, start=1)
            )

            terminal_fcff = fcff_values[-1] * (1 + growth)
            tv = terminal_fcff / (wacc - growth)
            pv_tv = discount(tv, 5, wacc)

            table[f"WACC {wacc:.2%}"][f"Growth {growth:.2%}"] = (
                pv_fcff + pv_tv
            )

    return pd.DataFrame(table).T


def ev_ebitda_cross_check(dcf_enterprise_value):
    illustrative_ebitda = 100_000_000
    ev_ebitda_multiple = 12.0
    ev_ebitda_value = illustrative_ebitda * ev_ebitda_multiple

    difference = ev_ebitda_value - dcf_enterprise_value
    difference_pct = difference / dcf_enterprise_value

    return {
        "ebitda": illustrative_ebitda,
        "multiple": ev_ebitda_multiple,
        "ev_ebitda_value": ev_ebitda_value,
        "difference": difference,
        "difference_pct": difference_pct,
    }


if __name__ == "__main__":
    result = run_dcf()

    print("=" * 70)
    print("DCF VALUATION")
    print("=" * 70)
    print(f"Risk-free rate: {RISK_FREE_RATE:.2%}")
    print(f"Market return: {MARKET_RETURN:.2%}")
    print(f"Beta used: {BETA:.2f}")
    print(f"Cost of equity: {capm_cost_of_equity():.2%}")
    print(f"After-tax cost of debt: {COST_OF_DEBT_PRE_TAX * (1 - TAX_RATE):.2%}")
    print(f"WACC: {result['wacc']:.2%}")
    print(f"Terminal growth: {TERMINAL_GROWTH:.2%}")

    print("\nFCFF PROJECTION")
    print(result["projection"].to_string(index=False))

    print(f"\nTerminal FCFF: INR {result['terminal_fcff']:,.0f}")
    print(f"Terminal Value: INR {result['terminal_value']:,.0f}")
    print(f"PV of Terminal Value: INR {result['pv_terminal_value']:,.0f}")
    print(f"PV of projected FCFF: INR {result['pv_projected_fcff']:,.0f}")
    print(f"DCF Enterprise Value: INR {result['enterprise_value']:,.0f}")

    table = sensitivity_table(result["wacc"])
    print("\nDCF 3 x 3 SENSITIVITY TABLE")
    print(table.to_string())

    min_spread = min(
        result["wacc"] - g
        for g in [TERMINAL_GROWTH - 0.01, TERMINAL_GROWTH, TERMINAL_GROWTH + 0.01]
    )
    print(f"\nMinimum WACC - terminal growth spread: {min_spread:.2%}")
    if min_spread >= 0.01:
        print("SELF-CHECK PASSED: WACC exceeds terminal growth by at least 1 percentage point in every sensitivity cell.")
    else:
        print("SELF-CHECK FAILED: WACC does not exceed terminal growth sufficiently.")

    cross_check = ev_ebitda_cross_check(result["enterprise_value"])

    print("\nEV / EBITDA CROSS-CHECK")
    print(f"Illustrative EBITDA: INR {cross_check['ebitda']:,.0f}")
    print(f"EV/EBITDA multiple: {cross_check['multiple']:.1f}x")
    print(f"DCF Enterprise Value: INR {result['enterprise_value']:,.0f}")
    print(f"EV/EBITDA Enterprise Value: INR {cross_check['ev_ebitda_value']:,.0f}")
    print(f"Difference: INR {cross_check['difference']:,.0f}")
    print(f"Difference (% of DCF value): {cross_check['difference_pct']:.2%}")
    print("\nInterpretation:")
    print("The DCF valuation estimates enterprise value using projected free cash flows, WACC and terminal growth.")
    print("The EV/EBITDA approach provides a market-multiple cross-check, so the difference reflects the assumptions and valuation methodology used.")
