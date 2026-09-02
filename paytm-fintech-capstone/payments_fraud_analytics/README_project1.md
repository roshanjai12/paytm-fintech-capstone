# Payments Fraud Analytics

## 1. Project Overview

This project analyses synthetic payment data to identify merchant-level patterns, fraud-related behaviour, payment discrepancies, and reconciliation issues.

The project combines Excel/Sheets, SQL, Python, and matplotlib to create an end-to-end payment analytics workflow.

The data is generated using a fixed random seed of `42` so that the results are reproducible.

---

## 2. Data Generation

The project uses `generate_data.py` to generate the required synthetic payment data.

The generation logic produces:

- A 547-row ledger consisting of 500 baseline transactions, 15 seeded burner-account chargebacks, and 32 velocity-attack transactions across 8 clusters.
- Merchant and user reference tables.
- A deliberately discrepant gateway export.

The gateway export contains seeded discrepancies of approximately:

- 5% missing transactions
- 3% amount mismatches
- 2% extra transactions
- 2% status mismatches

The project uses the generated data exactly as provided by the generation logic rather than creating a separate dataset.

### Design Decision

A fixed seed of `42` is used so that the generated datasets remain reproducible and the same seeded fraud patterns can be verified during grading.

---

# Part A — Excel / Sheets Merchant Workbook

## 3. Merchant Workbook

The Excel workbook is stored as:

`merchant_workbook.xlsx`

The workbook uses `ledger.csv` and `merchants.csv` to create a transaction-level merchant view.

The main purpose of this section is to enrich transaction data with merchant information and perform merchant-level analysis.

---

## 4. VLOOKUP with IFERROR

A fixed-range VLOOKUP with absolute `$` references is used to retrieve:

- `merchant_name`
- `category`
- `region`

from the merchant reference table.

`IFERROR` is used so that an unmatched `merchant_id` displays:

`Merchant not found`

instead of producing an Excel error.

### Why this was used

VLOOKUP provides a simple way to connect transaction records with merchant reference information. Absolute references ensure that the lookup range does not change when the formula is copied down.

---

## 5. HLOOKUP Demonstration

An HLOOKUP demonstration is included using a small horizontally arranged reference table.

The example uses payment methods such as:

- UPI
- Wallet
- Card
- Netbanking

with corresponding MDR-style fee percentages.

### Design Decision

The fee percentages are illustrative values used to demonstrate how HLOOKUP works. The exact assumptions are documented inside the workbook.

---

## 6. Nested IF / AND Classification

A nested `IF` / `AND` rule is used to classify transactions as:

`High-Value Merchant Day`

The required classification rule is:

- The merchant's daily transaction total must exceed **INR 5,000**
- The merchant's region must **not** be `East`

The daily transaction total is obtained using the pivot-table analysis.

### Why this rule was used

The rule combines transaction value with merchant location to create a simple business classification. It demonstrates how multiple conditions can be combined to flag potentially important merchant activity.

---

## 7. Pivot Table Analysis

A pivot table is used to summarise:

- Total `amount_inr`
- Transaction count
- `merchant_id`
- `status`

A count-versus-count-unique comparison is also included for at least five merchants.

The comparison considers:

- Unique days transacted
- Total transaction count

### Interpretation

Comparing unique transaction days with total transaction count helps distinguish merchants with consistent activity from merchants whose activity is concentrated into fewer days.

---

# Part B — SQL Fraud-Pattern Detection

## 8. SQLite Database

The datasets are loaded into a normalized SQLite database:

`paytm_payments.db`

The database contains three main tables:

- `merchants`
- `users`
- `transactions`

The schema declares primary keys and the required foreign-key relationships.

The `transactions` table connects users and merchants through their respective foreign keys.

---

## 9. SQL Queries

At least six SQL queries are included with their outputs.

Together, the queries demonstrate:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `GROUP BY`
- `HAVING`
- `INNER JOIN`
- `LEFT JOIN`

The queries focus on practical payment and fraud-analysis questions.

---

## 10. Chargeback Impact

The SQL analysis quantifies chargeback impact using:

- Number of chargeback transactions
- Number of unique users affected
- Total chargeback amount

### Interpretation

Looking at chargebacks through both transaction count and affected users provides a better view of the scale of the issue than looking only at the total monetary amount.

---

## 11. Burner Account Detection

Burner accounts are identified using users whose signup date is less than 30 days before the transaction time.

The analysis is restricted to:

`status = 'chargeback'`

The boundary is defined as:

```text
0 <= transaction_time - signup_date < 30 days

---

## 12. Velocity Attack Detection

Velocity attacks are identified as users with at least **3 transactions within a 10-minute window**.

The SQL analysis groups transactions by:

- `user_id`
- Rounded/floored 10-minute transaction-time bucket

The query should surface all **8 seeded velocity-attack clusters**.

### Interpretation

Transaction velocity is useful because a sudden concentration of multiple transactions in a short period can indicate automated or coordinated payment activity.

The analysis focuses on identifying the seeded clusters rather than requiring one exact row count or bucket boundary.

---

# Part C — Python Payment Reconciliation

## 13. Reconciliation Function

The reconciliation logic is implemented in:

`reconcile.py`

The main reusable function is:

```python
reconcile_payments(ledger_df, gateway_df)

---

##14. Dashboard Overview

The dashboard is generated using matplotlib and consists of four saved chart/image layers.

The dashboard is code-generated and does not depend on a live BI tool such as Power BI or Looker Studio.

Each layer is saved as an image and includes a short written interpretation.

---

##15. Headline Layer

The headline layer displays key payment metrics such as:

Total GMV
Overall success rate
Reconciliation match rate
Chargeback ratio

---

##16. Dashboard Design Decisions

The dashboard uses different chart types according to the type of information being communicated.

Scorecards are used for high-level KPIs.
Time-series charts are used for trends over time.
Bar charts are used for category and payment-method comparisons.
A saved table image is used for detailed merchant-level information.

The dashboard is intentionally kept simple so that the main payment and risk signals can be understood quickly.

---

##17. Key Interpretations
Payment Activity

GMV and transaction activity provide an overview of the scale of payment operations and help identify the largest contributing payment methods and categories.

Chargeback Risk

Chargeback ratios are used as risk indicators.

A high ratio does not automatically prove fraud, but it can identify merchants or transaction patterns that deserve further investigation.

Reconciliation

Differences between the ledger and gateway export can indicate operational or settlement issues.

Reconciliation therefore acts as an important control for payment-data consistency.

Fraud Patterns

Burner accounts and high transaction velocity provide different types of fraud signals.

Combining account age with transaction behaviour can help identify suspicious patterns more effectively than using a single indicator.
