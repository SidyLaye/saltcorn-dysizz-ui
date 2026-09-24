"""Famille « Projet » : tickets, kanban, cycles, feuille de route, jalons, charge.
Tout le CSS est dans styles/30-projet.css (préfixe dz-pj-)."""

FAMILY = "projet"

# ------------------------------------------------------------------ petits morceaux
PEOPLE = {
    "LM": ("Léa Moreau", 1), "KB": ("Karim Benali", 2), "SM": ("Sofia Marchetti", 3), "TG": ("Thomas Girard", 4),
    "IL": ("Inès Laurent", 5), "HF": ("Hugo Fontaine", 7), "NO": ("Nadia Ouali", 6), "JP": ("Julien Petit", 2),
}


def st(k):
    return f'<span class="dz-pj-st dz-pj-st-{k}"></span>'


def pri(n):
    return f'<span class="dz-pj-pri dz-pj-pri-{n}"></span>'


def av(ini, size=""):
    if ini is None:
        return f'<span class="dz-pj-av dz-pj-av-none{size}"><i class="fas fa-user"></i></span>'
    return f'<span class="dz-pj-av dz-pj-c{PEOPLE[ini][1]}{size}">{ini}</span>'


def avs(*inis, more=None):
    extra = f'<span class="dz-pj-more">+{more}</span>' if more else ""
    return '<span class="dz-pj-avs">' + "".join(av(i) for i in inis) + extra + "</span>"


def lbl(t, c):
    return f'<span class="dz-pj-lbl dz-pj-c{c}">{t}</span>'


LBL = {"Bug": 6, "Mobile": 2, "API": 7, "Design": 3, "Perf": 5, "Sécurité": 6, "Web": 1, "Dette": 5, "Client": 4}


def lbls(*names, cls=""):
    return "".join(f'<span class="dz-pj-lbl dz-pj-c{LBL[n]}{cls}">{n}</span>' for n in names)


# ------------------------------------------------------------------ 1. en-tête de projet
HEADER = """
<div class="dz-pj-shell dz-pj-top">
  <div class="dz-pj-top-main">
    <div class="dz-pj-top-id">
      <span class="dz-pj-picon dz-pj-picon-lg dz-pj-c2"><i class="fas fa-mobile-alt"></i></span>
      <div>
        <div class="dz-pj-crumbs"><a href="#">Nexora</a><i class="fas fa-chevron-right"></i><a href="#">Équipe Produit</a><i class="fas fa-chevron-right"></i><span>Projets</span></div>
        <h2 class="dz-pj-top-name">Application mobile 3.0</h2>
        <div class="dz-pj-top-sub">
          <span class="dz-pj-health">En bonne voie</span>
          <span><i class="far fa-calendar"></i> 1 sept. → 18 déc. 2026</span>
          <span><i class="fas fa-bullseye"></i> 64 % terminé</span>
        </div>
      </div>
    </div>
    <div class="dz-pj-top-actions">
      <span class="dz-pj-avs"><span class="dz-pj-av dz-pj-av-md dz-pj-c1">LM</span><span class="dz-pj-av dz-pj-av-md dz-pj-c2">KB</span><span class="dz-pj-av dz-pj-av-md dz-pj-c3">SM</span><span class="dz-pj-av dz-pj-av-md dz-pj-c4">TG</span><span class="dz-pj-more">+5</span></span>
      <a class="dz-pj-btn" href="#"><i class="fas fa-user-plus"></i> Inviter</a>
      <a class="dz-pj-ibtn" href="#" aria-label="Favori"><i class="far fa-star"></i></a>
      <a class="dz-pj-ibtn" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a>
      <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Nouveau ticket</a>
    </div>
  </div>
  <div class="dz-pj-tabs">
    <a class="dz-pj-tab" href="#"><i class="far fa-compass"></i> Vue d'ensemble</a>
    <a class="dz-pj-tab dz-active" href="#"><i class="far fa-check-circle"></i> Tickets <span class="dz-pj-count">48</span></a>
    <a class="dz-pj-tab" href="#"><i class="fas fa-columns"></i> Board</a>
    <a class="dz-pj-tab" href="#"><i class="fas fa-stream"></i> Roadmap</a>
    <a class="dz-pj-tab" href="#"><i class="far fa-file-alt"></i> Docs <span class="dz-pj-count">7</span></a>
    <a class="dz-pj-tab" href="#"><i class="fas fa-bullhorn"></i> Mises à jour</a>
  </div>
</div>
"""


# ------------------------------------------------------------------ 2. liste de tickets
def row(p, id_, s, title, labels=(), who="LM", date=None, late=False, sub=None, active=False):
    meta = ""
    if sub:
        meta += f'<span class="dz-pj-sub dz-pj-hide-sm"><i class="fas fa-code-branch"></i> {sub}</span>'
    if labels:
        meta += f'<span class="dz-pj-row-meta dz-pj-hide-sm">{lbls(*labels)}</span>'
    if date:
        meta += f'<span class="dz-pj-date{" dz-pj-late" if late else ""} dz-pj-hide-sm">{date}</span>'
    meta += av(who)
    return (f'<a class="dz-pj-row{" dz-active" if active else ""}" href="#">{pri(p)}<span class="dz-pj-id">{id_}</span>{st(s)}'
            f'<span class="dz-pj-row-title">{title}</span><span class="dz-pj-row-meta">{meta}</span></a>')


def group(s, name, n, rows):
    return (f'<div class="dz-pj-group"><div class="dz-pj-ghead">{st(s)}<b>{name}</b><span class="dz-pj-count">{n}</span>'
            f'<span class="dz-pj-sp"></span><a class="dz-pj-ibtn" href="#" aria-label="Ajouter un ticket"><i class="fas fa-plus"></i></a></div>'
            + "".join(rows) + "</div>")


LIST = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Tickets actifs</h3><span class="dz-pj-count">11</span>
    <span class="dz-pj-sp"></span>
    <a class="dz-pj-btn" href="#"><i class="fas fa-filter"></i> Filtrer</a>
    <a class="dz-pj-btn dz-pj-hide-sm" href="#"><i class="fas fa-sliders-h"></i> Affichage</a>
    <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Nouveau</a>
  </div>
  {group("prog", "En cours", 3, [
      row(4, "ENG-142", "prog", "Les brouillons hors ligne ne se synchronisent pas au retour du réseau", ("Bug", "Mobile"), "LM", "26 sept.", sub="2/4", active=True),
      row(3, "ENG-139", "prog", "Nouvel écran de paiement en une étape", ("Design", "Web"), "SM", "30 sept."),
      row(2, "ENG-131", "prog", "Pagination par curseur sur l'API des commandes", ("API",), "KB", "2 oct.", sub="1/3"),
  ])}
  {group("review", "En revue", 2, [
      row(3, "ENG-128", "review", "Réduire de 40 % le temps de démarrage à froid", ("Perf", "Mobile"), "TG", "25 sept."),
      row(2, "ENG-120", "review", "Journal d'audit pour les changements de rôle", ("Sécurité",), "NO", "3 oct."),
  ])}
  {group("todo", "À faire", 4, [
      row(3, "ENG-151", "todo", "Relance automatique des factures impayées", ("Client",), "IL", "22 sept.", late=True),
      row(2, "ENG-149", "todo", "Thème sombre pour le tableau de bord analytique", ("Design",), "SM", "8 oct."),
      row(1, "ENG-147", "todo", "Mettre à jour la bibliothèque de graphiques", ("Dette",), "HF"),
      row(0, "ENG-146", "todo", "Documenter les webhooks sortants", ("API",), None),
  ])}
  {group("done", "Terminé", 2, [
      row(2, "ENG-118", "done", "Export CSV des équipes et des rôles", ("Web",), "JP", "19 sept."),
      row(1, "ENG-112", "done", "Corriger l'arrondi des remises sur les devis", ("Bug",), "KB", "17 sept."),
  ])}
