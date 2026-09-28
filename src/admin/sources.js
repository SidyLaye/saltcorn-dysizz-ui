/* dysizz-ui — page d'admin des sources de données (/dysizz-ui/sources)
   Liste, création, modification, essai en direct et suppression.
   Réservée aux administrateurs ; chaque enregistrement est validé (champs
   vérifiés contre la table) avant d'être écrit. */
"use strict";
const { isAdmin, esc, denied, post } = require("../core");
const D = require("../donnees");

const EXEMPLES = {
  "Chiffre clé (avec comparaison)": { table: "lead", type: "agregat", mesures: { total: { fn: "count" }, ia: { fn: "count", si: { statut: "extrait_ia" } } }, filtres: { cree_le: "periode", source: "egal" }, comparer: true },
  "Courbe par jour": { table: "lead", type: "serie", groupe: { champ: "cree_le", par: "jour" }, mesures: { leads: { fn: "count" } }, filtres: { cree_le: "periode" } },
  "Barres par catégorie": { table: "lead", type: "agregat", groupe: "source", mesures: { leads: { fn: "count" } }, filtres: { cree_le: "periode" }, limite: 12 },
  "Liste paginée": { table: "lead", type: "liste", champs: ["id", "cree_le", "source", "statut"], tris: ["cree_le", "source"], tri: "cree_le", sens: "desc", par_page: 50, filtres: { q: { mode: "cherche", champs: ["reference_bien"] }, source: "egal", cree_le: "periode" }, enfants: { nom: { table: "lead_champ", ref: "lead", champ: "valeur", si: { nom_champ: "nom" } } } },
};

