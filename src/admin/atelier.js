/* dysizz-ui — atelier de blocs */
"use strict";
const { VERSION, pub, isAdmin, esc, post, slug } = require("../core");
const { readPack } = require("../assets");

/* ---------------- Atelier de blocs : créer / modifier / partager ses blocs ----------------
   Un bloc créé ici est un bloc HTML de la Library du builder, comme ceux du kit.
   Le code source (HTML, CSS, JS) est gardé dans le bloc (clé dz_src) pour pouvoir
   le rouvrir et le modifier ici. Le CSS est automatiquement limité au bloc
   (imbrication CSS native : .dzb-xxx { ton css }). */
const kitNames = () => new Set(readPack("blocks.json").library.map((b) => b.name));
const WRAPS = {
  none: "Brut (juste mon HTML)",
  section: "Section + conteneur centré",
  full: "Section pleine largeur",
};
const buildBlockLayout = ({ name, html, css, js, wrap }) => {
  const cls = "dzb-" + slug(name);
  let inner = `<div class="${cls}">${html || ""}</div>`;
  if (wrap === "section") inner = `<section class="dz-section"><div class="dz-container">${inner}</div></section>`;
  if (wrap === "full") inner = `<section class="dz-section dz-flush">${inner}</section>`;
  const style = css && css.trim() ? `<style>.${cls}{${css.replace(/<\/style/gi, "")}}</style>` : "";
  const script =
    js && js.trim()
      ? `<script>(function(){var s=document.currentScript;function run(){document.querySelectorAll(".${cls}").forEach(function(el){if(el.__dzb)return;el.__dzb=1;(function(el){${js.replace(/<\/script/gi, "<\\/script")}\n})(el);});}if(document.readyState!=="loading")run();else document.addEventListener("DOMContentLoaded",run);})();</script>`
      : "";
  return { type: "blank", isHTML: true, contents: style + inner + script, dz_src: { html: html || "", css: css || "", js: js || "", wrap: wrap || "none" } };
};
/* rend un bloc du kit en HTML statique pour s'en servir comme point de départ */
const blockToHtml = (layout) => {
  if (layout && layout.dz_src) return layout.dz_src;
  try {
    const render = require("@saltcorn/markup/layout");
    return { html: render({ blockDispatch: {}, layout, role: 1, req: {} }), css: "", js: "", wrap: "none" };
  } catch (e) {
    return { html: layout && layout.type === "blank" ? layout.contents : "", css: "", js: "", wrap: "none" };
  }
};

const atelierPage = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const kit = kitNames();
  const libs = (await Library.find({})).sort((a, b) => a.name.localeCompare(b.name));
  const mine = libs.filter((l) => !kit.has(l.name));
  let cur = { name: "", icon: "fas fa-cube", html: "", css: "", js: "", wrap: "section", id: "" };
  const q = req.query || {};
  if (q.edit || q.from) {
    const l = libs.find((x) => String(x.id) === String(q.edit || q.from));
    if (l) {
      const src = blockToHtml(l.layout);
      cur = { ...cur, ...src, icon: l.icon || cur.icon, name: q.edit ? l.name : `Mon · ${l.name.replace(/^[^·]*·\s*/, "")}`, id: q.edit ? l.id : "" };
    }
  }
  const data = {
    csrf, cur, wraps: WRAPS, ok: q.ok || "", err: q.err || "",
    mine: mine.map((l) => ({ id: l.id, name: l.name, icon: l.icon })),
    kit: libs.filter((l) => kit.has(l.name)).map((l) => ({ id: l.id, name: l.name })),
    dzjs: pub("dz.js"),
  };
  res.sendWrap(
    { title: "Atelier de blocs", requestFluidLayout: true },
    { above: [{ type: "blank", contents: `<div id="dza-app" style="padding:1rem clamp(.5rem,2vw,1.5rem) 3rem"><a href="/dysizz-ui" class="small">← Kit de design</a><h1 class="dz-h2" style="margin:.3rem 0">Atelier de blocs</h1><p class="dz-lead" style="font-size:1rem">Clique sur un élément de l'aperçu pour le modifier (texte, lien, image, classes, couleurs), ajoute des éléments depuis la palette, ou passe en code. Enregistre : le bloc arrive dans le panneau <b>Library</b> du builder.</p><noscript>JavaScript requis.</noscript></div>
<script type="application/json" id="dza-data">${JSON.stringify(data).replace(/</g, "\\u003c")}</script>
<script src="${pub("dz-editor-atelier.js")}" defer></script>` }] }
  );
};

