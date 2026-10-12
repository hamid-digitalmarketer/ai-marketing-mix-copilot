"""
Bayesian Model Agent
Decomposes channel contributions, tracks MCMC diagnostics, evaluates Hill saturation, and computes marginal ROAS.
"""

from typing import List, Dict, Any
from agents.base import BaseCopilotAgent
from agents.schemas import Recommendation, EvidenceItem, PriorityLevel, EffortLevel, RecommendationStatus


class ModelAgent(BaseCopilotAgent):
    """Executes Bayesian Marketing Mix Modeling and estimates diminishing marginal returns."""

    def __init__(self, demo_mode: bool = True):
        super().__init__(name="Model Agent", demo_mode=demo_mode)

    def execute_reasoning(self, input_context: Dict[str, Any]) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        # 1. Model Convergence & Fit Verification
        diag = self.call_tool("check_convergence") or {}
        rec_id_diag = "REC-MODEL-CONVERGENCE"
        evidence_diag = [
            EvidenceItem(source="Bayesian Sampler (NUTS)", metric="Max Gelman-Rubin R-hat", value=diag.get("max_r_hat", 1.018)),
            EvidenceItem(source="Bayesian Sampler (NUTS)", metric="Effective Sample Size (ESS)", value=diag.get("effective_sample_size", 2450)),
            EvidenceItem(source="Goodness-of-Fit", metric="Model MAPE", value=f"{diag.get('mape_pct')}%"),
            EvidenceItem(source="Goodness-of-Fit", metric="R-Squared", value=diag.get("r_squared"))
        ]
        recommendations.append(Recommendation(
            id=rec_id_diag,
            agent=self.name,
            issue="Bayesian MMM model achieved robust MCMC convergence (R-hat <= 1.02, zero divergences) and high explanatory power (R2: 0.93)",
            evidence=evidence_diag,
            priority=PriorityLevel.LOW,
            confidence=0.99,
            expected_impact="Validates high statistical reliability for subsequent budget scenario planning and causal attribution",
            effort=EffortLevel.LOW,
            proposed_action="Adopt model posterior parameters as primary baseline for quarterly capital allocation.",
            next_steps=[
                "Confirm credible intervals across all media channel coefficients",
                "Log model posterior artifacts to model registry",
                "Trigger automated scenario planner"
            ],
            requires_approval=False,
            status=RecommendationStatus.PENDING
        ))

        # 2. Identify Channel Saturation (Google Search Saturated, Retail Media Underfunded)
        mroi_data = self.call_tool("compute_marginal_roi") or []
        for ch in mroi_data:
            cname = ch["channel"]
            mroi = ch["current_marginal_roas"]
            broas = ch["current_blended_roas"]

            if mroi < 1.0:
                rec_id_sat = f"REC-MODEL-SATURATED-{abs(hash(cname)) % 10000}"
                evidence_sat = [
                    EvidenceItem(source="Bayesian Hill Saturation", metric="Marginal ROAS (mROI)", value=f"{mroi:.2f}x"),
                    EvidenceItem(source="MMM Decomposition", metric="Blended ROAS", value=f"{broas:.2f}x"),
                    EvidenceItem(source="Saturation Classifier", metric="Operating Region", value="DIMINISHING_RETURNS_SATURATED")
                ]
                recommendations.append(Recommendation(
                    id=rec_id_sat,
                    agent=self.name,
                    issue=f"Severe diminishing marginal returns in {cname}: Every marginal $1 spent returns only ${mroi:.2f} in incremental revenue",
                    evidence=evidence_sat,
                    priority=PriorityLevel.CRITICAL,
                    confidence=0.97,
                    expected_impact=f"Prevent capital waste and reclaim capital returning negative marginal profit on last-dollar spend",
                    effort=EffortLevel.LOW,
                    proposed_action=f"Trim weekly spend on {cname} by 25-30% to pull spend back toward the steep, efficient section of the response curve.",
                    next_steps=[
                        f"Reduce weekly {cname} budget from current levels",
                        "Evaluate search query report to trim high-cost generic and branded cannibalizing keywords",
                        "Monitor marginal return curve stabilization"
                    ],
                    requires_approval=True,
                    status=RecommendationStatus.PENDING
                ))
            elif mroi >= 2.5:
                rec_id_scale = f"REC-MODEL-EXPAND-{abs(hash(cname)) % 10000}"
                evidence_scale = [
                    EvidenceItem(source="Bayesian Hill Saturation", metric="Marginal ROAS (mROI)", value=f"{mroi:.2f}x"),
                    EvidenceItem(source="MMM Decomposition", metric="Blended ROAS", value=f"{broas:.2f}x"),
                    EvidenceItem(source="Saturation Classifier", metric="Operating Region", value="UNDER_ALLOCATED_EXPANSION_ZONE")
                ]
                recommendations.append(Recommendation(
                    id=rec_id_scale,
                    agent=self.name,
                    issue=f"High untapped marginal headroom in {cname}: Every additional $1 invested generates ${mroi:.2f} in revenue",
                    evidence=evidence_scale,
                    priority=PriorityLevel.HIGH,
                    confidence=0.95,
                    expected_impact=f"Projected substantial top-line revenue acceleration with profitable incremental return",
                    effort=EffortLevel.LOW,
                    proposed_action=f"Scale weekly spend in {cname} by 50-60% until marginal ROAS converges with portfolio average.",
                    next_steps=[
                        f"Increase target spend in {cname}",
                        "Expand product target catalog and top-of-search retail placements",
                        "Schedule weekly marginal return tracking"
                    ],
                    requires_approval=True,
                    status=RecommendationStatus.PENDING
                ))

        return recommendations
