/* dysizz-modules — outils communs aux vues maison (indicateurs, tableau, répartition, à venir) */
"use strict";
const { esc } = require("../core");

/* JSON écrit à la main dans la configuration d'une vue : erreur lisible plutôt qu'un plantage */
const parseJSON = (s, fallback) => {
  if (s && typeof s === "object") return s;
  try { return JSON.parse(String(s || "").trim() || "null") ?? fallback; } catch (e) { return { __error: e.message }; }
};

const day = (d, n = 0) => { const x = new Date(d); x.setHours(0, 0, 0, 0); x.setDate(x.getDate() + n); return x; };

/* période nommée → condition Saltcorn sur un champ date */
const periodWhere = (field, range, now = new Date()) => {
  if (!field || !range) return {};
  const t0 = day(now);
  const r = {
    today: { gt: t0, lt: day(now, 1), equal: true },
    past: { lt: t0 },
    overdue: { lt: t0 },
    week: { gt: t0, lt: day(now, 7), equal: true },
    next7: { gt: t0, lt: day(now, 7), equal: true },
    next30: { gt: t0, lt: day(now, 30), equal: true },
    last7: { gt: day(now, -7), lt: day(now, 1) },
    last30: { gt: day(now, -30), lt: day(now, 1) },
    month: { gt: new Date(now.getFullYear(), now.getMonth(), 1), lt: new Date(now.getFullYear(), now.getMonth() + 1, 1), equal: true },
    last_month: { gt: new Date(now.getFullYear(), now.getMonth() - 1, 1), lt: new Date(now.getFullYear(), now.getMonth(), 1), equal: true },
    year: { gt: new Date(now.getFullYear(), 0, 1), lt: new Date(now.getFullYear() + 1, 0, 1), equal: true },
  }[range];
  return r ? { [field]: r } : {};
};

/* fusion de conditions (and) */
const andWhere = (...ws) => {
  const out = {};
  for (const w of ws) for (const [k, v] of Object.entries(w || {})) {
    if (k in out) out.and = [...(out.and || []), { [k]: v }];
    else out[k] = v;
  }
  return out;
};

/* l'état de la page (?domaine=Maison…) filtre aussi nos vues, comme les vues natives */
const stateWhere = (table, state) => {
  const out = {};
  if (!state) return out;
  const fields = table.getFields();
  for (const f of fields) {
    const v = state[f.name];
    if (v === undefined || v === "" || f.name === "id") continue;
    if (f.type && f.type.name === "Bool") out[f.name] = v === true || v === "on" || v === "true";
    else if (f.is_fkey || (f.type && ["Integer", "Float"].includes(f.type.name))) out[f.name] = +v;
    else out[f.name] = String(v);
  }
  return out;
};

const canRead = (table, user) => table && (user ? user.role_id : 100) <= table.min_role_read;
const canWrite = (table, user) => table && (user ? user.role_id : 100) <= table.min_role_write;

const nf = (v, fmt) => {
  const n = Number(v || 0);
  switch (fmt) {
    case "eur": { const d = Math.abs(n) >= 100 || Number.isInteger(n) ? 0 : 2; return n.toLocaleString("fr-FR", { style: "currency", currency: "EUR", minimumFractionDigits: d, maximumFractionDigits: d }); }
    case "xof": return n.toLocaleString("fr-FR", { maximumFractionDigits: 0 }) + " FCFA";
    case "dec": return n.toLocaleString("fr-FR", { maximumFractionDigits: 1 });
    case "pct": return Math.round(n) + " %";
    default: return Math.round(n).toLocaleString("fr-FR");
  }
};

const dayLabel = (d, now = new Date()) => {
  const diff = Math.round((day(d) - day(now)) / 864e5);
  if (diff === 0) return "Aujourd'hui";
  if (diff === 1) return "Demain";
  if (diff === -1) return "Hier";
  if (diff < 0) return `En retard · ${new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "short" })}`;
  if (diff < 7) return new Date(d).toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "short" });
  return new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "long" });
};
const shortDate = (d) => (d ? new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "short" }) : "");
const hasTime = (d) => d && (new Date(d).getHours() || new Date(d).getMinutes());
const timeOf = (d) => new Date(d).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });

/* « projet.nom » → jointure Saltcorn */
const joinSpec = (table, paths) => {
  const joinFields = {};
  for (const p of paths) {
    const [k, target] = p.split(".");
    if (!target) continue;
    const f = table.getFields().find((x) => x.name === k);
    if (f && f.is_fkey) joinFields[`${k}_${target}`] = { ref: k, target };
  }
  return joinFields;
};
const pick = (row, path) => (path.includes(".") ? row[path.replace(".", "_")] : row[path]);

const errorBox = (msg) => `<div class="dzv-error"><i class="fas fa-exclamation-triangle"></i> ${esc(msg)}</div>`;

module.exports = { parseJSON, periodWhere, andWhere, stateWhere, canRead, canWrite, nf, dayLabel, shortDate, hasTime, timeOf, joinSpec, pick, errorBox, day };
