# flutter-clean-build-skill

OpenClaw skill for finding and cleaning Flutter project `build` directories under a root folder such as `~/Develop`.

## Contents

- `flutter-clean-build/` — skill source
- `flutter-clean-build.skill` — packaged skill artifact

## Main script

```bash
python3 flutter-clean-build/scripts/clean_flutter_builds.py --root ~/Develop --action list
python3 flutter-clean-build/scripts/clean_flutter_builds.py --root ~/Develop --action trash
python3 flutter-clean-build/scripts/clean_flutter_builds.py --root ~/Develop --action delete
```
