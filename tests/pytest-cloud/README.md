# Pytest / Playwright cloud proof

This is **Codex-authored Python adaptation of PR1 source**, not KaneAI-native generated pytest.
Source preview: https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/

1. Test Manager > GitHub PR QA POC 20261015 > Test Cases: TC-11 is the positive test; TC-12 is explicitly a controlled failure.
2. GitHub repository Settings > Secrets and variables > Actions: reuse LT_USERNAME and LT_ACCESS_KEY. Never put values in Git or terminal recordings.
3. Install `python -m pip install -r tests/pytest-cloud/requirements.txt` (Python 3.11).
4. `python -m pytest --collect-only tests/pytest-cloud/test_budget.py` makes no browser connection.
5. Run `python tests/pytest-cloud/run_ci.py` with the two environment variables and a unique LT_BUILD. This opens exactly two sequential cloud browser sessions, without retries.
6. The first test verifies Budget contains Brooklyn $120 and Scottsdale $145. The second confirms those same valid results and deliberately asserts count 3, producing a real pytest failure.
7. GitHub Actions stays failed (pytest exit 1). `if: always()` uploads JUnit, sanitized logs, screenshots and whitelisted session IDs; it does not convert the failed test to success.
8. Cloud setTestStatus marks each session. Exact project name plus `tms.tc_id` is the official Test Manager mapping capability; look under the matching build/run for TC-11 and TC-12.
9. JUnit is a GitHub artifact. No separate JUnit import into TMS is claimed.

Workflow: `.github/workflows/pytest-cloud-proof.yml`; only push to `qa/pytest-cloud-proof-20261015` or workflow_dispatch, contents:read, 12-minute job timeout.

Official references:
- https://www.testmuai.com/support/docs/playwright-testing/
- https://www.testmuai.com/support/docs/automated-test-cases-linked-using-capability/
- https://www.testmuai.com/support/docs/playwright-test-execution-setup/
