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
const textBody = (t) => {
  const lines = String(t).replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n").split("\n");
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

module.exports = { dz_mail, frameDoc, clean };
