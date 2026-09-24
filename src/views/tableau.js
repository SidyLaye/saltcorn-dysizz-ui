/* Vue « DZ Tableau » : un tableau en colonnes (kanban) sur n'importe quelle
   table. Les colonnes viennent des choix d'un champ (ex. statut). On glisse
   une carte d'une colonne à l'autre : le champ est mis à jour (et les
   déclencheurs de la table s'exécutent, comme pour une modification normale). */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, stateWhere, canRead, canWrite, joinSpec, pick, shortDate, errorBox, day } = require("./q");
const { configWorkflow, code, str, int, viewOptions } = require("./common");

const fieldsOf = (table_id) => {
  const Table = require("@saltcorn/data/models/table");
  const t = Table.findOne({ id: table_id });
  return t ? t.getFields() : [];
};

const badge = (field, v) => {
  if (v === null || v === undefined || v === "") return "";
  if (v instanceof Date || (field && field.type && field.type.name === "Date")) {
    const d = new Date(v);
    const late = d < day(new Date());
    const today = +day(d) === +day(new Date());
    return `<span class="dzv-meta${late ? " dzv-late" : today ? " dzv-today" : ""}"><i class="far fa-calendar"></i>${esc(shortDate(d))}</span>`;
  }
  if (typeof v === "boolean") return v ? `<span class="dzv-meta"><i class="fas fa-check"></i>${esc(field ? field.label : "")}</span>` : "";
  const cls = String(v).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-");
  return `<span class="dzv-meta dzv-v-${esc(cls)}">${esc(v)}</span>`;
};

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const fields = table.getFields();
  const gf = fields.find((f) => f.name === cfg.champ_colonnes);
  if (!gf) return errorBox("Choisis le champ qui donne les colonnes (Réglages de la vue)");
  let columns = String((gf.attributes && gf.attributes.options) || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (cfg.colonnes) columns = String(cfg.colonnes).split(",").map((s) => s.trim()).filter(Boolean);
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const meta = String(cfg.champs_infos || "").split(",").map((s) => s.trim()).filter(Boolean);
  const where = andWhere(where0, stateWhere(table, state));
  const rows = await table.getJoinedRows({ where, joinFields: joinSpec(table, meta), orderBy: cfg.tri || "id", orderDesc: false, limit: 1000 });
  const done = cfg.colonne_finie;
  const doneMax = +cfg.max_finies || 15;
  const writable = canWrite(table, req.user);
  const open = cfg.vue_fiche ? (id) => `ajax_modal('/view/${encodeURIComponent(cfg.vue_fiche)}?id=${id}')` : null;
  const create = cfg.vue_creation;
  const stateQs = Object.entries(state || {}).filter(([k]) => !k.startsWith("_") && k !== "id").map(([k, v]) => `&${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join("");
  const title = cfg.champ_titre || "id";

  const html = columns.map((col) => {
    let items = rows.filter((r) => String(r[gf.name] ?? "") === col);
    let more = 0;
    if (col === done && items.length > doneMax) { more = items.length - doneMax; items = items.slice(-doneMax).reverse(); }
    const cards = items.map((r) => `<div class="dzv-card${col === done ? " dzv-card-done" : ""}" data-id="${r.id}"${writable ? ' draggable="true"' : ""}${open ? ` onclick="${esc(open(r.id))}"` : ""} tabindex="0">
<div class="dzv-card-title">${esc(r[title])}</div>
<div class="dzv-card-meta">${meta.map((m) => badge(fields.find((f) => f.name === m), pick(r, m))).join("")}</div></div>`).join("");
    return `<section class="dzv-col" data-value="${esc(col)}">
<header class="dzv-col-head"><span class="dzv-col-name">${esc(col)}</span><span class="dzv-col-count">${items.length + more}</span>
${create ? `<a class="dzv-col-add" href="javascript:ajax_modal('/view/${encodeURIComponent(create)}?${encodeURIComponent(gf.name)}=${encodeURIComponent(col)}${esc(stateQs)}')" aria-label="Ajouter"><i class="fas fa-plus"></i></a>` : ""}</header>
<div class="dzv-col-body">${cards || '<div class="dzv-col-empty">Rien ici</div>'}${more ? `<div class="dzv-col-more">+ ${more} plus anciennes</div>` : ""}</div></section>`;
  }).join("");
  return `<div class="dzv-board" data-dzv-board="${esc(viewname)}"${writable ? "" : ' data-readonly="1"'}>${html}</div>`;
};

/* déplacement d'une carte (appelé par dzm.js) */
const move = async (table_id, viewname, cfg, body, { req, res }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canWrite(table, req.user)) return { json: { error: "Accès refusé" } };
  const gf = table.getFields().find((f) => f.name === cfg.champ_colonnes);
  const id = +body.id;
  const value = String(body.value || "");
  const allowed = String(cfg.colonnes || (gf.attributes && gf.attributes.options) || "").split(",").map((s) => s.trim());
  if (!id || !allowed.includes(value)) return { json: { error: "Valeur refusée" } };
  const r = await table.updateRow({ [gf.name]: value }, id, req.user);
  if (typeof r === "string") return { json: { error: r } };
  return { json: { success: "ok" } };
};

module.exports = {
  name: "DZ Tableau",
  description: "Tableau en colonnes (kanban) avec glisser-déposer, sur le champ de ton choix",
  get_state_fields: async (table_id) => fieldsOf(table_id),
  display_state_form: false,
  configuration_workflow: configWorkflow(async () => [
    str("champ_colonnes", "Champ des colonnes", "Un champ texte avec une liste de choix (ex. statut)"),
    str("colonnes", "Ordre des colonnes (facultatif)", "Ex. : à faire,en cours,en attente,fait. Vide = l'ordre des choix du champ"),
    str("champ_titre", "Champ du titre de carte", "Ex. : titre"),
    str("champs_infos", "Infos sous le titre", "Champs séparés par des virgules. Une date devient rouge si elle est passée. Ex. : echeance,priorite,projet.nom"),
    str("tri", "Trier par", "Ex. : echeance"),
    str("colonne_finie", "Colonne « terminé » (facultatif)", "On n'y montre que les dernières cartes"),
    int("max_finies", "Cartes montrées dans la colonne terminé", "", 15),
    str("vue_fiche", "Vue ouverte au clic sur une carte", "Souvent la vue de modification", { attributes: { options: await viewOptions() } }),
    str("vue_creation", "Vue pour ajouter depuis une colonne", "Le champ des colonnes est prérempli", { attributes: { options: await viewOptions() } }),
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"domaine":"Maison"}'),
  ]),
  run,
  routes: { move },
};
