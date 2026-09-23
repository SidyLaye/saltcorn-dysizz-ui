# Dysizz UI — kit de design pour Saltcorn

Plugin Saltcorn (1.6.x) qui apporte :

- un **design system** chargé sur toutes les pages du tenant, clair et sombre ;
- l'**habillage des vues natives** (List, Edit, Show, Filter, menus, modales, alertes, pagination…) ;
- un **moteur d'animations** sans dépendance, piloté par des classes et des attributs `data-dz-*` ;
- **6 univers visuels** complets (Nocturne, Éditorial, Studio, Aurora, Terre, Luxe) ;
- **73 blocs prêts** dans le panneau *Library* du builder : sites, applications web / bureau, mobile ;
- **7 pages de démo** : landing SaaS, présentation perso, studio, application (menu + Ctrl K), app mobile, 404, catalogue ;
- un **atelier de blocs** (`/dysizz-ui/blocks`) : crée tes blocs en HTML / CSS / JS avec aperçu en direct, exporte / importe-les entre tenants ;
- un **guide de production** (`docs/SCALING.md`) et un compose multi-nœud (`deploy/`).

Testé de bout en bout sur un vrai Saltcorn 1.6.2 : installation, réglages, blocs dans la Library, pages de démo.

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

1. **Installer les blocs** : ils apparaissent dans le builder, panneau *Library*.
2. **Installer les pages de démo** (visibles par les admins seulement).
3. **Ouvrir les réglages** : couleurs, polices, style.

### d. Le tenant modèle (pour tous les futurs tenants)

1. Crée un tenant `modele` (**Settings → Site structure → Tenants**, `/tenant/list`).
2. Dedans : installe le plugin, clique sur les deux boutons de `/dysizz-ui`, règle le thème de base.
3. Ajoute ce qui doit être partout : pages légales, page de connexion, rôles, menu, réglages de sécurité.
4. Dans le tenant racine, **New tenant template** = `modele`.

Chaque nouveau tenant démarre alors avec le plugin, les blocs, les pages et le thème. Saltcorn copie le modèle par une sauvegarde + restauration puis supprime les utilisateurs copiés (vérifié dans `admin-models/models/tenant.js`, `copy_tenant_template`).

Pour un tenant **déjà existant** : installe le plugin, puis `/dysizz-ui` → les deux boutons.

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

### Construire une page sans coder

1. **Pages → Create page**. Pour une landing : coche **No menu** et **Fluid layout** dans les réglages de la page.
2. Dans le builder, panneau **Library** : un bloc par ligne, rangés par famille (App, Hero, Mobile, Nav, Outil, Visuel, Web). Glisse-les dans la page.
3. Clique sur un texte pour le modifier, sur une image pour téléverser la tienne. Les conteneurs, colonnes et boutons se règlent dans le panneau de droite.
4. Les blocs « HTML code » (tarifs, FAQ, carrousels, palette Ctrl K…) se modifient en code : double-clic, puis change les textes entre les balises.

Dans le builder, le kit coupe les animations et affiche les grilles comme sur la page publiée. Ce qui bouge (défilements, compteurs, apparitions) ne se voit que sur la page.

### Mettre ta photo, ta capture d'écran ou ton appli dans un visuel

Les blocs **Visuel · portrait + cartes**, **Hero · portrait (présentation)**, **Hero · app mobile**, **Visuel · téléphone / navigateur / ordinateur portable** contiennent une vraie image Saltcorn :

1. Clique sur l'image dans le builder.
2. Panneau de droite : *Source* → **File** et téléverse ta photo (ou colle une URL).
3. Les cartes flottantes sont des conteneurs avec du texte : clique dessus pour changer le texte. Leur position se règle dans *Custom CSS* (ex. `left:-18px; bottom:64px`).
4. Le badge rond qui tourne est un bloc HTML : change le texte entre `<textPath …>` et `</textPath>`.

### Mélanger avec tes données

