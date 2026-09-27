/* dysizz-ui — sources de données : chiffres, courbes et listes calculés par la base.

   Une source (table dz_sources du tenant) décrit ce qu'on veut lire :
     { "table": "lead", "type": "agregat" | "serie" | "liste", … }
   Les pages la lisent en JSON : GET /dysizz/donnees/<nom>?<filtres>
   et le widget « tableau » l'affiche (chiffre clé, courbe, barres, liste).

   Pourquoi : un écran qui télécharge des tables entières pour compter dans le
   navigateur ralentit à mesure que les données grossissent. Ici la base ne
   renvoie que le résultat (quelques lignes), filtré, paginé et mis en cache.

   Sécurité :
     - seul un administrateur crée ou modifie une source ;
     - chaque nom de champ est vérifié contre la table (jamais collé tel quel) ;
     - toutes les valeurs venant de l'URL passent en paramètres SQL ;
     - seuls les filtres déclarés dans la source sont acceptés ;
     - lecteur : rôle ≤ rôle minimal de la source ET de chaque table lue,
       et propriété des lignes respectée hors administrateur ;
     - requête en lecture seule, arrêtée au bout de 5 s. */
"use strict";

const TABLE = "dz_sources";
const NOM_RE = /^[a-z0-9][a-z0-9_-]{0,60}$/;
const TYPES = ["agregat", "serie", "liste"];
const FNS = ["count", "countunique", "sum", "avg", "min", "max", "mediane", "duree_moyenne", "duree_mediane"];
const PAS = { heure: "hour", jour: "day", semaine: "week", mois: "month", annee: "year" };
const PERIODES = { aujourdhui: 0, "7j": 7, "30j": 30, "90j": 90, "12m": 365 };
const MAX_LIGNES = 500;
const TIMEOUT_MS = 5000;

/* ── stockage ──────────────────────────────────────────────────────────── */
const ensureTable = async () => {
  const Table = require("@saltcorn/data/models/table");
  const Field = require("@saltcorn/data/models/field");
  const { getState } = require("@saltcorn/data/db/state");
  let t = Table.findOne({ name: TABLE });
  if (t) return t;
  t = await Table.create(TABLE, { min_role_read: 1, min_role_write: 1, description: "Sources de données du kit Dysizz UI — à gérer depuis /dysizz-ui/sources" });
  const fields = [
    { name: "nom", label: "Nom", type: "String", required: true, is_unique: true },
    { name: "description", label: "Description", type: "String" },
    { name: "definition", label: "Définition (JSON)", type: "String" },
    { name: "role_min", label: "Rôle minimal", type: "Integer" },
    { name: "cache_s", label: "Cache (secondes)", type: "Integer" },
  ];
  for (const f of fields) await Field.create({ table: t, table_id: t.id, ...f });
  if (getState().refresh_tables) await getState().refresh_tables();
  return Table.findOne({ name: TABLE }) || t;
};

/* ── validation d'une définition ───────────────────────────────────────── */
const champOk = (table, nom) => typeof nom === "string" && !!table.fields.find((f) => f.name === nom);
const typeDe = (table, nom) => (table.fields.find((f) => f.name === nom) || {}).type;
const estDate = (table, nom) => { const t = typeDe(table, nom); return t && (t.name || t) === "Date"; };

/* conditions fixes { champ: valeur | [valeurs] | null | {gt,lt} } : champs vérifiés, valeurs scalaires */
const validerSi = (table, si, err, ou) => {
  if (si == null) return {};
  if (typeof si !== "object" || Array.isArray(si)) { err.push(`${ou} : « si » doit être un objet`); return {}; }
  const out = {};
  for (const [k, v] of Object.entries(si)) {
    if (!champOk(table, k)) { err.push(`${ou} : champ inconnu « ${k} » dans ${table.name}`); continue; }
    if (v === null || ["string", "number", "boolean"].includes(typeof v)) out[k] = v;
    else if (Array.isArray(v) && v.every((x) => ["string", "number"].includes(typeof x))) out[k] = { in: v };
    else if (typeof v === "object" && Object.keys(v).length === 1 && typeof v.vide === "boolean") out[k] = v.vide ? null : "__non_vide__";
    else if (typeof v === "object" && Object.keys(v).length === 1 && (typeof v.commence === "string" || typeof v.contient === "string")) {
      const t = String(v.commence ?? v.contient).replace(/[\\%_]/g, (c) => "\\" + c);
      out[k] = { ilike: v.commence !== undefined ? t + "%" : "%" + t + "%", fullMatch: true };
    } else if (typeof v === "object" && Object.keys(v).every((x) => ["gt", "lt", "non"].includes(x))) {
      if (v.non !== undefined) out[k] = { not: { in: [].concat(v.non) } };
      else out[k] = { ...(v.gt !== undefined ? { gt: v.gt } : {}), ...(v.lt !== undefined ? { lt: v.lt } : {}) };
    } else err.push(`${ou} : valeur non prise en charge pour « ${k} »`);
  }
  for (const [k, v] of Object.entries(out)) if (v === "__non_vide__") { delete out[k]; out.not = { ...(out.not || {}), [k]: null }; }
  return out;
};

