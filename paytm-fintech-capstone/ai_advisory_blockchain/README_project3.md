# AI-Augmented FinTech Advisory & Blockchain Risk

## 1. Project Overview

This project builds a lightweight AI-assisted advisory toolkit for a Paytm Money-style FinTech platform. It covers portfolio allocation using CAPM and portfolio variance, structured extraction from company disclosures, a three-agent bull/bear debate, DCF valuation, and a written blockchain/crypto risk appendix.

The graded implementation uses deterministic `MOCK_LLM` logic. No LLM API, signup, API key, network call, embeddings, vector database, or LangGraph pipeline is required for the graded baseline.

---

## 2. Project Structure

```text
ai_advisory_blockchain/
├── stock_universe.py
├── investor_profiles.py
├── disclosure_snippets.py
├── advisory_agent.py
├── extract_disclosure.py
├── debate.py
├── dcf_calculator.py
├── blockchain_risk_note.md
└── README.md
```

### File Purpose

- `stock_universe.py` — prescribed stock data, risk-free rate, and market return.
- `investor_profiles.py` — five investor profiles.
- `disclosure_snippets.py` — six exact disclosure snippets.
- `advisory_agent.py` — portfolio allocation, CAPM return, variance, and escalation logic.
- `extract_disclosure.py` — structured disclosure-risk extraction.
- `debate.py` — bull, bear, and synthesizer agents.
- `dcf_calculator.py` — five-year DCF valuation and sensitivity analysis.
- `blockchain_risk_note.md` — written blockchain/crypto risk appendix.
- `README.md` — project explanation, assumptions, interpretations, and run notes.

---

# Part A — Portfolio Advisory Agent

## 3. Agent Structure

The advisory agent follows the required **Think → Act → Observe** pattern.

- **Think:** reads an investor profile and determines the prescribed stock allocation from its risk-tolerance tier.
- **Act:** calls `get_stock_data(ticker)` to retrieve beta, analyst expected return, and standard deviation from the local stock universe.
- **Observe:** calculates CAPM expected return, portfolio expected return, portfolio variance, and portfolio standard deviation.

The agent then checks whether portfolio standard deviation exceeds the required 20% escalation threshold.

---

## 4. Prescribed Allocation Rules

The allocation is fixed by the task and is not a free-choice mapping.

| Risk Tolerance | Equal-Weight Allocation |
|---|---|
| Conservative | `PAYBOND`, `PAYGOLD`, `PAYRETAIL` |
| Moderate | `PAYRETAIL`, `PAYINFRA`, `PAYGOLD` |
| Aggressive | `PAYTECH`, `PAYFIN`, `PAYINFRA` |

Each selected stock receives an equal weight of **1/3**.

### Interpretation

Using a prescribed allocation makes the portfolio recommendations deterministic and reproducible. It also ensures that differences between investor profiles come from the defined risk tiers rather than arbitrary stock selection.

---

## 5. CAPM Expected Return

The CAPM formula used is:

```text
E(Ri) = Rf + βi × (E(Rm) − Rf)
```

Only the stock's **beta** is used in the CAPM calculation.

The `analyst_expected_return` field is kept as a separate illustrative reference and is **not** substituted into the CAPM calculation.

### Interpretation

CAPM provides a consistent risk-adjusted expected return based on systematic risk. Keeping analyst expectations separate prevents the advisory calculation from mixing two different return assumptions.

---

## 6. Portfolio Variance and Volatility

Portfolio variance is calculated using:

```text
Var(Rp) = Σ wi²σi² + 2Σ(i<j) wi wj Cov(Ri,Rj)
```

Pairwise covariance is calculated as:

```text
Cov(Ri,Rj) = ρ × σi × σj
```

The required pairwise correlation is:

```text
ρ = 0.3
```

Portfolio standard deviation is the square root of portfolio variance.

### Interpretation