const page = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const t = await D.ensureTable();
  const rows = await t.getRows({}, { orderBy: "nom" });
  const edit = req.query && req.query.edit ? rows.find((r) => String(r.id) === String(req.query.edit)) : null;
  const nouveau = req.query && req.query.nouveau !== undefined;
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const msg = req.query && (req.query.ok || req.query.err);
  const form = edit || nouveau ? formulaire(edit || { nom: "", description: "", definition: JSON.stringify(EXEMPLES["Chiffre clé (avec comparaison)"], null, 2), role_min: 1, cache_s: 30 }, csrf, req.query.err) : "";
  res.sendWrap(
    { title: "Sources de données", requestFluidLayout: true },
    {
      above: [{
        type: "blank",
        contents: `<div class="dz-container" style="padding:1rem 0 4rem;max-width:1100px">
<a href="/dysizz" class="small">← Accueil Dysizz</a>
<h1 class="dz-h2" style="margin:.4rem 0">Sources de données</h1>
<p class="dz-lead">Chiffres, courbes et listes calculés par la base, jamais dans le navigateur. Une page les lit avec le bloc « Tableau de bord » ou à l'adresse <code>/dysizz/donnees/&lt;nom&gt;</code>.</p>
${msg ? `<div class="dz-alert ${req.query.err ? "dz-alert-danger" : "dz-alert-success"}" style="margin:1rem 0">${esc(msg)}</div>` : ""}
${form}
<div style="display:flex;justify-content:space-between;align-items:center;margin:1.5rem 0 .6rem"><h2 class="dz-h4" style="margin:0">${rows.length} source${rows.length > 1 ? "s" : ""}</h2><a class="dz-btn dz-btn-primary" href="/dysizz-ui/sources?nouveau">Nouvelle source</a></div>
<div class="dz-card" style="padding:0;overflow:auto"><table class="table" style="margin:0"><thead><tr><th>Nom</th><th>Table</th><th>Type</th><th>Rôle</th><th>Cache</th><th></th></tr></thead><tbody>
${rows.map((r) => { let d = {}; try { d = JSON.parse(r.definition || "{}"); } catch (e) {} return `<tr><td><b>${esc(r.nom)}</b><div class="small" style="opacity:.7">${esc(r.description || "")}</div></td><td>${esc(d.table || "?")}</td><td>${esc(d.type || "agregat")}</td><td>${esc(r.role_min ?? 1)}</td><td>${esc(r.cache_s ?? 30)} s</td><td style="white-space:nowrap"><a href="/dysizz/donnees/${esc(r.nom)}" target="_blank">JSON</a> · <a href="/dysizz-ui/sources?edit=${r.id}">modifier</a></td></tr>`; }).join("") || `<tr><td colspan="6" style="opacity:.7">Aucune source. Commence par « Nouvelle source ».</td></tr>`}
</tbody></table></div>
<details style="margin-top:1.5rem"><summary><b>Aide : écrire une définition</b></summary><div class="small" style="line-height:1.6;margin-top:.6rem">
<p><b>type</b> : <code>agregat</code> (chiffres, éventuellement par catégorie avec <code>groupe</code>), <code>serie</code> (par heure, jour, semaine, mois, année), <code>liste</code> (lignes paginées et triables).</p>
<p><b>mesures</b> : <code>count</code>, <code>countunique</code>, <code>sum</code>, <code>avg</code>, <code>min</code>, <code>max</code>, <code>mediane</code> (avec <code>champ</code>), <code>duree_moyenne</code> / <code>duree_mediane</code> en minutes (avec <code>de</code> et <code>a</code>, deux dates). Chaque mesure peut avoir sa condition <code>si</code> : <code>{"statut": "rejete"}</code>, <code>{"statut": ["a","b"]}</code>, <code>{"prix": {"gt": 100000}}</code>, <code>{"statut": {"non": "rejete"}}</code>, <code>{"champ": null}</code>.</p>
<p><b>filtres</b> (paramètres acceptés dans l'adresse) : <code>egal</code> (<code>?source=seloger</code> ou <code>?source=a,b</code>), <code>periode</code> (<code>?periode=aujourdhui|7j|30j|90j|12m</code> ou <code>?du=2026-09-01&amp;au=2026-09-30</code>), <code>vide</code> (<code>?x=oui|non</code>), <code>cherche</code> (<code>?q=texte</code> sur les champs listés), <code>min</code> / <code>max</code> (<code>{\"mode\":\"min\",\"champ\":\"prix\"}</code>), <code>commence</code>, <code>choix</code> (<code>{\"mode\":\"choix\",\"options\":{\"0\":{\"bien\":null}}}</code>), période glissante <code>?j=7</code>. Un paramètre non déclaré est ignoré.</p>
<p><b>fixe</b> : conditions toujours appliquées. <b>comparer</b> : ajoute les mêmes chiffres sur la période précédente. <b>limite</b> : nombre de catégories.</p>
<p><b>liste</b> : <code>champs</code>, <code>tris</code> (tris autorisés, <code>?tri=…&amp;sens=asc|desc</code>), <code>par_page</code> (≤ 200, <code>?page=2</code>), <code>enfants</code> : valeur d'une table liée (<code>dernier</code>, <code>premier</code>, <code>count</code>, <code>sum</code>, <code>min</code>, <code>max</code>).</p>
<p>Le lecteur doit avoir un rôle suffisant pour la source <i>et</i> pour chaque table lue. Requête en lecture seule, arrêtée au bout de 5 secondes.</p>
</div></details>
</div>`,
      }],
    }
  );
};

