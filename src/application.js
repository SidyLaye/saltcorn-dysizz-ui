/* Présentation d'application, configurée par tenant ; aucun nom de page métier ici. */
"use strict";
const { VERSION } = require("./core");
const { patchCfg, getCfg } = require("./pluginCfg");
const valid = (v) => typeof v === "string" && /^[a-zA-Z0-9_-]{1,100}$/.test(v);
const clean = (raw) => {
  if (typeof raw === "string") { try { raw = JSON.parse(raw); } catch { return null; } }
  if (!raw || typeof raw !== "object" || Array.isArray(raw) || raw.enabled !== true) return null;
  const pages = Object.create(null);
  for (const [name, p] of Object.entries(raw.pages || {}).slice(0, 80)) {
    if (!valid(name) || ["__proto__", "constructor", "prototype"].includes(name) || !p || typeof p !== "object") continue;
    pages[name] = {
      title: String(p.title || "").slice(0, 120),
      layout: p.layout === "property" ? "property" : "standard",
      charts: p.charts === true,
      inline_sources: (Array.isArray(p.inline_sources) ? p.inline_sources : []).filter(valid).slice(0, 10),
      sections: (Array.isArray(p.sections) ? p.sections : []).slice(0, 12).map(s => ({
        title: String(s.title || "Rubrique").slice(0, 80),
        sources: (Array.isArray(s.sources) ? s.sources : []).filter(valid).slice(0, 40),
      })),
    };
  }
  if (!Object.keys(pages).length) return null;
  return { enabled: true, pages };
};
const widgetsOf = (layout, out = []) => {
  if (!layout || typeof layout !== "object") return out;
  if (layout.view === "dz_ecran") out.push(layout.configuration || {});
  else for (const v of Object.values(layout)) if (typeof v === "object") widgetsOf(v, out);
  return out;
};
const action = {
  description: "Présentation des applications : vérifier, activer ou restaurer",
  requireRow: false,
  configFields: async () => [
    { name: "operation", label: "Opération", type: "String", attributes: { options: ["verifier", "activer", "restaurer"] } },
    { name: "presentation", label: "Présentation (JSON)", type: "String", fieldview: "textarea" },
  ],
  run: async ({ configuration = {}, user }) => {
    if (!user || Number(user.role_id) !== 1) throw new Error("Réservé à l’administrateur");
    const { getState } = require("@saltcorn/data/db/state");
    const st = getState(), key = "dz_application_sauvegardes";
    const cfg = await getCfg();
    if (configuration.operation === "restaurer") {
      const backups = st.getConfig(key, []), last = backups.at(-1);
      if (!last) throw new Error("Aucune présentation sauvegardée");
      await patchCfg({ application_ui: last.application_ui || "" });
      return { version: VERSION, restaure: true, sauvegarde: last.date };
    }
    const next = clean(configuration.presentation || cfg.application_ui);
    if (!next) throw new Error("Présentation absente ou invalide");
    const Page = require("@saltcorn/data/models/page");
    const all = await Page.find({});
    const report = [];
    for (const [name, plan] of Object.entries(next.pages)) {
      const candidates = all.filter(p => p.name === name);
      if (candidates.length !== 1) throw new Error("Page absente ou multiple : " + name);
      const page = candidates[0], widgets = widgetsOf(page.layout);
      if (!widgets.length) throw new Error("Aucun bloc d’écran sur " + name);
      const sources = new Set(widgets.map(w => w.source).filter(Boolean));
      const absent = plan.sections.flatMap(s => s.sources).filter(s => !sources.has(s));
      if (absent.length) throw new Error("Sources absentes sur " + name + " : " + absent.join(", "));
      report.push({ page: name, blocs: widgets.length, rubriques: plan.sections.length });
    }
    const same = JSON.stringify(clean(cfg.application_ui)) === JSON.stringify(next);
    if (configuration.operation !== "activer") return { version: VERSION, verification: true, deja_actif: same, pages: report };
    if (!same) {
      const backups = st.getConfig(key, []);
      await st.setConfig(key, [...backups.slice(-4), { date: new Date().toISOString(), application_ui: cfg.application_ui || "" }]);
      await patchCfg({ application_ui: JSON.stringify(next) });
    }
    const stored = clean((await getCfg()).application_ui);
    if (JSON.stringify(stored) !== JSON.stringify(next)) throw new Error("Présentation enregistrée non confirmée");
    return { version: VERSION, actif: true, deja_actif: same, pages: report, menu_conserve: true };
  },
};
module.exports = { clean, widgetsOf, action };
