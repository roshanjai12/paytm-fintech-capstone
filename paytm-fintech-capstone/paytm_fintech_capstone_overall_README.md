# Overall Project Explanation — Paytm FinTech Capstone

The Paytm FinTech Capstone is an end-to-end FinTech analytics and decision-support project covering **payments, lending, investment advisory and financial risk management**.

The complete capstone is divided into three major projects:

- **Project 1 — Payments Fraud Analytics**
- **Project 2 — Credit Risk & Lending ML**
- **Project 3 — AI-Augmented FinTech Advisory & Blockchain Risk**

Together, the projects follow the workflow:

**Raw financial data → Data preparation → Analytical modelling → Risk identification → Financial decision-making → Visualization and reporting**

---

# Project 1 — Payments Fraud Analytics

Project 1 focuses on understanding and monitoring payment transactions from an operational and risk perspective.

The workflow covers **data generation, spreadsheet analysis, SQL fraud detection, Python reconciliation and dashboard creation**.

## Data Generation and Preparation

Payment and merchant datasets are prepared for analysis.

The payment data contains transaction-level information, while merchant reference data provides additional information for merchant-level analysis.

The data is then used across spreadsheet, SQL and Python workflows.

---

# Spreadsheet and Merchant Analysis

Google Sheets and Microsoft Excel are used for transaction cleaning, data inspection and merchant-level analysis.

The merchant workbook helps organize merchant information and identify where payment activity and risk may be concentrated.

This moves the analysis from individual transactions toward **merchant-level risk monitoring**.

---

# SQL Fraud Detection

Payment data is stored in SQLite and analysed using SQL.

Important fraud patterns include **burner accounts** and **transaction velocity**.

Burner-account analysis considers recently created accounts and their transaction behaviour.

Velocity attacks are identified as users with at least **3 transactions within a 10-minute window**.

The analysis groups transactions using:

- `user_id`
- Rounded/floored 10-minute transaction-time bucket

The objective is to identify the **8 seeded velocity-attack clusters**.

This demonstrates how transaction concentration and account behaviour can be used as fraud signals.

---

# Python Payment Reconciliation

Python is used to compare:

- `ledger.csv`
- `gateway_export.csv`

The reusable function:

`reconcile_payments(ledger_df, gateway_df)`

returns:

1. Transactions missing in the gateway
2. Transactions missing in the ledger
3. Amount mismatches
4. Status mismatches

Set operations on `transaction_id` identify missing or extra records, while Pandas merge operations compare matching transactions.

The results are checked against the seeded approximate rates:

- 5% missing
- 3% amount mismatch
- 2% extra
- 2% status mismatch

Reconciliation acts as an important **financial operations and control mechanism**.

---

# Four-Layer Analytics Dashboard

The dashboard provides a simple visual view of payment performance and risk.

## Headline Layer

The headline layer includes:

- Total GMV
- Overall success rate
- Reconciliation match rate
- Chargeback ratio

The match rate considers transactions present in both systems with identical amount and status.

The chargeback ratio is:

**Chargeback transactions / Total transactions**

---

## Trends Layer

The trends layer shows:

- Daily GMV
- Daily chargeback count

over the 30-day analysis period.

This helps identify changes in payment activity and chargeback behaviour over time.

---

## Breakdown Layer

The breakdown layer shows GMV by:

- Payment method
- Merchant category

Bar charts make comparisons between discrete categories easier and help identify major contributors to transaction value.

---

## Details Layer

The details layer shows the **top 10 merchants by transaction count**.

A merchant is flagged as high-risk when its chargeback ratio exceeds:

**1%**

The flag identifies merchants that may require further investigation.

---

# Overall Meaning of Project 1

Project 1 answers four main business questions:

**How much payment activity is happening?**

GMV, transaction counts and category breakdowns answer this.

**Where might fraud be occurring?**

SQL identifies patterns such as burner accounts and high transaction velocity.

**Are payment records consistent?**

Python reconciliation compares ledger and gateway records.

**Where should the business investigate?**

Merchant chargeback ratios and dashboard indicators help prioritize investigation.

Project 1 therefore demonstrates how raw payment transactions can become **operational monitoring, fraud detection and risk-based decision-making**.

---

# Project 2 — Credit Risk & Lending ML

Project 2 focuses on **credit risk and lending machine learning**.

The workflow covers credit-applicant data, preprocessing, classification models, ROC evaluation, risk-based pricing, anomaly detection and bias awareness.

---

# Credit Applicant Data

The project generates:

`credit_applicants.csv`

with **400 rows**.

The default rate is expected to remain within the required **15–25% range**.

The dataset also contains exactly **80 missing `credit_bureau_score` values**.

These missing values are used to evaluate thin-file handling.

---

# Thin-File Handling

The `is_thin_file` flag is created from the raw data **before imputation**.

The train/test split is performed before calculating the median credit score.

The median is calculated using only the training data and then applied to both training and testing sets.

Applicants are not simply dropped because of missing credit scores.

This prevents test-set information from leaking into the training process.

---

# Train/Test Split and Preprocessing

A stratified train/test split with:

