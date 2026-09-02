# Paytm FinTech Capstone Project

## Student Information

**Student Name:** Bonthu Roshan Jaisimha\
**Student ID:** bitsom_ftai_2601087\
**Public GitHub Repository:** *(add the final public GitHub repository
link here)*

------------------------------------------------------------------------

## 1. Project Overview

This repository contains the complete Paytm FinTech Capstone project. It
is divided into three parts:

1.  **Payments Fraud Analytics**
2.  **Credit Risk & Lending ML**
3.  **AI Advisory & Blockchain Risk**

Together, the three parts cover payment analytics, fraud detection, SQL,
Python reconciliation, machine learning, credit-risk analysis, financial
valuation, investment advisory, and blockchain-related risk analysis.

The project is designed so that the data, code, outputs, and written
explanations can be inspected directly from the repository. All monetary
values used in the project are in **Indian Rupees (INR)**.

------------------------------------------------------------------------

# 2. Repository Structure

``` text
paytm-fintech-capstone/
│
├── README.md
├── requirements.txt
│
├── payments_fraud_analytics/
│   ├── Part 1 - Data Generation/
│   ├── merchant_workbook.xlsx
│   ├── Part_B_SQL_Fraud_Detection.ipynb
│   ├── Part_C_Python_Payment_Reconciliation.ipynb
│   ├── Part_C_Python_Payment_Reconciliation.py
│   ├── Part_D_Analytics_Dashboard.ipynb
│   ├── paytm_payments.db
│   ├── D1_headline_scorecards.png
│   ├── D2_trends.png
│   ├── D3_gmv_by_category.png
│   ├── D3_gmv_by_payment_method.png
│   ├── D4_merchant_details.png
│   └── README.md
│
├── credit_risk_lending_ml/
│   ├── generate_data/
│   ├── generate_data.py
│   ├── credit_applicants.csv
│   ├── txn_behaviour.csv
│   ├── credit_risk_lending_ml.ipynb
│   ├── roc_curve_comparison.png
│   └── README.md
│
└── ai_advisory_blockchain/
    ├── stock_universe.py
    ├── investor_profiles.py
    ├── disclosure_snippets.py
    ├── advisory_agent.py
    ├── extract_disclosure.py
    ├── debate.py
    ├── dcf_calculator.py
    ├── blockchain_risk_note.md
    ├── README.md
    └── ai_advisory_blockchain.ipynb
```

> The exact file list should be kept in sync with the final files
> committed to GitHub.

------------------------------------------------------------------------

# 3. Tools and Technologies Used

-   **Microsoft Excel** -- spreadsheet analysis, lookup formulas, nested
    IF logic and pivot-table analysis.
-   **Google Sheets** -- spreadsheet-based analysis where applicable.
-   **Google Colab** -- running and sharing Python notebooks.
-   **Python** -- data processing, reconciliation, modelling and
    financial calculations.
-   **Pandas** -- data cleaning, transformation and tabular analysis.
-   **NumPy** -- numerical calculations.
-   **Matplotlib** -- analytical charts and model evaluation plots.
-   **Scikit-learn** -- preprocessing, classification and anomaly
    detection.
-   **SQL** -- transaction and fraud analysis.
-   **SQLite** -- local database for payment analytics.
-   **Looker Studio** -- interactive business dashboarding.
-   **Git** -- version control.
-   **GitHub** -- final repository hosting.

------------------------------------------------------------------------

# 4. Setup

## Python Version

Python 3.10+ is recommended.

## Install Dependencies

This project uses **one consolidated `requirements.txt` at the
repository root**.

From the repository root:

``` bash
pip install -r requirements.txt
```

The consolidated requirements file should include the Python packages
used across the project, such as:

``` text
pandas
numpy
matplotlib
scikit-learn
openpyxl
jupyter
```

SQLite is accessed through Python's standard library, so a separate
SQLite package is normally not required.

------------------------------------------------------------------------

# 5. Part 1 --- Payments Fraud Analytics

