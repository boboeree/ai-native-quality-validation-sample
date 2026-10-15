---
test: ../pagination-reset_test.md
status: passed
started: 2026-10-15T12:23:54.343Z
duration_s: 177
session_id: 76518dcf-919b-49df-b10e-70c0dd0b5734
---

# PR1 Category changes reset pagination and All restores the list — Result

## Start on the second page ✓ passed (64.7s)
md5: caed6aba6c47d1b11cc6eb72c70bff5f
On the preview home page, scroll to the bottom pagination and click Next once.
Read the page indicator beside the listing count, store its trimmed text as
second_page_indicator, and assert second_page_indicator equals "(Page 2 of 3)".
The indicator is a span, separate from the total count. Read it as text; do not
convert it to a number. Once this assertion passes, finish this step. Stay on
the preview and do not sign in, open listings, book, or modify data.

## Budget resets the page before filtering ✓ passed (51.2s)
md5: 50e8ca18b4ee4f20f2f27a7f25846eb5
Scroll up to the categories and click Budget. Assert the heading is "Budget
properties", the summary is "2 total properties", and the Brooklyn $120 and
Scottsdale $145 property cards are both visible. Assert "No listings found" is
absent. This checks that switching from page 2 resets pagination to page 1.

## All restores page one and unrestricted prices ✓ passed (55.3s)
md5: 933d31776bea24f66b1d26fc4761a3ef
Click All. Assert the heading is "Explore stays". Read the page indicator span
beside the listing count, trim whitespace, and assert it equals "(Page 1 of 3)".
Separately assert the listing summary contains the text "46 total properties".
Assert Austin, Texas at $275 per night is present again. Use DOM text and do not
open a listing. Finish this step when these assertions pass.
