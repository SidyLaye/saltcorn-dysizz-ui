/* dysizz-ui — page d'essai des transitions entre sections (/dysizz-ui/transitions) */
"use strict";
const { isAdmin, esc, denied } = require("../core");
const { TRANSITIONS, SNAPS, SMOOTHS } = require("../settings");

const EDGES = ["wave", "slant", "curve", "arc", "zigzag", "steps"];

const q = (req, k, list, d) => {
  const v = req.query && req.query[k];
  return Object.prototype.hasOwnProperty.call(list, v) ? v : d;
};

const transitionsPage = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const tr = q(req, "tr", TRANSITIONS, "rise");
  const snap = q(req, "snap", SNAPS, "off");
  const smooth = q(req, "smooth", SMOOTHS, "off");
  const morph = req.query && req.query.morph === "1";
  const url = (o) => "/dysizz-ui/transitions?" + new URLSearchParams({ tr, snap, smooth, morph: morph ? "1" : "0", ...o }).toString();
  const chip = (k, label, cur, key) =>
    `<a class="${k === cur ? "is-on" : ""}" href="${esc(url({ [key]: k }))}"${k === cur ? ' aria-current="true"' : ""}>${esc(label)}</a>`;
  const colors = ["bg", "surface", "primary", "surface-2", "accent", "bg"];
  const sections = [1, 2, 3, 4, 5, 6]
    .map((n, i) => {
      const edge = i === 2 ? ` dz-edge-${EDGES[n % EDGES.length]}` : i === 4 ? " dz-edge-round-top" : "";
      const bg = morph ? ` dz-morph-${colors[i]}` : i % 2 ? " dz-bg-surface" : "";
      return `<section class="dz-section${bg}${edge}" style="min-height:90vh;display:grid;place-items:center">
  <div class="dz-container dz-center">
    <span class="dz-eyebrow">Section ${n} / 6</span>
    <h2 class="dz-h1" style="margin:.4em 0">${esc(TRANSITIONS[tr].split(" — ")[0])}</h2>
    <p class="dz-lead" style="max-width:36rem;margin-inline:auto">${esc(TRANSITIONS[tr].split(" — ")[1] || "Aucune transition : les sections défilent normalement.")}${edge ? ` Bord : <code>${esc(edge.trim())}</code>.` : ""}</p>
    <div class="dz-grid dz-grid-3" style="margin-top:2rem;text-align:left">
      ${[1, 2, 3].map((k) => `<div class="dz-card"><div class="dz-icon"><i class="fas fa-${["bolt", "layer-group", "magic"][k - 1]}"></i></div><h3 class="dz-h4">Carte ${k}</h3><p>Contenu d'exemple pour juger l'effet.</p></div>`).join("")}
    </div>
  </div>
</section>`;
    })
    .join("\n");
  const html = `
<div class="dz-page-settings" data-dz-page-tr="${esc(tr)}" data-dz-page-snap="${esc(snap)}" data-dz-page-smooth="${esc(smooth)}" data-dz-page-bgmorph="${morph ? "on" : "off"}">Réglages de la page</div>
<details class="dz-trpanel" open>
  <summary>Transition : <b>${esc(TRANSITIONS[tr].split(" — ")[0])}</b> · aimant ${esc(snap)} · défilement ${esc(smooth)}${morph ? " · fond qui change" : ""}</summary>
  <div class="dz-trpanel-row">${Object.entries(TRANSITIONS).map(([k, v]) => chip(k, v.split(" — ")[0], tr, "tr")).join("")}</div>
  <div class="dz-trpanel-row">
    ${Object.entries(SNAPS).map(([k, v]) => chip(k, "Aimant : " + v.split(" (")[0], snap, "snap")).join("")}
    ${Object.entries(SMOOTHS).map(([k, v]) => chip(k, v.split(" (")[0], smooth, "smooth")).join("")}
    <a class="${morph ? "is-on" : ""}" href="${esc(url({ morph: morph ? "0" : "1" }))}">Fond qui change : ${morph ? "oui" : "non"}</a>
  </div>
  <p>Sur une page : bloc <b>Outil · Réglages de la page</b>, ou classe <code>dz-page-tr-${esc(tr)}</code> sur n'importe quel conteneur. Sur une section : classe <code>dz-tr-${esc(tr)}</code>.</p>
</details>
<style>
.dz-trpanel{position:fixed;left:50%;bottom:.8rem;transform:translateX(-50%);z-index:1040;width:min(94vw,980px);padding:.55rem .9rem;border:1px solid var(--dz-border);border-radius:16px;background:var(--dz-glass);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:var(--dz-shadow-lg);font-size:.82rem}
.dz-trpanel summary{cursor:pointer;list-style:none}
.dz-trpanel-row{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.45rem}
.dz-trpanel-row a{padding:.22rem .6rem;border:1px solid var(--dz-border);border-radius:99px;color:var(--dz-text);text-decoration:none}
.dz-trpanel-row a.is-on{background:var(--dz-primary);color:var(--dz-on-primary);border-color:transparent}
.dz-trpanel p{margin:.45rem 0 0;opacity:.75}
</style>
<section class="dz-section" style="min-height:70vh;display:grid;place-items:center"><div class="dz-container dz-center">
  <span class="dz-eyebrow">Essai des transitions</span><h1 class="dz-display">Fais défiler ↓</h1>
  <p class="dz-lead">Choisis une transition en bas de l'écran, puis descends.</p></div></section>
${sections}`;
  res.sendWrap({ title: "Transitions", no_menu: true, requestFluidLayout: true }, { above: [{ type: "blank", contents: html }] });
};

module.exports = { transitionsPage };
