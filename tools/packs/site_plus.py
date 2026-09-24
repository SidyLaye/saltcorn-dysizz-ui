"""Site (ajouts) : sections de sites vitrines haut de gamme. CSS : styles/43-site-plus.css (préfixe dz-st-)."""
FAMILY = "site"

BLOCKS = [
    # ------------------------------------------------------------------ 1
    dict(
        name="héros immersif (visuel plein écran)",
        icon="fas fa-image",
        wrap="none",
        html="""
<section class="dz-st-immersive">
  <div class="dz-st-immersive-media dz-parallax-slow"><img class="dz-cover" src="https://picsum.photos/seed/falaises-aube/1920/1280" alt="Falaises au lever du jour, vues depuis la mer"></div>
  <div class="dz-st-immersive-shade"></div>
  <div class="dz-container dz-st-immersive-inner">
    <div class="dz-st-immersive-top">
      <span class="dz-st-immersive-tag"><span class="dz-dot"></span> Saison 2026 · Expéditions ouvertes</span>
      <span class="dz-st-immersive-index">N° 07 — Côte d'Opale</span>
    </div>
    <h1 class="dz-st-immersive-title">Partir loin, <em>revenir changé.</em></h1>
    <div class="dz-st-immersive-bottom">
      <div class="dz-st-immersive-copy">
        <p class="dz-st-immersive-lead">Des voyages lents, en petits groupes, conçus avec les gens qui vivent là-bas. Douze destinations, zéro compromis sur l'essentiel.</p>
        <div class="dz-cluster">
          <a class="dz-btn dz-btn-light dz-btn-lg" href="#">Voir les départs <i class="fas fa-arrow-right"></i></a>
          <a class="dz-st-play" href="#"><span class="dz-st-play-icon"><i class="fas fa-play"></i></span><span class="dz-st-play-label">Le film · 1 min 40</span></a>
        </div>
      </div>
      <div class="dz-st-immersive-facts">
        <div class="dz-st-fact"><b class="dz-counter">12</b><span>destinations</span></div>
        <div class="dz-st-fact"><b class="dz-counter">8</b><span>voyageurs max.</span></div>
        <div class="dz-st-fact"><b>4,9/5</b><span>2 140 avis</span></div>
      </div>
    </div>
    <div class="dz-st-scroll-hint"><span class="dz-st-scroll-line"></span><span>Défiler</span></div>
  </div>
</section>
""",
    ),
    # ------------------------------------------------------------------ 2
    dict(
        name="héros capture (formulaire)",
        icon="fas fa-envelope-open",
        wrap="none",
        html="""
<section class="dz-section dz-st-capture-hero">
  <div class="dz-st-capture-glow"></div>
  <div class="dz-container dz-st-capture-grid">
    <div class="dz-st-capture-copy dz-reveal">
      <a class="dz-announce" href="#"><b>Nouveau</b> Relances automatiques par SMS <i class="fas fa-arrow-right"></i></a>
      <h1 class="dz-h1">Vos factures <em>se paient</em> pendant que vous travaillez.</h1>
      <p class="dz-lead">Devis, factures, relances et rapprochement bancaire au même endroit. Les indépendants encaissent en moyenne 11 jours plus tôt.</p>
      <div class="dz-st-capture">
        <div class="dz-st-capture-field"><i class="far fa-envelope"></i><input type="email" placeholder="vous@entreprise.fr" aria-label="Adresse e-mail professionnelle"></div>
        <a class="dz-btn dz-btn-lg" href="#">Essayer gratuitement</a>
      </div>
      <div class="dz-st-capture-notes">
        <span><i class="fas fa-check"></i> 14 jours offerts</span>
        <span><i class="fas fa-check"></i> Sans carte bancaire</span>
        <span><i class="fas fa-check"></i> Conforme e-facture 2026</span>
      </div>
      <div class="dz-st-proof">
        <div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">LM</span><span class="dz-avatar dz-avatar-sm">SB</span><span class="dz-avatar dz-avatar-sm">AK</span><span class="dz-avatar dz-avatar-sm">JR</span></div>
        <div class="dz-st-proof-text"><span class="dz-stars">★★★★★</span><span class="dz-small"><b>4,9/5</b> · 2 300 avis vérifiés</span></div>
      </div>
    </div>
    <div class="dz-st-capture-visual dz-reveal-right">
      <div class="dz-st-invoice">
        <div class="dz-st-invoice-head">
          <div class="dz-st-invoice-brand"><span class="dz-st-invoice-logo"></span><div class="dz-st-invoice-id"><b>Facture F-2026-0412</b><span>Atelier Lune · émise le 3 sept.</span></div></div>
          <span class="dz-badge dz-badge-success"><i class="fas fa-check"></i> Payée</span>
        </div>
        <div class="dz-st-invoice-lines">
          <div class="dz-st-invoice-line"><span>Identité visuelle — forfait</span><b>2 400,00 €</b></div>
          <div class="dz-st-invoice-line"><span>Déclinaisons réseaux (x12)</span><b>960,00 €</b></div>
          <div class="dz-st-invoice-line"><span>Direction artistique · 1,5 j</span><b>900,00 €</b></div>
        </div>
        <div class="dz-st-invoice-total"><span>Total TTC</span><b>5 112,00 €</b></div>
        <div class="dz-st-invoice-track"><span class="dz-st-invoice-step dz-st-on">Envoyée</span><span class="dz-st-invoice-step dz-st-on">Ouverte</span><span class="dz-st-invoice-step dz-st-on">Relancée</span><span class="dz-st-invoice-step dz-st-on">Payée</span></div>
      </div>
      <div class="dz-st-toast dz-st-toast-a"><span class="dz-st-toast-icon"><i class="fas fa-euro-sign"></i></span><div class="dz-st-toast-text"><b>+ 5 112,00 €</b><span>Virement reçu · il y a 2 min</span></div></div>
      <div class="dz-st-toast dz-st-toast-b"><span class="dz-st-toast-icon dz-st-toast-icon-alt"><i class="fas fa-paper-plane"></i></span><div class="dz-st-toast-text"><b>Relance envoyée</b><span>Studio Brume · J+7</span></div></div>
    </div>
  </div>
</section>
""",
    ),
    # ------------------------------------------------------------------ 3
    dict(
        name="fonctionnalités en défilement collant",
        icon="fas fa-thumbtack",
        html="""
<div class="dz-st-sticky">
  <div class="dz-section-head dz-reveal">
    <span class="dz-eyebrow">Comment l'équipe travaille</span>
    <h2 class="dz-h2">Un seul espace, <em>du brief à la livraison</em></h2>
    <p class="dz-lead">Faites défiler : chaque étape du projet a son écran, et tout reste relié.</p>
  </div>
  <div class="dz-st-sticky-grid">
    <div class="dz-st-sticky-text dz-st-r1">
      <span class="dz-st-sticky-num">01 — Planifier</span>
      <h3 class="dz-h3">Le planning se construit tout seul</h3>
      <p class="dz-text">Glissez vos tâches, les dépendances et la charge de chacun se recalculent. Les retards sont signalés avant de devenir des problèmes.</p>
      <ul class="dz-check-list"><li>Vue tableau, liste et chronologie</li><li>Charge d'équipe en temps réel</li><li>Jalons partagés avec le client</li></ul>
    </div>
    <div class="dz-st-sticky-visual dz-st-r1">
      <div class="dz-st-screen">
        <div class="dz-st-screen-bar"><span class="dz-st-screen-dots"></span><span class="dz-st-screen-title">Refonte boutique · Planning</span></div>
        <div class="dz-st-board">
          <div class="dz-st-board-col"><span class="dz-st-board-h">À faire <b>4</b></span><span class="dz-st-board-card"><i class="dz-st-tag dz-st-tag-a"></i>Arborescence</span><span class="dz-st-board-card"><i class="dz-st-tag dz-st-tag-b"></i>Photos produits</span><span class="dz-st-board-card"><i class="dz-st-tag dz-st-tag-c"></i>Textes légaux</span></div>
          <div class="dz-st-board-col"><span class="dz-st-board-h">En cours <b>2</b></span><span class="dz-st-board-card dz-st-lift"><i class="dz-st-tag dz-st-tag-a"></i>Maquettes mobile<span class="dz-st-board-meta"><span class="dz-avatar dz-avatar-sm">IL</span>12 sept.</span></span><span class="dz-st-board-card"><i class="dz-st-tag dz-st-tag-b"></i>Paiement en 3×</span></div>
          <div class="dz-st-board-col"><span class="dz-st-board-h">Terminé <b>9</b></span><span class="dz-st-board-card dz-st-done"><i class="dz-st-tag dz-st-tag-c"></i>Atelier cadrage</span><span class="dz-st-board-card dz-st-done"><i class="dz-st-tag dz-st-tag-a"></i>Benchmark</span></div>
        </div>
      </div>
    </div>
    <div class="dz-st-sticky-text dz-st-r2">
      <span class="dz-st-sticky-num">02 — Automatiser</span>
      <h3 class="dz-h3">Les tâches répétitives disparaissent</h3>
      <p class="dz-text">Quand un devis est signé, le projet se crée, l'équipe est prévenue et l'acompte est facturé. Sans une ligne de code.</p>
      <ul class="dz-check-list"><li>120 déclencheurs prêts à l'emploi</li><li>Conditions et délais</li><li>Historique de chaque exécution</li></ul>
    </div>
    <div class="dz-st-sticky-visual dz-st-r2">
      <div class="dz-st-screen">
        <div class="dz-st-screen-bar"><span class="dz-st-screen-dots"></span><span class="dz-st-screen-title">Automatisation · Devis signé</span></div>
        <div class="dz-st-flow">
          <div class="dz-st-node dz-st-node-trigger"><i class="fas fa-file-signature"></i><div class="dz-st-node-text"><b>Quand un devis est signé</b><span>Déclencheur</span></div></div>
          <span class="dz-st-link"></span>
          <div class="dz-st-node"><i class="fas fa-folder-plus"></i><div class="dz-st-node-text"><b>Créer le projet</b><span>Modèle « Site vitrine »</span></div></div>
          <span class="dz-st-link"></span>
          <div class="dz-st-flow-split">
            <div class="dz-st-node"><i class="fas fa-bell"></i><div class="dz-st-node-text"><b>Prévenir l'équipe</b><span>#projets</span></div></div>
            <div class="dz-st-node"><i class="fas fa-receipt"></i><div class="dz-st-node-text"><b>Facturer 30 %</b><span>Acompte</span></div></div>
          </div>
          <span class="dz-st-flow-run"><span class="dz-dot"></span> 1 284 exécutions ce mois-ci</span>
        </div>
      </div>
    </div>
    <div class="dz-st-sticky-text dz-st-r3">
      <span class="dz-st-sticky-num">03 — Mesurer</span>
      <h3 class="dz-h3">La rentabilité, projet par projet</h3>
      <p class="dz-text">Temps passé, marge et encaissements se croisent automatiquement. Vous savez enfin quels clients vous font gagner de l'argent.</p>
      <ul class="dz-check-list"><li>Marge prévisionnelle et réelle</li><li>Rapports exportables</li><li>Alertes de dépassement</li></ul>
    </div>
    <div class="dz-st-sticky-visual dz-st-r3">
      <div class="dz-st-screen">
        <div class="dz-st-screen-bar"><span class="dz-st-screen-dots"></span><span class="dz-st-screen-title">Rentabilité · T3 2026</span></div>
        <div class="dz-st-analytics">
          <div class="dz-st-analytics-kpis">
            <div class="dz-st-mini-kpi"><span>Marge moyenne</span><b>38,4 %</b><span class="dz-trend dz-trend-up">+4,2 pts</span></div>
            <div class="dz-st-mini-kpi"><span>Encaissé</span><b>184 900 €</b><span class="dz-trend dz-trend-up">+12 %</span></div>
          </div>
          <div class="dz-st-bars"><span style="--h:42%"></span><span style="--h:55%"></span><span style="--h:48%"></span><span style="--h:66%"></span><span style="--h:60%"></span><span style="--h:78%"></span><span style="--h:72%"></span><span style="--h:90%"></span></div>
        </div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 4
    dict(
        name="bento produit",
        icon="fas fa-th-large",
        html="""
<div class="dz-section-head dz-reveal">
  <span class="dz-eyebrow">Plateforme</span>
  <h2 class="dz-h2">Tout ce qu'il faut, <em>rien de superflu</em></h2>
  <p class="dz-lead">Six briques pensées pour fonctionner ensemble dès le premier jour.</p>
</div>
<div class="dz-st-bento dz-stagger">
  <div class="dz-st-cell dz-st-cell-wide dz-st-cell-tall">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-chart-line"></i> Pilotage</span><h3 class="dz-h4">Vos chiffres, en direct</h3><p>Chiffre d'affaires, conversion, panier moyen : actualisés toutes les 30 secondes.</p></div>
    <div class="dz-st-dash">
      <div class="dz-st-dash-head"><div class="dz-st-dash-value"><span>Revenu du mois</span><b>84 230 €</b></div><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 18,2 %</span></div>
      <div class="dz-st-area"><span style="--h:30%"></span><span style="--h:38%"></span><span style="--h:34%"></span><span style="--h:46%"></span><span style="--h:44%"></span><span style="--h:58%"></span><span style="--h:52%"></span><span style="--h:64%"></span><span style="--h:61%"></span><span style="--h:74%"></span><span style="--h:70%"></span><span style="--h:86%"></span></div>
      <div class="dz-st-dash-legend"><span>1 sept.</span><span>15 sept.</span><span>30 sept.</span></div>
    </div>
  </div>
  <div class="dz-st-cell">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-magic"></i> Assistant</span><h3 class="dz-h4">Posez la question</h3></div>
    <div class="dz-st-chat">
      <span class="dz-st-bubble dz-st-bubble-me">Quel produit a le plus progressé ?</span>
      <span class="dz-st-bubble">La <b>bougie Figuier</b> : +42 % en septembre, portée par la newsletter du 12.</span>
    </div>
  </div>
  <div class="dz-st-cell">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-bolt"></i> Automatisations</span><h3 class="dz-h4">En pilote automatique</h3></div>
    <div class="dz-st-toggles">
      <div class="dz-st-toggle-row"><span>Relance panier abandonné</span><span class="dz-st-switch dz-st-on"></span></div>
      <div class="dz-st-toggle-row"><span>Avis client à J+10</span><span class="dz-st-switch dz-st-on"></span></div>
      <div class="dz-st-toggle-row"><span>Alerte stock bas</span><span class="dz-st-switch"></span></div>
    </div>
  </div>
  <div class="dz-st-cell dz-st-cell-third">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-server"></i> Fiabilité</span><h3 class="dz-h4"><span class="dz-st-big">99,98 %</span> de disponibilité</h3></div>
    <div class="dz-st-uptime"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span class="dz-st-warn"></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
  </div>
  <div class="dz-st-cell dz-st-cell-third">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-users"></i> Collaboration</span><h3 class="dz-h4">À plusieurs, en même temps</h3></div>
    <div class="dz-st-cursors">
      <span class="dz-st-cursor dz-st-cursor-a"><i class="fas fa-mouse-pointer"></i><b>Inès</b></span>
      <span class="dz-st-cursor dz-st-cursor-b"><i class="fas fa-mouse-pointer"></i><b>Malik</b></span>
      <span class="dz-st-doc-line" style="--w:90%"></span><span class="dz-st-doc-line dz-st-sel" style="--w:70%"></span><span class="dz-st-doc-line" style="--w:82%"></span>
    </div>
  </div>
  <div class="dz-st-cell dz-st-cell-third">
    <div class="dz-st-cell-copy"><span class="dz-st-cell-kicker"><i class="fas fa-plug"></i> Connecteurs</span><h3 class="dz-h4">80+ intégrations</h3></div>
    <div class="dz-st-apps"><span><i class="fas fa-envelope"></i></span><span><i class="fas fa-credit-card"></i></span><span><i class="fas fa-truck"></i></span><span><i class="fas fa-calendar"></i></span><span><i class="fas fa-comments"></i></span><span><i class="fas fa-file-invoice"></i></span><span><i class="fas fa-cloud"></i></span><span class="dz-st-apps-more">+74</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 5
    dict(
        name="tarifs en tableau détaillé",
        icon="fas fa-table",
        html="""
<div class="dz-section-head dz-reveal">
  <span class="dz-eyebrow">Tarifs</span>
  <h2 class="dz-h2">Comparez les formules <em>ligne à ligne</em></h2>
  <p class="dz-lead">Prix HT par utilisateur. Changez de formule quand vous voulez, au prorata.</p>
  <div class="dz-st-billing"><span class="dz-st-billing-opt">Mensuel</span><span class="dz-st-billing-opt dz-st-on">Annuel <b>−20 %</b></span></div>
</div>
<div class="dz-st-pt-wrap">
  <div class="dz-st-pt">
    <div class="dz-st-pt-corner"><span class="dz-small">Toutes les formules incluent l'hébergement en France et le support par e-mail.</span></div>
    <div class="dz-st-pt-plan"><span class="dz-st-pt-name">Essentiel</span><div class="dz-st-pt-price"><b>9 €</b><span>/mois</span></div><span class="dz-st-pt-desc">Pour démarrer seul</span><a class="dz-btn dz-btn-ghost dz-btn-sm dz-btn-block" href="#">Choisir</a></div>
    <div class="dz-st-pt-plan dz-st-pt-hl dz-st-pt-top"><span class="dz-st-pt-name">Équipe <span class="dz-badge">Populaire</span></span><div class="dz-st-pt-price"><b>24 €</b><span>/mois</span></div><span class="dz-st-pt-desc">Pour les équipes jusqu'à 50</span><a class="dz-btn dz-btn-sm dz-btn-block" href="#">Essayer 14 jours</a></div>
    <div class="dz-st-pt-plan"><span class="dz-st-pt-name">Entreprise</span><div class="dz-st-pt-price"><b>Sur devis</b></div><span class="dz-st-pt-desc">Sécurité et volume</span><a class="dz-btn dz-btn-ghost dz-btn-sm dz-btn-block" href="#">Nous contacter</a></div>

    <div class="dz-st-pt-group">Utilisation</div>
    <div class="dz-st-pt-label">Projets actifs</div><div class="dz-st-pt-cell">3</div><div class="dz-st-pt-cell dz-st-pt-hl">Illimités</div><div class="dz-st-pt-cell">Illimités</div>
    <div class="dz-st-pt-label">Stockage</div><div class="dz-st-pt-cell">5 Go</div><div class="dz-st-pt-cell dz-st-pt-hl">500 Go</div><div class="dz-st-pt-cell">5 To</div>
    <div class="dz-st-pt-label">Invités externes</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl">20</div><div class="dz-st-pt-cell">Illimités</div>

    <div class="dz-st-pt-group">Fonctionnalités</div>
    <div class="dz-st-pt-label">Automatisations</div><div class="dz-st-pt-cell">100 / mois</div><div class="dz-st-pt-cell dz-st-pt-hl">10 000 / mois</div><div class="dz-st-pt-cell">Illimitées</div>
    <div class="dz-st-pt-label">Tableaux de bord</div><div class="dz-st-pt-cell"><i class="fas fa-check dz-st-yes"></i></div><div class="dz-st-pt-cell dz-st-pt-hl"><i class="fas fa-check dz-st-yes"></i></div><div class="dz-st-pt-cell"><i class="fas fa-check dz-st-yes"></i></div>
    <div class="dz-st-pt-label">Portail client en marque blanche</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl"><i class="fas fa-check dz-st-yes"></i></div><div class="dz-st-pt-cell"><i class="fas fa-check dz-st-yes"></i></div>
    <div class="dz-st-pt-label">API et webhooks</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl">Lecture seule</div><div class="dz-st-pt-cell">Complète</div>

    <div class="dz-st-pt-group">Sécurité et support</div>
    <div class="dz-st-pt-label">Authentification unique (SSO)</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell"><i class="fas fa-check dz-st-yes"></i></div>
    <div class="dz-st-pt-label">Journal d'audit</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl">90 jours</div><div class="dz-st-pt-cell">Illimité</div>
    <div class="dz-st-pt-label">Support</div><div class="dz-st-pt-cell">E-mail</div><div class="dz-st-pt-cell dz-st-pt-hl">Chat · 4 h</div><div class="dz-st-pt-cell">Dédié · 1 h</div>
    <div class="dz-st-pt-label">Engagement de service</div><div class="dz-st-pt-cell"><span class="dz-st-no">—</span></div><div class="dz-st-pt-cell dz-st-pt-hl dz-st-pt-bottom">99,9 %</div><div class="dz-st-pt-cell">99,99 %</div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 6
    dict(
        name="calculateur de prix",
        icon="fas fa-calculator",
        html="""
<div class="dz-st-calc">
  <div class="dz-st-calc-form dz-reveal">
    <span class="dz-eyebrow">Estimation</span>
    <h2 class="dz-h2">Calculez <em>votre tarif</em></h2>
    <p class="dz-lead">Ajustez selon votre équipe. Le prix affiché est celui que vous paierez, sans frais cachés.</p>
    <div class="dz-st-range-row">
      <div class="dz-st-range-head"><span>Utilisateurs</span><b>25</b></div>
      <div class="dz-st-range" style="--v:24%"><span class="dz-st-range-fill"></span><span class="dz-st-range-thumb"></span></div>
      <div class="dz-st-range-scale"><span>1</span><span>25</span><span>50</span><span>100+</span></div>
    </div>
    <div class="dz-st-range-row">
      <div class="dz-st-range-head"><span>Stockage partagé</span><b>500 Go</b></div>
      <div class="dz-st-range" style="--v:50%"><span class="dz-st-range-fill"></span><span class="dz-st-range-thumb"></span></div>
      <div class="dz-st-range-scale"><span>50 Go</span><span>500 Go</span><span>1 To</span></div>
    </div>
    <div class="dz-st-options">
      <div class="dz-st-option dz-st-on"><span class="dz-st-checkbox"><i class="fas fa-check"></i></span><div class="dz-st-option-text"><b>Support prioritaire</b><span>Réponse en moins de 4 h</span></div><span class="dz-st-option-price">+ 49 €</span></div>
      <div class="dz-st-option"><span class="dz-st-checkbox"><i class="fas fa-check"></i></span><div class="dz-st-option-text"><b>Accompagnement au démarrage</b><span>3 sessions avec un expert</span></div><span class="dz-st-option-price">+ 390 € une fois</span></div>
    </div>
  </div>
  <div class="dz-st-quote dz-reveal-right">
    <div class="dz-st-quote-top">
      <span class="dz-small">Votre estimation</span>
      <div class="dz-st-seg"><span>Mensuel</span><span class="dz-st-on">Annuel</span></div>
    </div>
    <div class="dz-st-quote-total"><b class="dz-counter">529 €</b><span>HT / mois, facturé annuellement</span></div>
    <span class="dz-st-save"><i class="fas fa-piggy-bank"></i> Vous économisez 1 596 € par an</span>
    <div class="dz-st-quote-lines">
      <div class="dz-st-quote-line"><span>25 utilisateurs × 19,20 €</span><b>480 €</b></div>
      <div class="dz-st-quote-line"><span>Stockage 500 Go</span><b>Inclus</b></div>
      <div class="dz-st-quote-line"><span>Support prioritaire</span><b>49 €</b></div>
      <div class="dz-st-quote-line dz-st-quote-sum"><span>Total annuel HT</span><b>6 348 €</b></div>
    </div>
    <a class="dz-btn dz-btn-lg dz-btn-block" href="#">Démarrer avec ce tarif</a>
    <span class="dz-st-quote-foot"><i class="fas fa-lock"></i> Paiement sécurisé · Résiliable à tout moment</span>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 7
    dict(
        name="mur de témoignages",
        icon="fas fa-comments",
        html="""
<div class="dz-st-wall-head dz-reveal">
  <div class="dz-st-wall-title"><span class="dz-eyebrow">Avis clients</span><h2 class="dz-h2">Ils en parlent <em>mieux que nous</em></h2></div>
  <div class="dz-st-score"><b>4,9</b><div class="dz-st-score-meta"><span class="dz-stars">★★★★★</span><span class="dz-small">2 318 avis · note moyenne</span></div></div>
</div>
<div class="dz-st-wall">
  <div class="dz-st-wall-item dz-st-wall-feature"><p class="dz-st-wall-quote">« On a remplacé quatre outils et deux tableurs. Six mois plus tard, personne ne veut revenir en arrière. »</p><div class="dz-person"><span class="dz-avatar">CL</span><div><div class="dz-person-name">Clémence Laurent</div><div class="dz-person-role">Directrice des opérations · Maison Oré</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★★</span><p>Mise en place en une après-midi. Le support a répondu en 6 minutes un dimanche soir.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">TG</span><div><div class="dz-person-name">Thomas Garnier</div><div class="dz-person-role">Fondateur · Kobalt</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★★</span><p>Les relances automatiques nous ont fait gagner 9 jours de délai de paiement moyen. Concrètement, c'est 40 000 € de trésorerie en plus chaque mois.</p><div class="dz-st-wall-metric"><b>−9 j</b><span>délai de paiement</span></div><div class="dz-person"><span class="dz-avatar dz-avatar-sm">NB</span><div><div class="dz-person-name">Nadia Benali</div><div class="dz-person-role">DAF · Groupe Hélio</div></div></div></div>
  <div class="dz-st-wall-item dz-st-wall-photo"><div class="dz-st-wall-img"><img class="dz-cover" src="https://picsum.photos/seed/atelier-bois/600/400" alt="Atelier de menuiserie"></div><p>Même mes artisans les moins à l'aise avec l'informatique l'utilisent sur leur téléphone.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">PM</span><div><div class="dz-person-name">Pierre Morel</div><div class="dz-person-role">Gérant · Menuiserie Morel</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★★</span><p>Enfin un outil français qui n'a rien à envier aux géants américains.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">AR</span><div><div class="dz-person-name">Awa Richard</div><div class="dz-person-role">CTO · Sillage</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★☆</span><p>Très complet. Il faut une semaine pour tout explorer, mais la documentation est excellente et les modèles font gagner un temps fou.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">JF</span><div><div class="dz-person-name">Julien Fabre</div><div class="dz-person-role">Chef de projet · Norden</div></div></div></div>
  <div class="dz-st-wall-item dz-st-wall-brand"><i class="fas fa-quote-left"></i><p>Notre taux de conversion a doublé après la refonte du tunnel. Le tableau de bord nous a montré exactement où ça bloquait.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">EV</span><div><div class="dz-person-name">Élise Vasseur</div><div class="dz-person-role">Growth · Tessera</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★★</span><p>Les droits d'accès sont fins et le journal d'audit a rassuré notre DSI dès la première démo.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">MD</span><div><div class="dz-person-name">Marc Dubois</div><div class="dz-person-role">RSSI · Brume Assurances</div></div></div></div>
  <div class="dz-st-wall-item"><span class="dz-stars">★★★★★</span><p>Simple, beau, rapide. Trois mots que je n'avais jamais associés à un logiciel de gestion.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">LS</span><div><div class="dz-person-name">Léa Simon</div><div class="dz-person-role">Designer indépendante</div></div></div></div>
</div>
<div class="dz-st-wall-more"><a class="dz-btn dz-btn-ghost" href="#">Lire les 2 318 avis <i class="fas fa-arrow-right"></i></a></div>
""",
    ),
    # ------------------------------------------------------------------ 8
    dict(
        name="études de cas",
        icon="fas fa-briefcase",
        html="""
<div class="dz-section-head dz-left dz-reveal">
  <span class="dz-eyebrow">Études de cas</span>
  <h2 class="dz-h2">Des résultats <em>mesurés</em>, pas promis</h2>
</div>
<a class="dz-st-case-main dz-reveal" href="#">
  <div class="dz-st-case-media"><img class="dz-cover" src="https://picsum.photos/seed/entrepot-lumiere/1200/900" alt="Entrepôt logistique lumineux"><span class="dz-st-case-client">Kobalt Logistique</span></div>
  <div class="dz-st-case-body">
    <div class="dz-cluster"><span class="dz-badge dz-badge-neutral">Logistique</span><span class="dz-badge dz-badge-neutral">420 salariés</span></div>
    <h3 class="dz-h3">Comment Kobalt a divisé par trois le temps de traitement de ses litiges</h3>
    <p class="dz-text">Les réclamations transporteurs passaient par six boîtes mail. En huit semaines, tout a été centralisé, priorisé et en partie automatisé.</p>
    <div class="dz-st-case-metrics">
      <div class="dz-st-case-metric"><b>÷ 3</b><span>temps de traitement</span></div>
      <div class="dz-st-case-metric"><b>312 k€</b><span>récupérés en 2026</span></div>
      <div class="dz-st-case-metric"><b>8 sem.</b><span>de déploiement</span></div>
    </div>
    <span class="dz-st-case-link">Lire l'étude complète <i class="fas fa-arrow-right"></i></span>
  </div>
</a>
<div class="dz-st-cases">
  <a class="dz-st-case" href="#"><div class="dz-st-case-thumb"><img class="dz-cover" src="https://picsum.photos/seed/boutique-ceramique/800/520" alt="Boutique de céramique"></div><div class="dz-st-case-info"><span class="dz-st-case-sector">Commerce · Maison Oré</span><h4 class="dz-st-case-title">+64 % de ventes en ligne après la refonte du tunnel</h4><span class="dz-st-case-stat"><b>+64 %</b> ventes</span></div></a>
  <a class="dz-st-case" href="#"><div class="dz-st-case-thumb"><img class="dz-cover" src="https://picsum.photos/seed/clinique-claire/800/520" alt="Cabinet médical"></div><div class="dz-st-case-info"><span class="dz-st-case-sector">Santé · Centre Hélio</span><h4 class="dz-st-case-title">2 400 rendez-vous pris en ligne chaque semaine</h4><span class="dz-st-case-stat"><b>−38 %</b> appels</span></div></a>
  <a class="dz-st-case" href="#"><div class="dz-st-case-thumb"><img class="dz-cover" src="https://picsum.photos/seed/bureau-verre/800/520" alt="Bureaux vitrés"></div><div class="dz-st-case-info"><span class="dz-st-case-sector">Conseil · Norden Partners</span><h4 class="dz-st-case-title">Des propositions commerciales envoyées en 20 minutes</h4><span class="dz-st-case-stat"><b>×4</b> propositions</span></div></a>
</div>
""",
    ),
    # ------------------------------------------------------------------ 9
    dict(
        name="chiffres clés sur fond sombre",
        icon="fas fa-sort-numeric-up",
        wrap="none",
        html="""
<section class="dz-st-night dz-st-stats-dark">
  <div class="dz-st-stats-grid-bg"></div>
  <div class="dz-container">
    <div class="dz-st-stats-head dz-reveal">
      <span class="dz-eyebrow">En chiffres</span>
      <h2 class="dz-h2">Une infrastructure qui <em>ne dort jamais</em></h2>
    </div>
    <div class="dz-st-stats dz-stagger">
      <div class="dz-st-stat"><span class="dz-st-stat-value"><span class="dz-counter">4,2</span> Md</span><span class="dz-st-stat-label">requêtes traitées par mois</span><span class="dz-st-stat-bar" style="--v:86%"></span></div>
      <div class="dz-st-stat"><span class="dz-st-stat-value"><span class="dz-counter">38</span> ms</span><span class="dz-st-stat-label">temps de réponse médian</span><span class="dz-st-stat-bar" style="--v:34%"></span></div>
      <div class="dz-st-stat"><span class="dz-st-stat-value"><span class="dz-counter">99,99</span> %</span><span class="dz-st-stat-label">disponibilité sur 12 mois</span><span class="dz-st-stat-bar" style="--v:99%"></span></div>
      <div class="dz-st-stat"><span class="dz-st-stat-value"><span class="dz-counter">12 400</span></span><span class="dz-st-stat-label">entreprises clientes</span><span class="dz-st-stat-bar" style="--v:64%"></span></div>
    </div>
    <div class="dz-st-stats-foot"><span class="dz-st-live"><span class="dz-dot"></span> Données en direct</span><span>Mesures publiques au 1er septembre 2026 · 3 centres de données en France</span></div>
  </div>
</section>
""",
    ),
    # ------------------------------------------------------------------ 10
    dict(
        name="logos clients en grille animée",
        icon="fas fa-building",
        html="""
<div class="dz-st-logos-head dz-reveal">
  <p class="dz-st-logos-lead">Plus de <b>4 000 équipes</b> de toutes tailles nous confient leur quotidien</p>
  <a class="dz-btn dz-btn-link" href="#">Voir les témoignages <i class="fas fa-arrow-right"></i></a>
</div>
<div class="dz-st-logos">
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-atom"></i> Nexora</span><span class="dz-st-logo"><i class="fas fa-moon"></i> Atelier Lune</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-star"></i> Polaris &amp; Co</span><span class="dz-st-logo"><i class="fas fa-water"></i> Ondine</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-mountain"></i> Vertige</span><span class="dz-st-logo"><i class="fas fa-gem"></i> Quartz Labs</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-sun"></i> Hélio</span><span class="dz-st-logo"><i class="fas fa-cube"></i> Kobalt</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-leaf"></i> Verdure</span><span class="dz-st-logo"><i class="fas fa-compass"></i> Norden</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-feather-alt"></i> Sillage</span><span class="dz-st-logo"><i class="fas fa-cloud"></i> Brume</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-shapes"></i> Tessera</span><span class="dz-st-logo"><i class="fas fa-circle-notch"></i> Maison Oré</span></div>
  <div class="dz-st-logo-cell"><span class="dz-st-logo"><i class="fas fa-wind"></i> Alizé</span><span class="dz-st-logo"><i class="fas fa-seedling"></i> Germe</span></div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 11
    dict(
        name="comment ça marche (3 étapes illustrées)",
        icon="fas fa-shoe-prints",
        html="""
<div class="dz-section-head dz-reveal">
  <span class="dz-eyebrow">Comment ça marche</span>
  <h2 class="dz-h2">Opérationnel <em>en trois étapes</em></h2>
  <p class="dz-lead">Comptez une heure entre la création du compte et votre premier rapport.</p>
</div>
<div class="dz-st-how dz-stagger">
  <div class="dz-st-how-step">
    <div class="dz-st-how-art">
      <div class="dz-st-drop"><i class="fas fa-cloud-upload-alt"></i><span>Déposez vos fichiers</span></div>
      <div class="dz-st-file"><i class="fas fa-file-csv"></i><div class="dz-st-file-info"><b>clients-2026.csv</b><span class="dz-st-file-bar"><span style="--v:72%"></span></span></div><span class="dz-st-file-pct">72 %</span></div>
    </div>
    <span class="dz-st-how-num">1</span>
    <h3 class="dz-h4">Importez vos données</h3>
    <p class="dz-text">Tableur, ancien logiciel ou saisie : les colonnes sont reconnues automatiquement.</p>
  </div>
  <div class="dz-st-how-step">
    <div class="dz-st-how-art">
      <div class="dz-st-rule"><span class="dz-st-rule-k">Si</span><span class="dz-st-rule-v">montant &gt; 5 000 €</span></div>
      <div class="dz-st-rule"><span class="dz-st-rule-k">Alors</span><span class="dz-st-rule-v">validation par Sarah</span></div>
      <div class="dz-st-rule dz-st-rule-ok"><i class="fas fa-check-circle"></i><span>Règle active · 3 règles au total</span></div>
    </div>
    <span class="dz-st-how-num">2</span>
    <h3 class="dz-h4">Réglez vos règles</h3>
    <p class="dz-text">Validations, notifications, affectations : décrivez comment votre équipe travaille.</p>
  </div>
  <div class="dz-st-how-step">
    <div class="dz-st-how-art">
      <div class="dz-st-how-kpi"><span>Délai moyen</span><b>2,4 j</b><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-down"></i> 61 %</span></div>
      <div class="dz-st-spark"><span style="--h:90%"></span><span style="--h:78%"></span><span style="--h:70%"></span><span style="--h:56%"></span><span style="--h:48%"></span><span style="--h:36%"></span><span style="--h:30%"></span></div>
    </div>
    <span class="dz-st-how-num">3</span>
    <h3 class="dz-h4">Suivez les résultats</h3>
    <p class="dz-text">Un tableau de bord prêt à l'emploi, partagé chaque lundi à 8 h avec qui vous voulez.</p>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 12
    dict(
        name="catalogue d'intégrations",
        icon="fas fa-puzzle-piece",
        html="""
<div class="dz-section-head dz-reveal">
  <span class="dz-eyebrow">Intégrations</span>
  <h2 class="dz-h2">Branché sur <em>vos outils</em></h2>
  <p class="dz-lead">86 connecteurs officiels, une API ouverte et des webhooks pour tout le reste.</p>
</div>
<div class="dz-st-int">
  <div class="dz-st-int-side">
    <div class="dz-st-search"><i class="fas fa-search"></i><span>Rechercher un outil…</span><span class="dz-kbd">/</span></div>
    <div class="dz-st-int-cats">
      <a class="dz-st-int-cat dz-st-on" href="#"><span>Toutes</span><b>86</b></a>
      <a class="dz-st-int-cat" href="#"><span>Relation client</span><b>14</b></a>
      <a class="dz-st-int-cat" href="#"><span>Paiement</span><b>9</b></a>
      <a class="dz-st-int-cat" href="#"><span>Messagerie</span><b>12</b></a>
      <a class="dz-st-int-cat" href="#"><span>Stockage</span><b>8</b></a>
      <a class="dz-st-int-cat" href="#"><span>Comptabilité</span><b>11</b></a>
      <a class="dz-st-int-cat" href="#"><span>Analyse</span><b>7</b></a>
    </div>
    <div class="dz-st-int-request"><b>Il manque un outil ?</b><span>Proposez-le, on le développe si 20 clients le demandent.</span><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Suggérer</a></div>
  </div>
  <div class="dz-st-int-grid">
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-1"><i class="fas fa-comment-dots"></i></span><span class="dz-badge dz-badge-success">Installée</span></div><b>Parlo</b><span class="dz-st-app-cat">Messagerie</span><p>Recevez les alertes dans vos canaux et répondez sans changer d'onglet.</p></a>
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-2"><i class="fas fa-credit-card"></i></span><span class="dz-st-app-add">Connecter</span></div><b>Payora</b><span class="dz-st-app-cat">Paiement</span><p>Encaissez par carte et prélèvement, rapprochement automatique.</p></a>
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-3"><i class="fas fa-address-book"></i></span><span class="dz-st-app-add">Connecter</span></div><b>Contakt</b><span class="dz-st-app-cat">Relation client</span><p>Synchronisez contacts, sociétés et opportunités dans les deux sens.</p></a>
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-4"><i class="fas fa-hdd"></i></span><span class="dz-badge dz-badge-success">Installée</span></div><b>Nuage Drive</b><span class="dz-st-app-cat">Stockage</span><p>Joignez des fichiers et gardez les versions à jour partout.</p></a>
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-5"><i class="fas fa-book"></i></span><span class="dz-st-app-add">Connecter</span></div><b>Comptalib</b><span class="dz-st-app-cat">Comptabilité</span><p>Export des écritures et des justificatifs chaque nuit.</p></a>
    <a class="dz-st-app" href="#"><div class="dz-st-app-top"><span class="dz-st-app-icon dz-st-hue-6"><i class="fas fa-chart-pie"></i></span><span class="dz-badge dz-badge-neutral">Bêta</span></div><b>Mesura</b><span class="dz-st-app-cat">Analyse</span><p>Envoyez chaque événement vers votre entrepôt de données.</p></a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 13
    dict(
        name="fondateurs et histoire",
        icon="fas fa-user-friends",
        html="""
<div class="dz-st-founders">
  <div class="dz-st-founders-story dz-reveal">
    <span class="dz-eyebrow">Notre histoire</span>
    <h2 class="dz-h2">Deux associés, <em>une obsession</em> : le temps des autres</h2>
    <p class="dz-lead">En 2019, Inès gérait une agence de 12 personnes et passait ses dimanches dans des tableurs. Malik, lui, construisait des outils internes pour des banques. Ils se sont rencontrés à Lyon, dans un atelier de céramique.</p>
    <div class="dz-st-milestones">
      <div class="dz-st-milestone"><b>2019</b><span>Premier prototype, testé par 8 agences amies</span></div>
      <div class="dz-st-milestone"><b>2022</b><span>Levée de 6 M€ et ouverture du bureau de Nantes</span></div>
      <div class="dz-st-milestone"><b>2026</b><span>12 400 clients, 86 personnes, toujours indépendants</span></div>
    </div>
    <p class="dz-st-signature">Inès &amp; Malik</p>
  </div>
  <div class="dz-st-founders-cards">
    <div class="dz-st-founder dz-st-founder-a dz-reveal">
      <div class="dz-st-founder-photo"><img class="dz-cover" src="https://picsum.photos/seed/portrait-ines/600/760" alt="Portrait d'Inès Carpentier"></div>
      <div class="dz-st-founder-info"><div><b>Inès Carpentier</b><span>Cofondatrice · Directrice générale</span></div><a class="dz-st-founder-link" href="#" aria-label="Profil d'Inès"><i class="fas fa-link"></i></a></div>
    </div>
    <div class="dz-st-founder dz-st-founder-b dz-reveal">
      <div class="dz-st-founder-photo"><img class="dz-cover" src="https://picsum.photos/seed/portrait-malik/600/760" alt="Portrait de Malik Haddad"></div>
      <div class="dz-st-founder-info"><div><b>Malik Haddad</b><span>Cofondateur · Directeur technique</span></div><a class="dz-st-founder-link" href="#" aria-label="Profil de Malik"><i class="fas fa-link"></i></a></div>
    </div>
    <div class="dz-st-founder-note"><i class="fas fa-quote-left"></i><span>On construit l'outil qu'on aurait aimé avoir.</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 14
    dict(
        name="carrières (offres d'emploi)",
        icon="fas fa-user-tie",
        html="""
<div class="dz-st-jobs-head dz-reveal">
  <div><span class="dz-eyebrow">Carrières</span><h2 class="dz-h2">Construisez <em>avec nous</em></h2><p class="dz-lead">86 personnes, 11 nationalités, bureaux à Lyon et Nantes, télétravail possible partout en France.</p></div>
  <div class="dz-st-perks">
    <div class="dz-st-perk"><i class="fas fa-laptop-house"></i><span>Télétravail flexible</span></div>
    <div class="dz-st-perk"><i class="fas fa-umbrella-beach"></i><span>30 jours de congés</span></div>
    <div class="dz-st-perk"><i class="fas fa-chart-pie"></i><span>BSPCE pour tous</span></div>
    <div class="dz-st-perk"><i class="fas fa-graduation-cap"></i><span>2 000 € de formation</span></div>
  </div>
</div>
<div class="dz-st-jobs">
  <div class="dz-st-jobs-filters dz-chips"><span class="dz-chip dz-active">Tous · 8</span><span class="dz-chip">Produit · 2</span><span class="dz-chip">Ingénierie · 3</span><span class="dz-chip">Ventes · 2</span><span class="dz-chip">Support · 1</span></div>
  <a class="dz-st-job" href="#"><div class="dz-st-job-main"><b>Développeur·se back-end senior</b><span class="dz-st-job-team">Ingénierie · Plateforme</span></div><div class="dz-st-job-meta"><span><i class="fas fa-map-marker-alt"></i> Lyon ou télétravail</span><span><i class="fas fa-file-contract"></i> CDI</span><span class="dz-st-job-salary">65 – 80 k€</span></div><span class="dz-st-job-go"><i class="fas fa-arrow-right"></i></span></a>
  <a class="dz-st-job" href="#"><div class="dz-st-job-main"><b>Product designer <span class="dz-badge">Nouveau</span></b><span class="dz-st-job-team">Produit · Expérience client</span></div><div class="dz-st-job-meta"><span><i class="fas fa-map-marker-alt"></i> Nantes</span><span><i class="fas fa-file-contract"></i> CDI</span><span class="dz-st-job-salary">52 – 62 k€</span></div><span class="dz-st-job-go"><i class="fas fa-arrow-right"></i></span></a>
  <a class="dz-st-job" href="#"><div class="dz-st-job-main"><b>Ingénieur·e fiabilité (SRE)</b><span class="dz-st-job-team">Ingénierie · Infrastructure</span></div><div class="dz-st-job-meta"><span><i class="fas fa-map-marker-alt"></i> Télétravail</span><span><i class="fas fa-file-contract"></i> CDI</span><span class="dz-st-job-salary">60 – 75 k€</span></div><span class="dz-st-job-go"><i class="fas fa-arrow-right"></i></span></a>
  <a class="dz-st-job" href="#"><div class="dz-st-job-main"><b>Account executive mid-market</b><span class="dz-st-job-team">Ventes · Paris et région</span></div><div class="dz-st-job-meta"><span><i class="fas fa-map-marker-alt"></i> Lyon</span><span><i class="fas fa-file-contract"></i> CDI</span><span class="dz-st-job-salary">45 k€ + variable</span></div><span class="dz-st-job-go"><i class="fas fa-arrow-right"></i></span></a>
  <a class="dz-st-job" href="#"><div class="dz-st-job-main"><b>Alternance · Chargé·e de support</b><span class="dz-st-job-team">Support · Niveau 1</span></div><div class="dz-st-job-meta"><span><i class="fas fa-map-marker-alt"></i> Nantes</span><span><i class="fas fa-file-contract"></i> Alternance</span><span class="dz-st-job-salary">Rentrée 2026</span></div><span class="dz-st-job-go"><i class="fas fa-arrow-right"></i></span></a>
  <div class="dz-st-jobs-foot"><span class="dz-small">Vous ne trouvez pas votre poste ?</span><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Candidature spontanée</a></div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 15
    dict(
        name="presse et médias",
        icon="fas fa-newspaper",
        html="""
<div class="dz-st-press">
  <div class="dz-st-press-feature dz-reveal">
    <span class="dz-st-outlet dz-st-outlet-lg">Le Quotidien Numérique</span>
    <p class="dz-st-press-quote">« L'un des rares logiciels de gestion qui donne <em>envie</em> de l'ouvrir le lundi matin. »</p>
    <div class="dz-st-press-meta"><span>Chronique « Outils » · 14 mai 2026</span><a class="dz-btn dz-btn-link" href="#">Lire l'article <i class="fas fa-arrow-right"></i></a></div>
  </div>
  <div class="dz-st-press-list">
    <a class="dz-st-article" href="#"><div class="dz-st-article-head"><span class="dz-st-outlet">Tech &amp; Société</span><span class="dz-small">2 sept. 2026</span></div><b>Les nouveaux champions français du logiciel pour PME</b><span class="dz-st-article-type"><i class="fas fa-file-alt"></i> Dossier</span></a>
    <a class="dz-st-article" href="#"><div class="dz-st-article-head"><span class="dz-st-outlet">Radio Bastion</span><span class="dz-small">18 juin 2026</span></div><b>Inès Carpentier, invitée de « L'Entreprise du matin »</b><span class="dz-st-article-type"><i class="fas fa-podcast"></i> Podcast · 24 min</span></a>
    <a class="dz-st-article" href="#"><div class="dz-st-article-head"><span class="dz-st-outlet">L'Hebdo des Start-up</span><span class="dz-small">3 mars 2026</span></div><b>Une levée de 18 M€ pour accélérer en Europe</b><span class="dz-st-article-type"><i class="fas fa-file-alt"></i> Article</span></a>
  </div>
  <div class="dz-st-presskit">
    <span class="dz-st-presskit-icon"><i class="fas fa-download"></i></span>
    <div class="dz-st-presskit-text"><b>Kit presse</b><span>Logos, photos HD, chiffres clés · ZIP 48 Mo</span></div>
    <a class="dz-btn dz-btn-sm" href="#">Télécharger</a>
    <div class="dz-st-presskit-contact"><span class="dz-avatar dz-avatar-sm">CR</span><div><b>Chloé Roux</b><span>presse@nexora.fr · 04 72 00 18 36</span></div></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 16
    dict(
        name="contact avec carte",
        icon="fas fa-map-marked-alt",
        html="""
<div class="dz-st-contact">
  <div class="dz-st-map dz-reveal">
    <span class="dz-st-map-river"></span><span class="dz-st-map-park dz-st-map-park-a"></span><span class="dz-st-map-park dz-st-map-park-b"></span>
    <span class="dz-st-map-road dz-st-map-road-a"></span><span class="dz-st-map-road dz-st-map-road-b"></span>
    <span class="dz-st-pin"><i class="fas fa-map-marker-alt"></i></span>
    <div class="dz-st-map-card"><span class="dz-st-map-thumb"><img class="dz-cover" src="https://picsum.photos/seed/facade-lyon/200/200" alt="Façade du siège"></span><div class="dz-st-map-card-text"><b>Siège · Lyon 2e</b><span>18 rue des Tanneurs, 69002 Lyon</span><a class="dz-btn dz-btn-link dz-btn-sm" href="#">Itinéraire <i class="fas fa-directions"></i></a></div></div>
    <div class="dz-st-map-zoom"><span>+</span><span>−</span></div>
  </div>
  <div class="dz-st-contact-info dz-reveal">
    <span class="dz-eyebrow">Contact</span>
    <h2 class="dz-h2">Passez nous voir, <em>ou écrivez-nous</em></h2>
    <div class="dz-st-channels">
      <a class="dz-st-channel" href="#"><span class="dz-icon"><i class="fas fa-comments"></i></span><div class="dz-st-channel-text"><b>Discuter maintenant</b><span><span class="dz-st-online"></span> 3 conseillers en ligne · réponse en 2 min</span></div><i class="fas fa-chevron-right"></i></a>
      <a class="dz-st-channel" href="#"><span class="dz-icon"><i class="fas fa-envelope"></i></span><div class="dz-st-channel-text"><b>bonjour@nexora.fr</b><span>Réponse sous 24 h ouvrées</span></div><i class="fas fa-chevron-right"></i></a>
      <a class="dz-st-channel" href="#"><span class="dz-icon"><i class="fas fa-phone"></i></span><div class="dz-st-channel-text"><b>04 72 00 18 30</b><span>Lun. – ven., 9 h – 18 h</span></div><i class="fas fa-chevron-right"></i></a>
    </div>
    <div class="dz-st-offices"><span class="dz-small">Autres bureaux</span><div class="dz-cluster"><span class="dz-chip">Nantes</span><span class="dz-chip">Lille</span><span class="dz-chip">Bruxelles</span></div></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 17
    dict(
        name="pied de page riche (newsletter)",
        icon="fas fa-shoe-prints",
        wrap="none",
        html="""
<footer class="dz-st-footer">
  <div class="dz-container">
    <div class="dz-st-footer-news">
      <div class="dz-st-footer-news-copy"><h3 class="dz-h3">La lettre du lundi</h3><p>Un conseil de gestion, un outil, un chiffre. Lu par 38 000 dirigeants, 3 minutes chrono.</p></div>
      <div class="dz-st-capture dz-st-capture-sm">
        <div class="dz-st-capture-field"><i class="far fa-envelope"></i><input type="email" placeholder="vous@entreprise.fr" aria-label="Adresse e-mail"></div>
        <a class="dz-btn" href="#">S'abonner</a>
      </div>
    </div>
    <div class="dz-st-footer-grid">
      <div class="dz-st-footer-brand">
        <a class="dz-brand" href="#"><span class="dz-brand-mark"></span>Nexora</a>
        <p>Le logiciel de gestion des équipes qui avancent vite. Conçu et hébergé en France.</p>
        <div class="dz-st-stores"><a class="dz-st-store" href="#"><i class="fas fa-mobile-alt"></i><span><small>Application</small>iPhone et Android</span></a><a class="dz-st-store" href="#"><i class="fas fa-desktop"></i><span><small>Application</small>Mac et Windows</span></a></div>
      </div>
      <div class="dz-st-footer-col"><span class="dz-st-footer-title">Produit</span><a href="#">Fonctionnalités</a><a href="#">Tarifs</a><a href="#">Intégrations</a><a href="#">Nouveautés <span class="dz-badge">4.0</span></a><a href="#">Feuille de route</a></div>
      <div class="dz-st-footer-col"><span class="dz-st-footer-title">Ressources</span><a href="#">Centre d'aide</a><a href="#">Documentation API</a><a href="#">Modèles</a><a href="#">Webinaires</a><a href="#">Blog</a></div>
      <div class="dz-st-footer-col"><span class="dz-st-footer-title">Entreprise</span><a href="#">À propos</a><a href="#">Carrières <span class="dz-badge dz-badge-success">8 postes</span></a><a href="#">Presse</a><a href="#">Partenaires</a><a href="#">Contact</a></div>
      <div class="dz-st-footer-col"><span class="dz-st-footer-title">Légal</span><a href="#">Mentions légales</a><a href="#">Confidentialité</a><a href="#">CGV</a><a href="#">Sécurité</a><a href="#">Cookies</a></div>
    </div>
    <div class="dz-st-footer-bottom">
      <span>© 2026 Nexora SAS · Lyon</span>
      <a class="dz-st-status" href="#"><span class="dz-st-online"></span> Tous les systèmes sont opérationnels</a>
      <div class="dz-st-footer-end">
        <span class="dz-st-lang"><i class="fas fa-globe"></i> Français</span>
        <div class="dz-socials"><a href="#" aria-label="Flux RSS"><i class="fas fa-rss"></i></a><a href="#" aria-label="Podcast"><i class="fas fa-podcast"></i></a><a href="#" aria-label="Vidéos"><i class="fas fa-video"></i></a></div>
      </div>
    </div>
  </div>
</footer>
""",
    ),
    # ------------------------------------------------------------------ 18
    dict(
        name="bannière d'annonce produit",
        icon="fas fa-bullhorn",
        html="""
<div class="dz-st-launch dz-reveal">
  <div class="dz-st-launch-inner">
    <div class="dz-st-launch-copy">
      <div class="dz-cluster"><span class="dz-st-launch-tag"><i class="fas fa-rocket"></i> Lancement</span><span class="dz-st-launch-date">Disponible depuis le 22 septembre 2026</span></div>
      <h2 class="dz-h2">Nexora 4.0 est là. <em>Et il pense avec vous.</em></h2>
      <p class="dz-lead">Un assistant qui prépare vos relances, résume vos réunions et repère les dérives de budget avant vous.</p>
      <div class="dz-cluster"><a class="dz-btn dz-btn-lg" href="#">Découvrir la 4.0 <i class="fas fa-arrow-right"></i></a><a class="dz-btn dz-btn-ghost dz-btn-lg" href="#"><i class="fas fa-play"></i> Keynote · 12 min</a></div>
    </div>
    <div class="dz-st-launch-list">
      <div class="dz-st-launch-item"><span class="dz-st-launch-ico"><i class="fas fa-magic"></i></span><div><b>Assistant intégré</b><span>Dans chaque écran, sur vos données</span></div></div>
      <div class="dz-st-launch-item"><span class="dz-st-launch-ico"><i class="fas fa-tachometer-alt"></i></span><div><b>2× plus rapide</b><span>Nouveau moteur de recherche</span></div></div>
      <div class="dz-st-launch-item"><span class="dz-st-launch-ico"><i class="fas fa-mobile-alt"></i></span><div><b>Mode hors ligne</b><span>Sur l'application mobile</span></div></div>
      <span class="dz-st-launch-version">v4.0.0</span>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 19
    dict(
        name="sécurité et conformité",
        icon="fas fa-shield-alt",
        html="""
<div class="dz-st-sec">
  <div class="dz-st-sec-copy dz-reveal">
    <span class="dz-eyebrow">Sécurité</span>
    <h2 class="dz-h2">Vos données restent <em>les vôtres</em></h2>
    <p class="dz-lead">Hébergement souverain, chiffrement de bout en bout et audits indépendants chaque année. Votre DSI va adorer.</p>
    <div class="dz-st-sec-points">
      <div class="dz-st-sec-point"><i class="fas fa-lock"></i><div><b>Chiffrement AES-256 et TLS 1.3</b><span>Au repos comme en transit, clés gérées en France.</span></div></div>
      <div class="dz-st-sec-point"><i class="fas fa-user-lock"></i><div><b>SSO, double authentification, rôles fins</b><span>Chaque accès est tracé dans le journal d'audit.</span></div></div>
      <div class="dz-st-sec-point"><i class="fas fa-history"></i><div><b>Sauvegardes chaque heure</b><span>Conservées 35 jours sur deux sites distincts.</span></div></div>
    </div>
    <a class="dz-btn dz-btn-ghost" href="#"><i class="fas fa-shield-alt"></i> Visiter le centre de confiance</a>
  </div>
  <div class="dz-st-seals dz-stagger">
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-user-shield"></i></span><b>RGPD</b><span>Conforme · DPO dédié</span></div>
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-certificate"></i></span><b>ISO 27001</b><span>Certifié depuis 2023</span></div>
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-clipboard-check"></i></span><b>SOC 2 Type II</b><span>Rapport sur demande</span></div>
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-heartbeat"></i></span><b>HDS</b><span>Données de santé</span></div>
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-flag"></i></span><b>Hébergé en France</b><span>3 centres de données</span></div>
    <div class="dz-st-seal"><span class="dz-st-seal-ring"><i class="fas fa-bug"></i></span><b>Tests d'intrusion</b><span>Chaque trimestre</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 20
    dict(
        name="appel final spectaculaire",
        icon="fas fa-rocket",
        html="""
<div class="dz-st-finale">
  <div class="dz-st-finale-rings"><span></span><span></span><span></span><span></span></div>
  <div class="dz-st-finale-grid"></div>
  <span class="dz-st-finale-av dz-st-finale-av-1 dz-avatar">IC</span>
  <span class="dz-st-finale-av dz-st-finale-av-2 dz-avatar">MH</span>
  <span class="dz-st-finale-av dz-st-finale-av-3 dz-avatar">LS</span>
  <span class="dz-st-finale-av dz-st-finale-av-4 dz-avatar">TG</span>
  <div class="dz-st-finale-inner dz-reveal-zoom">
    <span class="dz-st-finale-kicker"><span class="dz-dot"></span> 312 équipes ont démarré cette semaine</span>
    <h2 class="dz-st-finale-title">Prêt à reprendre <em>le contrôle</em> ?</h2>
    <p class="dz-st-finale-lead">Créez votre espace en 30 secondes. Importez vos données en une heure. Oubliez vos tableurs pour de bon.</p>
    <div class="dz-cluster dz-st-finale-actions"><a class="dz-btn dz-btn-lg dz-btn-shine" href="#">Commencer gratuitement <i class="fas fa-arrow-right"></i></a><a class="dz-btn dz-btn-ghost dz-btn-lg" href="#">Réserver une démo</a></div>
    <div class="dz-st-finale-notes"><span><i class="fas fa-check"></i> 14 jours offerts</span><span><i class="fas fa-check"></i> Sans carte bancaire</span><span><i class="fas fa-check"></i> Migration accompagnée</span></div>
  </div>
</div>
""",
    ),
]