const validerMesure = (table, nom, m, err) => {
  const ou = `mesure « ${nom} »`;
  if (!/^[a-z][a-z0-9_]{0,40}$/.test(nom)) err.push(`${ou} : nom invalide (minuscules, chiffres, _)`);
  if (!m || !FNS.includes(m.fn)) { err.push(`${ou} : fn doit être ${FNS.join(", ")}`); return null; }
  if (m.fn.startsWith("duree_")) {
    if (!champOk(table, m.de) || !champOk(table, m.a)) err.push(`${ou} : « de » et « a » doivent être deux champs date de ${table.name}`);
  } else if (m.fn !== "count" && !champOk(table, m.champ)) err.push(`${ou} : champ « ${m.champ} » inconnu dans ${table.name}`);
  return { fn: m.fn, champ: m.champ, de: m.de, a: m.a, si: validerSi(table, m.si, err, ou) };
};

const valider = (def) => {
  const Table = require("@saltcorn/data/models/table");
  const err = [];
  if (!def || typeof def !== "object") return { err: ["définition vide ou illisible"] };
  const table = Table.findOne({ name: def.table });
  if (!table || table.name === TABLE) return { err: [`table « ${def.table} » introuvable`] };
  const type = def.type || "agregat";
  if (!TYPES.includes(type)) err.push(`type doit être ${TYPES.join(", ")}`);
  const plan = { table: table.name, type, fixe: validerSi(table, def.fixe, err, "fixe"), filtres: {}, mesures: {} };

  for (const [param, f] of Object.entries(def.filtres || {})) {
    if (!/^[a-z][a-z0-9_]{0,40}$/.test(param)) { err.push(`filtre « ${param} » : nom invalide`); continue; }
    const spec = typeof f === "string" ? { mode: f, champ: param } : { champ: param, ...f };
    if (spec.mode === "cherche") {
      const champs = [].concat(spec.champs || []);
      if (!champs.every((c) => champOk(table, c))) err.push(`filtre « ${param} » : champs de recherche inconnus`);
      /* recherche aussi dans des tables liées : { table, ref, champ, si } */
      const enfants = [];
      for (const e of [].concat(spec.enfants || [])) {
        const ct = Table.findOne({ name: e && e.table });
        if (!ct || !champOk(ct, e.ref) || !champOk(ct, e.champ)) { err.push(`filtre « ${param} » : table liée ou champ inconnu`); continue; }
        enfants.push({ table: ct.name, ref: e.ref, champ: e.champ, si: validerSi(ct, e.si, err, `filtre « ${param} »`) });
      }
      if (!champs.length && !enfants.length) err.push(`filtre « ${param} » : aucun champ de recherche`);
      plan.filtres[param] = { mode: "cherche", champs, enfants };
    } else if (["egal", "periode", "vide"].includes(spec.mode)) {
      if (!champOk(table, spec.champ)) { err.push(`filtre « ${param} » : champ « ${spec.champ} » inconnu`); continue; }
      if (spec.mode === "periode" && !estDate(table, spec.champ)) err.push(`filtre « ${param} » : « ${spec.champ} » n'est pas une date`);
      plan.filtres[param] = { mode: spec.mode, champ: spec.champ };
    } else err.push(`filtre « ${param} » : mode doit être egal, periode, vide ou cherche`);
  }
  if (Object.values(plan.filtres).filter((f) => f.mode === "periode").length > 1) err.push("un seul filtre de période par source");

  if (type === "liste") {
    const champs = [].concat(def.champs || ["id"]);
    if (!champs.includes("id")) champs.unshift("id");
    for (const c of champs) if (!champOk(table, c)) err.push(`champ « ${c} » inconnu dans ${table.name}`);
    plan.champs = champs;
    const tris = [].concat(def.tris || [def.tri || "id"]);
    for (const c of tris) if (!champOk(table, c)) err.push(`tri « ${c} » inconnu`);
    plan.tris = tris;
    plan.tri = def.tri && tris.includes(def.tri) ? def.tri : tris[0];
    plan.sens = def.sens === "asc" ? "asc" : "desc";
    plan.par_page = Math.min(Math.max(+def.par_page || 50, 1), 200);
    plan.enfants = {};
    for (const [nom, e] of Object.entries(def.enfants || {})) {
      if (!/^[a-z][a-z0-9_]{0,40}$/.test(nom) || champOk(table, nom)) { err.push(`enfant « ${nom} » : nom invalide ou déjà pris par un champ`); continue; }
      const ct = Table.findOne({ name: e && e.table });
      if (!ct) { err.push(`enfant « ${nom} » : table « ${e && e.table} » introuvable`); continue; }
      if (!champOk(ct, e.ref)) { err.push(`enfant « ${nom} » : champ de lien « ${e.ref} » inconnu dans ${ct.name}`); continue; }
      const fn = e.fn || "dernier";
      if (!["dernier", "premier", "count", "sum", "min", "max"].includes(fn)) err.push(`enfant « ${nom} » : fn doit être dernier, premier, count, sum, min ou max`);
      if (fn !== "count" && !champOk(ct, e.champ)) err.push(`enfant « ${nom} » : champ « ${e.champ} » inconnu dans ${ct.name}`);
      plan.enfants[nom] = { table: ct.name, ref: e.ref, champ: e.champ, fn, si: validerSi(ct, e.si, err, `enfant « ${nom} »`) };
    }
  } else {
    const mesures = def.mesures || { total: { fn: "count" } };
    for (const [nom, m] of Object.entries(mesures)) { const v = validerMesure(table, nom, m, err); if (v) plan.mesures[nom] = v; }
    if (!Object.keys(plan.mesures).length) err.push("au moins une mesure");
    const g = def.groupe;
    if (type === "serie") {
      const gg = typeof g === "string" ? { champ: g, par: "jour" } : g || {};
      if (!champOk(table, gg.champ) || !estDate(table, gg.champ)) err.push("série : « groupe.champ » doit être un champ date");
      if (!PAS[gg.par || "jour"]) err.push(`série : « groupe.par » doit être ${Object.keys(PAS).join(", ")}`);
      plan.groupe = { champ: gg.champ, par: gg.par || "jour" };
    } else if (g) {
      const gg = typeof g === "string" ? { champ: g } : g;
      if (!champOk(table, gg.champ)) err.push(`groupe : champ « ${gg.champ} » inconnu`);
      plan.groupe = { champ: gg.champ, par: gg.par && PAS[gg.par] ? gg.par : null };
    }
    plan.limite = Math.min(Math.max(+def.limite || 50, 1), MAX_LIGNES);
    plan.comparer = !!def.comparer;
  }
  return { err, plan };
};

