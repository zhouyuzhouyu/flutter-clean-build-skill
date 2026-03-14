#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

PRUNE_DIRS = {'.git', '.dart_tool', 'build', 'node_modules', 'Pods', '.gradle'}


def is_flutter_project(project_dir: Path) -> bool:
    pubspec = project_dir / 'pubspec.yaml'
    if not pubspec.is_file():
        return False
    try:
        return 'flutter:' in pubspec.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return False


def iter_flutter_build_dirs(root: Path):
    for current_root, dirnames, filenames in __import__('os').walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        current = Path(current_root)
        if 'pubspec.yaml' in filenames and is_flutter_project(current):
            build_dir = current / 'build'
            if build_dir.is_dir():
                yield build_dir


def du_size(path: Path) -> str:
    try:
        out = subprocess.check_output(['du', '-sh', str(path)], text=True)
        return out.split()[0]
    except Exception:
        return 'unknown'


def move_to_trash(path: Path) -> None:
    trash_bin = shutil.which('trash')
    if trash_bin:
        subprocess.run([trash_bin, str(path)], check=True)
        return
    escaped = str(path).replace('\\', '\\\\').replace('"', '\\"')
    subprocess.run(['osascript', '-e', f'tell application "Finder" to delete POSIX file "{escaped}"'], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description='Find and remove build directories inside Flutter projects.')
    parser.add_argument('--root', default='~/Develop', help='Root directory to scan. Default: ~/Develop')
    parser.add_argument('--action', choices=['list', 'trash', 'delete'], default='list', help='list: only show matches; trash: move to Trash; delete: permanently delete')
    parser.add_argument('--json', action='store_true', help='Print JSON output')
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(json.dumps({'error': f'{root} does not exist'}) if args.json else f'ERROR: {root} does not exist')
        return 1

    results = []
    for build_dir in sorted(iter_flutter_build_dirs(root)):
        item = {'path': str(build_dir), 'size': du_size(build_dir), 'status': 'found'}
        if args.action == 'trash':
            move_to_trash(build_dir)
            item['status'] = 'trashed'
        elif args.action == 'delete':
            shutil.rmtree(build_dir)
            item['status'] = 'deleted'
        results.append(item)

    if args.json:
        print(json.dumps({'root': str(root), 'count': len(results), 'items': results}, ensure_ascii=False, indent=2))
    else:
        if not results:
            print(f'No Flutter build directories found under {root}')
        else:
            for item in results:
                print(f"{item['status']}\t{item['size']}\t{item['path']}")
            print(f'Total: {len(results)} build directories')
    return 0


if __name__ == '__main__':
    sys.exit(main())
