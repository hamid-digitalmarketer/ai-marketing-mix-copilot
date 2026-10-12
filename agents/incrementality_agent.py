"""
Incrementality & Causal Inference Agent
Analyzes geo holdout experiments, measures true incremental lift (iROAS), and calibrates platform attribution biases.
"""

from typing import List, Dict, Any
from agents.base import BaseCopilotAgent
from agents.schemas import Recommendation, EvidenceItem, PriorityLevel, EffortLevel, RecommendationStatus


class IncrementalityAgent(BaseCopilotAgent):
    """Calibrates marketing performance using empirical causal experiments and geo holdouts."""

    def __init__(self, demo_mode: bool = True):
        super().__init__(name="Incrementality Agent", demo_mode=demo_mode)

    def execute_reasoning(self, input_context: Dict[str, Any]) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        # 1. Geo Holdout Difference-in-Differences Findings
        did_res = self.call_tool("run_diff_in_diff") or {}
        sig = did_res.get("statistical_significance", {})
        
        rec_id_did = "REC-CAUSAL-LIFT-SEARCH"
        evidence_did = [
            EvidenceItem(source="Geo Holdout (30 DMAs)", metric="Causal Incremental ROAS (iROAS)", value=f"{did_res.get('incremental_roas_iroas')}x"),
            EvidenceItem(source="Google Ads Reported", metric="Platform Last-Touch ROAS", value=f"{did_res.get('platform_reported_roas')}x"),
            EvidenceItem(source="Causal Calibration Engine", metric="Attribution Overstatement Haircut", value=f"-{did_res.get('attribution_haircut_pct')}%"),
            EvidenceItem(source="Hypothesis Test", metric="P-Value", value=sig.get("p_value", 0.001))
        ]
        
        recommendations.append(Recommendation(
            id=rec_id_did,
            agent=self.name,
            issue="Google Ads platform is over-reporting ROAS by 61.8% (3.80x reported vs 1.45x true causal iROAS) due to brand search cannibalization",
            evidence=evidence_did,
            priority=PriorityLevel.CRITICAL,
            confidence=0.98,
            expected_impact="Corrects distorted capital allocation and stops overpaying for conversions that occur organically anyway",
            effort=EffortLevel.LOW,
            proposed_action="Calibrate Google Ads bidding targets by applying a 0.38 incrementality discount factor to in-platform ROAS targets.",
            next_steps=[
                "Adjust Google Ads tROAS targets upward by 60% to force algorithm to bid on true incremental queries",
                "Segment branded keywords into a separate zero-margin campaign with strict bid caps",
                "Re-test organic search lift during brand keyword suppression windows"
            ],
            requires_approval=True,
            status=RecommendationStatus.PENDING
        ))

        # 2. Incrementality Testing Roadmap (Meta Ads Experiment Design)
        design = self.call_tool("design_geo_holdout", channel="Meta Ads") or {}
        rec_id_design = "REC-CAUSAL-DESIGN-META"
        evidence_design = [
            EvidenceItem(source="Experiment Planner", metric="Target Channel", value=design.get("target_channel", "Meta Ads")),
            EvidenceItem(source="Experiment Planner", metric="Holdout Market Split", value=f"{design.get('recommended_holdout_pct')}% of DMAs"),
            EvidenceItem(source="Experiment Planner", metric="Minimum Detectable Lift", value=f"{design.get('estimated_minimum_detectable_lift_pct')}%"),
            EvidenceItem(source="Risk Assessment", metric="Revenue at Risk", value=f"${design.get('estimated_revenue_at_risk_usd'):,.2f}")
        ]

        recommendations.append(Recommendation(
            id=rec_id_design,
            agent=self.name,
            issue="Meta Ads currently relies on modeled attribution; requires 4-week geo holdout test across 10 control DMAs to establish true incremental baseline",
            evidence=evidence_design,
            priority=PriorityLevel.MEDIUM,
            confidence=0.93,
            expected_impact="Establishes definitive causal iROAS baseline for Meta mid-funnel spend and eliminates post-iOS14 attribution guesswork",
            effort=EffortLevel.MEDIUM,
            proposed_action="Launch a 4-week matched-market geo holdout test across 10 control DMAs using Synthetic Control methodology.",
            next_steps=[
                "Approve DMA market split selection (10 holdout DMAs vs 20 treatment DMAs)",
                "Configure geo-exclusion parameters in Meta Ads Manager for test period",
                "Set automated synthetic control daily revenue tracking dashboard"
            ],
            requires_approval=True,
            status=RecommendationStatus.PENDING
        ))

        return recommendations
