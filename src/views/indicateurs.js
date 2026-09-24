/* Vue « DZ Indicateurs » : une rangée de chiffres clés, chacun calculé sur
   n'importe quelle table (compte, somme, moyenne), avec filtre et période.
   Configuration : une liste JSON de tuiles (voir docs/VUES.md). */
"use strict";
const { esc } = require("../core");
const { parseJSON, periodWhere, andWhere, canRead, nf, errorBox } = require("./q");
const { configWorkflow, code, int } = require("./common");

const EXAMPLE = `[
  {"id":"retard","label":"En retard","icon":"fas fa-fire","table":"taches","stat":"count",
   "where":{"not":{"statut":"fait"}},"period":{"field":"echeance","range":"overdue"},
   "tone":"danger","href":"/page/taches"},
  {"id":"depense","label":"Dépensé ce mois","icon":"fas fa-wallet","table":"operations",
   "stat":"sum","field":"montant","where":{"type":"dépense"},
   "period":{"field":"date","range":"month"},"format":"eur"},
  {"label":"Reste","expr":"budget - depense","format":"eur","tone":"success"}
]`;

const STATS = { count: "Count", sum: "Sum", avg: "Avg", min: "Min", max: "Max" };

const computeTile = async (t, user, now) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ name: t.table });
  if (!table) return t.optional ? { skip: true } : { error: `table « ${t.table} » introuvable` };
  if (!canRead(table, user)) return { error: "accès refusé" };
  const where = andWhere(t.where || {}, t.period ? periodWhere(t.period.field, t.period.range, now) : {});
  const stat = (t.stat || "count").toLowerCase();
  if (stat === "count") return { value: await table.countRows(where) };
  if (!STATS[stat] || !t.field) return { error: "stat ou champ manquant" };
  const r = await table.aggregationQuery({ v: { field: t.field, aggregate: STATS[stat] } }, { where });
  return { value: Number((r && r.v) || 0) };
};

/* « budget - depense » : seulement des noms de tuiles, des nombres et + - * / ( ) */
const evalExpr = (expr, vals) => {
  if (!/^[\w\s+\-*/().]+$/.test(expr)) return NaN;
  const names = Object.keys(vals);
  try {
    // eslint-disable-next-line no-new-func
    return Number(new Function(...names, `return (${expr});`)(...names.map((n) => vals[n])));
  } catch (e) { return NaN; }
};

const run = async (table_id, viewname, cfg, state, { req }) => {
  const tiles = parseJSON(cfg.tuiles, []);
  if (tiles.__error) return errorBox(`JSON des tuiles invalide : ${tiles.__error}`);
  const now = new Date();
  const vals = {};
  const out = [];
  for (const t of tiles) {
    let r;
    if (t.expr) r = { value: evalExpr(t.expr, vals) };
    else if (t.value !== undefined) r = { value: Number(t.value) };
    else r = await computeTile(t, req.user, now).catch((e) => ({ error: e.message }));
    if (r.skip) continue;
    if (t.id && !r.error) vals[t.id] = r.value;
    if (!t.hidden) out.push({ t, r });
  }
  if (!out.length) return "";
  const cols = Math.max(1, Math.min(6, +cfg.colonnes || out.length || 1));
  return `<div class="dzv-kpis" style="--dzv-cols:${cols}">${out.map(({ t, r }) => {
    const tone = t.tone && !r.error ? ` dzv-tone-${esc(t.tone)}` : "";
    const zero = !r.error && !r.value ? " dzv-zero" : "";
    const inner = `<span class="dzv-kpi-top">${t.icon ? `<i class="${esc(t.icon)}"></i>` : ""}<span>${esc(t.label || "")}</span></span>
<span class="dzv-kpi-val">${r.error ? `<small class="dzv-err" title="${esc(r.error)}">—</small>` : esc(nf(r.value, t.format))}</span>
${t.sub ? `<span class="dzv-kpi-sub">${esc(t.sub)}</span>` : ""}`;
    return t.href ? `<a class="dzv-kpi${tone}${zero}" href="${esc(t.href)}">${inner}</a>` : `<div class="dzv-kpi${tone}${zero}">${inner}</div>`;
  }).join("")}</div>`;
};

module.exports = {
  name: "DZ Indicateurs",
  description: "Chiffres clés calculés sur tes tables (compte, somme, moyenne), avec période et lien",
  tableless: true,
  get_state_fields: () => [],
  display_state_form: false,
  configuration_workflow: configWorkflow([
    code("tuiles", "Tuiles (JSON)", "Une liste de tuiles. Exemple :<pre>" + esc(EXAMPLE) + "</pre>Périodes : today, overdue, next7, next30, last7, last30, month, last_month, year. Formats : eur, xof, dec, pct. Couleurs (tone) : primary, success, warning, danger, info."),
    int("colonnes", "Colonnes sur grand écran", "", 4),
  ], "Chaque tuile compte ou additionne les lignes d'une table. Une tuile avec « expr » calcule à partir des autres (par leur id)."),
  run,
  EXAMPLE,
};
