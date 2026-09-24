/* dysizz-ui — constantes et petits utilitaires partagés */
"use strict";

const PLUGIN = "dysizz-ui";
/* injecté par tools/build.mjs (esbuild --define) */
const VERSION = typeof __DZ_VERSION__ !== "undefined" ? __DZ_VERSION__ : "dev";
/* le numéro de version dans l'URL casse le cache navigateur à chaque mise à jour */
const pub = (file) => `/dysizz-ui/a/${VERSION}/${file}`;
const isAdmin = (req) => !!(req.user && req.user.role_id === 1);
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
const post = (req) => req.body || {};
const slug = (s) => String(s).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "bloc";
const denied = (res) => res.status(403).send("Réservé aux administrateurs");

module.exports = { PLUGIN, VERSION, pub, isAdmin, esc, post, slug, denied };