## Purpose

Part 1 focuses on payment and merchant analytics from an operational and
fraud-analysis perspective.

The workflow moves from data generation and spreadsheet analysis to SQL
fraud detection, Python reconciliation and dashboard preparation.

The aim is to understand transaction behaviour, identify suspicious
patterns, reconcile payment records and turn the results into useful
business insights.

## Main Components

### Data Generation

The data-generation stage creates the synthetic payment data used
throughout the analysis.

### Merchant Workbook

`merchant_workbook.xlsx` contains the spreadsheet analysis, including
lookup formulas, nested IF logic, pivot-table analysis and
merchant-level calculations.

### SQL Fraud Detection

`Part_B_SQL_Fraud_Detection.ipynb` contains the SQL-based fraud analysis
using the payment database.

### Python Payment Reconciliation

`Part_C_Python_Payment_Reconciliation.ipynb` and its Python script
perform reconciliation between the relevant payment records and identify
mismatches.

### Analytics Dashboard

`Part_D_Analytics_Dashboard.ipynb` prepares the business-facing
analytics.

Supporting chart outputs include:

-   `D1_headline_scorecards.png`
-   `D2_trends.png`
-   `D3_gmv_by_category.png`
-   `D3_gmv_by_payment_method.png`
-   `D4_merchant_details.png`

The images support the analysis; the actual interpretation remains
available as Markdown/notebook text.

## Running Part 1

Move into the folder:

``` bash
cd payments_fraud_analytics
```

If the final Part 1 structure contains `generate_data.py`, run it from
this directory:

``` bash
python generate_data.py
```

Then run the notebooks in this order:

``` text
1. Data generation
2. Merchant / spreadsheet analysis
3. SQL fraud detection
4. Python payment reconciliation
5. Dashboard analysis
```

The notebooks can be opened and run in Google Colab or Jupyter.

------------------------------------------------------------------------

# 6. Part 2 --- Credit Risk & Lending ML

## Purpose

Part 2 focuses on credit-risk modelling and responsible lending.

The workflow generates synthetic applicant and transaction-behaviour
data, handles thin-file applicants, trains and evaluates classifiers,
performs anomaly detection, creates risk-based pricing tiers, and
finishes with a bias-awareness note and deployment recommendation.

## Main Components

### Data Generation

`generate_data.py` produces:

``` text
credit_applicants.csv
txn_behaviour.csv
```

The applicant dataset is designed to contain 400 rows, including exactly
80 rows with missing `credit_bureau_score` values. The
transaction-behaviour dataset contains 265 rows and the required seeded
anomalies.

### Thin-File Handling

The workflow deliberately creates `is_thin_file` from the raw data
before imputation.

The order is:

1.  Create the thin-file indicator.
2.  Split into training and test sets.
3.  Calculate the median credit score using training data only.
4.  Use that value to fill missing scores in both splits.
5.  Keep all applicants rather than dropping rows.

This avoids test-set leakage while preserving thin-file applicants.

### Model Development

Both classifiers use the same train/test split, with:

``` text
random_state = 42
```

Preprocessing is fitted only on the training data and the models are
evaluated side by side.

### Risk-Based Pricing

Applicants are grouped into risk tiers and the observed default rates
are checked for the expected increasing pattern from lower- to
higher-risk groups.

### Isolation Forest

`IsolationForest` is applied to standardized behavioural features, with
contamination matched to the seeded anomaly proportion. Recall against
the seeded anomalies is reported.

### Bias-Awareness

The written analysis considers whether `employment_type`,
`monthly_income_inr` or `credit_bureau_score` could act as correlated
proxies for protected characteristics, even when protected fields are
not explicitly included.

It also recommends a concrete governance step before deployment.

### Final Recommendation

The final section compares the classifier metrics with the Isolation
Forest result and gives a practical model-deployment recommendation.

## Running Part 2

Move into the Part 2 folder:

``` bash
cd credit_risk_lending_ml
```

