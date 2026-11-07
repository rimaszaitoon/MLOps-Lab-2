# Model selection

## The question

The model predicts the probability that a customer will leave the telecom service (churn). A wrong prediction may cause the company to lose customers or waste retention resources, while customers may receive unnecessary offers.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | Simple and interpretable baseline | 0.7982 | 0.4948 | 0.2500 | 4.1 | 4 | bb519a64dd7a413b9d758858a0d596c3 |
| Random Forest | To capture nonlinear patterns | 0.7589 | 0.4536 | 0.2222 | 19.7 | 3160 | a64d5c9b48884dccb516395c12be4039 |
| Gradient Boosting | To test boosting performance | 0.7476 | 0.4167 | 0.2222 | 5.2 | 142 | e4c50bd7959142b4b831d736046c3d98 |

## The champion

I selected Logistic Regression as the champion because it achieved the highest AUC (0.7982) and F1 (0.4948), with the lowest latency (4.1 ms) and smallest model size (4 KB).

I accepted its lowest contract-slice F1 of 0.2500 because the other candidates had even lower worst-slice scores (0.2222).

## My promotion rules

- Latency budget (p95): 25 ms, because the prediction API should respond quickly.
- Minimum gain to replace the champion (F1 points): 0.005, because a new model should provide a measurable improvement before replacing the current champion.

## What I would check next

I would investigate performance across contract types, especially one-year and two-year contracts, because their F1 scores are relatively low. I would also monitor changes in customer behavior and data distribution over time.

