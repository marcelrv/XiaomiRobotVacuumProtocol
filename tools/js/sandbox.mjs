// Minimal Metro module runner used ONLY to evaluate small, pure predicate modules
// (DeviceModelManager / FeatureManager) of a bundle under a chosen device model and chosen runtime flags.
// Everything outside a whitelist of "real" module ids is replaced by an inert Proxy that records whether it was touched.
import vm from 'vm';

export function makeInert(label, touched) {
  const target = function () {};
  const p = new Proxy(target, {
    get(_t, prop) {
      if (prop === Symbol.toPrimitive) return () => 0;
      if (prop === 'then') return undefined;
      if (prop === '__esModule') return true;
      if (prop === 'prototype') return {};
      touched && touched.add(label + '.' + String(prop));
      return makeInert(label + '.' + String(prop), touched);
    },
    apply() { return makeInert(label + '()', touched); },
    construct() { return makeInert(label + '{}', touched); },
    set() { return true; },
    has() { return true; },
  });
  return p;
}

/**
 * mods: array from modload.loadModules; real: Set of module ids that are executed for real.
 * hooks.override(id) may return a replacement exports object for a module id.
 */
export class Runner {
  constructor(mods, real, hooks = {}) {
    this.byId = new Map(mods.map(m => [m.id, m]));
    this.real = real;
    this.cache = new Map();
    this.touched = new Set();
    this.hooks = hooks;
    this.errors = [];
    this.ctx = vm.createContext({ console: { log() {}, warn() {}, error() {}, info() {}, debug() {} }, setTimeout: () => 0, clearTimeout: () => 0, setInterval: () => 0, clearInterval: () => 0 });
    if (hooks.globals) for (const [k, v] of Object.entries(hooks.globals)) this.ctx[k] = v;
  }
  require(id) {
    if (this.cache.has(id)) return this.cache.get(id).exports;
    if (this.hooks.override) { const o = this.hooks.override(id); if (o !== undefined) { this.cache.set(id, { exports: o }); return o; } }
    const m = this.byId.get(id);
    if (!m || !this.real.has(id)) { const inert = makeInert('M' + id, this.touched); this.cache.set(id, { exports: inert }); return inert; }
    const module = { exports: {} };
    this.cache.set(id, module);
    let factory;
    const sandboxDefine = (f) => { factory = f; };
    try {
      const fn = vm.runInContext('(function(__d){' + m.text + '\n})', this.ctx, { timeout: 5000 });
      fn(sandboxDefine);
      const req = (n) => this.require(typeof n === 'number' ? n : n);
      const depMap = m.deps;
      const importDefault = (x) => (x && x.__esModule ? x : { default: x });
      const importAll = (x) => x;
      const g = { __DEV__: false, nativeModuleProxy: makeInert('native', this.touched) };
      if (factory.length >= 7) factory(g, (i) => this.require(i), importDefault, importAll, module, module.exports, depMap);
      else factory(g, (i) => this.require(i), module, module.exports, depMap);
    } catch (e) {
      this.errors.push({ id, error: String(e && e.message || e) });
    }
    return module.exports;
  }
}
