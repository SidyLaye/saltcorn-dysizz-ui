/* Sources de données (src/donnees.js) contre un vrai PostgreSQL.
   Saltcorn est simulé (tables, champs, rôles) ; le SQL, lui, tourne pour de vrai.

   Base : variables PG* habituelles (PGHOST, PGUSER, PGPASSWORD, PGDATABASE).
   Sans PostgreSQL joignable, le test est sauté (il tourne toujours en CI). */
const assert = require("assert");
const path = require("path");
const Module = require("module");

const tools = path.join(__dirname, "../tools/node_modules/");
const { Pool } = require(tools + "pg");
const internal = require(tools + "@saltcorn/db-common/dist/internal");

const SCHEMA = `dz_test_${process.pid}`;
const pool = new Pool({ max: 4, connectionTimeoutMillis: 3000 });

/* ── Saltcorn simulé ─────────────────────────────────────────────────────── */
const T = (id, name, fields, extra = {}) => ({ id, name, min_role_read: 40, fields: fields.map((f) => (typeof f === "string" ? { name: f, type: "String" } : f)), updateWhereWithOwnership: () => null, ...extra });
const D = { name: "Date" };
let TABLES = {};
let sources = [];
const fakeDb = {
  getTenantSchema: () => SCHEMA,
  getTenantSchemaPrefix: () => `"${SCHEMA}".`,
  getClient: async () => {
    const c = await pool.connect();
    await c.query(`set search_path to "${SCHEMA}"`);
    return c;
  },
};
const Table = {
  findOne: ({ name }) => (name === "dz_sources" ? { name, getRow: async ({ nom }) => sources.find((s) => s.nom === nom) || null } : TABLES[name] || null),
};
const mocks = {
  "@saltcorn/data/db": fakeDb,
  "@saltcorn/data/models/table": Table,
  "@saltcorn/data/db/state": { getState: () => ({ getConfig: (k) => (k === "timezone" ? "Europe/Paris" : undefined) }) },
  "@saltcorn/db-common/internal": internal,
};
const orig = Module._load;
Module._load = function (req, ...rest) {
  if (mocks[req]) return mocks[req];
  return orig.call(this, req, ...rest);
};
const S = require("../src/donnees");

const src = (nom, definition, extra = {}) => { sources = sources.filter((s) => s.nom !== nom); sources.push({ nom, definition: JSON.stringify(definition), role_min: 40, cache_s: 0, ...extra }); };
const admin = { id: 1, role_id: 1 }, staff = { id: 2, role_id: 40 }, public_ = { role_id: 100 };
const lire = (nom, q = {}, u = admin) => S.lireSource(nom, q, u);
const refus = async (p, code) => { try { await p; } catch (e) { assert.strictEqual(e.code, code, e.message); return e; } assert.fail("aurait dû être refusé"); };

