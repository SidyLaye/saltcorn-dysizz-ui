# dysizz-ui — design system Dysizz pour Saltcorn

À lire d'abord, pour les trois dépôts (ui, flow, me) : `docs/VISION.md`,
`docs/DECISIONS.md`, `docs/AUDIT.md`. Une décision de `DECISIONS.md` ne se rediscute pas.

## Stack
- Plugin Saltcorn **1.6.2** (épinglé, pas de bêta), Node ≥ 18, PostgreSQL 16, multi-tenant.
- Frères : `saltcorn-dysizz-flow` (blocs workflow), `saltcorn-dysizz-me` (modules perso, faits avec ui + flow).
- Structure : `docs/ARCHITECTURE.md`. Production et sécurité : `docs/SCALING.md`, `deploy/`.

## Commandes
- Build : `cd tools && npm ci && node build.mjs` (Python 3 + `pillow pyyaml` requis).
- Tests rapides : `cd tools && npm test` (chargement, page Santé, moteur navigateur) ;
  `python tests/test_html2layout.py`.
- Contrôle visuel : `cd tools && node preview.mjs all` (~20 min, 411 blocs × clair/sombre/mobile 390 px ;
  échoue sur débordement, erreur JS, bloc invisible, écart ≥ 2 % ; `--only "<nom>"`, `--no-fail`).
  Ne jamais le lancer en même temps qu'un build : il lit `build/`.

## Règles
- `index.js` est GÉNÉRÉ : on modifie `src/`, `styles/`, `client/`, `tools/packs/`, `blocks/`,
  puis on reconstruit et on commite `index.js` (la CI vérifie qu'il est à jour).
- Nouvelle version : `package.json` + `CHANGELOG.md` (la version entre dans les URL des fichiers).
- Données d'un tenant : dans Saltcorn (table `dz_classes`, config du plugin), jamais dans le dépôt.
- **Dépôt public** : aucun secret, IP, domaine interne ni détail de faille exploitable.
- Instance réelle : analyse, puis simulation sans écriture, puis écriture.
- Français simple dans l'UI, les commits et la doc.

## À connaître
- `/dysizz/sante` (`src/admin/sante.js`) : diagnostic du tenant ; toute correction = aperçu puis clic.
- `client/dz.js` : `once(el, clé)` écrit `data-dz-<clé>` ; la clé ne doit jamais être un attribut de réglage.
- Pas à pas serveur pour Sidy : `docs/DEMARRAGE.md`.

## Pièges Saltcorn
- Rôles inversés : 1 admin, 40 staff, 80 user, 100 public (plus petit = plus de droits).
- Racine servie sur un sous-domaine en multi-tenant : transactions HTTP inactives (`docs/SCALING.md` §6).
- Réglage de plugin modifié : rechargement forcé par `src/pluginCfg.js` (sinon visible après redémarrage).
- Un tenant ne peut installer un plugin GitHub que si la racine coche *Install git plugins* (voir AUDIT F8).
- Pas de nom unique pour pages, vues, déclencheurs, et `findOne` lit un cache : vérifier en base avant de créer.
- Le code Saltcorn de référence n'est pas dans le dépôt : `npm pack @saltcorn/server@1.6.2 @saltcorn/data@1.6.2`.
