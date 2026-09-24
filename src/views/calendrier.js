/* Vue « DZ Calendrier » : un mois en grille, les lignes placées à leur date
   (rendez-vous, échéances, paiements…). Navigation mois par mois, clic sur
   un élément = fenêtre de modification, clic sur un jour = ajout à cette date. */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, stateWhere, canRead, canWrite, hasTime, timeOf, errorBox } = require("./q");
const { configWorkflow, code, str } = require("./common");

const JOURS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."];
const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const COLOR = /^(#[0-9a-f]{3,8}|[a-z]{3,20})$/i;

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const fields = table.getFields().map((f) => f.name);
  if (!fields.includes(cfg.champ_date)) return errorBox("Choisis le champ date (Réglages de la vue)");
  if (!fields.includes(cfg.champ_titre)) return errorBox("Choisis le champ titre (Réglages de la vue)");
  const m = /^(\d{4})-(\d{2})$/.exec(String((state && state.dz_mois) || ""));
  const now = new Date();
  const first = m ? new Date(+m[1], +m[2] - 1, 1) : new Date(now.getFullYear(), now.getMonth(), 1);
  const start = new Date(first); start.setDate(1 - ((first.getDay() + 6) % 7));
  const end = new Date(start); end.setDate(start.getDate() + 42);
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const st = { ...(state || {}) }; delete st.dz_mois;
  const rows = await table.getRows(andWhere(where0, stateWhere(table, st), { [cfg.champ_date]: { gt: start, lt: end, equal: true } }), { orderBy: cfg.champ_date, limit: 1000 });
  const byDay = new Map();
  for (const r of rows) { if (!r[cfg.champ_date]) continue; const k = ymd(new Date(r[cfg.champ_date])); if (!byDay.has(k)) byDay.set(k, []); byDay.get(k).push(r); }
  const modal = (url) => `javascript:ajax_modal('${url}')`;
  const edit = cfg.vue ? (r) => modal(`/view/${encodeURIComponent(cfg.vue)}?id=${r.id}`) : null;
  const add = cfg.vue_ajout && canWrite(table, req.user) ? (d) => modal(`/view/${encodeURIComponent(cfg.vue_ajout)}?${encodeURIComponent(cfg.champ_date)}=${d}`) : null;
  const prev = new Date(first.getFullYear(), first.getMonth() - 1, 1), next = new Date(first.getFullYear(), first.getMonth() + 1, 1);
  const mk = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  const today = ymd(now);
  const max = +cfg.max_par_jour || 3;
  let cells = "";
  for (let i = 0; i < 42; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i);
    const k = ymd(d);
    const its = byDay.get(k) || [];
    const out = d.getMonth() !== first.getMonth();
    cells += `<div class="dzv-cal-day${out ? " out" : ""}${k === today ? " today" : ""}${its.length ? " has" : ""}">
<div class="dzv-cal-num">${add ? `<a href="${add(k)}" title="Ajouter le ${d.toLocaleDateString("fr-FR")}">${d.getDate()}<i class="fas fa-plus"></i></a>` : d.getDate()}</div>
${its.slice(0, max).map((r) => { const c = cfg.champ_couleur && COLOR.test(String(r[cfg.champ_couleur] || "")) ? r[cfg.champ_couleur] : ""; const t = hasTime(r[cfg.champ_date]) ? `<small>${timeOf(r[cfg.champ_date])}</small> ` : ""; const inner = `${t}${esc(r[cfg.champ_titre])}`; return edit ? `<a class="dzv-cal-ev" href="${edit(r)}"${c ? ` style="--ev:${esc(c)}"` : ""}>${inner}</a>` : `<span class="dzv-cal-ev"${c ? ` style="--ev:${esc(c)}"` : ""}>${inner}</span>`; }).join("")}
${its.length > max ? `<span class="dzv-cal-more">+${its.length - max}</span>` : ""}</div>`;
  }
  return `<div class="dzv-cal">
<div class="dzv-cal-head"><a class="dzv-cal-nav" href="?dz_mois=${mk(prev)}" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a>
<b>${esc(first.toLocaleDateString("fr-FR", { month: "long", year: "numeric" }))}</b>
<a class="dzv-cal-nav" href="?dz_mois=${mk(next)}" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a>
${m ? `<a class="dzv-cal-today" href="?">Aujourd'hui</a>` : ""}</div>
<div class="dzv-cal-grid">${JOURS.map((j) => `<div class="dzv-cal-wd">${j}</div>`).join("")}${cells}</div></div>`;
};

module.exports = {
  name: "DZ Calendrier",
  description: "Un mois en grille : les lignes à leur date, navigation, clic pour modifier ou ajouter",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("champ_date", "Champ date", "Ex. : date, echeance"),
    str("champ_titre", "Champ titre", "Ex. : titre, motif"),
    str("champ_couleur", "Champ couleur (facultatif)", "Une couleur (#hex ou nom) par ligne"),
    str("vue", "Vue de modification (facultatif)", "S'ouvre en fenêtre au clic"),
    str("vue_ajout", "Vue d'ajout (facultatif)", "S'ouvre au clic sur un jour, la date est pré-remplie"),
    { name: "max_par_jour", label: "Éléments visibles par jour", type: "Integer", default: 3 },
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"fait":false}'),
  ]),
  run,
};
