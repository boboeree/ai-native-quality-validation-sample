---
test: ../budget-threshold_test.md
status: passed
started: 2026-10-15T12:18:39.352Z
duration_s: 102
session_id: 7b7b3bf9-cac6-49a4-bb54-4a05c72ec9e3
---

# PR1 Budget threshold excludes formerly eligible stays — Result

## Validate the filtered listing cards ✓ passed (97.3s)
md5: d927a14032b1a7bee649bbb12356246a
On the already-open preview, click the Budget category and wait for the listing
results. Assert the heading is "Budget properties" and the summary is exactly
"2 total properties". Assert the only two property cards are Brooklyn, New York
at $120 per night and Scottsdale, Arizona at $145 per night. Assert no visible
property-card nightly price exceeds $150 (in particular $165, $275, and $280
must not appear as listing prices). Evaluate text and prices in the DOM. Do not
sign in, open a listing, book, modify data, or navigate to another site.
