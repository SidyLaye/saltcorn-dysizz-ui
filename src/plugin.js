/* =====================================================================
   dysizz-ui — plugin Saltcorn
   - charge le design system (CSS + JS) sur toutes les pages du tenant
   - réglages par tenant : couleurs, polices, arrondis, style, options
   - page d'admin /dysizz-ui : installe / met à jour les blocs de la
     Library du builder et les pages de démo
   Testé contre le code de Saltcorn 1.6.2.
   ===================================================================== */
const Workflow = require("@saltcorn/data/models/workflow");
const Form = require("@saltcorn/data/models/form");

const PLUGIN = "dysizz-ui";
const VERSION = /*__VERSION__*/ "0.0.0";
/* le numéro de version dans l'URL casse le cache navigateur à chaque mise à jour */
const pub = (file) => `/dysizz-ui/a/${VERSION}/${file}`;
/* Les fichiers sont servis par une route du plugin (et pas par /plugins/public)
   pour ne dépendre d'aucun dossier copié par l'installeur de Saltcorn. */
const ASSETS = {
  "dz-core.css": "text/css; charset=utf-8",
  "dz-skin.css": "text/css; charset=utf-8",
  "dz.js": "application/javascript; charset=utf-8",
};
/* Tout le kit (CSS, JS, blocs, pages) est embarqué dans ce fichier par
   tools/build_index.py : le plugin ne dépend d'aucun autre fichier sur le
   disque du serveur. Ne pas modifier EMBED à la main : modifier assets/ puis
   relancer le script. */
const EMBED = /*__EMBED__*/ {};
/* compression faite une seule fois par fichier (brotli + gzip), puis servie
   depuis la mémoire : zéro calcul par requête, même avec des milliers de visiteurs */
