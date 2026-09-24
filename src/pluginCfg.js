/* dysizz-ui — lire / modifier la configuration du plugin depuis nos pages.
   On passe par le mécanisme natif de Saltcorn : enregistrement en base,
   rechargement du plugin sur ce processus, puis message refresh_plugin_cfg
   pour les autres workers et les autres serveurs (multi-nœud). */
"use strict";
const { PLUGIN } = require("./core");

const findMe = async () => {
  const Plugin = require("@saltcorn/data/models/plugin");
  const all = await Plugin.find({});
  return all.find((p) => p.name === PLUGIN) || all.find((p) => /dysizz-ui/i.test(`${p.name} ${p.location || ""}`));
};

const getCfg = async () => {
  const me = await findMe();
  return (me && me.configuration) || {};
};

const patchCfg = async (patch) => {
  const Plugin = require("@saltcorn/data/models/plugin");
  const db = require("@saltcorn/data/db");
  const { getState } = require("@saltcorn/data/db/state");
  const me = await findMe();
  if (!me) throw new Error("plugin dysizz-ui introuvable");
  me.configuration = { ...(me.configuration || {}), ...patch };
  await me.upsert();
  await Plugin.loadPlugin(me);
  try {
    const st = getState();
    if (st.computeAssetsByRole) await st.computeAssetsByRole();
    st.processSend && st.processSend({ refresh_plugin_cfg: me.name, tenant: db.getTenantSchema() });
  } catch (e) {
    /* pas bloquant */
  }
  return me.configuration;
};

module.exports = { findMe, getCfg, patchCfg };
