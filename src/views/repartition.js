/* Vue « DZ Répartition » : barres horizontales d'un total regroupé par un
   champ (ex. dépenses du mois par catégorie), avec un objectif facultatif
   lu dans la table liée (ex. le budget mensuel de la catégorie). */
"use strict";
const { esc } = require("../core");
const { parseJSON, periodWhere, andWhere, stateWhere, canRead, nf, errorBox } = require("./q");
const { configWorkflow, code, str } = require("./common");

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const gf = table.getFields().find((f) => f.name === cfg.champ_groupe);
  if (!gf) return errorBox("Choisis le champ de regroupement (Réglages de la vue)");
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const where = andWhere(where0, cfg.champ_date && cfg.periode ? periodWhere(cfg.champ_date, cfg.periode) : {}, stateWhere(table, state));
  const stat = cfg.champ_valeur ? "Sum" : "Count";
  const rows = await table.aggregationQuery({ v: { field: cfg.champ_valeur || "id", aggregate: stat } }, { where, groupBy: gf.name });
  const byKey = new Map((rows || []).map((r) => [String(r[gf.name]), Number(r.v || 0)]));

  /* libellés, couleurs et objectifs depuis la table liée */
  let groups = [];
  if (gf.is_fkey) {
    const ref = Table.findOne({ name: gf.reftable_name });
    const refRows = ref ? await ref.getRows(parseJSON(cfg.filtre_groupes, {}) || {}) : [];
    const label = cfg.champ_libelle || (gf.attributes && gf.attributes.summary_field) || "id";
    groups = refRows.map((r) => ({ key: String(r.id), label: r[label], target: cfg.champ_objectif ? Number(r[cfg.champ_objectif] || 0) : 0, color: cfg.champ_couleur ? r[cfg.champ_couleur] : null, icon: cfg.champ_icone ? r[cfg.champ_icone] : null }));
  } else {
    groups = [...byKey.keys()].map((k) => ({ key: k, label: k, target: 0 }));
  }
  for (const g of groups) g.value = byKey.get(g.key) || 0;
  groups = groups.filter((g) => g.value || g.target);
  if (!cfg.garder_ordre) groups.sort((a, b) => b.value - a.value);
  if (!groups.length) return `<div class="dzv-empty"><i class="far fa-chart-bar"></i><p>${esc(cfg.texte_vide || "Rien sur cette période")}</p></div>`;
  const max = Math.max(...groups.map((g) => Math.max(g.value, g.target)), 1);
  const total = groups.reduce((s, g) => s + g.value, 0);
  const fmt = cfg.format || "int";
  return `<div class="dzv-bars">${groups.map((g) => {
    const pct = (g.value / max) * 100;
    const over = g.target && g.value > g.target;
    const tpct = g.target ? (g.target / max) * 100 : 0;
    return `<div class="dzv-bar${over ? " dzv-over" : ""}">
<div class="dzv-bar-head"><span class="dzv-bar-label">${g.icon ? `<i class="${esc(g.icon)}"></i>` : ""}${esc(g.label)}</span>
<span class="dzv-bar-val">${esc(nf(g.value, fmt))}${g.target ? `<small> / ${esc(nf(g.target, fmt))}</small>` : ""}</span></div>
<div class="dzv-bar-track"><span style="width:${pct.toFixed(1)}%${g.color && /^#[0-9a-f]{3,8}$/i.test(g.color) ? `;background:${g.color}` : ""}"></span>${g.target ? `<i class="dzv-bar-target" style="left:${tpct.toFixed(1)}%"></i>` : ""}</div></div>`;
  }).join("")}<div class="dzv-bars-total">Total <b>${esc(nf(total, fmt))}</b></div></div>`;
};

module.exports = {
  name: "DZ Répartition",
  description: "Barres d'un total regroupé par un champ, avec objectif facultatif (ex. budget par catégorie)",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("champ_groupe", "Regrouper par (champ)", "Souvent une clé vers une autre table (ex. categorie)"),
    str("champ_valeur", "Additionner (champ nombre)", "Vide = compter les lignes"),
    str("champ_date", "Champ date (facultatif)", "Pour limiter à une période"),
    str("periode", "Période", "today, next7, last30, month, last_month, year…", { attributes: { options: ",today,last7,last30,month,last_month,year" } }),
    str("champ_libelle", "Libellé dans la table liée", "Ex. : nom"),
    str("champ_objectif", "Objectif dans la table liée (facultatif)", "Ex. : budget_mensuel"),
    str("champ_couleur", "Couleur dans la table liée (facultatif)", "Ex. : couleur"),
    str("champ_icone", "Icône dans la table liée (facultatif)", "Ex. : icone"),
    str("format", "Format", "", { attributes: { options: "int,eur,xof,dec" } }),
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"type":"dépense"}'),
    code("filtre_groupes", "Filtre des groupes (JSON, facultatif)", 'Ex. : {"type":"dépense"}'),
    str("texte_vide", "Texte quand il n'y a rien", ""),
    { name: "garder_ordre", label: "Garder l'ordre de la table liée", type: "Bool" },
  ]),
  run,
};