const zlib = require("zlib");
const packed = {};
const getPacked = (file) => {
  if (!packed[file]) {
    const raw = Buffer.from(EMBED[file], "utf8");
    packed[file] = {
      raw,
      br: zlib.brotliCompressSync(raw, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 11 } }),
      gz: zlib.gzipSync(raw, { level: 9 }),
    };
  }
  return packed[file];
};
const serveAsset = (req, res) => {
  const file = req.params.file;
  const type = ASSETS[file];
  if (!type || typeof EMBED[file] !== "string") return res.status(404).send("Not found");
  const etag = `"dz-${VERSION}-${file}"`;
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

/* ---------------- polices proposées ---------------- */
const FONTS = {
  "Inter": { g: "Inter:wght@400;500;600;700;800", stack: '"Inter", system-ui, sans-serif' },
  "Plus Jakarta Sans": { g: "Plus+Jakarta+Sans:wght@400;500;600;700;800", stack: '"Plus Jakarta Sans", system-ui, sans-serif' },
  "Manrope": { g: "Manrope:wght@400;500;600;700;800", stack: '"Manrope", system-ui, sans-serif' },
  "DM Sans": { g: "DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700", stack: '"DM Sans", system-ui, sans-serif' },
  "Outfit": { g: "Outfit:wght@400;500;600;700;800", stack: '"Outfit", system-ui, sans-serif' },
  "Sora": { g: "Sora:wght@400;500;600;700;800", stack: '"Sora", system-ui, sans-serif' },
  "Space Grotesk": { g: "Space+Grotesk:wght@400;500;600;700", stack: '"Space Grotesk", system-ui, sans-serif' },
  "Poppins": { g: "Poppins:wght@400;500;600;700;800", stack: '"Poppins", system-ui, sans-serif' },
  "Montserrat": { g: "Montserrat:wght@400;500;600;700;800", stack: '"Montserrat", system-ui, sans-serif' },
  "Bricolage Grotesque": { g: "Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800", stack: '"Bricolage Grotesque", system-ui, sans-serif' },
  "Fraunces": { g: "Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700", stack: '"Fraunces", Georgia, serif' },
  "Playfair Display": { g: "Playfair+Display:wght@400;500;600;700", stack: '"Playfair Display", Georgia, serif' },
  "Instrument Serif": { g: "Instrument+Serif:ital@0;1", stack: '"Instrument Serif", Georgia, serif' },
  "Inter Tight": { g: "Inter+Tight:wght@400;500;600;700", stack: '"Inter Tight", system-ui, sans-serif' },
  "Système (aucun téléchargement)": { g: null, stack: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif' },
};
const FONT_AUTO = "(celle de l'univers)";
const FONT_NAMES = [FONT_AUTO, ...Object.keys(FONTS)];
const MONO = "JetBrains+Mono:wght@400;500;600";

/* univers : identité complète (couleurs claires + sombres dans dz-core.css,
   polices ici, police d'accent chargée si l'univers en utilise une) */
const PRESETS = {
  nocturne: { label: "Nocturne — noir, citron, mono (tech, SaaS, agence)", heading: "Space Grotesk", body: "Inter", mono: true },
  editorial: { label: "Éditorial — papier, encre, serif italique (marque perso, conseil, média)", heading: "Inter Tight", body: "Inter Tight", mono: true, accent: "Instrument+Serif:ital@0;1" },
  studio: { label: "Studio — noir & blanc, bleu électrique, angles vifs (portfolio, créatif)", heading: "Bricolage Grotesque", body: "Manrope", mono: true },
  aurora: { label: "Aurora — violet, cyan, dégradés (SaaS grand public, IA)", heading: "Plus Jakarta Sans", body: "Inter" },
  terre: { label: "Terre — sable, olive, terracotta (artisan, bien-être, immobilier)", heading: "Fraunces", body: "Manrope", accent: "Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,600" },
  luxe: { label: "Luxe — noir chaud, or, serif (hôtel, mode, premium)", heading: "Playfair Display", body: "Manrope", accent: "Playfair+Display:ital,wght@1,400;1,500" },
};
const PRESET_KEYS = Object.keys(PRESETS);
const STYLES = ["moderne", "glass", "minimal", "brutal"];
const MOTIONS = ["toujours", "suivre le réglage du visiteur", "désactivées"];

const DEFAULTS = {
  preset: "nocturne",
  style: "moderne",
  custom_colors: false,
  primary: "#c8f23c",
  accent: "#7cf7d4",
  accent_2: "#f2f2ee",
  font_body: FONT_AUTO,
  font_heading: FONT_AUTO,
  radius: 0,
  container: 1200,
  skin: true,
  glass_nav: true,
  motion: "toujours",
  cursor: false,
  to_top: false,
  remember_theme: true,
  custom_css: "",
};

/* ---------------- nettoyage des valeurs ---------------- */
const hex = (v, d) => (typeof v === "string" && /^#[0-9a-fA-F]{3,8}$/.test(v.trim()) ? v.trim() : d);
const int = (v, d, min, max) => {
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : d;
};
const pick = (v, list, d) => (list.includes(v) ? v : d);
const cfgOf = (c = {}) => {
  const preset = pick(c.preset, PRESET_KEYS, DEFAULTS.preset);
  let motion = pick(c.motion, MOTIONS, DEFAULTS.motion);
  if (c.motion === false) motion = "désactivées"; /* réglage de la v1 */
  return {
    preset,
    style: pick(c.style, STYLES, DEFAULTS.style),
    custom_colors: !!c.custom_colors,
    primary: hex(c.primary, DEFAULTS.primary),
    accent: hex(c.accent, DEFAULTS.accent),
    accent_2: hex(c.accent_2, DEFAULTS.accent_2),
    font_body: pick(c.font_body, FONT_NAMES, FONT_AUTO),
    font_heading: pick(c.font_heading, FONT_NAMES, FONT_AUTO),
    radius: int(c.radius, 0, 0, 40),
    container: int(c.container, DEFAULTS.container, 720, 1800),
    skin: c.skin !== false,
    glass_nav: c.glass_nav !== false,
    motion,
    cursor: !!c.cursor,
    to_top: !!c.to_top,
    remember_theme: c.remember_theme !== false,
    custom_css: typeof c.custom_css === "string" ? c.custom_css.replace(/<\/?style/gi, "") : "",
  };
};

/* ---------------- réglages (une page, par tenant) ---------------- */
const configuration_workflow = () =>
  new Workflow({
    steps: [
      {
        name: "Apparence",
        form: async () =>
          new Form({
            blurb:
              "Réglages du design system pour ce tenant. Les blocs de la Library utilisent ces couleurs et polices automatiquement. Page d'outils : <a href='/dysizz-ui'>/dysizz-ui</a>",
            fields: [
              { name: "preset", label: "Univers", type: "String", required: true, default: DEFAULTS.preset,
                attributes: { options: PRESET_KEYS.map((k) => ({ name: k, label: PRESETS[k].label })) },
                sublabel: "Identité complète : couleurs claires et sombres, polices, forme des boutons. Change d'univers et tout le site suit." },
              { name: "style", label: "Matière", type: "String", required: true, default: DEFAULTS.style,
                attributes: { options: STYLES },
                sublabel: "moderne = ombres douces · glass = verre dépoli · minimal = plat · brutal = bordures épaisses et ombres dures" },
              { name: "custom_colors", label: "Utiliser mes propres couleurs", type: "Bool", default: false,
                sublabel: "Sinon, les couleurs de l'univers sont utilisées" },
              { name: "primary", label: "Couleur principale", type: "Color", default: DEFAULTS.primary, showIf: { custom_colors: true } },
              { name: "accent", label: "Couleur d'accent", type: "Color", default: DEFAULTS.accent, showIf: { custom_colors: true } },
              { name: "accent_2", label: "Deuxième accent", type: "Color", default: DEFAULTS.accent_2, showIf: { custom_colors: true } },
              { name: "font_heading", label: "Police des titres", type: "String", required: true, default: FONT_AUTO, attributes: { options: FONT_NAMES } },
              { name: "font_body", label: "Police du texte", type: "String", required: true, default: FONT_AUTO, attributes: { options: FONT_NAMES } },
              { name: "radius", label: "Arrondi des angles (px, 0 = celui de l'univers)", type: "Integer", default: 0, attributes: { min: 0, max: 40 } },
              { name: "container", label: "Largeur max du contenu (px)", type: "Integer", default: DEFAULTS.container, attributes: { min: 720, max: 1800 } },
              { name: "skin", label: "Habiller les éléments Saltcorn", type: "Bool", default: true,
                sublabel: "Boutons, formulaires, tableaux, cartes, menus, modales et fond des vues natives prennent le style du kit" },
              { name: "glass_nav", label: "Barre de menu en verre au défilement", type: "Bool", default: true },
              { name: "motion", label: "Animations", type: "String", required: true, default: DEFAULTS.motion, attributes: { options: MOTIONS },
                sublabel: "« suivre le réglage du visiteur » coupe tout si son ordinateur demande de réduire les animations (Windows : Paramètres > Accessibilité > Effets visuels)" },
              { name: "cursor", label: "Curseur personnalisé (ordinateur)", type: "Bool", default: false },
              { name: "to_top", label: "Bouton « retour en haut » automatique", type: "Bool", default: false },
              { name: "remember_theme", label: "Retenir le choix clair / sombre du visiteur", type: "Bool", default: true },
              { name: "custom_css", label: "CSS en plus (optionnel)", type: "String", fieldview: "textarea",
                sublabel: "Chargé après le kit, pour les retouches propres à ce tenant" },
            ],
          }),
      },
    ],
  });

/* ---------------- ce qui est injecté dans chaque page ---------------- */
const fontUrl = (fams) => `https://fonts.googleapis.com/css2?${[...new Set(fams)].map((g) => "family=" + g).join("&")}&display=swap`;

const headers = (rawCfg) => {
  const c = cfgOf(rawCfg);
  const P = PRESETS[c.preset];
  const fHead = c.font_heading === FONT_AUTO ? P.heading : c.font_heading;
  const fBody = c.font_body === FONT_AUTO ? P.body : c.font_body;
  const fams = [...new Set([fBody, fHead])].map((f) => FONTS[f] && FONTS[f].g).filter(Boolean);
  if (P.mono) fams.push(MONO);
  if (P.accent) fams.push(P.accent);
  const out = [];
  if (fams.length)
    out.push({
      headerTag:
        /* polices chargées sans bloquer l'affichage (le texte apparaît tout de suite) */
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
        `<link rel="preload" as="style" href="${fontUrl(fams)}" onload="this.onload=null;this.rel='stylesheet'">` +
        `<noscript><link rel="stylesheet" href="${fontUrl(fams)}"></noscript>`,
    });
  out.push({ css: pub("dz-core.css") });
  if (c.skin) out.push({ css: pub("dz-skin.css") });
  const vars = [
    `--dz-font-body:${FONTS[fBody].stack}`,
    `--dz-font-heading:${FONTS[fHead].stack}`,
    `--dz-container:${c.container}px`,
  ];
  if (c.radius > 0) vars.push(`--dz-radius:${c.radius}px`);
  if (c.custom_colors) vars.push(`--dz-primary:${c.primary}`, `--dz-primary-ink:${c.primary}`, `--dz-accent:${c.accent}`, `--dz-accent-2:${c.accent_2}`);
  /* :root:root pour passer devant les univers ([data-dz-preset]) */
  out.push({ style: `:root:root{${vars.join(";")}}` + (c.custom_css ? "\n" + c.custom_css : "") });
  /* script de tête : pose les attributs avant l'affichage (pas de flash) */
  const flags = {
    preset: c.preset,
    style: c.style,
    skin: c.skin,
    glass: c.glass_nav,
    motion: c.motion === "toujours" ? "on" : c.motion === "désactivées" ? "off" : "system",
    cursor: c.cursor,
    top: c.to_top,
    remember: c.remember_theme,
  };
  out.push({
    headerTag:
      "<script>(function(f){var h=document.documentElement;" +
      "h.setAttribute('data-dz-preset',f.preset);h.setAttribute('data-dz-style',f.style);" +
      "if(f.skin)h.classList.add('dz-skin');if(f.glass)h.classList.add('dz-glass-nav');" +
      "var b=/^\\/(pageedit|viewedit)\\//.test(location.pathname);if(b)h.classList.add('dz-builder');" +
      "h.setAttribute('data-dz-motion',b?'off':f.motion);if(f.cursor)h.setAttribute('data-dz-cursor','on');if(f.top)h.setAttribute('data-dz-totop','on');" +
      "if(f.remember){try{var t=localStorage.getItem('dz-theme');if(t==='auto')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';if(t==='dark'||t==='light')h.setAttribute('data-bs-theme',t);}catch(e){}}" +
      "h.classList.add('dz-js');setTimeout(function(){if(!window.DZ)h.classList.remove('dz-js');},3000);" +
      "})(" + JSON.stringify(flags) + ");</script>",
  });
  out.push({ script: pub("dz.js"), defer: true });
  return out;
};

/* ---------------- page d'admin : installer les blocs ---------------- */
const readPack = (file) => EMBED[file];
const emptyPack = () => ({ tables: [], views: [], plugins: [], pages: [], page_groups: [], triggers: [], roles: [], library: [] });

const isAdmin = (req) => req.user && req.user.role_id === 1;
const esc = (s) => String(s).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));

const adminPage = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const Page = require("@saltcorn/data/models/page");
  const blocks = readPack("blocks.json").library;
  const demo = readPack("demo-pages.json").pages;
  const libs = await Library.find({});
  const libNames = new Set(libs.map((l) => l.name));
  const present = blocks.filter((b) => libNames.has(b.name)).length;
  const pagesPresent = demo.filter((p) => Page.findOne({ name: p.name })).length;
  const Plugin = require("@saltcorn/data/models/plugin");
  const plugins = await Plugin.find({});
  const me = plugins.find((p) => p.name === PLUGIN) || plugins.find((p) => /dysizz-ui/i.test(p.name + " " + (p.location || "")));
  const cfgName = me ? me.name : PLUGIN;
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const msg = req.query && req.query.ok ? `<div class="dz-callout dz-callout-success mb-4"><div>${esc(req.query.ok)}</div></div>` : "";
  const html = `
<div class="dz-container-narrow" style="padding-top:1rem">
  ${msg}
  <span class="dz-eyebrow">Dysizz UI · v${esc(VERSION)}</span>
  <h1 class="dz-h2">Kit de design</h1>
  <p class="dz-lead">Blocs prêts à glisser dans le builder (panneau <b>Library</b>), pages de démo, réglages du thème.</p>
  <div class="dz-grid dz-grid-2" style="margin-top:2rem">
    <div class="dz-card">
      <div class="dz-icon"><i class="fas fa-cubes"></i></div>
      <h3 class="dz-h4">Blocs de la Library</h3>
      <p>${present} / ${blocks.length} blocs installés dans ce tenant. Réinstaller met à jour les blocs du kit (ceux dont le nom commence par « DZ · »). Tes propres blocs ne sont pas touchés.</p>
      <form method="post" action="/dysizz-ui/install-blocks"><input type="hidden" name="_csrf" value="${esc(csrf)}">
        <button class="dz-btn" type="submit"><i class="fas fa-download"></i> ${present ? "Mettre à jour" : "Installer"} les blocs</button></form>
    </div>
    <div class="dz-card">
      <div class="dz-icon"><i class="fas fa-file-alt"></i></div>
      <h3 class="dz-h4">Pages de démo</h3>
      <p>${pagesPresent} / ${demo.length} pages installées : ${demo.map((p) => `<a href="/page/${encodeURIComponent(p.name)}">${esc(p.name)}</a>`).join(", ")}. Visibles par les admins seulement. Duplique-les pour démarrer un projet.</p>
      <form method="post" action="/dysizz-ui/install-pages"><input type="hidden" name="_csrf" value="${esc(csrf)}">
        <button class="dz-btn dz-btn-ghost" type="submit"><i class="fas fa-magic"></i> ${pagesPresent ? "Réinstaller" : "Installer"} les pages de démo</button></form>
    </div>
    <div class="dz-card">
      <div class="dz-icon"><i class="fas fa-palette"></i></div>
      <h3 class="dz-h4">Réglages du thème</h3>
      <p>Couleurs, polices, arrondis, style, animations. Propres à ce tenant.</p>
      <a class="dz-btn dz-btn-ghost" href="/plugins/configure/${encodeURIComponent(cfgName)}"><i class="fas fa-sliders-h"></i> Ouvrir les réglages</a>
    </div>
    <div class="dz-card">
      <div class="dz-icon"><i class="fas fa-code"></i></div>
      <h3 class="dz-h4">Atelier de blocs</h3>
      <p>Crée tes propres blocs en HTML / CSS / JS avec aperçu en direct, modifie une copie d'un bloc du kit, exporte / importe tes blocs d'un tenant à l'autre.</p>
      <a class="dz-btn" href="/dysizz-ui/blocks"><i class="fas fa-code"></i> Ouvrir l'atelier</a>
    </div>
    <div class="dz-card">
      <div class="dz-icon"><i class="fas fa-book"></i></div>
      <h3 class="dz-h4">Aide-mémoire</h3>
      <p>Toutes les classes et attributs <code>data-dz-*</code> sont dans le README du dépôt. La page de démo <b>dz-catalogue</b> montre chaque composant.</p>
    </div>
  </div>
</div>`;
  res.sendWrap("Dysizz UI", { above: [{ type: "blank", contents: html }] });
};