const formulaire = (r, csrf, err) => `<form method="post" action="/dysizz-ui/sources/save" class="dz-card" style="padding:1.2rem;margin:1rem 0">
<input type="hidden" name="_csrf" value="${esc(csrf)}"><input type="hidden" name="id" value="${esc(r.id || "")}">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.8rem">
<label>Nom <input name="nom" class="form-control" required pattern="[a-z0-9][a-z0-9_-]{0,60}" value="${esc(r.nom)}" placeholder="leads-par-jour"></label>
<label>Description <input name="description" class="form-control" value="${esc(r.description || "")}"></label>
<label>Rôle minimal <select name="role_min" class="form-control">${[[1, "admin"], [40, "staff"], [80, "user"], [100, "public"]].map(([v, l]) => `<option value="${v}"${+(r.role_min ?? 1) === v ? " selected" : ""}>${v} · ${l}</option>`).join("")}</select></label>
<label>Cache (secondes) <input name="cache_s" type="number" min="0" max="3600" class="form-control" value="${esc(r.cache_s ?? 30)}"></label>
</div>
<label style="display:block;margin-top:.8rem">Définition (JSON)
<textarea name="definition" class="form-control" rows="14" style="font-family:ui-monospace,Menlo,monospace;font-size:.85rem" spellcheck="false">${esc(r.definition || "")}</textarea></label>
<div class="small" style="margin:.4rem 0 .8rem">Exemples : ${Object.keys(EXEMPLES).map((k) => `<a href="#" data-ex="${esc(JSON.stringify(EXEMPLES[k], null, 2))}" onclick="this.form.definition.value=this.dataset.ex;return false">${esc(k)}</a>`).join(" · ")}</div>
<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center">
<button class="dz-btn dz-btn-primary" type="submit">Enregistrer</button>
<button class="dz-btn" type="submit" formaction="/dysizz-ui/sources/tester" formtarget="_blank">Essayer</button>
<input name="essai" class="form-control" style="max-width:320px" placeholder="paramètres d'essai : periode=30j&amp;source=seloger">
${r.id ? `<button class="dz-btn dz-btn-danger" type="submit" formaction="/dysizz-ui/sources/delete" onclick="return confirm('Supprimer cette source ? Les pages qui la lisent afficheront une erreur.')" style="margin-left:auto">Supprimer</button>` : ""}
<a href="/dysizz-ui/sources">Annuler</a></div></form>`;

const lireForm = (req) => {
  const b = post(req);
  let def;
  try { def = JSON.parse(String(b.definition || "")); } catch (e) { return { err: "JSON illisible : " + e.message }; }
  const { err } = D.valider(def);
  if (err.length) return { err: err.join(" · ") };
  const nom = String(b.nom || "").trim();
  if (!D.NOM_RE.test(nom)) return { err: "nom invalide (minuscules, chiffres, - et _)" };
  const role_min = [1, 40, 80, 100].includes(+b.role_min) ? +b.role_min : 1;
  const cache_s = Math.min(Math.max(Math.round(+b.cache_s || 0), 0), 3600);
  return { row: { nom, description: String(b.description || "").slice(0, 300), definition: JSON.stringify(def, null, 2), role_min, cache_s }, def };
};

const save = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const t = await D.ensureTable();
  const id = +post(req).id || null;
  const { err, row } = lireForm(req);
  const back = id ? `edit=${id}` : "nouveau";
  if (err) return res.redirect(`/dysizz-ui/sources?${back}&err=${encodeURIComponent(err)}`);
  /* nom unique : vérifié en base, pas dans un cache */
  const autre = await t.getRow({ nom: row.nom });
  if (autre && autre.id !== id) return res.redirect(`/dysizz-ui/sources?${back}&err=${encodeURIComponent("ce nom est déjà pris")}`);
  if (id) await t.updateRow(row, id); else await t.insertRow(row);
  D.cacheVider();
  res.redirect(`/dysizz-ui/sources?ok=${encodeURIComponent("Source « " + row.nom + " » enregistrée.")}`);
};

const tester = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const { err, def } = lireForm(req);
  res.setHeader("Cache-Control", "no-store");
  if (err) return res.status(400).json({ erreur: err });
  try {
    const { plan } = D.valider(def);
    const query = Object.fromEntries(new URLSearchParams(String(post(req).essai || "")));
    const t0 = Date.now();
    const r = await D.executer(plan, query, req.user);
    r.ms = Date.now() - t0;
    res.json(r);
  } catch (e) { res.status(500).json({ erreur: String(e.message || e) }); }
};

const del = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const t = await D.ensureTable();
  const id = +post(req).id;
  if (id) await t.deleteRows({ id });
  D.cacheVider();
  res.redirect(`/dysizz-ui/sources?ok=${encodeURIComponent("Source supprimée.")}`);
};

module.exports = { page, save, tester, del };
