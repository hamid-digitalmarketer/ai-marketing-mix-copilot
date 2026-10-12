"""
Explanation & Executive Communication Agent
Translates statistical Bayesian posteriors, diminishing returns curves, and causal p-values into CMO-ready strategic narratives.
"""

from typing import List, Dict, Any
from agents.base import BaseCopilotAgent
from agents.schemas import Recommendation, EvidenceItem, PriorityLevel, EffortLevel, RecommendationStatus


class ExplanationAgent(BaseCopilotAgent):
    """Bridges data science and marketing leadership with plain-language executive summaries."""

    def __init__(self, demo_mode: bool = True):
        super().__init__(name="Explanation Agent", demo_mode=demo_mode)

    def execute_reasoning(self, input_context: Dict[str, Any]) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        exec_summary = self.call_tool("generate_executive_summary") or {}
        plain_insights = self.call_tool("translate_to_plain_language") or []

        rec_id = "REC-EXEC-BRIEF-CAPITAL-ALLOCATION"
        evidence = [
            EvidenceItem(source="Executive Synthesis", metric="Core Thesis", value=exec_summary.get("headline", "Reallocation Strategy")),
            EvidenceItem(source="Incrementality Synthesis", metric="Causal Finding", value=exec_summary.get("key_finding_incrementality", "")),
            EvidenceItem(source="Optimization Synthesis", metric="Portfolio Impact", value=exec_summary.get("key_finding_optimization", ""))
        ]

        recommendations.append(Recommendation(
            id=rec_id,
            agent=self.name,
            issue="Executive Decision Brief: Reallocating media capital from saturated channels unlocks +$408k annual revenue with zero extra budget",
            evidence=evidence,
            priority=PriorityLevel.HIGH,
            confidence=0.98,
            expected_impact="High-confidence portfolio capital efficiency optimization (+14.8% portfolio ROAS improvement)",
            effort=EffortLevel.LOW,
            proposed_action="Present executive brief to VP of Marketing & CFO to align on Q4 media budget reallocation.",
            next_steps=[
                "Circulate plain-language executive briefing slides to executive leadership",
                "Review channel saturation curves and geo holdout empirical proof with brand managers",
                "Finalize sign-off in the Growth OS governance queue"
            ],
            requires_approval=False,
            status=RecommendationStatus.PENDING
        ))

        return recommendations
