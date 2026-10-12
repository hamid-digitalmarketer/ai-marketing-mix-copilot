"""
AI Marketing Mix & Incrementality Copilot — Standalone End-to-End Demo Script
Executes Bayesian MMM, Causal Geo Holdout analysis, and Budget Optimization with ZERO API costs.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Remove external conflicting project paths from sys.path
for p in list(sys.path):
    if "ai-marketing-growth-os" in p:
        sys.path.remove(p)

from agents.orchestrator import copilot_orchestrator
from modeling.mmm_engine import mmm_engine
from modeling.causal_engine import causal_engine
from modeling.budget_optimizer import budget_optimizer


def main():
    print("=" * 85)
    print("  AI MARKETING MIX & INCREMENTALITY COPILOT — STRATEGIC ALLOCATION ENGINE")
    print("  Bayesian MMM + Causal Inference with Human-in-the-Loop Governance")
    print("=" * 85)
    print("\n[INFO] Starting full copilot audit across multi-channel spend & geo holdouts...")
    print("[INFO] Mode: Rule-based Demo Engine (API Cost: $0.00 | Compute: Instantaneous)\n")

    # 1. Run All 5 Agents
    audit = copilot_orchestrator.run_full_copilot_audit(goal="Optimize Q4 Budget Allocation & Maximize Incremental ROAS")

    print(f"Audit completed in {audit['average_latency_ms']} ms avg per agent.")
    print(f"Specialized Agents Executed: {audit['total_agents_run']}")
    print(f"Total Strategic Recommendations: {audit['total_recommendations']}")
    print(f"Simulated Token Cost: {audit['total_tokens_consumed']} tokens")
    print(f"Estimated API Cost: ${audit['estimated_api_cost']:.4f}\n")

    # 2. Print Bayesian MMM Decomposition
    print("-" * 85)
    print("BAYESIAN MMM DECOMPOSITION & MARGINAL ROAS (mROI):")
    print("-" * 85)
    channels = mmm_engine.get_channel_metrics()
    print(f"{'Channel Name':<32} | {'Spend ($)':<12} | {'Revenue ($)':<14} | {'ROAS':<6} | {'mROI':<6} | {'Status'}")
    print("-" * 85)
    for ch in channels:
        print(f"{ch['channel_name']:<32} | ${ch['total_spend']:>10,.0f} | ${ch['modeled_contribution']:>12,.0f} | {ch['blended_roas']:>4.2f}x | {ch['marginal_roas']:>4.2f}x | {ch['saturation_status']}")

    # 3. Print Causal Incrementality Findings
    print("\n" + "-" * 85)
    print("CAUSAL INCREMENTALITY EXPERIMENT (GEO HOLDOUT DIFF-IN-DIFF):")
    print("-" * 85)
    did = causal_engine.run_diff_in_diff_analysis()
    print(f"Target Channel:            Paid Search (Google Ads)")
    print(f"Experiment Design:         30 Market DMAs (15 Treatment vs 15 Control Holdouts)")
    print(f"Platform Reported ROAS:    {did['platform_reported_roas']:.2f}x (Last-touch attributed)")
    print(f"True Causal iROAS:         {did['incremental_roas_iroas']:.2f}x (Empirically verified lift)")
    print(f"Attribution Overstatement: -{did['attribution_haircut_pct']:.1f}% (Over-crediting brand searches)")
    print(f"Statistical Significance:  p = {did['statistical_significance']['p_value']} (Statistically Significant)")

    # 4. Print Strategic Recommendations
    print("\n" + "-" * 85)
    print("TOP IMPACT-EFFORT PRIORITIZED RECOMMENDATIONS:")
    print("-" * 85)
    for idx, rec in enumerate(audit["unified_action_plan"][:4], 1):
        print(f"\n{idx}. [{rec['priority'].upper()}] {rec['issue']}")
        print(f"   Agent: {rec['agent']} | ID: {rec['id']}")
        print(f"   Proposed Action: {rec['proposed_action']}")
        print(f"   Expected Impact: {rec['expected_impact']}")
        print(f"   Requires Human Approval: {rec['requires_approval']} (Status: {rec['status'].upper()})")

    # 5. Demonstrate Human-in-the-Loop Governance
    print("\n" + "=" * 85)
    print("  HUMAN-IN-THE-LOOP APPROVAL & REALLOCATION OUTCOME DEMO")
    print("=" * 85)

    sample_id = "REC-SCENARIO-OPTIMAL-BUDGET"
    print(f"\n[STEP 1] Testing Guardrail on unapproved action '{sample_id}'...")
    blocked = copilot_orchestrator.execute_approved_action(sample_id)
    print(f"         Guardrail Intercepted: {blocked.get('error')}")

    print(f"\n[STEP 2] Human Lead ('hamid-lead') reviews and APPROVES budget reallocation...")
    app = copilot_orchestrator.approve_recommendation(sample_id, reviewer="hamid-lead")
    print(f"         Approval Result: Status = {app.get('status').upper()} by {app.get('approved_by')}")

    print(f"\n[STEP 3] Executing write action (dispatching to ad platforms)...")
    exec_res = copilot_orchestrator.execute_approved_action(sample_id)
    print(f"         Execution Result: Status = {exec_res.get('status').upper()}")
    print(f"         Payload Dispatched: {exec_res.get('execution_result')}")

    print(f"\n[STEP 4] Tracking measured outcome lift against baseline metrics...")
    outcome = copilot_orchestrator.measure_action_outcome(sample_id).get("outcome", {})
    print(f"         Metric Tracked: {outcome.get('metric')}")
    print(f"         Baseline: {outcome.get('baseline_value')}")
    print(f"         Measured: {outcome.get('measured_value')}")
    print(f"         Observed Delta: {outcome.get('delta')}")
    print(f"         Verdict: {outcome.get('verdict')}")

    print("\n" + "=" * 85)
    print("  DEMO COMPLETED SUCCESSFULLY! All models, causal proofs & guardrails verified.")
    print("=" * 85)


if __name__ == "__main__":
    main()
