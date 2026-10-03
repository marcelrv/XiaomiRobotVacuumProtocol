"""Constructed request examples built from the curated `Request` text of a command.

The first code span of the request text that is a JSON-like literal (`{"volume": <int>}`, `[<map id>]`, ...) is parsed; every
`<placeholder>` is replaced by a realistic literal of the documented type (integers stay integers, flags are 0/1). When a
placeholder has no known type the example is dropped: no example is better than a wrong one.
"""
import json
import re

# value by JSON key (checked first)
KEYVAL = {
    'volume': 50, 'status': 1, 'lock_status': 1, 'map_flag': 0, 'map_index': 0, 'multi_map': 0, 'source': 2, 'mode': 1, 'enable': True, 'record': True,
    'type': 1, 'action': 0, 'sid': 1, 'sver': 1, 'tid': 1, 'zid': 1, 'sid_': 1, 'update': 1, 'level': 9, 'version': 1, 'nonce': -1, 'id': 1,
    'hours': 120, 'timeout': 360, 'distance_off': 20, 'error_code': 1, 'retry_count': 1, 'retry_id': 1, 'length': 4, 'carpet_clean_mode': 0,
    'mop_template_id': 1, 'wash_mode': 0, 'show_index': 1, 'lab_status': 1, 'reserve_map': 0, 'dry_time': 7200, 'keep_seconds': 60,
    'enable_wakeup': 1, 'move_in_place': 1, 'img_id': 1, 'src_type': 1, 'actual_type': 1, 'wash_interval': 3600, 'smart_wash': 0,
    'round': 1700000000000, 'start_time': 1700000000, 'enable_password': 0, 'resume': 1, 'vol': 1, 'led': 1, 'dust': 1, 'dry': 1,
}
# value by placeholder text
TEXTVAL = {
    'int': 1, 'code': 0, 'bool': True, 'seconds': 3600, 'minutes': 60, 'map id': 0, 'id': 1, 'segment id': 16, 'room id': 16, 'pack id': 1, 'task id': 1,
    'photo id': 1, 'tag id': 1, 'start': 1700000000, 'record id': 1700000000, 'mapnonce': -1, 'ms timestamp': 1700000000000, 'name': 'name',
    'tz name': 'Europe/Berlin', 'mcc': 0, 'level': 9, 'int version': 1, '0–4': 1, '0|1|2|8': 0, '0|1': 1, 'v': None,
    'host': 'host.example.invalid', 'start hour': 22, 'start minute': 0, 'end hour': 8, 'end minute': 0,
}
STRVAL = {'https url of the .pkg': 'https://example.invalid/file.pkg', 'tz name': 'Europe/Berlin', 'url': 'https://example.invalid/file.pkg', 'md5 hex': '0123456789abcdef0123456789abcdef', 'md5 of the file': '0123456789abcdef0123456789abcdef', 'name': 'name',
          'original method': 'set_timer', 'string': 'text', 'md5 hex or empty': '', 'host': 'host.example.invalid', 'command string': 'command'}


class Drop(Exception):
    pass


def _value_for(key, text, in_string):
    t = text.strip().lower()
    if in_string:
        if t in STRVAL:
            return STRVAL[t]
        raise Drop(t)
    if key in KEYVAL:
        return KEYVAL[key]
    if t in TEXTVAL and TEXTVAL[t] is not None:
        return TEXTVAL[t]
    raise Drop(t)


def _convert(span):
    s = span
    s = re.sub(r',\s*…\s*(?=[\]}])', '', s)               # "[x, …]" -> "[x]"
    if '…' in s:
        raise Drop('ellipsis')
    s = re.sub(r'"(\w+)"\|"(\w+)"', r'"\1"', s)      # "on"|"off" -> "on"
    s = re.sub(r'(?<![<\w"])0\|1(?![\w>"])', '1', s)
    s = s.replace('0|1|3', '1')
    out, i, key = [], 0, None
    in_str = None
    last_key = None
    while i < len(s):
        c = s[i]
        if in_str:
            if c == '\\':
                out.append(s[i:i + 2])
                i += 2
                continue
            if c == in_str:
                in_str = None
            out.append(c)
            i += 1
            continue
        if c in '"\'':
            in_str = c
            # key detection: "key":
            m = re.match(r'"([^"]+)"\s*:', s[i:])
            if m:
                last_key = m.group(1)
            m2 = re.match(r'"([^"]*<[^>]+>[^"]*)"', s[i:])
            if m2 and re.fullmatch(r'<[^>]+>', m2.group(1)):
                val = _value_for(last_key, m2.group(1)[1:-1], True)
                out.append(json.dumps(val))
                i += m2.end()
                in_str = None
                continue
            out.append('"')
            i += 1
            continue
        if c == '<':
            j = s.index('>', i)
            val = _value_for(last_key, s[i + 1:j], False)
            out.append(json.dumps(val))
            i = j + 1
            continue
        out.append(c)
        i += 1
    txt = ''.join(out)
    return json.loads(txt)


# methods whose first `<int>` is a value with a known sensible range
OVERRIDE = {'change_sound_volume': [50], 'set_custom_clean_time': [3600]}


def example_params(request_text, shapes=None, method=None):
    """params value for the example, or None when no faithful example can be built."""
    if method in OVERRIDE:
        return OVERRIDE[method]
    if request_text:
        t = request_text
        for m in re.finditer(r'`([^`]+)`', t):
            span = m.group(1)
            if span[:1] in '[{' and not span.startswith('[`'):
                try:
                    return _convert(span)
                except (Drop, ValueError, json.JSONDecodeError, IndexError):
                    return None
        if re.search(r'none|no parameters', t[:60], re.I):
            return []
    # no curated request: only literal-only call shapes (`[]`, `{}`) are used
    for sh in shapes or []:
        if sh['kind'] in ('call', 'wrapper') and sh['src'].strip() in ('[]', '{}'):
            return json.loads(sh['src'].strip())
    return None


def example_json(method, params):
    return json.dumps({'id': 1, 'method': method, 'params': params}, ensure_ascii=False)
