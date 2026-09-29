# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions [SemVer](https://semver.org/lang/fr/).

## 3.12.0

### Ajouté
- **Bloc « fiche »** : formulaire relié à une table, à la place des vues d'édition natives de Saltcorn.
  - Il affiche les libellés en français, avec des listes déroulantes à noms lisibles : les clés vers une autre table et les listes de choix, avec `libelles`.
  - Il gère les sections, les aides, les champs obligatoires et les champs montrés sous condition (`si`).
  - Les champs protégés sont en lecture seule ; les champs peuvent aussi être cachés (`caches`) ou remplis avec l'utilisateur (`utilisateur`).
  - Il sait créer, modifier et supprimer, avec une adresse de retour après enregistrement.
  - L'écriture passe par l'API de Saltcorn : droits, propriétaire, champs `min_role_write` et déclencheurs Validate / Insert / Update restent vérifiés par le serveur.
  - Route de lecture : `GET /dysizz/fiche/:table`. Elle ne renvoie que les lignes et les listes que l'utilisateur peut lire.
- **Navigation** (réglages du plugin, nouvelle étape) :
  - forme du menu (latéral / en haut / laisser le thème) ;
  - nom et logo du site affichés ou non ;
  - entrée « Accueil » (coupée par défaut, retirée du menu si elle y est) ;
  - entrées réservées à l'administrateur en ambre.
  Tout est appliqué dès l'enregistrement, dans le tenant.
- Menu : l'entrée active est celle dont les paramètres correspondent à l'adresse (`/page/gestion?t=equipe`), y compris quand un onglet ou un filtre change l'adresse sans recharger la page.
- Mise en page d'application sans CSS propre à la page : `dz-ecran`, `dz-ecran-titre`, `dz-ecran-intro`, `dz-ecran-grille` (+ `dz-ecran-chiffres`, `dz-ecran-tuiles`, `dz-ecran-principale`, `dz-ecran-moities`), `dz-ecran-col`, `dz-ecran-note`, `dz-ecran-bt`, `dz-ecran-retour`, `dz-ecran-niveau`.

### Corrigé
- Barre de filtres : l'onglet ou le choix affiché suit l'adresse. Avant, en cliquant « Équipe », l'ancien onglet restait en surbrillance ; un filtre posé ailleurs (clic sur un chiffre, retour arrière) n'était pas reflété.

### Changé
- L'entrée « Accueil » n'est plus ajoutée d'office au menu. Elle se règle dans Navigation (réglage `dysizz_menu_accueil` abandonné).

## 3.11.0