(async () => {
  try { await pool.query("select 1"); } catch (e) { console.log("donnees.test : PostgreSQL injoignable, test sauté (" + e.message + ")"); await pool.end().catch(() => {}); return; }
  await pool.query(`create schema "${SCHEMA}"`);
  try {
    await pool.query(`set search_path to "${SCHEMA}";
      create table lead (id serial primary key, cree_le timestamptz, source text, statut text, agence text, reference_bien text, version_gabarit text, reponse_le timestamptz, prix float);
      create table lead_champ (id serial primary key, lead int, nom_champ text, valeur text);
      create table secret (id serial primary key, x text);
      insert into secret(x) values ('ne doit jamais sortir');`);
    /* 30 demandes : 3 portails, sur 10 jours autour d'un changement de jour Paris/UTC */
    const rows = [];
    for (let i = 0; i < 30; i++) {
      const src = ["leboncoin", "seloger", "figaro"][i % 3];
      const statut = i % 5 === 0 ? "rejete" : "cree";
      /* 22h30 UTC = 00h30 à Paris le lendemain : doit compter pour le lendemain */
      const t = new Date(Date.UTC(2026, 8, 10 + (i % 10), i % 2 ? 22 : 9, 30));
      rows.push(`('${t.toISOString()}','${src}','${statut}','agence${i % 2}','REF${i}','${i % 4 === 0 ? "ia" : src + "/g1"}',${i % 3 === 0 ? `'${new Date(t.getTime() + (30 + i) * 60000).toISOString()}'` : "null"},${100000 + i * 1000})`);
    }
    await pool.query(`set search_path to "${SCHEMA}"; insert into lead(cree_le,source,statut,agence,reference_bien,version_gabarit,reponse_le,prix) values ${rows.join(",")};
      insert into lead_champ(lead,nom_champ,valeur) select id,'nom','Nom'||id from lead;
      insert into lead_champ(lead,nom_champ,valeur) select id,'email','p'||id||'@example.com' from lead;
      insert into lead_champ(lead,nom_champ,valeur) values (1,'nom','Martin');`);

    TABLES = {
      lead: T(1, "lead", [{ name: "id", type: "Integer" }, { name: "cree_le", type: D }, "source", "statut", "agence", "reference_bien", "version_gabarit", { name: "reponse_le", type: D }, { name: "prix", type: "Float" }]),
      lead_champ: T(2, "lead_champ", [{ name: "id", type: "Integer" }, { name: "lead", type: "Key" }, "nom_champ", "valeur"]),
      secret: T(3, "secret", [{ name: "id", type: "Integer" }, "x"], { min_role_read: 1 }),
    };

    /* ── validation : noms de champ vérifiés, jamais collés tels quels ── */
    assert.ok(S.valider({ table: "lead", mesures: { n: { fn: "count" } } }).err.length === 0);
    assert.ok(S.valider({ table: "absente" }).err[0].includes("introuvable"));
    assert.ok(S.valider({ table: "lead", mesures: { n: { fn: "sum", champ: 'prix"; drop table lead; --' } } }).err.length, "champ inventé refusé");
    assert.ok(S.valider({ table: "lead", mesures: { n: { fn: "pg_sleep" } } }).err.length, "fonction hors liste refusée");
    assert.ok(S.valider({ table: "lead", type: "serie", groupe: { champ: "source" } }).err.length, "série sur un champ texte refusée");
    assert.ok(S.valider({ table: "lead", filtres: { x: { mode: "egal", champ: "inconnu" } } }).err.length);
    assert.ok(S.valider({ table: "lead", mesures: { "Mauvais Nom": { fn: "count" } } }).err.length, "nom de mesure contrôlé");
    assert.ok(S.valider({ table: "dz_sources" }).err.length, "la table des sources ne se lit pas par une source");

    /* ── agrégat + comparaison avec la période précédente ── */
    src("resume", { table: "lead", comparer: true, mesures: { total: { fn: "count" }, rejets: { fn: "count", si: { statut: "rejete" } }, ia: { fn: "count", si: { version_gabarit: { commence: "ia" } } }, prix: { fn: "avg", champ: "prix" }, delai: { fn: "duree_mediane", de: "cree_le", a: "reponse_le" }, repondus: { fn: "count", si: { reponse_le: { vide: false } } } }, filtres: { cree_le: "periode", source: "egal" } });
    let r = await lire("resume");
    assert.strictEqual(r.valeurs.total, 30);
    assert.strictEqual(r.valeurs.rejets, 6);
    assert.strictEqual(r.valeurs.ia, 8);
    assert.strictEqual(r.valeurs.repondus, 10);
    assert.ok(r.valeurs.delai > 30 && r.valeurs.delai < 70, "délai médian en minutes");
    assert.ok(!r.precedent, "pas de comparaison sans période");
    r = await lire("resume", { source: "seloger" });
    assert.strictEqual(r.valeurs.total, 10);
    r = await lire("resume", { source: "seloger,figaro" });
    assert.strictEqual(r.valeurs.total, 20, "plusieurs valeurs séparées par des virgules");
    r = await lire("resume", { du: "2026-09-12", au: "2026-09-13" });
    assert.ok(r.precedent && typeof r.precedent.total === "number", "période précédente calculée");
    /* bornes au fuseau de Paris : 00h30 locale compte pour le jour même */
    const parJour = {};
    for (let i = 0; i < 30; i++) { const t = new Date(Date.UTC(2026, 8, 10 + (i % 10), i % 2 ? 22 : 9, 30)); const k = new Date(t.getTime() + 2 * 3600e3).toISOString().slice(0, 10); parJour[k] = (parJour[k] || 0) + 1; }
    r = await lire("resume", { du: "2026-09-12", au: "2026-09-12" });
    assert.strictEqual(r.valeurs.total, parJour["2026-09-12"], "journée entière au fuseau du site");

    /* ── injections par l'URL : valeurs en paramètres, filtres non déclarés ignorés ── */
    r = await lire("resume", { source: "x' or '1'='1" });
    assert.strictEqual(r.valeurs.total, 0, "valeur piégée traitée comme du texte");
    r = await lire("resume", { statut: "rejete", "id; drop table lead": "1" });
    assert.strictEqual(r.valeurs.total, 30, "filtre non déclaré ignoré");
    r = await lire("resume", { du: "2026-13-45" });
    assert.strictEqual(r.valeurs.total, 30, "date invalide ignorée");
    assert.strictEqual((await pool.query(`select count(*)::int n from "${SCHEMA}".lead`)).rows[0].n, 30, "table intacte");

    /* ── série par jour : jours vides remplis à 0, clés au fuseau de Paris ── */
    src("jours", { table: "lead", type: "serie", groupe: { champ: "cree_le", par: "jour" }, mesures: { n: { fn: "count" } }, filtres: { cree_le: "periode" } });
    r = await lire("jours", { du: "2026-09-08", au: "2026-09-21" });
    assert.strictEqual(r.lignes.length, 14, "une ligne par jour, même vide");
    assert.strictEqual(r.lignes[0].cle, "2026-09-08"); assert.strictEqual(r.lignes[0].n, 0);
    assert.strictEqual(r.lignes.reduce((s, l) => s + l.n, 0), 30);
    for (const l of r.lignes) assert.strictEqual(l.n, parJour[l.cle] || 0, `jour ${l.cle}`);

    /* ── regroupement par catégorie ── */
    src("portails", { table: "lead", groupe: "source", mesures: { n: { fn: "count" } } });
    r = await lire("portails");
    assert.deepStrictEqual(r.lignes.map((l) => l.n), [10, 10, 10]);

    /* ── liste paginée, triée, avec tables liées et recherche ── */
    src("liste", { table: "lead", type: "liste", champs: ["cree_le", "source", "reference_bien"], tris: ["cree_le", "source"], par_page: 7, enfants: { nom: { table: "lead_champ", ref: "lead", champ: "valeur", si: { nom_champ: "nom" } }, nb: { table: "lead_champ", ref: "lead", fn: "count" } }, filtres: { q: { mode: "cherche", champs: ["reference_bien"], enfants: [{ table: "lead_champ", ref: "lead", champ: "valeur", si: { nom_champ: ["nom", "email"] } }] }, source: "egal" } });
    r = await lire("liste");
    assert.strictEqual(r.total, 30); assert.strictEqual(r.lignes.length, 7); assert.strictEqual(r.page, 1);
    assert.ok(r.lignes[0].nom.startsWith("Nom"), "valeur liée : la plus récente");
    assert.strictEqual(r.lignes[0].nb, 2, "compte lié en nombre");
    r = await lire("liste", { page: "5" });
    assert.strictEqual(r.lignes.length, 2, "dernière page");
    r = await lire("liste", { tri: "source", sens: "asc" });
    assert.strictEqual(r.lignes[0].source, "figaro");
    r = await lire("liste", { tri: "x; drop table lead" });
    assert.strictEqual(r.tri, "cree_le", "tri non autorisé ignoré");
    r = await lire("liste", { q: "martin" });
    assert.strictEqual(r.total, 1, "recherche dans la table liée");
    r = await lire("liste", { q: "REF1" });
    assert.ok(r.total >= 11, "recherche sur le champ principal (REF1, REF10…)");
    r = await lire("liste", { q: "%" });
    assert.strictEqual(r.total, 0, "joker traité comme du texte");
    r = await lire("liste", { par_page: "100000" });
    assert.strictEqual(r.par_page, 200, "taille de page plafonnée");

    /* ── droits ── */
    r = await lire("resume", {}, staff);
    assert.strictEqual(r.valeurs.total, 30, "staff lit une source ouverte au staff");
    await refus(lire("resume", {}, public_), 403);
    src("secret", { table: "secret", type: "liste", champs: ["x"] });
    await refus(lire("secret", {}, staff), 403);
    src("fuite", { table: "lead", type: "liste", enfants: { x: { table: "secret", ref: "id", champ: "x" } } });
    await refus(lire("fuite", {}, staff), 403);
    src("reservee", { table: "lead" }, { role_min: 1 });
    await refus(lire("reservee", {}, staff), 403);
    await refus(lire("absente"), 404);

    /* ── cache : même réponse sans relire, vidé à la demande ── */
    src("cache", { table: "lead", mesures: { n: { fn: "count" } } }, { cache_s: 60 });
    const a = await lire("cache");
    await pool.query(`insert into "${SCHEMA}".lead(source) values ('nouveau')`);
    const b = await lire("cache");
    assert.ok(b.cache && b.valeurs.n === a.valeurs.n, "servi par le cache");
    S.cacheVider();
    assert.strictEqual((await lire("cache")).valeurs.n, a.valeurs.n + 1);

    /* ── lecture seule : même un plan forgé ne peut pas écrire ── */
    const { plan } = S.valider({ table: "lead", mesures: { n: { fn: "count" } } });
    plan.table = 'lead" a; insert into lead(source) values (\'pirate\'); select 1 from "lead';
    await assert.rejects(S.executer(plan, {}, admin));
    assert.strictEqual((await pool.query(`select count(*)::int n from "${SCHEMA}".lead where source='pirate'`)).rows[0].n, 0, "aucune écriture");

    console.log("donnees.test : ok");
  } finally {
    await pool.query(`drop schema "${SCHEMA}" cascade`).catch(() => {});
    await pool.end();
  }
})().catch((e) => { console.error(e); process.exit(1); });
