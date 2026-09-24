/* =====================================================================
   Accueil Dysizz — « écran de démarrage » façon Windows 8.
   /dysizz : une tuile par endroit utile, rangées par groupes :
     - les applis et solutions (Me…), avec des infos en direct ;
     - les outils Dysizz (kit UI, blocs workflow…) ;
     - l'administration Saltcorn (tables, vues, pages, événements…).
   Chaque plugin peut apporter ses tuiles en exportant :
     dysizz_hub: (req) => [{ group, label, sub, url, icon, color, size, live, min_role }]
   size : "s" petite, "m" moyenne, "w" large, "l" grande.
   live : async (req) => ({ n: 3, text: "3 en erreur" }) (affiché sur la tuile).
   ===================================================================== */
"use strict";
const { esc, isAdmin, PLUGIN, VERSION } = require("./core");

const C = { blue: "#0063b1", sky: "#2d89ef", teal: "#00aba9", green: "#1e7145", lime: "#00a300", orange: "#e3a21a", red: "#b91d47", magenta: "#9f00a7", purple: "#603cba", violet: "#7e3878", slate: "#3a4a5c", brown: "#8a5a2b", pink: "#e3008c" };
const GROUP_ORDER = ["Mes applis", "Outils Dysizz", "Workflows", "Administration Saltcorn", "Mes pages"];

/* tuiles natives : l'administration de Saltcorn, en français */
const saltcornTiles = (req) => {
  if (!isAdmin(req)) return [];
  const g = "Administration Saltcorn";
  const multi = (() => { try { return require("@saltcorn/data/db").is_it_multi_tenant() && require("@saltcorn/data/db").getTenantSchema() === "public"; } catch (e) { return false; } })();
  return [
    { group: g, label: "Tables", sub: "tes données", url: "/table", icon: "fas fa-table", color: C.blue, size: "m" },
    { group: g, label: "Vues", url: "/viewedit", icon: "fas fa-eye", color: C.sky, size: "s" },
    { group: g, label: "Pages", url: "/pageedit", icon: "fas fa-file", color: C.teal, size: "s" },
    { group: g, label: "Événements", sub: "déclencheurs et workflows", url: "/actions", icon: "fas fa-bolt", color: C.orange, size: "m" },
    { group: g, label: "Modules", url: "/plugins", icon: "fas fa-cubes", color: C.purple, size: "s" },
    { group: g, label: "Utilisateurs", url: "/useradmin", icon: "fas fa-users", color: C.green, size: "s" },
    { group: g, label: "Fichiers", url: "/files", icon: "fas fa-folder-open", color: C.brown, size: "s" },
    { group: g, label: "Menu", url: "/menu", icon: "fas fa-bars", color: C.slate, size: "s" },
    { group: g, label: "Paramètres", url: "/settings", icon: "fas fa-cog", color: C.slate, size: "w", sub: "site, thème, e-mail, sécurité" },
    { group: g, label: "Sauvegardes", url: "/admin/backup", icon: "fas fa-life-ring", color: C.red, size: "s" },
    { group: g, label: "Erreurs", url: "/crashlog", icon: "fas fa-bug", color: C.red, size: "s", live: liveCrashes },
    ...(multi ? [{ group: g, label: "Tenants", url: "/tenant/list", icon: "fas fa-sitemap", color: C.magenta, size: "s" }] : []),
  ];
};
const liveCrashes = async () => {
  const Crash = require("@saltcorn/data/models/crash");
  const n = (await Crash.find({ occur_at: { gt: new Date(Date.now() - 864e5) } }, { limit: 100 }).catch(() => [])).length;
  return n ? { n, text: `${n} sur 24 h` } : { text: "rien sur 24 h" };
};

