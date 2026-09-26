/* Widgets « briques d'outils » dans un vrai Chromium : on les utilise comme un
   humain (clics, glisser, clavier) et on vérifie ce qui est enregistré dans le champ.
   Lancer après le build : node tests/widgets.test.mjs */
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
const page = (body) => `<!doctype html><html class="dz-skin dz-js" data-dz-motion="off"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="file://${ROOT}/build/dz-core.css"></head><body><form>${body}</form>
<script>window.__dzFam={map:{},url:"",w:"file://${ROOT}/build/dz-w-"};</script><script src="file://${ROOT}/build/dz.js"></script></body></html>`;

const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const tmp = path.join(os.tmpdir(), `dz-widgets-${process.pid}.html`);
export const ouvrir = async (body, largeur = 1100) => {
  fs.writeFileSync(tmp, page(body));
  const p = await browser.newPage();
  await p.setViewportSize({ width: largeur, height: 800 });
  const errs = [];
  p.on("pageerror", (e) => errs.push(e.message));
  await p.goto("file://" + tmp);
  await p.waitForTimeout(400);
  return { p, errs };
};
const valeur = (p, nom) => p.evaluate((n) => { const v = document.querySelector(`[name="${n}"]`).value; return v ? JSON.parse(v) : null; }, nom);
const ok = [];

try {
  /* ---------- parcours ---------- */
  {
    const { p, errs } = await ouvrir('<input type="hidden" name="schema" value=""><div data-dz-widget="parcours" data-champ="schema" data-hauteur="500"></div>');
    assert.ok(await p.isVisible("text=Ajoute une première étape"), "état vide expliqué");
    await p.click('.dzw-pc-pal button[title="Début"]');
    await p.click('.dzw-pc-pal button[title="Étape"]'); /* reliée toute seule à l'étape choisie */
    await p.fill(".dzw-pc-panneau input[aria-label=\"Nom de l'étape\"]", "Vérifier le dossier");
    await p.click('.dzw-pc-pal button[title="Fin"]');
    await p.waitForTimeout(600);
    let v = await valeur(p, "schema");
    assert.strictEqual(v.noeuds.length, 3, "3 étapes enregistrées dans le champ");
    assert.strictEqual(v.liens.length, 2, "reliées automatiquement dans l'ordre d'ajout");
    assert.strictEqual(v.noeuds[1].titre, "Vérifier le dossier");
    assert.ok(await p.isVisible("text=Parcours complet"), "contrôle du schéma au vert");

    /* relier à la main : ajouter une condition, tirer sa sortie « non » vers la fin */
    await p.click(".dzw-pc-zone", { position: { x: 30, y: 30 } }); /* rien de choisi : pas de liaison auto */
    await p.click('.dzw-pc-pal button[title="Condition"]');
    await p.waitForTimeout(100);
    const non = p.locator(".dzw-pc-n.sel .dzw-pc-p.out").nth(1);
    const fin = p.locator(".dzw-pc-n", { hasText: "Fin" }).first();
    const a = await non.boundingBox(), b = await fin.boundingBox();
    await p.mouse.move(a.x + a.width / 2, a.y + a.height / 2); await p.mouse.down();
    await p.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 8 }); await p.mouse.up();
    await p.waitForTimeout(500);
    v = await valeur(p, "schema");
    assert.ok(v.liens.some((l) => l.si === "non"), "flèche « non » créée en tirant");
    assert.ok(await p.isVisible("text=jamais atteinte"), "la condition isolée est signalée");

    /* clavier : Suppr retire l'étape choisie, Ctrl+Z la remet */
    await p.locator(".dzw-pc-n", { hasText: "Condition" }).first().click();
    await p.keyboard.press("Delete"); await p.waitForTimeout(400);
    assert.strictEqual((await valeur(p, "schema")).noeuds.length, 3);
    await p.keyboard.press("Control+z"); await p.waitForTimeout(400);
    assert.strictEqual((await valeur(p, "schema")).noeuds.length, 4, "annuler remet l'étape");
    assert.deepStrictEqual(errs, []);
    await p.close();
    ok.push("parcours");
  }
  /* parcours en lecture : étapes passées et en cours, pas de palette, rien d'écrit */
  {
    const doc = { v: 1, noeuds: [{ id: "d", type: "debut", cle: "debut", x: 0, y: 0 }, { id: "e", type: "etape", cle: "etape", titre: "Étape", x: 260, y: 0 }], liens: [{ id: "l", de: "d", vers: "e" }] };
    const { p, errs } = await ouvrir(`<div data-dz-widget="parcours" data-lecture="true" data-trace='["d"]' data-actif="e" data-valeur='${JSON.stringify(doc)}'></div>`, 390);
    assert.strictEqual(await p.locator(".dzw-pc-pal").count(), 0, "pas d'ajout en lecture");
    assert.strictEqual(await p.locator(".dzw-pc-n.passe").count(), 1);
    assert.strictEqual(await p.locator(".dzw-pc-n.actif").count(), 1);
    assert.ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), "pas de débordement sur mobile");
    assert.deepStrictEqual(errs, []);
    await p.close();
    ok.push("parcours en lecture");
  }
  console.log("widgets ok :", ok.join(", "));
} finally {
  await browser.close();
  fs.rmSync(tmp, { force: true });
}