Les blocs avec « ⬇ Glisse ici … » (carte + vue, contact + formulaire, liste + détail, coquille d'app, feuille du bas, tiroir, étapes) ont un emplacement prévu : tu y glisses une vue List, Edit, Show, Kanban, Calendrier ou Filter. Le kit la met en forme tout seul.

### Réglages par tenant

| Réglage | Effet |
|---|---|
| Univers, Matière | identité complète + finition |
| Mes propres couleurs | remplace les couleurs de l'univers |
| Polices | « (celle de l'univers) » ou 14 polices Google + « Système » (aucun appel externe) |
| Arrondi, largeur max | 0 = valeur de l'univers |
| Habiller les éléments Saltcorn | boutons, formulaires, tableaux, cartes, menus, modales **et fond de page** des vues natives |
| Animations | **toujours** (défaut) · **suivre le réglage du visiteur** · **désactivées** |
| Curseur personnalisé | rond qui suit la souris et grossit sur les liens (ordinateur seulement) |
| Retour en haut, thème mémorisé, CSS en plus | options |

À propos des animations : si l'ordinateur du visiteur demande de réduire les animations (Windows : *Paramètres → Accessibilité → Effets visuels → Effets d'animation* désactivé), le choix « suivre le réglage du visiteur » fige tout. C'est ce qui donne l'impression que « rien ne défile ». Le défaut est donc « toujours ».

### Performances

Mesuré sur une page de démo, processeur ralenti ×4 et réseau 4G simulé :

| | v2.0 | v2.1+ |
|---|---|---|
| Titre du hero visible | 2,7 s | **0,4 s** (dès le 1er affichage) |
| Temps bloqué (JS/CSS) | 887 ms | **413 ms** |
| Page prête (DOMContentLoaded) | 1,6 s | **0,8 s** |
| Défilement | saccades | 60 i/s |

Ce qui a changé :

- Les apparitions au défilement sont faites **par le navigateur** (CSS `animation-timeline: view()`), sans attendre le JS. Le JS ne sert que de secours pour les vieux navigateurs.
- Plus aucun sélecteur `:has()` (coûteux à chaque changement de la page) : remplacé par des classes posées une fois.
- Animations en boucle limitées à `transform` / `opacity` (calculées par la carte graphique), et mises en pause dès que leur section sort de l'écran.
- Les sections hors écran ne sont pas dessinées tant qu'on n'y arrive pas (`content-visibility`).
- Le JS s'initialise en deux temps : l'essentiel tout de suite, le reste quand le navigateur est libre.
- CSS et JS compressés une seule fois en brotli / gzip au démarrage puis servis depuis la mémoire, avec `ETag` et cache d'un an (l'URL change à chaque version).
- Polices chargées sans bloquer l'affichage.
- Dans l'éditeur de pages, le moteur JS ne tourne pas du tout.

Pour tenir des milliers d'utilisateurs sur plusieurs SaaS (serveurs multiples, Postgres, CDN, sécurité) : voir **[docs/SCALING.md](docs/SCALING.md)**.

### Modifier un bloc, créer les tiens

Un bloc glissé sur une page est une **copie** : tu la modifies librement, l'original de la Library ne bouge pas.

- **Modifier une instance** : clique le bloc dans le builder. Bloc HTML → panneau de droite, zone de code. Conteneur → classes, CSS, couleurs, espacements dans le panneau.
- **Sans code** : assemble des éléments dans le builder, sélectionne le conteneur parent, puis *Library → Add* (en haut du panneau Library). Il devient un bloc réutilisable dans ce tenant.
- **Atelier** (`/dysizz-ui/blocks`) : HTML + CSS + JS avec aperçu en direct (bureau / mobile, clair / sombre).
  - Le CSS est **limité au bloc** automatiquement : `padding:2rem` vise le bloc, `h2{…}` ses titres, `&:hover{…}` le bloc au survol.
  - Le JS reçoit `el` (le bloc) et tourne une fois par bloc présent sur la page.
  - *Partir d'un bloc du kit* copie son code dans l'atelier pour en faire ta version.
  - *Exporter* / *Importer* : un fichier JSON pour passer tes blocs d'un tenant à l'autre (ou les garder dans Git).
