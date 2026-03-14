---
name: flutter-clean-build
description: Find and clean Flutter project build directories under a root folder such as ~/Develop. Use when the user wants to list, size-check, trash, or permanently delete build folders from many Flutter projects at once, especially to reclaim disk space or batch-clean local development trees.
---

# Flutter Clean Build

Use `scripts/clean_flutter_builds.py` to scan a root directory, detect Flutter projects by `pubspec.yaml`, and operate on each project's `build` directory.

## Workflow

1. Run the script with `--action list` to show matching `build` directories and their sizes.
2. Confirm with the user before destructive cleanup.
3. Prefer `--action trash` over permanent deletion.
4. Use `--action delete` only when the user explicitly wants irreversible removal.

## Commands

```bash
python3 scripts/clean_flutter_builds.py --root ~/Develop --action list
python3 scripts/clean_flutter_builds.py --root ~/Develop --action trash
python3 scripts/clean_flutter_builds.py --root ~/Develop --action delete
```

## Notes

- Treat a directory as a Flutter project only if `pubspec.yaml` contains `flutter:`.
- Report each matched `build` directory with its size.
- Use Trash when possible (`trash` CLI if installed, otherwise Finder delete via AppleScript).
- Prune common heavy directories during traversal for speed: `.git`, `.dart_tool`, `build`, `node_modules`, `Pods`, `.gradle`.
- If the user asks for a machine-readable result, add `--json`.