Run the generator from inside this folder:

``` bash
python generate_data.py
```

Do not run the generator from the repository root because it uses
relative paths.

Then open:

``` text
credit_risk_lending_ml.ipynb
```

Run the notebook from top to bottom.

The recommended flow is:

``` text
1. Generate data
2. Inspect and prepare data
3. Create thin-file flag
4. Split train/test data
5. Fit preprocessing on training data
6. Train classifiers
7. Evaluate classifiers
8. Build risk-pricing tiers
9. Run Isolation Forest
10. Complete bias-awareness analysis
11. Produce final comparison and recommendation
```

`roc_curve_comparison.png` is a supporting visual output from the model
evaluation.

------------------------------------------------------------------------

# 7. Part 3 --- AI Advisory & Blockchain Risk

## Purpose

Part 3 combines investment advisory logic, disclosure analysis, DCF
valuation, EV/EBITDA cross-checking and blockchain-risk analysis.

The workflow is designed to be reproducible and uses deterministic mock
mode where required, so paid external services are not necessary.

## Main Components

### `stock_universe.py`

Contains the stock universe and stock data used by the advisory
workflow.

### `investor_profiles.py`

Defines the investor profiles and their prescribed portfolio
allocations.

### `advisory_agent.py`

Implements the advisory workflow using the required:

``` text
Think → Act → Observe
```

structure.

The stock-data tool call follows the required `get_stock_data(...)`
pathway. CAPM expected return is based on beta, while portfolio variance
and standard deviation are calculated for the investor profiles.

The human-in-the-loop escalation rule is applied when the portfolio risk
exceeds the specified threshold.

### `disclosure_snippets.py`

Contains the committed disclosure snippets used for signal extraction.

### `extract_disclosure.py`

Extracts required disclosure signals such as risk flags, hedging
language and confidence indicators. The required mock execution does not
need a network call.

### `debate.py`

Runs the three-agent debate demonstration using the selected ticker's
actual numerical values.

### `dcf_calculator.py`

Performs the DCF valuation, including:

-   Five-year FCFF projection
-   CAPM-based cost of equity
-   Cost of debt
-   Capital-structure weights
-   WACC
-   Terminal growth
-   Terminal value
-   Present values
-   3 × 3 sensitivity analysis
-   EV/EBITDA cross-check

The sensitivity table checks WACC and terminal-growth combinations and
verifies the required spread between them.

### `blockchain_risk_note.md`

Contains the required written blockchain-risk analysis covering:

1.  Stablecoin / DAO risk
2.  A justified crypto-allocation recommendation
3.  The T.A.N.G. framework
4.  Named bank-side real-time defence mechanisms

## Running Part 3

Move into the Part 3 directory:

``` bash
cd ai_advisory_blockchain
```

Run the required Python components:

``` bash
python advisory_agent.py
python extract_disclosure.py
python debate.py
python dcf_calculator.py
```

The complete workflow can also be run through:

``` text
ai_advisory_blockchain.ipynb
```

Use the deterministic mock configuration required by the project.

------------------------------------------------------------------------

# 8. Design Decisions

## Part 1

The payment workflow deliberately uses different tools for different
jobs. Excel provides business-friendly spreadsheet analysis, SQL handles
structured transaction queries, Python performs reconciliation, and the
dashboard stage turns the results into business-facing visuals.

This keeps the workflow understandable and reproducible rather than
putting every operation into one tool.

## Part 2

The most important modelling decision was to retain thin-file applicants
instead of dropping them.

The thin-file flag is created before imputation, and the imputation
value is calculated from training data only. Both classifiers then use
the same split so their results can be compared fairly.

Anomaly detection is treated as a separate risk-monitoring task, while
the final deployment decision considers model performance together with
fairness and governance.

## Part 3

The advisory workflow is separated into smaller Python modules so each
responsibility can be inspected independently.

The DCF valuation is supported by an EV/EBITDA cross-check rather than
relying on a single valuation method.

