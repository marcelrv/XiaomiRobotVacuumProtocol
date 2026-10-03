"""Shared helpers for build_enums.py: load the constant-table dump of a bundle and resolve localisation references."""
import json
import os
import re

import bundlelib as B


class BundleEnums:
    def __init__(self, enum_dir, corpus, bundle_id):
        self.id = bundle_id
        model, _, h = bundle_id.partition('@')
        self.model = model
        with open(os.path.join(enum_dir, bundle_id + '.json'), encoding='utf-8') as fh:
            self.tables = json.load(fh)
        self.android = B.android_dir(corpus, model, h or None)
        self._en = None

    @property
    def en(self):
        if self._en is None:
            self._en = B.load_strings(self.android, 'en')
        return self._en

    def find(self, name=None, pred=None, kind=None):
        out = []
        for t in self.tables:
            if name is not None and t['name'] != name:
                continue
            if kind and t['kind'] != kind:
                continue
            if pred is not None and not pred(t):
                continue
            out.append(t)
        return out

    def text(self, v):
        """Resolve a value produced by extract_enums.mjs to display text (English) where it is a string reference."""
        if isinstance(v, dict) and '$ref' in v:
            key = v['$ref'].split('.')[-1]
            if key in self.en:
                return self.en[key]
            return None
        if isinstance(v, str):
            return v
        return None

    def ref_key(self, v):
        if isinstance(v, dict) and '$ref' in v:
            return v['$ref'].split('.')[-1]
        return None