Variance combines the individual stock risks with the effect of relationships between stocks. The correlation assumption prevents the model from treating all assets as completely independent.

---

## 7. Human-in-the-Loop Escalation

If portfolio standard deviation is greater than **20%**, the recommendation is not automatically finalized.

Instead, the system returns:

```text
ESCALATED_TO_HUMAN_ADVISOR
```

with the calculated portfolio numbers attached.

The deterministic expected pattern is:

- `INV01` — approximately **8.44%**, no escalation.
- `INV02` and `INV04` — approximately **12.57%**, no escalation.
- `INV03` and `INV05` — approximately **20.58%**, escalation required.

### Interpretation

The escalation rule prevents the automated system from finalizing recommendations when portfolio volatility crosses the defined risk boundary. This provides a simple human-in-the-loop control for higher-risk cases.

---

## 8. Mock LLM Narrative

Only the final narrative sentence is gated by `MOCK_LLM`.

In the graded baseline, the narrative is generated from a deterministic template using the computed investor ID, allocation, expected return, and volatility.

All five investor profiles are run and their results are recorded.

The optional `MOCK_LLM=0` extension can use an actual LLM, but it is not required for the graded submission.

---

# Part B — Structured Disclosure Extraction

## 9. Disclosure Signal Extraction

`extract_disclosure.py` implements:

```python
extract_signals(snippet: str) -> dict
```

The function returns:

```text
{
    "risk_flags": [...],
    "hedging_detected": bool,
    "sentiment": "confident" | "cautious" | "neutral"
}
```

In mock mode, keyword/regex rules are used.

### Risk Flags

The extraction rules identify risk-related language such as:

- `litigation`
- `regulatory`
- `customer concentration`

### Hedging

Hedging is detected from phrases containing terms such as:

- `assuming`
- `cautiously`
- `visibility`

### Sentiment

- `confident` — triggered by terms such as `confident` or `approved`.
- `cautious` — triggered by a hedging phrase.
- `neutral` — used when neither condition applies.

### Interpretation

Structured extraction converts unstructured disclosure text into consistent fields that can be analysed programmatically. The deterministic rules make the graded baseline reproducible without requiring an external LLM.

---

## 10. Disclosure Results

The extractor is run against all six committed disclosure snippets.

The required checks include:

- `doc_02` is identified with a `litigation`-style risk flag.
- At least one hedging snippet returns `hedging_detected = True`.
- `doc_05`, the board-approval snippet, is classified as `confident`.

The recorded run also identifies the regulatory signal in `doc_06`.

---

# Part C — Multi-Agent Debate Demo

## 11. Three-Agent Debate

`debate.py` implements three agents for one selected ticker:

1. **Bull agent**
2. **Bear agent**
3. **Synthesizer**

The selected ticker in the recorded run is:

```text
PAYFIN
```

### Bull Agent

The bull argument references the ticker's actual:

- analyst expected return
- beta

It presents the positive risk-adjusted case.

### Bear Agent

The bear argument references the ticker's actual:

- standard deviation

It presents volatility as the main risk.

### Synthesizer

The synthesizer combines the two views into a balanced **2–3 sentence** summary.

### Interpretation

The debate structure forces the recommendation to consider both upside and downside rather than relying on a single narrative. Using the actual seed values keeps the arguments tied to the project's data.

---

# Part D — DCF Valuation Calculator

## 12. DCF Method

`dcf_calculator.py` implements a discounted-cash-flow valuation for a hypothetical Paytm business line.

The model uses unlevered Free Cash Flow to the Firm:

```text
FCFF = EBIT × (1 − tax rate) + D&A − CapEx − ΔNet Working Capital
```

The model projects five years of FCFF with a growth rate that fades toward a lower terminal growth rate.

---

## 13. WACC and CAPM

Cost of equity is calculated using:

```text
R_e = R_f + β(E(R_m) − R_f)
```

The WACC combines:

- cost of equity
- after-tax cost of debt
- illustrative capital-structure weights