const uiTiles = (req) => (isAdmin(req) ? [
  { group: "Outils Dysizz", label: "Kit UI", sub: "design, familles de blocs, pages de démo", url: "/dysizz-ui", icon: "fas fa-palette", color: C.pink, size: "w" },
  { group: "Outils Dysizz", label: "Galerie", sub: "tous les blocs", url: "/dysizz-ui/galerie?f=all", icon: "fas fa-th-large", color: C.magenta, size: "s" },
  { group: "Outils Dysizz", label: "Atelier UI", url: "/dysizz-ui/blocks", icon: "fas fa-pencil-ruler", color: C.violet, size: "s" },
  { group: "Outils Dysizz", label: "Classes", url: "/dysizz-ui/classes", icon: "fas fa-code", color: C.purple, size: "s" },
  { group: "Outils Dysizz", label: "Réglages du thème", url: "/plugins/configure/dysizz-ui", icon: "fas fa-sliders-h", color: C.slate, size: "s" },
] : []);

/* les pages du site que l'utilisateur peut ouvrir (sans les pages de démo du kit) */
const pageTiles = async (req) => {
  try {
    const Page = require("@saltcorn/data/models/page");
    const role = req.user ? req.user.role_id : 100;
    const pages = (await Page.find({}, { orderBy: "name" })).filter((p) => role <= p.min_role && !/^dz-/.test(p.name));
    const palette = [C.blue, C.teal, C.green, C.orange, C.purple, C.sky, C.brown, C.violet];
    return pages.slice(0, 24).map((p, i) => ({ group: "Mes pages", label: p.title || p.name, url: `/page/${encodeURIComponent(p.name)}`, icon: "far fa-file-alt", color: palette[i % palette.length], size: "s" }));
  } catch (e) { return []; }
};

/* tuiles apportées par les autres plugins */
const pluginTiles = async (req) => {
  let st;
  try { st = require("@saltcorn/data/db/state").getState(); } catch (e) { return []; }
  const out = [];
  for (const [name, p] of Object.entries((st && st.plugins) || {})) {
    if (!p || name === PLUGIN || !p.dysizz_hub) continue;
    try {
      const list = typeof p.dysizz_hub === "function" ? await p.dysizz_hub(req) : p.dysizz_hub;
      for (const t of list || []) if (t && t.label && t.url) out.push({ ...t, plugin: name });
    } catch (e) { /* une extension en panne ne casse pas l'accueil */ }
  }
  return out;
};

const withLive = async (tiles, req) => Promise.all(tiles.map(async (t) => {
  if (typeof t.live !== "function") return t;
  try { return { ...t, info: await Promise.race([t.live(req), new Promise((r) => setTimeout(() => r(null), 900))]) }; } catch (e) { return t; }
}));

const collect = async (req) => {
  const role = req.user ? req.user.role_id : 100;
  const all = [...(await pluginTiles(req)), ...uiTiles(req), ...saltcornTiles(req), ...(await pageTiles(req))]
    .filter((t) => role <= (t.min_role || 100) || (t.min_role === undefined));
  const tiles = await withLive(all, req);
  const groups = new Map();
  for (const t of tiles) { if (!groups.has(t.group)) groups.set(t.group, []); groups.get(t.group).push(t); }
  return [...groups.entries()].sort((a, b) => ((GROUP_ORDER.indexOf(a[0]) + 1) || 50) - ((GROUP_ORDER.indexOf(b[0]) + 1) || 50));
};

