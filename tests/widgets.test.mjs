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
    assert.ok(!/\bnull\b|undefined/.test(await p.innerText("body")), "jamais de « null » ni « undefined » affiché");

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
  /* ---------- formulaire : construire ---------- */
  {
    const { p, errs } = await ouvrir('<input type="hidden" name="f" value=""><div data-dz-widget="formulaire" data-champ="f"></div>');
    await p.fill('input[aria-label="Titre du formulaire"]', "Inscription");
    await p.click('.dzw-fo-types button[title="E-mail"]');
    await p.fill(".dzw-fo-edit input >> nth=0", "Votre e-mail");
    await p.click('.dzw-fo-edit input[type=checkbox]');
    await p.click('.dzw-fo-types button[title="Un choix"]');
    await p.fill(".dzw-fo-edit textarea", "Matin\nAprès-midi");
    await p.waitForTimeout(500);
    const v = await valeur(p, "f");
    assert.strictEqual(v.titre, "Inscription");
    assert.deepStrictEqual(v.champs.map((c) => c.type), ["email", "choix"]);
    assert.strictEqual(v.champs[0].requis, true); assert.deepStrictEqual(v.champs[1].options, ["Matin", "Après-midi"]);
    assert.ok(await p.isVisible('.dzw-fo-col[aria-label="Aperçu"] >> text=Après-midi'), "aperçu en direct");
    assert.ok(!/\bnull\b|undefined/.test(await p.innerText("body")), "jamais de « null » ni « undefined » affiché");
    await p.click('.dzw-fo-it >> nth=1 >> button[title="Monter"]'); await p.waitForTimeout(400);
    assert.strictEqual((await valeur(p, "f")).champs[0].type, "choix", "réordonner");
    assert.deepStrictEqual(errs, []); await p.close(); ok.push("formulaire (construire)");
  }
  /* ---------- formulaire : remplir, avec contrôles ---------- */
  {
    const sc = { v: 1, titre: "T", champs: [{ id: "n", type: "texte", label: "Nom", requis: true }, { id: "m", type: "email", label: "E-mail" }, { id: "c", type: "choix", label: "Créneau", options: ["Matin", "Soir"], requis: true }, { id: "e", type: "note", label: "Note", max: 5 }] };
    const { p, errs } = await ouvrir(`<input type="hidden" name="r" value=""><div data-dz-widget="formulaire" data-mode="remplir" data-champ="r" data-schema='${JSON.stringify(sc)}'></div><button id="go">Envoyer</button>`, 390);
    await p.evaluate(() => { document.querySelector("form").addEventListener("submit", (e) => { e.preventDefault(); window.__envoye = true; }); });
    await p.click("#go");
    assert.ok(!(await p.evaluate(() => window.__envoye)), "envoi bloqué tant qu'il manque des réponses");
    assert.ok(await p.isVisible("text=2 réponse(s) à corriger"));
    await p.fill("input[aria-required=true] >> nth=0", "Awa");
    await p.fill('input[type=email]', "pas-un-mail"); await p.press('input[type=email]', "Tab");
    assert.ok(await p.isVisible("text=Adresse e-mail invalide"), "format vérifié en direct");
    await p.fill('input[type=email]', "awa@exemple.fr");
    await p.click("text=Soir");
    await p.click('button[aria-label="4 sur 5"]');
    await p.click("#go");
    assert.ok(await p.evaluate(() => window.__envoye), "envoi accepté quand tout est bon");
    const r = await valeur(p, "r");
    assert.deepStrictEqual(r, { n: "Awa", m: "awa@exemple.fr", c: "Soir", e: 4 });
    assert.ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), "pas de débordement sur mobile");
    assert.deepStrictEqual(errs, []); await p.close(); ok.push("formulaire (remplir)");
  }
  /* ---------- règles ---------- */
  {
    const champs = [{ nom: "montant", label: "Montant", type: "nombre" }, { nom: "service", label: "Service", type: "choix", options: ["Achats", "RH"] }, { nom: "ref", label: "Référence", type: "texte" }];
    const { p, errs } = await ouvrir(`<input type="hidden" name="g" value=""><div data-dz-widget="regles" data-champ="g" data-champs='${JSON.stringify(champs)}'></div>`);
    await p.click('button[title="Ajouter une condition"]');
    await p.selectOption('select[aria-label="Opérateur"]', "sup");
    await p.fill('input[aria-label="Valeur"]', "500");
    await p.click('button[title="Ajouter une condition"]');
    await p.selectOption('select[aria-label="Champ"] >> nth=1', "service");
    await p.selectOption('select[aria-label="Valeur"]', "Achats");
    await p.waitForTimeout(400);
    const v = await valeur(p, "g");
    assert.strictEqual(v.texte, "Si Montant > « 500 » et Service est « Achats »");
    const f = new Function("ctx", `return (${v.expression});`);
    assert.strictEqual(f({ montant: 800, service: "Achats" }), true);
    assert.strictEqual(f({ montant: 800, service: "RH" }), false);
    assert.strictEqual(f({ montant: 100, service: "Achats" }), false);
    /* une valeur piégée reste une chaîne, jamais du code */
    await p.click('button[title="Ajouter une condition"]');
    await p.selectOption('select[aria-label="Champ"] >> nth=2', "ref");
    await p.fill('input[type=text][aria-label="Valeur"]', '") || process.exit(1) || ("');
    await p.waitForTimeout(400);
    const ex = (await valeur(p, "g")).expression;
    assert.strictEqual(new Function("ctx", `return (${ex});`)({ montant: 800, service: "Achats", ref: '") || process.exit(1) || ("' }), true, "la valeur piégée est comparée comme du texte, jamais exécutée");
    assert.deepStrictEqual(errs, []); await p.close(); ok.push("règles");
  }
  /* ---------- document ---------- */
  {
    const { p, errs } = await ouvrir('<input type="hidden" name="d" value=""><div data-dz-widget="document" data-champ="d"></div>');
    const b0 = p.locator(".dzw-doc-b [contenteditable] >> nth=0");
    await b0.click(); await p.keyboard.type("/tit");
    assert.ok(await p.isVisible(".dzw-doc-menu"), "menu « / »");
    await p.keyboard.press("Enter");
    await p.keyboard.type("Compte rendu");
    await p.keyboard.press("Enter");
    await p.keyboard.type("Présents : Awa et Moussa");
    await p.keyboard.press("Enter"); await p.keyboard.type("/case"); await p.keyboard.press("Enter");
    await p.keyboard.type("Envoyer le devis");
    await p.waitForTimeout(500);
    let v = await valeur(p, "d");
    assert.deepStrictEqual(v.blocs.map((b) => b.t), ["h1", "p", "tache"].map((t, i) => (i === 0 ? v.blocs[0].t : t)));
    assert.ok(["h1", "h2", "h3"].includes(v.blocs[0].t), "titre choisi au clavier");
    assert.strictEqual(v.blocs[2].html, "Envoyer le devis");
    await p.click('.dzw-doc-b.t-tache input[type=checkbox]'); await p.waitForTimeout(400);
    assert.strictEqual((await valeur(p, "d")).blocs[2].fait, true);
    /* nettoyage : un script collé ou injecté ne survit pas */
    await p.evaluate(() => { const e = document.querySelectorAll(".dzw-doc-b [contenteditable]")[1]; e.innerHTML = 'ok <img src=x onerror="window.__pwn=1"><script>window.__pwn=1</script><a href="javascript:alert(1)">x</a>'; e.dispatchEvent(new Event("input", { bubbles: true })); });
    await p.waitForTimeout(500);
    v = await valeur(p, "d");
    assert.ok(!/img|script|javascript:/i.test(v.blocs[1].html), `HTML nettoyé : ${v.blocs[1].html}`);
    assert.deepStrictEqual(errs, []); await p.close(); ok.push("document");
  }
  /* ---------- planning ---------- */
  {
    const { p, errs } = await ouvrir('<input type="hidden" name="pl" value=""><div data-dz-widget="planning" data-champ="pl" data-date="2026-09-28" data-jours="5" data-hauteur="560"></div>');
    const col = p.locator(".dzw-pl-col >> nth=1");
    const bb = await col.boundingBox();
    await p.mouse.move(bb.x + bb.width / 2, bb.y + 60); await p.mouse.down();
    await p.mouse.move(bb.x + bb.width / 2, bb.y + 140, { steps: 6 }); await p.mouse.up();
    await p.waitForTimeout(200);
    assert.ok(await p.isVisible(".dzw-pl-pop"), "fenêtre de modification ouverte après création");
    await p.fill('.dzw-pl-pop input[aria-label="Titre"]', "Rendez-vous banque");
    await p.keyboard.press("Enter");
    await p.waitForTimeout(400);
    let v = await valeur(p, "pl");
    assert.strictEqual(v.evenements.length, 1);
    assert.strictEqual(v.evenements[0].titre, "Rendez-vous banque"); assert.strictEqual(v.evenements[0].date, "2026-09-29");
    const avant = v.evenements[0].debut;
    await p.locator(".dzw-pl-ev").focus(); await p.keyboard.press("ArrowDown"); await p.keyboard.press("ArrowRight"); await p.waitForTimeout(400);
    v = await valeur(p, "pl");
    assert.notStrictEqual(v.evenements[0].debut, avant, "déplacé au clavier (heure)"); assert.strictEqual(v.evenements[0].date, "2026-09-30", "déplacé au clavier (jour)");
    await p.locator(".dzw-pl-ev").focus(); await p.keyboard.press("Delete"); await p.waitForTimeout(400);
    assert.strictEqual((await valeur(p, "pl")).evenements.length, 0);
    await p.setViewportSize({ width: 390, height: 800 }); await p.waitForTimeout(300);
    assert.strictEqual(await p.locator(".dzw-pl-col").count(), 1, "un jour à la fois sur téléphone");
    assert.ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), "pas de débordement sur mobile");
    assert.deepStrictEqual(errs, []); await p.close(); ok.push("planning");
  }
  /* ---------- tableau de bord (sources de données simulées par un petit serveur) ---------- */
  {
    const http = await import("node:http");
    const appels = [];
    const donnees = (nom, q) => {
      if (nom === "resume") return { type: "agregat", valeurs: { total: q.source === "b" ? 5 : 120, rejets: 12 }, precedent: { total: 100, rejets: 15 } };
      if (nom === "jours") return { type: "serie", par: "jour", lignes: Array.from({ length: 14 }, (_, i) => ({ cle: `2026-09-${String(i + 1).padStart(2, "0")}`, total: (i * 7) % 11 })) };
      if (nom === "portails") return { type: "agregat", lignes: [{ cle: "a", total: 80 }, { cle: "b", total: 40 }] };
      if (nom === "liste") { const page = +q.page || 1; return { type: "liste", total: 120, page, par_page: 50, tri: q.tri || "cree_le", sens: q.sens || "desc", lignes: Array.from({ length: 3 }, (_, i) => ({ id: page * 10 + i, cree_le: "2026-09-20T10:00:00Z", nom: "Nom" + i, source: "a", statut: i ? "ok" : "ko" })) }; }
      return null;
    };
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      if (u.pathname.startsWith("/dysizz/donnees/")) {
        const nom = u.pathname.split("/").pop(), q = Object.fromEntries(u.searchParams);
        appels.push({ nom, q });
        const d = donnees(nom, q);
        res.writeHead(d ? 200 : 404, { "Content-Type": "application/json" }); return res.end(JSON.stringify(d || { erreur: "source introuvable" }));
      }
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(page(`<div data-dz-widget="tableau" data-vue="filtres" data-champs='[{"type":"periode","param":"periode","defaut":"30j"},{"param":"source","titre":"Portail","source":"portails"},{"type":"texte","param":"q"}]' data-libelles='{"a":"Portail A","b":"Portail B"}'></div>
<div data-dz-widget="tableau" data-source="resume" data-vue="kpi" data-titre="Demandes" data-mesure="total"></div>
<div data-dz-widget="tableau" data-source="resume" data-vue="kpi" data-titre="Rejets" data-mesure="rejets" data-inverse="true"></div>
<div data-dz-widget="tableau" data-source="jours" data-vue="courbe" data-titre="Par jour"></div>
<div data-dz-widget="tableau" data-source="portails" data-vue="barres" data-filtre="source" data-libelles='{"a":"Portail A","b":"Portail B"}'></div>
<div data-dz-widget="tableau" data-source="portails" data-vue="anneau"></div>
<div data-dz-widget="tableau" data-source="absente" data-vue="kpi"></div>
<div data-dz-widget="tableau" data-source="liste" data-vue="liste" data-lien="/fiche?id={id}" data-colonnes='[{"champ":"nom","titre":"Nom"},{"champ":"statut","titre":"Statut","pastilles":{"ok":{"texte":"Bon","couleur":"#047857"}}}]'></div>`).replaceAll(`file://${ROOT}/build/`, "/build/"));
    });
    /* les fichiers du kit, servis par le même serveur */
    const servirFichier = srv.listeners("request")[0];
    srv.removeAllListeners("request");
    srv.on("request", (req, res) => {
      if (req.url.startsWith("/build/")) { const f = path.join(ROOT, req.url.split("?")[0]); if (fs.existsSync(f)) { res.writeHead(200, { "Content-Type": f.endsWith(".css") ? "text/css" : "text/javascript" }); return res.end(fs.readFileSync(f)); } }
      servirFichier(req, res);
    });
    await new Promise((r) => srv.listen(0, r));
    const base = `http://127.0.0.1:${srv.address().port}`;
    const p = await browser.newPage();
    await p.setViewportSize({ width: 1100, height: 900 });
    const errs = [];
    p.on("pageerror", (e) => errs.push(e.message));
    await p.goto(base + "/");
    await p.waitForSelector(".dzw-tb-table");
    await p.waitForTimeout(300);
    assert.ok(p.url().includes("periode=30j"), "période par défaut posée dans l'adresse");
    assert.ok(appels.filter((a) => a.nom === "resume").every((a) => a.q.periode === "30j"), "les chiffres lisent la période par défaut");
    const txt = await p.innerText("body");
    assert.ok(txt.includes("120") && /\+20 %/.test(txt), "chiffre clé et écart avec la période précédente");
    assert.ok(await p.isVisible(".dzw-tb-delta.inv.down"), "baisse des rejets affichée en bien (inverse)");
    assert.ok(await p.locator(".dzw-tb-barre", { hasText: "Portail A" }).isVisible(), "libellés appliqués");
    assert.ok(await p.isVisible("text=Lecture impossible : source introuvable"), "erreur de source expliquée");
    assert.ok(await p.isVisible("text=120 résultats"), "total de la liste");
    assert.ok(await p.isVisible("text=Bon"), "pastille de statut");
    assert.ok((await p.locator(".dzw-tb svg polyline").count()) >= 1, "courbe dessinée");
    /* un clic sur une barre filtre toute la page, sans recharger */
    await p.evaluate(() => { window.__pasRecharge = 1; });
    const avant = appels.length;
    await p.click('.dzw-tb-barre[data-cle="b"]');
    await p.waitForTimeout(500);
    assert.ok(p.url().includes("source=b"), "filtre écrit dans l'adresse");
    assert.strictEqual(await p.evaluate(() => window.__pasRecharge), 1, "page non rechargée");
    assert.ok(appels.slice(avant).some((a) => a.nom === "resume" && a.q.source === "b"), "les blocs relisent avec le filtre");
    assert.ok((await p.innerText("body")).includes("5"), "chiffre mis à jour");
    assert.strictEqual(await p.locator(".dzw-tb-filtres select").inputValue(), "", "la liste déroulante suit l'adresse au rechargement");
    /* pagination et tri */
    await p.click("text=Suivant ›"); await p.waitForTimeout(300);
    assert.ok(await p.isVisible("text=2 / 3"), "page suivante");
    await p.click('th[data-tri="nom"]'); await p.waitForTimeout(300);
    assert.ok(appels.at(-1).q.tri === "nom" && [undefined, "1"].includes(appels.at(-1).q.page), "tri demandé au serveur, retour page 1");
    /* recherche avec délai de frappe */
    await p.fill(".dzw-tb-filtres input[type=search]", "dupont"); await p.waitForTimeout(700);
    assert.ok(appels.some((a) => a.q.q === "dupont"), "recherche transmise");
    /* Retour du navigateur : les filtres reviennent */
    await p.goBack(); await p.waitForTimeout(500);
    assert.ok(!p.url().includes("dupont"), "retour arrière");
    /* ligne cliquable */
    await p.click(".dzw-tb-table tbody tr >> nth=0"); await p.waitForTimeout(300);
    assert.ok(p.url().includes("/fiche?id="), "ligne ouvre sa fiche");
    await p.goBack(); await p.waitForSelector(".dzw-tb-table");
    await p.setViewportSize({ width: 390, height: 800 }); await p.waitForTimeout(400);
    assert.ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), "pas de débordement sur mobile");
    assert.deepStrictEqual(errs, []); await p.close(); srv.close(); ok.push("tableau de bord");
  }
  console.log("widgets ok :", ok.join(", "));
} finally {
  await browser.close();
  fs.rmSync(tmp, { force: true });
}
