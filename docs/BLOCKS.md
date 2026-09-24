# Écrire des blocs pour le kit

Ce guide sert à toute personne (ou agent) qui ajoute des blocs au kit.
Un bloc s'écrit en **HTML + classes du kit** ; à la construction, il est
converti automatiquement en **éléments natifs du builder Saltcorn**
(conteneurs, textes, liens, images). Résultat : dans le builder, on clique
sur un texte pour l'écrire, sur un conteneur pour changer ses classes,
couleurs, marges, animation — sans toucher au code.

## 1. Où écrire

| Quoi | Fichier |
|---|---|
| Les blocs d'une famille | `tools/packs/<famille>.py` |
| Le CSS de ces blocs | `styles/NN-<famille>.css` (NN = numéro attribué, voir §8) |
| Les familles (nom, icône, description) | `tools/families.py` (ne pas modifier sans raison) |

Un module de famille :

```python
FAMILY = "projet"          # clé de tools/families.py
BLOCKS = [
    dict(
        name="tableau kanban",            # préfixe « Projet · » ajouté tout seul
        icon="fas fa-columns",            # Font Awesome 5 (fas / far / fab)
        wrap="section",                   # section | narrow | full | app | none
        html="""
<div class="dz-pj-board">…</div>
""",
    ),
]
```

`wrap` :
- `section` : `<section class="dz-section"><div class="dz-container">…</div></section>` (le plus courant)
- `narrow` : pareil avec un conteneur étroit (texte long, formulaire)
- `full` : section pleine largeur sans conteneur (fonds, héros, bandeaux)
- `app` : pour les écrans d'application (padding doux, pas de grande marge de section)
- `none` : ton HTML tel quel

## 2. Construire et contrôler

```bash
cd tools && npm install          # une fois
node build.mjs                   # construit tout (packs, CSS, JS, index.js)
node preview.mjs <famille>       # captures + contrôles
```

`preview.mjs` rend chaque bloc avec le vrai moteur de Saltcorn et écrit :
- `build/preview/<famille>-dark.png`, `-light.png`, `-mobile.png` : planches à regarder ;
- un ✓ / ⚠ par bloc : débordement sur mobile, erreurs JS, écart entre ton
  HTML et sa version convertie en éléments natifs (doit être ~0 %).

**Un bloc n'est fini que si** : il est beau en sombre ET en clair, ne
déborde pas à 390 px, n'a pas d'erreur, et son écart natif est < 0,5 %.

## 3. Le HTML : ce qui devient natif

Le convertisseur (`tools/html2layout.py`) transforme :

| Tu écris | Devient dans le builder |
|---|---|
| `<div class="…">…</div>` (et section, header, ul, li, p, article, nav…) | Conteneur (même balise, mêmes classes) |
| `<h2 class="dz-h2">Titre</h2>` | Texte, style titre h2 |
| `<span class="dz-badge">Nouveau</span>` | Texte (span + classes) |
| `<p class="dz-lead">Du <b>texte</b></p>` | Conteneur p + Texte (le gras est gardé) |
| `<a class="dz-btn" href="#"><i class="fas fa-plus"></i> Créer</a>` | Lien (bouton), icône reconnue |
| `<a class="dz-card" href="#">…contenu riche…</a>` | Conteneur cliquable |
| `<img src="…" alt="…">` sans classe (ou w-100, img-fluid, dz-cover) | Image |
| `<i class="fas fa-bolt"></i>` seul | Conteneur i (icône modifiable par sa classe) |

Reste **en code** (bloc HTML) : `svg`, `video`, `iframe`, `form`, `input`,
`select`, `textarea`, `table`, `canvas`, et tout élément qui porte un
attribut sans équivalent (autre que `class`, `id`, `style`, `href`, `src`,
`alt`, `title`, `target`, `aria-label`, `data-dz-*` listés ci-dessous).
C'est permis quand c'est utile (un graphique SVG, un tableau, un champ),
mais **garde ces morceaux petits** : le reste du bloc reste modifiable.

`aria-label` est gardé sous forme de texte caché (`visually-hidden`).

À éviter : attributs `onclick`, `data-*` maison, `<script>`, `<style>` dans
le HTML (le CSS va dans `styles/`), texte nu mélangé à des blocs dans un
même parent (mets le texte dans un `<span>` ou un `<p>`).

## 4. Les comportements : des classes, pas d'attributs

Le builder ne pose que des classes. Chaque effet du kit existe en classe
(voir `client/dz.js`, « classes sans code ») :

| Classe | Effet |
|---|---|
| `dz-reveal` · `dz-reveal-fade/zoom/blur/left/right/flip` | apparition au défilement |
| `dz-stagger` (sur le parent) | les enfants apparaissent l'un après l'autre |
| `dz-counter` | anime le nombre écrit dans le texte : `<span class="dz-counter">48 250 €</span>` |
| `dz-typewriter` | machine à écrire : `mot 1 \| mot 2 \| mot 3` |
| `dz-countdown` | le texte est la date : `2026-12-31 18:00` |
| `dz-progress dz-progress-72` | barre de progression (avec un `<span>` dedans) |
| `dz-parallax` · `-slow` · `-fast` · `-reverse` | parallaxe |
| `dz-tilt`, `dz-magnetic`, `dz-spotlight` | effets au survol |
| `dz-open-<id>` / `dz-close` | ouvre / ferme le panneau `#<id>` (tiroir, feuille, modale) |
| `dz-theme-toggle`, `dz-dismiss`, `dz-copy`, `dz-confetti` | bascule clair/sombre, fermer, copier, confettis |
| `dz-tabs` > `dz-tabs-nav` (boutons) + `dz-tab-panel` (autant que de boutons) | onglets : le n-ième bouton ouvre le n-ième panneau, `dz-active` sur l'onglet ouvert |
| `dz-chips` + `dz-chip` | puces sélectionnables |
| `dz-slider` | carrousel |
| `dz-zoomable` | image agrandie au clic |
| `dz-words`, `dz-letters` | texte révélé mot à mot / lettre à lettre |

