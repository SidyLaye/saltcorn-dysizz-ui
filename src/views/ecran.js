/* Vue « DZ Écran » : un bloc d'écran de dysizz-ui (liste, tableau, chiffres, graphique, fiche…) posé dans une
   page comme une VRAIE vue Saltcorn. Dans l'éditeur de page, on la pose, on choisit « État : fixe », et tous
   ses réglages (source, colonnes, titre, liens…) apparaissent dans la colonne de droite, bloc par bloc.
   Une seule vue (« dz_ecran ») sert à tous les blocs : chaque placement garde ses propres réglages.

   Le rendu est le même <div data-dz-widget="…"> que lit client/dz.js : rien ne change pour l'utilisateur.
   Les droits restent ceux des sources de données et des tables (vérifiés par le serveur). */
"use strict";
const { esc } = require("../core");

const NOM_VUE = "dz_ecran";
/* réglage → attribut data-* ; les réglages rares passent par « autres » (JSON) */
const CHAMPS = [
  ["widget", "Type de bloc", "tableau (listes, chiffres, graphiques, filtres) ou fiche (formulaire)", { options: "tableau,fiche" }],
  ["source", "Source de données", "Nom déclaré dans Dysizz → Sources"],
  ["vue", "Présentation", "liste, chiffres, tuiles, graphique, filtres, onglets…"],
  ["titre", "Titre"],
  ["sous", "Sous-titre"],
  ["colonnes", "Colonnes (JSON)", "", { area: true }],
  ["libelles", "Libellés (JSON)", "", { area: true }],
  ["champs", "Champs (JSON ou liste)", "", { area: true }],
  ["montrer", "Montrer"],
  ["lien", "Lien d'une ligne", "Ex. : /page/lead?id={id}"],
  ["params", "Paramètres de la source (JSON)", "Ex. : {\"q\":\"$q\"}", { area: true }],
  ["mesure", "Mesure"],
  ["vide", "Texte quand il n'y a rien"],
  ["rafraichir", "Rafraîchir (secondes)"],
  ["attention", "Mise en évidence (JSON)", "", { area: true }],
  ["niveau", "Niveau d'accès affiché", "admin : bandeau « Administrateur »"],
  ["table", "Table (fiche)"],
  ["titre_nouveau", "Titre d'une nouvelle fiche"],
  ["apres", "Après l'enregistrement (fiche)", "Ex. : /page/gestion?t=equipe"],
  ["aides", "Aides des champs (JSON)", "", { area: true }],
  ["supprimer", "Bouton supprimer (fiche)"],
  ["autres", "Autres réglages (JSON)", "Tout autre attribut : {\"clic\":\"…\",\"alerte\":\"…\"}", { area: true }],
];
const ATTR = (k) => "data-" + k.replace(/_/g, "-");

/* réglages d'un placement → balise lue par dz.js */
const balise = (s = {}) => {
  const w = /^(tableau|fiche)$/.test(String(s.widget || "")) ? s.widget : "tableau";
  const attrs = [];
  for (const [k] of CHAMPS) {
    if (k === "widget" || k === "autres") continue;
    const v = s[k];
    if (v === undefined || v === null || v === "") continue;
    attrs.push(`${ATTR(k)}="${esc(typeof v === "object" ? JSON.stringify(v) : String(v))}"`);
  }
  let autres = s.autres;
  if (typeof autres === "string" && autres.trim()) { try { autres = JSON.parse(autres); } catch (e) { return `<div class="alert alert-warning">DZ Écran : « Autres réglages » n'est pas un JSON valide.</div>`; } }
  if (autres && typeof autres === "object") for (const [k, v] of Object.entries(autres)) {
    if (!/^[a-z][a-z0-9-]*$/.test(k) || v === undefined || v === null) continue;
    attrs.push(`data-${k}="${esc(typeof v === "object" ? JSON.stringify(v) : String(v))}"`);
  }
  /* data-dz-bloc : posé par la vue (l'éditeur de page dit alors où régler le bloc) */
  return `<div data-dz-widget="${w}" data-dz-bloc="vue"${attrs.length ? " " + attrs.join(" ") : ""}></div>`;
};