/* ── construction SQL ──────────────────────────────────────────────────── */
const q = (s) => `"${String(s).replace(/"/g, "")}"`;

/* compteur de paramètres partagé entre les morceaux d'une même requête */
const params = () => {
  const values = [];
  return { values, push: (v) => { values.push(v); return `$${values.length}`; } };
};
const whereSql = (obj, ph) => {
  if (!obj || !Object.keys(obj).length) return "";
  const { mkWhere } = require("@saltcorn/db-common/internal");
  const { where, values } = mkWhere(obj, false, ph.values.length);
  ph.values.push(...values);
  return where.replace(/^where /, "");
};

const fuseau = () => {
  const { getState } = require("@saltcorn/data/db/state");
  const tz = (getState().getConfig && getState().getConfig("timezone")) || "Europe/Paris";
  try { Intl.DateTimeFormat("fr-FR", { timeZone: tz }); return tz; } catch (e) { return "Europe/Paris"; }
};

const jourIso = (s) => (/^\d{4}-\d{2}-\d{2}$/.test(String(s || "")) && !isNaN(Date.parse(s)) ? s : null);
const plusJours = (iso, n) => { const d = new Date(iso + "T00:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
const aujourdhui = (tz) => new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());

/* période demandée → bornes [du, au[ en jours locaux */
const bornes = (query, tz) => {
  const du = jourIso(query.du), au = jourIso(query.au);
  if (du || au) return { du, au: au ? plusJours(au, 1) : null };
  const p = String(query.periode || "");
  if (p in PERIODES) { const auj = aujourdhui(tz); return { du: plusJours(auj, -PERIODES[p]), au: plusJours(auj, 1) }; }
  return null;
};

/* filtres de l'URL → objet where (seuls les filtres déclarés) */
const whereDe = (plan, query, tz, decalage) => {
  const where = { ...plan.fixe };
  let periode = null;
  for (const [param, f] of Object.entries(plan.filtres)) {
    if (f.mode === "periode") {
      const b = bornes(query, tz);
      if (!b) continue;
      periode = { ...b, champ: f.champ };
      let { du, au } = b;
      if (decalage && du && au) { const n = Math.round((Date.parse(au) - Date.parse(du)) / 864e5); au = du; du = plusJours(du, -n); }
      const cond = [];
      if (du) cond.push({ gt: `${du}T00:00:00`, equal: true });
      if (au) cond.push({ lt: `${au}T00:00:00` });
      /* bornes exprimées dans le fuseau du site */
      where[f.champ] = cond.map((c) => { const k = c.gt ? "gt" : "lt"; return { ...c, [k]: enUtc(c[k], tz) }; });
      continue;
    }
    const v = query[param];
    if (v === undefined || v === "") continue;
    if (f.mode === "egal") {
      const vals = String(v).split(",").map((x) => x.trim()).filter(Boolean).slice(0, 50);
      where[f.champ] = vals.length > 1 ? { in: vals } : vals[0];
    } else if (f.mode === "vide") {
      if (v === "oui") where[f.champ] = null;
      else if (v === "non") where.not = { ...(where.not || {}), [f.champ]: null };
    } else if (f.mode === "cherche") {
      /* % et _ sont du texte, pas des jokers */
      const t = String(v).slice(0, 100).replace(/[\\%_]/g, (c) => "\\" + c);
      const db = require("@saltcorn/data/db");
      where.or = [
        ...f.champs.map((c) => ({ [c]: { ilike: t } })),
        ...(f.enfants || []).map((e) => ({ id: { inSelect: { table: e.table, field: e.ref, tenant: db.getTenantSchema(), where: { ...e.si, [e.champ]: { ilike: t } } } } })),
      ];
    }
  }
  return { where, periode };
};

/* « 2026-09-01T00:00:00 » heure de Paris → instant UTC ISO */
const enUtc = (local, tz) => {
  const guess = new Date(local + "Z");
  const parts = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(guess);
  const g = Object.fromEntries(parts.map((p) => [p.type, p.value]));
  const vu = Date.UTC(+g.year, +g.month - 1, +g.day, +g.hour, +g.minute, +g.second);
  return new Date(guess.getTime() - (vu - guess.getTime())).toISOString();
};

const mesureSql = (m, ph) => {
  const filtre = m.si && Object.keys(m.si).length ? ` filter (where ${whereSql(m.si, ph)})` : "";
  switch (m.fn) {
    case "count": return `count(*)${filtre}`;
    case "countunique": return `count(distinct a.${q(m.champ)})${filtre}`;
    case "mediane": return `percentile_cont(0.5) within group (order by a.${q(m.champ)})${filtre}`;
    case "duree_moyenne": return `avg(extract(epoch from (a.${q(m.a)} - a.${q(m.de)})) / 60)${filtre}`;
    case "duree_mediane": return `percentile_cont(0.5) within group (order by extract(epoch from (a.${q(m.a)} - a.${q(m.de)})) / 60)${filtre}`;
    default: return `${m.fn}(a.${q(m.champ)})${filtre}`;
  }
};

const nombre = (v) => (v === null || v === undefined ? null : isNaN(+v) ? v : Math.round(+v * 100) / 100);

/* lecture seule, arrêtée au bout de TIMEOUT_MS. Client dédié : db.withTransaction
   ne fait pas passer db.query dans la transaction (vérifié sur 1.6.2). */
const lire = async (sql, values) => {
  const db = require("@saltcorn/data/db");
  const c = await db.getClient();
  try {
    await c.query("begin read only");
    await c.query(`set local statement_timeout = ${TIMEOUT_MS}`);
    const r = await c.query(sql, values);
    await c.query("commit");
    return r.rows;
  } catch (e) {
    await c.query("rollback").catch(() => {});
    throw e;
  } finally { c.release(); }
};

const executer = async (plan, query, user) => {
  const Table = require("@saltcorn/data/models/table");
  const db = require("@saltcorn/data/db");
  const schema = db.getTenantSchemaPrefix();
  const table = Table.findOne({ name: plan.table });
  const tz = fuseau();
  const ph = params();
  const { where, periode } = whereDe(plan, query, tz, false);
  /* rôle au-dessus du minimum de lecture : seulement ses propres lignes (propriété) */
  if (user.role_id > (table.min_role_read ?? 1)) {
    const r = table.updateWhereWithOwnership(where, user, true);
    if (r && r.notAuthorized) throw Object.assign(new Error("accès refusé"), { code: 403 });
  }
  const w = whereSql(where, ph);
  const from = `${schema}${q(plan.table)} a${w ? ` where ${w}` : ""}`;

  if (plan.type === "liste") {
    const tri = plan.tris.includes(query.tri) ? query.tri : plan.tri;
    const sens = query.sens === "asc" ? "asc" : query.sens === "desc" ? "desc" : plan.sens;
    const parPage = Math.min(Math.max(+query.par_page || plan.par_page, 1), 200);
    const page = Math.max(Math.floor(+query.page || 1), 1);
    const cols = plan.champs.map((c) => `a.${q(c)}`);
    for (const [nom, e] of Object.entries(plan.enfants)) {
      const extra = e.si && Object.keys(e.si).length ? ` and ${whereSql(e.si, ph)}` : "";
      const base = `from ${schema}${q(e.table)} c where c.${q(e.ref)} = a."id"${extra}`;
      const sub = e.fn === "count" ? `select count(*)::int ${base}`
        : ["sum", "min", "max"].includes(e.fn) ? `select ${e.fn}(c.${q(e.champ)}) ${base}`
        : `select c.${q(e.champ)} ${base} order by c."id" ${e.fn === "premier" ? "asc" : "desc"} limit 1`;
      cols.push(`(${sub}) as ${q(nom)}`);
    }
    const lim = ph.push(parPage), off = ph.push((page - 1) * parPage);
    const lignes = await lire(`select ${cols.join(", ")} from ${from} order by a.${q(tri)} ${sens} nulls last, a."id" ${sens} limit ${lim} offset ${off}`, ph.values);
    const ph2 = params();
    const w2 = whereSql(where, ph2);
    const total = +(await lire(`select count(*) as n from ${schema}${q(plan.table)} a${w2 ? ` where ${w2}` : ""}`, ph2.values))[0].n;
    return { type: "liste", lignes, total, page, par_page: parPage, tri, sens };
  }

  const mesures = Object.entries(plan.mesures).map(([nom, m]) => `${mesureSql(m, ph)} as ${q(nom)}`);
  const noms = Object.keys(plan.mesures);
  const propre = (r) => { const o = {}; for (const n of noms) o[n] = nombre(r[n]); return o; };

  if (!plan.groupe) {
    const r = (await lire(`select ${mesures.join(", ")} from ${from}`, ph.values))[0] || {};
    const out = { type: "agregat", valeurs: propre(r) };
    if (plan.comparer && periode && periode.du && periode.au) {
      const php = params();
      const wp = whereSql(whereDe(plan, query, tz, true).where, php);
      const mp = Object.entries(plan.mesures).map(([nom, m]) => `${mesureSql(m, php)} as ${q(nom)}`);
      const rp = (await lire(`select ${mp.join(", ")} from ${schema}${q(plan.table)} a${wp ? ` where ${wp}` : ""}`, php.values))[0] || {};
      out.precedent = propre(rp);
    }
    return out;
  }

  const g = plan.groupe;
  const cle = g.par
    ? `to_char(date_trunc('${PAS[g.par]}', a.${q(g.champ)} at time zone ${ph.push(tz)}), '${g.par === "heure" ? "YYYY-MM-DD\"T\"HH24" : "YYYY-MM-DD"}')`
    : `a.${q(g.champ)}`;
  const ordre = g.par ? "1 asc" : `2 desc nulls last`;
  const rows = await lire(`select ${cle} as cle, ${mesures.join(", ")} from ${from} group by 1 order by ${ordre} limit ${plan.type === "serie" ? 2000 : plan.limite}`, ph.values);
  let lignes = rows.map((r) => ({ cle: r.cle, ...propre(r) }));
  if (plan.type === "serie" && (g.par === "jour" || g.par === "semaine" || g.par === "mois")) lignes = remplir(lignes, g.par, periode, noms);
  return { type: plan.type, par: g.par || null, lignes };
};

/* série continue : les jours sans donnée valent 0 (sinon la courbe ment) */
const remplir = (lignes, par, periode, noms) => {
  if (!lignes.length && !periode) return lignes;
  const par0 = new Map(lignes.map((l) => [l.cle, l]));
  const debut = (periode && periode.du) || (lignes[0] && lignes[0].cle);
  const fin = (periode && periode.au && plusJours(periode.au, -1)) || (lignes[lignes.length - 1] && lignes[lignes.length - 1].cle);
  if (!debut || !fin) return lignes;
  const aligne = (iso) => {
    const d = new Date(iso + "T00:00:00Z");
    if (par === "semaine") d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7));
    if (par === "mois") d.setUTCDate(1);
    return d;
  };
  const out = [];
  for (let d = aligne(debut), n = 0; d <= new Date(fin + "T00:00:00Z") && n < 800; n++) {
    const k = d.toISOString().slice(0, 10);
    out.push(par0.get(k) || { cle: k, ...Object.fromEntries(noms.map((x) => [x, 0])) });
    if (par === "jour") d.setUTCDate(d.getUTCDate() + 1);
    else if (par === "semaine") d.setUTCDate(d.getUTCDate() + 7);
    else d.setUTCMonth(d.getUTCMonth() + 1);
  }
  return out;
};