The recorded base-case output is:

```text
Risk-free rate:       7.00%
Market return:       13.00%
Beta:                 1.35
Cost of equity:      15.10%
After-tax debt cost:  6.75%
WACC:                12.60%
Terminal growth:      3.00%
```

### Interpretation

WACC represents the discount rate used to convert future unlevered cash flows into present value. CAPM provides the equity-return component while the debt component reflects the cost of financing.

---

## 14. FCFF Projection and Terminal Value

The recorded five-year FCFF projection uses declining growth:

```text
Year 1: 12%
Year 2: 10%
Year 3:  8%
Year 4:  7%
Year 5:  6%
```

The recorded results include:

```text
Terminal FCFF:       INR 155,439,479
Terminal Value:      INR 1,620,004,989
PV of Terminal Value: INR 895,201,550
PV of projected FCFF: INR 461,837,773
```

The resulting DCF enterprise value is:

```text
INR 1,357,039,323
```

### Interpretation

The DCF approach values the business from its expected future cash generation. Discounting the cash flows accounts for the time value of money and the risk represented by WACC.

---

## 15. DCF Sensitivity Analysis

A **3 × 3 sensitivity table** is produced by varying:

- WACC by ±1 percentage point.
- Terminal growth by ±1 percentage point.

Recorded WACC values:

```text
11.60%
12.60%
13.60%
```

Recorded terminal-growth values:

```text
2.00%
3.00%
4.00%
```

The minimum WACC minus terminal-growth spread is:

```text
7.60 percentage points
```

The required self-check therefore passes because WACC exceeds terminal growth by at least 1 percentage point in every sensitivity cell.

### Interpretation

Sensitivity analysis shows how valuation changes when the two major DCF assumptions move. The self-check also prevents an invalid situation where terminal growth approaches or exceeds the discount rate.

---

## 16. EV/EBITDA Cross-Check

An illustrative EBITDA of:

```text
INR 100,000,000
```

and an EV/EBITDA multiple of:

```text
12.0x
```

are used.

The cross-check produces:

```text
DCF Enterprise Value:       INR 1,357,039,323
EV/EBITDA Enterprise Value: INR 1,200,000,000
Difference:                INR -157,039,323
Difference vs DCF:         -11.57%
```

### Interpretation

The DCF estimates enterprise value from projected free cash flows, WACC, and terminal growth. The EV/EBITDA method provides a market-multiple cross-check, so the difference reflects the assumptions and valuation methodology used.

---

# Part E — Blockchain / Crypto Risk Analysis Appendix

## 17. Stablecoin and DeFi/DAO Risk

The written appendix evaluates the risks that a hypothetical Paytm Crypto Insights watchlist would need to address.

Key areas include:

- Stablecoin reserve and redemption risk.
- Deviation from the intended stable value.
- Operational, cyber, and financial-integrity risks.
- DeFi smart-contract and oracle risks.
- Leverage, liquidity, and liquidation risks.
- DAO governance concentration.

### Interpretation

Stablecoins, DeFi products, and DAOs should not be presented as automatically safe or equivalent to regulated deposits or traditional investment products. A retail-facing product should clearly distinguish the type of stablecoin, reserve quality, redemption mechanism, protocol risk, leverage, and governance concentration.

---

## 18. Crypto Asset-Class Recommendation

The project recommends a **0% strategic allocation to cryptocurrency for the standard retail portfolio**.

The recommendation considers:

- Lack of conventional intrinsic cash flows such as dividends.
- Heavy-tailed and asymmetric return behaviour.
- Low or negative correlation not being sufficient by itself.
- Survivorship bias.
- High transaction and custody risks.
- Regulatory and operational uncertainty.
- Potentially large drawdowns.

A future speculative allocation, if permitted, should be separately labelled, tightly capped, and accompanied by explicit risk disclosures.

### Interpretation

