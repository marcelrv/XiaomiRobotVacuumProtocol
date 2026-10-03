// Extract the cloud / smart-home calls of every plugin: calls that do not go to the robot over miIO.
//
// usage: node extract_cloud_calls.mjs <corpus> <outdir> [bundleIdRegex]
// output <outdir>/<bundleId>.json = [{kind, name, module, enclosing}]
//   kind = service    member call `<..>.Service.<namespace>.<fn>(` of the Mi Home plugin SDK (namespaces smarthome, storage, scene, room, ...)
//          sdk-helper `callSmartHomeAPI(<path>)`, `getVoicePackageList(`, `MHApi.<fn>(`
//          endpoint   string literal that is a smart-home API path (/home/..., /user/..., /scene/..., /v2/...)
// Nothing but identifiers and path literals is recorded.
import fs from 'fs';
import path from 'path';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import { loadModules } from './modload.mjs';

const [corpus, outdir, only] = process.argv.slice(2);
if (!corpus || !outdir) { console.error('usage: node extract_cloud_calls.mjs <corpus> <outdir> [regex]'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const onlyRx = only ? new RegExp(only) : null;
const NS = new Set(['smarthome', 'storage', 'scene', 'room', 'account', 'spec', 'miotspec']);
const PATH_RX = /^\/(home|user|scene|v2|app|miotspec|device)\/[a-z0-9_\/]+$/;

function enclosing(anc) {
  for (let i = anc.length - 2; i >= 0; i--) {
    const a = anc[i];
    if (a.type === 'Property' && a.key && a.value && /Function/.test(a.value.type)) return a.key.name || a.key.value;
    if (a.type === 'FunctionDeclaration' && a.id) return a.id.name;
    if (a.type === 'AssignmentExpression' && a.left.type === 'MemberExpression' && /Function/.test(a.right.type)) return a.left.property.name || a.left.property.value;
  }
  return null;
}
const isService = (n) => n && ((n.type === 'Identifier' && n.name === 'Service') || (n.type === 'MemberExpression' && !n.computed && n.property.name === 'Service'));

for (const model of fs.readdirSync(corpus).sort()) {
  const base = path.join(corpus, model);
  const jobs = [{ id: model, android: path.join(base, 'android') }];
  const vdir = path.join(base, 'variants');
  if (fs.existsSync(vdir)) for (const h of fs.readdirSync(vdir)) jobs.push({ id: `${model}@${h}`, android: path.join(vdir, h, 'android') });
  for (const b of jobs) {
    if ((onlyRx && !onlyRx.test(b.id)) || !fs.existsSync(b.android)) continue;
    const out = [];
    for (const m of loadModules(b.android)) {
      if (!/smarthome|storage|scene|room|spec|callSmartHomeAPI|getVoicePackageList|getCountryInfo|MHApi|'\/(home|user|scene)\//.test(m.text)) continue;
      let ast; try { ast = acorn.parse(m.text, { ecmaVersion: 'latest', allowReturnOutsideFunction: true }); } catch { continue; }
      walk.fullAncestor(ast, (n, _s, anc) => {
        if (n.type === 'Literal' && typeof n.value === 'string' && PATH_RX.test(n.value)) out.push({ kind: 'endpoint', name: n.value, module: m.id, enclosing: enclosing(anc) });
        if (n.type !== 'CallExpression') return;
        const c = n.callee;
        if (c.type === 'MemberExpression' && !c.computed && c.object.type === 'MemberExpression' && !c.object.computed && NS.has(c.object.property.name)) {      // `<sdk>.smarthome.fn(`; the SDK object is `Service` or, in minified code, a renamed local
          if (c.object.property.name === 'storage' && !/ThirdUserConfigs/.test(c.property.name)) return;      // other `.storage.*` members are not SDK calls
          out.push({ kind: 'service', name: `Service.${c.object.property.name}.${c.property.name}`, module: m.id, enclosing: enclosing(anc) });
        } else if (c.type === 'MemberExpression' && !c.computed && c.property.name === 'callSmartHomeAPI' || (c.type === 'Identifier' && c.name === 'callSmartHomeAPI')) {
          const a0 = n.arguments[0];
          out.push({ kind: 'sdk-helper', name: 'callSmartHomeAPI(' + (a0 && a0.type === 'Literal' ? a0.value : '<computed path>') + ')', module: m.id, enclosing: enclosing(anc) });
        } else if (c.type === 'MemberExpression' && !c.computed && c.property.name === 'getVoicePackageList') {
          out.push({ kind: 'sdk-helper', name: 'getVoicePackageList', module: m.id, enclosing: enclosing(anc) });
        } else if (c.type === 'MemberExpression' && !c.computed && ((c.object.type === 'Identifier' && c.object.name === 'MHApi') || c.property.name === 'getCountryInfo')) {
          out.push({ kind: 'sdk-helper', name: 'MHApi.' + c.property.name, module: m.id, enclosing: enclosing(anc) });
        }
      });
    }
    fs.writeFileSync(path.join(outdir, b.id + '.json'), JSON.stringify(out));
    console.log(b.id.padEnd(36), out.length);
  }
}
