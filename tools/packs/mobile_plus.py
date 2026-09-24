"""Mobile (ajouts) : écrans d'application mobile, dans un cadre de téléphone sur ordinateur
et en pleine largeur sur téléphone. CSS : styles/45-mobile-plus.css (préfixe dz-mb-)."""
FAMILY = "mobile"

STATUS = """<div class="dz-mb-status"><span class="dz-mb-time">9:41</span><span class="dz-mb-status-icons"><i class="fas fa-signal"></i><i class="fas fa-wifi"></i><i class="fas fa-battery-three-quarters"></i></span></div>"""
STATUS_LIGHT = STATUS.replace('dz-mb-status"', 'dz-mb-status dz-mb-status-light"')


def tabs(active, items=None):
    items = items or [("fas fa-home", "Accueil"), ("fas fa-compass", "Explorer"), ("fas fa-calendar-alt", "Agenda"), ("fas fa-user", "Profil")]
    out = []
    for i, (ic, label) in enumerate(items):
        on = " dz-mb-on" if i == active else ""
        out.append(f'<a class="dz-mb-tab{on}" href="#"><i class="{ic}"></i><span>{label}</span></a>')
    return '<nav class="dz-mb-tabs">' + "".join(out) + "</nav>"


def phone(inner, cls=""):
    return f'<div class="dz-mb-stage"><div class="dz-mb-phone"><div class="dz-mb-screen {cls}">{inner}</div></div></div>'