/* ── lecture d'une source (route publique, droits vérifiés) ────────────── */
const CACHE = new Map();
const cacheVider = () => CACHE.clear();

const trouver = async (nom) => {
  const Table = require("@saltcorn/data/models/table");
  const t = Table.findOne({ name: TABLE });
  if (!t) return null;
  return await t.getRow({ nom });
};

const peutLire = (plan, user) => {
  const Table = require("@saltcorn/data/models/table");
  const t = Table.findOne({ name: plan.table });
  if (!t) return false;
  /* table principale : rôle suffisant, ou propriété des lignes (vérifiée à l'exécution) */
  const principale = user.role_id <= (t.min_role_read ?? 1) || (user.role_id < 100 && !!(t.ownership_field_id || t.ownership_formula));
  /* tables enfants : rôle suffisant, sans exception */
  const enfants = Object.values(plan.enfants || {}).every((e) => { const c = Table.findOne({ name: e.table }); return c && user.role_id <= (c.min_role_read ?? 1); });
  return principale && enfants;
};

const lireSource = async (nom, query, user) => {
  const db = require("@saltcorn/data/db");
  const src = await trouver(nom);
  if (!src) throw Object.assign(new Error("source introuvable"), { code: 404 });
  if (user.role_id > (src.role_min ?? 1)) throw Object.assign(new Error("accès refusé"), { code: 403 });
  let def;
  try { def = JSON.parse(src.definition || "{}"); } catch (e) { throw Object.assign(new Error("définition illisible"), { code: 500 }); }
  const { err, plan } = valider(def);
  if (err.length) throw Object.assign(new Error("source invalide : " + err[0]), { code: 500 });
  if (!peutLire(plan, user)) throw Object.assign(new Error("accès refusé"), { code: 403 });
  const propres = Object.fromEntries(Object.entries(query || {}).filter(([k, v]) => typeof v === "string").sort());
  const cle = JSON.stringify([db.getTenantSchema(), nom, user.role_id === 1 ? "admin" : user.id || "public", propres]);
  const ttl = Math.max(0, src.cache_s ?? 30) * 1000;
  const hit = CACHE.get(cle);
  if (ttl && hit && hit.t > Date.now() - ttl) return { ...hit.r, cache: true };
  const t0 = Date.now();
  const r = await executer(plan, propres, user);
  r.ms = Date.now() - t0;
  if (ttl) { CACHE.set(cle, { t: Date.now(), r }); if (CACHE.size > 1000) CACHE.delete(CACHE.keys().next().value); }
  return r;
};

const route = async (req, res) => {
  res.setHeader("Cache-Control", "private, no-store");
  const nom = String((req.params && req.params.nom) || "");
  if (!NOM_RE.test(nom)) return res.status(404).json({ erreur: "source introuvable" });
  try {
    const user = req.user || { role_id: 100 };
    res.json(await lireSource(nom, req.query || {}, user));
  } catch (e) {
    const code = e.code && e.code < 600 ? e.code : 500;
    if (code === 500 && req.user && req.user.role_id === 1) return res.status(500).json({ erreur: String(e.message || e) });
    res.status(code).json({ erreur: code === 500 ? "erreur de lecture" : e.message });
  }
};

module.exports = { TABLE, NOM_RE, ensureTable, valider, executer, lireSource, route, cacheVider, trouver, _enUtc: enUtc, _bornes: bornes };
