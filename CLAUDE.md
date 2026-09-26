# dysizz-ui — design system Dysizz pour Saltcorn

À lire d'abord, pour les trois dépôts (ui, flow, me) : `docs/VISION.md`,
`docs/DECISIONS.md`, `docs/AUDIT.md`. Une décision de `DECISIONS.md` ne se rediscute pas.

## Stack
- Plugin Saltcorn **1.6.2** (épinglé, pas de bêta), Node ≥ 18, PostgreSQL 16, multi-tenant.
- Frères : `saltcorn-dysizz-flow` (blocs workflow), `saltcorn-dysizz-me` (modules perso, faits avec ui + flow).
- Structure : `docs/ARCHITECTURE.md`. Production et sécurité : `docs/SCALING.md`, `deploy/`.

## Commandes
- Build : `cd tools && npm ci && node build.mjs` (Python 3 + `pillow pyyaml` requis).
- Tests : `python tests/test_html2layout.py` ; `node tests/load-plugin.cjs` ;
  contrôle visuel : `cd tools && node preview.mjs all` (Playwright, Chromium).
- `npm test` est cassé (pointe vers `tests/run.mjs`, absent).

## Règles
- `index.js` est GÉNÉRÉ : on modifie `src/`, `styles/`, `client/`, `tools/packs/`, `blocks/`,
  puis on reconstruit et on commite `index.js` (la CI vérifie qu'il est à jour).
- Nouvelle version : `package.json` + `CHANGELOG.md` (la version entre dans les URL des fichiers).
- Données d'un tenant : dans Saltcorn (table `dz_classes`, config du plugin), jamais dans le dépôt.
- **Dépôt public** : aucun secret, IP, domaine interne ni détail de faille exploitable.
- Instance réelle : analyse, puis simulation sans écriture, puis écriture.
- Français simple dans l'UI, les commits et la doc.

## Pièges Saltcorn
- Rôles inversés : 1 admin, 40 staff, 80 user, 100 public (plus petit = plus de droits).
- Racine servie sur un sous-domaine en multi-tenant : transactions HTTP inactives (`docs/SCALING.md` §6).
- Réglage de plugin modifié : rechargement forcé par `src/pluginCfg.js` (sinon visible après redémarrage).
- Un tenant ne peut installer un plugin GitHub que si la racine coche *Install git plugins* (voir AUDIT F8).
- Le code Saltcorn de référence n'est pas dans le dépôt : `npm pack @saltcorn/server@1.6.2 @saltcorn/data@1.6.2`.