const installFrom = (file, key) => async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const { install_pack } = require("@saltcorn/admin-models/models/pack");
  const src = readPack(file);
  const pack = { ...emptyPack(), [key]: src[key] };
  if (key === "library") {
    /* on retire les anciens blocs du kit (noms de la v1 « DZ · … » et ceux de la liste actuelle) */
    const Library = require("@saltcorn/data/models/library");
    const names = new Set(src.library.map((l) => l.name));
    for (const l of await Library.find({})) {
      if (l.name.startsWith("DZ · ") || (src.previous || []).includes(l.name)) if (!names.has(l.name)) await l.delete();
    }
  }
  await install_pack(pack, undefined, async () => {});
  const { getState } = require("@saltcorn/data/db/state");
  if (key === "pages" && getState().refresh_pages) { await getState().refresh_pages(true); await getState().refresh_pages(); }
  const n = (src[key] || []).length;
  res.redirect(
    "/dysizz-ui?ok=" +
      encodeURIComponent(key === "library" ? `${n} blocs installés. Ouvre une page dans le builder, panneau Library.` : `${n} pages de démo installées.`)
  );
};


/* ---------------- Atelier de blocs : créer / modifier / partager ses blocs ----------------
   Un bloc créé ici est un bloc HTML de la Library du builder, comme ceux du kit.
   Le code source (HTML, CSS, JS) est gardé dans le bloc (clé dz_src) pour pouvoir
   le rouvrir et le modifier ici. Le CSS est automatiquement limité au bloc
   (imbrication CSS native : .dzb-xxx { ton css }). */
