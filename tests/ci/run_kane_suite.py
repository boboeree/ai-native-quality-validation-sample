"""One bounded, noninteractive two-case Kane CLI invocation. Never log secrets."""
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

out = Path('ci-results')
out.mkdir(exist_ok=True)
result = {'cli_version': '0.8.23', 'sha': os.environ.get('GITHUB_SHA'),
          'expected_tests': 2, 'wall_timeout_seconds': 420}
missing = [key for key in ('LT_USERNAME', 'LT_ACCESS_KEY') if not os.environ.get(key)]
if missing:
    result.update(status='blocked', reason='MissingSecret', missing_secret_names=missing,
                  process_exit_code=None, tests_executed=False, upload='not_attempted')
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print('::error::Missing Actions secrets: ' + ', '.join(missing) + '. No browser test ran.')
    raise SystemExit(2)

# Secret values are passed as arguments to the CLI, never included in printed commands.
command = ['kane-cli', 'testrun', 'run',
           'tests/codex-pr1/budget-threshold_test.md',
           'tests/codex-pr1/pagination-reset_test.md',
           '--parallel', '1', '--headless', '--no-adaptive-heal',
           '--on-failure', 'continue', '--agent', '--stream-members',
           '--name', 'github-actions-' + os.environ.get('GITHUB_RUN_ID', 'local'),
           '--username', os.environ['LT_USERNAME'], '--access-key', os.environ['LT_ACCESS_KEY']]
start = time.monotonic()
process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, start_new_session=True)
try:
    raw, _ = process.communicate(timeout=result['wall_timeout_seconds'])
    timed_out = False
except subprocess.TimeoutExpired:
    timed_out = True
    os.killpg(process.pid, signal.SIGINT)
    try:
        raw, _ = process.communicate(timeout=25)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        raw, _ = process.communicate()

# Redact credentials and URL query strings before persistence; keep full report IDs in summary fields.
for key in ('LT_USERNAME', 'LT_ACCESS_KEY'):
    raw = raw.replace(os.environ[key], '[REDACTED]')
raw = re.sub(r'(https?://[^\s"<>?]+)\?[^\s"<>]*', r'\1?[QUERY_REDACTED]', raw)
(out / 'run.ndjson').write_text(raw)
print(raw, end='')
result.update(process_exit_code=process.returncode,
              elapsed_seconds=round(time.monotonic() - start, 3),
              timed_out=timed_out, status='completed')
(out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
# Result gates below remain separate from collection, including a CLI non-zero exit.
