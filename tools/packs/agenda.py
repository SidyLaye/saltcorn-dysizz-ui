"""Famille « Agenda » : le temps. Calendriers, semaine, jour, prise de
rendez-vous, programmes, frises, comptes à rebours, fuseaux horaires…
Préfixe CSS : dz-ag-. Les événements se placent dans la grille par
style="grid-column / grid-row" (modifiable dans le builder).
Aujourd'hui, dans les contenus : jeudi 24 septembre 2026, 14:32."""

FAMILY = "agenda"
BLOCKS = []


def badge_html(t):
    return f'<span class="dz-badge">{t}</span>' if t else ""


CHECK = '<i class="fas fa-check"></i>'
FLAG = '<i class="fas fa-flag dz-ag-flag"></i>'


def av(ini, k=""):
    return f'<span class="dz-avatar dz-avatar-sm{(" dz-ag-av" + k) if k else ""}">{ini}</span>'


# 1. calendrier du mois -----------------------------------------------------
_ev = {
    1: [("09:00", "Point d'équipe", 2)], 2: [("14:00", "Démo Nexora", 1)], 3: [("10:30", "Dentiste", 5)],
    7: [("09:00", "Point d'équipe", 2), ("16:00", "Revue budget T4", 4)], 9: [("12:30", "Déjeuner Atelier Lune", 3)],
    10: [("", "Livraison v4.2", 1)], 14: [("09:00", "Point d'équipe", 2)],
    15: [("", "Salon Tech Lyon", 3)], 16: [("", "Salon Tech Lyon", 3)], 17: [("", "Salon Tech Lyon", 3), ("18:00", "Dîner partenaires", 4)],
    21: [("09:00", "Point d'équipe", 2), ("11:00", "Entretien : dév. front", 1), ("15:00", "Formation RGPD", 4)],
    22: [("10:00", "Atelier design", 1)], 24: [("09:30", "Comité produit", 1), ("14:00", "Appel Orbis Conseil", 2), ("16:30", "Bilan sprint 38", 4), ("18:00", "Afterwork", 3)],
    25: [("11:00", "Signature Vauclair", 5)], 28: [("09:00", "Point d'équipe", 2)], 30: [("", "Clôture du trimestre", 4)],
}
_cells = []
_days = [(31, "out")] + [(d, "") for d in range(1, 31)] + [(d, "out") for d in range(1, 5)]
for i, (d, st) in enumerate(_days):
    cls = "dz-ag-day"
    if st:
        cls += " dz-ag-out"
    if i % 7 >= 5:
        cls += " dz-ag-we"
    if not st and d == 24:
        cls += " dz-ag-today"
    evs = _ev.get(d, []) if not st else ([("10:00", "Séminaire annuel", 3)] if d == 1 else [])
    body = ""
    for j, (t, title, k) in enumerate(evs[:3]):
        span = " dz-ag-allday" if not t else ""
        tt = f"<b>{t}</b> " if t else ""
        body += f'<div class="dz-ag-ev dz-ag-k{k}{span}">{tt}{title}</div>'
    if len(evs) > 3:
        body += f'<span class="dz-ag-more">+{len(evs) - 3} autre</span>'
    num = f'<span class="dz-ag-dnum">{d}</span>' if not (st and d == 1) else '<span class="dz-ag-dnum">1 oct.</span>'
    _cells.append(f'<div class="{cls}">{num}{body}</div>')
