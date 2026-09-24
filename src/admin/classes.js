/* dysizz-ui — classes : référence du kit + classes perso (table Saltcorn dz_classes)
   Les classes perso sont stockées dans une vraie table du tenant (visible dans
   Tables, sauvegardée avec le tenant), puis compilées en CSS dans la config du
   plugin : elles arrivent sur toutes les pages sans requête supplémentaire. */
"use strict";
const { isAdmin, esc, denied, post, pub } = require("../core");
const { patchCfg } = require("../pluginCfg");

const TABLE = "dz_classes";
const NAME_RE = /^[a-z][a-z0-9-]{1,40}$/;

const ensureTable = async () => {
  const Table = require("@saltcorn/data/models/table");
  const Field = require("@saltcorn/data/models/field");
  const { getState } = require("@saltcorn/data/db/state");
  let t = Table.findOne({ name: TABLE });
  if (t) return t;
  t = await Table.create(TABLE, { min_role_read: 1, min_role_write: 1, description: "Classes CSS perso du kit Dysizz UI — à gérer depuis /dysizz-ui/classes" });
  const fields = [
    { name: "name", label: "Nom de la classe", type: "String", required: true, is_unique: true },
    { name: "description", label: "Description", type: "String" },
    { name: "category", label: "Catégorie", type: "String" },
    { name: "css", label: "CSS", type: "String" },
    { name: "style_json", label: "Réglages de l'éditeur visuel", type: "String" },
  ];
  for (const f of fields) await Field.create({ table: t, table_id: t.id, ...f });
  if (getState().refresh_tables) await getState().refresh_tables();
  return Table.findOne({ name: TABLE }) || t;
};

const rowsOf = async () => {
  const Table = require("@saltcorn/data/models/table");
  const t = Table.findOne({ name: TABLE });
  return t ? await t.getRows({}, { orderBy: "name" }) : [];
};

const balanced = (css) => {
  let d = 0;
  for (const ch of css.replace(/"[^"]*"|'[^']*'/g, "")) {
    if (ch === "{") d++;
    if (ch === "}") d--;
    if (d < 0) return false;
  }
  return d === 0;
};

const compile = (rows) =>
  rows
    .filter((r) => NAME_RE.test(r.name) && r.css)
    .map((r) => `.${r.name}{${String(r.css).replace(/<\/?style/gi, "")}}`)
    .join("\n");

const publish = async () => patchCfg({ classes_css: compile(await rowsOf()) });

const page = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const rows = await rowsOf();
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const data = {
    csrf,
    idx: pub("classes-index.json"),
    docs: pub("classes-docs.json"),
    group: pub("classes-"),
    fam: pub("dz-f-"),
    mine: rows.map((r) => ({ id: r.id, name: r.name, description: r.description || "", category: r.category || "", css: r.css || "", style: r.style_json || "" })),
    tab: (req.query && req.query.tab) || "kit",
    edit: req.query && req.query.edit,
    ok: req.query && req.query.ok,
    err: req.query && req.query.err,
  };
  res.sendWrap(
    { title: "Classes", requestFluidLayout: true },
    {
      above: [
        {
          type: "blank",
          contents: `<div id="dzc-app" class="dz-container" style="padding:1rem 0 4rem"><a href="/dysizz-ui" class="small">← Kit de design</a>
<h1 class="dz-h2" style="margin:.4rem 0">Classes</h1>
<p class="dz-lead">Ce qu'il y a derrière chaque classe du kit, et tes propres classes. Pour utiliser une classe : dans le builder, sélectionne un conteneur ou un texte, champ <b>Custom class</b> (classe perso), tape son nom.</p>
<noscript>Cette page a besoin de JavaScript.</noscript></div>
<script type="application/json" id="dzc-data">${JSON.stringify(data).replace(/</g, "\\u003c")}</script>
<script src="${pub("dz-editor-classes.js")}" defer></script>`,
        },
      ],
    }
  );
};

const save = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const b = post(req);
  const name = String(b.name || "").trim().toLowerCase();
  const back = (q) => res.redirect("/dysizz-ui/classes?tab=mine&" + q);
  if (!NAME_RE.test(name)) return back("err=" + encodeURIComponent("Nom invalide : lettres minuscules, chiffres et tirets, 2 à 41 caractères, commence par une lettre."));
  if (name.startsWith("dz-")) return back("err=" + encodeURIComponent("Le préfixe dz- est réservé au kit. Essaie par exemple « ma-" + name.slice(3) + " »."));
  const css = String(b.css || "").slice(0, 20000);
  if (!balanced(css)) return back("err=" + encodeURIComponent("Le CSS a des accolades { } non fermées."));
  const t = await ensureTable();
  const row = { name, description: String(b.description || "").slice(0, 300), category: String(b.category || "").slice(0, 60), css, style_json: String(b.style_json || "").slice(0, 20000) };
  const existing = (await t.getRows({ name }))[0];
  const byId = b.id ? (await t.getRows({ id: +b.id }))[0] : null;
  if (existing && (!byId || existing.id !== byId.id)) return back("err=" + encodeURIComponent(`La classe « ${name} » existe déjà.`) + (byId ? "&edit=" + byId.id : ""));
  let id;
  if (byId) { await t.updateRow(row, byId.id); id = byId.id; } else id = await t.insertRow(row);
  await publish();
  back(`edit=${id}&ok=` + encodeURIComponent(`Classe « ${name} » enregistrée : elle est active sur toutes les pages du tenant.`));
};

const del = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const t = await ensureTable();
  await t.deleteRows({ id: +post(req).id });
  await publish();
  res.redirect("/dysizz-ui/classes?tab=mine&ok=" + encodeURIComponent("Classe supprimée."));
};

const exportCls = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const rows = await rowsOf();
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Content-Disposition", `attachment; filename="classes-${new Date().toISOString().slice(0, 10)}.json"`);
  res.send(JSON.stringify({ format: "dysizz-classes", version: 1, classes: rows.map(({ id, ...r }) => r) }, null, 2));
};

const importCls = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  let data;
  try { data = JSON.parse(post(req).json || ""); } catch (e) { return res.redirect("/dysizz-ui/classes?tab=mine&err=" + encodeURIComponent("JSON illisible.")); }
  const t = await ensureTable();
  let n = 0;
  for (const r of (data && data.classes) || []) {
    if (!r || !NAME_RE.test(r.name || "") || r.name.startsWith("dz-") || !balanced(String(r.css || ""))) continue;
    const row = { name: r.name, description: String(r.description || ""), category: String(r.category || ""), css: String(r.css || ""), style_json: String(r.style_json || "") };
    const ex = (await t.getRows({ name: r.name }))[0];
    if (ex) await t.updateRow(row, ex.id); else await t.insertRow(row);
    n++;
  }
  await publish();
  res.redirect("/dysizz-ui/classes?tab=mine&ok=" + encodeURIComponent(`${n} classe(s) importée(s).`));
};

/* noms de toutes les classes (kit + perso) pour l'autocomplétion de l'atelier */
const names = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const { EMBED } = require("../assets");
  const idx = EMBED["classes-index.json"] || {};
  const docs = (EMBED["classes-docs.json"] || {}).classes || {};
  const kit = [];
  for (const [g, v] of Object.entries(idx)) for (const n of v.names) kit.push([n, v.label, (docs[n] || [])[0] || ""]);
  res.json({ kit, mine: (await rowsOf()).map((r) => [r.name, r.category || "perso", r.description || ""]) });
};

module.exports = { classesPage: page, saveClass: save, deleteClass: del, exportClasses: exportCls, importClasses: importCls, classNames: names };
