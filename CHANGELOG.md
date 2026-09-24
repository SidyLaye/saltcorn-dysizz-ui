# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions [SemVer](https://semver.org/lang/fr/).

## 3.0.0 — 2026-09-24

### Ajouté
- **390 blocs en 17 familles** à noms génériques (Site, App, Projet, Support, Mail, Commerce, Finance, Données, Agenda, Social, Contenu, Média, Compte, Équipe, Mobile, Outil, Insolite), installables famille par famille sur `/dysizz-ui`.
- **Blocs modifiables sans code** : chaque bloc est converti à la construction en éléments natifs du builder (conteneurs, textes, liens, images) ; seuls les morceaux techniques (SVG, champs, tableaux) restent en code.
- **Classes « sans code »** pour tous les comportements (`dz-counter`, `dz-typewriter`, `dz-reveal-zoom`, `dz-open-<id>`…), utilisables depuis le champ « classe » du builder.
- **Atelier de blocs visuel** : clic pour sélectionner, texte, lien, image, icône, classes (autocomplétion), couleurs, marges, animation, palette d'éléments, annuler / rétablir, aperçu bureau / mobile / clair / sombre, mode code.
- **Page Classes** : le CSS derrière chaque classe du kit avec aperçu, recherche, et **classes perso** (éditeur visuel ou code) stockées dans une table Saltcorn `dz_classes`, compilées dans la config du plugin.
- **Transitions entre sections** (12), **défilement doux** (Lenis), **sections aimantées**, **fond qui change de couleur**, **bords de sections** (vague, pente, courbe…), réglables par tenant, par page et par section. Page d'essai `/dysizz-ui/transitions`.
- Galerie par famille `/dysizz-ui/galerie`.
- Compose de production : nœuds multiples, cache HTTP nginx, Redis (limites de débit partagées).
- Tests (convertisseur, chargement du plugin, contrôle visuel de tous les blocs) et CI GitHub Actions.

### Modifié
- **Défilement** : parallaxe, texte mot à mot, défilement horizontal et barre de progression animés par le navigateur (`animation-timeline`) ; plus aucune écriture de style pendant le défilement (temps de rendu divisé par ~3).
- CSS du cœur seul chargé partout (17 Ko compressé) ; chaque famille a son fichier, chargé seulement si elle est activée ; le CSS du builder n'est chargé que dans l'éditeur.
- Parité builder générée automatiquement pour toutes les classes de mise en page.
- Code source découpé en modules (`src/`, `styles/`, `client/`), construit par esbuild en un seul `index.js`.
- Onglets `dz-tabs` utilisables sans attributs `data-tab`.

### Sécurité
- Les fichiers du kit ne posent plus de cookie de session (cache partagé possible).

## 2.2.0
- Atelier de blocs (HTML/CSS/JS), export / import. Premier guide de production.

## 2.1.0
- Chargement rapide : apparitions en CSS, suppression de `:has()`, fichiers pré-compressés.

## 2.0.0
- 6 univers, 72 blocs, habillage des vues natives.
