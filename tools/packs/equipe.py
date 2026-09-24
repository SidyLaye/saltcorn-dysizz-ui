"""Famille « Équipe » : organigramme, annuaire, fiches, congés, absences, recrutement,
onboarding, entretiens, humeur, temps, carrières, compétences, relève.
Tout le CSS est dans styles/41-equipe.css (préfixe dz-eq-)."""

FAMILY = "equipe"

# ------------------------------------------------------------------ petits morceaux
PEOPLE = {
    "CD": ("Claire Dubois", "Directrice générale", 1),
    "MR": ("Marc Rousseau", "Directeur technique", 2),
    "AB": ("Amina Benkirane", "Directrice des opérations", 3),
    "PL": ("Paul Lefèvre", "Directeur financier", 4),
    "OR": ("Olivia Renard", "Directrice produit", 7),
    "LM": ("Léa Moreau", "Lead développeuse mobile", 1),
    "KB": ("Karim Benali", "Ingénieur back-end", 2),
    "SM": ("Sofia Marchetti", "Product designer", 3),
    "TG": ("Thomas Girard", "Ingénieur qualité", 4),
    "IL": ("Inès Laurent", "Responsable RH", 5),
    "HF": ("Hugo Fontaine", "Ingénieur plateforme", 7),
    "NO": ("Nadia Ouali", "Responsable support", 6),
    "JP": ("Julien Petit", "Contrôleur de gestion", 2),
    "EV": ("Emma Vidal", "Développeuse front-end", 3),
    "YT": ("Yanis Traoré", "Chargé de recrutement", 4),
    "CG": ("Camille Garnier", "Comptable", 5),
    "RN": ("Romain Nguyen", "Data analyst", 7),
    "ZA": ("Zoé Adam", "Chargée de clientèle", 1),
    "BM": ("Baptiste Martin", "Product manager", 6),
}


def av(ini, size="", pres=None):
    p = f" dz-eq-pres-{pres}" if pres else ""
    if ini is None:
        return f'<span class="dz-eq-av dz-eq-av-none{size}"><i class="fas fa-user"></i></span>'
    return f'<span class="dz-eq-av dz-eq-c{PEOPLE[ini][2]}{size}{p}">{ini}</span>'


def avs(*inis, more=None, size=""):
    extra = f'<span class="dz-eq-more">+{more}</span>' if more else ""
    return '<span class="dz-eq-avs">' + "".join(av(i, size) for i in inis) + extra + "</span>"


def name(ini):
    return PEOPLE[ini][0]


def role(ini):
    return PEOPLE[ini][1]


def tag(t, c=1, cls=""):
    return f'<span class="dz-eq-tag dz-eq-c{c}{cls}">{t}</span>'


def pill(t, c=4):
    return f'<span class="dz-eq-pill dz-eq-c{c}">{t}</span>'


def meter(v, c=1, cls=""):
    return f'<span class="dz-eq-meter dz-eq-c{c}{cls}" style="--v:{v}%"><span></span></span>'


def stars(v):
    return f'<span class="dz-eq-stars" style="--v:{v}%" aria-label="Note {v / 20:.1f} sur 5"></span>'


DEPT = {"Tech": 2, "Produit": 7, "Opérations": 3, "Finance": 4, "RH": 5, "Support": 6, "Direction": 1}


# ------------------------------------------------------------------ 1. organigramme
def onode(ini, dept, n=None, cls=""):
    cnt = f'<span class="dz-eq-onode-n"><i class="fas fa-users"></i> {n}</span>' if n else ""
    return (f'<a class="dz-eq-onode{cls}" href="#">{av(ini, " dz-eq-av-md")}<span class="dz-eq-onode-t"><b>{name(ini)}</b>'
            f'<small>{role(ini)}</small></span><span class="dz-eq-onode-foot">{tag(dept, DEPT[dept])}{cnt}</span></a>')


def oleaf(ini, pres="on"):
    return (f'<a class="dz-eq-oleaf" href="#">{av(ini, "", pres)}<span class="dz-eq-oleaf-t"><b>{name(ini)}</b>'
            f'<small>{role(ini)}</small></span></a>')


def obranch(ini, dept, n, leaves):
    return (f'<li class="dz-eq-tli">{onode(ini, dept, n)}<div class="dz-eq-tstack">{"".join(leaves)}</div></li>')


ORG = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Organigramme</h3><span class="dz-eq-count">48</span>
    <span class="dz-eq-sp"></span>
    <div class="dz-eq-seg"><a href="#" class="dz-active"><i class="fas fa-sitemap"></i> Arbre</a><a href="#"><i class="fas fa-list"></i> Liste</a></div>
    <a class="dz-eq-btn dz-eq-hide-sm" href="#"><i class="fas fa-search"></i> Trouver quelqu'un</a>
    <a class="dz-eq-btn" href="#"><i class="fas fa-download"></i> Exporter</a>
  </div>
  <div class="dz-eq-org">
    <ul class="dz-eq-tul dz-eq-troot">
      <li class="dz-eq-tli">
        {onode("CD", "Direction", 48, " dz-eq-onode-top")}
        <ul class="dz-eq-tul">
          {obranch("MR", "Tech", 18, [oleaf("LM"), oleaf("KB", "away"), oleaf("HF"), '<a class="dz-eq-oleaf dz-eq-oleaf-open" href="#"><span class="dz-eq-av dz-eq-av-none"><i class="fas fa-plus"></i></span><span class="dz-eq-oleaf-t"><b>Poste ouvert</b><small>Ingénieur·e sécurité</small></span></a>'])}
          {obranch("OR", "Produit", 9, [oleaf("BM"), oleaf("SM"), oleaf("RN", "off")])}
          {obranch("AB", "Opérations", 14, [oleaf("IL"), oleaf("NO"), oleaf("ZA", "away")])}
          {obranch("PL", "Finance", 6, [oleaf("JP"), oleaf("CG")])}
        </ul>
      </li>
    </ul>
  </div>
  <div class="dz-eq-foot">
    <span class="dz-eq-legend"><span class="dz-eq-c4">En ligne</span><span class="dz-eq-c5">Absent·e</span><span class="dz-eq-cx">Hors ligne</span></span>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-mute">Mis à jour le 24 sept. 2026</span>
  </div>
</div>
"""


# ------------------------------------------------------------------ 2. annuaire
def drow(ini, dept, place, hour, pres="on", me=False):
    you = ' <span class="dz-eq-you">vous</span>' if me else ""
    return (f'<a class="dz-eq-drow" href="#">{av(ini, " dz-eq-av-md", pres)}'
            f'<span class="dz-eq-drow-t"><b>{name(ini)}{you}</b><small>{role(ini)}</small></span>'
            f'<span class="dz-eq-drow-d dz-eq-hide-sm">{tag(dept, DEPT[dept])}</span>'
            f'<span class="dz-eq-drow-p dz-eq-hide-sm"><i class="fas fa-map-marker-alt"></i> {place}</span>'
            f'<span class="dz-eq-drow-h dz-eq-hide-md"><i class="far fa-clock"></i> {hour}</span>'
            f'<span class="dz-eq-drow-a"><span class="dz-eq-ibtn" aria-label="Écrire"><i class="far fa-envelope"></i></span>'
            f'<span class="dz-eq-ibtn" aria-label="Message"><i class="far fa-comment-dots"></i></span></span></a>')


DIRECTORY = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Annuaire</h3><span class="dz-eq-count">48</span>
    <span class="dz-eq-sp"></span>
    <div class="dz-eq-search"><i class="fas fa-search"></i><span>Nom, poste, compétence…</span><span class="dz-eq-kbd">/</span></div>
    <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-user-plus"></i> Inviter</a>
  </div>
  <div class="dz-eq-filters dz-chips">
    <a class="dz-eq-fchip dz-chip dz-active" href="#">Tous <span>48</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Tech <span>18</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Produit <span>9</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Opérations <span>14</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Finance <span>6</span></a>
    <span class="dz-eq-sp"></span>
    <a class="dz-eq-btn dz-eq-btn-ghost" href="#"><i class="fas fa-map-marker-alt"></i> Tous les bureaux <i class="fas fa-chevron-down"></i></a>
  </div>
  <div class="dz-eq-dir">
    <div class="dz-eq-letter">B</div>
    {drow("KB", "Tech", "Lyon", "14:32", "away")}
    {drow("AB", "Opérations", "Paris", "14:32")}
    <div class="dz-eq-letter">D – G</div>
    {drow("CD", "Direction", "Paris", "14:32")}
    {drow("HF", "Tech", "Nantes", "14:32")}
    {drow("TG", "Tech", "Télétravail · Lisbonne", "13:32", "off")}
    <div class="dz-eq-letter">L – M</div>
    {drow("IL", "RH", "Paris", "14:32", me=True)}
    {drow("SM", "Produit", "Lyon", "14:32")}
    {drow("LM", "Tech", "Paris", "14:32")}
  </div>
  <div class="dz-eq-foot"><span class="dz-eq-mute">8 sur 48 affichés</span><span class="dz-eq-sp"></span><a class="dz-eq-btn" href="#">Voir tout <i class="fas fa-arrow-right"></i></a></div>
</div>
"""


