from math import sqrt
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

ALLOCATION_RULES = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
    "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
    "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
}

CORRELATION = 0.3
ESCALATION_THRESHOLD = 0.20


def get_stock_data(ticker):
    return STOCK_UNIVERSE[ticker]


def capm_expected_return(beta):
    return RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)


def portfolio_metrics(tickers):
    weights = [1 / 3] * len(tickers)
    returns = [capm_expected_return(get_stock_data(t)["beta"]) for t in tickers]
    stds = [get_stock_data(t)["std_dev"] for t in tickers]

    portfolio_return = sum(w * r for w, r in zip(weights, returns))

    variance = sum(
        (weights[i] ** 2) * (stds[i] ** 2)
        for i in range(len(tickers))
    )

    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            covariance = CORRELATION * stds[i] * stds[j]
            variance += 2 * weights[i] * weights[j] * covariance

    return portfolio_return, variance, sqrt(variance)


def build_recommendation(investor):
    tickers = ALLOCATION_RULES[investor["risk_tolerance"]]
    portfolio_return, variance, std_dev = portfolio_metrics(tickers)

    decision = (
        "ESCALATED_TO_HUMAN_ADVISOR"
        if std_dev > ESCALATION_THRESHOLD
        else "FINALIZED"
    )

    recommendation = (
        f"For {investor['risk_tolerance']} investor {investor['investor_id']}, "
        f"we recommend an allocation across {', '.join(tickers)} with an "
        f"expected portfolio return of {portfolio_return:.1%} and volatility "
        f"of {std_dev:.1%}."
    )

    return {
        "investor_id": investor["investor_id"],
        "risk_tolerance": investor["risk_tolerance"],
        "tickers": tickers,
        "portfolio_expected_return": portfolio_return,
        "portfolio_variance": variance,
        "portfolio_std_dev": std_dev,
        "escalation": decision,
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("PORTFOLIO ADVISORY AGENT")
    print("=" * 70)

    for investor in INVESTOR_PROFILES:
        result = build_recommendation(investor)
        print(f"\nInvestor: {result['investor_id']}")
        print(f"Risk: {result['risk_tolerance']}")
        print(f"Allocation: {result['tickers']}")
        print(f"Expected return: {result['portfolio_expected_return']:.2%}")
        print(f"Portfolio volatility: {result['portfolio_std_dev']:.2%}")
        print(f"Decision: {result['escalation']}")
        print(f"Recommendation: {result['recommendation']}")
