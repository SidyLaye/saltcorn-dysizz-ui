/* =====================================================================
   dysizz-ui — plugin Saltcorn (point d'entrée)
   Le fichier index.js à la racine du dépôt est GÉNÉRÉ depuis src/ par
   tools/build.mjs : ne pas le modifier à la main.
   ===================================================================== */
"use strict";
const { PLUGIN } = require("./core");
const { serveAsset } = require("./assets");
const { configuration_workflow } = require("./settings");
const { headers } = require("./headers");
const { adminPage, saveFamilies, installPages, galerie } = require("./admin/home");
const { classesPage, saveClass, deleteClass, exportClasses, importClasses, classNames } = require("./admin/classes");
const { transitionsPage } = require("./admin/transitions");
const hub = require("./hub");
const { dz_mail } = require("./fieldviews");
const { atelierPage, saveBlock, deleteBlock, exportBlocks, importBlocks } = require("./admin/atelier");

const onLoad = async () => {
  try {
    const { getState } = require("@saltcorn/data/db/state");
    const st = getState();
    if (st && st.assets_by_role && typeof st.computeAssetsByRole === "function") await st.computeAssetsByRole();
    await hub.ensureMenu();
  } catch (e) {
    /* pas bloquant */
  }
};

module.exports = {
  sc_plugin_api_version: 1,
  plugin_name: PLUGIN,
  onLoad,
  configuration_workflow,
  headers,
  /* affichages de champs : corps d'e-mail sûr et lisible */
  fieldviews: () => ({ dz_mail }),
  /* vues de données, utilisables dans tous les tenants (Vues → Créer) */
  viewtemplates: () => [require("./views/indicateurs"), require("./views/tableau"), require("./views/repartition"), require("./views/avenir"), require("./views/graphique"), require("./views/calendrier"), require("./views/journal"), require("./views/statut"), require("./views/disponibilite")],
  routes: () => [
    /* l'accueil façon Windows 8 : toutes les applis, outils Dysizz et l'admin Saltcorn */
    { url: "/dysizz", method: "get", callback: hub.hubPage },
    { url: "/dysizz/home", method: "post", callback: hub.setHome },
    { url: "/dysizz-ui", method: "get", callback: adminPage },
    { url: "/dysizz-ui/a/:ver/:file", method: "get", callback: serveAsset },
    { url: "/dysizz-ui/families", method: "post", callback: saveFamilies },
    { url: "/dysizz-ui/install-pages", method: "post", callback: installPages },
    { url: "/dysizz-ui/galerie", method: "get", callback: galerie },
    { url: "/dysizz-ui/classes", method: "get", callback: classesPage },
    { url: "/dysizz-ui/classes/save", method: "post", callback: saveClass },
    { url: "/dysizz-ui/classes/delete", method: "post", callback: deleteClass },
    { url: "/dysizz-ui/classes/export", method: "get", callback: exportClasses },
    { url: "/dysizz-ui/classes/import", method: "post", callback: importClasses },
    { url: "/dysizz-ui/classes/names", method: "get", callback: classNames },
    { url: "/dysizz-ui/transitions", method: "get", callback: transitionsPage },
    { url: "/dysizz-ui/blocks", method: "get", callback: atelierPage },
    { url: "/dysizz-ui/blocks/save", method: "post", callback: saveBlock },
    { url: "/dysizz-ui/blocks/delete", method: "post", callback: deleteBlock },
    { url: "/dysizz-ui/blocks/export", method: "get", callback: exportBlocks },
    { url: "/dysizz-ui/blocks/import", method: "post", callback: importBlocks },
  ],
};

