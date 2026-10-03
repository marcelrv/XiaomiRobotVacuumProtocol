// Dump every named constant table (object / array literal assigned to a variable or `exports.X`) of every module of every
// bundle, with simple values resolved: numbers, strings, `X.Y` references and localisation-string references.
//
// usage: node extract_enums.mjs <corpus> <outdir> [bundleIdRegex]
// output <outdir>/<bundleId>.json = [{module, name, kind, value}]   (value contains {"$ref": "A.B"} for non-literal members,
// {"$expr": "<NodeType>"} for anything more complex). Python (build_enums.py) selects the tables of interest by name.
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, outdir, only] = process.argv.slice(2);
if (!corpus || !outdir) { console.error('usage: node extract_enums.mjs <corpus> <outdir> [bundleIdRegex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;
const SKIP_NAME = /(propTypes|defaultProps|styles?|Styles?)$/;

function refText(n) {
  if (n.type === 'Identifier') return n.name;
  if (n.type === 'MemberExpression') return refText(n.object) + (n.computed ? '[…]' : '.' + (n.property.name ?? n.property.value));
  return null;
}

let SRC = '';
function val(n, depth = 0) {
  if (!n || depth > 6) return { $expr: 'deep' };
  switch (n.type) {
    case 'Literal': return n.value instanceof RegExp ? { $expr: 'regex' } : n.value;
    case 'UnaryExpression':
      if (n.argument.type === 'Literal' && typeof n.argument.value === 'number') return n.operator === '-' ? -n.argument.value : n.operator === '+' ? n.argument.value : { $expr: 'unary' };
      if (n.operator === '!' && n.argument.type === 'Literal') return !n.argument.value;
      if (n.operator === 'void') return null;
      return { $expr: 'unary' };
    case 'Identifier': return n.name === 'undefined' ? null : { $ref: n.name };
    case 'MemberExpression': { const t = refText(n); return t ? { $ref: t } : { $expr: 'member' }; }
    case 'ArrayExpression': return n.elements.map(e => (e ? val(e, depth + 1) : null));
    case 'ObjectExpression': {
      const o = {};
      for (const p of n.properties) {
        if (p.type !== 'Property') { o['…'] = { $expr: p.type }; continue; }
        const k = p.key.type === 'Identifier' && !p.computed ? p.key.name : p.key.type === 'Literal' ? String(p.key.value) : '[computed]';
        o[k] = (p.value.type === 'FunctionExpression' || p.value.type === 'ArrowFunctionExpression') ? { $expr: 'function' } : val(p.value, depth + 1);
      }
      return o;
    }
    case 'TemplateLiteral': return n.quasis.length === 1 ? n.quasis[0].value.cooked : { $expr: 'template' };
    case 'BinaryExpression': {
      const l = val(n.left, depth + 1), r = val(n.right, depth + 1);
      if (typeof l === 'number' && typeof r === 'number') { try { return Function(`return ${l}${n.operator}${r}`)(); } catch { /* fallthrough */ } }
      return { $expr: 'binary:' + n.operator };
    }
    case 'CallExpression': return { $expr: 'call:' + (refText(n.callee) || '?') };
    case 'ConditionalExpression': return { $cond: [SRC.slice(n.test.start, n.test.end).slice(0, 140), val(n.consequent, depth + 1), val(n.alternate, depth + 1)] };
    default: return { $expr: n.type };
  }
}

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

for (const b of bundles(corpus)) {
  if (onlyRx && !onlyRx.test(b.id)) continue;
  const out = [];
  for (const m of loadModules(b.android)) {
    let ast;
    try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
    SRC = m.text;
    // minified code renames local variables but keeps export names: `e.Errors = o` -> table `o` is called `Errors`
    const expAlias = Object.create(null);
    walk.simple(ast, { AssignmentExpression(x) { if (x.operator === '=' && x.left.type === 'MemberExpression' && !x.left.computed && x.right.type === 'Identifier' && x.left.object.type === 'Identifier' && x.left.object.name.length <= 8) expAlias[x.right.name] = x.left.property.name; } });
    // exported scalar constants (`var CustomCleanMode = 106; exports.CustomCleanMode = ...`) of a module are dumped as one table `$consts`
    const consts = {};
    walk.simple(ast, { VariableDeclarator(d) {
      if (d.id.type !== 'Identifier' || !d.init) return;
      const nm = expAlias[d.id.name];
      if (!nm) return;
      const init = d.init.type === 'SequenceExpression' ? d.init.expressions[d.init.expressions.length - 1] : d.init;      // minified `u = (r(d[6]), 106)`
      if (init.type === 'Literal' && typeof init.value === 'number') consts[nm] = init.value;
      else if (init.type === 'UnaryExpression' && init.operator === '-' && init.argument.type === 'Literal' && typeof init.argument.value === 'number') consts[nm] = -init.argument.value;
    } });
    walk.simple(ast, { AssignmentExpression(x) {      // minified `e.CustomWaterMode = 204`
      if (x.operator === '=' && x.left.type === 'MemberExpression' && !x.left.computed && x.left.object.type === 'Identifier' && x.left.object.name.length <= 8 && x.right.type === 'Literal' && typeof x.right.value === 'number') consts[x.left.property.name] = x.right.value;
    } });
    if (Object.keys(consts).length >= 3) out.push({ module: m.id, name: '$consts', kind: 'object', value: consts });
    walk.fullAncestor(ast, (n, _s, anc) => {
      if (n.type !== 'ObjectExpression' && n.type !== 'ArrayExpression') return;
      if (n.type === 'ObjectExpression' && n.properties.length < 2) return;
      if (n.type === 'ArrayExpression' && n.elements.length < 3) return;
      let parent = anc[anc.length - 2];
      let selfNode = n;
      // minified `X = (a.b, {...})`: the object is the last element of a sequence expression
      if (parent.type === 'SequenceExpression' && parent.expressions[parent.expressions.length - 1] === n && anc.length >= 3) { selfNode = parent; parent = anc[anc.length - 3]; }
      let name = null;
      if (parent.type === 'VariableDeclarator' && parent.id.type === 'Identifier' && parent.init === selfNode) name = expAlias[parent.id.name] || parent.id.name;
      else if (parent.type === 'AssignmentExpression' && parent.right === n && parent.left.type === 'MemberExpression') name = (refText(parent.left.object) || '') + '.' + (parent.left.property.name ?? parent.left.property.value);
      else if (parent.type === 'Property' && parent.value === n && parent.key) name = '.' + (parent.key.name ?? parent.key.value);
      else if (parent.type === 'ReturnStatement' || (parent.type === 'ArrowFunctionExpression' && parent.body === n)) {
        for (let i = anc.length - 3; i >= 0; i--) { const a = anc[i]; if (a.type === 'FunctionDeclaration' && a.id) { name = 'return@' + a.id.name; break; } if (a.type === 'VariableDeclarator' && a.id && a.id.name) { name = 'return@' + a.id.name; break; } if (a.type === 'Property' && a.key) { name = 'return@.' + (a.key.name ?? a.key.value); break; } if (a.type === 'AssignmentExpression' && a.left.type === 'MemberExpression') { name = 'return@' + (a.left.property.name ?? a.left.property.value); break; } }
      }
      if (!name || SKIP_NAME.test(name)) return;
      // only top-level-ish tables: skip tables nested inside functions that are style sheets etc. (kept; filtered by name later)
      const v = val(n);
      const s = JSON.stringify(v);
      if (s.length > 60000) return;
      out.push({ module: m.id, name, kind: n.type === 'ArrayExpression' ? 'array' : 'object', value: v });
    });
  }
  fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify(out));
  console.log(b.id.padEnd(36), out.length);
}
