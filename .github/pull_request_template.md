## Description
<!-- Provide a clear summary of the changes and motivation -->

## Related Issues
<!-- Reference any related issue (e.g. Closes #12) -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds agent, tool, or modeling capability)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Evaluation benchmark enhancement

## Checklist
- [ ] Code follows project style guidelines.
- [ ] All 19 unit & integration tests pass (`pytest evaluation/tests -v`).
- [ ] Evaluation benchmark passes (`python evaluation/eval_runner.py`).
- [ ] Read-only vs. Write-capable permissions are strictly maintained.
- [ ] Input data is sanitized against prompt injection.
- [ ] `DEMO_MODE=true` operates with zero required paid API credentials.