</div>
"""


# ------------------------------------------------------------------ 3. kanban
def card(id_, title, labels=(), who="LM", p=2, com=0, sub=None, date=None, late=False, cover=None, cls=""):
    foot = pri(p)
    if com:
        foot += f'<span><i class="far fa-comment"></i> {com}</span>'
    if sub:
        foot += f'<span><i class="fas fa-code-branch"></i> {sub}</span>'
    foot += '<span class="dz-pj-sp"></span>'
    if date:
        foot += f'<span class="dz-pj-date{" dz-pj-late" if late else ""}"><i class="far fa-calendar"></i> {date}</span>'
    cov = f'<div class="dz-pj-card-cover"><img src="https://picsum.photos/seed/{cover}/560/200" alt=""></div>' if cover else ""
    tags = f'<div class="dz-pj-card-tags">{lbls(*labels)}</div>' if labels else ""
    return (f'<a class="dz-pj-card{cls}" href="#">{cov}<div class="dz-pj-card-top"><span class="dz-pj-id">{id_}</span>'
            f'<span class="dz-pj-sp"></span>{av(who)}</div><p class="dz-pj-card-title">{title}</p>{tags}'
            f'<div class="dz-pj-card-foot">{foot}</div></a>')


def col(s, name, n, cards, wip=None):
    w = f'<span class="dz-pj-wip">{wip}</span>' if wip else ""
    return (f'<div class="dz-pj-col"><div class="dz-pj-colhead">{st(s)}<b>{name}</b><span class="dz-pj-count">{n}</span>{w}'
            f'<span class="dz-pj-sp"></span><a class="dz-pj-ibtn" href="#" aria-label="Ajouter"><i class="fas fa-plus"></i></a>'
            f'<a class="dz-pj-ibtn" href="#" aria-label="Options de colonne"><i class="fas fa-ellipsis-h"></i></a></div>'
            f'<div class="dz-pj-cards">{"".join(cards)}</div>'
            f'<a class="dz-pj-addcard" href="#"><i class="fas fa-plus"></i> Nouveau ticket</a></div>')


KANBAN = f"""
<div class="dz-pj-shell dz-pj-boardwrap">
  <div class="dz-pj-head">
    <span class="dz-pj-picon dz-pj-c2"><i class="fas fa-mobile-alt"></i></span>
    <h3 class="dz-pj-title">Application mobile 3.0</h3>
    <span class="dz-pj-lbl dz-pj-c1">Cycle 24</span>
    <span class="dz-pj-sp"></span>
    {avs("LM", "KB", "SM", "TG", more=3)}
    <a class="dz-pj-btn" href="#"><i class="fas fa-layer-group"></i> Grouper : statut</a>
    <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Ticket</a>
  </div>
  <div class="dz-pj-board">
    {col("backlog", "Backlog", 12, [
        card("ENG-156", "Mode lecture seule pour les comptes suspendus", ("Sécurité",), None, 1),
        card("ENG-154", "Raccourcis clavier dans l'éditeur de devis", ("Web",), "HF", 0, com=2),
    ])}
    {col("todo", "À faire", 4, [
        card("ENG-151", "Relance automatique des factures impayées", ("Client",), "IL", 3, com=4, date="22 sept.", late=True),
        card("ENG-149", "Thème sombre pour le tableau de bord analytique", ("Design",), "SM", 2, cover="palette", date="8 oct."),
    ])}
    {col("prog", "En cours", 3, [
        card("ENG-142", "Les brouillons hors ligne ne se synchronisent pas", ("Bug", "Mobile"), "LM", 4, com=7, sub="2/4", date="26 sept."),
        card("ENG-139", "Nouvel écran de paiement en une étape", ("Design", "Web"), "SM", 3, com=3, cls=" dz-pj-card-drag"),
        '<div class="dz-pj-drop"></div>',
        card("ENG-131", "Pagination par curseur sur l'API des commandes", ("API",), "KB", 2, sub="1/3"),
    ], wip="3 / 4")}
    {col("review", "En revue", 2, [
        card("ENG-128", "Réduire le temps de démarrage à froid", ("Perf", "Mobile"), "TG", 3, com=5, date="25 sept."),
        card("ENG-120", "Journal d'audit des changements de rôle", ("Sécurité",), "NO", 2, com=1),
    ])}
    {col("done", "Terminé", 9, [
        card("ENG-118", "Export CSV des équipes et des rôles", ("Web",), "JP", 2, cls=" dz-pj-card-done"),
        card("ENG-112", "Corriger l'arrondi des remises", ("Bug",), "KB", 1, cls=" dz-pj-card-done"),
    ])}
    <a class="dz-pj-col-new" href="#"><i class="fas fa-plus"></i><span>Ajouter une colonne</span></a>
  </div>
</div>
"""

# ------------------------------------------------------------------ 4. fiche ticket
ISSUE = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <div class="dz-pj-crumbs"><span class="dz-pj-picon dz-pj-c2"><i class="fas fa-mobile-alt"></i></span><a href="#">Application mobile 3.0</a><i class="fas fa-chevron-right"></i><span class="dz-pj-id">ENG-142</span></div>
    <span class="dz-pj-sp"></span>
    <span class="dz-pj-mute dz-pj-hide-sm">3 / 11</span>
    <a class="dz-pj-ibtn" href="#" aria-label="Ticket précédent"><i class="fas fa-chevron-up"></i></a>
    <a class="dz-pj-ibtn" href="#" aria-label="Ticket suivant"><i class="fas fa-chevron-down"></i></a>
    <span class="dz-pj-sep"></span>
    <a class="dz-pj-ibtn" href="#" aria-label="Copier le lien"><i class="fas fa-link"></i></a>
    <a class="dz-pj-ibtn" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a>
  </div>
  <div class="dz-pj-issue">
    <div class="dz-pj-issue-main">
      <h2 class="dz-pj-issue-title">Les brouillons hors ligne ne se synchronisent pas au retour du réseau</h2>
      <div class="dz-pj-prose">
        <p>Quand l'application repasse en ligne, les devis rédigés sans connexion restent en « brouillon local ». Reproduit sur iOS 19 et Android 16, uniquement si l'application a été mise en arrière-plan plus de <code>5 min</code>.</p>
        <ul><li>Attendu : synchronisation silencieuse, puis notification « 3 brouillons envoyés ».</li><li>Constaté : aucune requête sortante, file d'attente bloquée.</li></ul>
      </div>
      <div class="dz-pj-block">
        <div class="dz-pj-block-head"><b>Sous-tâches</b><span class="dz-pj-count">2 / 4</span><span class="dz-pj-sp"></span><span class="dz-pj-meter dz-pj-meter-sm" style="width:90px;--v:50%"><span></span></span></div>
        {row(3, "ENG-143", "done", "Tracer l'état de la file au réveil de l'app", (), "LM")}
        {row(3, "ENG-144", "done", "Écrire le test de bout en bout hors ligne", (), "TG")}
        {row(2, "ENG-145", "prog", "Relancer la file sur l'événement « réseau disponible »", (), "LM")}
        {row(1, "ENG-148", "todo", "Afficher un bandeau « envoi en cours »", (), "SM")}
      </div>
      <div class="dz-pj-section-t">Activité <span class="dz-pj-sp"></span><a class="dz-pj-btn" href="#"><i class="far fa-bell"></i> S'abonner</a></div>
      <div class="dz-pj-feed">
        <div class="dz-pj-ev"><span class="dz-pj-ev-ico"><i class="fas fa-plus"></i></span><span><b>Nadia Ouali</b> a créé le ticket depuis le support · 18 sept.</span></div>
        <div class="dz-pj-ev"><span class="dz-pj-ev-ico"><i class="fas fa-exclamation"></i></span><span><b>Karim Benali</b> a passé la priorité à <b>Urgente</b> · 19 sept.</span></div>
        <div class="dz-pj-comment">
          <div class="dz-pj-comment-head">{av("TG")}<b>Thomas Girard</b><span>il y a 3 h</span><span class="dz-pj-sp"></span><a class="dz-pj-ibtn" href="#" aria-label="Options"><i class="fas fa-ellipsis-h"></i></a></div>
          <p>Trouvé : le planificateur est suspendu par le système et on ne le réarme jamais. <span class="dz-pj-mention">@Léa</span> je te propose de brancher la relance sur l'écouteur réseau, c'est 20 lignes.</p>
          <div class="dz-pj-reacts"><span class="dz-pj-react dz-active">👍 3</span><span class="dz-pj-react">🎯 1</span><span class="dz-pj-react"><i class="far fa-smile"></i></span></div>
        </div>
        <div class="dz-pj-ev"><span class="dz-pj-ev-ico"><i class="fas fa-code-branch"></i></span><span><b>Léa Moreau</b> a lié la branche <b>lea/eng-142-relance</b> · il y a 1 h</span></div>
        <div class="dz-pj-composer"><span class="dz-pj-placeholder">Laisser un commentaire…</span><div class="dz-pj-composer-bar"><a class="dz-pj-ibtn" href="#" aria-label="Joindre"><i class="fas fa-paperclip"></i></a><a class="dz-pj-ibtn" href="#" aria-label="Mentionner"><i class="fas fa-at"></i></a><span class="dz-pj-sp"></span><a class="dz-pj-btn dz-pj-btn-primary" href="#">Commenter</a></div></div>
      </div>
    </div>
    <aside class="dz-pj-props">
      <div class="dz-pj-props-group">
        <div class="dz-pj-props-t">Propriétés</div>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Statut</span><span class="dz-pj-prop-v">{st("prog")} En cours</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Priorité</span><span class="dz-pj-prop-v">{pri(4)} Urgente</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Assigné</span><span class="dz-pj-prop-v">{av("LM")} Léa Moreau</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Étiquettes</span><span class="dz-pj-prop-v">{lbls("Bug", "Mobile")}</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Cycle</span><span class="dz-pj-prop-v"><i class="fas fa-sync-alt dz-pj-mute"></i> Cycle 24</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Estimation</span><span class="dz-pj-prop-v"><span class="dz-pj-est">5</span> points</span></a>
        <a class="dz-pj-prop" href="#"><span class="dz-pj-prop-k">Échéance</span><span class="dz-pj-prop-v dz-pj-soon"><i class="far fa-calendar"></i> 26 sept.</span></a>
      </div>
      <div class="dz-pj-props-group">
        <div class="dz-pj-props-t">Liens</div>
        <a class="dz-pj-linkcard" href="#"><i class="fas fa-code-branch"></i><div><b>#482 Relance de la file</b><small>Revue demandée · 2 vérifications OK</small></div></a>
      </div>
      <div class="dz-pj-props-group">
        <div class="dz-pj-props-t">Abonnés</div>
        <div class="dz-pj-prop">{avs("LM", "TG", "KB", "NO")}</div>
      </div>
    </aside>
  </div>
</div>
"""

