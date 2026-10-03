// Extract RPC-related facts from every module of every unpacked bundle using a real JS parser (acorn).
//
// usage: node extract_rpc.mjs <corpus> <outdir> [bundleIdRegex]
//   corpus  : folder produced by ../unpack_plugins.py (--variants optional)
//   outdir  : one <bundleId>.json per bundle; bundleId = <model> (best bundle) or <model>@<hash8> (other variant)
//
// Per bundle the JSON contains
//   tables     : object literals that look like a Methods table (Key -> 'rpc_method')
//   ids        : numeric ids of the interesting modules (protocol, robotApi, featureManager, deviceModelManager)
//   robotApi   : the wrapper functions of the "RobotApi" module (fn -> method, params source, transport)
//   rpcCalls   : every call whose first argument is an RPC method (string literal or <x>.Methods.<Key>) made through a
//                known wrapper, with the guards (enclosing if/&&/?: tests) found around the call
//   apiUses    : every use of a RobotApi wrapper function from other modules, with guards
//   methodsRefs: every `Methods.<Key>` reference (module id)
// Nothing here copies bundle code: only identifiers, string literals and short (<=300 char) argument/guard snippets.
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, outdir, only] = process.argv.slice(2);
if (!corpus || !outdir) { console.error('usage: node extract_rpc.mjs <corpus> <outdir> [bundleIdRegex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;

const METHOD_RX = /^(?:user\.|miIO\.)?[a-z][a-z0-9]*(?:_[a-z0-9]+)+$|^(?:user\.|miIO\.)[a-z_.0-9]+$/;
const KEY_RX = /^[A-Z][A-Za-z0-9]+$/;
const WRAPPER_RX = /(^|\.)(asyncCallMethod|callMethod|callMethodForceWay|callMethodForceWayNew|callMethodFromCloud|asyncCallMethodFromCloud|callMethodWithObject|getMapData|getAndDecBase64Data|getRobotData|downloadMap)$/;

function slice(text, n, max = 300) {
  const s = text.slice(n.start, n.end);
  return s.length > max ? s.slice(0, max) + ' …' : s;
}

function calleeText(c) {
  if (c.type === 'Identifier') return c.name;
  if (c.type === 'MemberExpression' && !c.computed && c.property.type === 'Identifier') {
    const o = c.object.type === 'Identifier' ? c.object.name : c.object.type === 'MemberExpression' ? calleeText(c.object) : '';
    return (o ? o + '.' : '') + c.property.name;
  }
  if (c.type === 'SequenceExpression') return calleeText(c.expressions[c.expressions.length - 1]);
  return '?';
}

function methodsKey(n) {
  if (n.type === 'MemberExpression' && !n.computed && n.property.type === 'Identifier' && KEY_RX.test(n.property.name)) {
    const o = n.object;
    if (o.type === 'MemberExpression' && !o.computed && o.property.name === 'Methods') return n.property.name;
    if (o.type === 'Identifier' && o.name === 'Methods') return n.property.name;
  }
  return null;
}

function enclosingName(anc) {
  for (let i = anc.length - 2; i >= 0; i--) {
    const a = anc[i];
    if (a.type === 'Property' && a.key) return a.key.name || a.key.value;
    if (a.type === 'FunctionDeclaration' && a.id) return a.id.name;
    if (a.type === 'MethodDefinition' && a.key) return a.key.name;
    if (a.type === 'AssignmentExpression' && a.left.type === 'MemberExpression' && a.left.property) return a.left.property.name || a.left.property.value;
    if (a.type === 'VariableDeclarator' && a.id && a.id.name && anc[i + 1] && anc[i + 1].type.endsWith('Function')) return a.id.name;
  }
  return null;
}

// guards: tests of enclosing if / ?: / && / || around node n (innermost first)
function guards(text, anc) {
  const out = [];
  for (let i = anc.length - 2; i >= 0 && out.length < 4; i--) {
    const a = anc[i], child = anc[i + 1];
    if (a.type === 'IfStatement' && (child === a.consequent || child === a.alternate)) out.push((child === a.alternate ? '!' : '') + '(' + slice(text, a.test, 220) + ')');
    else if (a.type === 'ConditionalExpression' && (child === a.consequent || child === a.alternate)) out.push((child === a.alternate ? '!' : '') + '(' + slice(text, a.test, 220) + ')');
    else if (a.type === 'LogicalExpression' && a.operator === '&&' && child === a.right) out.push('(' + slice(text, a.left, 220) + ')');
    else if (a.type === 'LogicalExpression' && a.operator === '||' && child === a.right) out.push('!(' + slice(text, a.left, 220) + ')');
  }
  return out;
}

// The function that "owns" a call: the nearest function ancestor; regenerator-compiled async functions
// (`regenerator.async(function name$(_context) {...})`) are lifted to the function that contains the `async(...)` call.
function ownerFn(anc) {
  let i = anc.length - 2;
  while (i >= 0 && !/Function/.test(anc[i].type)) i--;
  if (i < 0) return null;
  // lift out of `x.async(function ...)` / `x.default.async(...)`
  while (i > 0) {
    const par = anc[i - 1];
    if (par.type === 'CallExpression' && par.arguments.includes(anc[i]) && /(^|\.)async$/.test(calleeText(par.callee))) {
      let j = i - 2;
      while (j >= 0 && !/Function/.test(anc[j].type)) j--;
      if (j < 0) break;
      i = j;
    } else break;
  }
  return anc[i];
}

// `<x>.result...` member chains read inside a function (outermost chains only), as `result[0].field`
function resultReads(fn) {
  const reads = new Set();
  walk.fullAncestor(fn.body, (n, _s, anc) => {
    if (n.type !== 'MemberExpression') return;
    const parent = anc[anc.length - 2];
    if (parent && parent.type === 'MemberExpression' && parent.object === n) return;     // not the outermost chain
    const parts = [];
    let cur = n;
    while (cur.type === 'MemberExpression') {
      parts.unshift(cur.computed ? (cur.property.type === 'Literal' ? '[' + cur.property.value + ']' : '[…]') : '.' + cur.property.name);
      cur = cur.object;
    }
    const k = parts.findIndex(x => x === '.result');
    if (k < 0) return;
    const tail = parts.slice(k, k + 4).join('');
    reads.add(tail.replace(/^\./, ''));
  });
  return [...reads].sort();
}

// alias -> module id.  Handles `var X = require(dep[k])`, `X = interopRequireDefault(require(dep[k]))`, minified comma/sequence forms
// `v = (t(r(d[14])), t(r(d[15])))`, chains `Y = interopRequireDefault(X)` and plain assignments.
function importAliases(ast, mod) {
  const fn = ast.body[0] && ast.body[0].expression && ast.body[0].expression.arguments && ast.body[0].expression.arguments[0];
  const map = Object.create(null);
  if (!fn || !fn.params) return map;
  const depName = fn.params[fn.params.length - 1].name;
  const find = (n) => {
    if (!n) return null;
    if (n.type === 'MemberExpression' && n.computed && n.object.type === 'Identifier' && n.object.name === depName && n.property.type === 'Literal') return mod.deps[n.property.value] ?? null;
    if (n.type === 'Identifier') return map[n.name] ?? null;
    if (n.type === 'SequenceExpression') return find(n.expressions[n.expressions.length - 1]);
    if (n.type === 'CallExpression') { for (const a of n.arguments) { const r = find(a); if (r !== null) return r; } }
    return null;
  };
  const decls = [];
  walk.simple(ast, {
    VariableDeclarator(d) { if (d.id.type === 'Identifier' && d.init) decls.push([d.id.name, d.init]); },
    AssignmentExpression(a) { if (a.operator === '=' && a.left.type === 'Identifier') decls.push([a.left.name, a.right]); },
  });
  for (let pass = 0; pass < 4; pass++) {          // a few passes resolve alias chains
    let changed = false;
    for (const [name, init] of decls) {
      if (map[name] !== undefined) continue;
      const k = find(init);
      if (k !== null && k !== undefined) { map[name] = k; changed = true; }
    }
    if (!changed) break;
  }
  return map;
}

// local name -> exported name for `exports.<name> = <ident>` / `e.<name>=<ident>` (minified helpers such as getAndDecBase64Data = le)
function exportAliases(ast) {
  const map = Object.create(null);
  walk.simple(ast, {
    AssignmentExpression(a) {
      if (a.operator === '=' && a.left.type === 'MemberExpression' && !a.left.computed && a.right.type === 'Identifier' && a.left.object.type === 'Identifier' && a.left.object.name.length <= 8) map[a.right.name] = a.left.property.name;
    },
  });
  return map;
}

function rootAlias(n) {
  // X.default.fn / X.fn / X.default.a.b -> X
  let cur = n;
  while (cur && cur.type === 'MemberExpression') cur = cur.object;
  return cur && cur.type === 'Identifier' ? cur.name : null;
}

function analyse(mods) {
  const out = { ids: {}, tables: [], robotApi: {}, rpcCalls: [], apiUses: [], methodsRefs: [], parseErrors: [] };
  const parsed = [];
  const pending = [];   // {rec, fn} : calls whose reply reads are resolved after the scan
  for (const m of mods) {
    let ast;
    try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); }
    catch (e) { out.parseErrors.push({ module: m.id, error: String(e.message) }); continue; }
    parsed.push({ m, ast, alias: importAliases(ast, m), exp: exportAliases(ast) });
    if (/(exports|\b[a-z])\.callMethodFromCloud\s*=/.test(m.text)) (out.ids.rrmisdk ||= []).push(m.id);
    if (/key:\s*"isMapSegmentSupported"/.test(m.text)) (out.ids.featureManager ||= []).push(m.id);
    if (/function (isModel|isSomeModel)\(/.test(m.text) && /deviceModel/.test(m.text)) (out.ids.rrmisdkModelGroups ||= []).push(m.id);
    if (/DeviceInfoMap/.test(m.text) && /\bProducts\b/.test(m.text) && /\bDeviceSeries\b/.test(m.text) && /exports\.DMM|e\.DMM/.test(m.text)) (out.ids.deviceModelManager ||= []).push(m.id);
    if (/retry_request/.test(m.text) && /need_retry/.test(m.text)) (out.ids.robotApi ||= []).push(m.id);
  }
  // pass 1: tables + robotApi wrapper table
  for (const { m, ast } of parsed) {
    walk.fullAncestor(ast, (n, _s, anc) => {
      if (n.type !== 'ObjectExpression') return;
      const props = n.properties.filter(p => p.type === 'Property' && p.value.type === 'Literal' && typeof p.value.value === 'string');
      const hits = props.filter(p => METHOD_RX.test(p.value.value) && KEY_RX.test(p.key.name || p.key.value || ''));
      if (hits.length >= 10 && n.properties.some(p => (p.key.name || p.key.value) === 'AppStart')) {
        const parent = anc[anc.length - 2];
        let ctx = null;
        if (parent && parent.type === 'VariableDeclarator') ctx = { kind: 'var', name: parent.id.name };
        else if (parent && parent.type === 'ConditionalExpression') ctx = { kind: parent.consequent === n ? 'cond-then' : 'cond-else', test: slice(m.text, parent.test, 200) };
        out.tables.push({ module: m.id, ctx, entries: Object.fromEntries(props.map(p => [p.key.name || p.key.value, p.value.value])), total_props: n.properties.length });
        (out.ids.protocol ||= []).includes(m.id) || out.ids.protocol.push(m.id);
      }
    });
  }
  // pass 1b: older bundles have no retry logic but still a "RobotApi" module: a module in which >= 20 properties each
  // just forward to asyncCallMethod(<method>, ...)
  for (const { m, ast } of parsed) {
    let n = 0;
    walk.fullAncestor(ast, (x, _s, anc) => {
      if (x.type !== 'CallExpression' || !x.arguments[0]) return;
      if (!/(^|\.)asyncCallMethod$/.test(calleeText(x.callee))) return;
      const a0 = x.arguments[0];
      if (!((a0.type === 'Literal' && typeof a0.value === 'string') || methodsKey(a0))) return;
      const par = anc[anc.length - 2], gp = anc[anc.length - 3], ggp = anc[anc.length - 4];
      // return asyncCallMethod(...) inside `prop: function () {...}`
      if (par && par.type === 'ReturnStatement' && gp && gp.type === 'BlockStatement' && ggp && /Function/.test(ggp.type)) n++;
    });
    if (n >= 20 && !(out.ids.robotApi || []).includes(m.id)) (out.ids.robotApi ||= []).push(m.id);
  }
  const protocolIds = new Set(out.ids.protocol || []);
  const apiIds = new Set(out.ids.robotApi || []);
  const helperIds = new Set([...apiIds, ...(out.ids.rrmisdk || [])]);      // RobotApi + RRMISDK: modules that only wrap RPCs
  // pass 2: wrapper definitions, rpc calls, uses
  for (const { m, ast, alias, exp } of parsed) {
    const isApiModule = apiIds.has(m.id);
    const isHelper = helperIds.has(m.id);
    walk.fullAncestor(ast, (n, _s, anc) => {
      if (n.type === 'MemberExpression') {
        const k = methodsKey(n);
        if (k) {
          // how is the reference used?  arg0 of a call | nested in an array/object argument ("param") | anything else
          let ctxKind = 'other', callee = null;
          const parent = anc[anc.length - 2];
          if (parent && parent.type === 'CallExpression' && parent.arguments[0] === n) { ctxKind = 'arg0'; callee = calleeText(parent.callee); }
          else {
            for (let i = anc.length - 2; i >= 1; i--) {
              const a = anc[i];
              if (a.type === 'ArrayExpression' || a.type === 'ObjectExpression') continue;
              if (a.type === 'CallExpression' && anc[i + 1] !== a.callee && a.arguments.indexOf(anc[i + 1]) >= 1) { ctxKind = 'param'; callee = calleeText(a.callee); }
              break;
            }
          }
          out.methodsRefs.push({ module: m.id, key: k, ctx: ctxKind, callee });
        }
      }
      if (n.type !== 'CallExpression') return;
      let callee = calleeText(n.callee);
      if (n.callee.type === 'Identifier' && exp[callee]) callee = exp[callee];      // minified local alias of an exported helper
      const a0 = n.arguments[0];
      // RPC call through a known wrapper (or any call inside the RobotApi module with a method-like literal)
      let arg0 = null;
      if (a0) {
        if (a0.type === 'Literal' && typeof a0.value === 'string' && METHOD_RX.test(a0.value)) arg0 = { kind: 'lit', value: a0.value };
        else { const k = methodsKey(a0); if (k) arg0 = { kind: 'methods', value: k }; else if (WRAPPER_RX.test(callee)) arg0 = { kind: 'expr', value: slice(m.text, a0, 120) }; }
      }
      const viaWrapper = WRAPPER_RX.test(callee) || (isApiModule && arg0 && arg0.kind !== 'expr' && n.arguments.length >= 2 && n.arguments.length <= 4);
      if (arg0 && viaWrapper) {
        const rec = { module: m.id, callee, arg0, enclosing: enclosingName(anc), args: n.arguments.slice(1, 4).map(x => slice(m.text, x)), guards: guards(m.text, anc) };
        if (isHelper && rec.enclosing && exp[rec.enclosing]) rec.enclosing = exp[rec.enclosing];     // minified named exports: `e.start = T`
        out.rpcCalls.push(rec);
        pending.push({ rec, fn: ownerFn(anc) });
        if (isHelper && rec.enclosing) {
          const fromCloud = /FromCloud/i.test(callee) || n.arguments.some(x => /FromCloud/.test(slice(m.text, x, 80)));
          (out.robotApi[rec.enclosing] ||= []).push({ method: arg0, args: rec.args, fromCloud, callee });
        }
      }
      // use of a RobotApi wrapper function from another module
      if (n.callee.type === 'MemberExpression' && !n.callee.computed && !isHelper) {
        const root = rootAlias(n.callee);
        if (root && (helperIds.has(alias[root]) || root === 'RobotApi' || root === 'RRMISDK')) {
          const urec = { module: m.id, fn: n.callee.property.name, enclosing: enclosingName(anc), args: n.arguments.slice(0, 3).map(x => slice(m.text, x, 160)), guards: guards(m.text, anc) };
          out.apiUses.push(urec);
          pending.push({ rec: urec, fn: ownerFn(anc) });
        }
      }
    });
  }
  // reply reads: attributed to a call when it is the only RPC / wrapper call of its owning function
  const callsIn = new Map();
  for (const { fn } of pending) if (fn) callsIn.set(fn, (callsIn.get(fn) || 0) + 1);
  const readCache = new Map();
  for (const { rec, fn } of pending) {
    if (!fn) continue;
    if (!readCache.has(fn)) readCache.set(fn, resultReads(fn));
    rec.fnCalls = callsIn.get(fn);
    rec.fnStart = fn.start;
    const rr = readCache.get(fn);
    if (rr.length) rec.reads = rr.slice(0, 8);
  }
  return out;
}

function bundles(corpus) {
  const res = [];
  for (const model of fs.readdirSync(corpus).sort()) {
    const base = path.join(corpus, model);
    if (!fs.existsSync(path.join(base, 'android'))) continue;
    res.push({ id: model, model, android: path.join(base, 'android') });
    const vdir = path.join(base, 'variants');
    if (fs.existsSync(vdir)) for (const h of fs.readdirSync(vdir)) res.push({ id: `${model}@${h}`, model, android: path.join(vdir, h, 'android') });
  }
  return res;
}

for (const b of bundles(corpus)) {
  if (onlyRx && !onlyRx.test(b.id)) continue;
  const mods = loadModules(b.android);
  const res = analyse(mods);
  res.bundle = b.id; res.modules = mods.length;
  fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify(res));
  console.log(b.id.padEnd(40), 'modules', mods.length, 'tables', res.tables.length, 'rpcCalls', res.rpcCalls.length,
    'robotApi', Object.keys(res.robotApi).length, 'apiUses', res.apiUses.length, 'ids', JSON.stringify(res.ids), 'perr', res.parseErrors.length);
}
