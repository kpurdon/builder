#!/usr/bin/env python3
"""Check or explicitly install Builder's native Codex agent definitions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


AGENTS = Path(__file__).resolve().parents[3] / 'agents'
SOURCES = {name: AGENTS / (name + '.toml') for name in ['watcher', 'collector']}
MARKER = b'# builder-managed-sha256: '


def digest(content):
    return hashlib.sha256(content).hexdigest().encode('ascii')


def inspect(target, source):
    if target.is_symlink():
        return 'conflict', None
    try:
        content = target.read_bytes()
    except FileNotFoundError:
        return 'missing', None
    header, separator, payload = content.partition(b'\n')
    if not separator or not header.startswith(MARKER):
        return 'unmanaged', content
    if header[len(MARKER):] != digest(payload):
        return 'modified', content
    return ('current' if payload == source else 'stale'), content


def manage(action, agents_dir, source_path):
    source = source_path.read_bytes()
    target = agents_dir / source_path.name
    status, previous = inspect(target, source)
    outcome = {'status': status, 'target': str(target), 'source_sha256': digest(source).decode()}
    if action == 'check' or status in {'conflict', 'unmanaged', 'modified'}:
        return outcome
    if action == 'remove':
        if status != 'missing':
            # Never follow a replaced symlink or delete a file edited since inspection.
            if target.is_symlink() or target.read_bytes() != previous:
                return {**outcome, 'status': 'conflict'}
            target.unlink()
        return {**outcome, 'status': 'removed'}
    if status == 'current':
        return outcome
    agents_dir.mkdir(parents=True, exist_ok=True)
    content = MARKER + digest(source) + b'\n' + source
    with tempfile.NamedTemporaryFile(dir=agents_dir, prefix='.builder-agent-', delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(content)
            output.flush()
            if status == 'missing':
                # Publish a complete file without replacing anything created meanwhile.
                try:
                    os.link(temporary, target)
                except FileExistsError:
                    return {**outcome, 'status': 'conflict'}
            else:
                if target.is_symlink() or target.read_bytes() != previous:
                    return {**outcome, 'status': 'conflict'}
                os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    return {**outcome, 'status': 'installed' if status == 'missing' else 'updated'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'install', 'remove'])
    parser.add_argument('--agents-dir', type=Path, required=True,
                        help='Explicit user CODEX_HOME/agents or project .codex/agents directory')
    parser.add_argument('--agent', choices=SOURCES, action='append',
                        help='Select a role; repeat as needed. Defaults to all bundled roles.')
    args = parser.parse_args()
    outcomes = []
    for name in dict.fromkeys(args.agent or SOURCES):
        try:
            outcome = manage(args.action, args.agents_dir.expanduser().absolute(), SOURCES[name])
        except OSError as exc:
            outcome = {'status': 'error', 'reason': str(exc)}
        outcomes.append({'agent': name, **outcome})
    # Keep the single-role response useful when an agent is selected explicitly.
    success = all(item['status'] in {'current', 'installed', 'updated', 'removed'} for item in outcomes)
    print(json.dumps(outcomes[0] if len(outcomes) == 1 else
                     {'status': 'ok' if success else 'needs_attention', 'agents': outcomes}))
    return 0 if success else 1



if __name__ == '__main__':
    raise SystemExit(main())