# ------------------------------------------------------------------ 5. cycle en cours
BURN = """<svg viewBox="0 0 640 240" role="img" aria-label="Burndown du cycle 24">
<g class="dz-pj-svg-grid"><line x1="36" y1="20" x2="630" y2="20"/><line x1="36" y1="70" x2="630" y2="70"/><line x1="36" y1="120" x2="630" y2="120"/><line x1="36" y1="170" x2="630" y2="170"/><line x1="36" y1="210" x2="630" y2="210"/></g>
<g class="dz-pj-svg-axis"><text x="4" y="24">60</text><text x="4" y="74">45</text><text x="4" y="124">30</text><text x="4" y="174">15</text><text x="10" y="214">0</text>
<text x="36" y="232">15/09</text><text x="178" y="232">18/09</text><text x="320" y="232">22/09</text><text x="462" y="232">25/09</text><text x="590" y="232">28/09</text></g>
<path class="dz-pj-svg-scope" d="M36 63 H130 L130 43 H272 L272 36 H630"/>
<path class="dz-pj-svg-ideal" d="M36 63 L630 210"/>
<path class="dz-pj-svg-area" d="M36 210 L36 63 L83 66 L130 70 L177 83 L224 96 L272 103 L319 116 L366 130 L413 150 L413 210 Z"/>
<path class="dz-pj-svg-done" d="M36 63 L83 66 L130 70 L177 83 L224 96 L272 103 L319 116 L366 130 L413 150"/>
<path class="dz-pj-svg-start" d="M36 210 L83 196 L130 186 L177 176 L224 183 L272 170 L319 176 L366 163 L413 170"/>
<line class="dz-pj-svg-today" x1="413" y1="14" x2="413" y2="214"/>
<circle class="dz-pj-svg-dot" cx="413" cy="150" r="5"/>
</svg>"""


def who(ini, done, prog, pts):
    return (f'<div class="dz-pj-who">{av(ini, " dz-pj-av-md")}<b>{PEOPLE[ini][0]}</b><span class="dz-pj-pct">{pts}</span>'
            f'<div class="dz-pj-stack" style="grid-column:2 / -1;--_a:{done}%;--_b:{prog}%"><span class="dz-pj-s-done"></span><span class="dz-pj-s-prog"></span></div></div>')


CYCLE = f"""
<div class="dz-pj-shell dz-pj-cycle">
  <div class="dz-pj-head">
    <span class="dz-pj-picon dz-pj-c1"><i class="fas fa-sync-alt"></i></span>
    <div><h3 class="dz-pj-title">Cycle 24 · Hors ligne fiable</h3><span class="dz-pj-date">15 → 28 sept. 2026 · 2 semaines</span></div>
    <span class="dz-pj-sp"></span>
    <span class="dz-pj-health dz-pj-health-risk">4 jours restants</span>
    <a class="dz-pj-btn" href="#"><i class="fas fa-flag-checkered"></i> Clôturer</a>
  </div>
  <div class="dz-pj-cycle-kpis">
    <div class="dz-pj-kpi"><span class="dz-pj-kpi-k">{st("backlog")} Périmètre</span><span class="dz-pj-kpi-v">52 <small>points · +10 ajoutés</small></span></div>
    <div class="dz-pj-kpi"><span class="dz-pj-kpi-k">{st("prog")} Commencé</span><span class="dz-pj-kpi-v">16 <small>31 %</small></span></div>
    <div class="dz-pj-kpi"><span class="dz-pj-kpi-k">{st("done")} Terminé</span><span class="dz-pj-kpi-v">24 <small>46 %</small></span></div>
    <div class="dz-pj-kpi"><span class="dz-pj-kpi-k"><i class="fas fa-tachometer-alt"></i> Vélocité moyenne</span><span class="dz-pj-kpi-v">41 <small>pts / cycle</small></span></div>
  </div>
  <div class="dz-pj-cycle-body">
    <div class="dz-pj-chart">
      {BURN}
      <div class="dz-pj-legend"><span class="dz-pj-lg-scope">Périmètre</span><span>Restant</span><span class="dz-pj-lg-start">Commencé</span><span class="dz-pj-lg-ideal">Rythme idéal</span></div>
    </div>
    <div class="dz-pj-side">
      <div class="dz-pj-props-t" style="padding:0">Répartition par personne</div>
      {who("LM", 58, 24, "14 pts")}
      {who("TG", 70, 10, "11 pts")}
      {who("KB", 30, 45, "10 pts")}
      {who("SM", 40, 20, "9 pts")}
      {who("NO", 0, 60, "8 pts")}
      <div class="dz-pj-legend"><span>Terminé</span><span class="dz-pj-lg-start">En cours</span></div>
    </div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 6. feuille de route
def gweeks():
    days = ["7 sept.", "14 sept.", "21 sept.", "28 sept.", "5 oct.", "12 oct.", "19 oct.", "26 oct.", "2 nov.", "9 nov.", "16 nov.", "23 nov."]
    return "".join(f"<span><b>S{37 + i}</b>{d}</span>" for i, d in enumerate(days))


def grow(icon, c, name, lead, inner):
    return (f'<div class="dz-pj-grow"><div class="dz-pj-gname"><span class="dz-pj-picon dz-pj-c{c}"><i class="fas fa-{icon}"></i></span>'
            f'<span class="dz-pj-gname-t">{name}</span>{av(lead)}</div><div class="dz-pj-gtrack">{inner}</div></div>')


def gbar(a, b, c, label, v, pct):
    return f'<div class="dz-pj-gbar dz-pj-c{c}" style="grid-column:{a} / {b};--v:{v}%"><span>{label}</span><em>{pct}</em></div>'


ROADMAP = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Feuille de route · S2 2026</h3><span class="dz-pj-count">6 projets</span>
    <span class="dz-pj-sp"></span>
    <div class="dz-pj-seg"><a href="#" class="dz-active">Semaines</a><a href="#">Mois</a><a href="#">Trimestres</a></div>
    <a class="dz-pj-btn" href="#"><i class="far fa-dot-circle"></i> Aujourd'hui</a>
  </div>
  <div class="dz-pj-gantt">
    <div class="dz-pj-gantt-in" style="--_t:.29">
      <span class="dz-pj-today">24 SEPT.</span>
      <div class="dz-pj-grow dz-pj-ghead-row"><div class="dz-pj-gname">Projet</div><div class="dz-pj-gweeks">{gweeks()}</div></div>
      {grow("mobile-alt", 2, "Application mobile 3.0", "LM", gbar(1, 8, 2, "Hors ligne + paiement", 62, "62 %") + '<span class="dz-pj-gms" style="grid-column:9"></span><span class="dz-pj-gms-label" style="grid-column:10 / 13">Bêta publique</span>')}
      {grow("credit-card", 1, "Paiement en une étape", "SM", gbar(2, 6, 1, "Nouveau parcours", 45, "45 %") + '<span class="dz-pj-gms dz-pj-gms-risk" style="grid-column:6"></span>')}
      {grow("plug", 7, "API publique v2", "KB", gbar(1, 4, 7, "Cadrage", 100, "✓") + gbar(4, 11, 7, "Pagination, webhooks, SDK", 20, "20 %"))}
      {grow("shield-alt", 6, "Conformité RGPD 2026", "NO", gbar(3, 7, 6, "Audit + journalisation", 35, "35 %") + '<span class="dz-pj-gms" style="grid-column:8"></span><span class="dz-pj-gms-label" style="grid-column:9 / 12">Revue DPO</span>')}
      {grow("chart-line", 4, "Tableaux de bord 2.0", "TG", gbar(6, 13, 4, "Refonte des rapports", 0, "prévu"))}
      {grow("tachometer-alt", 5, "Performance web", "HF", gbar(1, 3, 5, "Mesure", 100, "✓") + '<span class="dz-pj-gms dz-pj-gms-done" style="grid-column:3"></span>' + gbar(4, 9, 5, "Découpage du bundle", 30, "30 %"))}
    </div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 7. backlog
def blrow(p, id_, s, title, labels, who, est):
    return (f'<a class="dz-pj-row dz-pj-row-bl" href="#"><i class="fas fa-grip-vertical dz-pj-grip"></i>{pri(p)}<span class="dz-pj-id">{id_}</span>'
            f'<span class="dz-pj-row-title">{title}</span><span class="dz-pj-row-meta"><span class="dz-pj-row-meta dz-pj-hide-sm">{lbls(*labels)}</span>'
            f'<span class="dz-pj-est">{est}</span>{av(who)}</span></a>')


BACKLOG = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Backlog</h3><span class="dz-pj-count">38</span>
    <span class="dz-pj-sp"></span>
    <a class="dz-pj-btn" href="#"><i class="fas fa-sort-amount-down"></i> Trier : priorité</a>
    <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Ticket</a>
  </div>
  <div class="dz-pj-toolbar">
    <div class="dz-chips">
      <a class="dz-chip dz-active" href="#">Tous</a>
      <a class="dz-chip" href="#"><span class="dz-pj-pri dz-pj-pri-4"></span> Urgents</a>
      <a class="dz-chip" href="#">Mes tickets</a>
      <a class="dz-chip" href="#"><span class="dz-pj-lbl dz-pj-c6" style="height:auto;padding:0;border:0;background:none">Bug</span> <i class="fas fa-times dz-pj-chip-x"></i></a>
      <a class="dz-chip" href="#"><i class="fas fa-plus"></i> Filtre</a>
    </div>
  </div>
  <div class="dz-pj-group">
    <div class="dz-pj-ghead"><i class="fas fa-sync-alt dz-pj-mute"></i><b>Cycle 25 · prochain</b><span class="dz-pj-count">5</span>
      <div class="dz-pj-cap"><span class="dz-pj-hide-sm">31 / 34 pts</span><span class="dz-pj-meter dz-pj-meter-sm dz-pj-hide-sm" style="--v:91%"><span></span></span></div></div>
    {blrow(4, "ENG-151", "todo", "Relance automatique des factures impayées", ("Client",), "IL", 5)}
    {blrow(3, "ENG-156", "todo", "Mode lecture seule pour les comptes suspendus", ("Sécurité",), "NO", 8)}
    {blrow(3, "ENG-149", "todo", "Thème sombre pour le tableau de bord analytique", ("Design",), "SM", 5)}
    {blrow(2, "ENG-153", "todo", "Import de contacts depuis un fichier tableur", ("Web", "Client"), "JP", 8)}
    {blrow(2, "ENG-147", "todo", "Mettre à jour la bibliothèque de graphiques", ("Dette",), "HF", 5)}
  </div>
  <div class="dz-pj-group">
    <div class="dz-pj-ghead">{st("backlog")}<b>Backlog</b><span class="dz-pj-count">33</span><span class="dz-pj-sp"></span><span class="dz-pj-mute dz-pj-hide-sm">Glisser un ticket vers un cycle</span></div>
    {blrow(2, "ENG-154", "backlog", "Raccourcis clavier dans l'éditeur de devis", ("Web",), "HF", 3)}
    {blrow(1, "ENG-146", "backlog", "Documenter les webhooks sortants", ("API",), "KB", 2)}
    {blrow(1, "ENG-158", "backlog", "Nettoyer les drapeaux de fonctionnalités expirés", ("Dette",), "TG", 3)}
    {blrow(0, "ENG-160", "backlog", "Étudier la signature électronique des devis", ("Client",), "LM", 13)}
  </div>
</div>
"""


