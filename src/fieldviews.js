/* Affichages de champs (fieldviews) ajoutés par dysizz-ui.
   « dz_mail » : le corps d'un e-mail, lisible et sûr.
     - HTML : affiché dans un cadre isolé (sandbox, aucun script), images
       distantes bloquées par défaut (pixels espions) avec un bouton pour les afficher,
       liens ouverts dans un nouvel onglet ;
     - texte : retours à la ligne gardés, liens cliquables, citations (« > ») atténuées. */
"use strict";
const { esc } = require("./core");

const looksHtml = (s) => /<\s*(html|body|div|p|table|br|span|a|img|td)\b/i.test(s);
const clean = (h) => String(h)
  .replace(/<(script|noscript|iframe|object|embed|applet|frameset|frame|form)\b[\s\S]*?<\/\1\s*>/gi, "")
  .replace(/<(script|iframe|object|embed|form|frame|frameset|applet|base|meta|link)\b[\s\S]*?(<\/\1\s*>|\/?>)/gi, "")
  .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, "")
  .replace(/(href|src|action|formaction)\s*=\s*(["']?)\s*(javascript|vbscript|data:text\/html)[^"'\s>]*/gi, "$1=$2#");

const CSP = (imgs) => `default-src 'none'; style-src 'unsafe-inline'; font-src data:; img-src data: cid:${imgs ? " https: http:" : ""}`;
const frameDoc = (html, imgs) => `<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="${CSP(imgs)}"><base target="_blank">
<style>html,body{margin:0;padding:0}body{font:15px/1.6 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#1c1f26;background:#fff;padding:4px 2px;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{max-width:100%!important}a{color:#2b59c3}blockquote{margin:0 0 0 .6em;padding-left:.8em;border-left:3px solid #d6d9e0;color:#5b6070}pre{white-space:pre-wrap}
body:not(.dz-all) .gmail_quote,body:not(.dz-all) blockquote[type=cite],body:not(.dz-all) .yahoo_quoted,body:not(.dz-all) #divRplyFwdMsg,body:not(.dz-all) #divRplyFwdMsg~*,body:not(.dz-all) #appendonsend~*,body:not(.dz-all) .moz-cite-prefix,body:not(.dz-all) .moz-cite-prefix+blockquote{display:none!important}</style></head><body>${html}</body></html>`;

const linkify = (t) => esc(t).replace(/(https?:\/\/[^\s<]+[^\s<.,;:!?)\]'"])/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
/* l'historique (réponses citées) est replié : on lit d'abord le nouveau message */
const HIST = /^(>|(Le |On ).{6,160}(a écrit|wrote)\s*:?\s*$|-{2,}\s*(Original Message|Message d'origine|Forwarded message|Message transféré)|(De|From)\s*:\s.+@)/i;
/* texte arrivé « à plat » (retours à la ligne perdus) : on remet une ligne
   avant « Le … a écrit : », avant chaque niveau de citation « > », avant « De : … @ » */
const unflatten = (t) => {
  const s = String(t);
  if (s.length < 400 || (s.match(/\n/g) || []).length > s.length / 400) return s;
  return s
    .replace(/\s((?:Le |On )(?:lun|mar|mer|jeu|ven|sam|dim|mon|tue|wed|thu|fri|sat|sun|\d)[^\n]{4,200}?(?:a écrit|wrote)\s*:)\s*/gi, "\n$1\n")
    .replace(/\s(\*?(?:De|From)\s*:\*?\s[^\n]{0,80}?@)/g, "\n$1")
    .replace(/[ \t]+(>(?:[ \t]*>)*)[ \t]+/g, "\n$1 ");
};
const textBody = (t) => {
  const lines = unflatten(t).replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n").split("\n");
  const cut = lines.findIndex((l, i) => i > 0 && HIST.test(l.trim()));
  const fmt = (ls) => ls.map((l) => (/^\s*>/.test(l) ? `<span class="q">${linkify(l)}</span>` : linkify(l))).join("\n");
  if (cut < 0) return `<div class="dzv-mailtext">${fmt(lines)}</div>`;
  const rest = lines.slice(cut);
  return `<div class="dzv-mailtext">${fmt(lines.slice(0, cut)).replace(/\s+$/, "")}</div><details class="dzv-mailhist"><summary>Afficher l'historique (${rest.length} lignes)</summary><div class="dzv-mailtext">${fmt(rest)}</div></details>`;
};

const dz_mail = {
  type: "String",
  isEdit: false,
  description: "Corps d'e-mail : HTML isolé et sûr, ou texte lisible",
  configFields: [{ name: "images", label: "Afficher les images distantes sans demander", type: "Bool" }],
  run: (v, req, attrs = {}) => {
    const s = String(v == null ? "" : v);
    if (!s.trim()) return '<div class="dzv-mailtext dzv-muted">(message vide)</div>';
    if (!looksHtml(s)) return textBody(s);
    const body = clean(s).slice(0, 400000);
    const hasRemote = /<img[^>]+src\s*=\s*["']?https?:/i.test(body);
    const imgs = !!attrs.images;
    return `<div class="dzv-mailframe">${hasRemote && !imgs ? `<div class="dzv-mailimg"><i class="far fa-image"></i> Images distantes masquées (elles peuvent servir à te suivre). <button type="button" data-dzv-mailimg>Afficher les images</button></div>` : ""}
<button type="button" class="dzv-mailhist-btn" data-dzv-mailhist hidden>Afficher l'historique</button><iframe sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox" referrerpolicy="no-referrer" loading="lazy" title="Contenu du mail" srcdoc="${esc(frameDoc(body, imgs))}"></iframe></div>`;
  },
};

/* ---------- champs interactifs : s'appuient sur les widgets du kit (chargés à la demande) ---------- */
const ea = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const hidden = (nm, v) => `<input type="hidden" name="${ea(nm)}" value="${ea(v)}">`;
const widget = (name, data, inner = "") => `<div data-dz-widget="${name}"${Object.entries(data).map(([k, v]) => (v === undefined || v === null || v === "" ? "" : ` data-${k}="${ea(typeof v === "object" ? JSON.stringify(v) : v)}"`)).join("")}>${inner}</div>`;
const H = { name: "hauteur", label: "Hauteur (px)", type: "Integer" };
const edit = (name, description, render, configFields = []) => ({ type: "String", isEdit: true, description, configFields, run: (nm, v, attrs = {}) => render(nm, v ?? "", attrs) });
const show = (name, description, render, configFields = []) => ({ type: "String", isEdit: false, description, configFields, run: (v, req, attrs = {}) => render(v ?? "", attrs) });

const dz_signature_saisie = edit("signature", "Signature au doigt ou à la souris (image PNG enregistrée dans le champ)", (nm, v, a) => hidden(nm, v) + widget("signature", { champ: nm, hauteur: a.hauteur }), [H]);
const dz_signature = show("signature", "Affiche la signature", (v) => (String(v).startsWith("data:image/") ? `<img src="${ea(v)}" alt="signature" style="max-width:100%;max-height:140px;background:#fff">` : '<span class="text-muted">—</span>'));
const dz_position_carte = edit("carte", "Choisir une position sur une carte (« lat,lon »)", (nm, v, a) => hidden(nm, v) + widget("carte", { mode: "choisir", champ: nm, hauteur: a.hauteur || 320, zoom: a.zoom }), [H, { name: "zoom", label: "Zoom de départ", type: "Integer" }]);
const dz_carte = show("carte", "Petite carte avec le point (champ « lat,lon »)", (v, a) => (/-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?/.test(v) ? widget("carte", { points: [{ position: v }], hauteur: a.hauteur || 220, zoom: 14 }) : '<span class="text-muted">—</span>'), [H]);
const dz_tableur_saisie = edit("tableur", "Petit tableur avec formules (enregistré en JSON)", (nm, v, a) => hidden(nm, v) + widget("tableur", { champ: nm, hauteur: a.hauteur, lignes: a.lignes, colonnes: a.colonnes }), [H, { name: "lignes", label: "Lignes", type: "Integer" }, { name: "colonnes", label: "Colonnes", type: "Integer" }]);
const dz_tableur = show("tableur", "Tableur en lecture", (v, a) => widget("tableur", { lecture: "true", valeur: v, hauteur: a.hauteur }), [H]);
const dz_tableau_blanc = edit("tableau-blanc", "Tableau blanc (dessins, formes, post-it) enregistré dans le champ", (nm, v, a) => hidden(nm, v) + widget("tableau-blanc", { champ: nm, hauteur: a.hauteur }), [H]);
const dz_tableau_blanc_vue = show("tableau-blanc", "Tableau blanc (modifs non enregistrées)", (v, a) => widget("tableau-blanc", { hauteur: a.hauteur }, `<input type="hidden" value="${ea(v)}">`), [H]);
const dz_3d_modeleur = edit("3d", "Modeleur 3D (scène enregistrée dans le champ)", (nm, v, a) => hidden(nm, v) + widget("3d", { mode: "modeleur", champ: nm, hauteur: a.hauteur }), [H]);
const dz_3d = show("3d", "Visionneuse 3D : scène du modeleur ou adresse d'un fichier .glb/.gltf/.stl/.obj", (v, a) => widget("3d", { src: v, hauteur: a.hauteur || 320, rotation: a.rotation === false ? "false" : "" }), [H, { name: "rotation", label: "Tourner tout seul", type: "Bool" }]);
const dz_scanner = edit("scanner", "Champ texte + bouton pour scanner un QR code / code-barres", (nm, v, a) => `<input type="text" class="form-control mb-2" name="${ea(nm)}" value="${ea(v)}"${a.placeholder ? ` placeholder="${ea(a.placeholder)}"` : ""}>` + widget("scanner", { champ: nm }), [{ name: "placeholder", label: "Texte d'aide", type: "String" }]);
const dz_photo = edit("photo", "Prendre une photo avec la caméra (image enregistrée dans le champ)", (nm, v) => hidden(nm, v) + widget("scanner", { mode: "photo", champ: nm }) + (String(v).startsWith("data:image/") ? `<img src="${ea(v)}" alt="" style="max-width:160px;margin-top:6px;border-radius:8px">` : ""));
const dz_image = show("photo", "Affiche une image enregistrée dans le champ (data:image…)", (v, a) => (String(v).startsWith("data:image/") || /^https?:\/\//.test(v) ? `<img src="${ea(v)}" alt="" style="max-width:100%;${a.hauteur ? `max-height:${+a.hauteur}px;` : ""}border-radius:8px">` : '<span class="text-muted">—</span>'), [H]);

const PAL = { name: "palette", label: "Types d'étapes (JSON, facultatif)", type: "String", sublabel: "Liste de { cle, type, label, icone, couleur, champs, branches }. Vide : Début, Étape, Condition, Validation, Fin." };
const dz_parcours_saisie = edit("parcours", "Éditeur de parcours : étapes reliées par des flèches (enregistré en JSON)", (nm, v, a) => hidden(nm, v) + widget("parcours", { champ: nm, hauteur: a.hauteur, palette: a.palette }), [H, PAL]);
const dz_parcours = show("parcours", "Parcours en lecture (déplacement et zoom), étapes passées mises en valeur", (v, a) => widget("parcours", { lecture: "true", valeur: v, hauteur: a.hauteur || 360, palette: a.palette }), [H, PAL]);

const WIDGET_FIELDVIEWS = { dz_parcours_saisie, dz_parcours, dz_signature_saisie, dz_signature, dz_position_carte, dz_carte, dz_tableur_saisie, dz_tableur, dz_tableau_blanc, dz_tableau_blanc_vue, dz_3d_modeleur, dz_3d, dz_scanner, dz_photo, dz_image };

module.exports = { dz_mail, frameDoc, clean, WIDGET_FIELDVIEWS };
