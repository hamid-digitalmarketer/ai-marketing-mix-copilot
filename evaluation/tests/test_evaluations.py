"""
Evaluation Benchmark Integration Test
Runs CopilotEvaluationLab automated benchmark suite.
"""

import pytest
from evaluation.eval_runner import CopilotEvaluationLab


def test_copilot_full_evaluation_benchmark():
    lab = CopilotEvaluationLab()
    report = lab.run_benchmark()
    assert report["evaluation_status"] == "PASSED"
    assert report["overall_pass_rate_pct"] == 100.0
    assert report["passed_checks"] == report["total_benchmark_checks"]
