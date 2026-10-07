/* Pièce jointe d'une fiche : seul un champ Fichier, seulement si on peut écrire dans la table,
   types et taille bornés, fichier lisible par les administrateurs et son auteur. Données fictives. */
"use strict";
const assert = require("node:assert/strict");
const Module = require("node:module");

let enregistre = null;
const TABLES = {
  ticket: { name: "ticket", min_role_write: 40, ownership_field_id: 7,
    getFields: () => [{ id: 7, name: "demandeur", type: "Key" }, { name: "titre", type: { name: "String" } }, { name: "piece_jointe", type: { name: "File" } }] },
  journal: { name: "journal", min_role_write: 1, getFields: () => [{ name: "piece_jointe", type: { name: "File" } }] },
};
const original = Module._load;
Module._load = function (n, ...rest) {
  if (n === "@saltcorn/data/models/table") return { findOne: ({ name }) => TABLES[name] || null };
  if (n === "@saltcorn/data/models/file") return {
    from_req_files: async (f, user_id, min_role_read) => { enregistre = { f, user_id, min_role_read }; return { filename: f.name, path_to_serve: f.name }; },
    fieldValueFromRelative: (p) => p,
  };
  return original.call(this, n, ...rest);
};
const { envoyer, typeDe } = require("../src/fiche");

const appel = async (table, champ, user, file) => {
  let code = 200, corps = null;
  const res = { status: (c) => { code = c; return res; }, json: (j) => { corps = j; return res; } };
  await envoyer({ params: { table, champ }, user, files: file ? { file } : undefined }, res);
  return { code, corps };
};
const fichier = (name, mimetype, size = 1000) => ({ name, mimetype, size, truncated: false });
const user = { id: 12, role_id: 80 };

(async () => {
  assert.equal(typeDe({ name: "piece_jointe", type: { name: "File" } }), "fichier");
  assert.equal((await appel("ticket", "titre", user, fichier("a.png", "image/png"))).code, 400, "champ texte : refusé");
  assert.equal((await appel("journal", "piece_jointe", user, fichier("a.png", "image/png"))).code, 403, "table sans droit d'écriture : refusé");
  assert.equal((await appel("ticket", "piece_jointe", null, fichier("a.png", "image/png"))).code, 401);
  assert.equal((await appel("ticket", "piece_jointe", user, fichier("page.html", "text/html"))).code, 415, "HTML refusé");
  assert.equal((await appel("ticket", "piece_jointe", user, fichier("page.pdf", "text/html"))).code, 415, "type annoncé incohérent refusé");
  assert.equal((await appel("ticket", "piece_jointe", user, fichier("gros.pdf", "application/pdf", 11 * 1024 * 1024))).code, 413);
  assert.equal(enregistre, null, "rien n'est enregistré tant que c'est refusé");
  const ok = await appel("ticket", "piece_jointe", user, fichier("capture.png", "image/png"));
  assert.equal(ok.code, 200); assert.equal(ok.corps.valeur, "capture.png");
  assert.equal(enregistre.user_id, 12); assert.equal(enregistre.min_role_read, 1, "lisible par les administrateurs (et l'auteur)");
  console.log("fiche — pièce jointe OK");
})().catch((e) => { console.error(e); process.exitCode = 1; });
