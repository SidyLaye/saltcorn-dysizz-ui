# Dysizz UI — kit de design pour Saltcorn

Plugin Saltcorn (1.6.x) qui apporte :

- un **design system** chargé sur toutes les pages du tenant : couleurs, polices, arrondis, clair/sombre, 5 styles (moderne, glass, minimal, brutal, luxe) ;
- l'**habillage des vues natives** (List, Edit, Show, Filter, menus, modales, alertes, pagination…) ;
- un **moteur d'animations** sans dépendance, piloté par des classes et des attributs `data-dz-*` ;
- **34 blocs prêts** dans le panneau *Library* du builder, à glisser-déposer ;
- **4 pages de démo** : landing SaaS, vitrine studio sombre, écran d'application, catalogue complet.

Testé de bout en bout sur un vrai Saltcorn 1.6.2 : installation, réglages, blocs dans la Library, pages de démo.

---

## 1. Installation (une seule fois)

### a. Mettre le code sur GitHub

Crée le dépôt `SidyLaye/saltcorn-dysizz-ui` et pousse ce dossier (tel quel, `index.js` à la racine).

### b. Réglages du tenant racine

Dans le tenant racine : **Settings → Site structure → Multitenancy** (`/tenant/settings`). « Install git plugins » est dans la rubrique *Tenant application capabilities*. Ce menu n'apparaît que dans le tenant racine, et seulement si le multi-tenant est activé.

| Réglage | Valeur | Pourquoi |
|---|---|---|
| Install git plugins | ✅ | sans ça, un tenant ne peut pas installer un plugin GitHub |
| New tenant template | `modele` (voir plus bas) | chaque nouveau tenant copie ce modèle |

### c. Installer le plugin

**Settings → Plugins → Add another plugin** :

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

### Construire une page sans coder

1. **Pages → Create page**.
2. Dans le builder, panneau **Library** : glisse les blocs `DZ · …`.
3. Clique sur un texte pour le modifier. Les conteneurs, colonnes et boutons se règlent dans le panneau de droite.
4. Pour une landing : dans les réglages de la page, coche **No menu** et **Fluid layout** (c'est ce que font les pages de démo).

Les blocs en **HTML code** (tarifs, FAQ, logos, barre du bas, navigation…) se modifient en code : double-clic dans le builder, puis change les textes entre les balises.

### Mélanger avec tes données

Les blocs « zone pour ta vue » (*carte pour une vue*, *capture de leads*, *deux colonnes*) ont un emplacement prévu. Tu y glisses une vue List, Edit, Show, Kanban ou Calendrier : le kit la met en forme tout seul.

### Réglages par tenant

`/plugins/configure/dysizz-ui` :

| Réglage | Effet |
|---|---|
| Style général | moderne · glass · minimal · brutal · luxe |
| Couleurs | principale, accent, 2e accent : tous les dégradés, boutons et badges suivent |
| Polices | 13 polices Google + « Système » (aucun appel externe) |
| Arrondi, largeur max | appliqués partout |
| Habiller les éléments Saltcorn | restyle Bootstrap (boutons, formulaires, tableaux…) |
| Animations | coupées aussi automatiquement si le visiteur a demandé moins d'animations |
| Retour en haut, thème mémorisé, CSS en plus | options |

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

En JavaScript (bouton d'action, code de page) : `DZ.toast("Enregistré")`, `DZ.confetti()`, `DZ.setTheme("dark")`, `DZ.init(element)`.

Le moteur relance tout seul l'initialisation quand Saltcorn recharge un morceau de page en ajax.

---

## 4. Mobile

- Tout est responsive. Les grilles passent en une colonne, les modales deviennent des feuilles qui montent du bas.
- Blocs mobiles : barre d'onglets en bas (`dz-bottom-nav dz-mobile-only`), bouton flottant, cartes défilantes.
- Application installable : active la PWA dans Saltcorn (**Settings → Notifications**, `/admin/notifications`, case *pwa_enabled*). Le mobile builder Capacitor marche aussi : le plugin passe ses fichiers en chemins mobiles (`normaliseHeaderForMobile` de Saltcorn).

---

## 5. Mettre à jour le kit

1. Modifie les fichiers, puis **augmente `version` dans `package.json`**. L'URL des CSS/JS contient la version, donc les navigateurs rechargent.
2. Si tu modifies les blocs : `python3 tools/build_packs.py` régénère `packs/`.
3. Réinstalle le plugin dans le tenant, puis `/dysizz-ui` → *Mettre à jour les blocs*. Les blocs `DZ · …` sont remplacés, les tiens ne sont pas touchés.

Point à savoir : le bouton de Saltcorn qui met à jour les plugins de **tous les tenants d'un coup** ne traite que les plugins npm (`upgrade_all_tenants_plugins` filtre `source: "npm"`). Tant que le kit est sur GitHub, la mise à jour se fait tenant par tenant. Quand il sera stable, le publier sur npm règle ça.

---

## 6. Sécurité et vie privée

- `/dysizz-ui` et ses deux actions sont réservées au rôle admin (`role_id === 1`). Les POST passent par le jeton CSRF de Saltcorn.
- Les pages de démo sont installées en `min_role = 1` (admin). Pense à passer en 100 (public) seulement les pages que tu publies.
- Les valeurs de réglage sont filtrées (couleurs en hexadécimal, listes fermées pour les polices et styles, bornes pour les nombres).
- **Google Fonts** : les polices sont chargées depuis les serveurs de Google, et ça fait sortir l'IP du visiteur. Pour un site public européen strict (RGPD), choisis « Système » ou héberge les polices toi-même (téléverse-les et déclare-les dans « CSS en plus » avec `@font-face`).

---

## 7. Limites connues

- Les blocs « HTML code » se modifient en code dans le builder. Ils sont regroupés et commentés pour que ce soit simple.
- Le style `brutal` et le thème Bootswatch *Brite* ont tous les deux des bordures épaisses. Avec le kit, un thème Bootstrap neutre dans *any-bootstrap-theme* rend mieux ; garde Brite seulement si tu choisis le style `brutal`.
- Sur une page en *Fluid layout* avec menu Saltcorn visible, utilise plutôt les blocs « App ». Les blocs de landing sont pensés pour des pages en *No menu*.
