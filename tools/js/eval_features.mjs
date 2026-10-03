// Evaluate the FeatureManager predicates of one bundle for a list of device models, under several runtime scenarios.
//
// usage: node eval_features.mjs <corpus> <rpcDir> <bundleId> <outfile.json> [model,model,...]
//   rpcDir : output folder of extract_rpc.mjs (gives the ids of the FeatureManager / DeviceModelManager modules)
//
// Two code generations exist in the bundles:
//   "dmm"    newer bundles: DeviceModelManager (DeviceInfoMap: model id -> product code name) + FeatureManager
//   "groups" older bundles: FeatureManager asks RRMISDK.isXxx() helpers, each `isModel([...model ids...])`
// The modules are executed in an isolated vm context; react-native, the native bridge and app state are replaced by
// inert proxies. Predicates that touch such a proxy are flagged `rt` (runtime dependent) instead of being trusted.
// Scenarios: firmware feature lists (get_fw_features / feature bit mask) empty or full  x  robot location cn/us/de.
import fs from 'fs';
import path from 'path';
import { loadModules } from './modload.mjs';
import { Runner, makeInert } from './sandbox.mjs';

const [corpus, rpcDir, bundleId, outFile, modelList] = process.argv.slice(2);
if (!corpus || !rpcDir || !bundleId || !outFile) { console.error('usage: node eval_features.mjs <corpus> <rpcDir> <bundleId> <out.json> [models]'); process.exit(2); }

const [model, hash] = bundleId.split('@');
const android = hash ? path.join(corpus, model, 'variants', hash, 'android') : path.join(corpus, model, 'android');
const mods = loadModules(android);
const rpc = JSON.parse(fs.readFileSync(path.join(rpcDir, bundleId + '.json'), 'utf8'));
const fmId = (rpc.ids.featureManager || [])[0];
const dmmId = (rpc.ids.deviceModelManager || [])[0];
const groupIds = rpc.ids.rrmisdkModelGroups || [];
if (fmId === undefined) { console.error('no FeatureManager module found in', bundleId); process.exit(3); }
const byId = new Map(mods.map(m => [m.id, m]));
const fmMod = byId.get(fmId);

// ---- which modules are executed for real: FM, DMM and small pure dependencies (resource tables, language lists)
const real = new Set();
function addDeps(id, depth) {
  if (real.has(id) || depth > 3) return;
  const m = byId.get(id); if (!m) return;
  real.add(id);
  for (const d of m.deps) {
    const dm = byId.get(d); if (!dm) continue;
    if (dm.text.length < 6000 && !/NativeModules|react-native|StyleSheet|Dimensions/.test(dm.text)) addDeps(d, depth + 1);
  }
}
addDeps(fmId, 0); if (dmmId !== undefined) addDeps(dmmId, 0);