BLOCKS.append(dict(name="calendrier du mois", icon="far fa-calendar-alt", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l">
      <h3 class="dz-ag-title">Septembre 2026</h3>
      <div class="dz-ag-nav"><a href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a><a class="dz-ag-todaybtn" href="#">Aujourd'hui</a><a href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a></div>
    </div>
    <div class="dz-ag-bar-r">
      <div class="dz-ag-seg"><a href="#">Jour</a><a href="#">Semaine</a><a class="dz-active" href="#">Mois</a></div>
      <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Événement</a>
    </div>
  </div>
  <div class="dz-ag-month">
    <div class="dz-ag-wd"><span>Lun</span><span>Mar</span><span>Mer</span><span>Jeu</span><span>Ven</span><span>Sam</span><span>Dim</span></div>
    <div class="dz-ag-mgrid">{''.join(_cells)}</div>
  </div>
  <div class="dz-ag-legend"><span class="dz-ag-key dz-ag-k1">Produit</span><span class="dz-ag-key dz-ag-k2">Clients</span><span class="dz-ag-key dz-ag-k3">Événements</span><span class="dz-ag-key dz-ag-k4">Interne</span><span class="dz-ag-key dz-ag-k5">Personnel</span></div>
</div>
"""))

# 2. semaine avec créneaux ---------------------------------------------------
_wd = [("Lun", "21"), ("Mar", "22"), ("Mer", "23"), ("Jeu", "24"), ("Ven", "25"), ("Sam", "26"), ("Dim", "27")]


def slot(h, m=0):
    """ligne de grille d'une heure (8 h = 3) ; demi-heures"""
    return 3 + int((h - 8) * 2 + m / 30)


_wevs = [(1, 9, 0, 9, 30, "Point d'équipe", "Visio", 2), (1, 11, 0, 12, 0, "Entretien : dév. front", "Salle Atelier", 1),
         (1, 15, 0, 17, 0, "Formation RGPD", "Amphi · 2e étage", 4), (2, 10, 0, 12, 30, "Atelier design", "Salle Horizon", 1),
         (2, 14, 0, 15, 0, "Appel fournisseur", "Téléphone", 2), (3, 9, 30, 10, 30, "Revue des devis", "Bureau", 4),
         (3, 13, 0, 14, 0, "Déjeuner Nexora", "Le Comptoir", 3), (3, 16, 0, 18, 0, "Préparation du salon", "Salle Atelier", 3),
         (4, 9, 30, 11, 0, "Comité produit", "Salle Horizon", 1), (4, 14, 0, 15, 0, "Appel Orbis Conseil", "Visio", 2),
         (4, 16, 30, 17, 30, "Bilan sprint 38", "Salle Atelier", 4), (5, 11, 0, 12, 0, "Signature Vauclair", "Chez le client", 5),
         (5, 14, 30, 16, 30, "Rédaction appel d'offres", "Focus", 4), (6, 10, 0, 12, 0, "Marché + courses", "", 5)]
_w = []
for d, h1, m1, h2, m2, t, p, k in _wevs:
    short = " dz-ag-short" if (h2 * 60 + m2) - (h1 * 60 + m1) <= 30 else ""
    _w.append(f'<div class="dz-ag-wev dz-ag-k{k}{short}" style="grid-column:{d + 1};grid-row:{slot(h1, m1)} / {slot(h2, m2)}">'
              f'<b>{t}</b><span>{h1:02d}:{m1:02d} – {h2:02d}:{m2:02d}{(" · " + p) if p else ""}</span></div>')
_hours = "".join(f'<span class="dz-ag-hr" style="grid-row:{slot(h)}">{h:02d}:00</span>' for h in range(9, 19))
_heads = "".join(f'<div class="dz-ag-wh{" dz-ag-today" if n == "24" else ""}" style="grid-column:{i + 2}"><span>{d}</span><b>{n}</b></div>' for i, (d, n) in enumerate(_wd))
BLOCKS.append(dict(name="semaine", icon="fas fa-calendar-week", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l">
      <h3 class="dz-ag-title">21 – 27 septembre 2026</h3>
      <span class="dz-badge dz-badge-neutral">Semaine 39</span>
    </div>
    <div class="dz-ag-bar-r">
      <div class="dz-ag-nav"><a href="#" aria-label="Semaine précédente"><i class="fas fa-chevron-left"></i></a><a class="dz-ag-todaybtn" href="#">Aujourd'hui</a><a href="#" aria-label="Semaine suivante"><i class="fas fa-chevron-right"></i></a></div>
      <div class="dz-ag-seg"><a href="#">Jour</a><a class="dz-active" href="#">Semaine</a><a href="#">Mois</a></div>
    </div>
  </div>
  <div class="dz-ag-scroll">
    <div class="dz-ag-week">
      {_heads}
      <span class="dz-ag-alllab">Journée</span>
      <div class="dz-ag-allrow" style="grid-column:2 / 9"></div>
      <div class="dz-ag-alldev dz-ag-k3" style="grid-column:4 / 6">Préparation Salon Tech · Lyon</div>
      <div class="dz-ag-alldev dz-ag-k5" style="grid-column:7 / 9">Week-end en Bretagne</div>
      <div class="dz-ag-wbg"></div>
      <div class="dz-ag-wkend"></div>
      {_hours}
      {''.join(_w)}
      <div class="dz-ag-nowline" style="grid-column:5;grid-row:16"><span>14:32</span></div>
    </div>
  </div>
</div>
"""))

# 3. vue jour -------------------------------------------------------------
_dev = [(9, 30, 11, 0, "Comité produit", "Salle Horizon · 8 participants", 1, "2 / 4"), (11, 30, 12, 0, "Relire la proposition Vauclair", "Tâche", 4, "2 / 4"),
        (12, 30, 13, 30, "Déjeuner avec Inès", "Café des Arts", 3, "2 / 4"), (14, 0, 15, 0, "Appel Orbis Conseil", "Visio · lien dans l'invitation", 2, "2 / 3"),
        (14, 0, 14, 30, "Entretien annuel · Tom", "Bureau 3", 5, "3 / 4"), (16, 30, 17, 30, "Bilan sprint 38", "Salle Atelier", 4, "2 / 4"),
        (18, 0, 19, 0, "Afterwork équipe", "Terrasse du 5e", 3, "2 / 4")]
_dd = "".join(f'<div class="dz-ag-wev dz-ag-k{k}{" dz-ag-short" if (h2 * 60 + m2) - (h1 * 60 + m1) <= 30 else ""}{" dz-ag-past" if h2 < 14 else ""}" style="grid-column:{col};grid-row:{slot(h1, m1)} / {slot(h2, m2)}">'
              f'<b>{t}</b><span>{h1:02d}:{m1:02d} – {h2:02d}:{m2:02d} · {p}</span></div>' for h1, m1, h2, m2, t, p, k, col in _dev)
_mini = ""
for i, d in enumerate([31] + list(range(1, 31)) + [1, 2, 3, 4]):
    out = i == 0 or i > 30
    c = "dz-ag-mc" + (" dz-ag-out" if out else "") + (" dz-ag-today" if d == 24 and not out else "") + (" dz-ag-has" if not out and d in _ev else "")
    _mini += f'<span class="{c}">{d}</span>'
BLOCKS.append(dict(name="journée", icon="far fa-calendar", html=f"""
<div class="dz-ag dz-ag-panel dz-ag-dayview">
  <div class="dz-ag-dmain">
    <div class="dz-ag-bar">
      <div class="dz-ag-bar-l">
        <div class="dz-ag-bigdate"><b>24</b><div><span>Jeudi</span><span>Septembre 2026</span></div></div>
      </div>
      <div class="dz-ag-bar-r">
        <div class="dz-ag-nav"><a href="#" aria-label="Jour précédent"><i class="fas fa-chevron-left"></i></a><a class="dz-ag-todaybtn" href="#">Aujourd'hui</a><a href="#" aria-label="Jour suivant"><i class="fas fa-chevron-right"></i></a></div>
      </div>
    </div>
    <div class="dz-ag-week dz-ag-day1">
      <div class="dz-ag-wbg"></div>
      {''.join(f'<span class="dz-ag-hr" style="grid-row:{slot(h)}">{h:02d}:00</span>' for h in range(8, 19))}
      {_dd}
      <div class="dz-ag-nowline" style="grid-column:2 / 4;grid-row:16"><span>14:32</span></div>
    </div>
  </div>
  <aside class="dz-ag-dside">
    <div class="dz-ag-minical">
      <div class="dz-ag-mhead"><b>Septembre 2026</b><div class="dz-ag-nav dz-ag-nav-sm"><a href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a><a href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a></div></div>
      <div class="dz-ag-mcgrid"><span class="dz-ag-mwd">L</span><span class="dz-ag-mwd">M</span><span class="dz-ag-mwd">M</span><span class="dz-ag-mwd">J</span><span class="dz-ag-mwd">V</span><span class="dz-ag-mwd">S</span><span class="dz-ag-mwd">D</span>{_mini}</div>
    </div>
    <div class="dz-ag-nextcard dz-ag-k2">
      <span class="dz-ag-eyebrow">En cours · encore 28 min</span>
      <b>Appel Orbis Conseil</b>
      <span class="dz-ag-meta"><i class="far fa-clock"></i> 14:00 – 15:00</span>
      <span class="dz-ag-meta"><i class="fas fa-video"></i> Visio · salle virtuelle « Orbis-T3 »</span>
      <div class="dz-ag-people"><div class="dz-avatars">{av("CM")}{av("PL")}{av("AR")}</div><span>Claire M., Paul L. et vous</span></div>
      <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-video"></i> Rejoindre l'appel</a>
    </div>
    <div class="dz-ag-dstats"><div><b>6</b><span>rendez-vous</span></div><div><b>5 h 30</b><span>en réunion</span></div><div><b>1 h</b><span>libre</span></div></div>
  </aside>
</div>
"""))

# 4. agenda en liste ------------------------------------------------------------
_list = [
    ("24", "Jeudi", "Aujourd'hui", [("09:30", "11:00", "Comité produit", "Salle Horizon", "fas fa-map-marker-alt", 1, ["NB", "LF", "SA"], "+5", "past"),
                                     ("14:00", "15:00", "Appel Orbis Conseil", "Visio", "fas fa-video", 2, ["CM", "PL"], "", "now"),
                                     ("16:30", "17:30", "Bilan sprint 38", "Salle Atelier", "fas fa-map-marker-alt", 4, ["TG", "KB", "IM"], "+3", "")]),
    ("25", "Vendredi", "Demain", [("11:00", "12:00", "Signature du contrat Vauclair", "12 rue des Tanneurs, Nantes", "fas fa-map-marker-alt", 5, ["JV"], "", ""),
                                  ("14:30", "16:30", "Rédaction de l'appel d'offres", "Bloc de concentration", "fas fa-headphones", 4, [], "", "")]),
    ("29", "Mardi", "Dans 5 jours", [("08:45", "18:00", "Salon Nouvelles Formes · jour 1", "Parc des expositions, Lyon", "fas fa-map-marker-alt", 3, ["NB", "SA"], "+12", "")]),
]
_lg = []
for num, wd, rel, items in _list:
    rows = ""
    for a, b, t, p, ic, k, people, more, st in items:
        stc = {"past": " dz-ag-past", "now": " dz-ag-live"}.get(st, "")
        badge = '<span class="dz-badge dz-badge-success"><span class="dz-dot"></span>En cours</span>' if st == "now" else ""
        ppl = ""
        if people:
            ppl = '<div class="dz-avatars">' + "".join(av(x) for x in people) + (f'<span class="dz-ag-plus">{more}</span>' if more else "") + '</div>'
        rows += (f'<div class="dz-ag-litem dz-ag-k{k}{stc}"><div class="dz-ag-ltime"><b>{a}</b><span>{b}</span></div><i class="dz-ag-lbar"></i>'
                 f'<div class="dz-ag-linfo"><b>{t}</b><span class="dz-ag-meta"><i class="{ic}"></i> {p}</span></div>{badge}{ppl}</div>')
    _lg.append(f'<div class="dz-ag-lday{" dz-ag-today" if num == "24" else ""}"><div class="dz-ag-lhead"><b>{num}</b><div><span>{wd}</span><span>{rel}</span></div></div><div class="dz-ag-litems">{rows}</div></div>')
BLOCKS.append(dict(name="agenda en liste", icon="fas fa-list-ul", wrap="narrow", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><h3 class="dz-ag-title">Prochains rendez-vous</h3><span class="dz-badge dz-badge-neutral">7</span></div>
    <div class="dz-ag-bar-r"><div class="dz-ag-seg"><a class="dz-active" href="#">Tous</a><a href="#">Réunions</a><a href="#">Déplacements</a></div></div>
  </div>
  <div class="dz-ag-list">{''.join(_lg)}</div>
</div>
"""))

# 5. prise de rendez-vous ---------------------------------------------------------
_bk = ""
_avail = {1, 2, 3, 6, 7, 8, 9, 13, 14, 15, 16, 20, 21, 22, 23, 27, 28, 29, 30}
for i in range(3):  # jeudi 1er octobre → décalage de 3
    _bk += '<span class="dz-ag-bd dz-ag-blank"></span>'
for d in range(1, 32):
    c = "dz-ag-bd"
    if d == 8:
        c += " dz-ag-sel"
    elif d in _avail:
        c += " dz-ag-free"
    _bk += f'<span class="{c}">{d}</span>'
_slots = ["09:00", "09:30", "10:30", "11:00", "14:00", "15:30", "16:00", "17:30"]
_sl = "".join((f'<div class="dz-ag-slotsel"><span>{s}</span><a class="dz-btn dz-btn-sm" href="#">Suivant</a></div>' if s == "10:30"
               else f'<a class="dz-ag-slot" href="#">{s}</a>') for s in _slots)
BLOCKS.append(dict(name="prise de rendez-vous", icon="fas fa-calendar-check", html=f"""
<div class="dz-ag dz-ag-booking">
  <div class="dz-ag-bhost">
    <span class="dz-avatar dz-avatar-lg">CR</span>
    <span class="dz-ag-eyebrow">Camille Roussel · Studio Ardoise</span>
    <h3 class="dz-ag-btitle">Premier échange : votre projet de site</h3>
    <div class="dz-ag-bmeta">
      <span class="dz-ag-meta"><i class="far fa-clock"></i> 30 minutes</span>
      <span class="dz-ag-meta"><i class="fas fa-video"></i> Visio, lien envoyé à la confirmation</span>
      <span class="dz-ag-meta"><i class="fas fa-euro-sign"></i> Gratuit, sans engagement</span>
    </div>
    <p class="dz-ag-bdesc">On fait le point sur vos objectifs, vos délais et votre budget. Vous repartez avec une première estimation.</p>
    <div class="dz-ag-bsum"><i class="far fa-calendar-check"></i><div><b>Jeudi 8 octobre 2026</b><span>10:30 – 11:00 · heure de Paris</span></div></div>
  </div>
  <div class="dz-ag-bcal">
    <div class="dz-ag-mhead"><b>Choisir une date</b><div class="dz-ag-nav dz-ag-nav-sm"><a href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a><span>Octobre 2026</span><a href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a></div></div>
    <div class="dz-ag-bgrid"><span class="dz-ag-mwd">Lun</span><span class="dz-ag-mwd">Mar</span><span class="dz-ag-mwd">Mer</span><span class="dz-ag-mwd">Jeu</span><span class="dz-ag-mwd">Ven</span><span class="dz-ag-mwd">Sam</span><span class="dz-ag-mwd">Dim</span>{_bk}</div>
    <div class="dz-ag-tz"><i class="fas fa-globe-europe"></i><span>Europe/Paris (UTC+2) · 14:32</span><i class="fas fa-chevron-down"></i></div>
  </div>
  <div class="dz-ag-bslots">
    <div class="dz-ag-mhead"><b>Jeudi 8 octobre</b><div class="dz-ag-seg dz-ag-seg-sm"><a class="dz-active" href="#">24 h</a><a href="#">12 h</a></div></div>
    <div class="dz-ag-slots">{_sl}</div>
  </div>
</div>
"""))

# 6. carte d'événement -----------------------------------------------------------
BLOCKS.append(dict(name="carte d'événement", icon="fas fa-ticket-alt", html=f"""
<article class="dz-ag dz-ag-evcard">
  <div class="dz-ag-evmedia">
    <img class="dz-cover" src="https://picsum.photos/seed/nouvellesformes/900/700" alt="Grande salle d'exposition éclairée">
    <div class="dz-ag-datetile"><span>Nov.</span><b>12</b><span>Jeu.</span></div>
    <span class="dz-ag-evtag"><i class="fas fa-fire"></i> Plus que 38 places</span>
  </div>
  <div class="dz-ag-evbody">
    <div class="dz-ag-evtop"><span class="dz-badge">Conférence</span><span class="dz-ag-meta"><i class="fas fa-users"></i> 462 inscrits</span></div>
    <h3 class="dz-ag-evtitle">Nouvelles Formes 2026 : design, produit et IA</h3>
    <p class="dz-ag-evdesc">Une journée de conférences et d'ateliers pour les équipes produit : 18 intervenants, 3 salles, des retours d'expérience concrets.</p>
    <div class="dz-ag-evfacts">
      <div><i class="far fa-calendar"></i><div><b>Jeudi 12 novembre 2026</b><span>09:00 – 18:30 · heure de Paris</span></div></div>
      <div><i class="fas fa-map-marker-alt"></i><div><b>La Sucrière</b><span>49 quai Rambaud, 69002 Lyon</span></div></div>
      <div><i class="fas fa-user-tie"></i><div><b>Organisé par Collectif Ardoise</b><span>12 événements · 4,9 / 5</span></div></div>
    </div>
    <div class="dz-ag-evpeople"><div class="dz-avatars">{av("LF")}{av("NB")}{av("SA")}{av("KB")}</div><span><b>Léa, Nathan</b> et 460 autres participent</span></div>
    <div class="dz-ag-evfoot">
      <div class="dz-ag-price"><span>À partir de</span><b>89 €</b></div>
      <div class="dz-ag-evbtns"><a class="dz-btn dz-btn-ghost" href="#"><i class="far fa-calendar-plus"></i> Ajouter à l'agenda</a><a class="dz-btn" href="#">Réserver</a></div>
    </div>
  </div>
</article>
"""))

# 7. programme d'une conférence --------------------------------------------------
def q(h, m):
    return 2 + int((h - 9) * 4 + m / 15)


_prog = [(2, 9, 45, 10, 30, "Des tableaux de bord que l'on lit vraiment", "Léa Fontaine · Nexora", 1, "Données"),
         (3, 9, 45, 10, 45, "Atelier : prototyper en une heure", "Karim Belkacem", 3, "Atelier"),
         (4, 9, 45, 10, 15, "Accessibilité : les 10 erreurs", "Chloé Vasseur", 2, "Design"),
         (4, 10, 15, 10, 45, "Écrire pour les interfaces", "Inès Morel", 2, "Design"),
         (2, 11, 0, 11, 45, "Tarifer un produit logiciel en 2026", "Nathan Brun · Orbis", 4, "Produit"),
         (3, 11, 0, 12, 30, "Atelier : cartographier le parcours client", "Sofia Amrani", 3, "Atelier"),
         (4, 11, 0, 11, 45, "Systèmes de design à petite échelle", "Tom Guérin", 2, "Design"),
         (2, 11, 45, 12, 30, "Retour d'expérience : migrer sans douleur", "Julien Vauclair", 1, "Données"),
         (4, 11, 45, 12, 30, "Table ronde : l'IA dans l'équipe produit", "4 intervenants", 4, "Produit")]
_pg = "".join(f'<div class="dz-ag-sess dz-ag-k{k}" style="grid-column:{c};grid-row:{q(h1, m1)} / {q(h2, m2)}"><span class="dz-ag-track">{tr}</span><b>{t}</b><span class="dz-ag-who">{who}</span><span class="dz-ag-stime">{h1:02d}:{m1:02d} – {h2:02d}:{m2:02d}</span></div>'
              for c, h1, m1, h2, m2, t, who, k, tr in _prog)
_ph = "".join(f'<span class="dz-ag-ptime" style="grid-row:{q(h, m)}">{h:02d}:{m:02d}</span>' for h, m in [(9, 0), (9, 45), (10, 45), (11, 0), (11, 45), (12, 30)])
BLOCKS.append(dict(name="programme de conférence", icon="fas fa-stream", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><div><span class="dz-ag-eyebrow">Nouvelles Formes 2026 · Lyon</span><h3 class="dz-ag-title">Programme de la matinée</h3></div></div>
    <div class="dz-ag-bar-r"><div class="dz-ag-seg"><a class="dz-active" href="#">Jeu. 12 nov.</a><a href="#">Ven. 13 nov.</a></div><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-download"></i> PDF</a></div>
  </div>
  <div class="dz-ag-legend"><span class="dz-ag-key dz-ag-k1">Données</span><span class="dz-ag-key dz-ag-k2">Design</span><span class="dz-ag-key dz-ag-k3">Atelier</span><span class="dz-ag-key dz-ag-k4">Produit</span></div>
  <div class="dz-ag-scroll">
    <div class="dz-ag-prog">
      <span class="dz-ag-room" style="grid-column:2"><b>Grand amphi</b><span>450 places</span></span>
      <span class="dz-ag-room" style="grid-column:3"><b>Salle Rhône</b><span>60 places · atelier</span></span>
      <span class="dz-ag-room" style="grid-column:4"><b>Salle Saône</b><span>120 places</span></span>
      {_ph}
      <div class="dz-ag-keynote" style="grid-column:2 / 5;grid-row:{q(9, 0)} / {q(9, 45)}"><span class="dz-ag-track">Ouverture</span><b>Plénière : ce que les meilleurs produits ont en commun</b><span class="dz-ag-who">Camille Roussel, Studio Ardoise · Grand amphi</span></div>
      {_pg}
      <div class="dz-ag-break" style="grid-column:2 / 5;grid-row:{q(10, 45)} / {q(11, 0)}"><i class="fas fa-coffee"></i><span>Pause café · espace partenaires</span></div>
      <div class="dz-ag-break dz-ag-lunch" style="grid-column:2 / 5;grid-row:{q(12, 30)} / {q(12, 45)}"><i class="fas fa-utensils"></i><span>Déjeuner · 12:30 – 14:00</span></div>
    </div>
  </div>
</div>
"""))

# 8. frise verticale ----------------------------------------------------------------
_tl = [("Mars 2019", "Création de l'atelier", "Deux fondateurs, un garage à Nantes et une première commande de 40 tables.", "fas fa-seedling", "done", ""),
       ("Sept. 2021", "Premier showroom", "Ouverture rue Crébillon. 1 200 visiteurs le premier mois.", "fas fa-store", "done", ""),
       ("Juin 2023", "Label Entreprise du patrimoine vivant", "Reconnaissance de notre savoir-faire d'ébénisterie.", "fas fa-award", "done", ""),
       ("Janv. 2025", "Boutique en ligne", "32 % du chiffre d'affaires dès la première année.", "fas fa-shopping-bag", "done", ""),
       ("Sept. 2026", "Nouvel atelier de 1 800 m²", "Déménagement à Rezé, 14 artisans, capacité doublée.", "fas fa-industry", "now", "En ce moment"),
       ("2027", "Ouverture à Lyon", "Deuxième showroom prévu au printemps.", "fas fa-flag", "next", "À venir")]
_t = "".join(f'<div class="dz-ag-tli dz-ag-{st}"><span class="dz-ag-tldot"><i class="{ic}"></i></span><div class="dz-ag-tlcard"><span class="dz-ag-tldate">{d}</span>'
             f'{badge_html(b)}<h4 class="dz-ag-tltitle">{t}</h4><p class="dz-ag-tltext">{x}</p></div></div>'
             for d, t, x, ic, st, b in _tl)
BLOCKS.append(dict(name="frise verticale", icon="fas fa-stream", html=f"""
<div class="dz-ag">
  <div class="dz-section-head"><span class="dz-eyebrow">Notre histoire</span><h2 class="dz-h2">Sept ans d'atelier, <em>une pièce à la fois</em></h2></div>
  <div class="dz-ag-tl">{_t}</div>
</div>
"""))

# 9. frise horizontale (feuille de route) ---------------------------------------
_ms = ["Janv.", "Févr.", "Mars", "Avr.", "Mai", "Juin", "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]
_rm = [(1, 3, "Nouvelle facturation", "Livré le 18 mars", 1, "done", 1), (3, 5, "Application mobile", "Livrée le 2 juin", 2, "done", 2),
       (5, 8, "Planning d'équipe", "Livré le 26 août", 3, "done", 1), (8, 11, "Portail client", "68 % · en cours", 1, "now", 2),
       (10, 12, "Connecteurs comptables", "Démarrage le 5 oct.", 4, "next", 1), (11, 13, "Tableaux de bord v2", "Décembre", 2, "next", 2)]
_r = "".join(f'<div class="dz-ag-rmbar dz-ag-k{k} dz-ag-{st}" style="grid-column:{a} / {b};grid-row:{row}"><b>{t}</b><span>{sub}</span></div>' for a, b, t, sub, k, st, row in _rm)
BLOCKS.append(dict(name="frise horizontale", icon="fas fa-road", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><div><span class="dz-ag-eyebrow">Feuille de route produit</span><h3 class="dz-ag-title">Ce qui arrive en 2026</h3></div></div>
    <div class="dz-ag-legend"><span class="dz-ag-key dz-ag-kdone">Livré</span><span class="dz-ag-key dz-ag-know">En cours</span><span class="dz-ag-key dz-ag-knext">Prévu</span></div>
  </div>
  <div class="dz-ag-scroll">
    <div class="dz-ag-road">
      <div class="dz-ag-rmonths">{''.join(f'<span class="{"dz-ag-cur" if m == "Sept." else ""}">{m}</span>' for m in _ms)}</div>
      <div class="dz-ag-rgrid">
        <div class="dz-ag-rtoday" style="left:73%"><span>Aujourd'hui</span></div>
        {_r}
      </div>
      <div class="dz-ag-rmiles">
        <span class="dz-ag-mile" style="left:20%"><i class="fas fa-flag"></i> T1 clos</span>
        <span class="dz-ag-mile" style="left:45%"><i class="fas fa-rocket"></i> Lancement mobile</span>
        <span class="dz-ag-mile dz-ag-milenext" style="left:86%"><i class="fas fa-star"></i> Salon Nouvelles Formes</span>
      </div>
    </div>
  </div>
</div>
"""))

# 10. compte à rebours ------------------------------------------------------------
BLOCKS.append(dict(name="compte à rebours d’événement", icon="fas fa-hourglass-half", html="""
<div class="dz-ag dz-ag-count">
  <div class="dz-ag-countbg"></div>
  <div class="dz-ag-countin">
    <span class="dz-ag-livetag"><span class="dz-dot"></span> Billetterie ouverte</span>
    <h2 class="dz-ag-counttitle">Nouvelles Formes 2026</h2>
    <p class="dz-ag-countsub">Jeudi 12 et vendredi 13 novembre · La Sucrière, Lyon</p>
    <div class="dz-ag-clock"><span class="dz-countdown dz-ag-cd">2026-11-12 09:00</span></div>
    <p class="dz-ag-cunits">avant l'ouverture des portes · jours, heures, minutes, secondes</p>
    <div class="dz-ag-cfoot">
      <a class="dz-btn dz-btn-lg" href="#">Réserver ma place <i class="fas fa-arrow-right"></i></a>
      <a class="dz-btn dz-btn-lg dz-btn-ghost" href="#"><i class="far fa-calendar-plus"></i> Ajouter à l'agenda</a>
    </div>
    <div class="dz-ag-cstock"><div class="dz-ag-cstock-t"><span>Tarif lève-tôt</span><b>412 / 500 places vendues</b></div><div class="dz-progress"><span style="--v:82%"></span></div></div>
  </div>
</div>
"""))

# 11. disponibilités d'une équipe --------------------------------------------------
def hs(h, m=0):
    return 2 + int((h - 8) * 2 + m / 30)


_team = [("CR", "Camille Roussel", "Paris", [(9, 0, 10, 30, "Comité"), (12, 0, 14, 0, "Déjeuner client"), (16, 0, 17, 0, "Revue")]),
         ("NB", "Nathan Brun", "Paris", [(8, 30, 10, 0, "Trajet"), (10, 30, 12, 0, "Atelier"), (13, 30, 15, 0, "Démo")]),
         ("SA", "Sofia Amrani", "Casablanca · −1 h", [(9, 0, 12, 0, "Formation"), (14, 0, 15, 0, "Point 1:1"), (17, 0, 18, 0, "Sport")]),
         ("KB", "Karim Belkacem", "Montréal · −6 h", [(8, 0, 14, 30, "Hors horaires"), (17, 0, 18, 0, "Standup")]),
         ("LF", "Léa Fontaine", "Paris · congés l'après-midi", [(10, 0, 11, 0, "Appel"), (13, 0, 18, 0, "Congé")])]
_tr = []
for ini, n, tz, busy in _team:
    blocks = "".join(f'<div class="dz-ag-busy{" dz-ag-off" if lab in ("Hors horaires", "Congé") else ""}" style="grid-column:{hs(a, b)} / {hs(c, d)}">{lab}</div>' for a, b, c, d, lab in busy)
    _tr.append(f'<div class="dz-ag-trow"><div class="dz-ag-tperson">{av(ini)}<div><b>{n}</b><span>{tz}</span></div></div>{blocks}</div>')
BLOCKS.append(dict(name="disponibilités de l'équipe", icon="fas fa-user-clock", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><div><h3 class="dz-ag-title">Trouver un créneau</h3><p class="dz-ag-sub">Réunion de lancement · 1 h · 5 participants</p></div></div>
    <div class="dz-ag-bar-r"><div class="dz-ag-nav"><a href="#" aria-label="Jour précédent"><i class="fas fa-chevron-left"></i></a><a class="dz-ag-todaybtn" href="#">Ven. 25 sept.</a><a href="#" aria-label="Jour suivant"><i class="fas fa-chevron-right"></i></a></div></div>
  </div>
  <div class="dz-ag-scroll">
    <div class="dz-ag-team">
      <div class="dz-ag-trow dz-ag-thead"><span class="dz-ag-tperson">Heure de Paris</span>{''.join(f'<span style="grid-column:{hs(h)} / span 2">{h:02d}:00</span>' for h in range(8, 18))}</div>
      <div class="dz-ag-tbody">
        <div class="dz-ag-common" style="--a:14;--n:2"><span>15:00 – 16:00 · tout le monde est libre</span></div>
        {''.join(_tr)}
      </div>
    </div>
  </div>
  <div class="dz-ag-foot"><span class="dz-ag-sub"><i class="fas fa-lightbulb"></i> 2 autres créneaux possibles sans Léa : 11:00 et 12:30</span><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-paper-plane"></i> Inviter à 15:00</a></div>
</div>
"""))

# 12. mini-calendrier ---------------------------------------------------------------
_mc = ""
for i, d in enumerate([31] + list(range(1, 31)) + [1, 2, 3, 4]):
    out = i == 0 or i > 30
    c = "dz-ag-mc"
    if out:
        c += " dz-ag-out"
    elif d == 15:
        c += " dz-ag-rs"
    elif d in (16, 17):
        c += " dz-ag-rin"
    elif d == 18:
        c += " dz-ag-re"
    if not out and d == 24:
        c += " dz-ag-today"
    if not out and d in (2, 9, 21, 22, 25, 30):
        c += " dz-ag-has"
    _mc += f'<span class="{c}">{d}</span>'
BLOCKS.append(dict(name="mini-calendrier", icon="far fa-calendar-alt", html=f"""
<div class="dz-ag dz-ag-minis">
  <div class="dz-ag-panel dz-ag-minical">
    <div class="dz-ag-mhead"><b>Septembre 2026</b><div class="dz-ag-nav dz-ag-nav-sm"><a href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a><a href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a></div></div>
    <div class="dz-ag-mcgrid"><span class="dz-ag-mwd">L</span><span class="dz-ag-mwd">M</span><span class="dz-ag-mwd">M</span><span class="dz-ag-mwd">J</span><span class="dz-ag-mwd">V</span><span class="dz-ag-mwd">S</span><span class="dz-ag-mwd">D</span>{_mc}</div>
    <div class="dz-ag-range"><div><span>Du</span><b>mar. 15 sept.</b></div><i class="fas fa-arrow-right"></i><div><span>Au</span><b>ven. 18 sept.</b></div><span class="dz-badge dz-badge-neutral">4 jours</span></div>
  </div>
  <div class="dz-ag-panel dz-ag-upnext">
    <div class="dz-ag-mhead"><b>À venir</b><a class="dz-ag-link" href="#">Tout voir</a></div>
    <div class="dz-ag-up dz-ag-k1"><div class="dz-ag-update"><span>Jeu.</span><b>24</b></div><div><b>Bilan sprint 38</b><span>16:30 – 17:30 · Salle Atelier</span></div></div>
    <div class="dz-ag-up dz-ag-k5"><div class="dz-ag-update"><span>Ven.</span><b>25</b></div><div><b>Signature Vauclair</b><span>11:00 · Nantes</span></div></div>
    <div class="dz-ag-up dz-ag-k4"><div class="dz-ag-update"><span>Mer.</span><b>30</b></div><div><b>Clôture du trimestre</b><span>Toute la journée</span></div></div>
  </div>
</div>
"""))

# 13. planning de salles / ressources --------------------------------------------
_rooms = [("fas fa-users", "Salle Horizon", "12 pers. · écran", [(9, 30, 11, 0, "Comité produit", 1), (14, 0, 16, 0, "Formation RGPD", 4)]),
          ("fas fa-chalkboard", "Salle Atelier", "6 pers. · tableau", [(10, 0, 12, 30, "Atelier design", 1), (16, 30, 17, 30, "Bilan sprint", 4)]),
          ("fas fa-headphones", "Box Focus", "2 pers.", [(8, 0, 9, 0, "Appel US", 2), (13, 0, 14, 30, "Entretien", 5), (15, 0, 18, 0, "Rédaction", 4)]),
          ("fas fa-video", "Studio vidéo", "Caméra, micros", [(11, 0, 13, 0, "Tournage tuto", 3)]),
          ("fas fa-car", "Voiture de service", "Zoé · 5 places", [(8, 0, 12, 0, "Visite chantier Rezé", 2), (17, 0, 19, 0, "Livraison", 3)])]
_rr = []
for ic, n, cap, bk in _rooms:
    items = "".join(f'<div class="dz-ag-bk dz-ag-k{k}" style="grid-column:{hs(a, b)} / {hs(c, d)}"><b>{t}</b><span>{a:02d}:{b:02d} – {c:02d}:{d:02d}</span></div>' for a, b, c, d, t, k in bk)
    _rr.append(f'<div class="dz-ag-rrow"><div class="dz-ag-rres"><span class="dz-ag-rico"><i class="{ic}"></i></span><div><b>{n}</b><span>{cap}</span></div></div>{items}</div>')
BLOCKS.append(dict(name="réservation de salles", icon="fas fa-door-open", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><div><h3 class="dz-ag-title">Salles et ressources</h3><p class="dz-ag-sub">Jeudi 24 septembre · 5 ressources · 3 libres maintenant</p></div></div>
    <div class="dz-ag-bar-r"><div class="dz-ag-seg"><a class="dz-active" href="#">Toutes</a><a href="#">Salles</a><a href="#">Matériel</a></div><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Réserver</a></div>
  </div>
  <div class="dz-ag-scroll">
    <div class="dz-ag-rsched">
      <div class="dz-ag-rrow dz-ag-thead"><span class="dz-ag-rres">Ressource</span>{''.join(f'<span style="grid-column:{hs(h)} / span 2">{h:02d}h</span>' for h in range(8, 19))}</div>
      <div class="dz-ag-rbody">
        <div class="dz-ag-rnow" style="--a:13.07"><span>14:32</span></div>
        {''.join(_rr)}
      </div>
    </div>
  </div>
</div>
"""))

# 14. rappels -------------------------------------------------------------------------
_rem = [("En retard", "danger", [("Relancer Orbis Conseil pour la facture n° 2026-118", "Hier, 17:00", "fas fa-exclamation-circle", "Clients", 2, True, False)]),
        ("Aujourd'hui", "", [("Envoyer l'ordre du jour du comité", "09:00", "far fa-clock", "Produit", 1, False, True),
                             ("Valider les congés de l'équipe", "15:00", "fas fa-redo", "Interne", 4, False, False),
                             ("Appeler le plombier pour l'atelier", "17:30", "far fa-clock", "Personnel", 5, True, False)]),
        ("Demain", "", [("Préparer la signature Vauclair", "10:00", "fas fa-paperclip", "Clients", 2, False, False)]),
        ("Plus tard", "", [("Renouveler l'assurance du local", "Mer. 30 sept.", "far fa-calendar", "Interne", 4, False, False),
                           ("Réserver l'hôtel pour le salon de Lyon", "Lun. 5 oct.", "far fa-calendar", "Événements", 3, False, False)])]
_rm_html = ""
for g, tone, items in _rem:
    rows = "".join(f'<div class="dz-ag-rem dz-ag-k{k}{" dz-ag-done" if done else ""}"><span class="dz-ag-rchk">{CHECK if done else ""}</span>'
                   f'<div class="dz-ag-rtext"><b>{t}</b><div class="dz-ag-rmeta"><span class="dz-ag-meta{" dz-ag-late" if tone else ""}"><i class="{ic}"></i> {when}</span><span class="dz-ag-rtag">{tag}</span></div></div>'
                   f'{FLAG if flag else ""}</div>'
                   for t, when, ic, tag, k, flag, done in items)
    _rm_html += f'<div class="dz-ag-rgroup"><div class="dz-ag-rgh{" dz-ag-late" if tone else ""}"><b>{g}</b><span>{len(items)}</span></div>{rows}</div>'
BLOCKS.append(dict(name="rappels", icon="fas fa-bell", wrap="narrow", html=f"""
<div class="dz-ag dz-ag-panel dz-ag-reminders">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><h3 class="dz-ag-title">Rappels</h3><span class="dz-badge dz-badge-danger">1 en retard</span></div>
    <div class="dz-ag-bar-r"><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-plus"></i> Nouveau rappel</a></div>
  </div>
  <div class="dz-ag-rstats"><div><b>7</b><span>à faire</span></div><div><b>3</b><span>aujourd'hui</span></div><div><b>12</b><span>faits cette semaine</span></div></div>
  {_rm_html}
</div>
"""))

# 15. fuseaux horaires -----------------------------------------------------------------
_clk = [("Paris", "Europe · UTC+2", "14:32", 76, 192, "Jeu. 24 sept.", "fas fa-sun", "Bureau ouvert", True),
        ("Dakar", "Afrique · UTC+0", "12:32", 16, 192, "Jeu. 24 sept.", "fas fa-sun", "−2 h", True),
        ("New York", "Amérique · UTC−4", "08:32", 256, 192, "Jeu. 24 sept.", "fas fa-cloud-sun", "−6 h", True),
        ("Tokyo", "Asie · UTC+9", "21:32", 286, 192, "Jeu. 24 sept.", "fas fa-moon", "+7 h", False)]
_ck = "".join(f'<div class="dz-ag-clockcard{"" if day else " dz-ag-night"}"><div class="dz-ag-face" style="--h:{h}deg;--m:{m}deg"><i class="dz-ag-hh"></i><i class="dz-ag-mh"></i><i class="dz-ag-sh"></i></div>'
              f'<div class="dz-ag-cinfo"><b>{city}</b><span>{zone}</span><span class="dz-ag-digital">{t}</span><span class="dz-ag-meta"><i class="{ic}"></i> {date} · {off}</span></div></div>'
              for city, zone, t, h, m, date, ic, off, day in _clk)
_work = {"Paris": range(9, 18), "Dakar": range(11, 20), "New York": range(15, 24), "Tokyo": range(2, 11)}
_zr = "".join(f'<div class="dz-ag-zrow"><span class="dz-ag-zname">{c}</span><div class="dz-ag-zcells">' + "".join(f'<i class="{"dz-ag-work" if h in _work[c] else ""}{" dz-ag-zc" if 15 <= h < 18 else ""}"></i>' for h in range(24)) + '</div></div>' for c in _work)
BLOCKS.append(dict(name="fuseaux horaires", icon="fas fa-globe", html=f"""
<div class="dz-ag dz-ag-panel">
  <div class="dz-ag-bar">
    <div class="dz-ag-bar-l"><div><h3 class="dz-ag-title">Horloges de l'équipe</h3><p class="dz-ag-sub">4 bureaux · heure d'été en Europe jusqu'au 25 octobre</p></div></div>
    <div class="dz-ag-bar-r"><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-plus"></i> Ajouter une ville</a></div>
  </div>
  <div class="dz-ag-clocks">{_ck}</div>
  <div class="dz-ag-zones">
    <div class="dz-ag-zhead"><b>Heures de bureau (9 h – 18 h), ramenées à l'heure de Paris</b><span class="dz-badge dz-badge-success"><i class="fas fa-check"></i> 15:00 – 18:00 commun à 3 bureaux</span></div>
    <div class="dz-ag-scroll"><div class="dz-ag-ztable">{_zr}<div class="dz-ag-zrow dz-ag-zaxis"><span class="dz-ag-zname"></span><div class="dz-ag-zcells"><span>00</span><span>03</span><span>06</span><span>09</span><span>12</span><span>15</span><span>18</span><span>21</span></div></div></div></div>
  </div>
</div>
"""))

# 16. billetterie -----------------------------------------------------------------------
_tk = [("Lève-tôt", "Accès aux 2 jours · conférences et ateliers", "89 €", "129 €", "Plus que 38 places", 92, 2, "", ["2 jours de conférences", "Replays pendant 1 an"]),
       ("Standard", "Accès aux 2 jours · conférences et ateliers", "129 €", "", "Disponible", 41, 0, "", ["2 jours de conférences", "Déjeuners inclus"]),
       ("Premium", "Tout Standard + dîner des intervenants", "249 €", "", "Places limitées", 70, 1, "Le plus complet", ["Dîner des intervenants", "Placement réservé", "Rencontres 1:1"]),
       ("Étudiant", "Sur justificatif · 2 jours", "39 €", "", "Complet", 100, 0, "", ["2 jours de conférences"])]
_tkh = []
for n, d, p, old, stock, v, qty, bdg, perks in _tk:
    sold = v >= 100
    step = ('<span class="dz-badge dz-badge-neutral">Complet</span>' if sold else
            f'<div class="dz-ag-qty"><a href="#" aria-label="Retirer un billet"><i class="fas fa-minus"></i></a><b>{qty}</b><a href="#" aria-label="Ajouter un billet"><i class="fas fa-plus"></i></a></div>')
    _tkh.append(f'<div class="dz-ag-ticket{" dz-ag-tsel" if qty else ""}{" dz-ag-tsold" if sold else ""}"><div class="dz-ag-tinfo"><div class="dz-ag-tname"><b>{n}</b>{badge_html(bdg)}</div>'
                f'<span class="dz-ag-tdesc">{d}</span><div class="dz-ag-perks">{"".join("<span>" + CHECK + " " + x + "</span>" for x in perks)}</div>'
                f'<div class="dz-ag-tstock"><div class="dz-progress"><span style="--v:{v}%"></span></div><span>{stock}</span></div></div>'
                f'<div class="dz-ag-tbuy"><div class="dz-ag-tprice"><b>{p}</b>{("<s>" + old + "</s>") if old else ""}</div>{step}</div></div>')
BLOCKS.append(dict(name="billetterie", icon="fas fa-ticket-alt", html=f"""
<div class="dz-ag dz-ag-tickets">
  <div class="dz-ag-tlist">
    <div class="dz-ag-bar"><div class="dz-ag-bar-l"><div><span class="dz-ag-eyebrow">Nouvelles Formes 2026 · 12 et 13 nov.</span><h3 class="dz-ag-title">Choisissez vos billets</h3></div></div></div>
    {''.join(_tkh)}
  </div>
  <aside class="dz-ag-panel dz-ag-cart">
    <b class="dz-ag-carttitle">Récapitulatif</b>
    <div class="dz-ag-cline"><span>2 × Lève-tôt</span><b>178,00 €</b></div>
    <div class="dz-ag-cline"><span>1 × Premium</span><b>249,00 €</b></div>
    <div class="dz-ag-cline dz-ag-cmute"><span>Frais de service</span><b>6,40 €</b></div>
    <div class="dz-ag-cline dz-ag-cdisc"><span><i class="fas fa-tag"></i> Code EQUIPE10</span><b>−42,70 €</b></div>
    <div class="dz-ag-ctotal"><span>Total TTC</span><b>390,70 €</b></div>
    <a class="dz-btn dz-btn-block dz-btn-lg" href="#"><i class="fas fa-lock"></i> Payer 390,70 €</a>
    <p class="dz-ag-cnote"><i class="fas fa-undo"></i> Remboursable jusqu'au 29 octobre · billets nominatifs envoyés par e-mail</p>
    <div class="dz-ag-hold"><i class="far fa-clock"></i><span>Places réservées pendant <b>9:41</b></span></div>
  </aside>
</div>
"""))

# 17. agenda mobile --------------------------------------------------------------------
BLOCKS.append(dict(name="agenda mobile", icon="fas fa-mobile-alt", html=f"""
<div class="dz-ag dz-ag-mobwrap">
  <div class="dz-ag-phone">
    <div class="dz-ag-screen">
      <div class="dz-ag-status"><b>14:32</b><span><i class="fas fa-signal"></i> <i class="fas fa-wifi"></i> <i class="fas fa-battery-three-quarters"></i></span></div>
      <div class="dz-ag-mtop"><div><span>Jeudi</span><b>Septembre</b></div><div class="dz-ag-mtopbtns"><a href="#" aria-label="Rechercher"><i class="fas fa-search"></i></a><span class="dz-avatar dz-avatar-sm">CR</span></div></div>
      <div class="dz-ag-strip">
        <div><span>L</span><b>21</b><i></i></div><div><span>M</span><b>22</b><i></i></div><div><span>M</span><b>23</b></div>
        <div class="dz-ag-sel"><span>J</span><b>24</b><i></i></div><div><span>V</span><b>25</b><i></i></div><div class="dz-ag-we"><span>S</span><b>26</b></div><div class="dz-ag-we"><span>D</span><b>27</b></div>
      </div>
      <div class="dz-ag-mlist">
        <div class="dz-ag-mev dz-ag-k1 dz-ag-past"><div class="dz-ag-mt"><b>09:30</b><span>11:00</span></div><div class="dz-ag-mc2"><b>Comité produit</b><span>Salle Horizon</span></div></div>
        <div class="dz-ag-mev dz-ag-k2 dz-ag-live"><div class="dz-ag-mt"><b>14:00</b><span>15:00</span></div><div class="dz-ag-mc2"><b>Appel Orbis Conseil</b><span><i class="fas fa-video"></i> Rejoindre · encore 28 min</span></div></div>
        <div class="dz-ag-mnow"><span>14:32</span></div>
        <div class="dz-ag-mev dz-ag-k4"><div class="dz-ag-mt"><b>16:30</b><span>17:30</span></div><div class="dz-ag-mc2"><b>Bilan sprint 38</b><span>Salle Atelier</span></div></div>
        <div class="dz-ag-mev dz-ag-k3"><div class="dz-ag-mt"><b>18:00</b><span>19:30</span></div><div class="dz-ag-mc2"><b>Afterwork</b><span>Terrasse du 5e</span></div></div>
      </div>
      <a class="dz-ag-mfab" href="#" aria-label="Nouvel événement"><i class="fas fa-plus"></i></a>
      <div class="dz-ag-mnav"><a class="dz-active" href="#"><i class="far fa-calendar"></i><span>Agenda</span></a><a href="#"><i class="far fa-check-square"></i><span>Tâches</span></a><a href="#"><i class="far fa-bell"></i><span>Rappels</span></a><a href="#"><i class="far fa-user"></i><span>Profil</span></a></div>
    </div>
  </div>
  <div class="dz-ag-mobtext">
    <span class="dz-eyebrow">Application mobile</span>
    <h2 class="dz-h2">Votre journée, <em>d'un coup d'œil</em></h2>
    <p class="dz-lead">Glissez d'un jour à l'autre, rejoignez un appel en un geste et recevez un rappel dix minutes avant chaque rendez-vous.</p>
    <div class="dz-ag-mfeat"><span><i class="fas fa-sync-alt"></i> Synchronisé avec tous vos agendas</span><span><i class="fas fa-bell"></i> Rappels intelligents</span><span><i class="fas fa-plane"></i> Fonctionne hors connexion</span></div>
  </div>
</div>
"""))

# 18. invitation / réponse --------------------------------------------------------------
_rs = [("NB", "Nathan Brun", "Organisateur", "org"), ("LF", "Léa Fontaine", "Participe", "yes"), ("SA", "Sofia Amrani", "Participe", "yes"),
       ("KB", "Karim Belkacem", "Peut-être · « en déplacement le matin »", "maybe"), ("TG", "Tom Guérin", "Ne participe pas", "no"), ("IM", "Inès Morel", "En attente", "wait")]
_rsh = "".join(f'<div class="dz-ag-guest dz-ag-g{st}">{av(i)}<div><b>{n}</b><span>{s}</span></div><span class="dz-ag-gico"></span></div>' for i, n, s, st in _rs)
BLOCKS.append(dict(name="invitation", icon="far fa-envelope-open", wrap="narrow", html=f"""
<div class="dz-ag dz-ag-panel dz-ag-invite">
  <div class="dz-ag-invhead">
    <div class="dz-ag-datetile dz-ag-dt-inline"><span>Oct.</span><b>02</b><span>Ven.</span></div>
    <div>
      <span class="dz-ag-eyebrow">Invitation de Nathan Brun</span>
      <h3 class="dz-ag-title dz-ag-invtitle">Séminaire de rentrée de l'équipe</h3>
      <div class="dz-ag-bmeta dz-ag-row">
        <span class="dz-ag-meta"><i class="far fa-clock"></i> 09:30 – 17:00</span>
        <span class="dz-ag-meta"><i class="fas fa-map-marker-alt"></i> Domaine des Iris, Clisson</span>
        <span class="dz-ag-meta"><i class="fas fa-bus"></i> Navette à 08:45</span>
      </div>
    </div>
  </div>
  <div class="dz-ag-rsvp">
    <b>Participerez-vous ?</b>
    <div class="dz-ag-rsvpbtns"><a class="dz-ag-yes dz-active" href="#"><i class="fas fa-check"></i> Oui</a><a class="dz-ag-maybe" href="#"><i class="fas fa-question"></i> Peut-être</a><a class="dz-ag-no" href="#"><i class="fas fa-times"></i> Non</a></div>
  </div>
  <div class="dz-ag-rsum"><span class="dz-ag-rs-yes"><b>8</b> oui</span><span class="dz-ag-rs-maybe"><b>2</b> peut-être</span><span class="dz-ag-rs-no"><b>1</b> non</span><span class="dz-ag-rs-wait"><b>3</b> en attente</span></div>
  <div class="dz-ag-rbar"><i class="dz-ag-rs-yes" style="flex:8"></i><i class="dz-ag-rs-maybe" style="flex:2"></i><i class="dz-ag-rs-no" style="flex:1"></i><i class="dz-ag-rs-wait" style="flex:3"></i></div>
  <div class="dz-ag-guests">{_rsh}</div>
  <div class="dz-ag-foot"><a class="dz-ag-link" href="#">Voir les 14 invités</a><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-comment"></i> Ajouter une note</a></div>
</div>
"""))

# 19. événements à venir ----------------------------------------------------------------
_up = [("Oct.", "08", "Jeu.", "atelier-ceramique", "Atelier", "Initiation au tour de potier", "18:30 · Atelier Lune, Nantes", "45 €", "6 places", ""),
       ("Oct.", "17", "Sam.", "marche-createurs", "Marché", "Marché des créateurs d'automne", "10:00 – 19:00 · Halles de Rezé", "Gratuit", "82 exposants", "k3"),
       ("Nov.", "12", "Jeu.", "conference-lyon", "Conférence", "Nouvelles Formes 2026", "09:00 · La Sucrière, Lyon", "89 €", "38 places", "k2")]
_uph = "".join(f'<a class="dz-ag-upcard dz-ag-{k or "k1"}" href="#"><div class="dz-ag-upimg"><img class="dz-cover" src="https://picsum.photos/seed/{img}/640/400" alt="{t}"><div class="dz-ag-datetile"><span>{mo}</span><b>{d}</b><span>{wd}</span></div></div>'
               f'<div class="dz-ag-upbody"><span class="dz-ag-cat">{cat}</span><h3 class="dz-ag-uptitle">{t}</h3><span class="dz-ag-meta"><i class="far fa-clock"></i> {where}</span>'
               f'<div class="dz-ag-upfoot"><b>{price}</b><span>{left}</span></div></div></a>'
               for mo, d, wd, img, cat, t, where, price, left, k in _up)
BLOCKS.append(dict(name="événements à venir", icon="far fa-calendar-plus", html=f"""
<div class="dz-ag">
  <div class="dz-ag-uphead">
    <div><span class="dz-eyebrow">Agenda</span><h2 class="dz-h2">Prochains <em>rendez-vous</em></h2></div>
    <div class="dz-ag-seg"><a class="dz-active" href="#">Tous</a><a href="#">Ateliers</a><a href="#">Marchés</a><a href="#">Conférences</a></div>
  </div>
  <div class="dz-ag-upgrid">{_uph}</div>
</div>
"""))

# 20. horaires d'ouverture ----------------------------------------------------------------
_hrs = [("Lundi", "Fermé", ""), ("Mardi", "09:30 – 13:00 · 14:00 – 19:00", ""), ("Mercredi", "09:30 – 13:00 · 14:00 – 19:00", ""),
        ("Jeudi", "09:30 – 19:00", "today"), ("Vendredi", "09:30 – 19:30", ""), ("Samedi", "10:00 – 18:00", ""), ("Dimanche", "10:00 – 13:00", "")]
_hh = "".join(f'<div class="dz-ag-hrow{" dz-ag-today" if st else ""}{" dz-ag-closed" if h == "Fermé" else ""}"><b>{d}</b><span>{h}</span>{badge_html("Aujourd’hui") if st else ""}</div>' for d, h, st in _hrs)
BLOCKS.append(dict(name="horaires d'ouverture", icon="far fa-clock", wrap="narrow", html=f"""
<div class="dz-ag dz-ag-panel dz-ag-hours">
  <div class="dz-ag-hstatus">
    <span class="dz-ag-open"><span class="dz-dot"></span> Ouvert</span>
    <div><b>Ferme à 19:00</b><span>dans 4 h 28 · jeudi 24 septembre</span></div>
  </div>
  <h3 class="dz-ag-title">Horaires de la boutique</h3>
  <div class="dz-ag-hlist">{_hh}</div>
  <div class="dz-ag-except"><i class="fas fa-info-circle"></i><div><b>Horaires exceptionnels</b><span>Fermé le mercredi 11 novembre · ouvert le dimanche 20 décembre de 10:00 à 18:00</span></div></div>
  <div class="dz-ag-foot"><span class="dz-ag-meta"><i class="fas fa-map-marker-alt"></i> 14 rue Kervégan, Nantes</span><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-directions"></i> Itinéraire</a></div>
</div>
"""))
