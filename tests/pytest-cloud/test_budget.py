"""Authored by Codex from PR1 source; not a native KaneAI code export."""
import re
import pytest
from playwright.sync_api import expect

URL = "https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/"


def budget_cards(page):
    page.goto(URL, wait_until="domcontentloaded")
    expect(page.get_by_role("heading", name="Explore stays", exact=True)).to_be_visible()
    page.get_by_role("button", name=re.compile("Budget")).click()
    expect(page.get_by_role("heading", name="Budget properties", exact=True)).to_be_visible()
    cards = page.locator(".cursor-pointer.group")
    expect(cards).to_have_count(2)
    expect(page.get_by_text("$120", exact=True)).to_be_visible()
    expect(page.get_by_text("$145", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", level=3)).to_have_text(["Brooklyn, New York", "Scottsdale, Arizona"])
    return cards


@pytest.mark.tms("TC-11")
def test_budget_correct_results(cloud_page):
    assert budget_cards(cloud_page).count() == 2


@pytest.mark.tms("TC-12")
def test_controlled_failure_wrong_expected_count(cloud_page):
    actual = budget_cards(cloud_page).count()
    assert actual == 3, f"CONTROLLED_FAILURE: intentionally expected 3; valid actual Budget count is {actual}"
