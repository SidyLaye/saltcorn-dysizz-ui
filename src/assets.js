/* dysizz-ui — fichiers du kit (CSS, JS, packs) servis depuis la mémoire */
"use strict";
const { VERSION } = require("./core");
/* Les fichiers sont servis par une route du plugin (et pas par /plugins/public)
   pour ne dépendre d'aucun dossier copié par l'installeur de Saltcorn. */
const ASSETS = {
  "dz-core.css": "text/css; charset=utf-8",
  "dz-skin.css": "text/css; charset=utf-8",
  "dz-builder.css": "text/css; charset=utf-8",
  "dz.js": "application/javascript; charset=utf-8",
  "dz-smooth.js": "application/javascript; charset=utf-8",
  "dz-editor.js": "application/javascript; charset=utf-8",
};
/* Tout le kit (CSS, JS, blocs, pages) est embarqué dans index.js par
   tools/build.mjs : le plugin ne dépend d'aucun autre fichier sur le disque
   du serveur. */
const EMBED = require("./generated/embed.js");
/* compression faite une seule fois par fichier (brotli + gzip), puis servie
   depuis la mémoire : zéro calcul par requête, même avec des milliers de visiteurs */
const zlib = require("zlib");
const packed = {};
const getPacked = (file) => {
  if (!packed[file]) {
    const src = typeof EMBED[file] === "string" ? EMBED[file] : JSON.stringify(EMBED[file]);
    const raw = Buffer.from(src, "utf8");
    packed[file] = {
      raw,
      br: zlib.brotliCompressSync(raw, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: raw.length > 400000 ? 9 : 11 } }),
      gz: zlib.gzipSync(raw, { level: 9 }),
    };
  }
  return packed[file];
};
const serveAsset = (req, res) => {
  const file = req.params.file;
  const type = ASSETS[file] || (/^dz-f-[a-z]+\.css$/.test(file) ? "text/css; charset=utf-8" : /^classes-[a-z0-9-]+\.json$/.test(file) ? "application/json; charset=utf-8" : /^dz-editor[a-z-]*\.js$/.test(file) ? "application/javascript; charset=utf-8" : null);
  if (!type || EMBED[file] === undefined) return res.status(404).send("Not found");
  const etag = `"dz-${VERSION}-${file}"`;
  /* un fichier du kit n'est propre à personne : pas de cookie de session
     (sinon aucun cache partagé ne peut le garder) */
  const setHeader = res.setHeader.bind(res);
  res.setHeader = (k, v) => (String(k).toLowerCase() === "set-cookie" ? res : setHeader(k, v));
  res.set("Content-Type", type);
  res.set("Vary", "Accept-Encoding");
  res.set("ETag", etag);
  res.set("Cache-Control", req.params.ver === VERSION ? "public, max-age=31536000, immutable" : "no-cache");
  if (req.headers["if-none-match"] === etag) return res.status(304).end();
  const p = getPacked(file);
  const ae = String(req.headers["accept-encoding"] || "");
  if (/\bbr\b/.test(ae)) { res.set("Content-Encoding", "br"); return res.end(p.br); }
  if (/\bgzip\b/.test(ae)) { res.set("Content-Encoding", "gzip"); return res.end(p.gz); }
  return res.end(p.raw);
};

const readPack = (file) => EMBED[file];

module.exports = { ASSETS, EMBED, serveAsset, readPack };