/* Type « texte » sans « préréglages » : pour un champ String, l'éditeur de page ajoute une liste « Preset … »
   (IP, SessionID) sans choix vide ; à l'enregistrement elle vaut « IP » et chaque réglage est remplacé par l'adresse
   IP du visiteur. Sans préréglages, la liste n'apparaît pas. */
const texteSansPreset = () => {
  try { const T = require("@saltcorn/data/db/state").getState().types.String; return T ? { ...T, presets: undefined } : "String"; } catch (e) { return "String"; }
};
const PRESET = /^preset_/;

/* ——— conversion : <div data-dz-widget=…></div> écrit en HTML dans une page → bloc « DZ Écran » ——— */
const ENT = { amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", apos: "'" };
const desEsc = (s) => String(s).replace(/&(amp|lt|gt|quot|#39|apos);/g, (m, k) => ENT[k]);
const connus = new Set(CHAMPS.map(([k]) => k));
const lireWidget = (w, attrs) => {
  const cfg = { widget: w }, autres = {};
  for (const m of String(attrs).matchAll(/data-([\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)) {
    const cle = m[1].replace(/-/g, "_"), val = desEsc(m[2] !== undefined ? m[2] : m[3]);
    if (connus.has(cle) && cle !== "widget" && cle !== "autres") cfg[cle] = val;
    else if (m[1] !== "dz-widget" && m[1] !== "dz-bloc") { let v = val; try { if (/^[[{]/.test(val)) v = JSON.parse(val); } catch (e) { v = val; } autres[m[1]] = v; }
  }
  if (Object.keys(autres).length) cfg.autres = JSON.stringify(autres);
  return cfg;
};
let n = 0;
const nomSegment = () => "dz" + Date.now().toString(36) + (n++).toString(36) + Math.random().toString(36).slice(2, 6);
const segmentVue = (cfg) => ({ type: "view", view: NOM_VUE, name: nomSegment(), state: "fixed", configuration: cfg });
/* un bloc HTML qui ne contient QUE des widgets (éventuellement dans une carte) devient des blocs de vue */
/* seuls « tableau » et « fiche » sont des blocs d'écran ; les autres widgets (jeux, signature, tableur…) restent en HTML */
const RE_SEUL = /^\s*(?:<div class="([^"]*)"(?:\s+style="([^"]*)")?\s*>)?\s*((?:<div data-dz-widget="(?:tableau|fiche)"[^>]*><\/div>\s*)+)(?:<\/div>)?\s*$/;
const convertirBloc = (html) => {
  const m = String(html || "").match(RE_SEUL);
  if (!m) return null;
  const ouverts = (html.match(/<div\b/g) || []).length, fermes = (html.match(/<\/div>/g) || []).length;
  if (ouverts !== fermes) return null;
  const vues = [...m[3].matchAll(/<div data-dz-widget="(tableau|fiche)"([^>]*)><\/div>/g)].map((x) => segmentVue(lireWidget(x[1], x[2])));
  const corps = vues.length === 1 ? vues[0] : { above: vues };
  if (m[1] === undefined) return corps;
  const style = {};
  for (const d of String(m[2] || "").split(";")) { const [k, v] = d.split(":").map((x) => x && x.trim()); if (k && v) style[k] = v; }
  return { type: "container", customClass: m[1], style, contents: corps };
};
/* parcourt une mise en page ; rend { layout, convertis, nettoyes } sans toucher à l'original.
   nettoyes : blocs « DZ Écran » dont on retire les « preset_… » enregistrés par l'éditeur (voir texteSansPreset) */
const convertirLayout = (layout) => {
  let convertis = 0, nettoyes = 0;
  const walk = (x) => {
    if (Array.isArray(x)) return x.map(walk);
    if (!x || typeof x !== "object") return x;
    if (x.type === "view" && x.view === NOM_VUE && x.configuration && Object.keys(x.configuration).some((k) => PRESET.test(k))) {
      nettoyes++;
      return { ...x, configuration: Object.fromEntries(Object.entries(x.configuration).filter(([k]) => !PRESET.test(k))) };
    }
    if (x.type === "blank" && x.isHTML && /data-dz-widget=/.test(String(x.contents || ""))) {
      const c = convertirBloc(x.contents);
      if (c) { convertis += (String(x.contents).match(/data-dz-widget="(tableau|fiche)"/g) || []).length; return c; }
      return x;
    }
    const o = { ...x };
    for (const k of ["contents", "above", "besides"]) if (k in o && typeof o[k] !== "string") o[k] = walk(o[k]);
    return o;
  };
  const l = walk(layout);
  return { layout: l, convertis, nettoyes };
};
/* widgets encore écrits en HTML dans une mise en page (pour la page Santé) */
const widgetsHTML = (layout) => {
  let k = 0;
  const walk = (x) => { if (Array.isArray(x)) return x.forEach(walk); if (!x || typeof x !== "object") return; if (x.type === "blank" && x.isHTML) k += (String(x.contents || "").match(/data-dz-widget=/g) || []).length; for (const v of Object.values(x)) if (v && typeof v === "object") walk(v); };
  walk(layout);
  return k;
};

/* La vue « dz_ecran » (une seule pour tous les blocs), créée si elle manque, sur la table « dz_ecran_reglages ».
   Cette table reste vide : Saltcorn ne garde, dans l'état fixe d'une vue posée dans une page, que les clés qui sont
   des champs de sa table ; elle sert donc seulement à déclarer les réglages. */
const TABLE = "dz_ecran_reglages";
const assurerVue = async () => {
  const View = require("@saltcorn/data/models/view"), Table = require("@saltcorn/data/models/table"), Field = require("@saltcorn/data/models/field");
  const db = require("@saltcorn/data/db");
  const st = () => require("@saltcorn/data/db/state").getState();
  let fait = false;
  let t = Table.findOne({ name: TABLE });
  if (!t && (await db.selectMaybeOne("_sc_tables", { name: TABLE }))) { await st().refresh_tables(true); t = Table.findOne({ name: TABLE }); }
  if (!t) { t = await Table.create(TABLE, { min_role_read: 1, min_role_write: 1, description: "Réglages des blocs « DZ Écran » (table vide, ne pas remplir)" }); fait = true; }
  const have = new Set(t.getFields().map((f) => f.name));
  for (const [name, label] of CHAMPS) if (!have.has(name)) { await Field.create({ table: t, name, label, type: "String", required: false }); fait = true; }
  await st().refresh_tables();
  t = Table.findOne({ name: TABLE });
  if (!View.findOne({ name: NOM_VUE }) && !(await db.selectMaybeOne("_sc_views", { name: NOM_VUE }))) {
    await View.create({ name: NOM_VUE, viewtemplate: "DZ Écran", table_id: t.id, configuration: {}, min_role: 100, description: "Blocs d'écran de dysizz-ui (réglés dans chaque page)" });
    fait = true;
  }
  try { await st().refresh_views(); } catch (e) { /* rien */ }
  return fait;
};

module.exports = {
  name: "DZ Écran",
  description: "Un bloc d'écran de dysizz-ui (liste, chiffres, graphique, filtres, fiche…). Pose la vue « dz_ecran » dans une page, choisis « État : fixe » et règle le bloc dans la colonne de droite.",
  display_state_form: false,
  get_state_fields: async () => CHAMPS.map(([name, label, sublabel, o = {}]) => ({
    name, label, sublabel: sublabel || "", type: texteSansPreset(), required: false,
    ...(o.options ? { attributes: { options: o.options } } : {}), ...(o.area ? { fieldview: "textarea" } : {}),
  })),
  configuration_workflow: () => {
    const Workflow = require("@saltcorn/data/models/workflow");
    const Form = require("@saltcorn/data/models/form");
    return new Workflow({ steps: [{ name: "Réglages", form: async () => new Form({ blurb: "Rien à régler ici : chaque bloc se règle dans la page, en choisissant « État : fixe » sur la vue posée.", fields: [] }) }] });
  },
  run: async (table_id, viewname, cfg, state) => balise(state || {}),
  NOM_VUE, TABLE, balise, lireWidget, convertirBloc, convertirLayout, widgetsHTML, assurerVue,
};
