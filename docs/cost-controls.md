# Cost Controls & Precomputed Demo Architecture

Bayesian MCMC sampling (e.g., PyMC / Stan) can take 5–15 minutes of heavy CPU/GPU compute, and frontier LLMs incur non-trivial API costs per analysis run.

**AI Marketing Mix & Incrementality Copilot** addresses this with a dual-engine architecture:

---

## 1. Zero-Cost, Instantaneous Demonstration Engine (`DEMO_MODE=true`)

When `DEMO_MODE=true` (default):
- **Precomputed Bayesian Posteriors**: Loads verified posterior parameter artifacts (`precomputed_mmm_results.json`) generated from 4 chains $\times$ 1,500 NUTS draws.
- **Instantaneous Execution**: Runs full end-to-end multi-agent orchestration, non-linear Hill response evaluation, and scenario optimization in **under 15 milliseconds**.
- **Zero API Keys & $0.00 Compute Cost**: Runs on any clean machine or GitHub Actions CI without requiring paid API keys or dedicated compute clusters.

---

## 2. Telemetry & Budget Caps

- **Token Cost Tracking**: Simulates input context characters and tool outputs to benchmark token footprint for production capacity planning.
- **Latency Monitoring**: High-precision timers trace every tool call to detect query bottlenecks.
- **Least-Privilege Enforcement**: All write-capable tools are blocked until human approval is recorded in the governance ledger.
