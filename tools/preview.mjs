/* =====================================================================
   Aperçu et contrôle des blocs, sans serveur Saltcorn.
     node tools/preview.mjs [famille|all] [--only "nom exact"] [--no-diff]
   Pour chaque bloc : rendu par le vrai moteur de Saltcorn (@saltcorn/markup),
   captures bureau sombre / bureau clair / mobile sombre, et contrôles :
     - débordement horizontal sur mobile,
     - erreurs JavaScript,
     - écart entre le HTML d'origine et la version convertie en éléments
       natifs du builder (doit être ~0 %).
   Sorties : build/preview/<famille>/*.png, planche contact
   build/preview/<famille>.png et rapport build/preview/report.json.
   (Lancer d'abord : node tools/build.mjs)
   ===================================================================== */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const require = createRequire(import.meta.url);
const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TOOLS, "..");
const render = require("@saltcorn/markup/layout");
const { chromium } = require("playwright");

const args = process.argv.slice(2);
const fam = args[0] && !args[0].startsWith("--") ? args[0] : "all";
const only = args.includes("--only") ? args[args.indexOf("--only") + 1] : null;
const doDiff = !args.includes("--no-diff");
const exe = ["/opt/pw-browsers/chromium", process.env.CHROMIUM_PATH].find((p) => p && fs.existsSync(p));

const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "build/blocks.json"), "utf8"));
const rawLib = JSON.parse(fs.readFileSync(path.join(ROOT, "build/blocks.raw.json"), "utf8")).library;
const famOf = {};
for (const [k, v] of Object.entries(packs.families)) for (const n of v.blocks) famOf[n] = k;
const blocks = packs.library.filter((b) => (fam === "all" || famOf[b.name] === fam) && (!only || b.name === only));
if (!blocks.length) { console.error("aucun bloc pour", fam, only || ""); process.exit(1); }
const rawOf = (name) => rawLib.find((b) => b.name === name);

const nm = (p) => "file://" + path.join(TOOLS, "node_modules", p);
const page = (layout, theme) => `<!doctype html><html lang="fr" data-bs-theme="${theme}" data-dz-preset="${process.env.PRESET || "nocturne"}" data-dz-style="moderne" class="dz-skin dz-js" data-dz-motion="off"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="${nm("bootstrap/dist/css/bootstrap.min.css")}"><link rel="stylesheet" href="file://${TOOLS}/fixtures/saltcorn.css"><link rel="stylesheet" href="${nm("@fortawesome/fontawesome-free/css/all.min.css")}">
<link rel="stylesheet" href="file://${ROOT}/build/dz-core.css"><link rel="stylesheet" href="file://${ROOT}/build/dz-skin.css">${fs.readdirSync(path.join(ROOT, "build")).filter((f) => /^dz-f-.*\.css$/.test(f)).map((f) => `<link rel="stylesheet" href="file://${ROOT}/build/${f}">`).join("")}
<style>*{animation-play-state:paused!important}.dz-reveal,[data-dz-reveal],.dz-stagger>*{opacity:1!important;transform:none!important}</style></head>
<body><div id="blk">${render({ blockDispatch: {}, layout, role: 1, req: {} })}</div><script src="file://${ROOT}/build/dz.js"></script></body></html>`;

const slug = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const outDir = path.join(ROOT, "build/preview");
fs.mkdirSync(outDir, { recursive: true });
const tmp = path.join(outDir, "_tmp.html");

