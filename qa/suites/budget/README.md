# TC-5 code export — observed incomplete automation

Exported from TestMu AI on 2026-10-15. This is a manually archived copy, not native Git synchronization.

- Project: GitHub PR QA POC 20261015
- Test case: TC-5
- Code export: AssertiveAlchemy, version 1, Python/Playwright
- Original requirement: Budget nightly price <= $150; exclude $275/$280; All restores listings.
- Actual generated code: navigate, vision-query Austin loft, assert visibility. Budget and All steps are absent.
- Code UI status: Unverified. Do not treat this archive as a passing regression suite.

## Files and execution entry

`test.py` is the original generated file. It calls `testmu.run(test)`; do not assume `pytest` is the correct runner just because `pytest-playwright` appears in requirements.

`requirements.txt` is the original dependency file. The export depends on TestMu bindings and a vision API for the semantic assertion.

`env.example` is a sanitized template. Put real credentials in local environment variables or CI secrets. Do not commit `.env`.

For dependency installation (does not start cloud testing):

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

After fixing the omitted test coverage and configuring the provider environment, the generated entry is `python test.py`. This command has not been validated locally in this demonstration. Running it may call TestMu services and consume credits.

## Git maintenance

Review changes to `test.py`, `requirements.txt`, and the suite manifest in Git. Retain the TC ID and export version to map code to Test Manager. A Git edit is not automatically imported back into the Test Manager case. Native Create PR is a separate Beta feature, unavailable in this account at inspection time.
