# Dysizz UI — kit de design pour Saltcorn

Plugin Saltcorn (1.6.x) qui apporte :

- un **design system** clair / sombre en **6 univers** (Nocturne, Éditorial, Studio, Aurora, Terre, Luxe) et l'habillage des vues natives ;
- un **accueil façon Windows 8** (`/dysizz`) qui mène à toutes tes applis, aux outils Dysizz et à l'administration Saltcorn ;
- **8 vues de données** branchées sur tes tables : Indicateurs, Tableau (kanban), Répartition, À venir, Graphique, Calendrier, Journal, Statut (voir [docs/VUES.md](docs/VUES.md)) ;
- **390 blocs** en **17 familles** : Site, App, Projet, Support, Mail, Commerce, Finance, Données, Agenda, Social, Contenu, Média, Compte, Équipe, Mobile, Outil, Insolite ;
- des blocs **modifiables sans code** dans le builder (éléments natifs : clic sur un texte pour l'écrire, sur un conteneur pour ses classes, couleurs, marges, animation) ;
- un **atelier visuel** pour créer ou modifier des blocs (sans code ou en code) ;
- une page **Classes** : ce qu'il y a derrière chaque classe, et **tes propres classes** (éditeur visuel ou code) ;
- des **transitions entre sections**, le **défilement doux**, l'aimantation, des **bords de sections** ;
- un moteur d'animations léger, qui ne calcule rien pendant le défilement ;
- un **guide de production** (plusieurs serveurs, cache, Redis, sécurité) et un compose prêt.

---

## 1. Installation (une seule fois)

### a. Mettre le code sur GitHub

Crée le dépôt **public** `SidyLaye/saltcorn-dysizz-ui` et pousse ce dossier (tel quel, `index.js` à la racine). La source « github » de Saltcorn télécharge `https://api.github.com/repos/<location>/tarball` sans authentification : un dépôt privé échoue. Pour un dépôt privé, prends la source « git » avec une clé de déploiement SSH.

### b. Réglages du tenant racine

Dans le tenant racine : **Settings → Site structure → Multitenancy** (`/tenant/settings`). « Install git plugins » est dans la rubrique *Tenant application capabilities*. Ce menu n'apparaît que dans le tenant racine, et seulement si le multi-tenant est activé.

| Réglage | Valeur | Pourquoi |
|---|---|---|
| Install git plugins | ✅ | sans ça, un tenant ne peut pas installer un plugin GitHub |
| New tenant template | `modele` (voir plus bas) | chaque nouveau tenant copie ce modèle |

### c. Installer le plugin

**Settings → Modules**, menu déroulant en haut à droite → **Add another module** (adresse directe : `/plugins/new`) :

- Name : `dysizz-ui` (garde ce nom, la page d'outils s'en sert)
- Source : `github`
- Location : `SidyLaye/saltcorn-dysizz-ui`

Ensuite, ouvre `/dysizz-ui` :

1. **Coche les familles de blocs** utiles à ce tenant, puis « Installer / mettre à jour ».
2. **Installe les pages de démo** si tu veux des exemples (visibles par les admins seulement).
3. **Ouvre les réglages** : univers, couleurs, polices, transitions.

### d. Le tenant modèle (pour tous les futurs tenants)

1. Crée un tenant `modele` (**Settings → Site structure → Tenants**, `/tenant/list`).
2. Dedans : installe le plugin, coche les familles voulues sur `/dysizz-ui`, règle le thème de base.
3. Ajoute ce qui doit être partout : pages légales, page de connexion, rôles, menu, réglages de sécurité.
4. Dans le tenant racine, **New tenant template** = `modele`.

Chaque nouveau tenant démarre alors avec le plugin, les blocs, les pages et le thème. Saltcorn copie le modèle par une sauvegarde + restauration puis supprime les utilisateurs copiés (vérifié dans `admin-models/models/tenant.js`, `copy_tenant_template`).

Pour un tenant **déjà existant** : installe le plugin, puis `/dysizz-ui` → coche les familles.

---


## 2. Utilisation au quotidien

### Choisir un univers

`/plugins/configure/dysizz-ui` → **Univers**. Chaque univers change tout d'un coup : couleurs claires et sombres, polices, forme des boutons, graisse des titres, style des mots mis en valeur.

| Univers | Identité | Pour |
|---|---|---|
| **Nocturne** (défaut) | noir profond, accent citron, sur-titres en mono | tech, SaaS, agence |
| **Éditorial** | papier crème, encre, orange, mots en serif italique | marque perso, conseil, média |
| **Studio** | noir & blanc, bleu électrique, angles vifs, ombres dures | portfolio, créatif, produit |
| **Aurora** | violet / cyan, dégradés | SaaS grand public, IA |
| **Terre** | sable, olive, terracotta, serif doux | artisan, bien-être, immobilier, resto |
| **Luxe** | noir chaud, or, serif | hôtel, mode, premium |

Ensuite, **Matière** (moderne, glass, minimal, brutal) ajuste les ombres et bordures. Tu peux aussi forcer tes couleurs (« Utiliser mes propres couleurs »), tes polices et l'arrondi.

Dans les titres, mets les mots importants en *italique* dans l'éditeur de texte (balise `<em>`) : selon l'univers, ils passent en serif italique, en couleur ou en dégradé.

### Construire une page sans code

1. Page → builder. Panneau **Library** : glisse un bloc (les familles installées apparaissent, préfixées « Site · », « Projet · »…).
2. Clique sur un texte pour l'écrire, sur un bouton pour son lien, sur une image pour son adresse.
3. Clique sur un conteneur : panneau de droite → classes (champ *Custom class*), couleurs, marges, animation Saltcorn, visibilité par écran.
4. Tout ce qui est « technique » (graphique SVG, champ de formulaire, tableau) reste un petit bloc HTML modifiable en code.

Pour **voir tous les blocs d'une famille** : `/dysizz-ui` → « voir » sur la famille (galerie).

### Les classes

`/dysizz-ui/classes` :

- **Classes du kit** : chaque classe, à quoi elle sert, un aperçu, et le CSS exact derrière. Recherche instantanée.
- **Comportements** : les classes qui ajoutent un effet sans code — `dz-counter` (chiffre animé), `dz-typewriter` (machine à écrire), `dz-reveal-zoom` (apparition), `dz-open-<id>` (ouvre un tiroir), `dz-confetti`, `dz-copy`…
- **Mes classes** : crée une classe en visuel (couleurs, texte, espacements, bordure, ombre, disposition, survol, animation, version mobile, version sombre) ou en CSS. Elle est active tout de suite sur toutes les pages du tenant. Elle est stockée dans la table Saltcorn `dz_classes` (visible dans *Tables*, sauvegardée avec le tenant) ; export / import JSON pour les autres tenants.

### L'atelier de blocs

`/dysizz-ui/blocks` :

- **Visuel** : clique un élément de l'aperçu → texte, lien, image, icône, classes (avec autocomplétion de toutes les classes), couleurs, marges, arrondi, taille, apparition ; monter, descendre, dupliquer, supprimer ; palette d'éléments à ajouter ; double-clic pour écrire directement ; annuler / rétablir (Ctrl Z / Ctrl Y).
- **Code** : HTML, CSS limité au bloc, JS optionnel.
- **Partir d'un bloc du kit** pour en faire ta version ; export / import entre tenants.
- Sans l'atelier, dans le builder : sélectionne un élément puis *Library → Add*.

### Transitions et défilement

Réglages du kit (`/plugins/configure/dysizz-ui`) :

| Réglage | Choix |
|---|---|
| Transition entre sections | aucune, fondu, montée douce, zoom, brume, bascule 3D, rideau, balayage, recouvrement, cartes empilées, profondeur, fondu enchaîné |
| Sections aimantées | libre, léger, strict |
| Défilement | natif, doux, très doux (coupé sur mobile, dans les applis et pour ceux qui réduisent les animations) |
| Fond qui change | la page prend la couleur de la section (classe `dz-morph-<couleur>` sur une section) |

Par page : bloc **Outil · réglages de la page** (classes `dz-page-tr-<nom>`, `dz-page-smooth-<…>`, `dz-page-snap-<…>`). Par section : classe `dz-tr-<nom>`. Bords : `dz-edge-wave`, `-slant`, `-curve`, `-arc`, `-zigzag`, `-steps`, `-fade`, `-round-top`. Essai en direct : `/dysizz-ui/transitions`.

### Réglages par tenant

Univers, matière, couleurs, polices, arrondi, largeur, habillage des vues, barre en verre, animations (toujours / selon le visiteur / jamais), curseur, bouton retour en haut, mémoire du thème, transitions, CSS en plus.

---

### Blocs interactifs (famille « Interactif »)

Des blocs vivants, chargés seulement sur les pages qui les utilisent :
3D (visionneuse et modeleur), jeux (serpent, casse-briques, 2048, mémoire,
morpion, coureur, quiz, ou ton propre jeu avec le mini-moteur), carte,
tableur, tableau blanc, signature, chat IA, portefeuille crypto, planning
Gantt, scanner QR / code-barres et photo.

Chaque bloc est un `<div data-dz-widget="nom" data-…>` : on le règle par ses
attributs dans le builder. Dans un formulaire, `data-champ="mon_champ"`
enregistre le résultat dans ce champ. Les mêmes outils existent en
« fieldviews » à choisir sur un champ texte : `dz_signature_saisie`,
`dz_position_carte`, `dz_tableur_saisie`, `dz_tableau_blanc`,
`dz_3d_modeleur`, `dz_3d`, `dz_scanner`, `dz_photo`, `dz_image`…

Le chat IA parle au modèle « Assistant IA pour tes pages » de dysizz-flow,
qui crée l'adresse `/dzf/api/assistant`.

## 3. Performance

- Le cœur du kit pèse **17 Ko** compressé ; chaque famille a son propre fichier (6 à 10 Ko), chargé seulement si elle est cochée pour le tenant. Le CSS de l'éditeur n'est chargé que dans l'éditeur.
- Pendant le défilement, **aucun JavaScript** ne tourne : apparitions, parallaxe, texte mot à mot, défilement horizontal, barre de progression et transitions sont calculés par le navigateur sur le processeur graphique. Mesuré sur la landing (processeur ralenti ×4) : image moyenne 46 ms → 20 ms, images lentes 105 → 9.
- Fichiers pré-compressés (brotli / gzip) en mémoire, cache d'un an, sans cookie.
- Boucles d'animation en pause hors écran ; sections hors écran non dessinées.

Production (plusieurs serveurs, Postgres, cache nginx, Redis, sécurité, transactions) : **[docs/SCALING.md](docs/SCALING.md)** et **[deploy/docker-compose.scale.yml](deploy/docker-compose.scale.yml)**.

---

## 4. Développer le kit

```bash
cd tools && npm install          # une fois
node build.mjs                   # construit index.js
node preview.mjs <famille|all>   # captures + contrôles de chaque bloc
python3 ../tests/test_html2layout.py && node ../tests/load-plugin.cjs
```

- Écrire des blocs : **[docs/BLOCKS.md](docs/BLOCKS.md)**.
- Organisation du code : **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.
- Versions : **[CHANGELOG.md](CHANGELOG.md)**. La CI GitHub construit, teste et vérifie que `index.js` est à jour.

Publier : modifier les sources, augmenter `version` dans `package.json`, `node build.mjs`, commit + push, mettre à jour le module dans Saltcorn, puis `/dysizz-ui` → « Installer / mettre à jour ».

---

## 5. Sécurité et vie privée

- Toutes les pages `/dysizz-ui` sont réservées au rôle admin ; les formulaires passent par le jeton CSRF de Saltcorn.
- Le HTML / JS d'un bloc et le CSS d'une classe s'exécutent tels quels : seuls les admins peuvent en créer ou en importer.
- Les pages de démo sont en `min_role = 1` (admin).
- **Google Fonts** fait sortir l'IP du visiteur : pour un site européen strict, choisis la police « Système » ou héberge tes polices.

## 6. Limites connues

- Les filtres, onglets et sélections de certains blocs de démonstration sont des états visuels : branche une vraie vue Saltcorn pour les données.
- Le builder de Saltcorn montre les liens sans leur style exact tant qu'ils n'ont pas de classe ; la page publiée, elle, est exacte.
