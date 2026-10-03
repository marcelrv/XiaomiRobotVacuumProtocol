// Load the modules of an unpacked bundle (see ../unpack_plugins.py for the layout).
import fs from 'fs';
import path from 'path';

const TAIL = /^\},\s*(\d+)\s*,\s*\[([\d,\s]*)\](?:\s*,\s*"([^"]*)")?\s*\);?\s*$/;
const TAIL_ANY = /\},\s*(\d+)\s*,\s*\[([\d,\s]*)\](?:\s*,\s*"([^"]*)")?\s*\);?\s*$/;

function parseOne(text, fn) {
  const m = TAIL_ANY.exec(text);
  const id = m ? +m[1] : (fn ? +/m(\d+)\.js/.exec(fn)[1] : -1);
  const deps = m ? m[2].replace(/\s/g, '').split(',').filter(Boolean).map(Number) : [];
  return { id, deps, path: m ? m[3] : undefined, text };
}

/** Return [{id, deps, path, text}] for the `android` folder of one unpacked bundle. */
export function loadModules(android) {
  const mods = [];
  const md = path.join(android, 'modules');
  if (fs.existsSync(md)) {
    for (const fn of fs.readdirSync(md)) {
      mods.push(parseOne(fs.readFileSync(path.join(md, fn), 'utf8'), fn));
    }
  } else {
    const lines = fs.readFileSync(path.join(android, 'main.bundle'), 'utf8').split('\n');
    let cur = null;
    for (const line of lines) {
      if (cur === null) { if (line.startsWith('__d(function')) cur = [line]; continue; }
      cur.push(line);
      if (line.startsWith('},') && TAIL.test(line.trim())) { mods.push(parseOne(cur.join('\n'))); cur = null; }
    }
  }
  return mods.sort((a, b) => a.id - b.id);
}

export function listModels(corpus) {
  return fs.readdirSync(corpus).filter(d => fs.existsSync(path.join(corpus, d, 'android'))).sort();
}
