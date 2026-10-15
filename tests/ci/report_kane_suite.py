"""Fail closed: require two real passes, a terminal event, and separate upload proof."""
import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--gate', choices=['tests', 'upload'])
args = parser.parse_args()
out = Path('ci-results')
out.mkdir(exist_ok=True)
path = out / 'result.json'
result = json.loads(path.read_text()) if path.exists() else {'status': 'not_run', 'reason': 'SetupFailed'}
events = []
log = out / 'run.ndjson'
if log.exists():
    for line in log.read_text().splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except json.JSONDecodeError:
            pass
summary = next((x for x in reversed(events) if x.get('type') == 'testrun_summary'), {})
done = next((x for x in reversed(events) if x.get('type') == 'testrun_done'), {})
totals = summary.get('totals', {})
tests_ok = (result.get('process_exit_code') == 0 and bool(done)
            and summary.get('execution', {}).get('status') == 'passed'
            and totals.get('tests') == 2 and totals.get('passed') == 2
            and all(totals.get(x, 0) == 0 for x in ('failed', 'broken', 'skipped', 'authored'))
            and not summary.get('cancelled') and not result.get('timed_out'))
upload = summary.get('upload', result.get('upload', 'unknown'))
upload_ok = bool(summary) and upload == 'ok'
result.update(execution=summary.get('execution'), totals=totals, upload=upload,
              terminal_event_seen=bool(done), tests_gate_passed=tests_ok,
              upload_gate_passed=upload_ok)
path.write_text(json.dumps(result, indent=2) + '\n')
markdown = '\n'.join([
    '## Kane UI suite: execution and upload are independent', '',
    f"- Commit: `{result.get('sha', 'unknown')}`",
    f"- CLI: `0.8.23`; exit: `{result.get('process_exit_code')}`; terminal event: `{bool(done)}`",
    f"- Test gate: **{'PASS' if tests_ok else 'FAIL / NOT RUN'}** — `{json.dumps(totals)}`",
    f"- Test Manager upload gate: **{'PASS' if upload_ok else 'FAIL / NOT CONFIRMED'}** — `{upload}`",
    f"- Execution ID: `{summary.get('execution', {}).get('id', 'none')}`",
    f"- Setup reason: `{result.get('reason', 'none')}`",
    '- Replay only: two committed tests, sequential; no adaptive heal; no automatic retry.',
    '- GitHub-hosted Linux Chrome runs the tests. This is not a HyperExecute/real-device run.',
    '- A successful dispatch or completed job alone does not establish test success.', '',
])
(out / 'summary.md').write_text(markdown)
if not args.gate:
    print(markdown)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f:
            f.write(markdown)
else:
    passed = tests_ok if args.gate == 'tests' else upload_ok
    print(f'{args.gate} gate: {"PASS" if passed else "FAIL"}')
    raise SystemExit(0 if passed else 1)