const kitNames = () => new Set(readPack("blocks.json").library.map((b) => b.name));
const slug = (s) => String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "bloc";
const WRAPS = {
  none: "Brut (juste mon HTML)",
  section: "Section + conteneur centré",
  full: "Section pleine largeur",
};
const buildBlockLayout = ({ name, html, css, js, wrap }) => {
  const cls = "dzb-" + slug(name);
  let inner = `<div class="${cls}">${html || ""}</div>`;
  if (wrap === "section") inner = `<section class="dz-section"><div class="dz-container">${inner}</div></section>`;
  if (wrap === "full") inner = `<section class="dz-section dz-flush">${inner}</section>`;
  const style = css && css.trim() ? `<style>.${cls}{${css.replace(/<\/style/gi, "")}}</style>` : "";
  const script =
    js && js.trim()
      ? `<script>(function(){var s=document.currentScript;function run(){document.querySelectorAll(".${cls}").forEach(function(el){if(el.__dzb)return;el.__dzb=1;(function(el){${js.replace(/<\/script/gi, "<\\/script")}\n})(el);});}if(document.readyState!=="loading")run();else document.addEventListener("DOMContentLoaded",run);})();</script>`
      : "";
  return { type: "blank", isHTML: true, contents: style + inner + script, dz_src: { html: html || "", css: css || "", js: js || "", wrap: wrap || "none" } };
};
/* rend un bloc du kit en HTML statique pour s'en servir comme point de départ */
const blockToHtml = (layout) => {
  if (layout && layout.dz_src) return layout.dz_src;
  try {
    const render = require("@saltcorn/markup/layout");
    return { html: render({ blockDispatch: {}, layout, role: 1, req: {} }), css: "", js: "", wrap: "none" };
  } catch (e) {
    return { html: layout && layout.type === "blank" ? layout.contents : "", css: "", js: "", wrap: "none" };
  }
};
const post = (req) => req.body || {};