const saveBlock = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const b = post(req);
  const name = String(b.name || "").trim().slice(0, 80);
  if (!name) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("Donne un nom au bloc."));
  if (kitNames().has(name)) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("Ce nom est réservé à un bloc du kit (il serait écrasé à la prochaine mise à jour). Choisis un autre nom, par ex. « Mon · … »."));
  const icon = /^[a-z0-9 -]{1,60}$/i.test(b.icon || "") ? b.icon : "fas fa-cube";
  const layout = buildBlockLayout({ name, html: b.html, css: b.css, js: b.js, wrap: WRAPS[b.wrap] ? b.wrap : "none" });
  const existing = b.id && !b.as_new ? await Library.findOne({ id: +b.id }) : null;
  const clash = await Library.findOne({ name });
  if (clash && (!existing || clash.id !== existing.id)) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent(`Un bloc « ${name} » existe déjà.`) + (existing ? "&edit=" + existing.id : ""));
  if (existing) await existing.update({ name, icon, layout });
  else await Library.create({ name, icon, layout });
  const saved = await Library.findOne({ name });
  res.redirect(`/dysizz-ui/blocks?edit=${saved ? saved.id : ""}&ok=` + encodeURIComponent(`« ${name} » est enregistré. Il est dans le panneau Library du builder.`));
};

const deleteBlock = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const l = await Library.findOne({ id: +post(req).id });
  if (l && !kitNames().has(l.name)) await l.delete();
  res.redirect("/dysizz-ui/blocks?ok=" + encodeURIComponent("Bloc supprimé."));
};

const exportBlocks = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const kit = kitNames();
  const all = req.query && req.query.all;
  const library = (await Library.find({})).filter((l) => all || !kit.has(l.name)).map((l) => ({ name: l.name, icon: l.icon, layout: l.layout }));
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Content-Disposition", `attachment; filename="blocs-${all ? "library" : "perso"}-${new Date().toISOString().slice(0, 10)}.json"`);
  res.send(JSON.stringify({ format: "dysizz-blocks", version: 1, kit: VERSION, library }, null, 2));
};

const importBlocks = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const b = post(req);
  let data;
  try { data = JSON.parse(b.json || ""); } catch (e) { return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("JSON illisible.")); }
  const items = Array.isArray(data) ? data : data.library || [];
  const kit = kitNames();
  let n = 0, skipped = 0;
  for (const it of items) {
    if (!it || typeof it.name !== "string" || !it.layout || typeof it.layout !== "object") { skipped++; continue; }
    const name = it.name.slice(0, 80);
    const icon = /^[a-z0-9 -]{1,60}$/i.test(it.icon || "") ? it.icon : "fas fa-cube";
    const ex = await Library.findOne({ name });
    if (ex) {
      if (!b.overwrite || kit.has(name)) { skipped++; continue; }
      await ex.update({ icon, layout: it.layout });
    } else await Library.create({ name, icon, layout: it.layout });
    n++;
  }
  res.redirect("/dysizz-ui/blocks?ok=" + encodeURIComponent(`${n} bloc(s) importé(s)${skipped ? `, ${skipped} ignoré(s)` : ""}.`));
};

/* Saltcorn 1.6 garde en cache les en-têtes par rôle : sans ça, un
   changement de réglage (couleur, police…) n'apparaît qu'après un
   redémarrage. On recalcule le cache à chaque (re)chargement du plugin. */

module.exports = { atelierPage, saveBlock, deleteBlock, exportBlocks, importBlocks, kitNames };