`random_state = 42`

is used.

Preprocessing is fitted only on the training data and then applied to the test set.

This ensures that model evaluation represents performance on unseen applicants.

Both classifiers use the **same split** for fair comparison.

---

# Credit-Risk Classification

Two classification models are trained and evaluated.

The models are compared using the required evaluation metrics and ROC analysis.

The ROC visualization is saved as:

`roc_curve_comparison.png`

ROC analysis helps compare model performance across different classification thresholds rather than relying on a single cutoff.

---

# Risk-Based Pricing

Applicants are divided into at least **four risk tiers**.

The observed default rate should increase monotonically, or materially so, from the lowest-risk tier to the highest-risk tier.

This ensures that the risk segmentation has meaningful business interpretation for lending and pricing decisions.

---

# Behavioural Anomaly Detection

The project also generates:

`txn_behaviour.csv`

containing **265 rows** and **15 seeded anomalies**.

Isolation Forest is applied to standardized behavioural features.

The model's recall against the seeded `BTXNA*` anomalies is reported.

This provides a second risk signal beyond traditional credit characteristics.

---

# Bias Awareness and Governance

The project considers potential proxy variables such as:

- `employment_type`
- `monthly_income_inr`
- `credit_bureau_score`

These variables could potentially correlate with protected characteristics in a real-world environment.

A governance mechanism such as **maker-checker or human-in-the-loop review** is therefore considered before deployment, particularly for declined thin-file applicants.

---

# Final Model Recommendation

The final comparison considers the classifier metrics together with the Isolation Forest recall.

The recommendation should therefore consider not only model performance, but also **risk, interpretability and governance**.

---

# Overall Meaning of Project 2

Project 2 answers:

**Who is likely to default?**

Classification models address this.

**How should incomplete credit information be handled?**

The thin-file strategy addresses this.

**Can unusual behaviour be detected?**

Isolation Forest addresses this.

**Can meaningful risk tiers be created?**

Risk-based pricing addresses this.

**Could automated lending create fairness concerns?**

Bias-awareness and governance address this.

Project 2 therefore demonstrates:

**Credit data → Preprocessing → Modelling → Evaluation → Anomaly detection → Risk segmentation → Responsible deployment**

---

# Project 3 — AI-Augmented FinTech Advisory & Blockchain Risk

Project 3 focuses on **investment advisory, financial disclosure analysis, valuation and blockchain/crypto risk**.

The major components are:

- Portfolio advisory
- CAPM
- Structured disclosure extraction
- Multi-agent debate
- DCF valuation
- EV/EBITDA cross-check
- Blockchain/crypto risk analysis

---

# Stock Universe

The project uses six illustrative securities:

- PAYFIN
- PAYRETAIL
- PAYINFRA
- PAYGOLD
- PAYBOND
- PAYTECH

Each contains:

- Beta
- Analyst expected return
- Standard deviation

CAPM uses **beta**, not analyst expected return.

The model uses:

Risk-free rate = **7%**

Market return = **13%**

---

# Investor Profiles and Portfolio Advisory

Five investor profiles are processed using prescribed allocations.

### Conservative

PAYBOND, PAYGOLD and PAYRETAIL

### Moderate

PAYRETAIL, PAYINFRA and PAYGOLD

### Aggressive

PAYTECH, PAYFIN and PAYINFRA

Each selected security receives an equal weight of **1/3**.

---

# Think-Act-Observe Workflow

**Think**

The agent reads the investor profile and determines the prescribed allocation.

**Act**

It retrieves stock information using `get_stock_data(ticker)`.

**Observe**

It calculates CAPM expected return, portfolio return, variance and volatility.

If portfolio standard deviation exceeds **20%**, the recommendation is:

`ESCALATED_TO_HUMAN_ADVISOR`

This creates a simple human-in-the-loop control for higher-risk portfolios.

---

# Structured Disclosure Extraction

The function:

`extract_signals(snippet: str) -> dict`

returns:

- `risk_flags`
- `hedging_detected`
- `sentiment`

Risk flags include signals such as:

- Litigation
- Regulatory
- Customer concentration

Hedging language includes terms such as:

- Assuming
- Cautiously
- Visibility

Sentiment is classified as:

- Confident
- Cautious
- Neutral

The six disclosure snippets are processed into structured information for analysis.

---

# Multi-Agent Debate

The debate system contains:

- Bull agent
- Bear agent
- Synthesizer

The selected ticker was:

**PAYFIN**

The bull argument references its analyst expected return and beta.

The bear argument references its standard deviation.

The synthesizer combines both perspectives into a balanced **2–3 sentence** view.

This provides a structured way to consider both upside and downside risk.

---

# DCF Valuation

The DCF calculator estimates enterprise value using projected unlevered free cash flow.

The FCFF formula is:

**FCFF = EBIT × (1 − tax rate) + D&A − CapEx − ΔNWC**

The model projects five years of FCFF and calculates:

- Cost of equity
- WACC
- Terminal value
- Present value of FCFF
- Present value of terminal value
- Enterprise value

The base case uses:

Risk-free rate: **7%**