# ------------------------------------------------------------------ 3. fiche membre
def week(days):
    out = ""
    for d, k, lab in days:
        out += f'<span class="dz-eq-wday dz-eq-wday-{k}"><b>{d}</b><small>{lab}</small></span>'
    return f'<div class="dz-eq-week">{out}</div>'


PROFILE = f"""
<div class="dz-eq-shell dz-eq-profile">
  <div class="dz-eq-cover"></div>
  <div class="dz-eq-pid">
    <span class="dz-eq-av dz-eq-c1 dz-eq-av-xl dz-eq-pres-on">LM</span>
    <div class="dz-eq-pid-t">
      <h2 class="dz-eq-pname">Léa Moreau <span class="dz-eq-mute">elle</span></h2>
      <p class="dz-eq-prole">Lead développeuse mobile · Équipe Produit mobile</p>
      <div class="dz-eq-pmeta"><span><i class="fas fa-map-marker-alt"></i> Paris · Bureau Oberkampf</span><span><i class="far fa-clock"></i> 14:32 heure locale</span><span><i class="fas fa-seedling"></i> Chez nous depuis 3 ans</span></div>
    </div>
    <div class="dz-eq-pid-a">
      <a class="dz-eq-btn" href="#"><i class="far fa-calendar-plus"></i> Planifier</a>
      <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="far fa-comment-dots"></i> Message</a>
      <a class="dz-eq-ibtn" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a>
    </div>
  </div>
  <div class="dz-eq-tabs">
    <a class="dz-eq-tab dz-active" href="#">Profil</a><a class="dz-eq-tab" href="#">Poste &amp; rémunération</a><a class="dz-eq-tab" href="#">Absences</a><a class="dz-eq-tab" href="#">Objectifs</a><a class="dz-eq-tab" href="#">Documents</a>
  </div>
  <div class="dz-eq-pbody">
    <aside class="dz-eq-pside">
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Coordonnées</div>
        <div class="dz-eq-kv"><i class="far fa-envelope"></i><span>lea.moreau@nexora.fr</span></div>
        <div class="dz-eq-kv"><i class="fas fa-phone-alt"></i><span>06 42 18 77 05</span></div>
        <div class="dz-eq-kv"><i class="fab fa-github"></i><span>@leamoreau</span></div>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Responsable</div>
        <a class="dz-eq-mini" href="#">{av("MR", " dz-eq-av-md")}<span><b>Marc Rousseau</b><small>Directeur technique</small></span></a>
        <div class="dz-eq-box-t">Équipe directe · 4</div>
        <div class="dz-eq-cluster">{avs("KB", "HF", "EV", "TG", size=" dz-eq-av-md")}</div>
      </div>
    </aside>
    <div class="dz-eq-pmain">
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">À propos</div>
        <p class="dz-eq-p">Je pilote l'application mobile depuis la version 2.0. Passionnée par les interfaces hors ligne et l'accessibilité ; je mentore volontiers les nouvelles recrues. Le vendredi, je suis au bureau de Lyon.</p>
        <div class="dz-eq-cluster"><span class="dz-eq-skill">Swift <b>Expert</b></span><span class="dz-eq-skill">Kotlin <b>Avancé</b></span><span class="dz-eq-skill">Accessibilité <b>Avancé</b></span><span class="dz-eq-skill">Mentorat</span><span class="dz-eq-skill">Architecture</span></div>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Cette semaine</div>
        {week([("Lun", "office", "Bureau"), ("Mar", "office", "Bureau"), ("Mer", "remote", "Télétravail"), ("Jeu", "off", "Congé"), ("Ven", "office", "Lyon")])}
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Parcours chez Nexora</div>
        <div class="dz-eq-path">
          <div class="dz-eq-step dz-eq-step-now"><b>Lead développeuse mobile</b><small>depuis mars 2025 · Équipe Produit mobile</small></div>
          <div class="dz-eq-step"><b>Développeuse mobile senior</b><small>janv. 2024 → mars 2025</small></div>
          <div class="dz-eq-step"><b>Développeuse mobile</b><small>sept. 2023 → janv. 2024 · arrivée</small></div>
        </div>
      </div>
    </div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 4. cartes équipe
def team(icon, c, title, desc, lead, members, more, n, open_=0, chan=""):
    op = f'<span class="dz-eq-open">{open_} poste{"s" if open_ > 1 else ""} ouvert{"s" if open_ > 1 else ""}</span>' if open_ else '<span class="dz-eq-mute">Au complet</span>'
    return (f'<a class="dz-eq-team" href="#"><div class="dz-eq-team-top"><span class="dz-eq-ticon dz-eq-c{c}"><i class="{icon}"></i></span>'
            f'<span class="dz-eq-sp"></span><span class="dz-eq-chan">#{chan}</span></div>'
            f'<h3 class="dz-eq-team-t">{title}</h3><p class="dz-eq-team-d">{desc}</p>'
            f'<div class="dz-eq-team-lead">{av(lead)}<span>Responsable : <b>{name(lead)}</b></span></div>'
            f'<div class="dz-eq-team-foot">{avs(*members, more=more)}<span class="dz-eq-mute">{n} membres</span><span class="dz-eq-sp"></span>{op}</div></a>')


TEAMS = f"""
<div class="dz-eq-teams-head">
  <div><h2 class="dz-eq-h">Nos équipes</h2><p class="dz-eq-lead">6 équipes, 48 personnes, 3 bureaux et beaucoup de café.</p></div>
  <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-plus"></i> Créer une équipe</a>
</div>
<div class="dz-eq-teams">
  {team("fas fa-mobile-alt", 1, "Produit mobile", "Applications iOS et Android, mode hors ligne et notifications.", "LM", ("LM", "KB", "EV", "TG"), 4, 8, 1, "mobile")}
  {team("fas fa-server", 7, "Plateforme", "Infrastructure, API publique, sécurité et fiabilité des services.", "HF", ("HF", "KB", "RN"), 7, 10, 2, "plateforme")}
  {team("fas fa-pencil-ruler", 3, "Design", "Système de design, recherche utilisateur et prototypage.", "SM", ("SM", "BM", "EV"), 1, 4, 0, "design")}
  {team("fas fa-headset", 6, "Support client", "Réponses en moins de 2 h, base de connaissances et retours produit.", "NO", ("NO", "ZA", "YT"), 5, 8, 1, "support")}
  {team("fas fa-coins", 4, "Finance", "Clôtures mensuelles, trésorerie, achats et contrôle de gestion.", "PL", ("PL", "JP", "CG"), 3, 6, 0, "finance")}
  {team("fas fa-heart", 5, "Personnes &amp; culture", "Recrutement, intégration, formation et vie d'équipe.", "IL", ("IL", "YT", "AB"), None, 3, 1, "rh")}
