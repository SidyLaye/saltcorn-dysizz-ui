/* dysizz-ui — page d'admin /dysizz-ui : familles de blocs, pages de démo, outils */
"use strict";
const { VERSION, isAdmin, esc, denied, post } = require("../core");
const { readPack } = require("../assets");
const { findMe, getCfg, patchCfg } = require("../pluginCfg");

const emptyPack = () => ({ tables: [], views: [], plugins: [], pages: [], page_groups: [], triggers: [], roles: [], library: [] });
const flash = (q) => (q.ok ? `<div class="dz-callout dz-callout-success mb-4"><div>${esc(q.ok)}</div></div>` : q.err ? `<div class="dz-callout dz-callout-danger mb-4"><div>${esc(q.err)}</div></div>` : "");

const adminPage = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const Library = require("@saltcorn/data/models/library");
  const Page = require("@saltcorn/data/models/page");
  const pack = readPack("blocks.json");
  const demo = readPack("demo-pages.json").pages;
  const libNames = new Set((await Library.find({})).map((l) => l.name));
  const cfg = await getCfg();
  const active = new Set(Array.isArray(cfg.families) ? cfg.families : []);
  const pagesPresent = demo.filter((p) => Page.findOne({ name: p.name })).length;
  const me = await findMe();
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const fams = Object.entries(pack.families).filter(([, f]) => f.blocks.length);
  const html = `
<style>
.dzh-fams{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:.8rem;margin:1rem 0}
.dzh-fam{display:flex;gap:.8rem;align-items:flex-start;padding:1rem;border:1px solid var(--dz-border);border-radius:var(--dz-radius);background:var(--dz-surface);cursor:pointer}
.dzh-fam:has(input:checked){border-color:var(--dz-primary);box-shadow:0 0 0 1px var(--dz-primary)}
.dzh-fam input{margin-top:.3rem;accent-color:var(--dz-primary)}
.dzh-fam b{display:block}.dzh-fam small{color:var(--dz-text-mute);line-height:1.35;display:block}
.dzh-count{font:600 .72rem var(--dz-font-mono);color:var(--dz-text-soft)}
</style>
<div class="dz-container" style="padding-top:1rem">
  ${flash(req.query || {})}
  <span class="dz-eyebrow">Dysizz UI · v${esc(VERSION)}</span>
  <h1 class="dz-h2">Kit de design</h1>
  <p class="dz-lead">Choisis les familles de blocs utiles à ce tenant : leurs blocs arrivent dans le panneau <b>Library</b> du builder et leur style est chargé sur les pages. Les autres ne pèsent rien.</p>
  <form method="post" action="/dysizz-ui/families"><input type="hidden" name="_csrf" value="${esc(csrf)}">
    <div class="dzh-fams">
      ${fams.map(([k, f]) => {
        const n = f.blocks.filter((b) => libNames.has(b)).length;
        return `<label class="dzh-fam"><input type="checkbox" name="fam_${esc(k)}" value="1"${active.has(k) || n ? " checked" : ""}>
          <span><b><i class="${esc(f.icon)}"></i> ${esc(f.label)}</b><small>${esc(f.description)}</small><span class="dzh-count">${n} / ${f.blocks.length} blocs installés · <a href="/dysizz-ui/galerie?f=${esc(k)}">voir</a></span></span></label>`;
      }).join("")}
    </div>
    <label class="small"><input type="checkbox" name="prune" value="1"> retirer de la Library les blocs du kit des familles décochées (tes blocs perso ne sont jamais touchés ; les pages déjà faites ne changent pas)</label>
    <div class="dz-cluster mt-3"><button class="dz-btn" type="submit"><i class="fas fa-download"></i> Installer / mettre à jour</button></div>
  </form>
  <div class="dz-grid dz-grid-3" style="margin-top:2.5rem">
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-code"></i></div><h3 class="dz-h4">Atelier de blocs</h3><p>Crée ou modifie un bloc en visuel (sans code) ou en code, avec aperçu. Export / import entre tenants.</p><a class="dz-btn" href="/dysizz-ui/blocks">Ouvrir l'atelier</a></div>
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-swatchbook"></i></div><h3 class="dz-h4">Classes</h3><p>Ce qu'il y a derrière chaque classe du kit (CSS + aperçu), et tes propres classes, créées en visuel ou en code.</p><a class="dz-btn" href="/dysizz-ui/classes">Ouvrir</a></div>
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-film"></i></div><h3 class="dz-h4">Transitions</h3><p>Essaie les transitions entre sections, le défilement doux et l'aimantation avant de les choisir.</p><a class="dz-btn dz-btn-ghost" href="/dysizz-ui/transitions">Essayer</a></div>
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-palette"></i></div><h3 class="dz-h4">Réglages du thème</h3><p>Univers, couleurs, polices, arrondis, animations, transitions. Propres à ce tenant.</p><a class="dz-btn dz-btn-ghost" href="/plugins/configure/${encodeURIComponent(me ? me.name : "dysizz-ui")}">Ouvrir les réglages</a></div>
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-file-alt"></i></div><h3 class="dz-h4">Pages de démo</h3><p>${pagesPresent} / ${demo.length} installées : ${demo.map((p) => `<a href="/page/${encodeURIComponent(p.name)}">${esc(p.name)}</a>`).join(", ")}. Visibles par les admins.</p>
      <form method="post" action="/dysizz-ui/install-pages"><input type="hidden" name="_csrf" value="${esc(csrf)}"><button class="dz-btn dz-btn-ghost" type="submit">${pagesPresent ? "Réinstaller" : "Installer"}</button></form></div>
    <div class="dz-card"><div class="dz-icon"><i class="fas fa-book"></i></div><h3 class="dz-h4">Documentation</h3><p>README, guide d'écriture des blocs (docs/BLOCKS.md) et guide de production (docs/SCALING.md) dans le dépôt.</p></div>
  </div>
</div>`;
  res.sendWrap("Dysizz UI", { above: [{ type: "blank", contents: html }] });
};

