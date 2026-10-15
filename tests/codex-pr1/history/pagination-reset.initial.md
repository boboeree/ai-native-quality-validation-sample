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
On the preview home page, scroll to pagination and click Next once. Assert the
listing summary reads "46 total properties (Page 2 of 3)"; whitespace can differ.
Do not parse all digits in this string as one number. Stay on the preview and
do not sign in, open listings, book, or modify data.

## Budget resets the page before filtering
Scroll up to the categories and click Budget. Assert the heading is "Budget
properties", the summary is "2 total properties", and the Brooklyn $120 and
Scottsdale $145 property cards are both visible. Assert "No listings found" is
absent. This checks that switching from page 2 resets pagination to page 1.

## All restores page one and unrestricted prices
Click All. Assert the heading is "Explore stays" and the summary reads
"46 total properties (Page 1 of 3)"; whitespace can differ. Assert Austin, Texas
at $275 per night is present again. Use DOM text and do not open a listing.
