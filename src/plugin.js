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
const serveAsset = (req, res) => {
  const file = req.params.file;
  const type = ASSETS[file];
  if (!type || typeof EMBED[file] !== "string") return res.status(404).send("Not found");
  res.set("Content-Type", type);
  res.set("Cache-Control", req.params.ver === VERSION ? "public, max-age=31536000, immutable" : "no-cache");
  res.send(EMBED[file]);
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
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
        `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?${[...new Set(fams)].map((g) => "family=" + g).join("&")}&display=swap">`,
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
  ],
};