</div>
"""


# ------------------------------------------------------------------ 5. demande de congés
def bal(label, val, unit, v, c, note):
    return (f'<div class="dz-eq-bal dz-eq-c{c}"><div class="dz-eq-ring" style="--v:{v}%"><b>{val}</b><small>{unit}</small></div>'
            f'<div class="dz-eq-bal-t"><b>{label}</b><small>{note}</small></div></div>')


def lreq(kind, dates, n, status, c):
    return (f'<div class="dz-eq-lreq"><span class="dz-eq-lreq-k dz-eq-c{c}"></span><span class="dz-eq-lreq-t"><b>{kind}</b><small>{dates}</small></span>'
            f'<span class="dz-eq-lreq-n">{n}</span>{status}</div>')


LEAVE = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Demander une absence</h3>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-mute dz-eq-hide-sm">Période de référence : juin 2026 → mai 2027</span>
  </div>
  <div class="dz-eq-leave">
    <div class="dz-eq-leave-bal">
      <div class="dz-eq-box-t">Mon solde</div>
      {bal("Congés payés", "18,5", "jours", 74, 1, "+ 2,08 j acquis le 1er oct.")}
      {bal("RTT", "6", "jours", 50, 7, "À poser avant le 31 déc.")}
      {bal("Récupération", "1,5", "jour", 30, 3, "Astreinte du 12 sept.")}
      <div class="dz-eq-note"><i class="fas fa-info-circle"></i><span>3 jours de RTT expirent dans <b>98 jours</b>.</span></div>
    </div>
    <div class="dz-eq-leave-form">
      <div class="dz-eq-field-l">Type d'absence</div>
      <div class="dz-eq-types"><a class="dz-eq-type dz-active" href="#"><i class="fas fa-umbrella-beach"></i> Congés payés</a><a class="dz-eq-type" href="#"><i class="fas fa-mug-hot"></i> RTT</a><a class="dz-eq-type" href="#"><i class="fas fa-notes-medical"></i> Maladie</a><a class="dz-eq-type" href="#"><i class="fas fa-ellipsis-h"></i> Autre</a></div>
      <div class="dz-eq-dates">
        <div class="dz-eq-field"><small>Du</small><b><i class="far fa-calendar"></i> lun. 19 oct. 2026</b><span class="dz-eq-half">Matin</span></div>
        <span class="dz-eq-dates-arrow"><i class="fas fa-arrow-right"></i></span>
        <div class="dz-eq-field"><small>Au</small><b><i class="far fa-calendar"></i> ven. 23 oct. 2026</b><span class="dz-eq-half">Soir</span></div>
      </div>
      <div class="dz-eq-calc">
        <div><small>Durée</small><b>5 jours ouvrés</b></div>
        <div><small>Solde après</small><b>13,5 jours</b></div>
        <div><small>Validation</small><span class="dz-eq-inline">{av("MR")} Marc Rousseau</span></div>
      </div>
      <div class="dz-eq-textarea">Vacances en famille — Thomas assure le relais sur les revues de code.</div>
      <div class="dz-eq-warn"><i class="fas fa-user-friends"></i><span><b>2 personnes</b> de votre équipe sont déjà absentes cette semaine-là.</span></div>
      <div class="dz-eq-actions"><a class="dz-eq-btn" href="#">Annuler</a><a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-paper-plane"></i> Envoyer la demande</a></div>
    </div>
  </div>
  <div class="dz-eq-sub-h">Mes demandes récentes</div>
  <div class="dz-eq-lreqs">
    {lreq("RTT", "ven. 9 oct. 2026", "1 j", pill("En attente", 5), 7)}
    {lreq("Congés payés", "3 → 21 août 2026", "15 j", pill("Approuvée", 4), 1)}
    {lreq("Récupération", "lun. 15 juin 2026", "0,5 j", pill("Refusée", 6), 3)}
  </div>
</div>
"""


# ------------------------------------------------------------------ 6. calendrier des absences
DAYS = [(d, "LMMJVSD"[(d - 2) % 7]) for d in range(2, 23)]


def crow(ini, bars):
    b = "".join(f'<span class="dz-eq-cbar dz-eq-c{c}{" dz-eq-cbar-p" if p else ""}" style="grid-column:{s} / span {n}">{t}</span>' for s, n, c, t, p in bars)
    return f'<div class="dz-eq-crow"><div class="dz-eq-cwho">{av(ini)}<span>{name(ini)}</span></div><div class="dz-eq-ctrack">{b}</div></div>'


ABSENCES = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Absences de l'équipe</h3>
    <a class="dz-eq-ibtn" href="#" aria-label="Période précédente"><i class="fas fa-chevron-left"></i></a>
    <b class="dz-eq-period">2 → 22 novembre 2026</b>
    <a class="dz-eq-ibtn" href="#" aria-label="Période suivante"><i class="fas fa-chevron-right"></i></a>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-legend dz-eq-hide-sm"><span class="dz-eq-c1">Congés</span><span class="dz-eq-c7">RTT</span><span class="dz-eq-c6">Maladie</span><span class="dz-eq-c3">Formation</span></span>
    <div class="dz-eq-seg"><a href="#">Semaine</a><a href="#" class="dz-active">3 semaines</a></div>
  </div>
  <div class="dz-eq-cal">
    <div class="dz-eq-cal-in">
      <div class="dz-eq-crow dz-eq-chead"><div class="dz-eq-cwho"><span class="dz-eq-mute">8 personnes</span></div><div class="dz-eq-ctrack">{"".join(f'<span class="dz-eq-cday{" dz-eq-cday-we" if l in "SD" and i % 7 >= 5 else ""}{" dz-eq-cday-hol" if d == 11 else ""}"><small>{l}</small><b>{d}</b></span>' for i, (d, l) in enumerate(DAYS))}</div></div>
      <div class="dz-eq-cbody">
        <span class="dz-eq-chol">Armistice</span>
        {crow("LM", [(1, 5, 1, "Congés · Crète", False)])}
        {crow("KB", [(4, 1, 7, "RTT", False), (15, 3, 3, "Formation", False)])}
        {crow("SM", [(8, 2, 6, "Maladie", False)])}
        {crow("TG", [(17, 3, 1, "Congés", True)])}
        {crow("HF", [])}
        {crow("EV", [(15, 5, 1, "Congés · Montréal", False)])}
        {crow("RN", [(5, 1, 7, "RTT", True), (19, 1, 7, "RTT", False)])}
        {crow("NO", [(9, 1, 3, "Salon", False)])}
      </div>
      <div class="dz-eq-crow dz-eq-cfoot"><div class="dz-eq-cwho"><span class="dz-eq-mute">Absents / jour</span></div><div class="dz-eq-ctrack">{"".join(f'<span class="dz-eq-cn dz-eq-cn-{n}">{n or "·"}</span>' for n in [1,1,1,2,2,0,0,1,2,0,0,0,0,0,2,2,3,2,3,0,0])}</div></div>
    </div>
  </div>
  <div class="dz-eq-foot"><i class="fas fa-circle-notch dz-eq-mute"></i><span class="dz-eq-mute">Hachuré : demande en attente de validation</span><span class="dz-eq-sp"></span><a class="dz-eq-btn" href="#"><i class="fas fa-download"></i> Exporter .ics</a></div>
</div>
"""


# ------------------------------------------------------------------ 7. pipeline de recrutement
def cand(ini, nom, now, v, src, days, tags=(), cls="", late=False):
    t = "".join(f'<span class="dz-eq-ctag">{x}</span>' for x in tags)
    d = f'<span class="dz-eq-days{" dz-eq-late" if late else ""}"><i class="far fa-clock"></i> {days}</span>'
    return (f'<a class="dz-eq-cand{cls}" href="#"><div class="dz-eq-cand-top"><span class="dz-eq-av dz-eq-av-md dz-eq-c{ini}">{nom[0]}{nom.split()[1][0]}</span>'
            f'<span class="dz-eq-cand-t"><b>{nom}</b><small>{now}</small></span></div>'
            f'<div class="dz-eq-cand-mid">{stars(v)}<span class="dz-eq-src">{src}</span></div>'
            + (f'<div class="dz-eq-cand-tags">{t}</div>' if tags else "") +
            f'<div class="dz-eq-cand-foot">{d}<span class="dz-eq-sp"></span></div></a>')


def stage(title, n, c, cards, conv=None):
    cv = f'<span class="dz-eq-conv">{conv}</span>' if conv else ""
    return (f'<div class="dz-eq-stage"><div class="dz-eq-stage-h"><span class="dz-eq-sdot dz-eq-c{c}"></span><b>{title}</b>'
            f'<span class="dz-eq-count">{n}</span><span class="dz-eq-sp"></span>{cv}</div>'
            f'<div class="dz-eq-stage-cards">{"".join(cards)}</div></div>')


PIPELINE = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <span class="dz-eq-ticon dz-eq-c2 dz-eq-ticon-sm"><i class="fas fa-code"></i></span>
    <div class="dz-eq-head-t"><h3 class="dz-eq-title">Ingénieur·e back-end senior</h3><small>Tech · Paris ou télétravail · CDI · 58–68 k€</small></div>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-hstat dz-eq-hide-sm"><b>44</b> candidatures</span>
    <span class="dz-eq-hstat dz-eq-hide-sm"><b>23 j</b> ouvert</span>
    {avs("YT", "MR", "KB")}
    <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-plus"></i> Candidat</a>
  </div>
  <div class="dz-eq-pipe">
    {stage("Candidatures", 24, 0, [cand(7, "Maël Durand", "Dév. PHP · Groupe Aldric", 60, "Site carrières", "2 j", ("Go", "SQL")), cand(3, "Chloé Perrin", "Freelance · 8 ans d'exp.", 70, "Cooptation", "5 j", ("Rust",))])}
    {stage("Présélection", 9, 7, [cand(2, "Samir Haddad", "Ingénieur · Veltis", 80, "Chasse", "1 j", ("Go", "Kafka")), cand(5, "Lucie Morel", "Back-end · Orbéa", 60, "Site carrières", "9 j", (), late=True)], "38 %")}
    {stage("Entretiens", 5, 5, [cand(1, "Antoine Leroy", "Lead dev · Kivo Santé", 90, "Cooptation", "3 j", ("Go", "Postgres"), " dz-eq-cand-hot"), cand(4, "Inès Faure", "SRE · Hélion", 80, "Salon", "4 j", ("K8s",))], "56 %")}
    {stage("Cas pratique", 3, 3, [cand(6, "David Kim", "Ingénieur · Nubo", 80, "Chasse", "2 j", ("Go",))], "60 %")}
    {stage("Offre", 1, 4, [cand(2, "Sarah Cohen", "Senior · Datafleur", 100, "Cooptation", "1 j", ("Offre envoyée",), " dz-eq-cand-offer")], "33 %")}
  </div>
</div>
"""


