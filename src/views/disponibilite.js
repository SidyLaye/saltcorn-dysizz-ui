/* Vue « DZ Disponibilité » : une ligne par service, une barre par jour
   (verte, orange, rouge selon le % de vérifications réussies), et le % global —
   comme les pages de statut des grands services. Calcul fait par la base. */
"use strict";
const { esc } = require("../core");
const { parseJSON, andWhere, stateWhere, canRead, errorBox } = require("./q");
const { configWorkflow, code, str, int } = require("./common");

const dayKey = (d) => { const x = new Date(d); return `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(x.getDate()).padStart(2, "0")}`; };

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const db = require("@saltcorn/data/db");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  const names = table.getFields().map((f) => f.name);
  for (const k of ["champ_date", "champ_ok", "champ_groupe"]) if (!names.includes(cfg[k])) return errorBox(`Choisis le champ « ${k.replace("champ_", "")} » (Réglages de la vue)`);
  const jours = Math.min(180, Math.max(7, +cfg.jours || 30));
  const since = new Date(); since.setHours(0, 0, 0, 0); since.setDate(since.getDate() - jours + 1);
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  /* groupes autorisés, lus dans une autre table (ex. sondes publiques) */
  let allowed = null;
  if (cfg.groupes_table) {
    const gt = Table.findOne({ name: cfg.groupes_table });
    if (gt) allowed = new Set((await gt.getRows(parseJSON(cfg.groupes_filtre, {}) || {})).map((r) => String(r[cfg.groupes_champ || "nom"])));
  }
  const where = andWhere(where0, { [cfg.champ_date]: { gt: since } }, stateWhere(table, state));
  let rows;
  if (!db.isSQLite) {
    const q = (n) => `"${db.sqlsanitize(n)}"`;
    const { where: w, values } = db.mkWhere(where);
    rows = (await db.query(`select ${q(cfg.champ_groupe)}::text as g, date_trunc('day', ${q(cfg.champ_date)}) as d, count(*)::int as n, sum(case when ${q(cfg.champ_ok)} then 1 else 0 end)::int as ok from "${db.getTenantSchema()}".${q(table.name)} ${w} group by 1, 2`, values)).rows;
  } else {
    const m = new Map();
    for (const r of await table.getRows(where, { limit: 200000 })) {
      const k = `${r[cfg.champ_groupe]}|${dayKey(r[cfg.champ_date])}`;
      const a = m.get(k) || { g: String(r[cfg.champ_groupe]), d: dayKey(r[cfg.champ_date]), n: 0, ok: 0 };
      a.n++; if (r[cfg.champ_ok]) a.ok++; m.set(k, a);
    }
    rows = [...m.values()];
  }
  const groups = new Map();
  for (const r of rows) {
    if (allowed && !allowed.has(String(r.g))) continue;
    if (!groups.has(r.g)) groups.set(r.g, new Map());
    groups.get(r.g).set(dayKey(r.d), r);
  }
  if (!groups.size) return `<div class="dzv-empty"><i class="fas fa-signal"></i><p>${esc(cfg.texte_vide || "Pas encore de données")}</p></div>`;
  const days = [...Array(jours)].map((_, i) => { const d = new Date(since); d.setDate(since.getDate() + i); return d; });
  const tone = (p) => (p === null ? "none" : p >= 99.5 ? "ok" : p >= 95 ? "warn" : "bad");
  const fmt = (p) => (p === null ? "—" : `${p.toLocaleString("fr-FR", { maximumFractionDigits: 2 })} %`);
  let totN = 0, totOk = 0;
  const lines = [...groups.entries()].sort((a, b) => String(a[0]).localeCompare(String(b[0]))).map(([g, m]) => {
    let n = 0, ok = 0;
    const bars = days.map((d) => {
      const r = m.get(dayKey(d));
      const p = r && r.n ? (100 * r.ok) / r.n : null;
      if (r) { n += r.n; ok += r.ok; }
      return `<i class="t-${tone(p)}" title="${esc(d.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short" }))} : ${esc(fmt(p))}${r ? ` (${r.n} vérif.)` : ""}"></i>`;
    }).join("");
    totN += n; totOk += ok;
    const p = n ? (100 * ok) / n : null;
    return `<div class="dzv-up-row"><div class="dzv-up-head"><b>${esc(g)}</b><span class="t-${tone(p)}">${esc(fmt(p))}</span></div><div class="dzv-up-bars" style="--n:${jours}">${bars}</div></div>`;
  });
  const gp = totN ? (100 * totOk) / totN : null;
  return `<div class="dzv-up">
${cfg.bandeau !== false ? `<div class="dzv-up-sum t-${tone(gp)}"><b>${gp === null ? "Pas de données" : gp >= 99.5 ? "Tous les services fonctionnent" : gp >= 95 ? "Quelques perturbations" : "Perturbations importantes"}</b><span>${esc(fmt(gp))} sur ${jours} jours</span></div>` : ""}
${lines.join("")}
<div class="dzv-up-axis"><span>il y a ${jours} jours</span><span>aujourd'hui</span></div></div>`;
};

module.exports = {
  name: "DZ Disponibilité",
  description: "Page de statut : une barre par jour et par service (vert, orange, rouge) avec le % de disponibilité",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("champ_date", "Champ date", "Ex. : quand"),
    str("champ_ok", "Champ « réussi » (oui / non)", "Ex. : ok"),
    str("champ_groupe", "Une ligne par (champ)", "Ex. : site"),
    int("jours", "Nombre de jours", "7 à 180", 30),
    str("groupes_table", "Limiter aux lignes d'une autre table (facultatif)", "Ex. : surveillance_sites"),
    str("groupes_champ", "… dont ce champ vaut le groupe", "Ex. : nom"),
    code("groupes_filtre", "… et qui passent ce filtre (JSON)", 'Ex. : {"publique":true}'),
    code("filtre", "Filtre (JSON, facultatif)", ""),
    str("texte_vide", "Texte quand il n'y a rien", ""),
  ]),
  run,
};
