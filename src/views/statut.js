/* Vue « DZ Statut » : l'état de tes services en un coup d'œil (sites,
   serveurs, API, sauvegardes…) — bandeau général + une tuile par ligne. */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, stateWhere, canRead, errorBox } = require("./q");
const { configWorkflow, code, str } = require("./common");

const tone = (v) => {
  if (v === true) return "ok";
  if (v === false) return "danger";
  const s = String(v == null ? "" : v).toLowerCase();
  if (!s) return "mute";
  if (/^(ok|up|en ligne|actif|réussi|fait|valide)$/.test(s)) return "ok";
  if (/(lent|warn|attention|dégradé|bientôt|expire)/.test(s)) return "warn";
  if (/(panne|down|err|ko|échec|fail|hors|expiré|critique)/.test(s)) return "danger";
  return "mute";
};
const ICON = { ok: "fas fa-check-circle", warn: "fas fa-exclamation-circle", danger: "fas fa-times-circle", mute: "far fa-question-circle" };
const since = (d) => {
  if (!d) return "";
  const s = Math.round((Date.now() - new Date(d)) / 1000);
  if (s < 60) return "à l'instant";
  if (s < 3600) return `il y a ${Math.round(s / 60)} min`;
  if (s < 86400) return `il y a ${Math.round(s / 3600)} h`;
  return new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
};

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const names = table.getFields().map((f) => f.name);
  for (const k of ["champ_nom", "champ_etat"]) if (!names.includes(cfg[k])) return errorBox(`Choisis le ${k === "champ_nom" ? "champ nom" : "champ état"} (Réglages de la vue)`);
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const rows = await table.getRows(andWhere(where0, stateWhere(table, state)), { orderBy: cfg.champ_nom, limit: 500 });
  if (!rows.length) return `<div class="dzv-empty"><i class="fas fa-server"></i><p>${esc(cfg.texte_vide || "Rien à surveiller pour l'instant")}</p></div>`;
  const items = rows.map((r) => ({ r, t: tone(r[cfg.champ_etat]) }));
  const order = { danger: 0, warn: 1, mute: 2, ok: 3 };
  items.sort((a, b) => order[a.t] - order[b.t]);
  const n = (t) => items.filter((x) => x.t === t).length;
  const bad = n("danger"), warn = n("warn");
  const banner = bad ? { t: "danger", txt: `${bad} en panne` } : warn ? { t: "warn", txt: `${warn} à surveiller` } : { t: "ok", txt: cfg.texte_ok || "Tout fonctionne" };
  const edit = cfg.vue ? (r) => `javascript:ajax_modal('/view/${encodeURIComponent(cfg.vue)}?id=${r.id}')` : null;
  const sub = [bad && `${bad} panne`, warn && `${warn} attention`, n("ok") && `${n("ok")} ok`].filter(Boolean).join(" · ");
  return `<div class="dzv-status">
<div class="dzv-status-banner t-${banner.t}"><i class="${ICON[banner.t]}"></i><b>${esc(banner.txt)}</b><small>${esc(sub)}</small></div>
<div class="dzv-status-grid">${items.map(({ r, t }) => {
    const det = cfg.champ_detail ? r[cfg.champ_detail] : "";
    const when = cfg.champ_date ? since(r[cfg.champ_date]) : "";
    const inner = `<span class="dzv-status-ic"><i class="${ICON[t]}"></i></span><span class="dzv-status-txt"><b>${esc(r[cfg.champ_nom])}</b>
<small>${esc(r[cfg.champ_etat] == null ? "inconnu" : String(r[cfg.champ_etat]))}${det !== "" && det != null ? ` · ${esc(det)}${cfg.unite ? " " + esc(cfg.unite) : ""}` : ""}${when ? ` · ${esc(when)}` : ""}</small></span>`;
    return edit ? `<a class="dzv-status-tile t-${t}" href="${edit(r)}">${inner}</a>` : `<div class="dzv-status-tile t-${t}">${inner}</div>`;
  }).join("")}</div></div>`;
};

module.exports = {
  name: "DZ Statut",
  description: "État de tes services en un coup d'œil : bandeau général + une tuile par ligne (ok, attention, panne)",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("champ_nom", "Champ nom", "Ex. : url, nom"),
    str("champ_etat", "Champ état", "ok / lent / panne, ou un booléen"),
    str("champ_detail", "Champ détail (facultatif)", "Ex. : ms"),
    str("unite", "Unité du détail (facultatif)", "Ex. : ms"),
    str("champ_date", "Champ « vérifié le » (facultatif)", "Ex. : verifie_le"),
    str("vue", "Vue de détail (facultatif)", ""),
    str("texte_ok", "Texte quand tout va bien", "Par défaut : Tout fonctionne"),
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"actif":true}'),
    str("texte_vide", "Texte quand il n'y a rien", ""),
  ]),
  run,
};