### Ajouté
- Bloc « tableau », listes regroupées : `grouper` (une colonne, ex. l'agence) affiche un en-tête par groupe avec son nombre de lignes ; un clic replie ou déplie le groupe, « Tout ouvrir / Tout fermer » pour survoler. `replie` : les groupes arrivent fermés, sauf un petit résultat (recherche, filtre) qui reste ouvert. `sans-groupe` : libellé des lignes sans valeur.
- Filtres : un choix peut en exclure d'autres (`exclut`, ex. la période « 90 jours » et les dates libres). Poser une date retire le raccourci, même par défaut ; la liste affiche alors `libre` (ex. « — dates choisies — »). Choisir « Tous » sur un filtre qui a une valeur par défaut garde ce choix.
- Bloc note : plusieurs boutons (`boutons`, `[["/view/x", "Ajouter"], ["/page/y", "Autre", "sec"]]`), liens internes seulement.
- Sources : dates relatives `@+7j` / `@-30j` (minuit local, dans N jours ou il y a N jours), en plus de `@maintenant` et `@aujourdhui`.

### Corrigé
- Une colonne au titre vide (`"titre": ""`) n'affiche plus le nom du champ ; dans une fiche, une ligne sans titre (un bouton) prend toute la largeur au lieu de déborder.
- Contrôle visuel (`tools/preview.mjs`) : les vidéos sont masquées dans la comparaison bloc natif / bloc du builder ; selon la vitesse de la machine, la première image était chargée dans une photo et pas dans l'autre (« Site · vidéo » échouait parfois en CI).

## 3.10.0

### Ajouté — refaire une interface existante sans code propre
- Sources : filtres `min` / `max` (aussi sur une colonne texte qui contient un nombre, ex. « 85 m² »), `commence` (référence qui commence par…), `choix` (valeur de l'adresse → condition déclarée, ex. `?bien=0` → « sans bien »), période glissante `?j=7` et noms de paramètres réglables. Valeurs liées (`enfants`) reliées par une autre colonne que `id` (`cle`).
- Bloc « tableau » :
  - chiffre clé en pourcentage d'un autre (`sur`), cliquable pour filtrer (`clic`), en alerte (`alerte`) ;
  - cellules riches : plusieurs lignes par cellule (`lignes`), pastilles conditionnelles (`badges`), liens modèles `{champ}`, formats `age` et `jour` ;
  - listes : lignes à surveiller (`attention`), message vide, total ; vue **grille** (tuiles) et bascule grille/tableau ;
  - **document** : lecture d'un e-mail d'origine dans une fenêtre isolée (aucun script exécuté) ;
  - filtres nombre, boutons, étiquettes des filtres actifs avec « Tout effacer » ;
  - bloc masqué quand le rôle n'a pas le droit (`masquer-refus`).
- Bloc « tableau » : `niveau="admin"` affiche le bloc avec la couleur et l'étiquette « Administrateur » (on voit d'un coup d'œil ce que le siège ne voit pas).
- Menu : l'entrée « Accueil » (vers /dysizz) n'est ajoutée qu'une fois ; si l'admin la retire, elle ne revient plus au redémarrage.
- Actualisation automatique sans clignotement : rien n'est redessiné si les données n'ont pas changé ; relecture au retour sur l'onglet.
- Sources, suite : filtre `lien` (valeur lue dans une autre table, ex. l'e-mail d'origine d'une demande), `sauf` (exclure une ligne), option par défaut d'un `choix` (ex. doublons repliés sauf `?tout=1`), mesure `taux` (part des lignes qui remplissent une condition, en %), conditions `ou`. Un identifiant illisible donne « aucun résultat », jamais une erreur.
- Bloc « tableau », suite : vue `titre` (en-tête de fiche), vue `note` (texte et bouton), `montrer` (bloc affiché pour un onglet `?t=…`), lien lu dans une colonne (`@champ`, adresses du site seulement), listes de filtres étiquetées depuis une source, âge en pastille colorée, formats `heure`, `ms`, `brut`, textes longs coupés (`court`), colonnes sans retour à la ligne (`nowrap`), modèles qui retirent les morceaux vides (« Maison · 4 pièces » sans « · m² »).

## 3.9.0

### Ajouté — tableaux de bord calculés par la base
- **Sources de données** (`/dysizz-ui/sources`, table `dz_sources` du tenant) : chiffres (`agregat`, avec comparaison à la période précédente), courbes (`serie` par heure, jour, semaine, mois, année, jours vides à 0, au fuseau du site) et listes paginées et triables (`liste`, avec valeurs de tables liées). Lecture en JSON : `GET /dysizz/donnees/<nom>`.
- Filtres déclarés dans la source et seuls acceptés : égalité (une ou plusieurs valeurs), période (`aujourdhui`, `7j`, `30j`, `90j`, `12m` ou `du`/`au`), vide, recherche (y compris dans les tables liées).
- Listes : valeurs de la ligne parente (`parents`, ex. le nom de l'assistante d'une personne). Conditions à dates relatives `@maintenant` / `@aujourdhui` (congés en cours, tickets en retard), « commence par », « contient », « vide ».
- **Bloc « tableau »** (`data-dz-widget="tableau"`) : chiffre clé, courbe, barres, anneau, liste, fiche (une ligne en libellé → valeur), boutons d'action dans les listes, paramètres tirés de l'adresse (`params="ticket={id}"`), et barre de filtres partagée. Les filtres vivent dans l'adresse : un lien filtré se partage, Retour fonctionne, et changer un filtre ne relit que les blocs, sans recharger la page. Clic sur une barre = filtre. Lisible sur téléphone.

### Sécurité
- Seul un administrateur crée une source ; chaque nom de champ est vérifié contre la table, toutes les valeurs de l'adresse passent en paramètres SQL.
- Lecteur : rôle suffisant pour la source et pour chaque table lue (propriété des lignes respectée).
- Requête en lecture seule sur une connexion dédiée, arrêtée au bout de 5 s ; cache court par tenant et par rôle.

### Tests
- `tests/donnees.test.cjs` contre un vrai PostgreSQL (résultats, fuseau horaire, injections, droits, lecture seule, cache), ajouté à la CI avec un service PostgreSQL 16.
- Bloc « tableau » utilisé comme un humain dans `tests/widgets.test.mjs`.

## 3.8.0

### Ajouté — des briques pour construire des outils (famille Interactif)
- **Parcours** : éditeur visuel de processus (étapes, conditions oui/non, validations, fin, ou palette sur mesure) ; panneau de réglages, souris, doigt, clavier, zoom, contrôle du schéma, lecture seule avec étapes passées et en cours. Exécuté pour de vrai par le bloc dysizz-flow « Exécuter un parcours » (2.4.2).
- **Formulaire** : constructeur (11 types de questions, aperçu en direct) et remplissage (obligatoires et formats vérifiés en direct, envoi bloqué tant qu'il reste une erreur).
- **Règles** : conditions « si … et/ou … » par menus, relues en français, expression prête pour les parcours (chaque valeur saisie reste du texte, jamais du code).
- **Document** : éditeur par blocs façon Notion, menu « / », clavier complet, HTML nettoyé.
- **Planning** : semaine en glisser-déposer, clavier, un jour à la fois sur téléphone.
- Chacune : affichages de champ (saisie et lecture) et bloc de démonstration.

### Ajouté — design
- **8 nouveaux univers** : Néon, Pastel, Institution, Rétro, Nature, Suisse, Océan, Sahel (clair et sombre, polices dédiées), soit 14 identités.
- Matière **« doux »** (grands arrondis, ombres diffuses).
- Polices : Unbounded, Nunito, IBM Plex Sans, Rubik, Lora, Syne.

### Corrigé / UX
- Variables CSS passées en style aux widgets jamais appliquées (couleurs par type restées bleues).
- « null » affiché sous les questions sans aide.
- Boutons clés qui perdaient leur libellé sur téléphone.
- Cibles tactiles d'au moins 44 px au doigt (boutons du kit et des widgets).

### Tests
- `tests/widgets.test.mjs` : chaque brique utilisée comme un humain dans Chromium (clics, glisser, clavier, mobile), dans `npm test` et la CI.

## 3.7.0

### Ajouté
- **Page Santé et sécurité** (`/dysizz/sante`, tuile sur `/dysizz`) : 16 vérifications en feux tricolores, expliquées en mots simples — double authentification, inscriptions, mots de passe, sauvegardes (automatiques, hors serveur, chiffrées), e-mail chiffré, données et actions ouvertes au public, pages ou vues en double, **test réel des transactions** (avec la cause probable si elles ne marchent pas), clé du coffre, cookies sécurisés derrière le proxy, CORS, en-têtes HTTP, plugins GitHub pour les tenants, versions. Chaque correction montre d'abord ce qui va changer (rien n'est écrit), puis s'applique en un clic. Réservée aux admins ; les réglages du serveur n'apparaissent que dans le tenant racine.
- `docs/DEMARRAGE.md` : mettre une instance en sécurité pas à pas (secrets, Dokploy en HTTPS, sauvegardes hors serveur, mises à jour, tenants confiés à des tiers).

### Corrigé
- **Texte qui s'écrit, bouton Copier, effet 3D** : le marqueur « déjà initialisé » écrasait leur réglage (même attribut). Le texte ne s'animait jamais et les blocs du builder affichaient « mot 1 | mot 2 | mot 3 » en entier (hero 400 px trop haut) ; Copier copiait « 1 » ou ne réagissait pas ; la 3D tombait à 1°. Test navigateur ajouté (`tests/dz-client.test.mjs`).
- **Débordement horizontal sur mobile** causé par les textes réservés aux lecteurs d'écran (`.visually-hidden`) placés dans une zone qui défile : ils sont ancrés à leur bloc conteneur. Premier cas trouvé : « App · table d'administration ».
- Page d'accueil `dysizz-accueil` : plus de doublon sur double clic (existence vérifiée en base).

### Contrôle qualité
- Le contrôle visuel rend enfin la variante mobile **à 390 px** (tout était rendu en 1280 px, le débordement mobile n'était jamais détecté), démarre les widgets interactifs, reconnaît les blocs flottants, nomme l'élément qui déborde, et **fait échouer la CI** sur un vrai défaut (débordement, erreur JS, bloc invisible, écart ≥ 2 %).
- CI : fichier de workflow valide (elle ne démarrait jamais) ; `npm test` lance la vraie suite.

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
