/* Page Santé et sécurité (src/admin/sante.js) avec un Saltcorn simulé :
   chaque vérification, l'aperçu qui n'écrit rien, puis l'application. */
const assert = require("assert");
const Module = require("module");

let config = {};
let tenant = "public";
let transactionsOk = true;
const meta = new Map();
let nextId = 1;
const triggers = [{ id: 7, name: "test", min_role: 100, when_trigger: "Never" }, { id: 8, name: "releve", min_role: 1, when_trigger: "Often" }];
const tables = [{ id: 1, name: "users", min_role_write: 100 }, { id: 2, name: "contacts", min_role_write: 100 }, { id: 3, name: "taches", min_role_write: 1 }];
const supprimes = [];
const ligne = (o) => ({ ...o, delete: async function () { supprimes.push(`${o.name}#${o.id}`); } });
let views = [ligne({ id: 1, name: "contact_form", viewtemplate: "Edit", min_role: 100, configuration: {} }), ligne({ id: 2, name: "liste", viewtemplate: "List", min_role: 100, configuration: {} })];
/* doublons : « accueil » identique ×2, « tableau » avec deux contenus différents */
let pages = [ligne({ id: 3, name: "accueil", title: "A", min_role: 1, layout: { a: 1 }, fixed_states: {} }), ligne({ id: 9, name: "accueil", title: "A", min_role: 1, layout: { a: 1 }, fixed_states: {} }), ligne({ id: 4, name: "tableau", title: "T", min_role: 1, layout: { b: 1 }, fixed_states: {} }), ligne({ id: 5, name: "tableau", title: "T", min_role: 1, layout: { b: 2 }, fixed_states: {} }), ligne({ id: 6, name: "seule", title: "S", min_role: 1, layout: {}, fixed_states: {} })];

const fakeState = {
  plugins: { "dysizz-flow": {} },
  getConfig: (k, d) => (k in config ? config[k] : d),
  setConfig: async (k, v) => { config[k] = v; },
  log: () => {},
};
const fakeDb = {
  getTenantSchema: () => tenant,
  connectObj: { default_schema: "public" },
  is_it_multi_tenant: () => true,
  withTransaction: async (f) => {
    const avant = new Map(meta);
    try { return await f(); } catch (e) { if (transactionsOk) { meta.clear(); for (const [k, v] of avant) meta.set(k, v); } throw e; }
  },
};
class MetaData {
  constructor(o) { Object.assign(this, o); }
  static async create(o) { const m = new MetaData({ ...o, id: nextId++ }); meta.set(m.id, m); return m; }
  static async findOne({ id }) { return meta.get(id) || null; }
  async delete() { meta.delete(this.id); }
}
const mocks = {
  "@saltcorn/data/db/state": { getState: () => fakeState },
  "@saltcorn/data/db": fakeDb,
  "@saltcorn/data/models/metadata": MetaData,
  "@saltcorn/data/models/table": { find: async () => tables },
  "@saltcorn/data/models/view": { find: async () => views },
  "@saltcorn/data/models/page": { find: async () => pages },
  "@saltcorn/data/models/trigger": { find: () => triggers, update: async (id, row) => Object.assign(triggers.find((t) => t.id === id), row) },
  "@saltcorn/data/models/plugin": { find: async () => [{ name: "dysizz-ui", version: "3.7.0" }, { name: "dysizz-flow", version: "2.4.1" }, { name: "base", version: "latest" }] },
};
const orig = Module._load;
Module._load = function (req, ...rest) {
  if (mocks[req]) return mocks[req];
  if (req.startsWith("@saltcorn/")) return class {};
  return orig.call(this, req, ...rest);
};

