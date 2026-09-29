/* dysizz-ui — navigation : entrée « Accueil », menu latéral, entrées réservées à l'administrateur.
   Réglée dans la configuration du plugin (étape « Navigation »), appliquée au chargement du
   plugin, donc aussitôt après l'enregistrement des réglages et dans chaque tenant. */
"use strict";

/* l'entrée « Accueil » (vers l'accueil Dysizz), telle que dysizz-ui l'ajoute */
const ACCUEIL = { type: "Link", text: "Accueil", label: "Accueil", url: "/dysizz", href: "/dysizz", icon: "fas fa-th-large", min_role: 1, max_role: "1", style: "", title: "", tooltip: "", target: "_self", target_blank: false, in_modal: false, location: "Standard", shortcut: "", disable_on_mobile: false };
const estAccueil = (x) => x && (x.url === "/dysizz" || x.href === "/dysizz");

/* Saltcorn affiche « unrolled_menu_items » s'il existe (menu déplié), sinon « menu_items » : on règle les deux */
const menuAccueil = async (voulu) => {
  const { getState } = require("@saltcorn/data/db/state");
  const st = getState();
  for (const key of ["menu_items", "unrolled_menu_items"]) {
    const items = st.getConfig(key, null);
    if (!Array.isArray(items) || (key === "unrolled_menu_items" && !items.length)) continue;
    const present = items.some(estAccueil);
    if (voulu && !present) await st.setConfig(key, [ACCUEIL, ...items]);
    if (!voulu && present) await st.setConfig(key, items.filter((x) => !estAccueil(x)));
  }
};

/* forme du menu du thème any-bootstrap-theme : « latéral » (Side Navbar) ou « en haut » (Top Navbar) */
const STYLES_MENU = { "latéral": "Side Navbar", "en haut": "Top Navbar" };
const menuTheme = async (choix) => {
  const voulu = STYLES_MENU[choix];
  if (!voulu) return; /* « thème » : on ne touche à rien */
  const Plugin = require("@saltcorn/data/models/plugin");
  const theme = (await Plugin.find({})).find((p) => p.name === "any-bootstrap-theme");
  if (!theme || (theme.configuration || {}).menu_style === voulu) return;
  theme.configuration = { ...(theme.configuration || {}), menu_style: voulu };
  await theme.upsert();
  await Plugin.loadPlugin(theme);
};

const appliquer = async (cfg) => {
  try { await menuAccueil(!!cfg.nav_accueil); } catch (e) { /* pas bloquant */ }
  try { await menuTheme(cfg.nav_menu); } catch (e) { /* pas bloquant */ }
};

/* GET /dysizz/nav-niveaux : pour l'administrateur, les liens et sections du menu réservés au rôle 1,
   que la page colore en ambre. Pour tout autre visiteur : rien (il ne voit pas ces entrées). */
const niveaux = async (req, res) => {
  const vide = { liens: [], sections: [] };
  if (!req.user || req.user.role_id !== 1) return res.json(vide);
  const { getState } = require("@saltcorn/data/db/state");
  const st = getState();
  const items = st.getConfig("unrolled_menu_items", null) || st.getConfig("menu_items", []) || [];
  const out = { liens: [], sections: [] };
  const url = (x) => (x.type === "Page" && x.pagename ? `/page/${x.pagename}` : x.type === "View" && x.viewname ? `/view/${x.viewname}` : x.url || null);
  const parcourir = (liste, parentAdmin) => {
    for (const x of liste || []) {
      if (!x) continue;
      const admin = parentAdmin || +x.min_role === 1;
      if (Array.isArray(x.subitems) && x.subitems.length) {
        if (+x.min_role === 1 && x.label) out.sections.push(String(x.label));
        parcourir(x.subitems, admin);
      } else if (admin && !estAccueil(x)) {
        const u = url(x);
        if (u) out.liens.push(u);
      }
    }
  };
  parcourir(items, false);
  res.json(out);
};

module.exports = { appliquer, niveaux, menuAccueil, menuTheme, ACCUEIL, STYLES_MENU };
