// For every bundle: which fields of the robot status object does RobotStatusManager.parseStatus() read, and how
// does the app store/interpret them?
//
// usage: node extract_status_fields.mjs <corpus> <outdir> [bundleIdRegex]
// output <outdir>/<bundleId>.json = { module, param, fields: { <status field>: [ {target, expr} ... ] } }
//   target = `this.xxx` / `RSM.xxx` property the value is assigned to (when it is a direct assignment)
//   expr   = the right-hand side expression, <=120 chars (short; used as evidence anchor and to read units/enums)
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, outdir, only] = process.argv.slice(2);
if (!corpus || !outdir) { console.error('usage: node extract_status_fields.mjs <corpus> <outdir> [regex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;
// functions of RobotStatusManager that read fields of the status object (their first parameter)
const STATUS_FNS = new Set(['parseStatus', 'getComputedState', 'parseRobotMotionStatus']);

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
const slice = (t, n, max = 120) => { const s = t.slice(n.start, n.end).replace(/\s+/g, ' '); return s.length > max ? s.slice(0, max) + ' …' : s; };
const memberName = (n) => (n.computed ? (n.property.type === 'Literal' ? String(n.property.value) : null) : n.property.name);

for (const b of bundles(corpus)) {
  if (onlyRx && !onlyRx.test(b.id)) continue;
  const result = [];
  for (const m of loadModules(b.android)) {
    if (!/parseStatus|getComputedState|parseRobotMotionStatus/.test(m.text)) continue;
    let ast; try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
    walk.fullAncestor(ast, (n) => {
      // createClass entry: { key: "parseStatus", value: function parseStatus(status) {...} }
      if (n.type !== 'ObjectExpression') return;
      const kp = n.properties.find(p => p.type === 'Property' && (p.key.name ?? p.key.value) === 'key' && p.value.type === 'Literal' && STATUS_FNS.has(p.value.value));
      const vp = n.properties.find(p => p.type === 'Property' && (p.key.name ?? p.key.value) === 'value');
      if (!kp || !vp) return;
      const fn = vp.value;
      if (!fn || !fn.params || !fn.params[0] || fn.params[0].type !== 'Identifier') return;
      const P = fn.params[0].name;
      const fields = {};
      walk.fullAncestor(fn.body, (x, _s, anc) => {
        if (x.type === 'MemberExpression' && x.object.type === 'Identifier' && x.object.name === P) {
          const f = memberName(x); if (!f) return;
          const rec = (fields[f] ||= []);
          // find a direct assignment target: nearest AssignmentExpression ancestor whose right side contains x
          for (let i = anc.length - 2; i >= 0; i--) {
            const a = anc[i];
            if (a.type === 'AssignmentExpression' && a.right.start <= x.start && a.right.end >= x.end) {
              const tgt = slice(m.text, a.left, 60);
              const expr = slice(m.text, a.right);
              if (!rec.some(r => r.target === tgt)) rec.push({ target: tgt, expr });
              break;
            }
            if (a.type === 'IfStatement' && a.test.start <= x.start && a.test.end >= x.end) { const e = 'if ' + slice(m.text, a.test, 100); if (!rec.some(r => r.expr === e)) rec.push({ target: null, expr: e }); break; }
            if (a.type === 'FunctionExpression' || a.type === 'FunctionDeclaration') break;
          }
        }
      });
      result.push({ module: m.id, param: P, fields });
    });
  }
  fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify(result));
  console.log(b.id.padEnd(36), result.map(r => `m${r.module}:${Object.keys(r.fields).length}`).join(' '));
}