const atelierPage = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const kit = kitNames();
  const libs = (await Library.find({}, { orderBy: "name" })).sort((a, b) => a.name.localeCompare(b.name));
  const mine = libs.filter((l) => !kit.has(l.name));
  let cur = { name: "", icon: "fas fa-cube", html: "", css: "", js: "", wrap: "section", id: "" };
  const q = req.query || {};
  if (q.edit || q.from) {
    const l = libs.find((x) => String(x.id) === String(q.edit || q.from));
    if (l) {
      const src = blockToHtml(l.layout);
      cur = { ...cur, ...src, icon: l.icon || cur.icon, name: q.edit ? l.name : `Mon · ${l.name.replace(/^[^·]*·\s*/, "")}`, id: q.edit ? l.id : "" };
    }
  }
  const msg = q.ok ? `<div class="dz-callout dz-callout-success mb-4"><div>${esc(q.ok)}</div></div>` : q.err ? `<div class="dz-callout dz-callout-danger mb-4"><div>${esc(q.err)}</div></div>` : "";
  const opt = (v, l, sel) => `<option value="${esc(v)}"${v === sel ? " selected" : ""}>${esc(l)}</option>`;
  const hid = `<input type="hidden" name="_csrf" value="${esc(csrf)}">`;
  const html = `
<style>
.dzb-ed textarea{font-family:var(--dz-font-mono,monospace);font-size:.82rem;line-height:1.5;min-height:9rem;tab-size:2;white-space:pre}
.dzb-ed textarea[name=html]{min-height:18rem}
.dzb-prev{position:sticky;top:1rem}
.dzb-frame{width:100%;height:70vh;border:1px solid var(--dz-border);border-radius:var(--dz-radius);background:var(--dz-bg);transition:width .3s}
.dzb-frame.m{width:390px;max-width:100%;margin-inline:auto;display:block}
.dzb-list td{vertical-align:middle}
</style>
<div class="container-fluid" style="padding-top:1rem">
  ${msg}
  <a href="/dysizz-ui" class="small">← Kit de design</a>
  <h1 class="dz-h2" style="margin-top:.5rem">Atelier de blocs</h1>
  <p class="dz-lead">Écris un bloc en HTML / CSS / JS (ou pars d'un bloc du kit), vois le rendu en direct, enregistre-le : il apparaît dans le panneau <b>Library</b> du builder, dans ce tenant.</p>
  <div class="row g-4" style="margin-top:1rem">
    <div class="col-xl-5">
      <form method="post" action="/dysizz-ui/blocks/save" class="dzb-ed" id="dzb-form">${hid}
        <input type="hidden" name="id" value="${esc(cur.id)}">
        <div class="row g-2">
          <div class="col-7"><label class="form-label">Nom (visible dans la Library)</label><input class="form-control" name="name" required maxlength="80" value="${esc(cur.name)}" placeholder="Mon · Bandeau promo"></div>
          <div class="col-5"><label class="form-label">Icône <a href="https://fontawesome.com/v5/search?m=free" target="_blank" rel="noopener">(liste)</a></label><input class="form-control" name="icon" value="${esc(cur.icon)}"></div>
        </div>
        <label class="form-label mt-3">Enveloppe</label>
        <select class="form-select" name="wrap">${Object.entries(WRAPS).map(([k, v]) => opt(k, v, cur.wrap)).join("")}</select>
        <label class="form-label mt-3">HTML <small class="text-muted">— toutes les classes dz-* et data-dz-* marchent</small></label>
        <textarea class="form-control" name="html" spellcheck="false">${esc(cur.html)}</textarea>
        <label class="form-label mt-3">CSS <small class="text-muted">— limité à ce bloc. Les règles directes visent le bloc, <code>h2{…}</code> vise ses h2, <code>&amp;:hover{…}</code> le bloc au survol</small></label>
        <textarea class="form-control" name="css" spellcheck="false" placeholder="padding:2rem;&#10;h2{color:var(--dz-primary)}">${esc(cur.css)}</textarea>
        <label class="form-label mt-3">JS (optionnel) <small class="text-muted">— exécuté une fois par bloc sur la page, la variable <code>el</code> est le bloc</small></label>
        <textarea class="form-control" name="js" spellcheck="false" placeholder="el.addEventListener('click', () => DZ.toast('Bonjour'));">${esc(cur.js)}</textarea>
        <div class="dz-cluster mt-3">
          <button class="dz-btn" type="submit"><i class="fas fa-save"></i> ${cur.id ? "Enregistrer les modifications" : "Ajouter à la Library"}</button>
          ${cur.id ? `<button class="dz-btn dz-btn-ghost" type="submit" name="as_new" value="1">Enregistrer comme nouveau</button><a class="dz-btn dz-btn-ghost" href="/dysizz-ui/blocks">Nouveau bloc</a>` : ""}
        </div>
      </form>
    </div>
    <div class="col-xl-7">
      <div class="dzb-prev">
        <div class="dz-cluster" style="justify-content:space-between;margin-bottom:.5rem">
          <b>Aperçu en direct</b>
          <div class="dz-cluster"><button type="button" class="dz-btn dz-btn-sm dz-btn-ghost" data-w="d"><i class="fas fa-desktop"></i></button><button type="button" class="dz-btn dz-btn-sm dz-btn-ghost" data-w="m"><i class="fas fa-mobile-alt"></i></button><button type="button" class="dz-btn dz-btn-sm dz-btn-ghost" id="dzb-theme"><i class="fas fa-adjust"></i></button></div>
        </div>
        <iframe class="dzb-frame" id="dzb-frame" title="Aperçu"></iframe>
      </div>
    </div>
  </div>

  <h2 class="dz-h3" style="margin-top:3rem">Mes blocs (${mine.length})</h2>
  ${mine.length ? `<div class="table-responsive"><table class="table dzb-list"><tbody>${mine.map((l) => `<tr><td><i class="${esc(l.icon || "fas fa-cube")}"></i> ${esc(l.name)}</td><td class="text-end">
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="/dysizz-ui/blocks?edit=${l.id}">Modifier</a>
    <form method="post" action="/dysizz-ui/blocks/delete" class="d-inline" onsubmit="return confirm('Supprimer ce bloc de la Library ? (les pages qui l\\'utilisent déjà ne changent pas)')">${hid}<input type="hidden" name="id" value="${l.id}"><button class="dz-btn dz-btn-sm dz-btn-ghost" type="submit"><i class="fas fa-trash"></i></button></form></td></tr>`).join("")}</tbody></table></div>`
    : `<p class="text-muted">Aucun bloc perso pour l'instant. Crée-en un ci-dessus, ou dans le builder : sélectionne un élément, puis <b>Library → Add</b>.</p>`}

  <div class="row g-4" style="margin-top:1rem">
    <div class="col-lg-4"><div class="dz-card">
      <h3 class="dz-h4">Partir d'un bloc du kit</h3>
      <p class="small">Copie son code dans l'atelier. L'original reste intact.</p>
      <form method="get" action="/dysizz-ui/blocks"><select class="form-select" name="from">${libs.filter((l) => kit.has(l.name)).map((l) => opt(String(l.id), l.name, "")).join("")}</select>
      <button class="dz-btn dz-btn-sm mt-2" type="submit">Ouvrir dans l'atelier</button></form>
    </div></div>
    <div class="col-lg-4"><div class="dz-card">
      <h3 class="dz-h4">Exporter</h3>
      <p class="small">Fichier JSON de tes blocs, à importer dans un autre tenant ou à garder dans ton dépôt Git.</p>
      <a class="dz-btn dz-btn-sm" href="/dysizz-ui/blocks/export"><i class="fas fa-file-export"></i> Mes blocs</a>
      <a class="dz-btn dz-btn-sm dz-btn-ghost" href="/dysizz-ui/blocks/export?all=1">Toute la Library</a>
    </div></div>
    <div class="col-lg-4"><div class="dz-card">
      <h3 class="dz-h4">Importer</h3>
      <form method="post" action="/dysizz-ui/blocks/import">${hid}
        <input type="file" accept=".json,application/json" class="form-control form-control-sm" id="dzb-file">
        <textarea name="json" class="form-control form-control-sm mt-2" rows="3" placeholder="…ou colle le JSON ici" required></textarea>
        <label class="small mt-1"><input type="checkbox" name="overwrite" value="1" checked> remplacer les blocs du même nom</label><br>
        <button class="dz-btn dz-btn-sm mt-2" type="submit"><i class="fas fa-file-import"></i> Importer</button></form>
    </div></div>
  </div>