const SAFE_COLOR = /^(#[0-9a-f]{3,8}|[a-z]{3,20})$/i;
const tileHtml = (t) => {
  const size = ["s", "m", "w", "l"].includes(t.size) ? t.size : "s";
  const color = SAFE_COLOR.test(t.color || "") ? t.color : C.blue;
  const info = t.info && (t.info.text || t.info.n !== undefined) ? `<span class="t-live">${t.info.n !== undefined && size === "s" ? esc(t.info.n) : esc(t.info.text || t.info.n)}</span>` : "";
  const badge = t.info && t.info.n && size !== "s" ? `<span class="t-badge">${esc(t.info.n)}</span>` : "";
  return `<a class="tile t-${size}" href="${esc(t.url)}" title="${esc(t.label + (t.sub ? " — " + t.sub : ""))}" aria-label="${esc(t.label)}" style="--c:${color}" data-k="${esc((t.label + " " + (t.sub || "") + " " + t.group).toLowerCase())}">
<i class="${esc(t.icon || "fas fa-square")}"></i>${badge}${info}
<span class="t-name">${esc(t.label)}</span>${t.sub && size !== "s" ? `<span class="t-sub">${esc(t.sub)}</span>` : ""}</a>`;
};

const CSS = `
#dzhub,#dzhub *{box-sizing:border-box}
#dzhub{position:fixed;inset:0;z-index:5000;overflow:auto;--bg1:#1b1f3b;--bg2:#2b1c4a;--ink:#fff;--mute:rgba(255,255,255,.7);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif;color:var(--ink);background:radial-gradient(1200px 700px at 10% -10%,#3b2b8f 0,transparent 60%),radial-gradient(900px 600px at 110% 110%,#0b5e7a 0,transparent 55%),linear-gradient(135deg,var(--bg1),var(--bg2));overflow-x:hidden}
#dzhub.light{--bg1:#e9eef6;--bg2:#f5f0fb;--ink:#141824;--mute:rgba(20,24,36,.65);background:radial-gradient(1000px 600px at 0 0,#dfe7ff 0,transparent 60%),linear-gradient(135deg,var(--bg1),var(--bg2))}
#dzhub a{color:inherit;text-decoration:none}
#dzhub header{display:flex;align-items:center;gap:1rem;padding:28px 48px 8px;flex-wrap:wrap}
#dzhub h1{font-weight:300;font-size:2.6rem;margin:0;letter-spacing:.01em}
#dzhub .who{margin-left:auto;display:flex;align-items:center;gap:.9rem;color:var(--mute)}
#dzhub .who b{color:var(--ink);font-weight:400;font-size:1.05rem}
#dzhub .av{width:40px;height:40px;border-radius:4px;background:rgba(255,255,255,.18);display:grid;place-items:center;font-weight:600}
#dzhub .clock{font-weight:200;font-size:1.6rem;color:var(--ink)}
#dzhub .btn{border:0;background:rgba(255,255,255,.12);color:var(--ink);padding:.45rem .8rem;font:inherit;font-size:.85rem;cursor:pointer}
#dzhub .btn:hover{background:rgba(255,255,255,.22)}#dzhub.light .btn{background:rgba(0,0,0,.07)}
#dzhub .search{width:min(420px,100%);padding:.6rem .9rem;border:0;outline:2px solid transparent;background:rgba(255,255,255,.14);color:var(--ink);font:inherit;font-size:1rem}
#dzhub.light .search{background:rgba(0,0,0,.06)}.search::placeholder{color:var(--mute)}.search:focus{outline-color:rgba(255,255,255,.5)}
#dzhub .bar{padding:0 48px 12px;display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
#dzhub main{display:flex;gap:56px;padding:18px 48px 48px;overflow-x:auto;align-items:flex-start;min-height:calc(100vh - 150px);scrollbar-width:thin}
#dzhub .group h2{font-weight:300;font-size:1.25rem;margin:0 0 14px;color:var(--ink);white-space:nowrap}
#dzhub .grid{display:grid;grid-template-columns:repeat(6,72px);grid-auto-rows:72px;gap:8px;grid-auto-flow:row dense}
#dzhub .tile{position:relative;background:var(--c);color:#fff;display:block;overflow:hidden;transition:transform .12s ease,box-shadow .12s ease,outline-color .12s;outline:2px solid transparent;outline-offset:-2px;animation:in .35s cubic-bezier(.2,.8,.2,1) both}
#dzhub .tile:hover{outline-color:rgba(255,255,255,.55)}#dzhub .tile:active{transform:scale(.96)}
#dzhub .tile:focus-visible{outline-color:#fff}
#dzhub .t-s{grid-column:span 1;grid-row:span 1}#dzhub .t-m{grid-column:span 2;grid-row:span 2}#dzhub .t-w{grid-column:span 4;grid-row:span 2}#dzhub .t-l{grid-column:span 4;grid-row:span 4}
#dzhub .tile i{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);font-size:26px;opacity:.95}
#dzhub .t-s i{font-size:22px;top:50%}#dzhub .t-m i{font-size:32px}#dzhub .t-w i{font-size:34px;left:24%}#dzhub .t-l i{font-size:56px;top:40%}
#dzhub .t-name{position:absolute;left:8px;bottom:6px;right:8px;font-size:.82rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#dzhub .t-s .t-name{display:none}
#dzhub .t-sub{position:absolute;left:44%;right:10px;top:50%;transform:translateY(-50%);font-size:.82rem;line-height:1.3;opacity:.9}
#dzhub .t-m .t-sub,#dzhub .t-l .t-sub{display:none}
#dzhub .t-live{position:absolute;right:8px;top:6px;font-size:.78rem;opacity:.95}
#dzhub .t-s .t-live{top:auto;bottom:4px;right:6px;font-size:.72rem;font-weight:600}
#dzhub .t-badge{position:absolute;right:8px;bottom:6px;font-size:1.4rem;font-weight:300}
#dzhub .t-l .t-live{position:absolute;left:10px;right:10px;top:auto;bottom:34px;font-size:.95rem}
#dzhub .hide{display:none!important}
#dzhub .empty{color:var(--mute);padding:2rem 48px}
@keyframes in{from{opacity:0;transform:translateX(24px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#dzhub .tile{animation:none}}
@media (max-width:760px){#dzhub header{padding:20px 16px 6px}#dzhub h1{font-size:2rem}#dzhub .bar{padding:0 16px 10px}#dzhub main{flex-direction:column;padding:12px 16px 40px;gap:28px;overflow:visible}
#dzhub .grid{grid-template-columns:repeat(4,1fr);grid-auto-rows:calc((100vw - 32px - 24px)/4)}#dzhub .who .clock{display:none}#dzhub .t-w,#dzhub .t-l{grid-column:span 4}}
`;

const JS = `
(function(){
 var H=document.getElementById('dzhub');document.documentElement.style.overflow='hidden';var q=document.getElementById('q'),tiles=[].slice.call(document.querySelectorAll('.tile'));
 function f(){var v=q.value.toLowerCase().trim();tiles.forEach(function(t){t.classList.toggle('hide',!!v&&t.dataset.k.indexOf(v)<0)});
  [].forEach.call(document.querySelectorAll('.group'),function(g){g.classList.toggle('hide',!g.querySelector('.tile:not(.hide)'))});}
 q.addEventListener('input',f);
 q.addEventListener('keydown',function(e){if(e.key==='Enter'){var t=document.querySelector('.tile:not(.hide)');if(t)location.href=t.href}});
 document.addEventListener('keydown',function(e){if(document.activeElement!==q&&e.key.length===1&&!e.ctrlKey&&!e.metaKey&&!e.altKey){q.focus()}});
 var m=document.querySelector('main');m.addEventListener('wheel',function(e){if(window.innerWidth>760&&Math.abs(e.deltaY)>Math.abs(e.deltaX)&&m.scrollWidth>m.clientWidth){m.scrollLeft+=e.deltaY;e.preventDefault()}},{passive:false});
 function tick(){var d=new Date(),c=document.getElementById('clock');if(c)c.textContent=d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'})}tick();setInterval(tick,15000);
 try{if(localStorage.getItem('dzHub')==='light')H.classList.add('light')}catch(e){}
 document.getElementById('th').addEventListener('click',function(){var l=H.classList.toggle('light');try{localStorage.setItem('dzHub',l?'light':'dark')}catch(e){}});
})();`;

const hubPage = async (req, res) => {
  if (!req.user) return res.redirect(`/auth/login?dest=${encodeURIComponent("/dysizz")}`);
  const groups = await collect(req);
  const name = (req.user.email || "").split("@")[0];
  const date = new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const homeForm = isAdmin(req) ? `<form method="post" action="/dysizz/home" style="display:inline"><input type="hidden" name="_csrf" value="${esc(csrf)}"><button class="btn" title="Cet écran s'ouvre après la connexion des administrateurs">Ouvrir ici à la connexion</button></form>` : "";
  res.set("Cache-Control", "no-store");
  /* rendu dans la page Saltcorn (thème, icônes), mais en plein écran par-dessus */
  const html = `<style>${CSS}</style><div id="dzhub">
<header><h1>Accueil</h1><div class="who"><span class="clock" id="clock"></span><span><b>${esc(name)}</b><br><small>${esc(date)}</small></span><span class="av">${esc(name.slice(0, 1).toUpperCase())}</span></div></header>
<div class="bar"><input id="q" class="search" type="search" placeholder="Tape pour chercher (ex. mails, tables, workflows)…" autocomplete="off">
<button class="btn" id="th" type="button">Clair / sombre</button>${homeForm}<a class="btn" href="/auth/logout">Déconnexion</a></div>
<main>${groups.map(([g, ts]) => `<section class="group"><h2>${esc(g)}</h2><div class="grid">${ts.map(tileHtml).join("")}</div></section>`).join("") || '<p class="empty">Rien à afficher pour ton compte.</p>'}</main></div>
<script>${JS}</script>`;
  res.sendWrap({ title: "Accueil", requestFluidLayout: true }, { above: [{ type: "blank", isHTML: true, contents: html.replace(/\{\{/g, "&#123;&#123;") }] });
};

/* « Ouvrir ici à la connexion » : une page Saltcorn « dysizz-accueil » qui renvoie ici,
   choisie comme page d'accueil des administrateurs */
const setHome = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Page = require("@saltcorn/data/models/page");
  const { getState } = require("@saltcorn/data/db/state");
  const name = "dysizz-accueil";
  const layout = { type: "blank", contents: '<script>location.replace("/dysizz")</script><p><a href="/dysizz">Accueil</a></p>', isHTML: true };
  const ex = Page.findOne({ name });
  if (!ex) await Page.create({ name, title: "Accueil", description: "Renvoie vers l'accueil Dysizz (/dysizz)", min_role: 1, layout, fixed_states: {} });
  const st = getState();
  const cur = { ...(st.getConfig("home_page_by_role", {}) || {}) };
  cur[1] = name;
  await st.setConfig("home_page_by_role", cur);
  res.redirect("/dysizz");
};

/* une entrée « Accueil » en tête du menu Saltcorn, ajoutée une seule fois */
const MENU = { type: "Link", text: "Accueil", label: "Accueil", url: "/dysizz", href: "/dysizz", icon: "fas fa-th-large", min_role: 1, max_role: "1", style: "", title: "", tooltip: "", target: "_self", target_blank: false, in_modal: false, location: "Standard", shortcut: "", disable_on_mobile: false };
/* Saltcorn affiche « unrolled_menu_items » s'il existe (menu déplié), sinon « menu_items » :
   on ajoute l'entrée aux deux */
const ensureMenu = async () => {
  try {
    const { getState } = require("@saltcorn/data/db/state");
    const st = getState();
    for (const key of ["menu_items", "unrolled_menu_items"]) {
      const items = st.getConfig(key, null);
      if (!Array.isArray(items) || (key === "unrolled_menu_items" && !items.length)) continue;
      const i = items.findIndex((x) => x && (x.url === "/dysizz" || x.href === "/dysizz"));
      if (i >= 0 && items[i].text) continue;
      await st.setConfig(key, [MENU, ...items.filter((_, k) => k !== i)]);
    }
  } catch (e) { /* pas bloquant */ }
};

module.exports = { hubPage, setHome, ensureMenu, collect, VERSION };