# ------------------------------------------------------------------ 8. fiche candidat
def score(crit, marks, note):
    m = "".join(f'<span class="dz-eq-mark dz-eq-mark-{k}"></span>' for k in marks)
    return f'<div class="dz-eq-score"><span class="dz-eq-score-t">{crit}</span><span class="dz-eq-marks">{m}</span><span class="dz-eq-score-n">{note}</span></div>'


CANDIDATE = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-chead2">
    <span class="dz-eq-av dz-eq-av-xl dz-eq-c1">AL</span>
    <div class="dz-eq-chead2-t">
      <div class="dz-eq-crumb">Ingénieur·e back-end senior <i class="fas fa-chevron-right"></i> Candidat 12 / 44</div>
      <h2 class="dz-eq-pname">Antoine Leroy</h2>
      <div class="dz-eq-pmeta"><span><i class="fas fa-briefcase"></i> Lead dev · Kivo Santé</span><span><i class="fas fa-map-marker-alt"></i> Montreuil</span><span><i class="fas fa-user-friends"></i> Coopté par Hugo Fontaine</span></div>
    </div>
    <div class="dz-eq-pid-a">
      <a class="dz-eq-btn dz-eq-btn-danger" href="#"><i class="fas fa-times"></i> Refuser</a>
      <a class="dz-eq-btn dz-eq-btn-primary" href="#">Étape suivante <i class="fas fa-arrow-right"></i></a>
    </div>
  </div>
  <div class="dz-eq-steps">
    <span class="dz-eq-sstep dz-eq-done"><i class="fas fa-check"></i> Candidature</span>
    <span class="dz-eq-sstep dz-eq-done"><i class="fas fa-check"></i> Présélection</span>
    <span class="dz-eq-sstep dz-eq-now"><b>3</b> Entretiens</span>
    <span class="dz-eq-sstep"><b>4</b> Cas pratique</span>
    <span class="dz-eq-sstep"><b>5</b> Offre</span>
  </div>
  <div class="dz-eq-pbody dz-eq-pbody-r">
    <div class="dz-eq-pmain">
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Grille d'évaluation <span class="dz-eq-sp"></span><span class="dz-eq-inline">{avs("MR", "KB", "YT")} 3 avis</span></div>
        {score("Conception d'API", "4444", "4,0")}
        {score("Bases de données", "4434", "3,8")}
        {score("Communication", "3444", "3,8")}
        {score("Autonomie", "4333", "3,3")}
        {score("Culture d'équipe", "4404", "4,0")}
        <div class="dz-eq-verdict"><span class="dz-eq-verdict-big">Oui, fortement</span><span class="dz-eq-mute">2 « oui fort » · 1 « oui »</span><span class="dz-eq-sp"></span><span class="dz-eq-verdict-n">3,8<small>/4</small></span></div>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Dernier retour</div>
        <div class="dz-eq-quote">{av("MR")}<p><b>Marc Rousseau</b> · entretien technique, 22 sept.<br>Très solide sur la conception d'API et le découpage en services. A posé les bonnes questions sur notre dette. À challenger sur le pilotage d'équipe lors de l'étape suivante.</p></div>
      </div>
    </div>
    <aside class="dz-eq-pside">
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Informations</div>
        <div class="dz-eq-kv2"><small>Prétentions</small><b>64 k€ brut</b></div>
        <div class="dz-eq-kv2"><small>Préavis</small><b>1 mois</b></div>
        <div class="dz-eq-kv2"><small>Disponible</small><b>2 nov. 2026</b></div>
        <div class="dz-eq-kv2"><small>Source</small><b>Cooptation</b></div>
        <a class="dz-eq-file" href="#"><i class="far fa-file-pdf"></i><span><b>CV_Antoine_Leroy.pdf</b><small>2 pages · 184 Ko</small></span></a>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Prochain entretien</div>
        <div class="dz-eq-next"><span class="dz-eq-date"><small>OCT</small><b>1</b></span><span><b>Entretien d'équipe</b><small>10:00 – 11:00 · Visio</small></span></div>
        <div class="dz-eq-cluster">{avs("LM", "HF")}<span class="dz-eq-mute">Léa, Hugo</span></div>
      </div>
    </aside>
  </div>
</div>
"""


# ------------------------------------------------------------------ 9. onboarding
def todo(t, who, when, done=False, late=False):
    w = f'<span class="dz-eq-due{" dz-eq-late" if late else ""}">{when}</span>'
    return (f'<a class="dz-eq-todo{" dz-eq-todo-done" if done else ""}" href="#"><span class="dz-eq-check"></span>'
            f'<span class="dz-eq-todo-t">{t}</span>{w}{av(who)}</a>')


def phase(title, n, items, c=1):
    return (f'<div class="dz-eq-phase"><div class="dz-eq-phase-h"><span class="dz-eq-sdot dz-eq-c{c}"></span><b>{title}</b>'
            f'<span class="dz-eq-count">{n}</span></div>{"".join(items)}</div>')


ONBOARDING = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-welcome">
    <span class="dz-eq-av dz-eq-av-xl dz-eq-c3">EV</span>
    <div class="dz-eq-welcome-t">
      <span class="dz-eq-eyebrow"><i class="fas fa-rocket"></i> Intégration</span>
      <h2 class="dz-eq-pname">Emma Vidal arrive lundi 5 octobre</h2>
      <p class="dz-eq-prole">Développeuse front-end · Équipe Produit mobile · CDI</p>
    </div>
    <div class="dz-eq-countdown"><b>11</b><small>jours</small></div>
    <div class="dz-eq-ring dz-eq-ring-lg dz-eq-c1" style="--v:62%"><b>62 %</b><small>prêt</small></div>
  </div>
  <div class="dz-eq-onb">
    <div class="dz-eq-onb-list">
      {phase("Avant l'arrivée", "5 / 6", [
          todo("Envoyer le contrat signé et le livret d'accueil", "IL", "18 sept.", True),
          todo("Commander l'ordinateur et l'écran", "HF", "22 sept.", True),
          todo("Créer les comptes (messagerie, dépôt de code, agenda)", "HF", "30 sept."),
      ], 4)}
      {phase("Premier jour", "0 / 4", [
          todo("Petit-déjeuner d'accueil avec l'équipe", "LM", "5 oct."),
          todo("Remise du badge et visite du bureau", "IL", "5 oct."),
          todo("Premier ticket : corriger une coquille dans l'app", "LM", "5 oct."),
      ], 1)}
      {phase("Premier mois", "0 / 5", [
          todo("Point d'étonnement avec la RH", "IL", "2 nov."),
          todo("Fixer les objectifs de période d'essai", "MR", "4 nov."),
      ], 7)}
    </div>
    <aside class="dz-eq-onb-side">
      <div class="dz-eq-buddy">
        <div class="dz-eq-box-t">Marraine</div>
        <div class="dz-eq-mini">{av("SM", " dz-eq-av-lg", "on")}<span><b>Sofia Marchetti</b><small>Product designer · 4 ans chez nous</small></span></div>
        <p class="dz-eq-p">« Je t'emmène déjeuner le premier jour, et on garde un café chaque jeudi du premier mois. »</p>
        <a class="dz-eq-btn dz-eq-btn-block" href="#"><i class="far fa-comment-dots"></i> Écrire à Sofia</a>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Matériel &amp; accès</div>
        <div class="dz-eq-kit dz-eq-ok"><i class="fas fa-laptop"></i><span>Ordinateur portable 14"</span><i class="fas fa-check-circle"></i></div>
        <div class="dz-eq-kit dz-eq-ok"><i class="fas fa-desktop"></i><span>Écran 27"</span><i class="fas fa-check-circle"></i></div>
        <div class="dz-eq-kit"><i class="fas fa-id-badge"></i><span>Badge d'accès</span><i class="far fa-circle"></i></div>
        <div class="dz-eq-kit"><i class="fas fa-key"></i><span>Comptes et accès</span><i class="far fa-circle"></i></div>
      </div>
    </aside>
  </div>
</div>
"""


