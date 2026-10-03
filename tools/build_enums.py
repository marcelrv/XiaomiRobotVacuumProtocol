#!/usr/bin/env python3
"""Build data/enums.json from the constant-table dumps of js/extract_enums.mjs.

usage: python build_enums.py --corpus <corpus> --enums <dir with <bundleId>.json> --out ../data/enums.json

Only the *best* bundle of each model is used for presence statements; regional variants are listed separately
(`variants`) so that differences between regional builds are visible.

Tables are located by *signature* (their key set) rather than by variable name, because four bundles are minified and
their local variable names are lost; property names survive minification.
"""
import argparse
import collections
import json
import os
import re
import sys

import bundlelib as B
import enumlib as E

# ---- simple integer/string enums: output name -> (required keys, optional description)
SIMPLE = {
    'ModeConstants':           (['CustomCleanMode', 'CustomWaterMode', 'CustomMopMode'], 'mode code constants of the app (custom fan / water / mop modes, route modes)'),
    'CleanSettingMode':        (['SilentClean', 'StandardClean', 'StrongClean', 'MaxClean'], 'fan power presets of the cleaning-mode picker (set_custom_mode / customize modes)'),
    'WaterSettingMode':        (['NoWater', 'LowWater', 'MediumWater', 'HighWater'], 'water flow presets of the picker (water_box_mode)'),
    'MopSettingMode':          (['Normal', 'Intensive'], 'mop route modes (mop_mode)'),
    'GarnetMopMode':           (['Dry', 'Normal', 'Wet'], 'wet/dry mop modes of the Garnet product line'),
    'CarpetCleanMode':         (['CarpetDynamicAdaptionMode', 'CarpetIgnoreMode', 'CarpetSelfAdaptionMode', 'CarpetAvoidMode'], 'carpet handling modes (set_carpet_clean_mode)'),
    'DustCollectionMode':      (['DustCollectionModeSmart', 'DustCollectionModeQuick', 'DustCollectionModeDaily', 'DustCollectionModeStrong'], 'auto-empty (dust collection) modes'),
    'WashTowelMode':           (['WashTowelModeQuick', 'WashTowelModeDaily', 'WashTowelModeDeep'], 'mop washing modes of the dock (set_wash_towel_mode)'),
    'BackWashMode':            (['BackWashModeSmart', 'BackWashModeCustom', 'BackWashModeLevel'], 'back-wash (mid-clean mop washing) modes'),
    'MoppingType':             (['MOPPING_TYPE_NONE', 'MOPPING_TYPE_PURE'], 'mopping type of a clean task'),
    'DockType':                (['Other', 'Normal'], 'dock type classes seen by the app'),
    'InCleaningStatus':        (['COMPLETE', 'GLOBAL_CLEAN_NOT_COMPLETE', 'ZONE_CLEAN_NOT_COMPLETE', 'SEGMENT_CLEAN_NOT_COMPLETE'], 'values of the in_cleaning status field'),
    'CleanResumeFlag':         (None, 'clean_resume codes (see CleanResumeFlagCodeMap)'),
    'UnsaveMapReason':         (['Saved', 'ChargerOffset', 'Relocation', 'ReachMaxFloorCount'], 'reasons why a map was not saved'),
    'UnsaveMapHandle':         (['Ignore', 'Update', 'Load', 'Done'], 'handling of an unsaved map'),
    'SpecialInfoType':         (['Timer', 'DryRemainTime', 'PureClean', 'PureMop'], 'special info banner types shown on the main screen'),
    'RRHomeSecStatus':         (['RRHomeSecStatusDisconnected', 'RRHomeSecStatusConnected'], 'home-security (camera) connection status'),
    'LogLevel':                (['None', 'BlackBox', 'Pickup', 'Full'], 'log upload levels (enable_log_upload)'),
    'privacyName':             (['PN_NONE', 'PN_CN', 'PN_GENERAL', 'PN_EU'], 'privacy policy region codes sent with enable_log_upload'),
    'OperatorCode':            (['OPERATOR_NONE', 'OPERATOR_CN', 'OPERATOR_NOT_CN'], 'operator codes'),
    'mapOpErrorCode':          (['VENDOR_ERROR_CODE', 'PROCESS_BUSY_ERROR_CODE', 'ERROR_ACCESS_DENIED'], 'error codes returned by map operations'),
    'MapStatusCodeMap':        (None, 'map_status codes'),
    'CleanRectType':           None, 'DoorSillType': None, 'FbzType': None, 'FurnitureType': None,
    'RepeatMode':              (['Once', 'Everyday', 'Weekdays', 'Weekends'], 'timer repeat modes (UI)'),
    'customCleanTimeList':     None,
}
SIMPLE = {k: v for k, v in SIMPLE.items() if v}


