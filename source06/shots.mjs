// 全スライドを1つのChromeで撮り、はみ出しも測る。
// 使い方: node source06/shots.mjs <index.html の絶対パス> <出力フォルダ>
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [, , html, outDir] = process.argv;
const PORT = 9400 + (process.pid % 200);
const profile = join(tmpdir(), 'deck-shots-' + process.pid);
mkdirSync(outDir, { recursive: true });
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  `--user-data-dir=${profile}`, `--remote-debugging-port=${PORT}`, '--window-size=1440,810', 'about:blank',
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let id = 0; const pending = new Map();
const call = (ws, method, params = {}) => new Promise((res, rej) => {
  const n = ++id; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, method, params }));
});
try {
  for (let i = 0; i < 100; i++) { try { if ((await fetch(`http://127.0.0.1:${PORT}/json/version`)).ok) break; } catch {} await sleep(200); }
  const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => { ws.onopen = r; });
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); } };
  await call(ws, 'Page.enable');
  await call(ws, 'Emulation.setDeviceMetricsOverride', { width: 1440, height: 810, deviceScaleFactor: 1, mobile: false });
  await call(ws, 'Page.navigate', { url: 'file://' + html });
  await sleep(1500);
  const ev = async (expression) => (await call(ws, 'Runtime.evaluate', { expression, returnByValue: true })).result.value;
  await ev(`(()=>{const s=document.createElement('style');s.textContent='*{transition:none!important;animation:none!important}';document.head.appendChild(s)})()`);
  const n = await ev('slides.length');
  const bad = [];
  for (let i = 0; i < n; i++) {
    await ev(`show(${i},true)`);
    await sleep(120);
    const box = await ev(`(()=>{const st=document.querySelector('#stage').getBoundingClientRect();let t=1e9,b=-1e9,l=1e9,r=-1e9;
      slides[${i}].querySelectorAll('h1,h2,h3,p,article,.st,.question,.lb,.x-core-txt').forEach(e=>{const q=e.getBoundingClientRect();if(!q.width||!q.height)return;
      t=Math.min(t,q.top-st.top);b=Math.max(b,q.bottom-st.top);l=Math.min(l,q.left-st.left);r=Math.max(r,q.right-st.left)});return [Math.round(l),Math.round(r),Math.round(t),Math.round(b)]})()`);
    if (box[0] < 20 || box[1] > 1420 || box[2] < 70 || box[3] > 780) bad.push([i + 1, ...box]);
    const shot = await call(ws, 'Page.captureScreenshot', { format: 'jpeg', quality: 80 });
    writeFileSync(join(outDir, `p${String(i + 1).padStart(2, '0')}.jpg`), Buffer.from(shot.data, 'base64'));
  }
  console.log(n + '枚', 'はみ出し候補:', JSON.stringify(bad));
} finally {
  chrome.kill(); await sleep(400);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