# ------------------------------------------------------------------ 10. entretien annuel
def obj(t, w, v, self_, mgr, c=1):
    return (f'<div class="dz-eq-obj"><div class="dz-eq-obj-t"><b>{t}</b><small>Poids {w} %</small></div>'
            f'<div class="dz-eq-obj-m">{meter(v, c)}<span class="dz-eq-pct">{v} %</span></div>'
            f'<div class="dz-eq-obj-r"><span class="dz-eq-rate" title="Auto-évaluation">{self_}</span><span class="dz-eq-rate dz-eq-rate-m" title="Manager">{mgr}</span></div></div>')


def comp(t, s, m):
    return (f'<div class="dz-eq-comp"><span class="dz-eq-comp-t">{t}</span><span class="dz-eq-scale">'
            + "".join(f'<span class="dz-eq-sc{" dz-eq-sc-s" if i == s else ""}{" dz-eq-sc-m" if i == m else ""}"></span>' for i in range(1, 6))
            + "</span></div>")


REVIEW = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <div class="dz-eq-inline">{avs("LM", "MR", size=" dz-eq-av-md")}</div>
    <div class="dz-eq-head-t"><h3 class="dz-eq-title">Entretien annuel 2026 · Léa Moreau</h3><small>avec Marc Rousseau · jeudi 15 oct., 14:00</small></div>
    <span class="dz-eq-sp"></span>
    <a class="dz-eq-btn" href="#"><i class="far fa-file-pdf"></i> PDF</a>
    <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-signature"></i> Signer</a>
  </div>
  <div class="dz-eq-steps">
    <span class="dz-eq-sstep dz-eq-done"><i class="fas fa-check"></i> Auto-évaluation</span>
    <span class="dz-eq-sstep dz-eq-done"><i class="fas fa-check"></i> Avis du manager</span>
    <span class="dz-eq-sstep dz-eq-now"><b>3</b> Entretien</span>
    <span class="dz-eq-sstep"><b>4</b> Signatures</span>
  </div>
  <div class="dz-eq-rev">
    <div class="dz-eq-rev-main">
      <div class="dz-eq-sub-h">Objectifs 2026 <span class="dz-eq-sp"></span><span class="dz-eq-rkey"><span class="dz-eq-rate">A</span> Léa <span class="dz-eq-rate dz-eq-rate-m">M</span> Marc</span></div>
      {obj("Sortir l'application 3.0 avec le mode hors ligne", 40, 92, "4", "4", 4)}
      {obj("Réduire le temps de démarrage sous 1,5 s", 25, 70, "3", "3", 5)}
      {obj("Faire monter 2 développeurs en autonomie", 20, 100, "4", "5", 4)}
      {obj("Porter l'accessibilité au niveau AA", 15, 45, "3", "2", 6)}
      <div class="dz-eq-sub-h">Compétences <span class="dz-eq-sp"></span><span class="dz-eq-rkey"><span class="dz-eq-sc dz-eq-sc-s"></span> Léa <span class="dz-eq-sc dz-eq-sc-m"></span> Marc</span></div>
      {comp("Expertise technique", 5, 5)}
      {comp("Leadership", 3, 4)}
      {comp("Communication", 4, 4)}
      {comp("Priorisation", 4, 3)}
    </div>
    <aside class="dz-eq-rev-side">
      <div class="dz-eq-verdict-card">
        <small>Appréciation globale</small>
        <b>Dépasse les attentes</b>
        <div class="dz-eq-5">
          <span></span><span></span><span></span><span class="dz-eq-on"></span><span></span>
        </div>
        <span class="dz-eq-mute">4 / 5 · proposée par Marc</span>
      </div>
      <div class="dz-eq-box">
        <div class="dz-eq-box-t">Pour 2027</div>
        <div class="dz-eq-kit"><i class="fas fa-graduation-cap"></i><span>Formation « Manager une équipe technique »</span></div>
        <div class="dz-eq-kit"><i class="fas fa-arrow-up"></i><span>Évolution visée : Engineering manager</span></div>
        <div class="dz-eq-kit"><i class="fas fa-euro-sign"></i><span>Révision salariale : proposée au comité</span></div>
      </div>
    </aside>
  </div>
</div>
"""


# ------------------------------------------------------------------ 11. anniversaires et arrivées
def cel(ini, what, when, badge=None, today=False):
    b = f'<span class="dz-eq-years">{badge}</span>' if badge else ""
    return (f'<div class="dz-eq-cel{" dz-eq-cel-today" if today else ""}">{av(ini, " dz-eq-av-md")}<span class="dz-eq-cel-t"><b>{name(ini)}</b><small>{what}</small></span>'
            f'{b}<span class="dz-eq-when">{when}</span></div>')


CELEBRATIONS = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">À fêter cette semaine</h3>
    <span class="dz-eq-mute">21 → 27 sept.</span>
    <span class="dz-eq-sp"></span>
    <a class="dz-eq-btn dz-confetti" href="#"><i class="fas fa-glass-cheers"></i> Envoyer des confettis</a>
  </div>
  <div class="dz-eq-cels">
    <div class="dz-eq-celcol">
      <div class="dz-eq-celh"><span class="dz-eq-ticon dz-eq-ticon-sm dz-eq-c3"><i class="fas fa-birthday-cake"></i></span><b>Anniversaires</b><span class="dz-eq-count">3</span></div>
      {cel("SM", "Design", "Aujourd'hui", today=True)}
      {cel("JP", "Finance", "Sam. 26")}
      {cel("RN", "Produit", "Dim. 27")}
    </div>
    <div class="dz-eq-celcol">
      <div class="dz-eq-celh"><span class="dz-eq-ticon dz-eq-ticon-sm dz-eq-c5"><i class="fas fa-award"></i></span><b>Ancienneté</b><span class="dz-eq-count">3</span></div>
      {cel("NO", "Support client", "Jeu. 24", "5 ans", True)}
      {cel("KB", "Plateforme", "Ven. 25", "3 ans")}
      {cel("ZA", "Support client", "Lun. 28", "1 an")}
    </div>
    <div class="dz-eq-celcol">
      <div class="dz-eq-celh"><span class="dz-eq-ticon dz-eq-ticon-sm dz-eq-c4"><i class="fas fa-hand-sparkles"></i></span><b>Arrivées</b><span class="dz-eq-count">2</span></div>
      <div class="dz-eq-newbie">{av("EV", " dz-eq-av-lg")}<div><b>Emma Vidal</b><small>Développeuse front-end · 5 oct.</small><p>Vient de Bordeaux, grimpe le week-end et prépare les meilleurs cannelés.</p></div></div>
      <div class="dz-eq-newbie">{av("YT", " dz-eq-av-lg")}<div><b>Yanis Traoré</b><small>Chargé de recrutement · 12 oct.</small><p>Ancien coach de basket, il va remplir nos 6 postes ouverts.</p></div></div>
    </div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 12. sondage d'humeur (eNPS)
def theme(t, v, d, up=True):
    return (f'<div class="dz-eq-theme"><span class="dz-eq-theme-t">{t}</span>{meter(v * 10, 4 if v >= 7.5 else (5 if v >= 6.5 else 6), " dz-eq-meter-lg")}'
            f'<b class="dz-eq-theme-v">{str(v).replace(".", ",")}</b><span class="dz-eq-trend{"" if up else " dz-eq-trend-down"}"><i class="fas fa-arrow-{"up" if up else "down"}"></i> {d}</span></div>')


ENPS_SPARK = """<svg class="dz-eq-spark" viewBox="0 0 160 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0 34 L27 30 L53 32 L80 24 L107 20 L133 14 L160 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>"""

