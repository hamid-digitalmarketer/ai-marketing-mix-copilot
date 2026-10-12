# Contributing to AI Marketing Mix & Incrementality Copilot

Thank you for your interest in contributing to **AI Marketing Mix & Incrementality Copilot**! We welcome contributions from data scientists, econometricians, AI engineers, and marketing technologists.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful, constructive, and collaborative in all discussions and pull requests.

---

## Development Workflow

### 1. Prerequisites
- Python 3.11+
- Git
- Optional: Docker and Docker Compose

### 2. Fork and Clone
```bash
git clone https://github.com/hamid-digitalmarketer/ai-marketing-mix-copilot.git
cd ai-marketing-mix-copilot
```

### 3. Virtual Environment Setup
```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Running Tests & Evaluations
Before committing code, make sure all tests pass:
```bash
pytest evaluation/tests -v
python evaluation/eval_runner.py
```

---

## Architecture Guidelines

1. **Evidence Over Opinion**:
   - Any agent recommendation must be backed by quantitative evidence (`EvidenceItem`) derived from verified model results or causal experiments.
2. **Deterministic Fallbacks (`DEMO_MODE=true`)**:
   - All modules must be runnable out-of-the-box with `$0.00` API cost and without third-party credentials.
3. **Least-Privilege Tool Permissions**:
   - Analytical tools (data summarization, adstock/Hill transformations, MCMC diagnostics) must be registered with `ToolPermission.READ_ONLY`.
   - Modifying tools (budget reallocations, API bidding dispatches) must be registered with `ToolPermission.WRITE_CAPABLE` and guarded by the Human-in-the-Loop orchestrator.
4. **Input Sanitization**:
   - All external time-series and user parameters must be processed through `sanitize_text()` to prevent prompt-injection attacks.

---

## Submitting Pull Requests

1. Create a descriptive feature branch:
   ```bash
   git checkout -b feat/bayesian-meridian-prior-calibration
   ```
2. Commit using conventional commit format:
   - `feat(...)`: New feature or agent capability
   - `fix(...)`: Bug fix
   - `docs(...)`: Documentation updates
   - `test(...)`: Additional tests or benchmark cases
   - `refactor(...)`: Code refactoring without behavior change
3. Ensure CI passes on your branch.
4. Submit a Pull Request targeting `main`.

---

## Reporting Security Issues

Please do not submit public GitHub issues for security vulnerabilities. Contact the maintainer directly or email security concerns to `hamid-digitalmarketer@users.noreply.github.com`.
