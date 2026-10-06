import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(path.join(root, "tools", "package.json"));
const { chromium } = require("playwright");
const script = fs.readFileSync(path.join(root, "client", "application.js"), "utf8");
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });

const kpi = (t) => `<div data-dz-widget="tableau" data-vue="kpi" data-source="parcours" class="dzw-tb">
  <h3><span>${t}</span><small></small></h3><div class="corps"><b>12</b><p class="dzw-tb-sous">Part des demandes ${t}.</p></div></div>`;

try {
  const page = await browser.newPage();
  await page.setContent(`<html class="dz-app-ui"><body><div id="page-inner-content">
    <div class="dz-ecran dz-page">
      <div class="dz-ecran-titre"><h1>Statistiques</h1></div>
      <div class="dz-ecran-grille"><div data-dz-widget="tableau" data-vue="filtres" data-source="f" class="dzw-tb"></div></div>
      <div class="dz-h4">Le parcours d'une demande</div>
      <div class="dz-ecran-grille dz-ecran-chiffres">${kpi("reçues")}${kpi("retrouvées")}</div>
      <div class="dz-ecran-grille"><div data-dz-widget="tableau" data-vue="barres" data-source="portails" class="dzw-tb"><h3>Portails</h3></div></div>
    </div>
    <div class="dz-ecran-intro">Uniquement ce que les tables savent.</div>
  </div></body></html>`);
  await page.evaluate((s) => {
    window.__dzApplication = { title: "Statistiques", layout: "standard", charts: true, inline_sources: [], sections: [{ title: "Synthèse", sources: ["portails"] }] };
    new Function(s)();
  }, script);

  // le widget redessine son corps à chaque actualisation, en gardant son titre
  for (let i = 0; i < 4; i++) {
    await page.evaluate(() => document.querySelectorAll('[data-vue="kpi"] .corps').forEach((c) => {
      const p = document.createElement("p"); p.className = "dzw-tb-sous"; p.textContent = "Part des demandes.";
      c.replaceChildren(p);
    }));
    await page.waitForTimeout(60);
  }
  const aides = await page.$$eval('[data-vue="kpi"] h3', (hs) => hs.map((h) => h.querySelectorAll(".ux-inline-help").length));
  assert.deepEqual(aides, [1, 1], "une seule aide « i » par indicateur, même après plusieurs actualisations");

  const ordre = await page.evaluate(() => {
    const c = document.querySelector(".dz-app-content"), t = document.querySelector(".ux-section-title"), k = document.querySelector(".ux-kpi-row");
    return { dansEcran: c.contains(t), avantChiffres: t.nextElementSibling === k, intro: c.contains(document.querySelector(".dz-ecran-intro")) };
  });
  assert.deepEqual(ordre, { dansEcran: true, avantChiffres: true, intro: true }, "titre de section et intro restent avec leurs chiffres, pas en bas de page");
  console.log("Présentation navigateur : aide des indicateurs unique, titres de section et intro à leur place OK");
} finally {
  await browser.close();
}