Les données chiffrées sont écrites **en clair** dans le HTML (« 48 250 € »),
jamais « 0 » + un attribut : le bloc reste lisible et modifiable sans JS.

## 5. Le CSS

- **Uniquement les jetons** du kit pour couleurs, rayons, ombres, polices,
  durées : `var(--dz-bg)`, `--dz-surface`, `--dz-surface-2`, `--dz-text`,
  `--dz-text-soft`, `--dz-text-mute`, `--dz-border`, `--dz-border-strong`,
  `--dz-primary`, `--dz-primary-soft`, `--dz-primary-ink` (texte couleur
  primaire sur fond clair), `--dz-on-primary` (texte SUR la couleur
  primaire), `--dz-accent`, `--dz-accent-2`, `--dz-success`, `--dz-warning`,
  `--dz-danger`, `--dz-info`, `--dz-radius`, `--dz-radius-sm`,
  `--dz-radius-lg`, `--dz-radius-pill`, `--dz-shadow-xs/sm/(rien)/lg/glow`,
  `--dz-font-heading`, `--dz-font-body`, `--dz-font-mono`, `--dz-ease`,
  `--dz-dur`, `--dz-dur-fast`, `--dz-gradient`. Jamais de couleur en dur
  (sauf rouge/orange/vert des feux de fenêtre et effets très particuliers).
  Ainsi le bloc suit les 6 univers, le clair et le sombre, et les couleurs
  perso du tenant.
- **Préfixe de famille** pour toute nouvelle classe (voir §8), et réutilise
  d'abord l'existant : `dz-card`, `dz-btn*`, `dz-badge*`, `dz-avatar`,
  `dz-chip`, `dz-icon`, `dz-grid*`, `dz-cluster`, `dz-stack`, `dz-split`,
  `dz-h1…h4`, `dz-lead`, `dz-small`, `dz-mono`, `dz-eyebrow`, `dz-kbd`,
  `dz-progress`, `dz-trend-up/down`, `dz-dot`, `dz-divider`, `dz-window`…
  (tout est dans `styles/`).
- **Mobile d'abord** : pas de largeur fixe > 360 px sans `min()`, grilles en
  `repeat(auto-fit, minmax(min(100%, 260px), 1fr))`, défilement horizontal
  (`overflow-x:auto`) pour les grands tableaux / kanbans.
- **Performance** : n'anime que `transform` et `opacity` ; pas de `:has()` ;
  pas de `backdrop-filter` sur de grandes surfaces ; boucles infinies
  seulement si utiles, et elles s'arrêtent hors écran si le bloc est dans une
  `.dz-section` (classe `.dz-offscreen` posée par le kit :
  `.dz-offscreen .ma-boucle { animation-play-state: paused; }`).
- `prefers-reduced-motion` est géré globalement par le kit.
- Le builder : les grilles / flex d'une classe sont reportées toutes seules
  dans l'éditeur. Rien à faire, sauf éviter les sélecteurs trop profonds
  (`.a > .b > .c > span`) : préfère une classe sur l'élément visé.

## 6. Le contenu

- En français, réaliste et crédible (noms, montants, dates en 2026, statuts).
- **Aucun nom, logo ou marque réels** (pas de Slack, Gmail, Stripe…) : des
  noms inventés (« Nexora », « Atelier Lune »…).
- Images : `https://picsum.photos/seed/<mot>/<l>/<h>` ou des dégradés CSS.
  Avatars : initiales dans `dz-avatar`.
- Accessibilité : un titre par bloc, contrastes suffisants, `aria-label` sur
  les boutons icône, `alt` sur les images.

## 7. Le niveau attendu

Chaque bloc doit pouvoir figurer dans un produit professionnel : hiérarchie
visuelle nette, espacements réguliers, alignements parfaits, états
(survol, actif, sélectionné, vide) soignés, détails (compteurs, badges,
raccourcis clavier, horodatages). S'inspirer des meilleurs logiciels du
marché **sans copier** leur interface : on reprend des usages, pas un design.

## 8. Numéros de fichiers CSS et préfixes

| Famille | Fichier | Préfixe |
|---|---|---|
| projet | `styles/30-projet.css` | `dz-pj-` |
| support | `styles/31-support.css` | `dz-sp-` |
| mail | `styles/32-mail.css` | `dz-ml-` |
| commerce | `styles/33-commerce.css` | `dz-cm-` |
| finance | `styles/34-finance.css` | `dz-fi-` |
| donnees | `styles/35-donnees.css` | `dz-dt-` |
| agenda | `styles/36-agenda.css` | `dz-ag-` |
| social | `styles/37-social.css` | `dz-so-` |
| contenu | `styles/38-contenu.css` | `dz-ct-` |
| media | `styles/39-media.css` | `dz-md-` |
| compte | `styles/40-compte.css` | `dz-ac-` |
| equipe | `styles/41-equipe.css` | `dz-eq-` |
| insolite | `styles/42-insolite.css` | `dz-in-` |
| site (ajouts) | `styles/43-site-plus.css` | `dz-st-` |
| app (ajouts) | `styles/44-app-plus.css` | `dz-ap-` |
| mobile (ajouts) | `styles/45-mobile-plus.css` | `dz-mb-` |
| outils (ajouts) | `styles/46-outils.css` | `dz-ot-` |
