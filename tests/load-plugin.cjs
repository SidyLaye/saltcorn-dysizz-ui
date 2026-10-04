/* Charge index.js avec des doublures de @saltcorn/* et vérifie l'essentiel. */
const Module = require("module");
const orig = Module._load;
Module._load = function (req, ...rest) {
  if (req.startsWith("@saltcorn/")) return class { constructor(o) { Object.assign(this, o); } };
  return orig.call(this, req, ...rest);
};
const assert = require("assert");
const plugin = require("../index.js");
assert.strictEqual(plugin.sc_plugin_api_version, 1);
assert.strictEqual(plugin.plugin_name, "dysizz-ui");
// Saltcorn State.registerPlugin appelle chaque contribution avec la configuration
// lorsque le plugin expose configuration_workflow (contrat Saltcorn 1.6.2).
const withCfg = (key, fallback) => plugin.configuration_workflow
  ? plugin[key] ? plugin[key]({}) : fallback
  : plugin[key] || fallback;
const registeredViews = withCfg("viewtemplates", []);
assert(registeredViews.some(v => v.name === "DZ Écran"), "DZ Écran enregistré");
const registeredActions = withCfg("actions", {});
assert.strictEqual(typeof registeredActions.dz_ui_application.run, "function", "action enregistrable par Saltcorn");
for (const [key, fallback] of [["types", []], ["functions", {}], ["modelpatterns", {}], ["fileviews", {}], ["eventTypes", {}], ["fonts", {}], ["icons", []], ["table_providers", {}], ["authentication", {}], ["exchange", {}], ["copilot_skills", []], ["external_tables", {}], ["fieldviews", {}], ["headers", []], ["routes", []]]) {
  assert.doesNotThrow(() => withCfg(key, fallback), key + " respecte le contrat de chargement");
}
const h = plugin.headers({ families: ["projet"], transition: "stack", smooth: "light" });
const css = h.filter((x) => x.css).map((x) => x.css);
assert(css.some((c) => c.endsWith("dz-core.css")), "dz-core.css chargé");
assert(css.some((c) => c.endsWith("dz-f-projet.css")), "famille projet chargée");
assert(h.some((x) => x.script && x.script.endsWith("dz-smooth.js")), "défilement doux chargé");
assert(h.some((x) => x.headerTag && x.headerTag.includes("data-dz-tr")), "transition posée");
const routes = plugin.routes({}).map((r) => r.url);
for (const u of ["/dysizz-ui", "/dysizz-ui/blocks", "/dysizz-ui/classes", "/dysizz-ui/transitions", "/dysizz-ui/a/:ver/:file"]) assert(routes.includes(u), "route " + u);
console.log("plugin OK :", routes.length, "routes,", h.length, "en-têtes");
