// Static definition of every FeatureManager predicate: which firmware feature codes (get_fw_features), which bits of the
// 64-bit "new feature" mask, which product-line predicates and which runtime conditions it depends on.
//
// usage: node extract_feature_defs.mjs <corpus> <rpcDir> <outdir> [bundleIdRegex]
// output <outdir>/<bundleId>.json = { featureManagerModule, methods: { name: { codes, bits, products, region, userGate, other } } }
//
//   codes     [101, 116, ...]  numeric arguments of isSupportFeature(n) / RSM.isSupportFeature(n)
//   bits      [{ word: 'lo'|'hi', mask: '0x40000000' | bit: 5 }]  tests on robotNewFeatures (lo = low 32 bits: `& mask`;
//             hi = high 32 bits: `/ Math.pow(2,32)` followed by `& mask` / `>> n & 1`)
//   products  product / model predicates referenced: DMM.isXxx, Products.Xxx, RRMISDK.isXxx
//   region    true when isFCC / isCE / isFCCOrCE / deviceLocation is consulted
//   userGate  true when the method compares the account id with a hard-coded list (list contents are NOT recorded)
//   calls     other FeatureManager methods called (this.x() / FeatureManager.x())
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, rpcDir, outdir, only] = process.argv.slice(2);
if (!corpus || !rpcDir || !outdir) { console.error('usage: node extract_feature_defs.mjs <corpus> <rpcDir> <outdir> [regex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;

function bundles(corpus) {
  const res = [];
  for (const model of fs.readdirSync(corpus).sort()) {
    const base = path.join(corpus, model);
    if (!fs.existsSync(path.join(base, 'android'))) continue;
    res.push({ id: model, android: path.join(base, 'android') });
    const vdir = path.join(base, 'variants');
    if (fs.existsSync(vdir)) for (const h of fs.readdirSync(vdir)) res.push({ id: `${model}@${h}`, android: path.join(vdir, h, 'android') });
  }
  return res;
}
const txt = (t, n) => t.slice(n.start, n.end);

for (const b of bundles(corpus)) {
  if (onlyRx && !onlyRx.test(b.id)) continue;
  const rpcFile = path.join(rpcDir, b.id + '.json');
  if (!fs.existsSync(rpcFile)) continue;
  const rpc = JSON.parse(fs.readFileSync(rpcFile, 'utf8'));
  const fmId = (rpc.ids.featureManager || [])[0];
  if (fmId === undefined) continue;
  const mod = loadModules(b.android).find(m => m.id === fmId);
  const ast = acorn.parse(mod.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true });
  const methods = {};
  walk.simple(ast, {
    ObjectExpression(o) {
      const kp = o.properties.find(p => p.type === 'Property' && (p.key.name ?? p.key.value) === 'key' && p.value.type === 'Literal' && typeof p.value.value === 'string');
      const vp = o.properties.find(p => p.type === 'Property' && (p.key.name ?? p.key.value) === 'value' && /Function/.test(p.value.type));
      if (!kp || !vp) return;
      const name = kp.value.value; const fn = vp.value; const src = txt(mod.text, fn);
      const rec = { codes: [], bits: [], products: [], region: false, userGate: false, calls: [] };
      walk.simple(fn.body, {
        CallExpression(c) {
          const callee = txt(mod.text, c.callee);
          if (/isSupportFeature$/.test(callee) && c.arguments[0] && c.arguments[0].type === 'Literal') rec.codes.push(c.arguments[0].value);
          else if (/(^|\.)(this|FeatureManager|[A-Za-z_$.]*FeatureManager)\.(is\w+|should\w+|has\w+)$/.test(callee) || /^this\.(is|should|has)\w+$/.test(callee)) rec.calls.push(callee.split('.').pop());
          else if (/isFCCOrCE|isFCC|isCE$|isOversea/.test(callee)) rec.region = true;
        },
        MemberExpression(m) {
          const t = txt(mod.text, m);
          let mm;
          if ((mm = /(?:DMM|DeviceModelManager\.DMM|RRMISDK)\.(is\w+)$/.exec(t))) rec.products.push(mm[1]);
          else if ((mm = /Products\.(\w+)$/.exec(t))) rec.products.push(mm[1]);
          else if (/deviceLocation$/.test(t)) rec.region = true;
        },
      });
      // bit tests on the numeric feature word, written either way round and with decimal or hex masks (minified code:
      // `67108864&t.robotNewFeatures`):  mask & X.robotNewFeatures | X.robotNewFeatures & mask | X.robotNewFeatures / 2^32 [>> n] & mask|1
      const hex = (v) => '0x' + Number(v).toString(16);
      const NUM = '(0x[0-9a-fA-F]+|\\d+)';
      const RNF = '[\\w$.]*robotNewFeatures';
      for (const x of src.matchAll(new RegExp(NUM + '\\s*&\\s*\\(?' + RNF + '(?!\\s*/)', 'g'))) rec.bits.push({ word: 'lo', mask: hex(x[1]) });
      for (const x of src.matchAll(new RegExp(RNF + '(?!\\s*/)\\s*&\\s*' + NUM, 'g'))) rec.bits.push({ word: 'lo', mask: hex(x[1]) });
      for (const x of src.matchAll(new RegExp(RNF + '\\s*/\\s*Math\\.pow\\(2,\\s*32\\)\\s*&\\s*' + NUM, 'g'))) rec.bits.push({ word: 'hi', mask: hex(x[1]) });
      for (const x of src.matchAll(new RegExp(NUM + '\\s*&\\s*\\(?' + RNF + '\\s*/\\s*Math\\.pow\\(2,\\s*32\\)', 'g'))) rec.bits.push({ word: 'hi', mask: hex(x[1]) });
      for (const x of src.matchAll(new RegExp(RNF + '\\s*/\\s*Math\\.pow\\(2,\\s*32\\)\\s*>>\\s*(\\d+)\\s*&\\s*1', 'g'))) rec.bits.push({ word: 'hi', bit: +x[1] });
      for (const x of src.matchAll(new RegExp(RNF + '\\s*>>\\s*(\\d+)\\s*&\\s*1', 'g'))) rec.bits.push({ word: 'lo', bit: +x[1] });
      // hex-string feature word (new_feature_info_str): parseInt('0x' + newFeatureInfoStr.slice(a[, b])) & mask; recorded as a global bit
      // number counted from the least significant bit of the string (digit index from the right * 4 + bit inside the digit)
      for (const x of src.matchAll(/newFeatureInfoStr\.slice\((-\d+)(?:,\s*(-\d+))?\)/g)) {
        // mask written in front of parseInt(...) (minified code: 8&parseInt('0x'+...)) or after the assignment (featureInfo & 0x08)
        const before = /(0x[0-9a-fA-F]+|\d+)\s*&\s*parseInt\(\s*['"]0x['"]\s*\+\s*[\w$.]*$/.exec(src.slice(Math.max(0, x.index - 80), x.index));
        const after = /&\s*(0x[0-9a-fA-F]+|\d+)/.exec(src.slice(x.index + x[0].length));
        const mk = before || after;
        if (!mk) continue;
        const mask = Number(mk[1]); const base = x[2] ? -Number(x[2]) : 0;
        if (mask > 0 && (mask & (mask - 1)) === 0) rec.bits.push({ word: 'str', bit: 4 * base + Math.log2(mask) });
        else rec.bits.push({ word: 'str', mask: mk[1], base });
      }
      if (/whiteList|blackList|\.userId\b/.test(src)) rec.userGate = true;
      if (!/^(constructor)$/.test(name)) { for (const k of ['codes', 'products', 'calls']) rec[k] = [...new Set(rec[k])]; methods[name] = rec; }
    },
  });
  // every use of isSupportFeature(<code>) / robotNewFeatures anywhere in the plugin (what does each feature id gate?)
  const uses = [];
  const guardTxt = (t, anc) => {
    for (let i = anc.length - 2; i >= 0; i--) {
      const a = anc[i];
      if (a.type === 'IfStatement' || a.type === 'ConditionalExpression') return 'cond: ' + t.slice(a.test.start, a.test.end).replace(/\s+/g, ' ').slice(0, 160);
      if (a.type === 'ReturnStatement') return 'return: ' + t.slice(a.start, a.end).replace(/\s+/g, ' ').slice(0, 160);
    }
    return null;
  };
  const fnName = (anc) => {
    for (let i = anc.length - 2; i >= 0; i--) {
      const a = anc[i];
      if (a.type === 'FunctionDeclaration' && a.id) return a.id.name;
      if (a.type === 'Property' && a.key && /Function/.test(a.value.type) && (a.key.name ?? a.key.value) !== 'value') return a.key.name ?? a.key.value;
      if (a.type === 'ObjectExpression') { const kp = a.properties.find(p => p.type === 'Property' && (p.key.name ?? p.key.value) === 'key' && p.value.type === 'Literal'); if (kp && (anc[i + 1] || {}).type === 'Property' && ((anc[i + 1].key || {}).name ?? (anc[i + 1].key || {}).value) === 'value') return kp.value.value; }
    }
    return null;
  };
  for (const m2 of loadModules(b.android)) {
    if (!/isSupportFeature|robotNewFeatures/.test(m2.text)) continue;
    let a2; try { a2 = acorn.parse(m2.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
    walk.fullAncestor(a2, (n, _s, anc) => {
      if (n.type === 'CallExpression' && /isSupportFeature$/.test(txt(m2.text, n.callee)) && n.arguments[0] && n.arguments[0].type === 'Literal') {
        uses.push({ kind: 'fw', code: n.arguments[0].value, module: m2.id, fn: fnName(anc), ctx: guardTxt(m2.text, anc) });
      }
    });
  }
  fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify({ bundle: b.id, featureManagerModule: fmId, methods, uses }));
  console.log(b.id.padEnd(36), Object.keys(methods).length, 'methods;', Object.values(methods).filter(m => m.codes.length).length, 'with fw codes;', Object.values(methods).filter(m => m.bits.length).length, 'with bit masks');
}
