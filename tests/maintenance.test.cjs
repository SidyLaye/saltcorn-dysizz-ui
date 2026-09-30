/* Mode maintenance : heure de retour (heure de Paris), application au réglage de Saltcorn seulement quand le choix
   change, états et droits des routes (Saltcorn simulé). */
"use strict";
const assert = require("assert");
const Module = require("module");
const cfg = {}, logs = [];
let plugin = {};
const state = { getConfig: (k, d) => (k in cfg ? cfg[k] : d), setConfig: async (k, v) => { cfg[k] = v; }, log: (n, m) => logs.push(m), refresh_views: async () => {}, refresh_pages: async () => {} };
const crees = [];
const orig = Module._load;
Module._load = function (req, parent, ...rest) {
  if (req === "@saltcorn/data/db/state") return { getState: () => state };
  if (req === "@saltcorn/data/db") return { selectMaybeOne: async () => null };
  if (req === "@saltcorn/data/models/view") return { findOne: () => null, create: async (v) => crees.push(["vue", v.name]) };
  if (req === "@saltcorn/data/models/page") return { findOne: () => null, create: async (p) => crees.push(["page", p.name]) };
  if (req.startsWith("@saltcorn/")) return class {};
  if (/pluginCfg$/.test(req)) return { getCfg: async () => ({ ...plugin }), patchCfg: async (p) => { plugin = { ...plugin, ...p }; } };
  return orig.call(this, req, parent, ...rest);
};
const M = require("../src/maintenance");
const rep = () => { const r = { code: 200, h: {} }; r.status = (c) => ((r.code = c), r); r.set = (k, v) => ((r.h[k] = v), r); r.json = (b) => ((r.body = b), r); r.redirect = (u) => ((r.loc = u), r); return r; };
(async () => {
  /* heure de Paris, été (UTC+2) et hiver (UTC+1) */
  assert.strictEqual(M.dateFin("2026-07-01 18:30").toISOString(), "2026-07-01T16:30:00.000Z");
  assert.strictEqual(M.dateFin("2026-12-01T08:05").toISOString(), "2026-12-01T07:05:00.000Z");
  assert.strictEqual(M.dateFin("demain"), null);
  assert.strictEqual(M.dateFin(""), null);
  assert.match(M.finLisible("2026-07-01 18:30"), /18:30/);
  assert.deepStrictEqual(M.lireCfg({}).active, false);
  assert.strictEqual(M.lireCfg({ maintenance: "on" }).active, true);

  /* première installation sans maintenance : une maintenance mise à la main dans Saltcorn reste */
  cfg.maintenance_mode_enabled = true;
  assert.strictEqual(await M.appliquer({}), false);
  assert.strictEqual(cfg.maintenance_mode_enabled, true); assert.strictEqual(cfg.dz_maintenance_applique, false);
  delete cfg.maintenance_mode_enabled; delete cfg.dz_maintenance_applique;
  /* activer : page créée, réglages de Saltcorn posés */
  assert.strictEqual(await M.appliquer({ maintenance: true }), true);
  assert.deepStrictEqual(crees, [["vue", "dz_maintenance"], ["page", "maintenance"]]);
  assert.strictEqual(cfg.maintenance_mode_enabled, true); assert.strictEqual(cfg.maintenance_mode_page, "maintenance");
  /* même choix : rien n'est réécrit (une maintenance mise à la main dans Saltcorn n'est pas coupée au redémarrage) */
  cfg.maintenance_mode_enabled = "touché";
  assert.strictEqual(await M.appliquer({ maintenance: true }), false);
  assert.strictEqual(cfg.maintenance_mode_enabled, "touché");
  cfg.maintenance_mode_enabled = true;

  /* rendu de la page : texte échappé, heure de retour */
  plugin = { maintenance: true, maintenance_titre: "Mise à jour <b>", maintenance_message: "Ligne 1\nLigne 2", maintenance_fin: "2026-07-01 18:30" };
  const html = await M.vue.run();
  assert.match(html, /data-dz-maintenance="1"/); assert.match(html, /data-fin="2026-07-01T16:30:00.000Z"/);
  assert.match(html, /Mise à jour &lt;b&gt;/); assert.match(html, /Ligne 1<br>Ligne 2/);

  /* /view/<nom> pendant la maintenance (Saltcorn 1.6.2 n'envoie rien) : la vue envoie la page, en 503 */
  const envoi = (url, user, deja = false) => new Promise((ok) => {
    const res = { headersSent: deja, sent: null, code: 200, status(c) { this.code = c; return this; }, sendWrap(o, h) { this.sent = h; this.opts = o; } };
    M.vue.run(null, "dz_maintenance", {}, {}, { req: { originalUrl: url, user }, res }).then(() => setImmediate(() => ok(res)));
  });
  let e = await envoi("/view/liste", null); assert.strictEqual(e.code, 503); assert.match(e.sent, /data-dz-maintenance/);
  assert.strictEqual(e.opts.no_menu, true, "pas de menu sur /view/"); assert.ok(e.sent.includes(M.SANS_MENU), "menu caché hors admin");
  /* page vue par l'administrateur (aperçu) : le menu reste */
  assert.ok(!(await M.vue.run(null, "dz_maintenance", {}, {}, { req: { originalUrl: "/page/maintenance", user: { role_id: 1 } } })).includes(M.SANS_MENU));
  e = await envoi("/page/accueil", null); assert.strictEqual(e.sent, null, "route /page : Saltcorn envoie lui-même");
  e = await envoi("/view/liste", { role_id: 1 }); assert.strictEqual(e.sent, null, "admin : rien");
  e = await envoi("/view/liste", null, true); assert.strictEqual(e.sent, null, "déjà répondu : rien");

  /* état : lisible par tous, dit si c'est l'admin */
  let r = rep(); await M.etat({ user: { role_id: 80 } }, r);
  assert.deepStrictEqual(r.body, { active: true, fin: "2026-07-01T16:30:00.000Z", admin: false });
  assert.strictEqual(r.h["Cache-Control"], "no-store");
  r = rep(); await M.etat({}, r); assert.strictEqual(r.body.admin, false);

  /* couper : réservé à l'admin */
  r = rep(); await M.basculer({ user: { role_id: 40 }, body: { active: false }, headers: {} }, r);
  assert.strictEqual(r.code, 403); assert.strictEqual(cfg.maintenance_mode_enabled, true);
  r = rep(); await M.basculer({ body: { active: false }, headers: {} }, r); assert.strictEqual(r.code, 403);
  r = rep(); await M.basculer({ user: { role_id: 1 }, body: { active: false }, headers: { accept: "application/json" } }, r);
  assert.deepStrictEqual(r.body, { active: false });
  assert.strictEqual(cfg.maintenance_mode_enabled, false); assert.strictEqual(plugin.maintenance, false);
  /* redirection : jamais vers un autre site */
  r = rep(); await M.basculer({ user: { role_id: 1 }, body: { active: "1", retour: "//ailleurs.example" }, headers: {} }, r);
  assert.strictEqual(r.loc, "/"); assert.strictEqual(cfg.maintenance_mode_enabled, true);
  console.log("maintenance : OK");
})().catch((e) => { console.error(e); process.exit(1); });
