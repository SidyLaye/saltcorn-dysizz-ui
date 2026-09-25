# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions [SemVer](https://semver.org/lang/fr/).

## 3.6.2

- Vidéos YouTube : fin de l'erreur 153. Saltcorn envoie « Referrer-Policy: same-origin », donc YouTube ne recevait pas l'adresse du site. Chaque lecteur YouTube de la page (y compris dans les anciennes vues et les fenêtres) reçoit sa propre règle et le paramètre origin, puis se recharge une fois.

## 3.6.1

- Mails en texte arrivés « à plat » (retours à la ligne perdus) : les lignes de citation et « Le … a écrit : » sont reconstituées, l'historique est replié.

## 3.6.0

- **Blocs interactifs** (famille « Interactif ») chargés seulement là où ils servent : visionneuse et **modeleur 3D** (three.js : formes, déplacer/tourner/taille, couleurs, import GLB/STL/OBJ, export GLB/STL, annuler), **mini-moteur de jeux** avec serpent, casse-briques, 2048, mémoire, morpion, coureur, quiz et jeu à coder soi-même, **carte** (Leaflet/OpenStreetMap, points d'une table, choisir une position), **tableur** (formules en français, copier-coller Excel, CSV), **tableau blanc**, **signature**, **chat IA** (intégré ou en bulle), **portefeuille crypto** (connexion, signature, paiement), **planning Gantt**, **scanner** QR / code-barres et photo.
- Nouveaux champs (fieldviews) : signature, position sur carte, tableur, tableau blanc, modeleur / visionneuse 3D, scanner, photo, image.

## 3.5.0

- Nouvelle vue **DZ Disponibilité** : page de statut, une barre par jour et par service, % de disponibilité (calcul fait par Postgres).
- Mails : historique des réponses replié (texte et HTML Gmail / Outlook / Apple), bouton pour le déplier.
- Images d'articles avec vignette de couleur quand il n'y en a pas, logos d'entreprise sur les offres, lien « Ouvrir sur YouTube » sous le lecteur.

## 3.4.0

- **Accueil façon Windows 8** sur `/dysizz` : une tuile par appli (Me et ses modules), outil Dysizz (kit UI, workflows) et page d'administration Saltcorn, avec des infos en direct (mails non lus, workflows en erreur…), recherche au clavier, clair / sombre. Ajouté en tête du menu Saltcorn ; bouton « Ouvrir ici à la connexion ». Les autres plugins ajoutent leurs tuiles avec l'export `dysizz_hub`.
- Affichage de champ **dz_mail** : corps d'e-mail HTML dans un cadre isolé (aucun script, images distantes bloquées jusqu'au clic, liens dans un nouvel onglet), ou texte lisible (retours à la ligne, liens, citations).
- Bandeau « à régler » pour les solutions, graphique plus lisible sur téléphone.

## 3.3.0

- 4 nouvelles vues : **DZ Graphique** (courbe, aire, barres dans le temps, regroupement fait par Postgres, plusieurs séries), **DZ Calendrier** (mois en grille, ajout et modification en fenêtre), **DZ Journal** (fil d'événements filtrable), **DZ Statut** (état des services). Voir docs/VUES.md.
- Elles vont de pair avec dysizz-flow 2.0 : métriques (`dzf_mesures`), journal (`dzf_journal`), surveillance de sites.

## 3.2.0

- 4 vues de données, disponibles dans tous les tenants : **DZ Indicateurs** (chiffres clés), **DZ Tableau** (kanban glisser-déposer), **DZ Répartition** (barres avec objectif), **DZ À venir** (frise des prochains jours). Voir docs/VUES.md.
- Styles « vues de données et coquille d'application » (préfixe `dzv-`) : menu latéral, barre du bas mobile, panneaux, cartes, listes, lecteur de mail, articles, vidéos, formulaires. Utilisés par les solutions construites avec le kit.
- Script : puces de filtre actives, glisser-déposer du kanban, salutation du jour.

## 3.1.0

- Une page de démo par famille (`dz-famille-<famille>`, 17 pages) : tous les blocs de la famille, avec leur nom, modifiables et copiables dans l'éditeur de pages. Navigation entre familles en haut de chaque page.
- Le catalogue (`dz-catalogue`) ouvre ces pages ; la galerie admin reste accessible (`/dysizz-ui/galerie?f=all`).
- Les éléments fixes (barres, tiroirs, boutons flottants) sont montrés dans un cadre pour ne pas recouvrir la page.

## 3.0.1 — 2026-09-24

### Corrigé
- La page `dz-catalogue` liste maintenant les 17 familles et les 390 blocs (elle ne montrait que les blocs de la v2).
- Galerie : option « Tout » (`/dysizz-ui/galerie?f=all`) ; les éléments fixes (menu, bandeau cookies, palette, tiroirs) sont montrés dans un cadre au lieu de disparaître.
- Cartes cliquables : plus de texte souligné.

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
