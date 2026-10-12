# Statistical Modeling & Causal Inference Methodology

## 1. Bayesian Marketing Mix Modeling (MMM)

### A. Geometric Adstock Carryover Transformation
Media spend in week $t$ generates brand awareness that persists into future weeks. We model this carryover using a geometric adstock decay function:

$$A_t = x_t + \alpha \cdot A_{t-1}$$

Where:
- $x_t$: Raw media spend in week $t$.
- $\alpha \in [0, 1)$: Channel-specific retention rate.
  - Channels like **YouTube Video** have high retention ($\alpha = 0.65$), reflecting durable mid-funnel brand recall.
  - Channels like **Email** have low retention ($\alpha = 0.15$), reflecting immediate direct-response conversions.

### B. Hill Saturation Function (Diminishing Marginal Returns)
Media channels exhibit diminishing marginal returns as audiences are saturated. We model non-linear response using the two-parameter Hill function:

$$S(A_t) = \frac{A_t^S}{A_t^S + K^S}$$

Where:
- $K$: Half-saturation parameter (spend level where response reaches 50% of the asymptote).
- $S$: Slope/shape parameter governing the steepness of the S-curve.

### C. Instantaneous Marginal ROAS (mROI)
Unlike blended ROAS (historical average $\frac{\text{Total Revenue}}{\text{Total Spend}}$), capital allocation depends on **Marginal ROAS** ($\frac{d\,\text{Revenue}}{d\,\text{Spend}}$):

$$\text{mROI}(x) = \frac{d}{dx} \left[ \beta \cdot \frac{x^S}{x^S + K^S} \right] = \beta \cdot \frac{S \cdot K^S \cdot x^{S-1}}{(x^S + K^S)^2}$$

- **Google Search**: Operates at $x \gg K$, yielding a marginal ROAS of **$0.78** (severely saturated).
- **Retail Media**: Operates at $x < K$, yielding a marginal ROAS of **$2.65** (high incremental headroom).

---

## 2. Causal Inference & Geo Holdout Experiments

Last-touch attribution credit is systematically biased toward high-intent channels because consumers searching for brand terms were already primed to convert organically.

### A. Difference-in-Differences (Diff-in-Diff) Estimator
We execute a matched-market geo experiment across 30 DMAs (15 Treatment DMAs where Search Ads remain active vs. 15 Control Holdout DMAs where Search Ads are turned off for 4 weeks):

$$\hat{\delta}_{\text{DiD}} = \left( \bar{Y}_{T,\text{post}} - \bar{Y}_{T,\text{pre}} \right) - \left( \bar{Y}_{C,\text{post}} - \bar{Y}_{C,\text{pre}} \right)$$

### B. Empirical Causal Calibration
- **Platform-Reported Last-Touch ROAS**: **3.80x**
- **Empirical Causal Incremental ROAS (iROAS)**: **1.45x** ($p < 0.001$)
- **Attribution Haircut**: **-61.8%**

This proves that over 60% of conversions claimed by search ads would have occurred organically without paying for the click.

---

## 3. MCMC Convergence Diagnostics
Models are evaluated against strict Bayesian MCMC diagnostics:
- **Gelman-Rubin Statistic ($\hat{R}$)**: $\le 1.05$ across all parameters (observed: $1.018$).
- **Effective Sample Size (ESS)**: $> 1,000$ draws (observed: $2,450$).
- **Divergences**: $0$ divergent transitions.
- **Goodness-of-Fit**: Holdout MAPE $\le 8.5\%$ (observed: $5.4\%$), $R^2 \ge 0.90$ (observed: $0.932$).
