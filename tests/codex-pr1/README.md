# Codex + Kane CLI: PR #1 regression suite

Codex generated these tests by directly reading the PR diff and the related
repository source. No manually prepared change-summary document was supplied
to the generator. The test files are the generated output.

## Source provenance

- PR: https://github.com/boboeree/ai-native-quality-validation-sample/pull/1
- Base: `b77e5928f48ea3d2a23e5a7a40b21b00fad73883`
- Tested head: `9f74d4896fcc0f94535d762c86a7b459b2fbf368`
- `frontend/src/pages/Home.tsx`: Budget maxPrice 300 → 150, category switching
  resets currentPage, result summaries and pagination.
- `frontend/src/services/mock/mockListingService.ts`: inclusive price filter,
  filter-before-pagination order and total/pages calculation.
- `frontend/src/data/mockData.ts`: 46 listings; eligible prices 120 and 145;
  165 is the nearest excluded price. No exact $150/$151 fixture exists, so
  this suite does not claim exact-boundary fixture coverage.
- `frontend/src/services/listingService.ts` and `.github/workflows/`: Pages
  preview uses the mock service. This run covers preview UI, not the backend API.
- `frontend/src/components/ListingCard.tsx`: visible city/state and nightly price.

## Execute

From the repository root, with Kane CLI 0.8.23 and your own authorized login:

```sh
kane-cli whoami
kane-cli config project 01M4Z35ACC422PBAYF8WTX10HF
kane-cli config folder 01M4Z36KFEZDKWBKS41WJYWFSF
kane-cli testrun run --tags codex-pr1 --parallel 1 --dry-run --agent
kane-cli testrun run --tags codex-pr1 --parallel 1 --headless --no-adaptive-heal --on-failure fail-fast --name codex-pr1-source-suite --stream-members --agent
```

Run the same command again to verify cached replay. A changed step re-authors
that step and its following steps; `--no-adaptive-heal` prevents silently
re-authoring a failing replay. Keep `_test.md` and the complete `output-*` directories in Git, including both
`Result.md` (step hash/status) and `.internal/` (recordings and TMS identity).
Omitting Result.md caused a fresh clone to author again during this demo.
Keep credentials, raw evidence, logs and browser profiles out of Git.

Kane CLI uploads cases and suite results to Test Manager. Git branch/commit/PR
creation and the PR result comment in this demo are performed by Codex through
Git/GitHub, not by an implicit Kane CLI Git integration.
