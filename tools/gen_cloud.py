"""Generated page docs/commands/cloud.md: cloud and smart-home calls of the plugins (not miIO RPCs).
Sources: data/cloud_calls.json (tools/js/extract_cloud_calls.mjs), tools/curated/cloud_calls.yaml."""
import os

import yaml


def run(ctx, G):
    data = G.load_json('cloud_calls.json')['calls']
    cur = yaml.safe_load(open(os.path.join(G.CUR, 'cloud_calls.yaml'), encoding='utf-8'))
    total = len(ctx.all_models)
    L = ['# Cloud and smart-home calls (not miIO)', '', '[Home](../../README.md) / [Commands](index.md) / Cloud calls', '',
         'Besides the miIO RPCs of the [command reference](index.md), the plugins call services of the Mi Home plugin SDK and the Xiaomi cloud. '
         'These are **cloud only**: an integrator that talks to the robot over the local network cannot use them, and none of them is a robot method. '
         'They are listed because they explain behaviour that otherwise looks like a robot feature (map download addresses, account-side timers, stored settings). '
         'Generated from [`data/cloud_calls.json`](../../data/cloud_calls.json) (`tools/js/extract_cloud_calls.mjs`) and `tools/curated/cloud_calls.yaml`; evidence tag ✅ Bundle for every row.', '',
         '| Call | Kind | What the app does with it | Present in |', '|---|---|---|---|']
    from gen_reference import presence
    for c in data:
        if c['kind'] == 'endpoint':
            continue
        nm = c['name']
        desc = cur['service'].get(nm) or cur['helper'].get(nm) or ''
        if nm.startswith('callSmartHomeAPI(/'):
            desc = 'Passes the path to the SDK helper (no-op, see below).'
        L.append('| `%s` | %s | %s | %s |' % (nm, 'SDK service' if c['kind'] == 'service' else 'SDK helper', desc, presence(G, ctx, c['models'])))
    ep = [c for c in data if c['kind'] == 'endpoint']
    L += ['', '## Smart-home endpoint paths named in the code', '', '| Path | Present in |', '|---|---|']
    for c in ep:
        L.append('| `%s` | %s |' % (c['name'], presence(G, ctx, c['models'])))
    L += ['', cur['note'], '', '## See also', '', '- [Transports and dispatch](../concepts/transports.md)', '- [Maps overview](../concepts/maps-overview.md)', '- [Command index](index.md)', '']
    G.OUT['docs/commands/cloud.md'] = '\n'.join(L)