const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const ctx = await browser.newContext();
await ctx.route(/^https?:\/\/(?!fonts)/, (r) => {
  const u = r.request().url();
  if (/picsum\.photos|images\.unsplash|i\.pravatar/.test(u)) return r.fulfill({ path: path.join(TOOLS, "fixtures", "photo.jpg"), contentType: "image/jpeg" }).catch(() => r.abort());
  return r.abort();
});
const report = [];
const variants = [
  ["dark", 1280, "dark"],
  ["light", 1280, "light"],
  ["mobile", 390, "dark"],
];
for (const b of blocks) {
  const f = famOf[b.name];
  fs.mkdirSync(path.join(outDir, f), { recursive: true });
  const item = { name: b.name, family: f, errors: [], overflowMobile: false, diff: null, shots: [] };
  for (const [v, w, theme] of variants) {
    const p = await ctx.newPage({ viewport: { width: w, height: 900 } });
    p.on("pageerror", (e) => item.errors.push(e.message));
    fs.writeFileSync(tmp, page(b.layout, theme));
    await p.goto("file://" + tmp);
    await p.waitForTimeout(250);
    if (v === "mobile") item.overflowMobile = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    const el = await p.$("#blk");
    const bb = await el.boundingBox();
    const file = path.join(outDir, f, `${slug(b.name)}-${v}.png`);
    if (bb && bb.height > 1) {
      await p.setViewportSize({ width: w, height: Math.min(Math.max(200, Math.ceil(bb.height)), 4000) });
      await el.screenshot({ path: file });
      item.shots.push(path.relative(ROOT, file));
    } else item.errors.push("bloc invisible (hauteur 0) en " + v);
    await p.close();
  }
  if (doDiff) {
    const r = rawOf(b.name);
    if (r) {
      const shot = async (layout, name) => {
        const p = await ctx.newPage({ viewport: { width: 1280, height: 900 } });
        fs.writeFileSync(tmp, page(layout, "dark"));
        await p.goto("file://" + tmp);
        await p.waitForTimeout(150);
        const el = await p.$("#blk");
        const bb = await el.boundingBox();
        const out = path.join(outDir, `_${name}.png`);
        if (bb && bb.height > 1) { await p.setViewportSize({ width: 1280, height: Math.min(Math.ceil(bb.height), 4000) }); await el.screenshot({ path: out }); }
        await p.close();
        return out;
      };
      const a = await shot(r.layout, "a"), c = await shot(b.layout, "c");
      try {
        item.diff = execFileSync("python3", ["-c", `
from PIL import Image, ImageChops
import sys
A=Image.open(sys.argv[1]).convert("RGB"); C=Image.open(sys.argv[2]).convert("RGB")
if A.size!=C.size: print("taille %sx%s -> %sx%s" % (A.size+C.size))
else:
    d=ImageChops.difference(A,C).convert("L").point(lambda x:255 if x>40 else 0)
    print("%.2f%%" % (100*sum(d.histogram()[255:])/(A.size[0]*A.size[1])))
`, a, c]).toString().trim();
      } catch (e) { item.diff = "?"; }
    }
  }
  report.push(item);
  const flags = [item.overflowMobile && "DÉBORDE sur mobile", item.errors.length && "erreurs: " + item.errors.join(" / "), item.diff && item.diff !== "0.00%" && "écart natif: " + item.diff].filter(Boolean);
  console.log((flags.length ? "⚠ " : "✓ ") + b.name + (flags.length ? "  — " + flags.join(" ; ") : ""));
}
await browser.close();
fs.rmSync(tmp, { force: true });
fs.writeFileSync(path.join(outDir, "report.json"), JSON.stringify(report, null, 1));

/* planches contact : une par famille et par variante */
for (const f of [...new Set(report.map((r) => r.family))]) {
  for (const [v] of variants) {
    const files = report.filter((r) => r.family === f).map((r) => r.shots.find((s) => s.endsWith(`-${v}.png`))).filter(Boolean).map((s) => path.join(ROOT, s));
    if (!files.length) continue;
    execFileSync("python3", ["-c", `
from PIL import Image, ImageDraw
import sys, os
files=sys.argv[2:]; W=${v === "mobile" ? 390 : 1280}; S=${v === "mobile" ? 0.6 : 0.4}
ims=[Image.open(f) for f in files]
cols=${v === "mobile" ? 5 : 3}; cw=int(W*S)+16
rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
H=sum(max(int(im.height*S) for im in r)+34 for r in rows)
sheet=Image.new("RGB",(cw*cols, H),(40,40,44)); d=ImageDraw.Draw(sheet); y=0
for ri,r in enumerate(rows):
    h=max(int(im.height*S) for im in r)
    for ci,im in enumerate(r):
        t=im.resize((int(im.width*S), int(im.height*S)))
        sheet.paste(t,(ci*cw+8,y+26)); d.text((ci*cw+8,y+6), os.path.basename(files[ri*cols+ci])[:60], fill=(230,230,230))
    y+=h+34
sheet.save(sys.argv[1])
`, path.join(outDir, `${f}-${v}.png`), ...files]);
  }
}
const bad = report.filter((r) => r.overflowMobile || r.errors.length || (r.diff && r.diff !== "0.00%" && !/^0\.[0-4]\d%$/.test(r.diff)));
console.log(`\n${report.length} blocs contrôlés, ${bad.length} à revoir. Planches : build/preview/<famille>-<dark|light|mobile>.png`);
