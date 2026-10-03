"""Generated page docs/appendix/legacy-captures.md: every fenced example (requests and replies) of the old documentation pages,
read from git history (the legacy ref of make_stubs.py), labelled "legacy capture (unverified)".
Personal identifiers (device token, MAC addresses, serial numbers) are replaced by placeholders."""
import re

import make_stubs as MS

MAC = re.compile(r'\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b')
TOKEN = re.compile(r'("token"\s*:\s*")[0-9a-fA-F]{32}(")')
SERIAL = re.compile(r'("serial_number"\s*:\s*")[^"]*(")')
HEAD = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')


def clean(t):
    t = TOKEN.sub(r'\1<32 hex digits>\2', t)
    t = SERIAL.sub(r'\1<serial number>\2', t)
    t = re.sub(r'(roboroommap%22)[0-9]+', r'\1<id>', t)
    t = re.sub(r'("ssid"\s*:\s*")[^"]*(")', r'\1<SSID>\2', t)
    t = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '<IP address>', t)
    t = re.sub(r'"\d{11,13}"', '"<room id>"', t)
    return MAC.sub('<MAC address>', t)


def run(ctx, G):
    ref = 'be636c7'
    L = ['# Legacy captures', '', '[Home](../../README.md) / [Appendix](index.md) / Legacy captures', '',
         'The request and reply examples of the pre-existing pages of this repository (commit `%s`), kept as **legacy captures (unverified)**: no bundle contains robot replies, '
         'so these are the only real-device samples. Device token, MAC addresses, IP addresses, Wi-Fi names, room ids and serial numbers were replaced by placeholders. The current reference for every call is linked in the heading; '
         'where a legacy example differs from what the app code shows, the command page says so.' % ref, '']
    for name in sorted(MS.MAP):
        if name == 'Protocol.md':
            continue
        text = MS.git_show(ref, name)
        lines = text.splitlines()
        title = next((l[2:].strip() for l in lines if l.startswith('# ')), name)
        default = MS.MAP[name][0]
        blocks = []
        head = ''
        i = 0
        while i < len(lines):
            l = lines[i]
            m = HEAD.match(l)
            if m:
                head = m.group(2)
            if l.lstrip().startswith('```'):
                lang = l.strip()[3:].strip() or 'text'
                j = i + 1
                body = []
                while j < len(lines) and not lines[j].lstrip().startswith('```'):
                    body.append(lines[j])
                    j += 1
                blocks.append((head, lang, '\n'.join(body)))
                i = j
            i += 1
        if not blocks:
            continue
        L += ['## %s' % title, '', 'Now documented in [%s](../../%s) (old page: [`%s`](../../%s)).' % (default, default, name, name), '']
        for head, lang, body in blocks:
            L += ['**Example — legacy capture (unverified)**' + ('' if re.match(r'(?i)example', head) else ' — %s' % head), '', '```%s' % lang, clean(body).rstrip(), '```', '']
    L += ['## See also', '', '- [Corrections](corrections.md)', '- [Command index](../commands/index.md)', '']
    G.OUT['docs/appendix/legacy-captures.md'] = '\n'.join(L)
