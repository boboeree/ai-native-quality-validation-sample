"""Run once, sanitize evidence, retain pytest's nonzero exit code."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, quote_plus
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent.resolve()
OUT = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)


def sanitize(value):
    for key in ("LT_USERNAME", "LT_ACCESS_KEY"):
        secret = os.environ.get(key, "")
        if secret:
            for form in (secret, quote(secret), quote_plus(secret)):
                value = value.replace(form, "[REDACTED]")
    return re.sub(r"wss://cdp\.lambdatest\.com/playwright\?[^\s<>]+", "[CLOUD_ENDPOINT_REDACTED]", value)


result = subprocess.run([sys.executable, "-m", "pytest", str(ROOT / "test_budget.py"),
    "--junitxml=" + str(OUT / "junit.xml")], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = sanitize(result.stdout)
print(log)
(OUT / "pytest.log").write_text(log)
for path in OUT.glob("*.xml"):
    path.write_text(sanitize(path.read_text()))
summary = {"pytest_exit_code": result.returncode, "expected_demo_outcome": "1 passed, 1 controlled assertion failed; CI must remain failed"}
try:
    suites = ET.parse(OUT / "junit.xml").getroot()
    summary["junit"] = [{k: s.get(k) for k in ("tests", "failures", "errors", "skipped")} for s in suites.findall("testsuite")]
except (OSError, ET.ParseError):
    summary["junit"] = "unavailable"
(OUT / "exit-code.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
sys.exit(result.returncode)