def numeric(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def find_by_keys(be, keys, kind='object'):
    out = []
    for t in be.tables:
        if t['kind'] != kind or not isinstance(t['value'], dict):
            continue
        if all(k in t['value'] for k in keys):
            out.append(t)
    return out


def is_state_table(t):
    v = t['value']
    if t['kind'] != 'object' or len(v) < 12:
        return False
    sample = list(v.values())[:6]
    return all(isinstance(x, dict) and 'name' in x and 'value' in x for x in sample) and any('UNKNOWN' in json.dumps(x) for x in v.values())


def is_error_table(t):
    v = t['value']
    if t['kind'] != 'object' or len(v) < 15:
        return False
    return any(k.lstrip('-').isdigit() and isinstance(x, list) and x and x[0] in ('OK', 'Laser', 'Bumper', 'Drop') for k, x in v.items())


def cond_text(be, v):
    """Resolve a string / ref / {$cond: [test, a, b]} node to text, keeping conditional alternatives."""
    if isinstance(v, dict) and '$cond' in v:
        test, a, b = v['$cond']
        return dict(cond=test[:60], then=cond_text(be, a), otherwise=cond_text(be, b))
    if isinstance(v, dict) and '$ref' in v:
        return be.text(v) if be.text(v) is not None else '{' + v['$ref'].split('.')[-1] + '}'
    if isinstance(v, str):
        return v
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--enums', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    index = B.load_index(args.corpus)

    states = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
    errors = collections.defaultdict(lambda: collections.defaultdict(set))   # code -> json(entry) -> bundles
    simple = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
    code_maps = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
    resume = collections.defaultdict(lambda: collections.defaultdict(set))
    fan_tables = collections.defaultdict(lambda: collections.defaultdict(set))
    text_tables = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))   # table -> code -> text -> bundles
    video_errors = collections.defaultdict(lambda: collections.defaultdict(set))                                      # name -> (code, text) -> bundles
    for model in sorted(index):
        be = E.BundleEnums(args.enums, args.corpus, model)
        mshort = model
        # ---- states
        cands = be.find(pred=is_state_table)
        if cands:
            for code, v in cands[0]['value'].items():
                const = v['value'].get('$ref', '?').split('.')[-1] if isinstance(v['value'], dict) else str(v['value'])
                states[int(code)][const][be.text(v['name']) or ''].add(mshort)
        # ---- errors
        # every table of this shape counts (the main `Errors` table and, in the a01 family, `ErrorsCodeToastMap` with extra codes)
        for cand in be.find(pred=is_error_table):
            for code, arr in cand['value'].items():
                if not isinstance(arr, list) or not arr or not isinstance(arr[0], str):
                    continue
                entry = dict(name=arr[0], title=cond_text(be, arr[1]) if len(arr) > 1 else None,
                             subtitle=cond_text(be, arr[2]) if len(arr) > 2 else None,
                             detail=cond_text(be, arr[3]) if len(arr) > 3 else None)
                errors[int(code)][json.dumps(entry, sort_keys=True, ensure_ascii=False)].add(mshort)
        # ---- simple enums by key signature
        for name, (keys, _desc) in SIMPLE.items():
            if not keys:
                continue
            for t in find_by_keys(be, keys):
                for k, x in t['value'].items():
                    if numeric(x) or isinstance(x, str):
                        simple[name][k][json.dumps(x)].add(mshort)
        # ---- code maps keyed by number
        for t in be.tables:
            if t['kind'] != 'object' or not isinstance(t['value'], dict):
                continue
            v = t['value']
            if set(v) >= {'0', '1', '3'} and len(v) == 3 and all(isinstance(x, dict) and '$ref' in x for x in v.values()) and 'None' in json.dumps(v) or (set(v) == {'0', '1', '3'} and 'Has_With' in json.dumps(v)):
                for k, x in v.items():
                    code_maps['MapStatusCodeMap'][k][x['$ref'].split('.')[-1]].add(mshort)
            if set(v) >= {'0', '1', '2', '3'} and 'Global_Clean' in json.dumps(v) and 'Zone_Clean' in json.dumps(v) and len(v) <= 6:
                for k, x in v.items():
                    resume['CleanResumeFlagCodeMap'][k + ':' + x['$ref'].split('.')[-1]].add(mshort)
        # ---- code -> text tables (record start types, finish reasons)
        for tname in ('CleanStartType', 'CleanFinishCleanReasons', 'obstacleNames'):
            for t in be.find(pred=lambda t, tname=tname: t['name'] in (tname, 'return@' + tname) and t['kind'] == 'object'):
                for k, x in t['value'].items():
                    text_tables[tname][k][be.text(x) if isinstance(x, dict) else str(x)].add(mshort)
        for t in be.find(pred=lambda t: t['kind'] == 'object' and isinstance(t['value'], dict) and any(k.startswith('Video_') for k in t['value'])):
            for nm, x in t['value'].items():
                if isinstance(x, dict) and 'code' in x:
                    video_errors[nm][(x['code'], be.text(x.get('resolve')))].add(mshort)
        # ---- fan / clean-mode code tables
        for nm in ('CleanModeMap', 'CleanModeMapOld', 'WaterBoxModeMap', 'FanModel_sapphire', 'FanModel_sapphireCC', 'FanModel_sapphire_liteC_and_liteD'):
            for t in be.find(name=nm, kind='object'):
                val = {k: (be.text(x) if isinstance(x, dict) else x) for k, x in t['value'].items()}
                fan_tables[nm][json.dumps(val, sort_keys=True, ensure_ascii=False)].add(mshort)

    def conv(m):
        return sorted(m, key=lambda x: x)

    out = dict(meta=dict(generator='tools/build_enums.py', note='bundle ids are model ids of the best bundle of each model'),
               states=[], errors=[], simple_enums={}, code_maps={}, clean_resume={}, fan_tables={})
    for code in sorted(states):
        for const, names in sorted(states[code].items()):
            out['states'].append(dict(code=code, constant=const, names=[dict(text=n, bundles=conv(b)) for n, b in sorted(names.items())]))
    for code in sorted(errors):
        out['errors'].append(dict(code=code, entries=[dict(entry=json.loads(e), bundles=conv(b)) for e, b in sorted(errors[code].items())]))
    for name in simple:
        out['simple_enums'][name] = dict(description=SIMPLE[name][1], values={k: [dict(value=json.loads(v), bundles=conv(b)) for v, b in vv.items()] for k, vv in simple[name].items()})
    for name in code_maps:
        out['code_maps'][name] = {k: [dict(value=v, bundles=conv(b)) for v, b in vv.items()] for k, vv in code_maps[name].items()}
    for name in resume:
        out['clean_resume'][name] = [dict(entry=k, bundles=conv(b)) for k, b in resume[name].items()]
    for name in fan_tables:
        out['fan_tables'][name] = [dict(table=json.loads(k), bundles=conv(b)) for k, b in fan_tables[name].items()]
    out['text_tables'] = {n: {k: [dict(text=t, bundles=conv(b)) for t, b in vv.items()] for k, vv in sorted(tt.items(), key=lambda kv: int(kv[0]) if kv[0].lstrip('-').isdigit() else 0)} for n, tt in text_tables.items()}
    out['video_errors'] = {n: [dict(code=c, resolve=t, bundles=conv(b)) for (c, t), b in vv.items()] for n, vv in sorted(video_errors.items(), key=lambda kv: min(c for c, _t in kv[1]), reverse=True)}
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print('states', len(out['states']), 'error codes', len(out['errors']), 'simple enums', len(out['simple_enums']))


if __name__ == '__main__':
    sys.exit(main())