ENPS = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Baromètre d'humeur</h3><span class="dz-eq-pill dz-eq-c4">Anonyme</span>
    <span class="dz-eq-sp"></span>
    <div class="dz-eq-seg"><a href="#">T2</a><a href="#" class="dz-active">T3 2026</a></div>
  </div>
  <div class="dz-eq-enps">
    <div class="dz-eq-gauge-card">
      <div class="dz-eq-gauge" style="--v:66%"><div class="dz-eq-gauge-in"><b>+32</b><small>eNPS</small></div></div>
      <div class="dz-eq-gauge-scale"><span>−100</span><span>+100</span></div>
      <div class="dz-eq-split">
        <span class="dz-eq-split-p" style="--w:48%"></span><span class="dz-eq-split-n" style="--w:36%"></span><span class="dz-eq-split-d" style="--w:16%"></span>
      </div>
      <div class="dz-eq-split-l"><span class="dz-eq-c4"><b>48 %</b> promoteurs</span><span class="dz-eq-cx"><b>36 %</b> passifs</span><span class="dz-eq-c6"><b>16 %</b> détracteurs</span></div>
    </div>
    <div class="dz-eq-enps-mid">
      <div class="dz-eq-minikpis">
        <div class="dz-eq-minikpi"><small>Participation</small><b>84 %</b><span class="dz-eq-trend"><i class="fas fa-arrow-up"></i> 6 pts</span></div>
        <div class="dz-eq-minikpi dz-eq-minikpi-spark"><small>Évolution sur 6 trimestres</small><b>+32</b><span class="dz-eq-c4 dz-eq-sparkw">{ENPS_SPARK}</span></div>
      </div>
      <div class="dz-eq-sub-h">Par thème</div>
      {theme("Sens du travail", 8.4, "0,3")}
      {theme("Management", 8.1, "0,5")}
      {theme("Ambiance", 7.9, "0,1")}
      {theme("Charge de travail", 6.2, "0,8", False)}
      {theme("Rémunération", 6.8, "0,2")}
    </div>
    <div class="dz-eq-verbatims">
      <div class="dz-eq-sub-h">Verbatims</div>
      <div class="dz-eq-verb dz-eq-c4"><p>« Les rituels d'équipe sont vraiment utiles, et on se sent écouté. »</p><small>Tech · promoteur</small></div>
      <div class="dz-eq-verb dz-eq-c6"><p>« La fin de trimestre a été intense, on manque de monde au support. »</p><small>Support · détracteur</small></div>
      <div class="dz-eq-verb dz-eq-c5"><p>« J'aimerais plus de visibilité sur les évolutions possibles. »</p><small>Produit · passif</small></div>
    </div>
  </div>
  <div class="dz-eq-ask">
    <b>Recommanderiez-vous Nexora comme employeur à un proche ?</b>
    <div class="dz-eq-nps">{"".join(f'<a class="dz-eq-npsb{" dz-active" if i == 9 else ""}" href="#">{i}</a>' for i in range(11))}</div>
    <div class="dz-eq-nps-l"><span>Pas du tout</span><span>Tout à fait</span></div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 13. feuille de temps
def trow(c, proj, client, hours):
    cells = "".join(f'<span class="dz-eq-tc{" dz-eq-tc-we" if i >= 5 else ""}{" dz-eq-tc-0" if h == "" else ""}">{h or "–"}</span>' for i, h in enumerate(hours))
    tot = sum(float(h.replace(",", ".")) for h in hours if h)
    return (f'<div class="dz-eq-trow"><span class="dz-eq-tproj"><span class="dz-eq-sdot dz-eq-c{c}"></span><span><b>{proj}</b><small>{client}</small></span></span>'
            f'{cells}<span class="dz-eq-ttot">{f"{tot:g}".replace(".", ",")} h</span></div>')


TIMESHEET = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Feuille de temps</h3>
    <a class="dz-eq-ibtn" href="#" aria-label="Semaine précédente"><i class="fas fa-chevron-left"></i></a>
    <b class="dz-eq-period">Semaine 39 · 21 → 27 sept.</b>
    <a class="dz-eq-ibtn" href="#" aria-label="Semaine suivante"><i class="fas fa-chevron-right"></i></a>
    <span class="dz-eq-sp"></span>
    {pill("Brouillon", 5)}
    <a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-paper-plane"></i> Soumettre</a>
  </div>
  <div class="dz-eq-ts">
    <div class="dz-eq-ts-in">
      <div class="dz-eq-trow dz-eq-thead"><span class="dz-eq-tproj">Projet</span>{"".join(f'<span class="dz-eq-tc{" dz-eq-tc-we" if i >= 5 else ""}{" dz-eq-tc-today" if i == 3 else ""}"><small>{d}</small><b>{n}</b></span>' for i, (d, n) in enumerate(zip(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], range(21, 28))))}<span class="dz-eq-ttot">Total</span></div>
      {trow(1, "Application mobile 3.0", "Interne · développement", ["4", "5,5", "3", "6", "", "", ""])}
      {trow(2, "Refonte portail Atelier Lune", "Client · facturable", ["2", "1,5", "4", "1", "", "", ""])}
      {trow(3, "Revues de code", "Interne", ["1", "0,5", "0,5", "", "", "", ""])}
      {trow(5, "Réunions &amp; rituels", "Interne", ["1", "0,5", "", "0,5", "", "", ""])}
      <a class="dz-eq-tadd" href="#"><i class="fas fa-plus"></i> Ajouter une ligne</a>
      <div class="dz-eq-trow dz-eq-tfoot"><span class="dz-eq-tproj">Total jour</span>{"".join(f'<span class="dz-eq-tc{" dz-eq-tc-we" if i >= 5 else ""}"><b>{h}</b><span class="dz-eq-tbar" style="--v:{p}%"></span></span>' for i, (h, p) in enumerate([("8", 100), ("8", 100), ("7,5", 94), ("7,5", 94), ("0", 0), ("–", 0), ("–", 0)]))}<span class="dz-eq-ttot">31 h</span></div>
    </div>
  </div>
  <div class="dz-eq-foot">
    <span class="dz-eq-tsum"><b>31 h</b> sur 35 h</span>{meter(89, 1, " dz-eq-tsum-m")}
    <span class="dz-eq-mute dz-eq-hide-sm">dont 8,5 h facturables · 27 %</span>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-mute"><i class="fas fa-lock"></i> Clôture vendredi 18:00</span>
  </div>
</div>
"""


# ------------------------------------------------------------------ 14. page carrières
def job(title, dept, c, place, contract, salary, new=False, remote=None):
    n = '<span class="dz-eq-new">Nouveau</span>' if new else ""
    r = f'<span><i class="fas fa-house-user"></i> {remote}</span>' if remote else ""
    return (f'<a class="dz-eq-job" href="#"><div class="dz-eq-job-t"><b>{title}</b>{n}<div class="dz-eq-job-m">{tag(dept, c)}'
            f'<span><i class="fas fa-map-marker-alt"></i> {place}</span><span><i class="far fa-file-alt"></i> {contract}</span>{r}</div></div>'
            f'<span class="dz-eq-job-s">{salary}</span><span class="dz-eq-job-go"><i class="fas fa-arrow-right"></i></span></a>')


CAREERS = f"""
<div class="dz-eq-careers">
  <div class="dz-eq-car-hero">
    <span class="dz-eq-eyebrow"><i class="fas fa-circle"></i> 6 postes ouverts</span>
    <h2 class="dz-eq-car-h">Construisons les outils que vous auriez aimé avoir.</h2>
    <p class="dz-eq-lead">Chez Nexora, 48 personnes aident 3 000 artisans à gérer leur activité. On travaille en petites équipes autonomes, à Paris, Lyon, Nantes ou depuis chez vous.</p>
    <div class="dz-eq-car-stats"><div><b>48</b><small>personnes</small></div><div><b>4,6/5</b><small>bien-être au travail</small></div><div><b>2 j</b><small>de télétravail et plus</small></div><div><b>42 %</b><small>de femmes en tech</small></div></div>
  </div>
  <div class="dz-eq-filters dz-chips dz-eq-filters-plain">
    <a class="dz-eq-fchip dz-chip dz-active" href="#">Tous les postes <span>6</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Tech <span>3</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Produit <span>1</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">Support <span>1</span></a>
    <a class="dz-eq-fchip dz-chip" href="#">RH <span>1</span></a>
  </div>
  <div class="dz-eq-jobs">
    {job("Ingénieur·e back-end senior", "Tech", 2, "Paris", "CDI", "58–68 k€", True, "Hybride")}
    {job("Ingénieur·e sécurité", "Tech", 2, "Lyon", "CDI", "55–65 k€", True, "Hybride")}
    {job("Développeur·se mobile", "Tech", 2, "Nantes", "CDI", "45–55 k€", remote="Télétravail complet")}
    {job("Product designer confirmé·e", "Produit", 7, "Paris", "CDI", "48–56 k€", remote="Hybride")}
    {job("Chargé·e de clientèle", "Support", 6, "Lyon", "CDI", "32–36 k€")}
    {job("Alternant·e RH", "RH", 5, "Paris", "Alternance · 24 mois", "Selon grille")}
  </div>
  <div class="dz-eq-perks">
    <div><i class="fas fa-laptop-house"></i><b>Télétravail souple</b><small>+ 600 € pour équiper votre bureau</small></div>
    <div><i class="fas fa-heartbeat"></i><b>Mutuelle prise à 100 %</b><small>pour vous et vos enfants</small></div>
    <div><i class="fas fa-book-open"></i><b>1 500 € de formation</b><small>par an et par personne</small></div>
    <div><i class="fas fa-baby"></i><b>Congé second parent</b><small>8 semaines rémunérées</small></div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 15. trombinoscope