# ------------------------------------------------------------------ 8. objectifs (OKR)
def kr(n, t, sub, v, cur, c=1):
    return (f'<div class="dz-pj-kr"><span class="dz-pj-kr-n">KR{n}</span><div class="dz-pj-kr-t">{t}<small>{sub}</small></div>'
            f'<div class="dz-pj-kr-v"><span><span>{cur}</span><span>{v} %</span></span><div class="dz-pj-meter dz-pj-c{c}" style="--v:{v}%"><span></span></div></div></div>')


def okr(title, owner, v, health, hcls, krs, c=1):
    return (f'<div class="dz-pj-shell dz-pj-okr"><div class="dz-pj-okr-head"><div class="dz-pj-ring dz-pj-c{c}" style="--v:{v}">{v}%</div>'
            f'<div><h3>{title}</h3><div class="dz-pj-okr-meta">{av(owner)}<span>{PEOPLE[owner][0]}</span><span>·</span><span>T4 2026</span></div></div>'
            f'<span class="dz-pj-health{hcls}">{health}</span></div><div class="dz-pj-krs">{"".join(krs)}</div></div>')


OKR = f"""
<div class="dz-page-head"><div><span class="dz-eyebrow">Objectifs · T4 2026</span><h2 class="dz-h3">Ce qui compte ce trimestre</h2></div>
  <div class="dz-pj-summary"><span><span class="dz-pj-dot"></span><b>5</b> en bonne voie</span><span><span class="dz-pj-dot" style="--_c:var(--dz-warning)"></span><b>2</b> à risque</span><span><span class="dz-pj-dot" style="--_c:var(--dz-danger)"></span><b>1</b> en retard</span></div></div>
<div class="dz-pj-okrs">
  {okr("Rendre l'application mobile fiable hors ligne", "LM", 68, "En bonne voie", "", [
      kr(1, "Taux de synchronisation réussie", "Mesuré sur 7 jours glissants", 82, "97,4 % / 99,5 %", 1),
      kr(2, "Crashs par millier de sessions", "De 4,1 à moins de 1,0", 71, "1,9 / 1,0", 1),
      kr(3, "Note moyenne sur les magasins", "De 4,2 à 4,6", 50, "4,4 / 4,6", 1),
  ], 1)}
  {okr("Doubler l'adoption de l'API publique", "KB", 34, "À risque", " dz-pj-health-risk", [
      kr(1, "Intégrations actives", "Clients ayant fait au moins 100 appels", 42, "126 / 300", 5),
      kr(2, "Temps jusqu'au premier appel", "Documentation, clés, SDK", 30, "18 min / 5 min", 5),
      kr(3, "Tickets de support API", "Réduire de moitié", 28, "−14 % / −50 %", 5),
  ], 5)}
</div>
"""


# ------------------------------------------------------------------ 9. jalons
def mile(cls, date, title, text, v, tix):
    return (f'<div class="dz-pj-mile{cls}"><span class="dz-pj-mile-dia"></span><span class="dz-pj-mile-date">{date}</span><h4>{title}</h4><p>{text}</p>'
            f'<div class="dz-pj-mile-foot"><div class="dz-pj-meter dz-pj-meter-sm" style="--v:{v}%"><span></span></div><span class="dz-pj-pct">{tix}</span></div></div>')


MILESTONES = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Jalons · Application mobile 3.0</h3>
    <span class="dz-pj-sp"></span>
    <span class="dz-pj-health">Livraison prévue le 18 déc.</span>
    <a class="dz-pj-btn" href="#"><i class="fas fa-plus"></i> Jalon</a>
  </div>
  <div class="dz-pj-miles">
    {mile(" dz-pj-mile-done", "12 sept.", "Cadrage validé", "Périmètre, maquettes et plan de tests signés.", 100, "9 / 9")}
    {mile(" dz-pj-mile-now", "3 oct.", "Hors ligne fiable", "Brouillons, file d'envoi, reprise sur erreur.", 64, "14 / 22")}
    {mile(" dz-pj-mile-risk", "31 oct.", "Paiement en une étape", "Nouveau parcours, 3-D Secure, reçus.", 20, "4 / 19")}
    {mile("", "21 nov.", "Bêta publique", "2 000 testeurs, retours intégrés en continu.", 0, "0 / 12")}
    {mile("", "18 déc.", "Lancement 3.0", "Publication sur les magasins et annonce.", 0, "0 / 8")}
  </div>