</div>
<script>
(function(){
  var f=document.getElementById("dzb-form"),fr=document.getElementById("dzb-frame"),dark=null,t;
  var head=[].slice.call(document.querySelectorAll('link[rel=stylesheet],head style')).map(function(n){return n.outerHTML}).join("");
  var de=document.documentElement,attrs=[].slice.call(de.attributes).filter(function(a){return a.name!=="style"}).map(function(a){return a.name+'="'+a.value.replace(/"/g,"&quot;")+'"'}).join(" ");
  function slug(s){return (s||"").toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,40)||"bloc"}
  function draw(){
    var cls="dzb-"+slug(f.name.value),h='<div class="'+cls+'">'+f.html.value+'</div>',w=f.wrap.value;
    if(w==="section")h='<section class="dz-section"><div class="dz-container">'+h+'</div></section>';
    if(w==="full")h='<section class="dz-section dz-flush">'+h+'</section>';
    var css=f.css.value.trim()?'<style>.'+cls+'{'+f.css.value+'}</style>':"";
    var js=f.js.value.trim()?'<script>document.querySelectorAll(".'+cls+'").forEach(function(el){try{'+f.js.value+'\\n}catch(e){console.error(e)}});<\\/script>':"";
    var a=attrs;if(dark!==null)a=a.replace(/data-bs-theme="[^"]*"/,"")+' data-bs-theme="'+(dark?"dark":"light")+'"';
    fr.srcdoc='<!doctype html><html '+a+'><head><meta name="viewport" content="width=device-width,initial-scale=1">'+head+'<style>body{padding:0;margin:0}</style></head><body>'+css+h+'<script src="${pub("dz.js")}"><\\/script>'+js+'</body></html>';
  }
  f.addEventListener("input",function(){clearTimeout(t);t=setTimeout(draw,350)});
  f.querySelectorAll("textarea").forEach(function(ta){ta.addEventListener("keydown",function(e){if(e.key==="Tab"){e.preventDefault();var s=ta.selectionStart;ta.setRangeText("  ",s,ta.selectionEnd,"end")}})});
  document.querySelectorAll("[data-w]").forEach(function(b){b.onclick=function(){fr.classList.toggle("m",b.dataset.w==="m")}});
  document.getElementById("dzb-theme").onclick=function(){dark=dark===null?!(de.getAttribute("data-bs-theme")==="dark"):!dark;draw()};
  var fi=document.getElementById("dzb-file");fi&&fi.addEventListener("change",function(){var r=new FileReader();r.onload=function(){fi.form.json.value=r.result};fi.files[0]&&r.readAsText(fi.files[0])});
  draw();
})();
</script>`;
  res.sendWrap("Atelier de blocs", { above: [{ type: "blank", contents: html }] });
};

const saveBlock = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const b = post(req);
  const name = String(b.name || "").trim().slice(0, 80);
  if (!name) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("Donne un nom au bloc."));
  if (kitNames().has(name)) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("Ce nom est réservé à un bloc du kit (il serait écrasé à la prochaine mise à jour). Choisis un autre nom, par ex. « Mon · … »."));
  const icon = /^[a-z0-9 -]{1,60}$/i.test(b.icon || "") ? b.icon : "fas fa-cube";
  const layout = buildBlockLayout({ name, html: b.html, css: b.css, js: b.js, wrap: WRAPS[b.wrap] ? b.wrap : "none" });
  const existing = b.id && !b.as_new ? await Library.findOne({ id: +b.id }) : null;
  const clash = await Library.findOne({ name });
  if (clash && (!existing || clash.id !== existing.id)) return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent(`Un bloc « ${name} » existe déjà.`) + (existing ? "&edit=" + existing.id : ""));
  if (existing) await existing.update({ name, icon, layout });
  else await Library.create({ name, icon, layout });
  const saved = await Library.findOne({ name });
  res.redirect(`/dysizz-ui/blocks?edit=${saved ? saved.id : ""}&ok=` + encodeURIComponent(`« ${name} » est enregistré. Il est dans le panneau Library du builder.`));
};

const deleteBlock = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const l = await Library.findOne({ id: +post(req).id });
  if (l && !kitNames().has(l.name)) await l.delete();
  res.redirect("/dysizz-ui/blocks?ok=" + encodeURIComponent("Bloc supprimé."));
};

const exportBlocks = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const kit = kitNames();
  const all = req.query && req.query.all;
  const library = (await Library.find({})).filter((l) => all || !kit.has(l.name)).map((l) => ({ name: l.name, icon: l.icon, layout: l.layout }));
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Content-Disposition", `attachment; filename="blocs-${all ? "library" : "perso"}-${new Date().toISOString().slice(0, 10)}.json"`);
  res.send(JSON.stringify({ format: "dysizz-blocks", version: 1, kit: VERSION, library }, null, 2));
};

const importBlocks = async (req, res) => {
  if (!isAdmin(req)) return res.status(403).send("Réservé aux administrateurs");
  const Library = require("@saltcorn/data/models/library");
  const b = post(req);
  let data;
  try { data = JSON.parse(b.json || ""); } catch (e) { return res.redirect("/dysizz-ui/blocks?err=" + encodeURIComponent("JSON illisible.")); }
  const items = Array.isArray(data) ? data : data.library || [];
  const kit = kitNames();
  let n = 0, skipped = 0;
  for (const it of items) {
    if (!it || typeof it.name !== "string" || !it.layout || typeof it.layout !== "object") { skipped++; continue; }
    const name = it.name.slice(0, 80);
    const icon = /^[a-z0-9 -]{1,60}$/i.test(it.icon || "") ? it.icon : "fas fa-cube";
    const ex = await Library.findOne({ name });
    if (ex) {
      if (!b.overwrite || kit.has(name)) { skipped++; continue; }
      await ex.update({ icon, layout: it.layout });
    } else await Library.create({ name, icon, layout: it.layout });
    n++;
  }
  res.redirect("/dysizz-ui/blocks?ok=" + encodeURIComponent(`${n} bloc(s) importé(s)${skipped ? `, ${skipped} ignoré(s)` : ""}.`));
};

/* Saltcorn 1.6 garde en cache les en-têtes par rôle : sans ça, un
   changement de réglage (couleur, police…) n'apparaît qu'après un
   redémarrage. On recalcule le cache à chaque (re)chargement du plugin. */
const onLoad = async () => {
  try {
    const { getState } = require("@saltcorn/data/db/state");
    const st = getState();
    if (st && st.assets_by_role && typeof st.computeAssetsByRole === "function") await st.computeAssetsByRole();
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
  routes: () => [
    { url: "/dysizz-ui", method: "get", callback: adminPage },
    { url: "/dysizz-ui/a/:ver/:file", method: "get", callback: serveAsset },
    { url: "/dysizz-ui/install-blocks", method: "post", callback: installFrom("blocks.json", "library") },
    { url: "/dysizz-ui/install-pages", method: "post", callback: installFrom("demo-pages.json", "pages") },
    { url: "/dysizz-ui/blocks", method: "get", callback: atelierPage },
    { url: "/dysizz-ui/blocks/save", method: "post", callback: saveBlock },
    { url: "/dysizz-ui/blocks/delete", method: "post", callback: deleteBlock },
    { url: "/dysizz-ui/blocks/export", method: "get", callback: exportBlocks },
    { url: "/dysizz-ui/blocks/import", method: "post", callback: importBlocks },
  ],
};