The recommendation prioritizes capital preservation and transparent risk-adjusted portfolio construction rather than adding crypto simply for diversification.

---

## 19. T.A.N.G. Social-Engineering Analysis

Two social-engineering risks are selected as particularly relevant to a UPI/wallet + lending + wealth platform.

### Authority

Fraudsters may impersonate bank employees, regulators, police, platform representatives, or other trusted authorities.

**Real-time defence:** detect unusual high-value payments, new beneficiaries, device changes, and abnormal customer behaviour. Suspicious transactions can be paused or stepped up for verification through a trusted, pre-registered channel.

### Greed

Fraudsters may exploit the customer's desire for unusually high or guaranteed returns through fake investment, crypto, lending, or wealth opportunities.

**Real-time defence:** detect unusual investment-related payments, first-time beneficiaries, sudden high-value transfers, rapid account funding, or behaviour inconsistent with the customer's history. A targeted warning and cooling-off/confirmation step can be triggered before payment release.

### Interpretation

The T.A.N.G. analysis treats social engineering as a human-behaviour risk as well as a technology risk. Real-time behavioural monitoring and intervention can reduce losses when customers are manipulated into authorising suspicious payments.

---

# 20. Overall Project Interpretation

The project combines deterministic financial modelling with lightweight AI-agent patterns.

The portfolio agent demonstrates risk-based allocation and human escalation. The disclosure extractor converts company text into structured risk signals, while the multi-agent debate demonstrates how opposing financial views can be combined into a balanced summary.

The DCF component provides a fundamental valuation perspective, and the blockchain appendix extends the analysis to crypto, DeFi, DAO, and social-engineering risks. Together, the components demonstrate how FinTech advisory systems can combine quantitative analysis, structured information extraction, controlled automation, and human oversight.

---

# 21. Reproducibility and Run Notes

The graded baseline should be run with:

```text
MOCK_LLM left at its default setting
```

This keeps all required LLM-related behaviour deterministic and avoids external API/network dependencies.

The project should be executed in the following order:

```text
1. Verify seed data
2. Run advisory agent for all 5 investors
3. Run disclosure extraction for all 6 snippets
4. Run the 3-agent debate
5. Run the DCF calculator
6. Verify the 3 × 3 sensitivity self-check
7. Run the EV/EBITDA cross-check
8. Include blockchain_risk_note.md
9. Review this README before submission
```

---

# 22. Final Acceptance Checklist

- [x] Stock universe contains 6 prescribed stocks.
- [x] Five investor profiles are processed.
- [x] Prescribed allocations are followed exactly.
- [x] CAPM uses beta, risk-free rate, and market return.
- [x] Portfolio variance uses the required ρ = 0.3.
- [x] 20% volatility escalation rule is implemented.
- [x] `MOCK_LLM` baseline is deterministic.
- [x] All 6 disclosure snippets are processed.
- [x] Risk flags, hedging, and sentiment are extracted.
- [x] Three-agent debate is completed.
- [x] Bull, bear, and synthesizer outputs reference actual ticker values.
- [x] Five-year FCFF projection is completed.
- [x] Terminal value and present values are calculated.
- [x] WACC and CAPM calculations are completed.
- [x] 3 × 3 DCF sensitivity table is produced.
- [x] WACC-versus-terminal-growth self-check passes.
- [x] EV/EBITDA cross-check is completed.
- [x] `blockchain_risk_note.md` contains all three required sections.
- [x] README records the important assumptions and interpretations.
- [x] All required project files are included in the repository.

---

## 23. Submission Files

The final `ai_advisory_blockchain` folder should contain:

```text
stock_universe.py
investor_profiles.py
disclosure_snippets.py
advisory_agent.py
extract_disclosure.py
debate.py
dcf_calculator.py
blockchain_risk_note.md
README.md
```

The README is intentionally kept concise while documenting the important assumptions, decisions, outputs, and interpretations required for reproducibility and submission.