/* installe les familles cochées, enregistre le choix dans la config du plugin */
const saveFamilies = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const Library = require("@saltcorn/data/models/library");
  const { install_pack } = require("@saltcorn/admin-models/models/pack");
  const b = post(req);
  const pack = readPack("blocks.json");
  const chosen = Object.keys(pack.families).filter((k) => b[`fam_${k}`]);
  const wanted = new Set(chosen.flatMap((k) => pack.families[k].blocks));
  const kitAll = new Set(pack.library.map((l) => l.name));
  let removed = 0;
  for (const l of await Library.find({})) {
    const oldName = (pack.previous || []).includes(l.name) && !kitAll.has(l.name);
    const unwanted = b.prune && kitAll.has(l.name) && !wanted.has(l.name);
    if (oldName || unwanted || l.name.startsWith("DZ · ")) { await l.delete(); removed++; }
  }
  const lib = pack.library.filter((l) => wanted.has(l.name));
  await install_pack({ ...emptyPack(), library: lib }, undefined, async () => {});
  await patchCfg({ families: chosen });
  res.redirect("/dysizz-ui?ok=" + encodeURIComponent(`${lib.length} blocs installés (${chosen.length} familles)${removed ? `, ${removed} retirés` : ""}. Ouvre une page dans le builder, panneau Library.`));
};

const installPages = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const { install_pack } = require("@saltcorn/admin-models/models/pack");
  const src = readPack("demo-pages.json");
  await install_pack({ ...emptyPack(), pages: src.pages }, undefined, async () => {});
  const { getState } = require("@saltcorn/data/db/state");
  if (getState().refresh_pages) { await getState().refresh_pages(true); await getState().refresh_pages(); }
  /* les pages de démo utilisent les familles site, app et mobile */
  const cfg = await getCfg();
  const fams = new Set([...(cfg.families || []), "site", "app", "mobile"]);
  await patchCfg({ families: [...fams] });
  res.redirect("/dysizz-ui?ok=" + encodeURIComponent(`${src.pages.length} pages de démo installées.`));
};

/* galerie d'une famille : tous ses blocs rendus sur une seule page */
const galerie = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const pack = readPack("blocks.json");
  const f = (req.query && req.query.f) || "site";
  const fam = pack.families[f];
  if (!fam) return res.redirect("/dysizz-ui");
  const render = require("@saltcorn/markup/layout");
  const { pub } = require("../core");
  const blocks = pack.library.filter((l) => fam.blocks.includes(l.name));
  const body = blocks.map((l) => `<div class="dzg-item"><div class="dzg-label">${esc(l.name)}</div>${render({ blockDispatch: {}, layout: l.layout, role: 1, req })}</div>`).join("");
  const nav = Object.entries(pack.families).filter(([, x]) => x.blocks.length).map(([k, x]) => `<a class="dz-chip${k === f ? " dz-active" : ""}" href="?f=${k}">${esc(x.label)} (${x.blocks.length})</a>`).join("");
  res.sendWrap({ title: `Galerie · ${fam.label}`, requestFluidLayout: true, headers: [{ css: pub(`dz-f-${f}.css`) }] }, { above: [{ type: "blank", contents: `
<style>.dzg-item{position:relative;margin:0 0 3rem}.dzg-label{position:sticky;top:0;z-index:5;display:inline-block;margin:0 0 .5rem 1rem;padding:.25rem .7rem;border-radius:99px;background:var(--dz-text);color:var(--dz-bg);font:600 .78rem var(--dz-font-mono)}</style>
<div class="dz-container" style="padding:1rem 0"><a href="/dysizz-ui" class="small">← Kit de design</a><h1 class="dz-h2">${esc(fam.label)}</h1><p class="dz-lead">${esc(fam.description)}</p><div class="dz-chips" style="flex-wrap:wrap;gap:.4rem">${nav}</div></div>${body}` }] });
};

module.exports = { adminPage, saveFamilies, installPages, galerie, emptyPack };
