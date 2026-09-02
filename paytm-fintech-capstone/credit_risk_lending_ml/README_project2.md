# Credit Risk & Lending ML

## 1. Project Overview

This project develops a credit-risk and lending analytics workflow using applicant-level credit data and transaction behaviour data.

The project covers:
- Exploratory data analysis and preprocessing
- Credit default classification
- Risk-based pricing
- Transaction anomaly detection
- Bias awareness and deployment recommendations

---

## 2. Dataset Generation

The datasets were generated using the provided deterministic data-generation process with `random_state/seed = 42`.

### Credit Applicants
- Applicants: **400**
- Default cases: **81**
- Default rate: **20.25%**
- Missing credit bureau scores: **80**
- Missing bureau score rate: **20.00%**

### Transaction Behaviour
- Transactions: **265**
- Seeded `BTXNA*` anomalies: **15**

DATA GENERATED IS STORED IN "generate_data"

---

## 3. Part A — EDA & Preprocessing

### Default Rate

The dataset contains 81 default cases among 400 applicants, resulting in an exact default rate of **20.25%**, which falls within the required 15–25% range.

### Missing Credit Bureau Scores

There are **80 missing credit bureau scores**, representing **20.00%** of applicants.

### Thin-File Flag

An `is_thin_file` indicator was created directly from the original missing bureau-score values before imputation.

- `is_thin_file = 0`: 320 applicants
- `is_thin_file = 1`: 80 applicants

### Train/Test Split

The data was split using a **75/25 stratified split** with `random_state=42`.

- Training: 300 rows
- Test: 100 rows

### Median Imputation

The credit bureau score median was calculated **using training data only**.

- Training-derived median: **612.00**
- Missing values after imputation: **0** in both train and test

### Employment Encoding

`employment_type` was one-hot encoded, with training and test features aligned to the same columns.

### Standard Scaling

Numerical model features were standardized using `StandardScaler`, fitted only on the training data to prevent data leakage.

---

## 4. Part B — Classification Models

Two classification models were trained:

- Logistic Regression
- Decision Tree (`random_state=42`)

### Model Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 76.00% | 38.89% | 35.00% | 36.84% | 71.88% |
| Decision Tree | 67.00% | 24.00% | 30.00% | 26.67% | 53.12% |

### ROC Curve

The ROC curve comparison shows that Logistic Regression provides substantially better discrimination than the Decision Tree.

![ROC Curve](roc_curve_comparison.png)

---

## 5. Risk-Based Pricing

Risk tiers were created using Logistic Regression predicted default probabilities.

| Risk Tier | Observed Default Rate | Interest Rate |
|---|---:|---:|
| Low Risk | 8% | 10–14% |
| Medium-Low Risk | 12% | 14–18% |
| Medium-High Risk | 20% | 18–22% |
| High Risk | 40% | 22–28% |

### Monotonicity Check

The observed default rate increases consistently across the four risk tiers:

**8% → 12% → 20% → 40%**

This indicates that the predicted risk tiers provide a meaningful ordering of applicants by observed default risk.

---

## 6. Part C — Anomaly Detection

### Transaction Behaviour Dataset

The transaction behaviour dataset contains **265 transactions**, including **15 seeded `BTXNA*` anomalies**.

### Feature Selection

Isolation Forest was applied using:

- `txn_hour`
- `is_new_device`
- `txn_amount_inr`

### Standardization

The three behavioural features were standardized before anomaly detection.

### Isolation Forest

Isolation Forest was configured with:

- `random_state=42`
- Contamination = **15/265 ≈ 5.66%**

The model flagged **15 transactions** as anomalies overall.

### Anomaly Recall

Of the 15 seeded `BTXNA*` anomalies:

- Detected: **11**
- Missed: **4**
- Recall: **73.33%**

---

## 7. Part D — Bias-Awareness Note

[Paste the 200–400 word bias-awareness note here.]

---

## 8. Final Model Comparison

Logistic Regression outperformed the Decision Tree across accuracy, precision, recall, F1-score, and ROC-AUC.

Isolation Forest achieved **73.33% recall** on the 15 seeded transaction anomalies and can therefore serve as a complementary transaction-anomaly signal rather than the primary credit-risk classifier.

---

## 9. Deployment Recommendation

Logistic Regression is recommended as the primary credit-risk classifier because it achieved a test accuracy of **76.00%** and ROC-AUC of **71.88%**, outperforming the Decision Tree. The Decision Tree achieved only **53.12% ROC-AUC** and showed a large training/test accuracy gap, indicating overfitting. Isolation Forest can be used as a complementary anomaly-detection layer, while high-impact lending decisions should include appropriate human review and fairness monitoring.
