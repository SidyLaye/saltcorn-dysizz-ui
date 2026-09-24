/* Vue « DZ À venir » : une frise jour par jour qui rassemble plusieurs tables
   (tâches à rendre, rendez-vous, documents qui expirent, relances…). */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, canRead, dayLabel, hasTime, timeOf, errorBox, day } = require("./q");
const { configWorkflow, code, int } = require("./common");

const EXAMPLE = `[
  {"table":"taches","date":"echeance","titre":"titre","icon":"fas fa-check-circle",
   "where":{"not":{"statut":"fait"}},"vue":"tache_modifier","retard":true},
  {"table":"rdv_sante","date":"date","titre":"motif","icon":"fas fa-stethoscope",
   "where":{"fait":false},"vue":"rdv_modifier","tone":"info"}
]`;

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const sources = parseJSON(cfg.sources, []);
  if (sources.__error) return errorBox(`JSON des sources invalide : ${sources.__error}`);
  const days = +cfg.jours || 7;
  const t0 = day(new Date());
  const end = day(new Date(), days);
  const items = [];
  for (const s of sources) {
    const table = Table.findOne({ name: s.table });
    if (!table || !canRead(table, req.user)) continue;
    const range = s.retard ? { lt: end } : { gt: t0, lt: end, equal: true };
    const rows = await table.getRows(andWhere(s.where || {}, { [s.date]: range }), { orderBy: s.date, limit: 60 }).catch(() => []);
    for (const r of rows) {
      if (!r[s.date]) continue;
      const d = new Date(r[s.date]);
      const late = d < t0;
      /* une date passée compte pour aujourd'hui, marquée « en retard » */
      items.push({ when: late ? t0 : d, d, late, title: r[s.titre], sub: s.sous_titre ? r[s.sous_titre] : "", icon: s.icon || "fas fa-circle", tone: late ? "danger" : s.tone || "", url: s.vue ? `javascript:ajax_modal('/view/${encodeURIComponent(s.vue)}?id=${r.id}')` : "", label: s.libelle || "" });
    }
  }
  items.sort((a, b) => a.when - b.when || a.d - b.d);
  if (!items.length) return `<div class="dzv-empty"><i class="far fa-calendar-check"></i><p>${esc(cfg.texte_vide || "Rien de prévu. Profites-en.")}</p></div>`;
  const byDay = new Map();
  for (const it of items) { const k = +day(it.when); if (!byDay.has(k)) byDay.set(k, []); byDay.get(k).push(it); }
  return `<div class="dzv-agenda">${[...byDay.entries()].map(([k, its]) => `<div class="dzv-day">
<div class="dzv-day-label">${esc(dayLabel(new Date(k)))}</div>
<div class="dzv-day-items">${its.map((it) => {
    const inner = `<i class="${esc(it.icon)}"></i><span class="dzv-ag-title">${esc(it.title)}${it.sub ? `<small>${esc(it.sub)}</small>` : ""}</span>
<span class="dzv-ag-when">${it.late ? `en retard · ${esc(new Date(it.d).toLocaleDateString("fr-FR", { day: "numeric", month: "short" }))}` : hasTime(it.d) ? esc(timeOf(it.d)) : esc(it.label)}</span>`;
    return it.url ? `<a class="dzv-ag${it.tone ? " dzv-tone-" + esc(it.tone) : ""}" href="${esc(it.url)}">${inner}</a>` : `<div class="dzv-ag${it.tone ? " dzv-tone-" + esc(it.tone) : ""}">${inner}</div>`;
  }).join("")}</div></div>`).join("")}</div>`;
};

module.exports = {
  name: "DZ À venir",
  description: "Frise des prochains jours qui rassemble plusieurs tables (échéances, rendez-vous, expirations)",
  tableless: true,
  get_state_fields: () => [],
  display_state_form: false,
  configuration_workflow: configWorkflow([
    code("sources", "Sources (JSON)", "Exemple :<pre>" + esc(EXAMPLE) + "</pre>« retard »: true = montre aussi ce qui est passé (en rouge)."),
    int("jours", "Nombre de jours", "", 7),
    { name: "texte_vide", label: "Texte quand il n'y a rien", type: "String" },
  ]),
  run,
};
