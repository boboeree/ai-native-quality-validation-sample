# Execution oracle repair for this public preview only

The test requirements and all five ACs remain unchanged. The old recording
incorrectly compared an unconstrained visual prose answer to a long exact string.
This author run must fix the extraction contract, not relax the expected result.

Use DOM extraction and deterministic JavaScript for every asserted fact. Do not
use visual/prose extraction for these DOM-readable values, and do not treat any
nonempty natural-language answer as true. Missing elements must fail the check.

The actual preview renders listing cards as `.cursor-pointer.group`. Each card
has an `h3` city/state and a `div.pt-1 > span` containing the dollar price. These
selectors come from ListingCard.tsx and were independently exercised by the
pytest suite. Count every visible card, not just matching cards; extra cards fail.

Retain five explicit checks and combine them with AND:
1. The visible h2 is exactly `Budget properties`.
2. The result summary text is exactly `2 total properties`.
3. Exactly two visible `.cursor-pointer.group` cards exist, and their sorted
   `[cityState, nightlyPrice]` tuples are exactly
   `[["Brooklyn, New York",120],["Scottsdale, Arizona",145]]`.
4. Every visible card has a finite numeric nightly price at most 150. An empty
   card collection must fail, and card prices must be extracted, not assumed.
5. The visible button whose text ends in Budget has all three class tokens
   `bg-gray-100`, `border-b-2`, `border-gray-900`.

The exact set check may use a DOM-derived JSON string or a boolean expression
with expected true. Its value must be derived from the current page. Keep
separate count and tuple checks if needed; never delete the no-additional-cards
requirement, price limit, heading, summary, or selected-category class checks.