def face(ini, seed, dept, pres=None):
    p = f'<span class="dz-eq-face-pres dz-eq-pres-{pres}"></span>' if pres else ""
    return (f'<a class="dz-eq-face" href="#"><div class="dz-eq-face-img"><img class="dz-cover" src="https://picsum.photos/seed/{seed}/400/480" alt="{name(ini)}">{p}</div>'
            f'<div class="dz-eq-face-t"><b>{name(ini)}</b><small>{role(ini)}</small></div><span class="dz-eq-face-d">{dept}</span></a>')


FACES = f"""
<div class="dz-eq-teams-head">
  <div><h2 class="dz-eq-h">Trombinoscope</h2><p class="dz-eq-lead">Mettez un visage sur chaque nom — 48 personnes, 3 bureaux.</p></div>
  <div class="dz-eq-filters dz-chips dz-eq-filters-plain"><a class="dz-eq-fchip dz-chip dz-active" href="#">Tous</a><a class="dz-eq-fchip dz-chip" href="#">Paris</a><a class="dz-eq-fchip dz-chip" href="#">Lyon</a><a class="dz-eq-fchip dz-chip" href="#">Nantes</a></div>
</div>
<div class="dz-eq-faces dz-stagger">
  {face("CD", "claire", "Direction", "on")}
  {face("MR", "marc", "Tech", "on")}
  {face("SM", "sofia", "Produit", "away")}
  {face("LM", "lea", "Tech", "on")}
  {face("KB", "karim", "Tech")}
  {face("IL", "ines", "RH", "on")}
  {face("NO", "nadia", "Support", "on")}
  {face("HF", "hugo", "Tech", "away")}
  {face("OR", "olivia", "Produit")}
  {face("JP", "julien", "Finance", "on")}
</div>
"""


# ------------------------------------------------------------------ 16. notes de frais d'équipe
def exp(ini, what, cat, icon, date, amount, status, sel=False, receipt=True):
    r = '<i class="fas fa-paperclip dz-eq-rcpt"></i>' if receipt else '<i class="fas fa-exclamation-triangle dz-eq-norcpt" title="Justificatif manquant"></i>'
    return (f'<a class="dz-eq-exp{" dz-eq-exp-sel" if sel else ""}" href="#"><span class="dz-eq-check{" dz-eq-check-on" if sel else ""}"></span>'
            f'{av(ini, " dz-eq-av-md")}<span class="dz-eq-exp-t"><b>{what}</b><small>{name(ini)} · {date}</small></span>'
            f'<span class="dz-eq-exp-c dz-eq-hide-sm"><i class="{icon}"></i> {cat}</span>{r}'
            f'<span class="dz-eq-exp-a">{amount}</span>{status}</a>')


EXPENSES = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Notes de frais de l'équipe</h3><span class="dz-eq-count">7</span>
    <span class="dz-eq-sp"></span>
    <div class="dz-eq-seg"><a href="#" class="dz-active">À valider</a><a href="#">Validées</a><a href="#">Remboursées</a></div>
  </div>
  <div class="dz-eq-kpis">
    <div class="dz-eq-kpi"><small>À valider</small><b>1 842,60 €</b><span class="dz-eq-mute">7 notes · 4 personnes</span></div>
    <div class="dz-eq-kpi"><small>Remboursé en septembre</small><b>6 215,00 €</b><span class="dz-eq-trend dz-eq-trend-down"><i class="fas fa-arrow-down"></i> 12 % vs août</span></div>
    <div class="dz-eq-kpi"><small>Budget déplacements T3</small><b>64 %</b>{meter(64, 5)}</div>
  </div>
  <div class="dz-eq-bulk"><span class="dz-eq-check dz-eq-check-mid"></span><b>3 sélectionnées</b><span class="dz-eq-mute">· 1 128,40 €</span><span class="dz-eq-sp"></span><a class="dz-eq-btn dz-eq-hide-sm" href="#"><i class="fas fa-times"></i> Refuser</a><a class="dz-eq-btn dz-eq-btn-primary" href="#"><i class="fas fa-check"></i> Approuver</a></div>
  <div class="dz-eq-exps">
    {exp("LM", "Train Paris ⇄ Lyon · atelier client", "Transport", "fas fa-train", "22 sept.", "186,40 €", pill("Soumise", 7), True)}
    {exp("TG", "Hôtel 2 nuits · salon DevCon", "Hébergement", "fas fa-bed", "18 sept.", "842,00 €", pill("Soumise", 7), True)}
    {exp("SM", "Déjeuner équipe design", "Repas", "fas fa-utensils", "17 sept.", "100,00 €", pill("Soumise", 7), True)}
    {exp("KB", "Clavier ergonomique", "Matériel", "fas fa-keyboard", "15 sept.", "129,90 €", pill("Justificatif ?", 5), receipt=False)}
    {exp("LM", "Taxi aéroport", "Transport", "fas fa-taxi", "12 sept.", "54,30 €", pill("Soumise", 7))}
  </div>
</div>
"""


# ------------------------------------------------------------------ 17. matrice de compétences
SKILLS = ["Swift", "Kotlin", "React", "Go", "SQL", "Infra", "Sécurité", "UX"]
MATRIX = [("LM", [4, 3, 2, 0, 2, 1, 1, 2]), ("KB", [0, 1, 1, 4, 4, 2, 2, 0]), ("HF", [0, 0, 1, 3, 3, 4, 3, 0]),
          ("EV", [1, 2, 4, 0, 1, 0, 0, 3]), ("TG", [2, 2, 2, 1, 2, 1, 1, 1]), ("SM", [0, 0, 2, 0, 0, 0, 0, 4])]


def mrow(ini, lv):
    return (f'<div class="dz-eq-mrow"><span class="dz-eq-mwho">{av(ini)}<span>{name(ini)}</span></span>'
            + "".join(f'<span class="dz-eq-lv dz-eq-lv-{v}">{v or ""}</span>' for v in lv) + "</div>")


COVER = [(sum(1 for _, l in MATRIX if l[i] >= 3)) for i in range(len(SKILLS))]

SKILLMATRIX = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Matrice de compétences · Équipe mobile &amp; plateforme</h3>
    <span class="dz-eq-sp"></span>
    <span class="dz-eq-mlegend dz-eq-hide-sm"><span class="dz-eq-lv dz-eq-lv-1">1</span> Notions <span class="dz-eq-lv dz-eq-lv-2">2</span> Pratique <span class="dz-eq-lv dz-eq-lv-3">3</span> Autonome <span class="dz-eq-lv dz-eq-lv-4">4</span> Référent</span>
  </div>
  <div class="dz-eq-mx">
    <div class="dz-eq-mx-in">
      <div class="dz-eq-mrow dz-eq-mhead"><span class="dz-eq-mwho"><span class="dz-eq-mute">6 personnes · 8 compétences</span></span>{"".join(f'<span class="dz-eq-msk">{s}</span>' for s in SKILLS)}</div>
      {"".join(mrow(i, l) for i, l in MATRIX)}
      <div class="dz-eq-mrow dz-eq-mfoot"><span class="dz-eq-mwho"><b>Couverture</b><small class="dz-eq-mute">niveau 3 ou plus</small></span>{"".join(f'<span class="dz-eq-mcov{" dz-eq-mcov-risk" if c < 2 else ""}">{c}</span>' for c in COVER)}</div>
    </div>
  </div>
  <div class="dz-eq-foot"><span class="dz-eq-warn dz-eq-warn-inline"><i class="fas fa-exclamation-triangle"></i><span><b>Risque de dépendance</b> : Swift, Kotlin et React n'ont qu'une seule personne autonome.</span></span><span class="dz-eq-sp"></span><a class="dz-eq-btn" href="#"><i class="fas fa-graduation-cap"></i> Plan de formation</a></div>
</div>
"""


