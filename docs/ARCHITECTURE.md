# Architecture du dépôt

```
index.js            ← GÉNÉRÉ : le plugin complet (ce que Saltcorn installe)
package.json        ← version du plugin (SemVer), aucune dépendance de dev
src/                ← code serveur du plugin (CommonJS)
  index.js            point d'entrée : réglages, en-têtes, routes
  core.js             constantes (version, URL des fichiers), utilitaires
  settings.js         réglages par tenant et leur nettoyage
  headers.js          ce qui est injecté dans chaque page
  assets.js           fichiers servis depuis la mémoire (brotli/gzip, ETag, cache 1 an)
  pluginCfg.js        lecture / écriture de la config du plugin (+ synchro multi-nœud)
  admin/              pages /dysizz-ui : accueil, atelier, classes, transitions
styles/             ← CSS source : 00-29 = cœur (chargé partout), 30+ = familles
client/             ← JS navigateur : dz.js (moteur), smooth.js (Lenis), editor-*.js
tools/              ← outils de construction et de contrôle (jamais installés sur le serveur)
  build.mjs           construit tout → index.js
  build_packs.py      blocs historiques + chargement de tools/packs/*.py
  packs/              un fichier par famille de blocs
  html2layout.py      HTML → éléments natifs du builder
  builder-parity.mjs  règles CSS de l'éditeur générées depuis le CSS du kit
  class-catalog.mjs   catalogue « ce qu'il y a derrière chaque classe »
  class-docs.mjs      descriptions et exemples des classes principales
  preview.mjs         captures et contrôles de chaque bloc
blocks/             ← blocs écrits à la main en .html (ajoutés au kit)
tests/              ← tests (convertisseur, chargement du plugin)
docs/               ← BLOCKS.md (écrire des blocs), SCALING.md (production), ce fichier
deploy/             ← docker-compose de production
```

## Flux de construction

1. `build_packs.py` : blocs (HTML) → mises en page natives Saltcorn (`build/blocks.json`), familles, pages de démo.
2. CSS : cœur concaténé + une feuille par famille + CSS de l'éditeur (parité builder), minifiés par esbuild.
3. JS navigateur empaqueté et minifié (esbuild).
4. Tout est embarqué dans `src/generated/embed.js`, puis `src/` est empaqueté en `index.js`.

## Règles

- On modifie `src/`, `styles/`, `client/`, `tools/packs/`, jamais `index.js`.
- Chaque changement : `cd tools && node build.mjs`, puis commit de `index.js` (la CI vérifie qu'il est à jour).
- Montée de version : `package.json` + `CHANGELOG.md`. La version entre dans les URL des fichiers : les navigateurs et le cache reprennent la nouvelle version tout de suite.
- Données propres à un tenant : dans Saltcorn (table `dz_classes`, config du plugin), jamais dans le dépôt.
