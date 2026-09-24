/* =====================================================================
   Build du kit : une seule commande, un seul fichier livré (index.js).
     cd tools && npm install && npm run build
   Étapes :
     1. blocs et pages de démo  (tools/build_packs.py → build/*.json)
     2. CSS  : styles/NN-*.css concaténés dans l'ordre, minifiés (esbuild)
     3. JS navigateur : client/*.js minifiés / empaquetés (esbuild)
     4. src/generated/embed.js : tout ce qui précède, embarqué
     5. index.js : le plugin serveur empaqueté (esbuild, @saltcorn/* externes)
   ===================================================================== */
import { build, transform } from "esbuild";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import zlib from "node:zlib";
import { builderParity } from "./builder-parity.mjs";
import { classCatalog } from "./class-catalog.mjs";
import { CLASS_DOCS, EXTRA_DOCS } from "./class-docs.mjs";

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TOOLS, "..");
const r = (...p) => path.join(ROOT, ...p);
const pkg = JSON.parse(fs.readFileSync(r("package.json"), "utf8"));
const VERSION = pkg.version;
const TARGET_CSS = ["chrome115", "firefox120", "safari17"];
const TARGET_JS = ["chrome100", "firefox100", "safari15"];
fs.mkdirSync(r("build"), { recursive: true });
fs.mkdirSync(r("src/generated"), { recursive: true });

/* 1. packs */
const py = spawnSync("python3", [r("tools/build_packs.py")], { stdio: "inherit" });
if (py.status !== 0) process.exit(py.status || 1);

/* 2. CSS */
/* le cœur (00-29) est chargé partout ; chaque famille de blocs (30+) a son
   propre fichier, chargé seulement par les tenants qui l'utilisent */
const FAMILY_OF = (f) => {
  const k = f.replace(/^\d\d-/, "").replace(/\.css$/, "").replace(/-plus$/, "");
  return k === "outils" ? "outils" : k;
};
const allCss = fs.readdirSync(r("styles")).filter((f) => /^\d\d-.*\.css$/.test(f)).sort();
const cssFiles = allCss.filter((f) => +f.slice(0, 2) < 30);
const famFiles = allCss.filter((f) => +f.slice(0, 2) >= 30);
const readCss = (f) => `/* ${f} */\n` + fs.readFileSync(r("styles", f), "utf8");
const coreSrc = cssFiles.map(readCss).join("\n");
const minCss = async (code) => (await transform(code, { loader: "css", minify: true, target: TARGET_CSS, logLevel: "warning" })).code;
const famSrc = {};
for (const f of famFiles) (famSrc[FAMILY_OF(f)] ||= []).push(readCss(f));
const allSrc = coreSrc + "\n" + Object.values(famSrc).flat().join("\n");
const parity = builderParity(allSrc);
fs.writeFileSync(r("build/builder-parity.css"), parity.css);
const out = {
  "dz-core.css": await minCss(coreSrc),
  /* chargé seulement dans l'éditeur de pages (voir src/headers.js) */
  "dz-builder.css": await minCss(parity.css + "\n" + Object.values(famSrc).flat().join("\n")),
  "dz-skin.css": await minCss(fs.readFileSync(r("styles/skin.css"), "utf8")),
};
for (const [fam, parts] of Object.entries(famSrc)) out[`dz-f-${fam}.css`] = await minCss(parts.join("\n"));
/* préfixes de classes → famille (pour le chargement à la demande dans dz.js) */
const famPrefix = {};
for (const [fam, parts] of Object.entries(famSrc)) {
  const m = parts.join("").match(/\.dz-([a-z]{2})-[a-z0-9]/g) || [];
  const counts = {};
  m.forEach((x) => (counts[x.slice(1, 6)] = (counts[x.slice(1, 6)] || 0) + 1));
  const best = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];
  if (best) famPrefix[best[0]] = fam;
}
fs.writeFileSync(r("build/family-prefixes.json"), JSON.stringify(famPrefix));

/* catalogue des classes (page /dysizz-ui/classes) : un fichier par groupe */
const catalog = classCatalog([
  ...cssFiles.filter((f) => !/^0[0-2]/.test(f)).map((f) => ({ group: "c-" + f.slice(0, 2), label: f.slice(3, -4).replace(/-/g, " "), css: fs.readFileSync(r("styles", f), "utf8") })),
  ...Object.entries(famSrc).map(([fam, parts]) => ({ group: "f-" + fam, label: fam, css: parts.join("\n") })),
]);
const catIndex = Object.fromEntries(Object.entries(catalog).map(([g, v]) => [g, { label: v.label, names: Object.keys(v.classes).sort() }]));
fs.writeFileSync(r("build/classes.json"), JSON.stringify(catalog));

/* 3. JS navigateur */
const bundleClient = async (entry, globalName) =>
  (
    await build({
      entryPoints: [r("client", entry)],
      bundle: true,
      minify: true,
      format: "iife",
      globalName,
      target: TARGET_JS,
      write: false,
      legalComments: "inline",
      nodePaths: [r("tools/node_modules")],
      logLevel: "warning",
    })
  ).outputFiles[0].text;
out["dz.js"] = (await bundleClient("dz.js")) + "\n" + (await bundleClient("vues.js"));
out["dz-smooth.js"] = await bundleClient("smooth.js");
for (const f of fs.readdirSync(r("client")).filter((f) => /^editor.*\.js$/.test(f))) out["dz-" + f] = await bundleClient(f);
for (const [k, v] of Object.entries(out)) fs.writeFileSync(r("build", k), v);

/* 4. embarqué : assets + packs + catalogue des classes */
for (const f of ["blocks.json", "demo-pages.json"]) out[f] = JSON.parse(fs.readFileSync(r("build", f), "utf8"));
out["family-prefixes.json"] = famPrefix;
out["classes-index.json"] = catIndex;
out["classes-docs.json"] = { classes: CLASS_DOCS, behaviours: EXTRA_DOCS };
for (const [g, v] of Object.entries(catalog)) out[`classes-${g}.json`] = v.classes;
fs.writeFileSync(r("src/generated/embed.js"), "/* généré par tools/build.mjs — ne pas modifier */\nmodule.exports = " + JSON.stringify(out) + ";\n");

/* 5. serveur */
await build({
  entryPoints: [r("src/index.js")],
  bundle: true,
  platform: "node",
  format: "cjs",
  target: "node18",
  external: ["@saltcorn/*"],
  define: { __DZ_VERSION__: JSON.stringify(VERSION) },
  outfile: r("index.js"),
  legalComments: "inline",
  banner: { js: `/* dysizz-ui ${VERSION} — FICHIER GÉNÉRÉ par tools/build.mjs depuis src/, styles/, client/ et blocks/. Ne pas modifier à la main. */` },
  logLevel: "warning",
});

const kb = (s) => (Buffer.byteLength(s) / 1024).toFixed(0);
const br = (s) => (zlib.brotliCompressSync(Buffer.from(s)).length / 1024).toFixed(0);
console.log(`parité builder : ${parity.layoutClasses.length} classes de mise en page`);
console.log(`dysizz-ui ${VERSION} → index.js ${kb(fs.readFileSync(r("index.js"), "utf8"))} Ko`);
for (const k of Object.keys(out).filter((k) => /\.(css|js)$/.test(k))) console.log(`  ${k.padEnd(18)} ${kb(out[k]).padStart(4)} Ko  (brotli ${br(out[k])} Ko)`);
