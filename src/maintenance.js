/* dysizz-ui — mode maintenance.
   S'appuie sur le mode maintenance de Saltcorn (réglages maintenance_mode_enabled et maintenance_mode_page) :
   pages, vues, API, fichiers, recherche et menu répondent « en maintenance » à tout le monde sauf à
   l'administrateur (rôle 1), qui continue de tout voir et de tester. dysizz-ui y ajoute :
   - la page « maintenance » prête à l'emploi (vue « DZ Maintenance ») : titre, message, heure de retour prévue,
     compte à rebours, et rechargement tout seul dès que la maintenance est finie ;
   - les réglages en français (étape « Maintenance » des réglages de dysizz-ui) ;
   - un bandeau pour l'administrateur tant que la maintenance est active, avec un bouton pour la couper. */
"use strict";
const { esc } = require("./core");

const PAGE = "maintenance";
const VUE = "dz_maintenance";

const lireCfg = (c = {}) => ({
  active: c.maintenance === true || c.maintenance === "on",
  titre: String(c.maintenance_titre || "Site en maintenance"),
  message: String(c.maintenance_message || "Nous améliorons le service. Merci de revenir un peu plus tard."),
  fin: String(c.maintenance_fin || "").trim(),
});
/* « 2026-10-01 18:30 » ou « 2026-10-01T18:30 » → Date (heure de Paris) */
const dateFin = (s) => {
  const m = String(s || "").match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{1,2}):(\d{2})/);
  if (!m) return null;
  /* l'heure saisie est celle de Paris, quel que soit le fuseau du serveur */
  const utc = Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5]);
  const vuParis = new Date(new Date(utc).toLocaleString("en-US", { timeZone: "Europe/Paris" }));
  const vuUtc = new Date(new Date(utc).toLocaleString("en-US", { timeZone: "UTC" }));
  const d = new Date(utc - (vuParis - vuUtc));
  return isNaN(d) ? null : d;
};
const finLisible = (s) => {
  const d = dateFin(s);
  return d ? d.toLocaleString("fr-FR", { timeZone: "Europe/Paris", weekday: "long", day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" }) : "";
};

/* Saltcorn 1.6.2, route /view/<nom> pendant la maintenance : la page de maintenance est calculée mais jamais
   envoyée (le navigateur attend sans fin). Si personne n'a répondu une fois le calcul fini, on l'envoie. */
const envoyerSurVue = ({ req, res } = {}, c, html) => {
  if (!req || !res || typeof res.sendWrap !== "function") return;
  if (!/^\/view\//.test(String(req.originalUrl || req.url || ""))) return;
  const st = require("@saltcorn/data/db/state").getState();
  if (!st.getConfig("maintenance_mode_enabled", false) || (req.user && req.user.role_id <= 1)) return;
  setImmediate(() => {
    if (res.headersSent) return;
    try { res.status(503); res.sendWrap({ title: c.titre, bodyClass: "page_" + PAGE }, html); } catch (e) { /* rien */ }
  });
};

/* Vue « DZ Maintenance » : ce que voient les utilisateurs pendant la maintenance */
const vue = {
  name: "DZ Maintenance",
  description: "Page de maintenance : titre, message et heure de retour prévue (réglés dans dysizz-ui → Maintenance). Se recharge toute seule quand la maintenance est finie.",
  tableless: true,
  display_state_form: false,
  get_state_fields: async () => [],
  configuration_workflow: () => {
    const Workflow = require("@saltcorn/data/models/workflow");
    const Form = require("@saltcorn/data/models/form");
    return new Workflow({ steps: [{ name: "Réglages", form: async () => new Form({ blurb: "Le texte se règle dans les réglages de dysizz-ui, étape « Maintenance ».", fields: [] }) }] });
  },
  run: async (table_id, viewname, cfg, state, extra = {}) => {
    const c = lireCfg(await require("./pluginCfg").getCfg().catch(() => ({})));
    const fin = dateFin(c.fin);
    const msg = esc(c.message).replace(/\n/g, "<br>");
    const html = `<div class="dz-maintenance" data-dz-maintenance="1"${fin ? ` data-fin="${esc(fin.toISOString())}"` : ""}>
<div class="dz-maintenance-carte"><div class="dz-maintenance-ic"><i class="fas fa-tools"></i></div>
<h1>${esc(c.titre)}</h1><p>${msg}</p>
${fin ? `<p class="dz-maintenance-fin">Retour prévu : <b>${esc(finLisible(c.fin))}</b><span class="dz-maintenance-rebours"></span></p>` : ""}
<p class="dz-maintenance-note">Cette page se recharge toute seule dès que le site est de nouveau disponible.</p>
<p class="dz-maintenance-admin"><a href="/auth/login">Connexion administrateur</a></p></div></div>`;
    envoyerSurVue(extra, c, html);
    return html;
  },
};

/* crée la vue et la page si elles manquent (vérifié en base : findOne lit un cache) */
const assurerPage = async () => {
  const View = require("@saltcorn/data/models/view"), Page = require("@saltcorn/data/models/page");
  const db = require("@saltcorn/data/db");
  const st = require("@saltcorn/data/db/state").getState();
  if (!View.findOne({ name: VUE }) && !(await db.selectMaybeOne("_sc_views", { name: VUE }))) {
    await View.create({ name: VUE, viewtemplate: "DZ Maintenance", table_id: null, configuration: {}, min_role: 100, description: "Page de maintenance de dysizz-ui" });
    await st.refresh_views();
  }
  if (!Page.findOne({ name: PAGE }) && !(await db.selectMaybeOne("_sc_pages", { name: PAGE }))) {
    await Page.create({ name: PAGE, title: "Maintenance", description: "Page montrée pendant la maintenance (dysizz-ui)", min_role: 100, fixed_states: {},
      layout: { type: "container", customClass: "dz-ecran", contents: { type: "view", view: VUE, name: "dzmaintenance", state: "shared" } } });
    await st.refresh_pages();
  }
};

/* Applique le réglage au mode maintenance de Saltcorn. Ne touche au réglage de Saltcorn que si le choix fait dans
   dysizz-ui a changé : une maintenance activée à la main dans Saltcorn n'est pas coupée au redémarrage. */
const appliquer = async (raw = {}) => {
  const c = lireCfg(raw);
  const st = require("@saltcorn/data/db/state").getState();
  const dernier = st.getConfig("dz_maintenance_applique", null);
  if (dernier === c.active) return false;
  /* première installation, maintenance non demandée : on note seulement, sans toucher au réglage de Saltcorn */
  if (dernier === null && !c.active) { await st.setConfig("dz_maintenance_applique", false); return false; }
  if (c.active) await assurerPage();
  await st.setConfig("maintenance_mode_page", PAGE);
  await st.setConfig("maintenance_mode_enabled", c.active);
  await st.setConfig("dz_maintenance_applique", c.active);
  try { st.log(2, `[dysizz-ui] maintenance ${c.active ? "activée" : "coupée"}`); } catch (e) { /* rien */ }
  return true;
};

/* GET /dysizz/maintenance/etat : pour la page de maintenance (recharger à la fin) et le bandeau de l'admin */
const etat = async (req, res) => {
  const st = require("@saltcorn/data/db/state").getState();
  const active = !!st.getConfig("maintenance_mode_enabled", false);
  const c = lireCfg(await require("./pluginCfg").getCfg().catch(() => ({})));
  res.set("Cache-Control", "no-store");
  res.json({ active, fin: active && dateFin(c.fin) ? dateFin(c.fin).toISOString() : null, admin: !!(req.user && req.user.role_id === 1) });
};

/* POST /dysizz/maintenance : l'administrateur coupe (ou active) la maintenance depuis le bandeau */
const basculer = async (req, res) => {
  if (!req.user || req.user.role_id !== 1) return res.status(403).json({ error: "réservé à l'administrateur" });
  const b = req.body || {};
  const active = b.active === true || b.active === "1" || b.active === "true";
  await require("./pluginCfg").patchCfg({ maintenance: active });
  await appliquer({ ...(await require("./pluginCfg").getCfg()), maintenance: active });
  if (req.xhr || /json/.test(String(req.headers.accept || ""))) return res.json({ active });
  const retour = String(b.retour || "/");
  /* chemin local seulement : ni « //site », ni « /\site » */
  return res.redirect(/^\/(?![\/\\])/.test(retour) ? retour : "/");
};

module.exports = { PAGE, VUE, vue, envoyerSurVue, lireCfg, dateFin, finLisible, assurerPage, appliquer, etat, basculer };