</div>
"""


# ------------------------------------------------------------------ 10. charge de l'équipe
def hrow(ini, role, cells, tot, cap):
    out = f'<div class="dz-pj-hrow"><div class="dz-pj-hwho">{av(ini, " dz-pj-av-md")}<div><b>{PEOPLE[ini][0]}</b><small>{role}</small></div></div>'
    for c in cells:
        if c == "off":
            out += '<span class="dz-pj-hc dz-pj-hoff">congé</span>'
        else:
            h = int(c)
            k = "dz-pj-hover" if h > 40 else "dz-pj-h4" if h >= 34 else "dz-pj-h3" if h >= 26 else "dz-pj-h2" if h >= 16 else "dz-pj-h1"
            out += f'<span class="dz-pj-hc {k}">{h} h</span>'
    return out + f'<div class="dz-pj-htot">{tot}<small>{cap}</small></div></div>'


WORKLOAD = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Charge de l'équipe</h3><span class="dz-pj-count">6 personnes</span>
    <span class="dz-pj-sp"></span>
    <div class="dz-pj-hscale dz-pj-hide-sm"><span>Faible</span><span class="dz-pj-hc dz-pj-h1"></span><span class="dz-pj-hc dz-pj-h2"></span><span class="dz-pj-hc dz-pj-h3"></span><span class="dz-pj-hc dz-pj-h4"></span><span class="dz-pj-hc dz-pj-hover"></span><span>Surcharge</span></div>
    <a class="dz-pj-btn" href="#"><i class="fas fa-random"></i> Rééquilibrer</a>
  </div>
  <div class="dz-pj-heat"><div class="dz-pj-heat-in">
    <div class="dz-pj-hrow dz-pj-hrow-head"><span>Personne</span><span>S39 · 21/09</span><span>S40 · 28/09</span><span>S41 · 05/10</span><span>S42 · 12/10</span><span>S43 · 19/10</span><span>S44 · 26/10</span><span style="text-align:right">Total</span></div>
    {hrow("LM", "Mobile", [38, 42, 36, 30, 24, 12], "182 h", "95 % de 192 h")}
    {hrow("KB", "API", [30, 34, 38, 44, 36, 20], "202 h", "105 % · surcharge")}
    {hrow("SM", "Design", [28, "off", "off", 32, 30, 26], "116 h", "91 % de 128 h")}
    {hrow("TG", "Mobile", [36, 32, 20, 18, 14, 8], "128 h", "67 % · disponible")}
    {hrow("NO", "Sécurité", [22, 26, 30, 36, 38, 34], "186 h", "97 % de 192 h")}
    {hrow("HF", "Web", [12, 16, 24, 28, 30, 34], "144 h", "75 % de 192 h")}
  </div></div>
</div>
"""


# ------------------------------------------------------------------ 11. mes tâches
def task(title, proj, c, due, cls="", p=2, id_="ENG-151", done=False):
    chk = '<span class="dz-pj-check dz-pj-check-done"></span>' if done else '<span class="dz-pj-check"></span>'
    return (f'<a class="dz-pj-task{" dz-pj-task-done" if done else ""}" href="#">{chk}<div class="dz-pj-task-t"><b>{title}</b>'
            f'<small><span class="dz-pj-id">{id_}</span><span class="dz-pj-tag dz-pj-c{c}">{proj}</span></small></div>'
            f'<span class="dz-pj-row-meta">{pri(p)}<span class="dz-pj-date{cls}">{due}</span></span></a>')


MYTASKS = f"""
<div class="dz-pj-my">
  <div class="dz-pj-shell">
    <div class="dz-pj-head">
      {av("LM", " dz-pj-av-md")}<h3 class="dz-pj-title">Mes tâches</h3><span class="dz-pj-count">9</span>
      <span class="dz-pj-sp"></span>
      <div class="dz-pj-seg"><a href="#" class="dz-active">Liste</a><a href="#">Semaine</a></div>
    </div>
    <div class="dz-pj-sec dz-pj-sec-late"><i class="fas fa-exclamation-circle"></i> En retard <span class="dz-pj-count">2</span></div>
    {task("Relancer les factures impayées de septembre", "Finance", 5, "hier", " dz-pj-late", 3, "ENG-151")}
    {task("Valider les maquettes de l'écran de paiement", "Paiement", 1, "22 sept.", " dz-pj-late", 2, "ENG-139")}
    <div class="dz-pj-sec"><i class="far fa-sun dz-pj-mute"></i> Aujourd'hui <span class="dz-pj-count">3</span></div>
    {task("Corriger la synchronisation des brouillons hors ligne", "Mobile 3.0", 2, "aujourd'hui", " dz-pj-soon", 4, "ENG-142")}
    {task("Relire la PR #482 de Thomas", "Mobile 3.0", 2, "16:00", "", 2, "ENG-145")}
    {task("Préparer la démo du cycle 24", "Mobile 3.0", 2, "fait", "", 1, "ENG-150", done=True)}
    <div class="dz-pj-sec"><i class="far fa-calendar-alt dz-pj-mute"></i> Cette semaine <span class="dz-pj-count">4</span></div>
    {task("Écrire la note de cadrage de la bêta publique", "Mobile 3.0", 2, "ven. 26", "", 2, "ENG-157")}
    {task("Entretien avec le client Atelier Lune", "Clients", 4, "ven. 26", "", 1, "OPS-38")}
    {task("Mettre à jour la feuille de route T4", "Produit", 3, "dim. 27", "", 0, "PRD-12")}
  </div>
  <div class="dz-pj-shell dz-pj-focus">
    <div class="dz-pj-props-t" style="padding:0">Ma semaine</div>
    <div class="dz-pj-bigstat"><b>12</b><span class="dz-pj-mute">tickets terminés · +4 vs S38</span></div>
    <div><div class="dz-pj-days"><span style="--h:45%"></span><span style="--h:70%"></span><span style="--h:55%"></span><span class="dz-active" style="--h:90%"></span><span style="--h:8%"></span><span style="--h:4%"></span><span style="--h:4%"></span></div>
    <div class="dz-pj-dayl" style="margin-top:.4rem"><span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span></div></div>
    <div class="dz-pj-props-group">
      <div class="dz-pj-prop"><span class="dz-pj-prop-k">Points faits</span><span class="dz-pj-prop-v">23 / 30</span></div>
      <div class="dz-pj-prop"><span class="dz-pj-prop-k">En revue</span><span class="dz-pj-prop-v">{st("review")} 2 tickets</span></div>
      <div class="dz-pj-prop"><span class="dz-pj-prop-k">Mentions</span><span class="dz-pj-prop-v">5 non lues</span></div>
    </div>
    <a class="dz-pj-btn" href="#" style="justify-content:center"><i class="fas fa-bullseye"></i> Mode concentration</a>
  </div>
</div>
"""


# ------------------------------------------------------------------ 12. portefeuille de projets
def prow(icon, c, name, desc, health, hcls, v, lead, date, tix):
    return (f'<a class="dz-pj-prow" href="#"><div class="dz-pj-pname"><span class="dz-pj-picon dz-pj-c{c}"><i class="fas fa-{icon}"></i></span>'
            f'<div><b>{name}</b><small>{desc}</small></div></div><span><span class="dz-pj-health{hcls}">{health}</span></span>'
            f'<div class="dz-pj-pprog"><div class="dz-pj-meter dz-pj-c{c}" style="--v:{v}%"><span></span></div><span class="dz-pj-pct">{v} %</span></div>'
            f'<span class="dz-pj-p-lead">{av(lead)}</span><span class="dz-pj-date dz-pj-p-date">{date}</span><span class="dz-pj-p-tix dz-pj-pct">{tix}</span></a>')


PORTFOLIO = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Projets</h3><span class="dz-pj-count">6</span>
    <div class="dz-pj-summary dz-pj-hide-sm" style="margin-left:.5rem"><span><span class="dz-pj-dot"></span><b>3</b> en bonne voie</span><span><span class="dz-pj-dot" style="--_c:var(--dz-warning)"></span><b>2</b> à risque</span><span><span class="dz-pj-dot" style="--_c:var(--dz-danger)"></span><b>1</b> en retard</span></div>
    <span class="dz-pj-sp"></span>
    <a class="dz-pj-btn" href="#"><i class="fas fa-filter"></i> Actifs</a>
    <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Projet</a>
  </div>
  <div class="dz-pj-prow dz-pj-prow-head"><span>Nom</span><span>Santé</span><span>Avancement</span><span>Pilote</span><span>Date cible</span><span>Tickets</span></div>
  {prow("mobile-alt", 2, "Application mobile 3.0", "Hors ligne, paiement, bêta", "En bonne voie", "", 64, "LM", "18 déc.", "31 / 48")}
  {prow("credit-card", 1, "Paiement en une étape", "Nouveau parcours d'achat", "À risque", " dz-pj-health-risk", 38, "SM", "31 oct.", "7 / 19")}
  {prow("plug", 7, "API publique v2", "Pagination, webhooks, SDK", "En bonne voie", "", 45, "KB", "20 nov.", "18 / 40")}
  {prow("shield-alt", 6, "Conformité RGPD 2026", "Audit, journal, rétention", "En retard", " dz-pj-health-late", 29, "NO", "15 oct.", "6 / 21")}
  {prow("tachometer-alt", 5, "Performance web", "Temps de chargement < 1,5 s", "À risque", " dz-pj-health-risk", 52, "HF", "6 nov.", "11 / 21")}
  {prow("chart-line", 4, "Tableaux de bord 2.0", "Rapports personnalisables", "En bonne voie", "", 12, "TG", "19 déc.", "3 / 26")}
