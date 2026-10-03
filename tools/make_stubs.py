#!/usr/bin/env python3
"""Replace the old root-level documentation pages by short pointer pages (URL stability).

usage: python tools/make_stubs.py [--ref be636c7] [--check]

For every old page (read from git history, so the script can be re-run) it writes a stub with the old title, a pointer
to the new location and the old section headings (so that deep links to old anchors such as `status.md#error-codes`
still land on the page), each heading linking to the best matching new section. The mapping is defined below.
Generic headings (Command, Response, Example) are omitted. `Protocol.md` and the README are not stubs (moved / rewritten).
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = 'docs/commands/'
R = 'docs/reference/'
K = 'docs/concepts/'

# old page -> (default target, {old heading (lower case): target})
MAP = {
    'Protocol.md': (K + 'miio-protocol.md', {}),
    'basic.md': (C + 'cleaning-control.md', {'start cleaning': C + 'cleaning-control.md#app_start', 'stop cleaning': C + 'cleaning-control.md#app_stop',
                                              'start spot cleaning': C + 'cleaning-control.md#app_spot', 'pause cleaning': C + 'cleaning-control.md#app_pause',
                                              'start charging': C + 'cleaning-control.md#app_charge'}),
    'clean_summary+record.md': (C + 'clean-history.md', {'get clean summary (older devices)': C + 'clean-history.md#get_clean_summary', 'get clean summary (newer devices)': C + 'clean-history.md#get_clean_summary',
                                                         'get clean record': C + 'clean-history.md#get_clean_record', 'get clean record map': C + 'clean-history.md#get_clean_record_map'}),
    'consumable.md': (C + 'consumables.md', {'get consumable': C + 'consumables.md#get_consumable', 'reset consumable': C + 'consumables.md#reset_consumable'}),
    'current_sound.md': (C + 'sound.md#get_current_sound', {}),
    'custom_mode.md': (C + 'cleaning-modes.md', {'get custom mode': C + 'cleaning-modes.md#get_custom_mode', 'set custom mode': C + 'cleaning-modes.md#set_custom_mode',
                                                 'regular modes': R + 'fan-water-mop.md#fan-power', 'extended modes': R + 'fan-water-mop.md#fan-power'}),
    'dnd_timer.md': (C + 'timers.md', {'get dnd timer': C + 'timers.md#get_dnd_timer', 'set dnd timer': C + 'timers.md#set_dnd_timer'}),
    'find_me.md': (C + 'cleaning-control.md#find_me', {}),
    'fw_features.md': (K + 'feature-flags.md', {'model - features matrix': K + 'feature-flags.md#legacy-captures', 'list of features functionality': K + 'feature-flags.md#feature-codes',
                                                'command description': C + 'status.md#get_fw_features', 'get firmware features': C + 'status.md#get_fw_features'}),
    'goto_target.md': (C + 'cleaning-control.md#app_goto_target', {}),
    'init_status.md': (C + 'status.md#app_get_init_status', {}),
    'install_sound.md': (C + 'sound.md', {'install sound': C + 'sound.md#dnld_install_sound', 'get sound installation progress': C + 'sound.md#get_sound_progress'}),
    'lab_status.md': (C + 'maps.md#set_lab_status', {}),
    'locale.md': (C + 'status.md#app_get_locale', {}),
    'log_upload.md': (C + 'system.md', {}),
    'map.md': (C + 'maps.md#save_map', {}),
    'map_v1.md': (C + 'maps.md#get_map_v1', {}),
    'miIO-info.md': (K + 'miio-protocol.md#generic-methods', {}),
    'miIO-ota.md': (K + 'miio-protocol.md#generic-methods', {}),
    'miIO-wifi_assoc_state.md': (K + 'miio-protocol.md#generic-methods', {}),
    'multimap.md': (C + 'maps.md#get_multi_maps_list', {'load multimap': C + 'maps.md#load_multi_map'}),
    'network_info.md': (C + 'system.md#get_network_info', {}),
    'rc.md': (C + 'remote-control.md', {'start remote control': C + 'remote-control.md#app_rc_start', 'end remote control': C + 'remote-control.md#app_rc_end',
                                        'movement remote control': C + 'remote-control.md#app_rc_move'}),
    'room_mapping.md': (C + 'rooms-and-areas.md#get_room_mapping', {}),
    'segment_clean.md': (C + 'cleaning-control.md#app_segment_clean', {'start segment cleaning': C + 'cleaning-control.md#app_segment_clean',
                                                                      'stop segment cleaning': C + 'cleaning-control.md#stop_segment_clean', 'resume segment cleaning': C + 'cleaning-control.md#resume_segment_clean'}),
    'serial_number.md': (C + 'status.md#get_serial_number', {}),
    'sound_volume.md': (C + 'sound.md', {'get sound volume': C + 'sound.md#get_sound_volume', 'change sound volume': C + 'sound.md#change_sound_volume',
                                         'test sound volume': C + 'sound.md#test_sound_volume'}),
    'status.md': (C + 'status.md#get_status', {'get status message': C + 'status.md#get_status', 'codes': R + 'states.md', 'status codes': R + 'states.md', 'error codes': R + 'errors.md'}),
    'timer.md': (C + 'timers.md', {'get cleaning timer': C + 'timers.md#get_timer', 'set cleaning timer': C + 'timers.md#set_timer', 'enable/disable cleaning timer': C + 'timers.md#upd_timer'}),
    'timezone.md': (C + 'system.md#get_timezone', {'get timezone': C + 'system.md#get_timezone', 'set timezone': C + 'system.md#set_timezone'}),
    'water_box_custom_mode.md': (C + 'cleaning-modes.md#set_water_box_custom_mode', {'get water box custom mode': C + 'cleaning-modes.md#get_water_box_custom_mode',
                                                                                    'set water box custom mode': C + 'cleaning-modes.md#set_water_box_custom_mode',
                                                                                    'modes': R + 'fan-water-mop.md#water-box-mode', 'levels': R + 'fan-water-mop.md#water-box-mode',
                                                                                    'note': R + 'fan-water-mop.md#notes'}),
    'zoned_clean.md': (C + 'cleaning-control.md#app_zoned_clean', {'start zone cleaning': C + 'cleaning-control.md#app_zoned_clean', 'stop zone cleaning': C + 'cleaning-control.md#stop_zoned_clean',
                                                                    'resume zone cleaning': C + 'cleaning-control.md#resume_zoned_clean'}),
}
SKIP = re.compile(r'^(command|response|example)$', re.I)   # bare skeleton headings only; "Example (s5e)" is a named anchor


def git_show(ref, path):
    return subprocess.run(['git', 'show', '%s:%s' % (ref, path)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', check=True).stdout


def build(ref, name):
    default, over = MAP[name]
    text = git_show(ref, name)
    lines = text.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith('# ')), name)
    out = ['# %s' % title, '', '> **Moved.** This page is now [%s](%s). The old description was merged into the bundle-verified reference; the old request and reply examples are kept in [legacy captures](docs/appendix/legacy-captures.md). This file only keeps the old link and section anchors working.' % (default, default), '']
    for l in lines:
        m = re.match(r'^(#{2,6})\s+(.*?)\s*#*\s*$', l)
        if not m or SKIP.match(m.group(2)):
            continue
        tgt = over.get(m.group(2).lower(), default)
        if name == 'Protocol.md':   # same headings exist in the moved page
            tgt = default + '#' + re.sub(r'\s+', '-', re.sub(r'[^\w\- ]', '', m.group(2).lower()).strip())
        out += ['%s %s' % (m.group(1), m.group(2)), '', 'See [%s](%s).' % (tgt, tgt), '']
    if name == 'fw_features.md':
        out += ['<a id="feature-codes"></a>', '']
    return '\n'.join(out).rstrip('\n') + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='be636c7')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    n = 0
    for name in sorted(MAP):
        text = build(a.ref, name)
        p = os.path.join(ROOT, name)
        old = open(p, encoding='utf-8', newline='').read() if os.path.exists(p) else None
        if old != text:
            n += 1
            if not a.check:
                with open(p, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(text)
    print(('would change' if a.check else 'wrote'), n, 'stubs of', len(MAP))
    return 1 if (a.check and n) else 0


if __name__ == '__main__':
    sys.exit(main())
