/* Moteur navigateur (client/dz.js, construit dans build/dz.js) dans un vrai Chromium.
   Garde contre le bug des marqueurs « déjà initialisé » qui écrasaient les réglages :
   texte qui s'écrit, bouton Copier, effet 3D.
   Lancer après le build : cd tools && node ../tests/dz-client.test.mjs */
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import assert from "node:assert";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(path.join(ROOT, "tools", "package.json"));
const { chromium } = require("playwright");
const exe = ["/opt/pw-browsers/chromium", process.env.CHROMIUM_PATH].find((p) => p && fs.existsSync(p));

const page = (body, motion) => `<!doctype html><html class="dz-skin dz-js"${motion ? "" : ' data-dz-motion="off"'}><head><meta charset="utf-8">
<link rel="stylesheet" href="file://${ROOT}/build/dz-core.css"></head><body>${body}
<script>window.__dzFam={map:{},url:"",w:""};</script><script src="file://${ROOT}/build/dz.js"></script></body></html>`;

const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const ctx = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
const tmp = path.join(os.tmpdir(), `dz-client-${process.pid}.html`);
const open = async (body, motion = false) => {
  fs.writeFileSync(tmp, page(body, motion));
  const p = await ctx.newPage();
  const errs = [];
  p.on("pageerror", (e) => errs.push(e.message));
  await p.goto("file://" + tmp);
  await p.waitForTimeout(150);
  return { p, errs };
};

try {
  /* 1. texte qui s'écrit, écrit comme dans le builder (classe + « a | b | c ») */
  let { p, errs } = await open('<h1><span id="t" class="dz-typewriter">sites qui vendent | apps qui plaisent | outils</span></h1>');
  let r = await p.evaluate(() => { const t = document.getElementById("t"); return { txt: t.textContent, cls: t.className, mots: t.getAttribute("data-dz-typed") }; });
  assert.strictEqual(r.txt, "sites qui vendent", "sans animation : seulement le premier mot, jamais « a | b | c »");
  assert.ok(r.cls.includes("dz-typed"), "le moteur a bien pris le bloc en charge");
  assert.ok(r.mots.includes("apps qui plaisent"), "les mots ne sont pas écrasés par le marqueur");
  assert.deepStrictEqual(errs, []);
  await p.close();

  /* 1 bis. avec animation : le texte s'écrit lettre à lettre puis passe au mot suivant */
  ({ p } = await open('<span id="t" data-dz-typed="ab|cd" data-dz-speed="20" data-dz-pause="50">ab</span>', true));
  await p.waitForTimeout(400);
  const vus = await p.evaluate(async () => { const t = document.getElementById("t"), seen = new Set(); const seq = []; for (let i = 0; i < 120; i++) { if (seq[seq.length - 1] !== t.textContent) seq.push(t.textContent); await new Promise((r) => setTimeout(r, 15)); } return seq; });
  assert.ok(vus.some((v) => v.startsWith("c")), `le mot suivant arrive (vu : ${vus.join(", ")})`);
  await p.close();

  /* 2. bouton Copier (classe dz-copy) : copie le code voisin, pas « 1 » */
  ({ p } = await open('<div class="dz-code"><pre><code>npm run build</code></pre><button id="b" class="dz-copy">Copier</button></div>'));
  await p.click("#b");
  await p.waitForTimeout(100);
  assert.strictEqual(await p.evaluate(() => navigator.clipboard.readText()), "npm run build");
  await p.close();

  /* 2 bis. data-dz-copy avec un texte donné : le bouton marche et copie ce texte */
  ({ p } = await open('<button id="b" data-dz-copy="SALUT-2026">Copier</button>'));
  await p.click("#b");
  await p.waitForTimeout(100);
  assert.strictEqual(await p.evaluate(() => navigator.clipboard.readText()), "SALUT-2026");
  await p.close();

  /* 3. effet 3D : l'angle réglé reste celui donné (souris « fine » requise) */
  ({ p } = await open('<div id="c" data-dz-tilt="14" style="width:300px;height:200px">carte</div>', true));
  r = await p.evaluate(() => ({ fin: matchMedia("(hover: hover) and (pointer: fine)").matches, tilt: document.getElementById("c").getAttribute("data-dz-tilt") }));
  assert.strictEqual(r.tilt, "14", "l'angle n'est pas écrasé par le marqueur");
  await p.close();

  console.log("moteur navigateur ok : texte qui s'écrit, Copier, 3D");
} finally {
  await browser.close();
  fs.rmSync(tmp, { force: true });
}