</div>
"""

# ------------------------------------------------------------------ 13. actions rapides
PALETTE = f"""
<div class="dz-pj-shell dz-pj-palette">
  <div class="dz-pj-pal-ctx"><span class="dz-pj-tag dz-pj-c2"><b class="dz-pj-id">ENG-142</b><span>Les brouillons hors ligne ne se synchronisent pas</span></span></div>
  <div class="dz-pj-pal-input"><i class="fas fa-search"></i><span class="dz-pj-pal-q">stat</span><span class="dz-pj-caret"></span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">Échap</span></div>
  <div class="dz-pj-pal-list">
    <div class="dz-pj-pal-group">Changer le statut</div>
    <a class="dz-pj-pal-item" href="#">{st("backlog")}<span>Backlog</span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">1</span></a>
    <a class="dz-pj-pal-item" href="#">{st("todo")}<span>À faire</span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">2</span></a>
    <a class="dz-pj-pal-item" href="#">{st("prog")}<span>En cours</span><span class="dz-pj-pal-hint">actuel</span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">3</span></a>
    <a class="dz-pj-pal-item dz-active" href="#">{st("review")}<span>En revue</span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">4</span></a>
    <a class="dz-pj-pal-item" href="#">{st("done")}<span>Terminé</span><span class="dz-pj-sp"></span><span class="dz-pj-kbd">5</span></a>
    <div class="dz-pj-pal-group">Actions</div>
    <a class="dz-pj-pal-item" href="#"><i class="fas fa-user"></i><span>Assigner à…</span><span class="dz-pj-sp"></span><span class="dz-pj-pal-keys"><span class="dz-pj-kbd">A</span></span></a>
    <a class="dz-pj-pal-item" href="#"><i class="fas fa-signal"></i><span>Changer la priorité</span><span class="dz-pj-sp"></span><span class="dz-pj-pal-keys"><span class="dz-pj-kbd">P</span></span></a>
    <a class="dz-pj-pal-item" href="#"><i class="fas fa-tag"></i><span>Ajouter une étiquette</span><span class="dz-pj-sp"></span><span class="dz-pj-pal-keys"><span class="dz-pj-kbd">L</span></span></a>
    <a class="dz-pj-pal-item" href="#"><i class="fas fa-sync-alt"></i><span>Déplacer vers le cycle 25</span><span class="dz-pj-sp"></span><span class="dz-pj-pal-keys"><span class="dz-pj-kbd">⇧</span><span class="dz-pj-kbd">C</span></span></a>
    <a class="dz-pj-pal-item" href="#"><i class="fas fa-link"></i><span>Copier le lien du ticket</span><span class="dz-pj-sp"></span><span class="dz-pj-pal-keys"><span class="dz-pj-kbd">Ctrl</span><span class="dz-pj-kbd">⇧</span><span class="dz-pj-kbd">,</span></span></a>
  </div>
  <div class="dz-pj-pal-foot"><span><span class="dz-pj-kbd">↑</span><span class="dz-pj-kbd">↓</span> naviguer</span><span><span class="dz-pj-kbd">↵</span> valider</span><span><span class="dz-pj-kbd">Tab</span> sous-menu</span><span class="dz-pj-sp"></span><span>10 actions</span></div>
</div>
"""

# ------------------------------------------------------------------ 14. wiki de projet
WIKI = f"""
<div class="dz-pj-shell dz-pj-wiki">
  <nav class="dz-pj-tree">
    <div class="dz-pj-tree-t">Application mobile 3.0</div>
    <a class="dz-pj-tree-i" href="#"><i class="far fa-compass"></i> Vue d'ensemble</a>
    <a class="dz-pj-tree-i dz-active" href="#"><i class="far fa-file-alt"></i> Spécification hors ligne</a>
    <a class="dz-pj-tree-i dz-pj-tree-sub" href="#"><i class="far fa-file"></i> File d'envoi</a>
    <a class="dz-pj-tree-i dz-pj-tree-sub" href="#"><i class="far fa-file"></i> Résolution de conflits</a>
    <a class="dz-pj-tree-i" href="#"><i class="far fa-file-alt"></i> Parcours de paiement</a>
    <a class="dz-pj-tree-i" href="#"><i class="fas fa-vial"></i> Plan de tests</a>
    <a class="dz-pj-tree-i" href="#"><i class="far fa-clipboard"></i> Comptes rendus</a>
    <div class="dz-pj-tree-t">Équipe</div>
    <a class="dz-pj-tree-i" href="#"><i class="fas fa-book"></i> Conventions de code</a>
    <a class="dz-pj-tree-i" href="#"><i class="fas fa-rocket"></i> Procédure de mise en production</a>
    <a class="dz-pj-tree-i" href="#"><i class="fas fa-plus"></i> Nouvelle page</a>
  </nav>
  <article class="dz-pj-doc">
    <div class="dz-pj-crumbs" style="margin-bottom:1.2rem"><a href="#">Docs</a><i class="fas fa-chevron-right"></i><span>Spécification hors ligne</span></div>
    <div class="dz-pj-doc-emoji"><i class="fas fa-wifi"></i></div>
    <h2>Spécification : mode hors ligne</h2>
    <div class="dz-pj-doc-meta"><span>{avs("LM", "TG")} Léa Moreau, Thomas Girard</span><span><i class="far fa-clock"></i> Modifié il y a 2 h</span><span class="dz-pj-lbl dz-pj-c4">Validé</span><span><i class="far fa-eye"></i> 34 lectures</span></div>
    <p>L'application doit rester entièrement utilisable sans réseau pendant au moins 72 heures. Toute action est enregistrée localement puis rejouée dans l'ordre dès que la connexion revient.</p>
    <div class="dz-pj-note"><i class="fas fa-info-circle"></i><span><b>Décision du 16 sept.</b> — en cas de conflit, la dernière modification l'emporte champ par champ ; l'historique garde les deux versions.</span></div>
    <h3>Objectifs</h3>
    <div class="dz-pj-todo">
      <div><span class="dz-pj-box dz-pj-box-on"></span><span>Création et modification de devis sans réseau</span></div>
      <div><span class="dz-pj-box dz-pj-box-on"></span><span>File d'envoi persistante, chiffrée sur l'appareil</span></div>
      <div><span class="dz-pj-box"></span><span>Reprise automatique au retour du réseau (ENG-142)</span></div>
    </div>
    <h3>Format d'une action en file</h3>
    <pre class="dz-pj-code">{{
  <b>"id"</b>: "act_8f2c",
  <b>"type"</b>: "devis.update",
  <b>"cree_le"</b>: "2026-09-24T09:12:05Z",
  <b>"tentatives"</b>: 0
}}</pre>
    <p>Chaque action porte un identifiant unique : le serveur ignore les doublons, ce qui rend la relance sans risque.</p>
  </article>
  <nav class="dz-pj-toc">
    <div class="dz-pj-tree-t" style="padding-left:.6rem">Sur cette page</div>
    <a href="#">Introduction</a>
    <a href="#" class="dz-active">Objectifs</a>
    <a href="#">Format d'une action</a>
    <a href="#" class="dz-pj-toc-sub">Identifiant unique</a>
    <a href="#" class="dz-pj-toc-sub">Tentatives</a>
    <a href="#">Conflits</a>
  </nav>
</div>
"""


# ------------------------------------------------------------------ 15. mises à jour de projet
def post(who, when, health, hcls, title, body, reacts, comments):
    rs = "".join(f'<span class="dz-pj-react{" dz-active" if i == 0 else ""}">{r}</span>' for i, r in enumerate(reacts))
    return (f'<div class="dz-pj-shell dz-pj-post"><div class="dz-pj-post-head"><div class="dz-pj-post-who">{av(who, " dz-pj-av-lg")}'
            f'<span><b>{PEOPLE[who][0]}</b> a publié une mise à jour · {when}</span></div><span class="dz-pj-health{hcls}">{health}</span></div>'
            f'<div class="dz-pj-post-body"><h4>{title}</h4>{body}</div>'
            f'<div class="dz-pj-post-foot"><div class="dz-pj-reacts">{rs}</div><span class="dz-pj-sp"></span>'
            f'<span><i class="far fa-comment"></i> {comments} commentaires</span></div></div>')


UPDATES = f"""
<div class="dz-pj-updates">
  <div class="dz-pj-shell">
    <div class="dz-pj-head"><h3 class="dz-pj-title">Mises à jour du projet</h3><span class="dz-pj-sp"></span><span class="dz-pj-date"><i class="far fa-bell"></i> Rappel chaque vendredi</span></div>
    <div class="dz-pj-composer" style="margin:1rem 1.15rem;border-style:dashed">
      <span class="dz-pj-placeholder">Comment avance le projet cette semaine ?</span>
      <div class="dz-pj-composer-bar" style="flex-wrap:wrap;gap:.5rem"><div class="dz-pj-seg"><a href="#" class="dz-active"><span class="dz-pj-dot"></span> En bonne voie</a><a href="#"><span class="dz-pj-dot" style="--_c:var(--dz-warning)"></span> À risque</a><a href="#"><span class="dz-pj-dot" style="--_c:var(--dz-danger)"></span> En retard</a></div><span class="dz-pj-sp"></span><a class="dz-pj-btn dz-pj-btn-primary" href="#">Publier</a></div>
    </div>
  </div>
  {post("LM", "aujourd'hui, 9:40", "En bonne voie", "", "Semaine 39 : le hors ligne tient la route",
        "<p>La relance de la file est corrigée (ENG-142) et passe les 48 scénarios de test. Le taux de synchronisation remonte à <b>97,4 %</b>.</p><ul><li>Terminé : 9 tickets, 24 points</li><li>Prochaine étape : bêta interne lundi 28 sept.</li><li>Besoin : 2 testeurs Android supplémentaires</li></ul>",
        ["👏 6", "🚀 3", "👀 1"], 4)}
  {post("SM", "18 sept.", "À risque", " dz-pj-health-risk", "Paiement : dépendance au prestataire bancaire",
        "<p>Le bac à sable 3-D Secure du prestataire est instable depuis mardi. On garde la date du 31 oct. si l'accès est rétabli avant le 2 oct. ; sinon, glissement d'une semaine.</p>",
        ["🙏 4", "👍 2"], 7)}
