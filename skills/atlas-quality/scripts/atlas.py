#!/usr/bin/env python3
"""Small, dependency-free evidence helper. Does not interpret test output."""
import argparse
import datetime as dt
import json
import math
import pathlib
import subprocess
import sys
import time
import uuid


def revision(project):
    def git(*args):
        try:
            return subprocess.check_output(
                ['git', '-C', str(project), *args], stderr=subprocess.DEVNULL,
                timeout=5, text=True).strip()
        except (OSError, subprocess.SubprocessError):
            return None
    head = git('rev-parse', 'HEAD')
    status = git('status', '--porcelain')
    return {'head': head, 'dirty': None if status is None else bool(status)}


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0 or number > 3600:
        raise argparse.ArgumentTypeError('timeout must be > 0 and <= 3600 seconds')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    init = sub.add_parser('init', help='create missing quality record files only')
    init.add_argument('--project', required=True)
    run = sub.add_parser('run', help='record a command or a user-requested skip')
    run.add_argument('--project', required=True)
    run.add_argument('--label', required=True, help='non-sensitive check name')
    run.add_argument('--timeout', type=positive, default=120)
    run.add_argument('--skip', action='store_true')
    run.add_argument('--reason', default='not supplied')
    run.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    project = pathlib.Path(args.project).resolve()
    if not project.is_dir():
        parser.error('project must be an existing directory')
    if args.action == 'init':
        folder = project / 'docs' / 'quality'
        folder.mkdir(parents=True, exist_ok=True)
        for name, title, prompt in [
            ('system-map.md', 'System map', 'Record observed components, sources, boundaries and unknowns.'),
            ('decisions.md', 'Quality decisions', 'Record consequential rules, rationale and revisit conditions.'),
            ('changes.md', 'Change evidence', 'Link requirements, revisions, risks, checks and remaining work.')]:
            try:
                with (folder / name).open('x', encoding='utf-8') as file:
                    file.write(f'# {title}\n\n{prompt}\n')
            except FileExistsError:
                pass
        print(folder)
        return 0
    command = args.command
    if command[:1] == ['--']:
        command = command[1:]
    if args.skip and command:
        parser.error('--skip cannot be combined with a command')
    if not args.skip and not command:
        parser.error('provide a command after -- or use --skip')
    # Capture the revision before creating evidence files.
    record = {'schema_version': 1, 'id': str(uuid.uuid4()),
              'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'label': args.label, 'revision': revision(project),
              'status': 'skipped' if args.skip else 'incomplete',
              'exit_code': None, 'output_captured': False,
              'interpretation': 'No test or security verdict is inferred.'}
    start = time.monotonic()
    result_code = 2
    if args.skip:
        record['reason'] = args.reason
        result_code = 2
    else:
        try:
            # No shell; no saved output or arguments. The command may itself create artifacts.
            result = subprocess.run(command, cwd=project, timeout=args.timeout,
                                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL, shell=False)
            record['exit_code'] = result.returncode
            record['status'] = 'executed' if result.returncode == 0 else 'failed'
            result_code = 0 if result.returncode == 0 else 1
        except subprocess.TimeoutExpired:
            record['status'] = 'incomplete'
            record['error'] = 'deadline exceeded; check for descendant processes'
        except OSError:
            record['status'] = 'blocked'
            record['error'] = 'command could not start; check executable and permissions'
    record['duration_seconds'] = round(time.monotonic() - start, 3)
    destination = project / '.atlas' / 'runs' / record['id']
    destination.mkdir(parents=True, exist_ok=False)
    path = destination / 'result.json'
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(path)
    return result_code


if __name__ == '__main__':
    sys.exit(main())
