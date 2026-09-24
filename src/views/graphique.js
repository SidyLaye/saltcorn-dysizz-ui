/* Vue « DZ Graphique » : l'évolution d'une valeur dans le temps (courbe,
   aire ou barres), une ou plusieurs séries. Le regroupement par heure / jour /
   semaine / mois est fait par la base (Postgres) : des millions de lignes ne
   remontent jamais jusqu'au navigateur. SVG maison, sans bibliothèque. */
"use strict";
const { esc } = require("../core");
const { parseJSON, periodWhere, andWhere, stateWhere, canRead, nf, errorBox } = require("./q");
const { configWorkflow, code, str } = require("./common");

const PAS = { heure: "hour", jour: "day", semaine: "week", mois: "month" };
const AGG = { somme: "sum", moyenne: "avg", max: "max", min: "min", compter: "count" };
const PALETTE = ["var(--dz-primary,#5b5bf0)", "#12b886", "#f59f00", "#e64980", "#228be6", "#7950f2", "#fa5252", "#15aabf"];

const trunc = (d, pas) => {
  const x = new Date(d);
  if (pas === "hour") x.setMinutes(0, 0, 0);
  else { x.setHours(0, 0, 0, 0); if (pas === "week") x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); if (pas === "month") x.setDate(1); }
  return +x;
};

/* [{t, serie, v}] regroupés */
const fetchSeries = async (table, cfg, where) => {
  const db = require("@saltcorn/data/db");
  const pas = PAS[cfg.pas] || "day";
  const agg = AGG[cfg.calcul] || (cfg.champ_valeur ? "sum" : "count");
  const fields = new Set(table.getFields().map((f) => f.name));
  for (const f of [cfg.champ_date, cfg.champ_valeur, cfg.champ_serie].filter(Boolean)) if (!fields.has(f)) throw new Error(`champ « ${f} » absent de la table`);
  if (!db.isSQLite) {
    const q = (n) => `"${db.sqlsanitize(n)}"`;
    const { where: w, values } = db.mkWhere(where);
    const val = agg === "count" ? "count(*)" : `${agg}(${q(cfg.champ_valeur)})`;
    const serie = cfg.champ_serie ? `, ${q(cfg.champ_serie)}::text as serie` : "";
    const sql = `select date_trunc('${pas}', ${q(cfg.champ_date)}) as t${serie}, ${val}::float as v from "${db.getTenantSchema()}".${q(table.name)} ${w} group by 1${serie ? ", 2" : ""} order by 1 limit 20000`;
    return (await db.query(sql, values)).rows.map((r) => ({ t: +new Date(r.t), serie: r.serie ?? "", v: Number(r.v || 0) }));
  }
  /* SQLite (développement) : regroupement ici, sur 50 000 lignes max */
  const rows = await table.getRows(where, { orderBy: cfg.champ_date, limit: 50000 });
  const m = new Map();
  for (const r of rows) {
    if (!r[cfg.champ_date]) continue;
    const k = `${trunc(r[cfg.champ_date], pas)}|${cfg.champ_serie ? r[cfg.champ_serie] ?? "" : ""}`;
    const a = m.get(k) || { n: 0, s: 0, max: -Infinity, min: Infinity };
    const v = Number(cfg.champ_valeur ? r[cfg.champ_valeur] : 1) || 0;
    a.n++; a.s += v; a.max = Math.max(a.max, v); a.min = Math.min(a.min, v);
    m.set(k, a);
  }
  return [...m.entries()].map(([k, a]) => {
    const [t, serie] = k.split("|");
    return { t: +t, serie, v: agg === "count" ? a.n : agg === "avg" ? a.s / a.n : agg === "max" ? a.max : agg === "min" ? a.min : a.s };
  }).sort((x, y) => x.t - y.t);
};

const fmtT = (t, pas) => {
  const d = new Date(t);
  if (pas === "hour") return d.toLocaleString("fr-FR", { day: "numeric", month: "short", hour: "2-digit" }).replace(/\s*h$/, "") + " h";
  if (pas === "month") return d.toLocaleDateString("fr-FR", { month: "short", year: "2-digit" });
  return d.toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
};

