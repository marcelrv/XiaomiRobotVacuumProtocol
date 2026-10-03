// Extract the block schema of the app's own map parser (raw/*_parser_workermapparser.jx) for every bundle.
//
// usage: node extract_map_schema.mjs <corpus> <out.json>
// For each model: { file, scale, maxBlockNum, schema: { "<id>": { type, header: [[name, bytes], ...] } } }
// (header fields are the per-block header; payload decoding code is not copied, see docs/maps/rr-map-format.md for the layouts.)
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';

const [corpus, outFile] = process.argv.slice(2);
if (!corpus || !outFile) { console.error('usage: node extract_map_schema.mjs <corpus> <out.json>'); process.exit(2); }
const out = {};
for (const model of fs.readdirSync(corpus).sort()) {
  const raw = path.join(corpus, model, 'android', 'raw');
  if (!fs.existsSync(raw)) continue;
  const f = fs.readdirSync(raw).find(x => x.endsWith('_parser_workermapparser.jx'));
  if (!f) continue;
  const text = fs.readFileSync(path.join(raw, f), 'utf8');
  let ast; try { ast = acorn.parse(text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch (e) { out[model] = { error: String(e.message) }; continue; }
  const rec = { file: f, bytes: text.length, schema: {} };
  walk.simple(ast, {
    VariableDeclarator(d) {
      if (d.id.type !== 'Identifier' || !d.init) return;
      if (d.id.name === 'Scale' && d.init.type === 'Literal') rec.scale = d.init.value;
      if (d.id.name === 'MaxBlockNum' && d.init.type === 'Literal') rec.maxBlockNum = d.init.value;
      if (d.id.name === 'Schema' && d.init.type === 'ObjectExpression') {
        for (const p of d.init.properties) {
          const key = String(p.key.value ?? p.key.name);
          const e = { type: null, header: [] };
          if (p.value.type === 'ObjectExpression') {
            for (const q of p.value.properties) {
              const k = q.key.name ?? q.key.value;
              if (k === 'type' && q.value.type === 'Literal') e.type = q.value.value;
              if (k === 'header' && q.value.type === 'ArrayExpression') e.header = q.value.elements.map(el => el.elements.map(x => x.value));
            }
          }
          rec.schema[Number(key)] = e;
        }
      }
    },
  });
  out[model] = rec;
}
fs.writeFileSync(outFile, JSON.stringify(out, null, 1));
console.log(Object.keys(out).length, 'parsers;', Object.entries(out).map(([m, r]) => m.replace('roborock.vacuum.', '') + ':' + Object.keys(r.schema || {}).length).join(' '));