Market return: **13%**

Beta: **1.35**

Cost of equity: **15.10%**

After-tax cost of debt: **6.75%**

WACC: **12.60%**

Terminal growth: **3.00%**

The resulting DCF enterprise value was approximately:

**INR 1.357 billion**

---

# DCF Sensitivity Analysis

A **3 × 3 sensitivity table** varies:

WACC:

- 11.60%
- 12.60%
- 13.60%

Terminal growth:

- 2.00%
- 3.00%
- 4.00%

The minimum WACC-minus-growth spread was:

**7.60 percentage points**

The required self-check therefore passed.

---

# EV/EBITDA Cross-Check

An illustrative:

EBITDA = **INR 100 million**

EV/EBITDA multiple = **12.0x**

produced an EV/EBITDA enterprise value of:

**INR 1.2 billion**

Compared with the DCF enterprise value of:

**INR 1.357 billion**

the difference was approximately:

**11.57%**

The EV/EBITDA approach provides a market-multiple cross-check against the DCF valuation.

---

# Blockchain and Crypto Risk Analysis

The final component evaluates blockchain and crypto risks relevant to a hypothetical Paytm Money product.

The analysis considers:

- Stablecoin risk
- DeFi risk
- DAO governance risk
- Crypto asset-class suitability
- Social-engineering risks

Stablecoin analysis considers reserve, redemption and operational risks.

DeFi and DAO analysis considers smart-contract, liquidity, leverage and governance risks.

---

# Crypto as an Asset Class

The analysis considers:

- Lack of conventional cash flows
- High volatility
- Heavy-tailed returns
- Survivorship bias
- Transaction and custody risks
- Regulatory and operational uncertainty

The recommendation is designed around **risk-adjusted portfolio construction and retail suitability**, rather than adding crypto simply for diversification.

---

# T.A.N.G. Fraud Framework

The project applies the T.A.N.G. framework:

**Temptation  
Authority  
Need  
Greed**

Two social-engineering risks are analysed:

### Authority

Fraudsters may impersonate trusted institutions or employees.

A real-time defence can detect unusual payments, new beneficiaries, device changes and abnormal behaviour before requiring trusted-channel verification.

### Greed

Fraudsters may use fake investment opportunities or unusually high returns to manipulate customers.

A real-time defence can detect unusual investment-related payments and trigger warnings or additional confirmation before payment release.

---

# How the Three Projects Connect

The three projects represent different parts of a modern FinTech platform.

**Project 1 asks:**

What is happening in the payment system?

**Project 2 asks:**

What is the financial risk associated with applicants and their behaviour?

**Project 3 asks:**

How can financial decisions be supported using quantitative models and structured risk analysis?

Together, they represent:

**Payments → Lending → Wealth/Investment**

---

# Overall Technical Workflow

The capstone uses different tools for different stages.

**Google Sheets and Microsoft Excel** are used for spreadsheet and merchant analysis.

**Google Colab** is used for notebook-based execution.

**Python and Pandas** are used for data processing, reconciliation, modelling and financial calculations.

**SQL and SQLite** are used for transaction querying and fraud analysis.

**Matplotlib** is used for analytical charts and dashboard images.

**Looker Studio** is used for interactive visualization where applicable.

**Git and GitHub** are used for version control and repository submission.

---

# Overall Business Meaning

The main takeaway is that **FinTech decision-making cannot depend on a single model or metric**.

A payment platform needs:

- Transaction monitoring
- Fraud detection
- Reconciliation
- Merchant risk analysis

A lending platform needs:

- Credit-risk modelling
- Anomaly detection
- Risk segmentation
- Governance

A wealth platform needs:

- Portfolio analysis
- Disclosure analysis
- Valuation
- Blockchain and crypto risk assessment

The project therefore connects analytical results to practical business decisions:

- Suspicious transaction → Investigate
- Reconciliation mismatch → Resolve
- High-chargeback merchant → Monitor
- High-risk borrower → Assess
- Unusual behaviour → Investigate
- High portfolio volatility → Human escalation
- Risky disclosure → Flag
- Uncertain valuation → Cross-check
- Crypto exposure → Assess suitability
- Social-engineering threat → Introduce controls

---

# Final Summary

The Paytm FinTech Capstone demonstrates an end-to-end approach to **data analysis, financial modelling, machine learning, fraud detection and risk management**.

**Project 1 — Payments Fraud Analytics** demonstrates payment monitoring, fraud detection, reconciliation and merchant risk analysis.

**Project 2 — Credit Risk & Lending ML** demonstrates credit-risk modelling, anomaly detection, risk segmentation and responsible lending deployment.

**Project 3 — AI-Augmented FinTech Advisory & Blockchain Risk** demonstrates portfolio analysis, CAPM, disclosure extraction, multi-agent debate, DCF valuation and blockchain/crypto risk analysis.

The common theme across all three projects is:

**Risk-aware financial decision-making.**

The capstone therefore demonstrates how **data analysis, statistical modelling, machine learning, financial mathematics, fraud detection, business intelligence and risk governance** can work together to support real-world FinTech operations and financial decision-making.