# ------------------------------------------------------------------ 18. plan de relève
def nine(label, c, people, hl=False):
    p = "".join(av(i) for i in people)
    return f'<div class="dz-eq-nine-c dz-eq-c{c}{" dz-eq-nine-hl" if hl else ""}"><small>{label}</small><span class="dz-eq-nine-p">{p}</span></div>'


def succ(ini, ready, c):
    return f'<div class="dz-eq-succ">{av(ini)}<span><b>{name(ini)}</b><small>{role(ini)}</small></span>{pill(ready, c)}</div>'


def keypos(title, holder, risk, rc, succs):
    return (f'<div class="dz-eq-kp"><div class="dz-eq-kp-h"><span class="dz-eq-kp-t"><b>{title}</b><small>Titulaire : {name(holder)}</small></span>'
            f'<span class="dz-eq-risk dz-eq-c{rc}">Risque {risk}</span></div>{"".join(succs)}</div>')


SUCCESSION = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Plan de relève 2026</h3><span class="dz-eq-pill dz-eq-c6">Confidentiel</span>
    <span class="dz-eq-sp"></span>
    <a class="dz-eq-btn" href="#"><i class="fas fa-filter"></i> Direction &amp; leads</a>
  </div>
  <div class="dz-eq-succession">
    <div class="dz-eq-ninebox">
      <div class="dz-eq-box-t">Performance × potentiel</div>
      <div class="dz-eq-nine-wrap">
        <span class="dz-eq-axis-y">Potentiel</span>
        <div class="dz-eq-nine">
          {nine("Talent à révéler", 5, ["EV"])}
          {nine("Futur leader", 4, ["RN"])}
          {nine("Étoile", 1, ["LM", "BM"], True)}
          {nine("À accompagner", 6, [])}
          {nine("Pilier", 5, ["TG", "ZA", "CG"])}
          {nine("Performant", 4, ["KB", "SM"])}
          {nine("À risque", 6, [])}
          {nine("Contributeur", 7, ["JP"])}
          {nine("Expert", 7, ["HF", "NO"])}
        </div>
        <span class="dz-eq-axis-x">Performance</span>
      </div>
    </div>
    <div class="dz-eq-kps">
      {keypos("Direction technique", "MR", "moyen", 5, [succ("LM", "Prêt·e d'ici 1 an", 4), succ("HF", "2 à 3 ans", 5)])}
      {keypos("Responsable support", "NO", "élevé", 6, [succ("ZA", "2 à 3 ans", 5), '<div class="dz-eq-succ dz-eq-succ-gap"><span class="dz-eq-av dz-eq-av-none"><i class="fas fa-plus"></i></span><span><b>Aucun successeur prêt</b><small>Recrutement externe à prévoir</small></span></div>'])}
      {keypos("Direction financière", "PL", "faible", 4, [succ("JP", "Prêt·e maintenant", 1)])}
    </div>
  </div>
</div>
"""


# ------------------------------------------------------------------ 19. effectifs (tableau de bord RH)
HEADCOUNT_SVG = """<svg class="dz-eq-hc-svg" viewBox="0 0 300 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70 L25 68 L50 66 L75 62 L100 60 L125 55 L150 52 L175 46 L200 44 L225 36 L250 30 L275 24 L300 18 L300 90 L0 90Z" fill="currentColor" opacity=".14"/><path d="M0 70 L25 68 L50 66 L75 62 L100 60 L125 55 L150 52 L175 46 L200 44 L225 36 L250 30 L275 24 L300 18" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>"""


def dept_row(d, n, v, c):
    return f'<div class="dz-eq-drep"><span class="dz-eq-sdot dz-eq-c{c}"></span><span>{d}</span>{meter(v, c)}<b>{n}</b></div>'


HEADCOUNT = f"""
<div class="dz-eq-shell">
  <div class="dz-eq-head">
    <h3 class="dz-eq-title">Effectifs</h3><span class="dz-eq-mute">au 24 sept. 2026</span>
    <span class="dz-eq-sp"></span>
    <div class="dz-eq-seg"><a href="#">Trimestre</a><a href="#" class="dz-active">12 mois</a></div>
  </div>
  <div class="dz-eq-kpis dz-eq-kpis-4">
    <div class="dz-eq-kpi"><small>Effectif total</small><b class="dz-counter">48</b><span class="dz-eq-trend"><i class="fas fa-arrow-up"></i> +11 sur 12 mois</span></div>
    <div class="dz-eq-kpi"><small>Arrivées / départs</small><b>14 / 3</b><span class="dz-eq-mute">dont 2 en période d'essai</span></div>
    <div class="dz-eq-kpi"><small>Turnover annuel</small><b>6,8 %</b><span class="dz-eq-trend"><i class="fas fa-arrow-down"></i> 2,1 pts</span></div>
    <div class="dz-eq-kpi"><small>Délai de recrutement</small><b>34 j</b><span class="dz-eq-trend dz-eq-trend-down"><i class="fas fa-arrow-up"></i> 5 j</span></div>
  </div>
  <div class="dz-eq-hc">
    <div class="dz-eq-hc-chart">
      <div class="dz-eq-box-t">Évolution de l'effectif</div>
      <div class="dz-eq-hc-plot dz-eq-c1">{HEADCOUNT_SVG}</div>
      <div class="dz-eq-hc-x"><span>oct. 25</span><span>janv.</span><span>avr.</span><span>juil.</span><span>sept. 26</span></div>
    </div>
    <div class="dz-eq-hc-rep">
      <div class="dz-eq-box-t">Répartition</div>
      {dept_row("Tech", 18, 100, 2)}
      {dept_row("Opérations", 14, 78, 3)}
      {dept_row("Produit", 9, 50, 7)}
      {dept_row("Finance", 6, 33, 4)}
      {dept_row("Direction", 1, 6, 1)}
      <div class="dz-eq-parity"><span>Parité</span><span class="dz-eq-parity-bar" style="--v:46%"></span><small>46 % femmes · 54 % hommes</small></div>
    </div>
  </div>
</div>
"""


BLOCKS = [
    dict(name="organigramme", icon="fas fa-sitemap", wrap="section", html=ORG),
    dict(name="annuaire", icon="fas fa-address-book", wrap="section", html=DIRECTORY),
    dict(name="fiche membre", icon="fas fa-id-card", wrap="section", html=PROFILE),
    dict(name="cartes équipe", icon="fas fa-users", wrap="section", html=TEAMS),
    dict(name="trombinoscope", icon="fas fa-portrait", wrap="section", html=FACES),
    dict(name="effectifs", icon="fas fa-chart-area", wrap="section", html=HEADCOUNT),
    dict(name="demande de congés", icon="fas fa-umbrella-beach", wrap="section", html=LEAVE),
    dict(name="calendrier des absences", icon="fas fa-calendar-alt", wrap="section", html=ABSENCES),
    dict(name="pipeline de recrutement", icon="fas fa-filter", wrap="section", html=PIPELINE),
    dict(name="fiche candidat", icon="fas fa-user-tie", wrap="section", html=CANDIDATE),
    dict(name="page carrières", icon="fas fa-briefcase", wrap="section", html=CAREERS),
    dict(name="onboarding", icon="fas fa-rocket", wrap="section", html=ONBOARDING),
    dict(name="entretien annuel", icon="fas fa-comments", wrap="section", html=REVIEW),
    dict(name="anniversaires et arrivées", icon="fas fa-birthday-cake", wrap="section", html=CELEBRATIONS),
    dict(name="baromètre d'humeur", icon="far fa-smile", wrap="section", html=ENPS),
    dict(name="feuille de temps", icon="far fa-clock", wrap="section", html=TIMESHEET),
    dict(name="notes de frais", icon="fas fa-receipt", wrap="section", html=EXPENSES),
    dict(name="matrice de compétences", icon="fas fa-th", wrap="section", html=SKILLMATRIX),
    dict(name="plan de relève", icon="fas fa-chess", wrap="section", html=SUCCESSION),
]
