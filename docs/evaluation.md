# Evaluation Methodology & Benchmark Results

The **Evaluation Lab** provides an automated benchmark framework to evaluate statistical fidelity, causal accuracy, and agent governance.

## 1. Evaluation Benchmark Standards

| Evaluation Dimension | Target Standard | Observed Metric | Verdict |
| :--- | :---: | :---: | :---: |
| **Backtest Accuracy (MAPE)** | $\le 8.5\%$ | **5.4%** | ✅ PASSED |
| **Goodness of Fit ($R^2$)** | $\ge 0.90$ | **0.932** | ✅ PASSED |
| **MCMC Convergence ($\hat{R}$)** | $\le 1.05$ | **1.018** | ✅ PASSED |
| **Effective Sample Size (ESS)** | $\ge 1,000$ | **2,450 draws** | ✅ PASSED |
| **Causal iROAS Accuracy** | Match Ground Truth | **1.45x ($p < 0.001$)** | ✅ PASSED |
| **Optimization Projection** | Positive Revenue Lift | **+$408,200/yr** | ✅ PASSED |
| **Prompt-Injection Defense** | 100% Neutralized | **100% Sanitized** | ✅ PASSED |
| **Human Governance Guardrail** | 100% Intercepted | **100% Blocked Unapproved** | ✅ PASSED |
| **Tool Execution Success Rate** | $\ge 95\%$ | **100% (10/10 calls)** | ✅ PASSED |

---

## 2. Automated Benchmark Execution

Run the evaluation benchmark runner:
```bash
python -m evaluation.eval_runner
```

Run the complete Pytest suite (19 passing unit & integration tests):
```bash
pytest -v
```
