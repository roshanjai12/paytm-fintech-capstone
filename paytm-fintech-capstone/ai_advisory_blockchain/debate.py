from stock_universe import STOCK_UNIVERSE


def run_debate(ticker):
    data = STOCK_UNIVERSE[ticker]

    bull = (
        f"Bull view: {ticker} has an analyst expected return of "
        f"{data['analyst_expected_return']:.1%} and a beta of {data['beta']:.2f}, "
        f"suggesting attractive risk-adjusted upside."
    )

    bear = (
        f"Bear view: {ticker} has a standard deviation of "
        f"{data['std_dev']:.1%}, indicating meaningful volatility "
        f"and therefore material downside risk."
    )

    synthesizer = (
        f"Balanced view: {ticker} offers an analyst expected return of "
        f"{data['analyst_expected_return']:.1%} with a beta of {data['beta']:.2f}, "
        f"but its standard deviation of {data['std_dev']:.1%} represents "
        f"a meaningful risk that should be considered."
    )

    return {
        "ticker": ticker,
        "bull": bull,
        "bear": bear,
        "synthesizer": synthesizer,
    }


if __name__ == "__main__":
    ticker = "PAYFIN"
    result = run_debate(ticker)

    print("=" * 70)
    print("MULTI-AGENT DEBATE")
    print("=" * 70)
    print(f"\nTicker: {ticker}")
    print("\nBULL AGENT")
    print(result["bull"])
    print("\nBEAR AGENT")
    print(result["bear"])
    print("\nSYNTHESIZER")
    print(result["synthesizer"])
