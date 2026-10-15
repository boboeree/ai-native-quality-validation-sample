---
assurance:
  id: t-2
  base: sha256:f4d972b151501c6b7109df06651d0b91234dc8be8a7145542637cbc5d18babe3
---
# Budget category shows exactly the two eligible preview listings

> Select Budget on the public preview home page without search filters and prove its heading, summary, exact two-card result set, and visible nightly-price ceiling.

## Step 1

At https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/, reach the public preview home page with no search filters active.

## Step 2 @verifies ac-1, ac-2, ac-3, ac-4, ac-5

On the public preview home page, select the visible Budget category and inspect the results heading, summary, DOM text of every visible listing card, and Budget button DOM classes; then assert the heading is exactly "Budget properties", the summary is exactly "2 total properties", the complete visible card set is exactly Brooklyn, New York at $120 per night and Scottsdale, Arizona at $145 per night with no additional cards, every visible listing-card nightly price is at most $150, and the Budget button's DOM class list contains `bg-gray-100 border-b-2 border-gray-900`.

## Step 3 — explicit no-additional-cards check @verifies ac-2

On the already Budget-filtered page, locate the common listings-grid container that owns the listing cards. Read its current DOM descendants with `grid.querySelectorAll('.cursor-pointer.group')`, filter by `getClientRects().length > 0`, and assert the resulting numeric length is exactly 2. Implement the extraction with a fresh selector query rooted at the grid container (or document), for example `Array.from(grid.querySelectorAll('.cursor-pointer.group')).filter(e => e.getClientRects().length > 0).length`. Do NOT use an array of individually grounded card elements such as `[el(31), el(44)]`: that array has fixed membership and cannot detect an unexpected third card. Do not use city-name locators or the summary text to count cards. This is the original exact-two-cards/no-additional-cards requirement; no business condition is changed.