// ---- Babel runtime helpers live in the host app's shared bundle (ids absent from the plugin): recognise them by the
// variable names the plugin code gives them and provide tiny equivalents.
const HELPER_NAMES = ['classCallCheck', 'createClass', 'defineProperty', 'construct', 'toConsumableArray', 'inherits', 'possibleConstructorReturn', 'getPrototypeOf', 'slicedToArray', 'objectSpread', 'extends', 'assertThisInitialized'];
const helperIds = new Map();
for (const m of mods) {
  for (const x of m.text.matchAll(/var _(\w+?)2? = (?:_interopRequireDefault\()?_\$\$_REQUIRE\(_dependencyMap\[(\d+)\]\)/g)) {
    if (HELPER_NAMES.includes(x[1]) && m.deps[+x[2]] !== undefined) helperIds.set(m.deps[+x[2]], x[1]);
  }
  const y = /var _interopRequireDefault = _\$\$_REQUIRE\(_dependencyMap\[(\d+)\]\)/.exec(m.text);
  if (y && m.deps[+y[1]] !== undefined) helperIds.set(m.deps[+y[1]], 'interopRequireDefault');
}
// minified bundles hide the variable names: borrow the id -> helper map from the newest non-minified bundle (same shared host bundle)
if (helperIds.size < 3) {
  const fb = path.join(corpus, 'roborock.vacuum.a65', 'android');
  if (fs.existsSync(fb)) {
    for (const m of loadModules(fb)) {
      for (const x of m.text.matchAll(/var _(\w+?)2? = (?:_interopRequireDefault\()?_\$\$_REQUIRE\(_dependencyMap\[(\d+)\]\)/g)) {
        if (HELPER_NAMES.includes(x[1]) && m.deps[+x[2]] !== undefined) helperIds.set(m.deps[+x[2]], x[1]);
      }
      const y = /var _interopRequireDefault = _\$\$_REQUIRE\(_dependencyMap\[(\d+)\]\)/.exec(m.text);
      if (y && m.deps[+y[1]] !== undefined) helperIds.set(m.deps[+y[1]], 'interopRequireDefault');
    }
  }
}
const HELPERS = {
  interopRequireDefault: (x) => (x && x.__esModule ? x : { default: x }),
  classCallCheck: () => {},
  createClass: (C, protoProps, staticProps) => {
    const def = (t, props) => { for (const p of props || []) { const d = { enumerable: false, configurable: true }; if ('value' in p) { d.value = p.value; d.writable = true; } if (p.get) d.get = p.get; if (p.set) d.set = p.set; Object.defineProperty(t, p.key, d); } };
    def(C.prototype, protoProps); def(C, staticProps); return C;
  },
  defineProperty: (o, k, v) => { Object.defineProperty(o, k, { value: v, enumerable: true, configurable: true, writable: true }); return o; },
  construct: (P, args, C) => Reflect.construct(P, args, C || P),
  toConsumableArray: (a) => Array.from(a),
  slicedToArray: (a, n) => Array.from(a).slice(0, n),
  inherits: () => {}, possibleConstructorReturn: (s, c) => c || s, getPrototypeOf: Object.getPrototypeOf, assertThisInitialized: (s) => s,
  objectSpread: (...a) => Object.assign({}, ...a), extends: Object.assign,
};

// ---- locate the modules FM talks to
const depVar = (name) => { const r = new RegExp('var _' + name + ' = (?:_interopRequireDefault\\()?' + REQ + '\\(_dependencyMap\\[(\\d+)\\]\\)').exec(fmMod.text); return r ? fmMod.deps[+r[1]] : undefined; };
const REQ = '(?:_\\$\\$_REQUIRE|_require\\d*)';   // RAM bundles: _$$_REQUIRE, plain bundles: _require / _require2 ...
const rrmisdkVarMatch = new RegExp('var RRMISDK = (?:_interopRequireDefault\\()?' + REQ + '\\(_dependencyMap\\[(\\d+)\\]\\)').exec(fmMod.text);
const rrmisdkId = rrmisdkVarMatch ? fmMod.deps[+rrmisdkVarMatch[1]] : undefined;
const rsmId = depVar('RobotStatusManager');          // old generation: state holder (RSM) lives in RobotStatusManager
const groupsId = groupIds.includes(rrmisdkId) ? rrmisdkId : groupIds[0];     // the RRMISDK module FeatureManager really imports, else the first candidate
let groups = null;                                    // old generation: isXxx() -> model list (kept for the group-name check)
let groupSrc = null;                                  // old generation: source of the model-group helpers of RRMISDK (isModel/isSomeModel based)
if (groupsId !== undefined) {
  groups = {};
  const gtext = byId.get(groupsId).text;
  for (const x of gtext.matchAll(/function (is\w+)\(\) \{\s*return (?:isModel|isSomeModel)\(\[([^\]]*)\]\);/g)) groups[x[1]] = [...x[2].matchAll(/'([^']+)'/g)].map(y => y[1]);
  // composite helpers (`function isTanosV() { return isTanosV_CN() || isTanosV_CE(); }`) and the model helpers themselves are evaluated for the
  // device model with a tiny scope: only functions whose body consists of calls of other helpers, model lists, ||, && and ! are taken.
  const safe = [];
  for (const x of gtext.matchAll(/function (is\w+)\(\)\s*\{\s*return ([^;{}]*);\s*\}/g)) {
    const body = x[2];
    const stripped = body.replace(/'[^']*'/g, '').replace(/\bis\w+\(/g, '').replace(/[\[\]\s,()!|&]/g, '');
    if (stripped === '' || /^(true|false)$/.test(stripped)) safe.push(x[0]);
  }
  groupSrc = safe.join('\n');
}
function evalGroup(name, devModel, isMiApp) {
  const fn = new Function('deviceModel', 'isMiApp', 'function isModel(m){return m.indexOf(deviceModel)!=-1;} function isSomeModel(m){return m.indexOf(deviceModel)!=-1;}\n' + groupSrc + '\nreturn typeof ' + name + " === 'function' ? " + name + '() : undefined;');
  return fn(devModel, isMiApp);
}

const models = modelList ? modelList.split(',') : [model];
const scenarios = [];
for (const loc of ['cn', 'us', 'de']) for (const fw of ['none', 'all']) scenarios.push({ loc, fw });

function evaluate(devModel, miApp = true) {
  const touched = new Set();
  const state = { robotFeatures: [], robotNewFeatures: 0, newFeatureInfoStr: '', deviceLocation: 'cn' };
  state.isSupportFeature = (c) => !!(state.robotFeatures && state.robotFeatures.indexOf(c) !== -1);
  const runner = new Runner(mods, real, {
    globals: { babelHelpers: { ...HELPERS, default: undefined } },
    override(id) {
      if (helperIds.has(id)) return HELPERS[helperIds.get(id)];
      if (id === rsmId) return { RSM: state, RobotStatusManager: { sharedManager: () => state }, __esModule: true };
      if (id === rrmisdkId || (dmmId !== undefined && id === (byId.get(dmmId).deps.find(d => byId.get(d) && /\.deviceModel\s*=[^=]/.test(byId.get(d).text))))) {
        const inert = makeInert('RRMISDK', touched);
        return new Proxy({}, {
          get(_t, p) {
            if (p === 'deviceModel') return devModel;
            if (p === '__esModule') return true;
            if (p === 'Device') return { model: devModel };
            if (p === 'isMiApp') return miApp;
            if (groupSrc && typeof p === 'string' && /^is\w+$/.test(p)) { let v; try { v = evalGroup(p, devModel, miApp); } catch { v = undefined; } if (v !== undefined) return () => !!v; }
            touched.add('RRMISDK.' + String(p));
            return inert[p];
          },
        });
      }
    },
  });
  const fmExports = runner.require(fmId);
  const FM = fmExports.default || fmExports;
  if (!FM || typeof FM !== 'function') return { error: 'FeatureManager export missing', errors: runner.errors };
  const names = Object.getOwnPropertyNames(FM).filter(n => typeof FM[n] === 'function' && !['length', 'name', 'prototype'].includes(n) && FM[n].length === 0);
  const res = {};
  for (const n of names) {
    const r = [];
    for (const sc of scenarios) {
      state.deviceLocation = FM.deviceLocation = sc.loc;
      state.robotFeatures = FM.robotFeatures = sc.fw === 'all' ? Array.from({ length: 40 }, (_x, i) => 101 + i) : [];
      state.robotNewFeatures = FM.robotNewFeatures = sc.fw === 'all' ? Number.MAX_SAFE_INTEGER : 0;
      state.newFeatureInfoStr = FM.newFeatureInfoStr = sc.fw === 'all' ? 'ffffffffffffffff' : '';
      touched.clear();
      let v; let err;
      try { v = FM[n].call(FM); } catch (e) { err = String(e.message).slice(0, 60); }
      const rec = {};
      if (err) rec.err = err;
      else if (typeof v === 'boolean') rec.v = v;
      else { rec.v = !!v; rec.nb = typeof v; }
      if (touched.size) rec.rt = [...touched].slice(0, 4);
      r.push(rec);
    }
    res[n] = r;
  }
  return { methods: res, errors: runner.errors.slice(0, 5) };
}

// product table of the DeviceModelManager (new generation): series -> models, product code name
let deviceInfo = null;
if (dmmId !== undefined) {
  const r0 = new Runner(mods, real, { globals: { babelHelpers: { ...HELPERS } }, override(id) { if (helperIds.has(id)) return HELPERS[helperIds.get(id)]; } });
  const ex = r0.require(dmmId);
  if (ex.DeviceInfoMap) {
    deviceInfo = { products: ex.Products ? Object.assign({}, ex.Products) : undefined, series: {} };
    for (const [k, v] of Object.entries(ex.DeviceInfoMap)) deviceInfo.series[k] = { models: Array.from(v.models || []), product: v.product || v.bucket || null, volume: v.volume ? { min: v.volume.min, max: v.volume.max } : undefined };
  }
}
const out = { bundle: bundleId, deviceInfo, generation: dmmId !== undefined ? 'dmm' : 'groups', featureManagerModule: fmId, dmmModule: dmmId ?? null, groups: groups || undefined, scenarios, results: {} };
for (const dm of models) {
  // fixed scenario: the plugin runs inside Mi Home (isMiApp = true); a second pass with isMiApp = false marks predicates that are
  // off in Mi Home but on in the Roborock app (`ra`)
  const res = evaluate(dm, true);
  const alt = evaluate(dm, false);
  for (const [n, rs] of Object.entries(res.methods || {})) {
    const other = (alt.methods || {})[n];
    if (rs.every(r => r.v === false && !r.err && !r.rt) && other && other.some(r => r.v === true)) rs[0].ra = true;
  }
  out.results[dm] = res;
}
fs.writeFileSync(outFile, JSON.stringify(out));
const first = out.results[models[0]];
console.log(bundleId.padEnd(36), out.generation, 'models', models.length, 'methods', Object.keys(first.methods || {}).length, 'errors', JSON.stringify(first.errors));
