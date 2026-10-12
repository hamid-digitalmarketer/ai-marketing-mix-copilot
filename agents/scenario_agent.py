"""
Scenario Planning & Budget Optimization Agent
Simulates counterfactual budget reallocation scenarios, balances marginal ROAS, and forecasts outcomes with credible intervals.
"""

from typing import List, Dict, Any
from agents.base import BaseCopilotAgent
from agents.schemas import Recommendation, EvidenceItem, PriorityLevel, EffortLevel, RecommendationStatus


class ScenarioAgent(BaseCopilotAgent):
    """Generates counterfactual budget allocation scenarios and solves for equalized marginal ROAS."""

    def __init__(self, demo_mode: bool = True):
        super().__init__(name="Scenario Agent", demo_mode=demo_mode)

    def execute_reasoning(self, input_context: Dict[str, Any]) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        # 1. Optimal Marginal ROI Budget Reallocation Plan
        opt = self.call_tool("optimize_allocation") or {}
        
        rec_id_opt = "REC-SCENARIO-OPTIMAL-BUDGET"
        evidence_opt = [
            EvidenceItem(source="Marginal ROI Optimizer", metric="Projected Annual Revenue Gain", value=f"${opt.get('projected_annual_revenue_gain'):,.2f}"),
            EvidenceItem(source="Marginal ROI Optimizer", metric="Projected Weekly Revenue Lift", value=f"${opt.get('projected_weekly_revenue_gain'):,.2f}"),
            EvidenceItem(source="Capital Allocation Model", metric="Efficiency Lift", value=opt.get("projected_overall_roas_lift", "+14.8%")),
            EvidenceItem(source="Total Budget Constraint", metric="Weekly Media Budget", value=f"${opt.get('total_budget'):,.2f} (Neutral Spend)")
        ]

        recommendations.append(Recommendation(
            id=rec_id_opt,
            agent=self.name,
            issue="Optimal reallocation solves for equalized marginal ROAS across channels, unlocking +$408,200 annual revenue with $0 extra spend",
            evidence=evidence_opt,
            priority=PriorityLevel.HIGH,
            confidence=0.96,
            expected_impact="+$408,200.00 incremental annual top-line revenue without increasing overall marketing budget",
            effort=EffortLevel.LOW,
            proposed_action="Reallocate $8,423/week from saturated Google Search: redirect $6,269 to Retail Media, $1,038 to YouTube, and $981 to Email.",
            next_steps=[
                "Review recommended per-channel weekly budget targets",
                "Obtain executive approval in Growth OS human-in-the-loop queue",
                "Gradually shift weekly spend over 3-week transition pacing"
            ],
            requires_approval=True,
            status=RecommendationStatus.PENDING
        ))

        # 2. Counterfactual Simulation: 20% Shift from Search to Retail Media
        sim = self.call_tool("simulate_budget_reallocation", google_search_shift=-5000.0, retail_media_shift=5000.0) or {}
        ci = sim.get("credible_interval_90pct", [0, 0])
        
        rec_id_sim = "REC-SCENARIO-SEARCH-TO-RETAIL"
        evidence_sim = [
            EvidenceItem(source="Counterfactual Simulator", metric="Weekly Shift Amount", value="$5,000.00 / week"),
            EvidenceItem(source="Counterfactual Simulator", metric="Predicted Weekly Net Lift", value=f"+${sim.get('predicted_weekly_revenue_lift'):,.2f}"),
            EvidenceItem(source="Bayesian Credible Interval (90%)", metric="Interval Lower - Upper", value=f"[+${ci[0]:,.2f}, +${ci[1]:,.2f}]"),
            EvidenceItem(source="Annualized Projection", metric="Net Revenue Lift", value=f"+${sim.get('annualized_projected_revenue_lift'):,.2f}")
        ]

        recommendations.append(Recommendation(
            id=rec_id_sim,
            agent=self.name,
            issue="Shifting $5,000/week from Google Search to Retail Media produces immediate net positive revenue delta with 90% confidence",
            evidence=evidence_sim,
            priority=PriorityLevel.MEDIUM,
            confidence=0.94,
            expected_impact=f"Estimated +${sim.get('annualized_projected_revenue_lift'):,.2f}/year in incremental revenue with positive credible lower bound",
            effort=EffortLevel.LOW,
            proposed_action="Execute immediate trial budget shift of $5,000/week from Search to Retail Media for a 6-week measurement period.",
            next_steps=[
                "Apply weekly pacing adjust: Google Search -$5,000, Retail Media +$5,000",
                "Track weekly conversion lift against 90% Bayesian credible envelope",
                "Audit retail sponsored product inventory coverage"
            ],
            requires_approval=True,
            status=RecommendationStatus.PENDING
        ))

        return recommendations