</div>
"""


# ------------------------------------------------------------------ 16. calendrier des échéances
def cal_chip(id_, t, c, ms=False):
    icon = '<i class="fas fa-flag"></i>' if ms else f"<b>{id_}</b>"
    return f'<a class="dz-pj-ev-chip dz-pj-c{c}{" dz-pj-ev-ms" if ms else ""}" href="#">{icon}<span>{t}</span></a>'


EVENTS = {
    1: [cal_chip("ENG-112", "Arrondi des remises", 4)],
    4: [cal_chip("ENG-118", "Export CSV équipes", 4)],
    8: [cal_chip("ENG-109", "Refonte des e-mails", 7)],
    11: [cal_chip("", "Cadrage validé", 3, True)],
    15: [cal_chip("ENG-131", "Début du cycle 24", 1)],
    17: [cal_chip("ENG-120", "Journal d'audit", 7)],
    22: [cal_chip("ENG-151", "Relance factures", 6), cal_chip("ENG-139", "Maquettes paiement", 6)],
    24: [cal_chip("ENG-145", "Relance de la file", 5)],
    25: [cal_chip("ENG-128", "Démarrage à froid", 1), cal_chip("ENG-144", "Test hors ligne", 1), '<span class="dz-pj-ev-more">+2 autres</span>'],
    26: [cal_chip("ENG-142", "Brouillons hors ligne", 5)],
    28: [cal_chip("", "Fin du cycle 24", 3, True)],
    30: [cal_chip("ENG-139", "Paiement en une étape", 1)],
}


def calendar():
    out = "".join(f'<div class="dz-pj-cal-dow">{d}</div>' for d in ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])
    cells = [(31, "out")] + [(d, "") for d in range(1, 31)] + [(d, "out") for d in range(1, 5)]
    for i, (d, k) in enumerate(cells):
        cls = "dz-pj-day"
        if k == "out":
            cls += " dz-pj-day-out"
        elif i % 7 >= 5:
            cls += " dz-pj-day-we"
        if k == "" and d == 24:
            cls += " dz-pj-day-today"
        evs = "".join(EVENTS.get(d, [])) if k == "" else ""
        out += f'<div class="{cls}"><span class="dz-pj-day-n">{d}</span>{evs}</div>'
    return out


CALENDAR = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Septembre 2026</h3>
    <a class="dz-pj-ibtn" href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a>
    <a class="dz-pj-ibtn" href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a>
    <a class="dz-pj-btn" href="#">Aujourd'hui</a>
    <span class="dz-pj-sp"></span>
    <div class="dz-pj-legend dz-pj-hide-sm" style="margin:0"><span style="--_c:var(--dz-danger)">En retard</span><span style="--_c:var(--dz-warning)">Cette semaine</span><span style="--_c:var(--dz-primary)">À venir</span><span style="--_c:var(--dz-accent-2)">Jalon</span></div>
    <div class="dz-pj-seg"><a href="#" class="dz-active">Mois</a><a href="#">Semaine</a></div>
  </div>
  <div class="dz-pj-cal">{calendar()}</div>
</div>
"""

# ------------------------------------------------------------------ 17. création rapide
CREATE = f"""
<div class="dz-pj-shell dz-pj-create">
  <div class="dz-pj-create-top"><span class="dz-pj-tag dz-pj-c2"><i class="fas fa-mobile-alt"></i> ENG</span><i class="fas fa-chevron-right" style="font-size:.6rem"></i><span>Nouveau ticket</span><span class="dz-pj-sp"></span>
    <a class="dz-pj-ibtn" href="#" aria-label="Agrandir"><i class="fas fa-expand-alt"></i></a><a class="dz-pj-ibtn" href="#" aria-label="Fermer"><i class="fas fa-times"></i></a></div>
  <div class="dz-pj-create-body">
    <div class="dz-pj-create-title">Afficher le nombre de brouillons en attente<span class="dz-pj-caret"></span></div>
    <div class="dz-pj-create-desc">Ajouter une description, des captures, ou taper <span class="dz-pj-kbd">/</span> pour les modèles…</div>
  </div>
  <div class="dz-pj-pills">
    <a class="dz-pj-pill" href="#">{st("todo")} À faire</a>
    <a class="dz-pj-pill" href="#">{pri(3)} Haute</a>
    <a class="dz-pj-pill" href="#">{av("SM")} Sofia</a>
    <a class="dz-pj-pill" href="#"><span class="dz-pj-lbl dz-pj-c2" style="height:auto;padding:0;border:0;background:none">Mobile</span></a>
    <a class="dz-pj-pill" href="#"><i class="fas fa-sync-alt"></i> Cycle 25</a>
    <a class="dz-pj-pill dz-pj-pill-ghost" href="#"><i class="far fa-calendar"></i> Échéance</a>
    <a class="dz-pj-pill dz-pj-pill-ghost" href="#"><i class="fas fa-ellipsis-h"></i></a>
  </div>
  <div class="dz-pj-attach"><i class="fas fa-paperclip"></i><span>Glisser des fichiers ici ou <b>parcourir</b></span></div>
  <div class="dz-pj-create-foot">
    <span class="dz-pj-toggle"><span></span><span>Créer d'autres tickets</span></span>
    <span class="dz-pj-sp"></span>
    <a class="dz-pj-btn" href="#">Annuler</a>
    <a class="dz-pj-btn dz-pj-btn-primary" href="#">Créer le ticket <span class="dz-pj-kbd" style="background:transparent;border-color:currentColor;color:inherit">Ctrl ↵</span></a>
  </div>
</div>
"""

# ------------------------------------------------------------------ 18. état vide
EMPTY = """
<div class="dz-pj-shell dz-pj-empty">
  <div class="dz-pj-illu">
    <div class="dz-pj-illu-1"><div class="dz-pj-illu-row"><span class="dz-pj-st"></span><span class="dz-pj-line"></span></div><span class="dz-pj-line dz-pj-line-s"></span></div>
    <div class="dz-pj-illu-2"><div class="dz-pj-illu-row"><span class="dz-pj-st dz-pj-st-prog"></span><span class="dz-pj-line"></span></div><span class="dz-pj-line dz-pj-line-s"></span></div>
    <div class="dz-pj-illu-3"><div class="dz-pj-illu-row"><span class="dz-pj-st dz-pj-st-done"></span><span class="dz-pj-line dz-pj-line-p"></span></div><div class="dz-pj-illu-row"><span class="dz-pj-line dz-pj-line-s"></span><span class="dz-pj-sp"></span><span class="dz-pj-av dz-pj-c1">LM</span></div></div>
  </div>
  <h3>Aucun ticket dans ce cycle</h3>
  <p>Planifiez le cycle 25 en y glissant des tickets du backlog, ou créez-en un nouveau. Les tickets non terminés du cycle précédent seront reportés automatiquement.</p>
  <div class="dz-cluster" style="justify-content:center;--dz-gap:.5rem">
    <a class="dz-pj-btn dz-pj-btn-primary" href="#"><i class="fas fa-plus"></i> Créer un ticket</a>
    <a class="dz-pj-btn" href="#"><i class="fas fa-inbox"></i> Ouvrir le backlog</a>
  </div>
  <div class="dz-pj-empty-keys"><span>ou appuyez sur</span><span class="dz-pj-kbd">C</span><span>pour créer,</span><span class="dz-pj-kbd">Ctrl</span><span class="dz-pj-kbd">K</span><span>pour les commandes</span></div>
</div>
"""


