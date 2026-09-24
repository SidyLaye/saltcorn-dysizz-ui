"""Famille « Outil » : blocs utilitaires (réglages de page, bords, espaceurs)."""
FAMILY = "outils"

TR = "rise"  # valeur d'exemple, modifiable dans le builder (classe)

BLOCKS = [
    dict(name="réglages de la page", icon="fas fa-sliders-h", wrap="none", html="""
<div class="dz-page-settings dz-page-tr-rise dz-page-smooth-light">⚙ Réglages de cette page — invisible sur le site. Change les classes de ce conteneur : dz-page-tr-&lt;fade|rise|zoom|blur|tilt|curtain|wipe|cover|stack|depth|fadeout|none&gt;, dz-page-smooth-&lt;off|light|strong&gt;, dz-page-snap-&lt;off|soft|strict&gt;, dz-page-bgmorph-&lt;on|off&gt;. Aperçu : /dysizz-ui/transitions</div>
"""),
]

for key, label in [("wave", "vague"), ("slant", "pente"), ("curve", "courbe"), ("arc", "arche"), ("zigzag", "zigzag"), ("steps", "marches")]:
    BLOCKS.append(dict(name=f"section à bord {label}", icon="fas fa-water", wrap="none", html=f"""
<section class="dz-section dz-bg-surface dz-edge-{key}">
  <div class="dz-container dz-center">
    <span class="dz-eyebrow">Bord « {label} »</span>
    <h2 class="dz-h2">Une section qui se termine en {label}</h2>
    <p class="dz-lead">Mets n'importe quel contenu ici. La forme du bas vient de la classe dz-edge-{key} (ou dz-edge-top-{key} pour le haut).</p>
  </div>
</section>
"""))

BLOCKS += [
    dict(name="section en fondu", icon="fas fa-adjust", wrap="none", html="""
<section class="dz-section dz-bg-surface dz-edge-fade">
  <div class="dz-container dz-center"><h2 class="dz-h2">Une section qui se fond dans la page</h2><p class="dz-lead">Classe dz-edge-fade : les bords haut et bas disparaissent en douceur.</p></div>
</section>
"""),
    dict(name="section qui recouvre la précédente", icon="fas fa-layer-group", wrap="none", html="""
<section class="dz-section dz-bg-surface dz-edge-round-top">
  <div class="dz-container dz-center"><h2 class="dz-h2">Coins arrondis qui montent sur la section d'avant</h2><p class="dz-lead">Classe dz-edge-round-top.</p></div>
</section>
"""),
    dict(name="espace petit", icon="fas fa-arrows-alt-v", wrap="none", html='<div class="dz-ot-space dz-ot-space-s"></div>'),
    dict(name="espace moyen", icon="fas fa-arrows-alt-v", wrap="none", html='<div class="dz-ot-space dz-ot-space-m"></div>'),
    dict(name="espace grand", icon="fas fa-arrows-alt-v", wrap="none", html='<div class="dz-ot-space dz-ot-space-l"></div>'),
    dict(name="barre de lecture", icon="fas fa-ruler-horizontal", wrap="none", html='<div class="dz-scroll-progress"></div>'),
    dict(name="emplacement pour une vue", icon="fas fa-th-list", wrap="section", html="""
<div class="dz-ot-slot"><i class="fas fa-plug"></i><div><b>Glisse ici une vue Saltcorn</b> (liste, fiche, formulaire, calendrier…).<br><span class="dz-small">Puis supprime ce cadre.</span></div></div>
"""),
]
