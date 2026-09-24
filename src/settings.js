/* dysizz-ui — réglages par tenant */
"use strict";
const Workflow = require("@saltcorn/data/models/workflow");
const Form = require("@saltcorn/data/models/form");

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
/* transitions entre sections (clé CSS → libellé) */
const TRANSITIONS = {
  none: "Aucune",
  fade: "Fondu — la section apparaît en douceur",
  rise: "Montée douce — elle monte et se pose",
  zoom: "Zoom — elle grandit jusqu'à sa taille",
  blur: "Brume — du flou vers le net",
  tilt: "Bascule 3D — elle se redresse",
  curtain: "Rideau — elle s'ouvre depuis le centre",
  wipe: "Balayage — elle se dévoile de gauche à droite",
  cover: "Recouvrement — la suivante glisse par-dessus",
  stack: "Cartes empilées — la précédente recule et s'efface",
  depth: "Profondeur — parallaxe entre les sections",
  fadeout: "Fondu enchaîné — apparaît puis s'efface",
};
const TR_KEYS = Object.keys(TRANSITIONS);
const SNAPS = { off: "Libre", soft: "Aimanté léger (s'aligne si on s'arrête près d'une section)", strict: "Aimanté strict (une section à la fois)" };
const SMOOTHS = { off: "Natif du navigateur", light: "Doux (léger)", strong: "Très doux (effet « Apple »)" };

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
  transition: "none",
  snap: "off",
  smooth: "off",
  bg_morph: true,
  families: [],
  classes_css: "",
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
    transition: pick(c.transition, TR_KEYS, DEFAULTS.transition),
    snap: pick(c.snap, Object.keys(SNAPS), DEFAULTS.snap),
    smooth: pick(c.smooth, Object.keys(SMOOTHS), DEFAULTS.smooth),
    bg_morph: c.bg_morph !== false,
    /* réglages gérés par les pages /dysizz-ui (pas par le formulaire) */
    families: Array.isArray(c.families) ? c.families.filter((f) => /^[a-z]{2,12}$/.test(f)) : [],
    classes_css: typeof c.classes_css === "string" ? c.classes_css.replace(/<\/?style/gi, "") : "",
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
              { name: "transition", label: "Transition entre les sections", type: "String", required: true, default: DEFAULTS.transition,
                attributes: { options: TR_KEYS.map((k) => ({ name: k, label: TRANSITIONS[k] })) },
                sublabel: "Par défaut pour tout le tenant. Une page peut choisir autre chose (bloc « Outil · Réglages de la page »), une section aussi (classe dz-tr-<nom>). Aperçu de chaque transition : /dysizz-ui/transitions" },
              { name: "snap", label: "Sections aimantées", type: "String", required: true, default: DEFAULTS.snap,
                attributes: { options: Object.keys(SNAPS).map((k) => ({ name: k, label: SNAPS[k] })) } },
              { name: "smooth", label: "Défilement", type: "String", required: true, default: DEFAULTS.smooth,
                attributes: { options: Object.keys(SMOOTHS).map((k) => ({ name: k, label: SMOOTHS[k] })) },
                sublabel: "Doux = défilement à la souris avec inertie (sites vitrines). Coupé automatiquement sur mobile, dans les applications et pour les visiteurs qui réduisent les animations." },
              { name: "bg_morph", label: "Couleur de fond qui suit les sections", type: "Bool", default: true,
                sublabel: "Actif seulement sur les sections qui ont une couleur (classe dz-morph-<couleur> ou attribut data-dz-bg)" },
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


module.exports = { TRANSITIONS, TR_KEYS, SNAPS, SMOOTHS, FONTS, FONT_AUTO, FONT_NAMES, MONO, PRESETS, PRESET_KEYS, STYLES, MOTIONS, DEFAULTS, cfgOf, configuration_workflow };
