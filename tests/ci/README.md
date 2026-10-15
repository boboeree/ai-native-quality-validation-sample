# GitHub Actions: actual Kane CLI replay proof

This isolated demonstration branch runs two committed UI tests and verifies both
execution and Test Manager upload. It does not change application code, merge a
PR, authorize a GitHub App, provision cloud machines, or schedule recurring runs.

1. Repository Settings → Secrets and variables → Actions → New repository secret.
   The repository owner supplies `LT_USERNAME` and `LT_ACCESS_KEY` from their
   TestMu dashboard Credentials. Do not paste credentials into a PR or log.
2. Push this workflow to `qa/actions-proof-20261015`. Its push trigger is restricted
   to this exact branch and the workflow/test paths. No default-branch change is
   required. For an already-created run, choose **Re-run all jobs** after secrets
   are configured. `workflow_dispatch` is included for future manual invocation;
   GitHub may not offer Run workflow until the file is on the default branch.
3. Open Actions → **Kane UI suite proof** → the latest run. Confirm checkout SHA,
   CLI 0.8.23, Chrome version, and the two-test preflight plan.
4. Inspect **Run cached suite**. Only this step receives the two TestMu secrets.
   It passes them to the documented Basic Auth flags, runs without a TTY, uses a
   420-second process timeout and 12-minute job timeout, and saves sanitized logs.
   Missing secrets stop before any browser test is launched.
5. Inspect **Publish separate execution and upload results**. Test success
   requires CLI exit 0, a `testrun_done` event, exactly 2 passes, and zero failed,
   broken, skipped, or authored cases. Upload independently requires `upload: ok`.
6. Download **kane-ui-proof-RUN_ID-ATTEMPT** from Artifacts. It contains the plan,
   sanitized NDJSON, result.json, summary.md and sealed `.evidence` pack if created.
   No CLI profiles/credentials or browser-profile directory is archived.
7. Open Test Manager → project → Test Runs, find `github-actions-RUN_ID`, and match
   the execution ID from result.json. Verify both instances and their assertions.
8. Review this workflow/scripts through Git. The two existing `_test.md` files and
   complete replay caches remain the source suite. Commits and workflow statuses
   give traceability; PR result commentary is handled separately by Codex.

The public preview target is PR #1. The suite assets do not claim testing the
current branch's application code. Full replay depends on the committed cache,
Chrome/platform compatibility and access to TestMu services. Failures are evidence,
not silently repaired: adaptive heal is off and all two members are attempted.

Official references:
- https://www.testmuai.com/docs/kane-cli-cicd
- https://www.testmuai.com/docs/kane-cli-authentication
- https://www.testmuai.com/docs/kane-cli-testrun
- https://www.testmuai.com/docs/kane-cli-installation
