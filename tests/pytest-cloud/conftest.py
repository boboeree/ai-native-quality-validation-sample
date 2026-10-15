"""Codex-authored adapter for pytest -> native Playwright cloud -> Test Manager."""
import json
import os
from pathlib import Path
from urllib.parse import quote

import pytest
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "artifacts"
PROJECT = "GitHub PR QA POC 20261015"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + outcome.get_result().when, outcome.get_result())


@pytest.fixture
def cloud_page(request):
    """One connection per test; no retry or additional browser session."""
    OUT.mkdir(exist_ok=True)
    case = request.node.get_closest_marker("tms").args[0]
    for key in ("LT_USERNAME", "LT_ACCESS_KEY"):
        if not os.environ.get(key):
            pytest.fail("Missing required GitHub repository secret: " + key)
    caps = {
        "browserName": "Chrome", "browserVersion": "latest",
        "LT:Options": {
            "platform": "Windows 10", "build": os.environ.get("LT_BUILD", "pytest-cloud-local"),
            "name": case + " " + request.node.name,
            "project": PROJECT, "tms.tc_id": case,
            "user": os.environ["LT_USERNAME"], "accessKey": os.environ["LT_ACCESS_KEY"],
            "video": True, "console": True, "network": True,
            "idleTimeout": 120,
        },
    }
    safe = {"case_id": case, "test": request.node.name, "project": PROJECT,
            "build": caps["LT:Options"]["build"]}
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect(
                "wss://cdp.lambdatest.com/playwright?capabilities=" + quote(json.dumps(caps)), timeout=90000
            )
        except Exception as exc:
            # Playwright connection errors can include the credential-bearing URL.
            raise RuntimeError("Cloud connection failed (" + type(exc).__name__ + "); credential URL suppressed") from None
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.set_default_timeout(20000)
        page.set_default_navigation_timeout(45000)
        try:
            yield page
        finally:
            report = getattr(request.node, "rep_call", None)
            status = "passed" if report and report.passed else "failed"
            safe["pytest_status"] = status
            try:
                try:
                    page.screenshot(path=str(OUT / (case + ".png")), full_page=True, timeout=10000)
                except Exception as screenshot_error:
                    safe["screenshot_error"] = type(screenshot_error).__name__
                controlled = bool(report and "CONTROLLED_FAILURE" in str(report.longrepr))
                remark = "pytest passed" if status == "passed" else ("CONTROLLED_FAILURE: expected 3, actual 2" if controlled else "pytest failed; inspect JUnit for actual failure")
                page.evaluate("_ => {}", "lambdatest_action: " + json.dumps({
                    "action": "setTestStatus", "arguments": {"status": status, "remark": remark}}))
                safe["status_hook"] = "sent"
                details = page.evaluate("_ => {}", 'lambdatest_action: {"action":"getTestDetails"}')
                if isinstance(details, str):
                    details = json.loads(details)
                details = details.get("data", details)
                allowed = ("test_id", "build_id", "name", "platform", "browser", "browser_version", "status_ind", "session_id", "build_name", "create_timestamp", "start_timestamp")
                safe["cloud"] = {k: details[k] for k in allowed if k in details}
            except Exception as exc:
                safe["evidence_error"] = type(exc).__name__
            finally:
                (OUT / (case + "-session.json")).write_text(json.dumps(safe, indent=2))
                browser.close()
