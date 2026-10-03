// Extract the consumable ("supplies") definitions of the plugin: every object literal with a `suppliesKey`.
//
// usage: node extract_consumables.mjs <corpus> <outdir> [bundleIdRegex]
// output <outdir>/<bundleId>.json = [{module, key, total, unitsTime, needTime, needState, nameKey, textKey}]
//   key      = field of the get_consumable reply (or pseudo key such as mopSwabSupplies)
//   total    = nominal life as written in the plugin (hours when unitsTime, otherwise a count)
//   nameKey  = key of the English string table for the display name (resolved by build_consumables.py)
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, outdir, only] = process.argv.slice(2);
if (!corpus || !outdir) { console.error('usage: node extract_consumables.mjs <corpus> <outdir> [regex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;
const pk = (p) => (p.key.name ?? p.key.value);
const lit = (n) => (n && n.type === 'Literal' ? n.value : n && n.type === 'UnaryExpression' && n.operator === '!' && n.argument.type === 'Literal' ? !n.argument.value : undefined);
const refKey = (n) => (n && n.type === 'MemberExpression' && !n.computed ? n.property.name : null);

for (const model of fs.readdirSync(corpus).sort()) {
  const base = path.join(corpus, model);
  const jobs = [{ id: model, android: path.join(base, 'android') }];
  const vdir = path.join(base, 'variants');
  if (fs.existsSync(vdir)) for (const h of fs.readdirSync(vdir)) jobs.push({ id: `${model}@${h}`, android: path.join(vdir, h, 'android') });
  for (const b of jobs) {
    if ((onlyRx && !onlyRx.test(b.id)) || !fs.existsSync(b.android)) continue;
    const out = [];
    for (const m of loadModules(b.android)) {
      if (!m.text.includes('suppliesKey')) continue;
      let ast; try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
      walk.simple(ast, {
        ObjectExpression(o) {
          const props = Object.fromEntries(o.properties.filter(p => p.type === 'Property').map(p => [pk(p), p.value]));
          if (!props.suppliesKey || !lit(props.suppliesKey)) return;
          out.push({
            module: m.id, key: lit(props.suppliesKey), total: lit(props.total) ?? null, unitsTime: lit(props.isUnitsTime) ?? null,
            needTime: lit(props.isNeedTime) ?? null, needState: lit(props.isNeedState) ?? null,
            nameKey: refKey(props.name) || (props.name && props.name.type === 'ConditionalExpression' ? refKey(props.name.alternate) : null),
          });
        },
      });
    }
    // older layout: an object keyed 0..n whose entries carry `name` and `total`; the index -> reply key order is an array of key strings
    //   keys = ['filter_work_time', 'side_brush_work_time', 'main_brush_work_time', ...]   (same order as the indexes)
    if (out.length === 0) {
      let order = null;
      const mods = loadModules(b.android);
      for (const m of mods) {
        if (!m.text.includes('main_brush_work_time')) continue;
        let ast; try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
        walk.simple(ast, { ArrayExpression(a) {
          const v = a.elements.map(e => (e && e.type === 'Literal' ? e.value : null));
          if (!order && v.length >= 5 && v.every(x => typeof x === 'string') && v.includes('main_brush_work_time') && v.includes('filter_work_time')) order = v;
        } });
      }
      if (order) {
        for (const m of mods) {
          if (!m.text.includes('total:')) continue;
          let ast; try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
          walk.simple(ast, { ObjectExpression(o) {
            const ent = o.properties.filter(p => p.type === 'Property' && /^\d+$/.test(String(pk(p))) && p.value.type === 'ObjectExpression');
            if (ent.length < 5) return;
            const rows = ent.map(p => {
              const props = Object.fromEntries(p.value.properties.filter(q => q.type === 'Property').map(q => [pk(q), q.value]));
              return { idx: +pk(p), total: lit(props.total), nameKey: refKey(props.name) };
            });
            if (!rows.every(r => typeof r.total === 'number')) return;
            for (const r of rows) if (order[r.idx]) out.push({ module: m.id, key: order[r.idx], total: r.total, unitsTime: true, needTime: null, needState: null, nameKey: r.nameKey });
          } });
        }
      }
    }
    fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify(out));
    console.log(b.id.padEnd(36), out.length);
  }
}
