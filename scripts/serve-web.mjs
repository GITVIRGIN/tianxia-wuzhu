import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const option = (name, fallback) => {
  const i = args.indexOf(name);
  return i < 0 ? fallback : args[i + 1];
};
const root = path.resolve(option('--root', path.join(path.dirname(fileURLToPath(import.meta.url)), '../dist/browser')));
const port = Number(option('--port', '8791'));
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Invalid port');
if (!fs.existsSync(path.join(root, 'index.html'))) throw new Error(`Web build missing: ${root}`);
const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.wasm':'application/wasm','.pck':'application/octet-stream','.png':'image/png','.svg':'image/svg+xml','.webp':'image/webp','.json':'application/json; charset=utf-8','.ico':'image/x-icon'};
const server = http.createServer((req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405); res.end(); return; }
  let name;
  try { name = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname); }
  catch { res.writeHead(400); res.end(); return; }
  if (name === '/__health') {
    res.writeHead(200, {'Content-Type':'application/json', 'Cache-Control':'no-store'});
    res.end(JSON.stringify({app:'tianxia-wuzhu',root,port})); return;
  }
  const target = path.resolve(root, '.' + (name === '/' ? '/index.html' : name));
  const relative = path.relative(root, target);
  if (relative.startsWith('..') || path.isAbsolute(relative) || relative.split(/[\\/]/).some(p => p.startsWith('.'))) { res.writeHead(403); res.end(); return; }
  fs.stat(target, (error, stat) => {
    if (error || !stat.isFile()) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, {'Content-Type':types[path.extname(target)] || 'application/octet-stream','Content-Length':stat.size,'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
    if (req.method === 'HEAD') { res.end(); return; }
    const stream = fs.createReadStream(target);
    stream.on('error', () => res.destroy());
    stream.pipe(res);
  });
});
server.on('error', error => { console.error(error.message); process.exitCode = 1; });
server.listen(port, '127.0.0.1', () => console.log(`天下无主 http://127.0.0.1:${port}/\n${root}`));
