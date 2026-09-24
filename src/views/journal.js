/* Vue « DZ Journal » : un fil d'événements (logs, erreurs, historique,
   activité), groupé par jour, coloré par niveau, avec filtres par niveau et
   recherche instantanée côté navigateur. */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, stateWhere, canRead, timeOf, errorBox, day } = require("./q");
const { configWorkflow, code, str, int } = require("./common");

/* niveau → ton (ok, info, warn, danger), accepte booléens et mots courants */
const tone = (v) => {
  if (v === true) return "ok";
  if (v === false) return "danger";
  const s = String(v == null ? "" : v).toLowerCase();
  if (/^(ok|succès|success|réussi|fait|up|info?)$/.test(s)) return s.startsWith("info") ? "info" : "ok";
  if (/(warn|attention|lent|avert)/.test(s)) return "warn";
  if (/(err|panne|échec|fail|crit|fatal|down|ko)/.test(s)) return "danger";
  return "info";
};
const LABEL = { ok: "OK", info: "Info", warn: "Attention", danger: "Erreur" };

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const names = table.getFields().map((f) => f.name);
  for (const k of ["champ_date", "champ_message"]) if (!names.includes(cfg[k])) return errorBox(`Choisis le ${k === "champ_date" ? "champ date" : "champ message"} (Réglages de la vue)`);
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const since = +cfg.jours ? { [cfg.champ_date]: { gt: new Date(Date.now() - +cfg.jours * 864e5) } } : {};
  const rows = await table.getRows(andWhere(where0, since, stateWhere(table, state)), { orderBy: cfg.champ_date, orderDesc: true, limit: Math.min(+cfg.limite || 200, 2000) });
  if (!rows.length) return `<div class="dzv-empty"><i class="fas fa-stream"></i><p>${esc(cfg.texte_vide || "Rien à signaler")}</p></div>`;
  const counts = { ok: 0, info: 0, warn: 0, danger: 0 };
  const items = rows.map((r) => { const t = cfg.champ_niveau ? tone(r[cfg.champ_niveau]) : "info"; counts[t]++; return { r, t }; });
  const byDay = new Map();
  for (const it of items) { const k = +day(it.r[cfg.champ_date] || 0); if (!byDay.has(k)) byDay.set(k, []); byDay.get(k).push(it); }
  const edit = cfg.vue ? (r) => `javascript:ajax_modal('/view/${encodeURIComponent(cfg.vue)}?id=${r.id}')` : null;
  const today = +day(new Date());
  const dl = (k) => (k === today ? "Aujourd'hui" : k === today - 864e5 ? "Hier" : new Date(k).toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" }));
  const chips = cfg.champ_niveau ? `<div class="dzv-log-bar"><div class="dzv-log-chips">${["tout", "danger", "warn", "ok", "info"].filter((k) => k === "tout" || counts[k]).map((k) => `<button type="button" data-dzv-log="${k}" class="${k === "tout" ? "on" : ""}">${k === "tout" ? "Tout" : LABEL[k]} <small>${k === "tout" ? items.length : counts[k]}</small></button>`).join("")}</div>` : `<div class="dzv-log-bar">`;
  return `<div class="dzv-log" data-dzv-logs>${chips}<input type="search" class="form-control form-control-sm dzv-log-q" placeholder="Chercher…" data-dzv-log-q></div>
${[...byDay.entries()].map(([k, its]) => `<div class="dzv-log-day"><h4>${esc(dl(k))}</h4>${its.map(({ r, t }) => {
    const src = cfg.champ_source ? r[cfg.champ_source] : "";
    const det = cfg.champ_detail ? r[cfg.champ_detail] : "";
    const inner = `<span class="dzv-log-dot"></span><time>${r[cfg.champ_date] ? timeOf(r[cfg.champ_date]) : ""}</time>
<span class="dzv-log-main">${det !== "" && det != null ? `<small>${esc(typeof det === "object" ? JSON.stringify(det) : det)}${cfg.unite ? " " + esc(cfg.unite) : ""}</small>` : ""}${src ? `<code>${esc(src)}</code>` : ""}${esc(r[cfg.champ_message])}</span>`;
    return edit ? `<a class="dzv-log-row t-${t}" data-t="${t}" href="${edit(r)}">${inner}</a>` : `<div class="dzv-log-row t-${t}" data-t="${t}">${inner}</div>`;
  }).join("")}</div>`).join("")}</div>`;
};

module.exports = {
  name: "DZ Journal",
  description: "Fil d'événements par jour (logs, erreurs, historique), coloré par niveau, filtres et recherche",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("champ_date", "Champ date", "Ex. : quand"),
    str("champ_message", "Champ message", "Ex. : message, titre"),
    str("champ_niveau", "Champ niveau (facultatif)", "ok / info / attention / erreur, ou un booléen (vrai = ok)"),
    str("champ_source", "Champ source (facultatif)", "Ex. : bloc, service"),
    str("champ_detail", "Champ détail (facultatif)", "Affiché à droite. Ex. : duree_ms"),
    str("unite", "Unité du détail (facultatif)", "Ex. : ms"),
    str("vue", "Vue de détail (facultatif)", "S'ouvre en fenêtre au clic"),
    int("jours", "Sur les N derniers jours", "0 = tout", 7),
    int("limite", "Lignes max", "", 200),
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"ok":false}'),
    str("texte_vide", "Texte quand il n'y a rien", ""),
  ]),
  run,
};
