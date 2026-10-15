---
url: https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/
mode: testing
tags: [codex-pr1, budget-regression]
max_steps: 12
timeout: 100
code_export: true
code_language: python
---

# PR1 Category changes reset pagination and All restores the list

## Start on the second page
On the preview home page, scroll to the bottom pagination and click Next once.
Read the page indicator beside the listing count, store its trimmed text as
second_page_indicator, and assert second_page_indicator equals "(Page 2 of 3)".
The indicator is a span, separate from the total count. Read it as text; do not
convert it to a number. Once this assertion passes, finish this step. Stay on
the preview and do not sign in, open listings, book, or modify data.

## Budget resets the page before filtering
Scroll up to the categories and click Budget. Assert the heading is "Budget
properties", the summary is "2 total properties", and the Brooklyn $120 and
Scottsdale $145 property cards are both visible. Assert "No listings found" is
absent. This checks that switching from page 2 resets pagination to page 1.

## All restores page one and unrestricted prices
Click All. Assert the heading is "Explore stays". Read the page indicator span
beside the listing count, trim whitespace, and assert it equals "(Page 1 of 3)".
Separately assert the listing summary contains the text "46 total properties".
Assert Austin, Texas at $275 per night is present again. Use DOM text and do not
open a listing. Finish this step when these assertions pass.