const svg = (series, cfg) => {
  const pas = PAS[cfg.pas] || "day";
  const W = 560, H = +cfg.hauteur || 240, L = 44, R = 12, T = 12, B = 28;
  const ts = [...new Set(series.flatMap((s) => s.points.map((p) => p.t)))].sort((a, b) => a - b);
  const all = series.flatMap((s) => s.points.map((p) => p.v));
  const lo = Math.min(0, ...all), hi = Math.max(...all, 1);
  const x = (t) => (ts.length < 2 ? L + (W - L - R) / 2 : L + ((ts.indexOf(t)) / (ts.length - 1)) * (W - L - R));
  const y = (v) => T + (1 - (v - lo) / (hi - lo || 1)) * (H - T - B);
  const fmt = cfg.format || "int";
  const grid = [0, 0.25, 0.5, 0.75, 1].map((k) => { const v = lo + (hi - lo) * k; return `<line x1="${L}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" class="dzv-g-grid"/><text x="${L - 6}" y="${(y(v) + 4).toFixed(1)}" class="dzv-g-ax" text-anchor="end">${esc(nf(v, fmt === "eur" ? "int" : fmt))}</text>`; }).join("");
  const step = Math.max(1, Math.ceil(ts.length / 5));
  const long = ts.length > 1 && ts[ts.length - 1] - ts[0] > 2 * 864e5;
  let nth = 0;
  const xl = ts.map((t, i) => ((i % step === 0 && ts.length - 1 - i >= step / 2) || i === ts.length - 1 ? `<text x="${x(t).toFixed(1)}" y="${H - 8}" class="dzv-g-ax${nth++ % 2 ? " dzv-g-x2" : ""}" text-anchor="${i === ts.length - 1 && ts.length > 1 ? "end" : i === 0 && ts.length > 1 ? "start" : "middle"}">${esc(pas === "hour" && long ? fmtT(t, "day") : fmtT(t, pas))}</text>` : "")).join("");
  const type = cfg.type || "courbe";
  const bw = Math.max(2, ((W - L - R) / Math.max(ts.length, 1)) * 0.8 / series.length);
  const body = series.map((s, si) => {
    const c = PALETTE[si % PALETTE.length];
    const tip = (p) => `<title>${esc(s.nom ? s.nom + " · " : "")}${esc(fmtT(p.t, pas))} : ${esc(nf(p.v, fmt))}</title>`;
    if (type === "barres") return s.points.map((p) => `<rect x="${(x(p.t) - (bw * series.length) / 2 + si * bw).toFixed(1)}" y="${Math.min(y(p.v), y(0)).toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.abs(y(0) - y(p.v)).toFixed(1)}" rx="2" style="fill:${c}">${tip(p)}</rect>`).join("");
    const d = s.points.map((p, i) => `${i ? "L" : "M"}${x(p.t).toFixed(1)},${y(p.v).toFixed(1)}`).join("");
    const area = type === "aire" && s.points.length > 1 ? `<path d="${d}L${x(s.points[s.points.length - 1].t).toFixed(1)},${y(lo).toFixed(1)}L${x(s.points[0].t).toFixed(1)},${y(lo).toFixed(1)}Z" style="fill:${c};opacity:.14"/>` : "";
    const dots = s.points.length <= 60 ? s.points.map((p) => `<circle cx="${x(p.t).toFixed(1)}" cy="${y(p.v).toFixed(1)}" r="3" style="fill:${c}">${tip(p)}</circle>`).join("") : "";
    return `${area}<path d="${d}" style="fill:none;stroke:${c}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>${dots}`;
  }).join("");
  const legend = series.length > 1 ? `<div class="dzv-g-legend">${series.map((s, i) => `<span><i style="background:${PALETTE[i % PALETTE.length]}"></i>${esc(s.nom || "—")}</span>`).join("")}</div>` : "";
  return `<svg class="dzv-g-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${esc(cfg.titre || "Graphique")}">${grid}${xl}${body}</svg>${legend}`;
};

const run = async (table_id, viewname, cfg, state, { req }) => {
  const Table = require("@saltcorn/data/models/table");
  const table = Table.findOne({ id: table_id });
  if (!canRead(table, req.user)) return errorBox("Accès refusé");
  if (!cfg.champ_date) return errorBox("Choisis le champ date (Réglages de la vue)");
  const where0 = parseJSON(cfg.filtre, {});
  if (where0.__error) return errorBox(`Filtre JSON invalide : ${where0.__error}`);
  const where = andWhere(where0, periodWhere(cfg.champ_date, cfg.periode || "last30"), stateWhere(table, state));
  let pts;
  try { pts = await fetchSeries(table, cfg, where); } catch (e) { return errorBox(e.message); }
  const byS = new Map();
  for (const p of pts) { if (!byS.has(p.serie)) byS.set(p.serie, []); byS.get(p.serie).push(p); }
  const series = [...byS.entries()].slice(0, 8).map(([nom, points]) => ({ nom, points }));
  const head = cfg.titre ? `<div class="dzv-g-head"><b>${esc(cfg.titre)}</b>${series.length === 1 && series[0].points.length ? `<span>${esc(nf(series[0].points[series[0].points.length - 1].v, cfg.format || "int"))}</span>` : ""}</div>` : "";
  if (!pts.length) return `<div class="dzv-graph">${head}<div class="dzv-empty"><i class="fas fa-chart-line"></i><p>${esc(cfg.texte_vide || "Pas encore de données sur cette période")}</p></div></div>`;
  return `<div class="dzv-graph">${head}${svg(series, cfg)}</div>`;
};

module.exports = {
  name: "DZ Graphique",
  description: "Évolution d'une valeur dans le temps : courbe, aire ou barres, par heure / jour / semaine / mois, une ou plusieurs séries",
  get_state_fields: async (table_id) => { const T = require("@saltcorn/data/models/table"); const t = T.findOne({ id: table_id }); return t ? t.getFields() : []; },
  display_state_form: false,
  configuration_workflow: configWorkflow([
    str("titre", "Titre (facultatif)", ""),
    str("champ_date", "Champ date", "Ex. : quand, date, cree_le"),
    str("champ_valeur", "Champ valeur (nombre)", "Vide = compter les lignes"),
    str("calcul", "Calcul", "", { attributes: { options: "somme,moyenne,max,min,compter" } }),
    str("champ_serie", "Une courbe par (champ, facultatif)", "Ex. : nom (pour dzf_mesures), categorie…"),
    str("periode", "Période", "", { attributes: { options: "last30,last7,today,month,last_month,year" } }),
    str("pas", "Regrouper par", "", { attributes: { options: "jour,heure,semaine,mois" } }),
    str("type", "Type", "", { attributes: { options: "courbe,aire,barres" } }),
    str("format", "Format des valeurs", "", { attributes: { options: "int,dec,eur,xof,pct" } }),
    { name: "hauteur", label: "Hauteur (px)", type: "Integer", default: 240 },
    code("filtre", "Filtre (JSON, facultatif)", 'Ex. : {"nom":"site.ms"}'),
    str("texte_vide", "Texte quand il n'y a rien", ""),
  ]),
  run,
};