const { evaluer, santePage, corriger } = require("../src/admin/sante");
const req = (extra = {}) => ({ user: { id: 1, role_id: 1, email: "a@b.c" }, headers: { "x-forwarded-proto": "https" }, subdomains: ["web"], csrfToken: () => "jeton", query: {}, body: {}, ...extra });
const res = () => { const r = { redirected: null, html: null, code: 200 }; r.redirect = (u) => { r.redirected = u; }; r.sendWrap = (t, b) => { r.html = b.above[0].contents; }; r.status = (c) => { r.code = c; return r; }; r.send = (s) => { r.html = s; }; return r; };
const par = (rs) => Object.fromEntries(rs.map((r) => [r.id, r]));

(async () => {
  /* instance neuve, racine, derrière un proxy HTTPS, transactions cassées */
  delete process.env.DZF_CLE_COFFRE;
  config = { smtp_host: "ssl0.ovh.net", smtp_port: 25, tenants_install_git: true };
  transactionsOk = false;
  let r = par(await evaluer(req()));
  assert.strictEqual(r["2fa"].etat, "ko"); assert.strictEqual(r["2fa"].gravite, "critique"); assert.ok(r["2fa"].fixable);
  assert.strictEqual(r.inscriptions.etat, "ko");
  assert.strictEqual(r.mots_de_passe.etat, "ko");
  assert.strictEqual(r.sauvegardes.etat, "ko"); assert.ok(r.sauvegardes.fixable);
  assert.strictEqual(r.sauvegardes_chiffrees.etat, "ko"); assert.ok(!r.sauvegardes_chiffrees.fixable, "mot de passe : jamais choisi à ta place");
  assert.strictEqual(r.smtp.etat, "ko");
  assert.strictEqual(r.ecriture_publique.etat, "ko");
  assert.ok(r.ecriture_publique.dit.includes("contacts") && r.ecriture_publique.dit.includes("contact_form"), "table et vue d'édition publiques listées");
  assert.ok(!r.ecriture_publique.dit.includes(">users<"), "users ignorée (inscription gérée à part)");
  assert.ok(!r.ecriture_publique.dit.includes(">liste<"), "une vue List publique n'écrit pas");
  assert.strictEqual(r.declencheurs_publics.etat, "ko"); assert.ok(r.declencheurs_publics.dit.includes("test"));
  assert.strictEqual(r.transactions.etat, "ko"); assert.ok(r.transactions.dit.includes("<b>web</b>"), "cause expliquée : sous-domaine pris pour un tenant");
  assert.strictEqual(meta.size, 0, "la sonde ne laisse rien derrière elle");
  assert.strictEqual(r.cle_coffre.etat, "ko");
  assert.strictEqual(r.cookies.etat, "ko"); assert.strictEqual(r.cors.etat, "ko"); assert.strictEqual(r.en_tetes.etat, "ko");
  assert.strictEqual(r.plugins_git.etat, "ko");
  assert.strictEqual(r.versions.etat, "info"); assert.ok(r.versions.dit.includes("dysizz-flow 2.4.1"));

  assert.strictEqual(r.doublons.etat, "ko"); assert.ok(r.doublons.fixable);
  assert.ok(r.doublons.dit.includes("<b>accueil</b> × 2 (copies identiques)") && r.doublons.dit.includes("<b>tableau</b> × 2 (contenus différents)"));

  /* la page s'affiche, triée : critiques en premier */
  const p = res(); await santePage(req(), p);
  assert.ok(p.html.includes("Santé et sécurité") && p.html.includes("À traiter"));
  assert.ok(p.html.indexOf("Double authentification") < p.html.indexOf("Inscriptions ouvertes"), "critique avant important");

  /* réservé aux admins */
  const refus = res(); await santePage(req({ user: { id: 2, role_id: 80 } }), refus);
  assert.strictEqual(refus.code, 403);

  /* aperçu : rien n'est écrit */
  const avant = JSON.stringify(config);
  const a = res(); await corriger(req({ body: { id: "2fa" } }), a);
  assert.strictEqual(JSON.stringify(config), avant, "l'aperçu n'écrit rien");
  assert.ok(a.html.includes("Aperçu") && a.html.includes("Mandatory") && a.html.includes("confirmer"));

  /* application */
  const b = res(); await corriger(req({ body: { id: "2fa", confirmer: "1" } }), b);
  assert.deepStrictEqual(config.twofa_policy_by_role, { 1: "Mandatory" });
  assert.ok(b.redirected.includes("ok="));
  /* doublons : aperçu sans suppression, puis seules les copies identiques partent (la plus ancienne reste) */
  const ad = res(); await corriger(req({ body: { id: "doublons" } }), ad);
  assert.deepStrictEqual(supprimes, [], "l'aperçu ne supprime rien");
  assert.ok(ad.html.includes("<b>accueil</b> : 1 copie(s) en moins") && !ad.html.includes("<b>tableau</b> : "));
  await corriger(req({ body: { id: "doublons", confirmer: "1" } }), res());
  assert.deepStrictEqual(supprimes, ["accueil#9"], "copie la plus récente retirée, contenus différents gardés");
  pages = pages.filter((x) => x.id !== 9);

  for (const id of ["inscriptions", "mots_de_passe", "sauvegardes", "declencheurs_publics", "cookies", "cors", "en_tetes"]) await corriger(req({ body: { id, confirmer: "1" } }), res());
  assert.strictEqual(config.allow_signup, false);
  assert.strictEqual(config.min_password_length, 12); assert.strictEqual(config.check_common_passwords, true);
  assert.strictEqual(config.auto_backup_frequency, "Daily");
  assert.strictEqual(triggers.find((t) => t.name === "test").min_role, 1, "action publique repassée en admin");
  assert.strictEqual(triggers.find((t) => t.name === "releve").min_role, 1, "les autres ne bougent pas");
  assert.strictEqual(config.force_secure_cookies, true); assert.strictEqual(config.cors_enabled, false);
  assert.ok(config.custom_http_headers.includes("Strict-Transport-Security"));

  /* en-têtes : les lignes existantes sont gardées, pas de doublon */
  config.custom_http_headers = "X-Perso: 1\nX-Content-Type-Options: nosniff";
  await corriger(req({ body: { id: "en_tetes", confirmer: "1" } }), res());
  const lignes = config.custom_http_headers.split("\n");
  assert.ok(lignes.includes("X-Perso: 1"));
  assert.strictEqual(lignes.filter((l) => l.startsWith("X-Content-Type-Options")).length, 1);

  /* déjà corrigé : rien à faire ; correction inconnue refusée */
  const c = res(); await corriger(req({ body: { id: "2fa", confirmer: "1" } }), c);
  assert.ok(decodeURIComponent(c.redirected).includes("déjà en ordre"));
  const d = res(); await corriger(req({ body: { id: "nimporte", confirmer: "1" } }), d);
  assert.ok(d.redirected.includes("err="));

  /* sauvegarde gardée sur le serveur : signalée, mais pas « corrigée » automatiquement */
  r = par(await evaluer(req()));
  assert.strictEqual(r.sauvegardes.etat, "ko"); assert.strictEqual(r.sauvegardes.gravite, "important"); assert.ok(!r.sauvegardes.fixable);

  /* tenant non racine : les réglages du serveur ne sont ni montrés ni modifiables */
  tenant = "client1";
  r = par(await evaluer(req()));
  for (const id of ["cookies", "cors", "plugins_git"]) assert.ok(!r[id], `${id} réservé à la racine`);
  const e = res(); await corriger(req({ body: { id: "cors", confirmer: "1" } }), e);
  assert.ok(e.redirected.includes("err="));

  /* transactions qui marchent */
  tenant = "public"; transactionsOk = true;
  r = par(await evaluer(req()));
  assert.strictEqual(r.transactions.etat, "ok");
  assert.strictEqual(meta.size, 0);

  console.log("santé et sécurité ok :", Object.keys(r).length, "vérifications");
})().catch((e) => { console.error(e); process.exit(1); });