The blockchain section approaches crypto from a risk-management
perspective and gives a justified allocation recommendation rather than
assuming crypto belongs in every portfolio.

Mock mode keeps the required demonstrations deterministic and
reproducible without depending on paid external services.

------------------------------------------------------------------------

# 9. Reproducibility

The project uses synthetic datasets where required by the capstone
specification.

The data-generation scripts are included so that the required datasets
can be reproduced.

Part 1 and Part 2 generators that use relative paths should always be
executed from their respective part folders.

For example:

``` bash
cd credit_risk_lending_ml
python generate_data.py
```

The same principle applies to the Part 1 generator if it is included in
its final folder structure.

------------------------------------------------------------------------

# 10. Submission Requirements

This project is submitted as **one public GitHub repository**.

The repository must contain all three part folders at its root:

``` text
paytm-fintech-capstone/
├── payments_fraud_analytics/
├── credit_risk_lending_ml/
├── ai_advisory_blockchain/
├── requirements.txt
└── README.md
```

Only one repository link should be submitted.

All required written interpretations should remain as Markdown content
in the root README, part-level READMEs, or notebook Markdown cells.
Required analysis should not exist only inside screenshots or other
non-text artifacts.

The project does not require screenshots, presentation slides, PDFs,
videos or audio for submission. Generated `.png` charts may be included
as supporting artifacts.

------------------------------------------------------------------------

# 11. Final Pre-Submission Checklist

### Repository

-   [ ] One public GitHub repository is used.
-   [ ] All three part folders are at the repository root.
-   [ ] Root `README.md` is present.
-   [ ] Root `requirements.txt` is present.
-   [ ] The final repository link is public.

### Part 1

-   [ ] Required datasets are present or reproducible.
-   [ ] Excel workbook is committed as `.xlsx`.
-   [ ] SQL notebook is present.
-   [ ] Python reconciliation notebook/script is present.
-   [ ] Dashboard notebook is present.
-   [ ] Required chart images are included where applicable.
-   [ ] Required written interpretations are present.

### Part 2

-   [ ] `generate_data.py` is present.
-   [ ] Required CSV datasets are present or reproducible.
-   [ ] Thin-file handling follows the required order.
-   [ ] Training-only preprocessing is used.
-   [ ] Train/test split uses the required random state.
-   [ ] Both classifiers use the identical split.
-   [ ] Evaluation metrics are reported.
-   [ ] Risk-pricing table is present.
-   [ ] Isolation Forest recall is reported.
-   [ ] Bias-awareness note is included.
-   [ ] Final model comparison and recommendation are included.
-   [ ] `roc_curve_comparison.png` is included if generated.

### Part 3

-   [ ] All required Python modules are present.
-   [ ] DCF calculator is present.
-   [ ] Blockchain risk note is present.
-   [ ] Required DCF sensitivity table is present.
-   [ ] EV/EBITDA cross-check is present.
-   [ ] Required advisory/disclosure/debate workflows run in mock mode.
-   [ ] Required written interpretations are present.

### General

-   [ ] All monetary figures are in INR.
-   [ ] No required interpretation exists only as an image.
-   [ ] No paid service is required for the submitted workflow.
-   [ ] Notebooks run from top to bottom without unexplained errors.
-   [ ] README paths match the final GitHub structure.
-   [ ] The single repository link is submitted through the LMS by the
    deadline communicated there.

------------------------------------------------------------------------

# 12. Final Note

The repository is organised so that a reviewer can start at this README,
understand the purpose of each part, install the required dependencies,
run the workflows, and inspect the outputs without needing additional
documents.

The three parts complement one another:

-   **Part 1** focuses on payment operations, fraud analytics and
    business reporting.
-   **Part 2** focuses on credit-risk modelling, anomaly detection and
    responsible lending.
-   **Part 3** focuses on investment advisory, financial valuation and
    blockchain-related risk.

Together, they provide a practical FinTech workflow covering data
analysis, risk management, machine learning, financial modelling and
business decision-making.