BLOCKS = [
    # ------------------------------------------------------------------ 1
    dict(
        name="accueil d'app",
        icon="fas fa-mobile-alt",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body">
  <div class="dz-mb-hello">
    <span class="dz-avatar dz-mb-av">LS</span>
    <div class="dz-mb-hello-text"><span>Bonjour,</span><b>Léa Simon</b></div>
    <a class="dz-mb-round dz-mb-has-badge" href="#" aria-label="Notifications"><i class="far fa-bell"></i><span class="dz-mb-badge">3</span></a>
  </div>
  <div class="dz-mb-searchbar"><i class="fas fa-search"></i><span>Cours, coachs, studios…</span><i class="fas fa-sliders-h"></i></div>
  <div class="dz-mb-hero-card">
    <div class="dz-mb-hero-text"><span class="dz-mb-kicker">Cette semaine</span><b>3 séances sur 4</b><span>Plus qu'une pour tenir votre objectif</span></div>
    <div class="dz-mb-ring" style="--v:75"><span>75 %</span></div>
  </div>
  <div class="dz-mb-chips"><span class="dz-mb-chip dz-mb-on">Tout</span><span class="dz-mb-chip">Yoga</span><span class="dz-mb-chip">Pilates</span><span class="dz-mb-chip">Course</span><span class="dz-mb-chip">Méditation</span></div>
  <div class="dz-mb-sec-head"><b>À la une</b><a href="#">Tout voir</a></div>
  <div class="dz-mb-hscroll">
    <a class="dz-mb-feature" href="#"><div class="dz-mb-feature-img"><img class="dz-cover" src="https://picsum.photos/seed/yoga-matin/400/300" alt="Cours de yoga au lever du soleil"><span class="dz-mb-tag">Nouveau</span></div><b>Vinyasa du matin</b><span>Nadia · 35 min · Tous niveaux</span></a>
    <a class="dz-mb-feature" href="#"><div class="dz-mb-feature-img"><img class="dz-cover" src="https://picsum.photos/seed/pilates-studio/400/300" alt="Studio de pilates lumineux"></div><b>Pilates gainage</b><span>Hugo · 25 min · Intermédiaire</span></a>
  </div>
  <div class="dz-mb-sec-head"><b>Prochaine séance</b></div>
  <div class="dz-mb-next"><div class="dz-mb-date"><b>26</b><span>sept.</span></div><div class="dz-mb-next-text"><b>Yoga doux</b><span>Samedi · 10:00 · Studio Canopée</span></div><i class="fas fa-chevron-right"></i></div>
</div>
""" + tabs(0)),
    ),
    # ------------------------------------------------------------------ 2
    dict(
        name="liste avec balayage",
        icon="fas fa-hand-point-left",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body dz-mb-body-flush">
  <div class="dz-mb-largehead"><div class="dz-mb-toprow"><a class="dz-mb-link" href="#">Listes</a><a class="dz-mb-link" href="#">Modifier</a></div><h2 class="dz-mb-large">Aujourd'hui</h2><span class="dz-mb-sub">Jeudi 24 septembre · 6 tâches</span></div>
  <div class="dz-mb-seg"><span class="dz-mb-on">À faire</span><span>Planifié</span><span>Terminé</span></div>
  <div class="dz-mb-swipe-list">
    <div class="dz-mb-swipe"><div class="dz-mb-swipe-row"><span class="dz-mb-circle"></span><div class="dz-mb-row-text"><b>Appeler le plombier</b><span><i class="far fa-clock"></i> 10:00 · Maison</span></div><span class="dz-mb-flag"><i class="fas fa-flag"></i></span></div></div>
    <div class="dz-mb-swipe dz-mb-swiped-left">
      <div class="dz-mb-swipe-actions"><span class="dz-mb-act dz-mb-act-more"><i class="fas fa-ellipsis-h"></i>Plus</span><span class="dz-mb-act dz-mb-act-flag"><i class="fas fa-flag"></i>Signaler</span><span class="dz-mb-act dz-mb-act-del"><i class="fas fa-trash-alt"></i>Supprimer</span></div>
      <div class="dz-mb-swipe-row"><span class="dz-mb-circle"></span><div class="dz-mb-row-text"><b>Renouveler l'assurance habitation</b><span><i class="far fa-calendar"></i> Avant le 30 sept.</span></div></div>
    </div>
    <div class="dz-mb-swipe dz-mb-swiped-right">
      <div class="dz-mb-swipe-actions dz-mb-swipe-actions-left"><span class="dz-mb-act dz-mb-act-done"><i class="fas fa-check"></i>Fait</span></div>
      <div class="dz-mb-swipe-row"><span class="dz-mb-circle"></span><div class="dz-mb-row-text"><b>Courses pour le dîner</b><span><i class="fas fa-list"></i> 8 articles</span></div></div>
    </div>
    <div class="dz-mb-swipe"><div class="dz-mb-swipe-row"><span class="dz-mb-circle dz-mb-prio"></span><div class="dz-mb-row-text"><b>Envoyer le devis à Norden</b><span class="dz-mb-late"><i class="fas fa-exclamation-circle"></i> En retard · hier</span></div></div></div>
    <div class="dz-mb-swipe"><div class="dz-mb-swipe-row"><span class="dz-mb-circle"></span><div class="dz-mb-row-text"><b>Réserver le train pour Nantes</b><span><i class="fas fa-paperclip"></i> 1 pièce jointe</span></div></div></div>
    <div class="dz-mb-swipe"><div class="dz-mb-swipe-row"><span class="dz-mb-circle"></span><div class="dz-mb-row-text"><b>Arroser les plantes du bureau</b><span><i class="fas fa-redo"></i> Chaque lundi</span></div></div></div>
  </div>
  <div class="dz-mb-hint"><i class="fas fa-arrows-alt-h"></i> Balayez une tâche pour agir</div>
  <a class="dz-mb-fab" href="#" aria-label="Nouvelle tâche"><i class="fas fa-plus"></i></a>
</div>
""" + tabs(0, [("fas fa-check-circle", "Tâches"), ("fas fa-calendar-alt", "Agenda"), ("fas fa-search", "Chercher"), ("fas fa-cog", "Réglages")])),
    ),
    # ------------------------------------------------------------------ 3
    dict(
        name="fiche détail",
        icon="fas fa-info-circle",
        wrap="none",
        html=phone("""
<div class="dz-mb-detail-media"><img class="dz-cover" src="https://picsum.photos/seed/cabane-pins/600/700" alt="Cabane en bois dans une forêt de pins">
""" + STATUS_LIGHT + """
  <div class="dz-mb-media-bar"><a class="dz-mb-glass" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i></a><div class="dz-mb-media-right"><a class="dz-mb-glass" href="#" aria-label="Partager"><i class="fas fa-share-alt"></i></a><a class="dz-mb-glass dz-mb-fav" href="#" aria-label="Favori"><i class="fas fa-heart"></i></a></div></div>
  <span class="dz-mb-media-count">1 / 18</span>
</div>
<div class="dz-mb-body dz-mb-sheet-body">
  <div class="dz-mb-detail-head"><div><span class="dz-mb-kicker">Cabane · Landes</span><h2 class="dz-mb-title">Cabane des Grands Pins</h2></div><div class="dz-mb-rating"><i class="fas fa-star"></i><b>4,96</b><span>(214)</span></div></div>
  <div class="dz-mb-facts"><span><i class="fas fa-user-friends"></i> 4 voyageurs</span><span><i class="fas fa-bed"></i> 2 chambres</span><span><i class="fas fa-bath"></i> 1 bain</span></div>
  <div class="dz-mb-host"><span class="dz-avatar dz-avatar-sm">CM</span><div><b>Hôte : Chloé M.</b><span>Superhôte · répond en 1 h</span></div><a class="dz-mb-round" href="#" aria-label="Écrire à l'hôte"><i class="far fa-comment"></i></a></div>
  <p class="dz-mb-text">Perchée à 4 mètres dans les pins, à 800 m de l'océan. Bain nordique, poêle à bois et petit-déjeuner local livré chaque matin.</p>
  <div class="dz-mb-amen"><span><i class="fas fa-wifi"></i> Wi-Fi</span><span><i class="fas fa-hot-tub"></i> Bain nordique</span><span><i class="fas fa-fire"></i> Poêle</span><span><i class="fas fa-bicycle"></i> Vélos</span></div>
</div>
<div class="dz-mb-buybar"><div class="dz-mb-price"><b>189 €</b><span>/ nuit · 2 – 4 oct.</span></div><a class="dz-btn" href="#">Réserver</a></div>
""", "dz-mb-screen-media"),
    ),
    # ------------------------------------------------------------------ 4
    dict(
        name="paiement mobile",
        icon="fas fa-credit-card",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-navbar"><a class="dz-mb-round" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i></a><b>Paiement</b><span class="dz-mb-secure"><i class="fas fa-lock"></i></span></div>
<div class="dz-mb-body">
  <div class="dz-mb-card">
    <div class="dz-mb-card-top"><span class="dz-mb-card-chip"></span><i class="fas fa-wifi dz-mb-nfc"></i></div>
    <span class="dz-mb-card-num">•••• •••• •••• 4821</span>
    <div class="dz-mb-card-bottom"><div><span>Titulaire</span><b>LÉA SIMON</b></div><div><span>Expire</span><b>09/29</b></div><span class="dz-mb-card-brand"><i class="fas fa-circle"></i><i class="fas fa-circle"></i></span></div>
  </div>
  <span class="dz-mb-label">Moyen de paiement</span>
  <div class="dz-mb-methods">
    <div class="dz-mb-method dz-mb-on"><span class="dz-mb-m-ico"><i class="fas fa-credit-card"></i></span><div><b>Carte •••• 4821</b><span>Par défaut</span></div><span class="dz-mb-radio"></span></div>
    <div class="dz-mb-method"><span class="dz-mb-m-ico"><i class="fas fa-university"></i></span><div><b>Virement instantané</b><span>Depuis votre banque</span></div><span class="dz-mb-radio"></span></div>
    <div class="dz-mb-method"><span class="dz-mb-m-ico"><i class="fas fa-calendar-check"></i></span><div><b>En 3 fois sans frais</b><span>3 × 49,33 €</span></div><span class="dz-mb-radio"></span></div>
  </div>
  <div class="dz-mb-summary">
    <div class="dz-mb-sum-line"><span>Sous-total</span><b>139,00 €</b></div>
    <div class="dz-mb-sum-line"><span>Livraison express</span><b>9,00 €</b></div>
    <div class="dz-mb-sum-line dz-mb-sum-total"><span>Total</span><b>148,00 €</b></div>
  </div>
</div>
<div class="dz-mb-paybar"><a class="dz-btn dz-btn-block dz-btn-lg" href="#"><i class="fas fa-fingerprint"></i> Payer 148,00 €</a><span class="dz-mb-fine"><i class="fas fa-shield-alt"></i> Paiement chiffré · validation par empreinte</span></div>
"""),
    ),
    # ------------------------------------------------------------------ 5
    dict(
        name="profil utilisateur",
        icon="fas fa-user-circle",
        wrap="none",
        html=phone("""
<div class="dz-mb-cover">""" + STATUS_LIGHT + """<div class="dz-mb-media-bar"><a class="dz-mb-glass" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i></a><a class="dz-mb-glass" href="#" aria-label="Options"><i class="fas fa-ellipsis-h"></i></a></div></div>
<div class="dz-mb-body dz-mb-profile">
  <div class="dz-mb-pf-head"><span class="dz-avatar dz-mb-pf-av">AM</span><span class="dz-mb-pf-online"></span></div>
  <h2 class="dz-mb-title">Awa Martin <i class="fas fa-check-circle dz-mb-verified"></i></h2>
  <span class="dz-mb-sub">@awa.martin · Céramiste à Lyon</span>
  <p class="dz-mb-text dz-mb-center">Pièces uniques en grès, tournées à la main. Ateliers d'initiation le samedi.</p>
  <div class="dz-mb-stats"><div><b>142</b><span>Créations</span></div><div><b>12,4 k</b><span>Abonnés</span></div><div><b>318</b><span>Abonnements</span></div></div>
  <div class="dz-mb-pf-acts"><a class="dz-btn dz-btn-sm" href="#">Suivre</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Message</a><a class="dz-mb-round" href="#" aria-label="Plus"><i class="fas fa-user-plus"></i></a></div>
  <div class="dz-mb-tabline"><span class="dz-mb-on"><i class="fas fa-th"></i></span><span><i class="fas fa-shopping-bag"></i></span><span><i class="far fa-bookmark"></i></span></div>
  <div class="dz-mb-grid3">
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/bol-gres/300/300" alt="Bol en grès"></span>
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/vase-bleu/300/300" alt="Vase bleu"></span>
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/tour-potier/300/300" alt="Tour de potier"></span>
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/tasses-email/300/300" alt="Tasses émaillées"></span>
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/four-atelier/300/300" alt="Four de l'atelier"></span>
    <span class="dz-mb-gi"><img class="dz-cover" src="https://picsum.photos/seed/assiettes-sable/300/300" alt="Assiettes couleur sable"></span>
  </div>
</div>
""" + tabs(3), "dz-mb-screen-media"),
    ),
    # ------------------------------------------------------------------ 6
    dict(
        name="réglages de l'app",
        icon="fas fa-cog",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body dz-mb-grouped">
  <h2 class="dz-mb-large">Réglages</h2>
  <div class="dz-mb-searchbar dz-mb-searchbar-sm"><i class="fas fa-search"></i><span>Rechercher</span></div>
  <a class="dz-mb-account" href="#"><span class="dz-avatar">LS</span><div><b>Léa Simon</b><span>Compte, sécurité, abonnement Premium</span></div><i class="fas fa-chevron-right"></i></a>
  <div class="dz-mb-group">
    <div class="dz-mb-cell"><span class="dz-mb-ci dz-mb-ci-a"><i class="fas fa-plane"></i></span><span class="dz-mb-cell-l">Mode avion</span><span class="dz-mb-switch"></span></div>
    <div class="dz-mb-cell"><span class="dz-mb-ci dz-mb-ci-b"><i class="fas fa-bell"></i></span><span class="dz-mb-cell-l">Notifications</span><span class="dz-mb-cell-v">Résumé à 18 h</span><i class="fas fa-chevron-right"></i></div>
    <div class="dz-mb-cell"><span class="dz-mb-ci dz-mb-ci-c"><i class="fas fa-moon"></i></span><span class="dz-mb-cell-l">Concentration</span><span class="dz-mb-switch dz-mb-on"></span></div>
  </div>
  <div class="dz-mb-group">
    <div class="dz-mb-cell"><span class="dz-mb-ci dz-mb-ci-d"><i class="fas fa-palette"></i></span><span class="dz-mb-cell-l">Apparence</span><span class="dz-mb-cell-v">Auto</span><i class="fas fa-chevron-right"></i></div>
    <div class="dz-mb-cell"><span class="dz-mb-ci dz-mb-ci-e"><i class="fas fa-lock"></i></span><span class="dz-mb-cell-l">Confidentialité</span><i class="fas fa-chevron-right"></i></div>
    <div class="dz-mb-cell dz-mb-cell-col"><div class="dz-mb-cell-top"><span class="dz-mb-ci dz-mb-ci-f"><i class="fas fa-database"></i></span><span class="dz-mb-cell-l">Stockage</span><span class="dz-mb-cell-v">41,2 / 64 Go</span></div><div class="dz-mb-storage"><span style="--v:34%" class="dz-mb-st-a"></span><span style="--v:18%" class="dz-mb-st-b"></span><span style="--v:12%" class="dz-mb-st-c"></span></div></div>
  </div>
  <span class="dz-mb-group-foot">Le mode Concentration masque les notifications non urgentes de 21 h à 7 h.</span>
  <div class="dz-mb-group"><a class="dz-mb-cell dz-mb-danger" href="#">Se déconnecter</a></div>
  <span class="dz-mb-version">Version 4.2.0 (1180)</span>
</div>
""" + tabs(3)),
    ),
    # ------------------------------------------------------------------ 7
    dict(
        name="onboarding en cartes",
        icon="fas fa-layer-group",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body dz-mb-onb">
  <div class="dz-mb-onb-top"><span class="dz-mb-logo"><span class="dz-brand-mark"></span> Pécule</span><a class="dz-mb-link" href="#">Passer</a></div>
  <div class="dz-mb-onb-art">
    <div class="dz-mb-ocard dz-mb-ocard-3"><i class="fas fa-plane"></i><b>Voyage à Lisbonne</b><span>620 € / 900 €</span></div>
    <div class="dz-mb-ocard dz-mb-ocard-2"><i class="fas fa-laptop"></i><b>Nouvel ordinateur</b><span>1 140 € / 1 400 €</span></div>
    <div class="dz-mb-ocard dz-mb-ocard-1"><div class="dz-mb-oc-head"><span class="dz-mb-oc-ico"><i class="fas fa-umbrella-beach"></i></span><span class="dz-mb-oc-pct">68 %</span></div><b>Vacances d'été</b><span>2 040 € sur 3 000 €</span><div class="dz-mb-oc-bar"><span></span></div><span class="dz-mb-oc-foot">+ 120 € arrondis ce mois-ci</span></div>
    <span class="dz-mb-spark dz-mb-spark-a"><i class="fas fa-star"></i></span><span class="dz-mb-spark dz-mb-spark-b"><i class="fas fa-coins"></i></span>
  </div>
  <div class="dz-mb-onb-text"><h2 class="dz-mb-onb-title">Épargnez <em>sans y penser</em></h2><p class="dz-mb-text dz-mb-center">Chaque achat est arrondi à l'euro supérieur. La différence part vers vos projets, automatiquement.</p></div>
  <div class="dz-mb-dots"><span></span><span class="dz-mb-on"></span><span></span></div>
  <a class="dz-btn dz-btn-block dz-btn-lg" href="#">Continuer</a>
  <span class="dz-mb-fine dz-mb-center">Déjà inscrit ? <a href="#">Se connecter</a></span>
</div>
"""),
    ),
    # ------------------------------------------------------------------ 8
    dict(
        name="messagerie",
        icon="fas fa-comment-dots",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-chat-head"><a class="dz-mb-link" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i> 12</a><div class="dz-mb-chat-who"><span class="dz-avatar dz-avatar-sm">IC</span><div><b>Inès Carpentier</b><span class="dz-mb-online-t">En ligne</span></div></div><div class="dz-mb-chat-acts"><i class="fas fa-phone"></i><i class="fas fa-video"></i></div></div>
<div class="dz-mb-body dz-mb-thread">
  <span class="dz-mb-daysep">Aujourd'hui 09:12</span>
  <div class="dz-mb-msg dz-mb-them"><p>Tu as pu voir les photos de l'atelier ?</p></div>
  <div class="dz-mb-msg dz-mb-them dz-mb-msg-img"><span class="dz-mb-msg-pic"><img class="dz-cover" src="https://picsum.photos/seed/atelier-lumiere/400/300" alt="Atelier baigné de lumière"></span><p>La lumière le matin est incroyable</p><span class="dz-mb-react"><i class="fas fa-heart"></i> 2</span></div>
  <div class="dz-mb-msg dz-mb-me"><p>Magnifique ! On garde celle-ci pour la page d'accueil</p><span class="dz-mb-meta">09:15 <i class="fas fa-check-double"></i></span></div>
  <div class="dz-mb-msg dz-mb-me dz-mb-voice"><span class="dz-mb-play"><i class="fas fa-play"></i></span><span class="dz-mb-wave"><i style="--h:30%"></i><i style="--h:60%"></i><i style="--h:90%"></i><i style="--h:50%"></i><i style="--h:70%"></i><i style="--h:40%"></i><i style="--h:85%"></i><i style="--h:55%"></i><i style="--h:35%"></i><i style="--h:65%"></i><i style="--h:45%"></i><i style="--h:25%"></i><i style="--h:60%"></i><i style="--h:30%"></i></span><span class="dz-mb-dur">0:14</span></div>
  <div class="dz-mb-msg dz-mb-them"><p>Parfait. Je t'envoie le devis final avant midi.</p></div>
  <div class="dz-mb-typing"><span></span><span></span><span></span></div>
</div>
<div class="dz-mb-composer"><span class="dz-mb-round" aria-label="Ajouter"><i class="fas fa-plus"></i></span><div class="dz-mb-input"><span>Message</span><i class="far fa-smile"></i></div><span class="dz-mb-send" aria-label="Message vocal"><i class="fas fa-microphone"></i></span></div>
"""),
    ),
    # ------------------------------------------------------------------ 9
    dict(
        name="carte + fiche du bas",
        icon="fas fa-map",
        wrap="none",
        html=phone("""
<div class="dz-mb-map">
  <span class="dz-mb-map-water"></span><span class="dz-mb-map-park"></span><span class="dz-mb-map-road dz-mb-road-a"></span><span class="dz-mb-map-road dz-mb-road-b"></span><span class="dz-mb-map-road dz-mb-road-c"></span>
  <span class="dz-mb-pin dz-mb-pin-a">12 €</span><span class="dz-mb-pin dz-mb-pin-b dz-mb-on">18 €</span><span class="dz-mb-pin dz-mb-pin-c">9 €</span><span class="dz-mb-pin dz-mb-pin-d">24 €</span>
  <span class="dz-mb-me-dot"></span>
</div>
""" + STATUS + """
<div class="dz-mb-map-top"><div class="dz-mb-searchbar dz-mb-float"><i class="fas fa-search"></i><span>Restaurants autour de moi</span><span class="dz-avatar dz-avatar-sm">LS</span></div><div class="dz-mb-chips"><span class="dz-mb-chip dz-mb-on"><i class="fas fa-utensils"></i> Restaurants</span><span class="dz-mb-chip"><i class="fas fa-coffee"></i> Cafés</span><span class="dz-mb-chip"><i class="fas fa-leaf"></i> Végé</span></div></div>
<a class="dz-mb-locate" href="#" aria-label="Me localiser"><i class="fas fa-location-arrow"></i></a>
<div class="dz-mb-bsheet">
  <span class="dz-mb-handle"></span>
  <div class="dz-mb-bs-head"><b>24 adresses</b><span class="dz-mb-sub">à moins de 10 min à pied</span></div>
  <a class="dz-mb-place dz-mb-on" href="#"><span class="dz-mb-place-img"><img class="dz-cover" src="https://picsum.photos/seed/bistrot-lyon/200/200" alt="Salle du bistrot"></span><div class="dz-mb-place-text"><b>Le Petit Comptoir</b><span><i class="fas fa-star"></i> 4,8 · Bistrot · 18 € · 350 m</span><span class="dz-mb-open">Ouvert · ferme à 23 h</span></div><i class="far fa-heart"></i></a>
  <a class="dz-mb-place" href="#"><span class="dz-mb-place-img"><img class="dz-cover" src="https://picsum.photos/seed/cantine-verte/200/200" alt="Cantine végétarienne"></span><div class="dz-mb-place-text"><b>Cantine Germe</b><span><i class="fas fa-star"></i> 4,6 · Végétarien · 12 € · 500 m</span><span class="dz-mb-open">Ouvert · ferme à 15 h</span></div><i class="far fa-heart"></i></a>
</div>
""", "dz-mb-screen-map"),
    ),
    # ------------------------------------------------------------------ 10
    dict(
        name="lecteur audio",
        icon="fas fa-headphones",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body dz-mb-player">
  <div class="dz-mb-pl-top"><a class="dz-mb-round" href="#" aria-label="Réduire"><i class="fas fa-chevron-down"></i></a><div class="dz-mb-pl-src"><span>Lecture depuis</span><b>Podcast · Les Bâtisseurs</b></div><a class="dz-mb-round" href="#" aria-label="Options"><i class="fas fa-ellipsis-h"></i></a></div>
  <div class="dz-mb-art"><img class="dz-cover" src="https://picsum.photos/seed/podcast-bois/600/600" alt="Pochette de l'épisode"></div>
  <div class="dz-mb-track"><div><b>Ép. 42 — Bâtir sans lever de fonds</b><span>Les Bâtisseurs · Inès Carpentier</span></div><i class="fas fa-heart dz-mb-liked"></i></div>
  <div class="dz-mb-scrub"><div class="dz-mb-scrub-bar" style="--v:38%"><span></span><i></i></div><div class="dz-mb-scrub-t"><span>18:24</span><span>−29:51</span></div></div>
  <div class="dz-mb-controls"><span class="dz-mb-ctl-sm">1,25×</span><span class="dz-mb-ctl" aria-label="Reculer de 15 s"><i class="fas fa-undo"></i></span><span class="dz-mb-ctl-main" aria-label="Pause"><i class="fas fa-pause"></i></span><span class="dz-mb-ctl" aria-label="Avancer de 30 s"><i class="fas fa-redo"></i></span><span class="dz-mb-ctl-sm"><i class="fas fa-moon"></i></span></div>
  <div class="dz-mb-pl-foot"><span><i class="fas fa-broadcast-tower"></i> Enceinte du salon</span><span><i class="fas fa-list-ul"></i> File (6)</span></div>
</div>
""", "dz-mb-screen-player"),
    ),
    # ------------------------------------------------------------------ 11
    dict(
        name="recherche",
        icon="fas fa-search",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body">
  <div class="dz-mb-search-row"><div class="dz-mb-searchbar dz-mb-focus"><i class="fas fa-search"></i><span class="dz-mb-q">céramique<span class="dz-mb-caret"></span></span><i class="fas fa-times-circle"></i></div><a class="dz-mb-link" href="#">Annuler</a></div>
  <div class="dz-mb-suggest">
    <div class="dz-mb-sug"><i class="fas fa-search"></i><span><b>céramique</b> atelier Lyon</span><i class="fas fa-arrow-up dz-mb-fill"></i></div>
    <div class="dz-mb-sug"><i class="fas fa-search"></i><span><b>céramique</b> débutant week-end</span><i class="fas fa-arrow-up dz-mb-fill"></i></div>
    <div class="dz-mb-sug"><span class="dz-avatar dz-avatar-sm">AM</span><span>Awa Martin · <em>céramiste</em></span><i class="fas fa-arrow-up dz-mb-fill"></i></div>
  </div>
  <div class="dz-mb-sec-head"><b>Recherches récentes</b><a href="#">Effacer</a></div>
  <div class="dz-mb-recent"><span class="dz-mb-chip"><i class="fas fa-history"></i> tournage</span><span class="dz-mb-chip"><i class="fas fa-history"></i> émaillage</span><span class="dz-mb-chip"><i class="fas fa-history"></i> cours enfants</span></div>
  <div class="dz-mb-sec-head"><b>Parcourir</b></div>
  <div class="dz-mb-cats">
    <a class="dz-mb-cat dz-mb-cat-a" href="#"><b>Ateliers</b><i class="fas fa-hands"></i></a>
    <a class="dz-mb-cat dz-mb-cat-b" href="#"><b>Objets</b><i class="fas fa-wine-glass-alt"></i></a>
    <a class="dz-mb-cat dz-mb-cat-c" href="#"><b>Créateurs</b><i class="fas fa-user-astronaut"></i></a>
    <a class="dz-mb-cat dz-mb-cat-d" href="#"><b>Événements</b><i class="fas fa-ticket-alt"></i></a>
  </div>
  <div class="dz-mb-sec-head"><b>Tendances</b></div>
  <div class="dz-mb-trends"><div class="dz-mb-trend"><b>1</b><span>Marché des potiers</span><i class="fas fa-arrow-up"></i></div><div class="dz-mb-trend"><b>2</b><span>Raku en plein air</span><i class="fas fa-arrow-up"></i></div></div>
</div>
""" + tabs(1)),
    ),
    # ------------------------------------------------------------------ 12
    dict(
        name="panier",
        icon="fas fa-shopping-basket",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-navbar"><a class="dz-mb-round" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i></a><b>Panier (3)</b><a class="dz-mb-link" href="#">Vider</a></div>
<div class="dz-mb-body">
  <div class="dz-mb-ship"><div class="dz-mb-ship-t"><i class="fas fa-truck"></i><span>Plus que <b>11,00 €</b> pour la livraison offerte</span></div><div class="dz-mb-ship-bar"><span style="--v:82%"></span></div></div>
  <div class="dz-mb-items">
    <div class="dz-mb-item"><span class="dz-mb-item-img"><img class="dz-cover" src="https://picsum.photos/seed/bougie-figuier/200/200" alt="Bougie Figuier"></span><div class="dz-mb-item-info"><b>Bougie Figuier</b><span>220 g · cire de colza</span><b class="dz-mb-item-price">24,00 €</b></div><div class="dz-mb-stepper"><span aria-label="Retirer">−</span><b>2</b><span aria-label="Ajouter">+</span></div></div>
    <div class="dz-mb-item"><span class="dz-mb-item-img"><img class="dz-cover" src="https://picsum.photos/seed/tasse-gres/200/200" alt="Tasse en grès"></span><div class="dz-mb-item-info"><b>Tasse grès sable</b><span>Lot de 2</span><b class="dz-mb-item-price">32,00 €</b></div><div class="dz-mb-stepper"><span aria-label="Retirer">−</span><b>1</b><span aria-label="Ajouter">+</span></div></div>
    <div class="dz-mb-item"><span class="dz-mb-item-img"><img class="dz-cover" src="https://picsum.photos/seed/plaid-lin/200/200" alt="Plaid en lin"></span><div class="dz-mb-item-info"><b>Plaid lin lavé</b><span>Terracotta · 130 × 170</span><b class="dz-mb-item-price">89,00 €</b><span class="dz-mb-stock">Plus que 2 en stock</span></div><div class="dz-mb-stepper"><span aria-label="Retirer">−</span><b>1</b><span aria-label="Ajouter">+</span></div></div>
  </div>
  <div class="dz-mb-promo"><i class="fas fa-tag"></i><span>AUTOMNE10</span><b>− 16,90 €</b></div>
  <div class="dz-mb-summary">
    <div class="dz-mb-sum-line"><span>Sous-total</span><b>169,00 €</b></div>
    <div class="dz-mb-sum-line"><span>Remise</span><b class="dz-mb-green">− 16,90 €</b></div>
    <div class="dz-mb-sum-line"><span>Livraison</span><b>4,90 €</b></div>
  </div>
</div>
<div class="dz-mb-paybar dz-mb-paybar-row"><div class="dz-mb-price"><span>Total TTC</span><b>157,00 €</b></div><a class="dz-btn dz-btn-lg" href="#">Commander <i class="fas fa-arrow-right"></i></a></div>
"""),
    ),
    # ------------------------------------------------------------------ 13
    dict(
        name="portefeuille",
        icon="fas fa-wallet",
        wrap="none",
        html=phone(STATUS + """
<div class="dz-mb-body">
  <div class="dz-mb-hello"><span class="dz-avatar dz-mb-av">LS</span><div class="dz-mb-hello-text"><span>Solde total</span><b class="dz-mb-balance">4 382,60 €</b></div><a class="dz-mb-round" href="#" aria-label="Masquer le solde"><i class="far fa-eye"></i></a></div>
  <span class="dz-mb-delta"><i class="fas fa-arrow-up"></i> + 312,40 € ce mois-ci</span>
  <div class="dz-mb-quick">
    <a class="dz-mb-q-act" href="#"><span><i class="fas fa-paper-plane"></i></span>Envoyer</a>
    <a class="dz-mb-q-act" href="#"><span><i class="fas fa-download"></i></span>Recevoir</a>
    <a class="dz-mb-q-act" href="#"><span><i class="fas fa-plus"></i></span>Recharger</a>
    <a class="dz-mb-q-act" href="#"><span><i class="fas fa-th-large"></i></span>Plus</a>
  </div>
  <div class="dz-mb-wcards">
    <div class="dz-mb-wcard dz-mb-wcard-a"><div class="dz-mb-wc-top"><b>Compte courant</b><i class="fas fa-wifi"></i></div><b class="dz-mb-wc-amt">3 120,45 €</b><span>•••• 4821</span></div>
    <div class="dz-mb-wcard dz-mb-wcard-b"><div class="dz-mb-wc-top"><b>Épargne</b><i class="fas fa-piggy-bank"></i></div><b class="dz-mb-wc-amt">1 262,15 €</b><span>3,1 % / an</span></div>
  </div>
  <div class="dz-mb-sec-head"><b>Transactions</b><a href="#">Tout voir</a></div>
  <div class="dz-mb-tx-list">
    <div class="dz-mb-tx"><span class="dz-mb-tx-ico dz-mb-tx-a"><i class="fas fa-shopping-basket"></i></span><div><b>Marché Croix-Rousse</b><span>Aujourd'hui · Courses</span></div><b class="dz-mb-neg">− 34,80 €</b></div>
    <div class="dz-mb-tx"><span class="dz-mb-tx-ico dz-mb-tx-b"><i class="fas fa-briefcase"></i></span><div><b>Atelier Lune</b><span>Hier · Virement reçu</span></div><b class="dz-mb-pos">+ 1 280,00 €</b></div>
    <div class="dz-mb-tx"><span class="dz-mb-tx-ico dz-mb-tx-c"><i class="fas fa-train"></i></span><div><b>Billet Lyon → Nantes</b><span>22 sept. · Transport</span></div><b class="dz-mb-neg">− 58,00 €</b></div>
  </div>
</div>
""" + tabs(0, [("fas fa-home", "Accueil"), ("fas fa-chart-pie", "Budget"), ("fas fa-credit-card", "Cartes"), ("fas fa-user", "Profil")])),
    ),
]
