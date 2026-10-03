#!/usr/bin/env python3
"""Extract the Roborock / Rockrobo model list and the robot enumerations of the openHAB miio binding (cross-check source, NOT truth).

usage: python openhab_models.py --openhab <path to org.openhab.binding.miio> [--ref main] --out ../data/openhab_models.json
The files are read from git (`git show <ref>:<path>`), so the result does not depend on which branch is checked out in the working
tree; the commit hash, commit date and ref are recorded in both output files. Without a git checkout the working-tree files are read
(recorded as ref "working tree").
Reads internal/MiIoDevices.java (enum entries `NAME("model.id", "Name", THING_TYPE_X)`) and internal/robot/{StatusType, VacuumErrorType,
FanModeType, ConsumablesType, DockStatusType}.java -> openhab_models.json and openhab_robot_enums.json (next to --out).
"""
import argparse
import json
import os
import re
import subprocess
import sys

ENUM_RX = re.compile(r'^\s*([A-Z0-9_]+)\("((?:roborock|rockrobo)\.[a-z]+\.[a-z0-9]+)",\s*"([^"]*)",\s*(THING_TYPE_[A-Z_]+)\)', re.M)
ROBOT_ENUMS = ('StatusType', 'VacuumErrorType', 'FanModeType', 'ConsumablesType', 'DockStatusType')
BASE = 'src/main/java/org/openhab/binding/miio/internal/'


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True, encoding='utf-8', check=True).stdout


class Source:
    def __init__(self, binding, ref):
        self.binding = binding
        self.ref = ref
        self.git = None
        try:
            top = git(binding, 'rev-parse', '--show-toplevel').strip()
            self.rel = os.path.relpath(os.path.abspath(binding), top).replace(os.sep, '/')
            self.top = top
            self.commit = git(top, 'rev-parse', ref).strip()
            self.date = git(top, 'log', '-1', '--format=%cs', ref).strip()
            self.git = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.commit, self.date, self.ref = None, None, 'working tree'

    def read(self, rel):
        if self.git:
            return git(self.top, 'show', '%s:%s/%s' % (self.ref, self.rel, rel))
        with open(os.path.join(self.binding, *rel.split('/')), encoding='utf-8') as fh:
            return fh.read()

    def meta(self):
        return dict(ref=self.ref, commit=self.commit, commit_date=self.date)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--openhab', required=True)
    ap.add_argument('--ref', default='main', help='git ref to read (default main)')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    src = Source(args.openhab, args.ref)
    text = src.read(BASE + 'MiIoDevices.java')
    models = {}
    for sym, model, name, thing in ENUM_RX.findall(text):
        models[model] = dict(enum=sym, name=name, thing_type=thing)
    out = dict(source='openHAB miio binding, MiIoDevices.java', openhab=src.meta(), file=BASE + 'MiIoDevices.java', models=dict(sorted(models.items())))
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(models), 'roborock/rockrobo models; openHAB', json.dumps(src.meta()))
    enums = {}
    for name in ROBOT_ENUMS:
        try:
            t = src.read(BASE + 'robot/%s.java' % name)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        enums[name] = {int(v): d for _n, v, d in re.findall(r'^\s*([A-Z_0-9]+)\((-?\d+),\s*"([^"]*)"\)', t, re.M)}
    with open(os.path.join(os.path.dirname(os.path.abspath(args.out)), 'openhab_robot_enums.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(source='openHAB miio binding, internal/robot/*.java', openhab=src.meta(),
                       enums={k: {str(c): d for c, d in v.items()} for k, v in enums.items()}), fh, indent=1, ensure_ascii=False)
    print({k: len(v) for k, v in enums.items()}, 'openHAB robot enumerations')


if __name__ == '__main__':
    sys.exit(main())