- **En code, pour tous les tenants** : un fichier `.html` dans `blocks/` devient un bloc du kit à la prochaine version (voir `blocks/README.md`).

Les noms des blocs du kit sont réservés : un bloc perso ne peut pas les écraser, et « Mettre à jour les blocs » ne touche jamais aux tiens.

---

## 3. Aide-mémoire des classes

### Mise en page

| Classe | Rôle |
|---|---|
| `dz-section` · `dz-section-sm` · `dz-section-alt` · `dz-section-dark` · `dz-section-brand` | bande de page (espacement vertical, fond) |
| `dz-container` · `dz-container-narrow` | largeur max centrée |
| `dz-grid` + `dz-grid-2/3/4` | grille responsive automatique |
| `dz-split` (+ `dz-reverse`) | texte / visuel côte à côte, empilé sur mobile |
| `dz-bento` + `dz-span-2/4/6`, `dz-row-2` | grille bento |
| `dz-stack`, `dz-cluster`, `dz-center` | pile verticale, ligne qui passe à la ligne, centrage |
| `dz-scroller` (+ `dz-grid-desktop`) | cartes qui défilent au doigt sur mobile |

### Composants

`dz-btn` (+ `-lg` `-sm` `-ghost` `-soft` `-dark` `-light` `-gradient` `-glow` `-shine` `-link` `-block`), `dz-badge` (+ `-success` `-warning` `-danger` `-neutral`), `dz-announce`, `dz-card` (+ `-hover` `-glass` `-soft` `-brand` `-flat`), `dz-spotlight`, `dz-border-glow`, `dz-icon` (+ `-gradient` `-lg` `-round`), `dz-stat`, `dz-kpi`, `dz-trend-up/down`, `dz-progress`, `dz-ring`, `dz-pricing`, `dz-price-card` (+ `dz-featured`), `dz-check-list`, `dz-faq`, `dz-steps`, `dz-timeline`, `dz-cta`, `dz-footer`, `dz-nav`, `dz-marquee`, `dz-quote`, `dz-avatar(s)`, `dz-empty`, `dz-list`, `dz-callout` (+ `-success` `-warning` `-danger`), `dz-skeleton`, `dz-tabs`, `dz-compare`, `dz-video`, `dz-countdown`, `dz-masonry`, `dz-prose`, `dz-mock` (maquette d'app en CSS), `dz-browser`, `dz-float-card`, `dz-bottom-nav`, `dz-fab`, `dz-to-top`, `dz-scroll-progress`.

### Nouveaux composants (v2)

Sites : `dz-topbar`, `dz-index`, `dz-marquee-xl`, `dz-words` (+ `dz-words-reveal`), `dz-split-text`, `dz-clip`, `dz-stack-cards`, `data-dz-hscroll` (+ `dz-hscroll-sticky`, `dz-hscroll-track`, `dz-hpanel`), `dz-tabs-v` (+ `data-dz-autoplay="6"`), `dz-ctable`, `dz-orbit`, `data-dz-slider="6"`, `dz-portrait-wrap`, `dz-badge-round`, `dz-phone`, `dz-laptop`, `dz-browser`, `dz-work` + `data-dz-filter`, `dz-post`, `dz-logo-grid`, `dz-wordmark`, `dz-huge`, `data-dz-lightbox`, `data-dz-cookie`.

Applications : `dz-app` (+ `dz-side`, `dz-side-item`, `dz-app-main`, `dz-app-top`, `dz-app-body`, `dz-search`), `data-dz-cmdk` (Ctrl K / ⌘K), `dz-settings` + `dz-setting`, `dz-switch`, `dz-profile`, `dz-stepper`, `dz-chips` + `dz-chip`, `dz-notifs` + `dz-notif`, `dz-chat` + `dz-msg` + `dz-typing`, `dz-checklist` + `dz-check`, `dz-dropzone`, `data-dz-tip`, `dz-window`.

Mobile : `dz-appbar`, `dz-largetitle`, `dz-ios-list` + `dz-cell`, `dz-sheet`, `dz-drawer` (+ `data-dz-open="#id"` / `data-dz-close`), `dz-stories`.

### Titres et textes

`dz-display`, `dz-h1`…`dz-h4`, `dz-lead`, `dz-text`, `dz-small`, `dz-eyebrow`, `dz-gradient-text`, `dz-underline`, `dz-highlight`, `dz-stroke-text`.

### Fonds et effets

`dz-hero` (+ `dz-hero-full`), `dz-aurora` (conteneur vide en premier dans la section), `dz-bg-mesh`, `dz-bg-grid`, `dz-bg-dots`, `dz-noise`, `dz-glow-under`, `dz-glass`, `dz-float`, `dz-float-slow`, `dz-pulse`, `dz-spin-slow`, `dz-hover-lift`, `dz-hover-zoom`.

### Animations et interactions (sans code)

| À poser sur l'élément | Effet |
|---|---|
| classe `dz-reveal` ou `data-dz-reveal="fade / zoom / blur / left / right / flip"` | apparition au défilement (`data-dz-delay="200"` en ms) |
| classe `dz-stagger` sur le parent | les enfants apparaissent l'un après l'autre |
| `data-dz-count="2400"` (+ `data-dz-suffix`, `data-dz-prefix`, `data-dz-decimals`) | compteur animé |
| `data-dz-typed="mot 1\|mot 2\|mot 3"` | texte qui s'écrit |
| `data-dz-tilt="8"` | inclinaison 3D à la souris |
| classe `dz-magnetic` | bouton attiré par la souris |
| `data-dz-parallax="0.2"` | parallaxe |
| `data-dz-theme-toggle` | bouton clair / sombre |
| `data-dz-price-toggle` + `data-monthly` / `data-yearly` | bascule de prix |
| `data-dz-menu-toggle="#id"` | ouvre / ferme un menu mobile |
| `data-dz-countdown="2026-12-31T23:59:59"` | compte à rebours |
| `data-dz-copy="texte"` ou `"#id"` | copie dans le presse-papier |
| `data-dz-confetti` | confettis au clic |
| `.dz-progress[data-dz-value="72"]` | barre qui se remplit à l'affichage |
| classe `dz-words-reveal` | texte qui s'éclaire mot par mot au défilement |
| classe `dz-split-text` | titre dont les lettres montent une à une |
| classe `dz-clip` | image qui se dévoile |
| `data-dz-hscroll` | section qui défile à l'horizontale |
| `data-dz-slider="6"` | carrousel (6 = défilement auto toutes les 6 s, 0 = manuel) |
| `data-dz-filter="#grille"` + `data-filter` / `data-tags` | filtres de portfolio |
| `data-dz-open="#id"` / `data-dz-close` | ouvre / ferme une feuille ou un tiroir |
| `data-dz-cmdk` | palette de commandes (Ctrl K) |
| `data-dz-lightbox` | image ou vidéo YouTube en plein écran |
| `data-dz-dismiss` | bouton qui ferme un bandeau (mémorisé) |

En JavaScript (bouton d'action, code de page) : `DZ.toast("Enregistré")`, `DZ.confetti()`, `DZ.setTheme("dark")`, `DZ.init(element)`.

Le moteur relance tout seul l'initialisation quand Saltcorn recharge un morceau de page en ajax.

---

## 4. Mobile

- Tout est responsive. Les grilles passent en une colonne, les modales deviennent des feuilles qui montent du bas.
- Blocs mobiles : barre d'onglets en bas (`dz-bottom-nav dz-mobile-only`), bouton flottant, cartes défilantes.
- Application installable : active la PWA dans Saltcorn (**Settings → Notifications**, `/admin/notifications`, case *pwa_enabled*). Le mobile builder Capacitor marche aussi : le plugin passe ses fichiers en chemins mobiles (`normaliseHeaderForMobile` de Saltcorn).

---

## 5. Structure et mise à jour

```
index.js            ← généré : le plugin complet en UN fichier (CSS, JS, blocs, pages embarqués)
package.json
src/plugin.js       ← le code du plugin (à modifier)
blocks/             ← tes blocs en code (.html), ajoutés au kit
docs/SCALING.md     ← production : multi-serveurs, Postgres, CDN, sécurité
deploy/             ← docker-compose multi-nœud pour Dokploy / Traefik
assets/             ← dz-core.css, dz-skin.css, dz.js, blocks.json, demo-pages.json
tools/build_packs.py   ← régénère assets/blocks.json et assets/demo-pages.json
tools/build_index.py   ← reconstruit index.js à partir de src/ et assets/
```

Pourquoi un seul fichier : l'installeur de Saltcorn peut laisser un dossier de module incomplet (dossier déjà présent et jamais retéléchargé, ou deux workers qui installent en même temps). Avec tout dans `index.js`, le plugin n'a besoin d'aucun autre fichier sur le serveur. Le CSS et le JS sont servis par le plugin lui-même sur `/dysizz-ui/a/<version>/<fichier>`, avec un cache long qui saute à chaque nouvelle version.

Pour publier une modification :

1. Modifie `src/plugin.js` ou les fichiers de `assets/`.
2. Augmente `version` dans `package.json`.
3. `python3 tools/build_packs.py` (si tu as touché aux blocs), puis `python3 tools/build_index.py`.
4. Pousse sur GitHub, réinstalle le module dans Saltcorn, puis `/dysizz-ui` → *Mettre à jour les blocs*. Les blocs `DZ · …` sont remplacés, les tiens ne sont pas touchés.

Le bouton de Saltcorn qui met à jour les plugins de **tous les tenants d'un coup** ne traite que les plugins npm (`upgrade_all_tenants_plugins` filtre `source: "npm"`). Tant que le kit est sur GitHub, la mise à jour se fait tenant par tenant.

---

## 6. Sécurité et vie privée

- `/dysizz-ui`, l'atelier et toutes leurs actions sont réservés au rôle admin (`role_id === 1`). Les POST passent par le jeton CSRF de Saltcorn.
- Le HTML / JS d'un bloc s'exécute tel quel sur les pages : seuls les admins peuvent en créer ou en importer. N'importe que des fichiers de blocs dont tu connais la source.
- Les pages de démo sont installées en `min_role = 1` (admin). Pense à passer en 100 (public) seulement les pages que tu publies.
- Les valeurs de réglage sont filtrées (couleurs en hexadécimal, listes fermées pour les polices et styles, bornes pour les nombres).
- **Google Fonts** : les polices sont chargées depuis les serveurs de Google, et ça fait sortir l'IP du visiteur. Pour un site public européen strict (RGPD), choisis « Système » ou héberge les polices toi-même (téléverse-les et déclare-les dans « CSS en plus » avec `@font-face`).

---

## 7. Limites connues

- Les blocs « HTML code » se modifient en code dans le builder. Ils sont regroupés et commentés pour que ce soit simple.
- Le style `brutal` et le thème Bootswatch *Brite* ont tous les deux des bordures épaisses. Avec le kit, un thème Bootstrap neutre dans *any-bootstrap-theme* rend mieux ; garde Brite seulement si tu choisis le style `brutal`.
- Sur une page en *Fluid layout* avec menu Saltcorn visible, utilise plutôt les blocs « App ». Les blocs de landing sont pensés pour des pages en *No menu*.