# ------------------------------------------------------------------ 19. graphe de dépendances
def node(x, y, id_, s, title, who, cls="", flag=""):
    f = f'<span class="dz-pj-flag"><i class="fas fa-ban"></i> {flag}</span>' if flag else ""
    return (f'<a class="dz-pj-node{cls}" href="#" style="left:{x}px;top:{y}px"><div class="dz-pj-node-top">{st(s)}<span class="dz-pj-id">{id_}</span>'
            f'<span class="dz-pj-sp"></span>{av(who)}</div><span class="dz-pj-node-t">{title}</span>{f}</a>')


DEPS_SVG = """<svg viewBox="0 0 900 360" aria-hidden="true">
<defs><marker id="dzpjA" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path class="dz-pj-svg-head" d="M0 0 L8 4 L0 8 z"/></marker>
<marker id="dzpjB" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path class="dz-pj-svg-head-hot" d="M0 0 L8 4 L0 8 z"/></marker>
<marker id="dzpjC" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path class="dz-pj-svg-head-block" d="M0 0 L8 4 L0 8 z"/></marker></defs>
<path class="dz-pj-svg-edge-hot" marker-end="url(#dzpjB)" d="M232 88 C 290 88, 286 172, 344 172"/>
<path class="dz-pj-svg-edge" marker-end="url(#dzpjA)" d="M232 262 C 290 262, 286 190, 344 190"/>
<path class="dz-pj-svg-edge-hot" marker-end="url(#dzpjB)" d="M552 172 C 610 172, 606 88, 664 88"/>
<path class="dz-pj-svg-edge-block" marker-end="url(#dzpjC)" d="M552 190 C 610 190, 606 262, 664 262"/>
</svg>"""

DEPS = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Dépendances · ENG-142</h3>
    <span class="dz-pj-sp"></span>
    <div class="dz-pj-legend dz-pj-hide-sm" style="margin:0"><span>Chemin critique</span><span style="--_c:var(--dz-danger)">Bloque</span><span style="--_c:var(--dz-border-strong)">Lié</span></div>
    <a class="dz-pj-btn" href="#"><i class="fas fa-project-diagram"></i> Ajouter un lien</a>
  </div>
  <div class="dz-pj-dep"><div class="dz-pj-dep-canvas">
    {DEPS_SVG}
    <span class="dz-pj-coltag" style="left:24px">Pré-requis</span><span class="dz-pj-coltag" style="left:344px">Ticket</span><span class="dz-pj-coltag" style="left:664px">Débloque</span>
    {node(24, 48, "ENG-143", "done", "Tracer l'état de la file au réveil de l'app", "LM", " dz-pj-node-done")}
    {node(24, 222, "API-77", "review", "Endpoint idempotent pour les devis", "KB")}
    {node(344, 140, "ENG-142", "prog", "Les brouillons hors ligne ne se synchronisent pas", "LM", " dz-pj-node-focus")}
    {node(664, 48, "ENG-157", "todo", "Bêta interne : ouverture à 50 testeurs", "TG")}
    {node(664, 222, "ENG-139", "todo", "Paiement en une étape hors ligne", "SM", " dz-pj-node-blocked", "Bloqué")}
  </div></div>
</div>
"""


# ------------------------------------------------------------------ 20. boîte de réception
def imsg(who, text, snippet, id_, title, when, active=False, unread=False, s="prog"):
    cls = (" dz-active" if active else "") + (" dz-pj-unread" if unread else "")
    return (f'<a class="dz-pj-imsg{cls}" href="#">{av(who, " dz-pj-av-md")}<div class="dz-pj-imsg-t">{text}<small>{snippet}</small></div>'
            f'<span class="dz-pj-imsg-when">{when}</span><div class="dz-pj-imsg-ctx">{st(s)}<span class="dz-pj-id">{id_}</span><span>{title}</span></div></a>')


INBOX = f"""
<div class="dz-pj-shell">
  <div class="dz-pj-head">
    <h3 class="dz-pj-title">Boîte de réception</h3><span class="dz-pj-count">4</span>
    <span class="dz-pj-sp"></span>
    <div class="dz-pj-seg"><a href="#" class="dz-active">Tout</a><a href="#">Mentions</a><a href="#">Assignés</a></div>
    <a class="dz-pj-ibtn" href="#" aria-label="Tout marquer comme lu"><i class="fas fa-check-double"></i></a>
  </div>
  <div class="dz-pj-inbox">
    <div class="dz-pj-ilist">
      {imsg("TG", "<b>Thomas Girard</b> vous a mentionnée", "« @Léa je te propose de brancher la relance sur l'écouteur réseau… »", "ENG-142", "Brouillons hors ligne", "3 h", True, True)}
      {imsg("KB", "<b>Karim Benali</b> a changé la priorité", "Haute → Urgente", "ENG-142", "Brouillons hors ligne", "5 h", unread=True)}
      {imsg("SM", "<b>Sofia Marchetti</b> vous a assigné un ticket", "Valider les maquettes de l'écran de paiement", "ENG-139", "Paiement en une étape", "hier", unread=True, s="todo")}
      {imsg("NO", "<b>Nadia Ouali</b> a demandé votre revue", "#479 Journal d'audit des rôles", "ENG-120", "Journal d'audit", "hier", unread=True, s="review")}
      {imsg("JP", "<b>Julien Petit</b> a terminé un ticket", "Export CSV des équipes et des rôles", "ENG-118", "Export CSV", "19 sept.", s="done")}
    </div>
    <div class="dz-pj-ipreview">
      <div class="dz-pj-crumbs"><span class="dz-pj-id">ENG-142</span><i class="fas fa-chevron-right"></i><span>Application mobile 3.0</span><span class="dz-pj-sp"></span></div>
      <h3 class="dz-pj-issue-title" style="font-size:1.25rem">Les brouillons hors ligne ne se synchronisent pas au retour du réseau</h3>
      <div class="dz-cluster" style="--dz-gap:.4rem"><span class="dz-pj-pill">{st("prog")} En cours</span><span class="dz-pj-pill">{pri(4)} Urgente</span><span class="dz-pj-pill">{av("LM")} Léa Moreau</span>{lbls("Bug", "Mobile")}</div>
      <div class="dz-pj-comment" style="margin-left:0">
        <div class="dz-pj-comment-head">{av("TG")}<b>Thomas Girard</b><span>il y a 3 h</span></div>
        <p>Trouvé : le planificateur est suspendu par le système et on ne le réarme jamais. <span class="dz-pj-mention">@Léa</span> je te propose de brancher la relance sur l'écouteur réseau, c'est 20 lignes.</p>
      </div>
      <div class="dz-pj-composer" style="margin-left:0"><span class="dz-pj-placeholder">Répondre à Thomas…</span><div class="dz-pj-composer-bar"><span class="dz-pj-sp"></span><a class="dz-pj-btn" href="#"><i class="far fa-clock"></i> Plus tard</a><a class="dz-pj-btn dz-pj-btn-primary" href="#">Répondre</a></div></div>
    </div>
  </div>
</div>
"""

BLOCKS = [
    dict(name="en-tête de projet", icon="fas fa-heading", wrap="section", html=HEADER),
    dict(name="liste de tickets", icon="fas fa-list-ul", wrap="section", html=LIST),
    dict(name="tableau kanban", icon="fas fa-columns", wrap="section", html=KANBAN),
    dict(name="fiche ticket", icon="fas fa-file-alt", wrap="section", html=ISSUE),
    dict(name="cycle en cours", icon="fas fa-sync-alt", wrap="section", html=CYCLE),
    dict(name="feuille de route", icon="fas fa-stream", wrap="section", html=ROADMAP),
    dict(name="backlog", icon="fas fa-inbox", wrap="section", html=BACKLOG),
    dict(name="objectifs", icon="fas fa-bullseye", wrap="section", html=OKR),
    dict(name="jalons", icon="fas fa-flag-checkered", wrap="section", html=MILESTONES),
    dict(name="charge de l'équipe", icon="fas fa-th", wrap="section", html=WORKLOAD),
    dict(name="mes tâches", icon="fas fa-check-square", wrap="section", html=MYTASKS),
    dict(name="portefeuille de projets", icon="fas fa-briefcase", wrap="section", html=PORTFOLIO),
    dict(name="actions rapides", icon="fas fa-bolt", wrap="section", html=PALETTE),
    dict(name="wiki de projet", icon="fas fa-book", wrap="section", html=WIKI),
    dict(name="mises à jour", icon="fas fa-bullhorn", wrap="section", html=UPDATES),
    dict(name="calendrier des échéances", icon="fas fa-calendar-alt", wrap="section", html=CALENDAR),
    dict(name="création rapide", icon="fas fa-plus-square", wrap="section", html=CREATE),
    dict(name="état vide", icon="far fa-folder-open", wrap="section", html=EMPTY),
    dict(name="graphe de dépendances", icon="fas fa-project-diagram", wrap="section", html=DEPS),
    dict(name="boîte de réception", icon="fas fa-bell", wrap="section", html=INBOX),
]
