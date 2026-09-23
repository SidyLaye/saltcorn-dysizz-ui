"""Génère packs/blocks.json (Library du builder) et packs/demo-pages.json.

Les blocs sont écrits dans le format de layout natif de Saltcorn 1.6
(container / blank / link / besides / above), pour rester modifiables au
glisser-déposer. Les widgets qui ont besoin d'une structure précise
(tarifs avec bascule, FAQ, défilement de logos, barre du bas…) sont des
éléments « HTML code », modifiables en code dans le builder.

Lancer :  python3 tools/build_packs.py
"""
import json, os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)


# ------------------------------------------------------------------ aides
def box(cls, *children, el="div", full=False, cid=None, **extra):
    """Conteneur natif (élément Container du builder)."""
    seg = {"type": "container", "customClass": cls, "htmlElement": el,
           "display": "block", "contents": above(*children)}
    if full:
        seg["fullPageWidth"] = True
    if cid:
        seg["customId"] = cid
    seg.update(extra)
    return seg


def above(*children):
    ch = [c for c in children if c is not None]
    if len(ch) == 1:
        return ch[0]
    return {"above": ch}


def text(html, style=None, cls="", block=True):
    """Élément Texte natif. style = h1…h6 ou None."""
    seg = {"type": "blank", "contents": html, "block": block, "customClass": cls}
    if style:
        seg["textStyle"] = style
    return seg


def html(code):
    """Élément HTML code."""
    return {"type": "blank", "isHTML": True, "contents": textwrap.dedent(code).strip()}


def link(label, url, cls="dz-btn", icon=""):
    return {"type": "link", "text": label, "url": url, "link_src": "URL",
            "link_style": "", "link_class": cls, "link_icon": icon}


def cols(children, widths, bp="lg", cls="", valign=None):
    seg = {"besides": children, "widths": widths, "breakpoints": [bp] * len(children), "customClass": cls}
    if valign:
        seg["vAligns"] = [valign] * len(children)
    return seg


def section(inner, cls="dz-section", narrow=False, cid=None, extra_first=None):
    kids = [extra_first] if extra_first else []
    kids.append(box("dz-container-narrow" if narrow else "dz-container", *inner) if isinstance(inner, list) else box("dz-container-narrow" if narrow else "dz-container", inner))
    return box(cls, *kids, el="section", full=True, cid=cid)


def head(eyebrow, title, lead, left=False):
    return box("dz-section-head dz-reveal" + (" dz-left" if left else ""),
               text(eyebrow, cls="dz-eyebrow", block=False) if eyebrow else None,
               text(title, "h2", "dz-h2"),
               text(lead, cls="dz-lead") if lead else None)


def reveal(seg, kind="up"):
    """Ajoute l'apparition au défilement à un conteneur (attribut via classe)."""
    seg = dict(seg)
    seg["customClass"] = (seg.get("customClass", "") + " dz-reveal").strip()
    return seg


def feature_card(icon, title, body, extra_cls=""):
    return box(("dz-card dz-card-hover dz-spotlight " + extra_cls).strip(),
               html(f'<span class="dz-icon"><i class="{icon}"></i></span>'),
               text(title, "h4", "dz-h4"),
               text(body, cls="dz-text"))


LIB = []


def add(name, icon, layout):
    LIB.append({"name": "DZ · " + name, "icon": icon, "layout": layout})
    return layout


# ============================================================ NAVIGATION
NAV = add("Navigation · landing", "fas fa-bars", html("""
<header class="dz-nav">
  <div class="dz-container dz-nav-inner">
    <a class="dz-brand" href="/"><span class="dz-brand-mark"></span>Marque</a>
    <nav class="dz-nav-links">
      <a href="#fonctionnalites">Fonctionnalités</a>
      <a href="#tarifs">Tarifs</a>
      <a href="#temoignages">Clients</a>
      <a href="#faq">FAQ</a>
    </nav>
    <div class="dz-cluster" style="--dz-gap:.5rem">
      <button class="dz-btn dz-btn-ghost dz-icon-btn dz-theme-btn" data-dz-theme-toggle aria-label="Changer de thème"><i class="fas fa-moon dz-moon"></i><i class="fas fa-sun dz-sun"></i></button>
      <a class="dz-btn dz-btn-ghost dz-btn-sm dz-nav-cta" href="/auth/login">Connexion</a>
      <a class="dz-btn dz-btn-sm dz-nav-cta" href="/auth/signup">Commencer</a>
      <button class="dz-nav-burger" data-dz-menu-toggle="#dz-mobile-menu" aria-label="Menu"><i class="fas fa-bars"></i></button>
    </div>
  </div>
</header>
<div class="dz-nav-spacer"></div>
<nav class="dz-mobile-menu" id="dz-mobile-menu">
  <a href="#fonctionnalites">Fonctionnalités</a>
  <a href="#tarifs">Tarifs</a>
  <a href="#temoignages">Clients</a>
  <a href="#faq">FAQ</a>
  <a class="dz-btn dz-btn-block" style="margin-top:1rem;border:0" href="/auth/signup">Commencer gratuitement</a>
</nav>
<div class="dz-scroll-progress"></div>
"""))

# ============================================================ HEROS
HERO_AURORA = add("Hero · aurora centré", "fas fa-star", box(
    "dz-hero dz-center",
    html('<div class="dz-aurora"></div>'),
    box("dz-container-narrow",
        html('<a class="dz-announce" href="#" data-dz-reveal><strong>Nouveau</strong> Découvrez la version 2.0 <i class="fas fa-arrow-right"></i></a>'),
        text('Construisez plus vite, <span class="dz-gradient-text">sans compromis</span>', "h1", "dz-display dz-reveal", ),
        text("Une plateforme pensée pour aller de l'idée au lancement en quelques jours. Belle sur tous les écrans, rapide, sécurisée.", cls="dz-lead dz-reveal"),
        box("dz-cluster dz-reveal",
            link("Commencer gratuitement", "#", "dz-btn dz-btn-lg dz-btn-shine dz-magnetic", "fas fa-arrow-right"),
            link("Voir la démo", "#", "dz-btn dz-btn-lg dz-btn-ghost", "fas fa-play")),
        html("""
        <div class="dz-cluster dz-reveal" style="justify-content:center;margin-top:2.2rem;--dz-gap:.9rem">
          <div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">AL</span><span class="dz-avatar dz-avatar-sm" style="background:linear-gradient(135deg,#f472b6,#fb923c)">MK</span><span class="dz-avatar dz-avatar-sm" style="background:linear-gradient(135deg,#22d3ee,#10b981)">SD</span><span class="dz-avatar dz-avatar-sm" style="background:linear-gradient(135deg,#f59e0b,#ef4444)">+</span></div>
          <div class="dz-small" style="text-align:left"><span class="dz-stars">★★★★★</span><br>Déjà adopté par <b>2 400+</b> équipes</div>
        </div>""")),
    el="section", full=True))

MOCK = """
<div class="dz-browser dz-float-slow">
  <div class="dz-mock">
    <div class="dz-mock-side"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="dz-mock-main">
      <div class="dz-mock-top"><span class="dz-mock-line dz-dark" style="--w:120px"></span><span class="dz-badge dz-badge-success"><span class="dz-dot"></span>En ligne</span></div>
      <div class="dz-mock-kpis">
        <div><span class="dz-small">Revenus</span><b>48,2 k€</b><span class="dz-trend dz-trend-up">▲ 12 %</span></div>
        <div><span class="dz-small">Clients</span><b>1 284</b><span class="dz-trend dz-trend-up">▲ 8 %</span></div>
        <div><span class="dz-small">Churn</span><b>1,9 %</b><span class="dz-trend dz-trend-down">▼ 0,4</span></div>
      </div>
      <div class="dz-mock-chart"><span style="--h:35%;--i:0"></span><span style="--h:52%;--i:1"></span><span style="--h:44%;--i:2"></span><span style="--h:68%;--i:3"></span><span style="--h:58%;--i:4"></span><span style="--h:80%;--i:5"></span><span style="--h:72%;--i:6"></span><span style="--h:92%;--i:7"></span><span style="--h:84%;--i:8"></span><span style="--h:100%;--i:9"></span></div>
    </div>
  </div>
</div>"""

HERO_SPLIT = add("Hero · texte + visuel", "fas fa-columns", box(
    "dz-hero dz-bg-mesh",
    box("dz-container",
        box("dz-split",
            box("dz-mobile-center",
                text('<span class="dz-dot"></span> Disponible maintenant', cls="dz-badge dz-reveal", block=False),
                text('Votre activité, <span class="dz-gradient-text">enfin pilotée</span> au même endroit', "h1", "dz-h1 dz-reveal"),
                text("Clients, ventes, équipes et automatisations dans une seule interface. Moins d'outils, plus de résultats.", cls="dz-lead dz-reveal"),
                box("dz-cluster dz-reveal",
                    link("Essayer 14 jours", "#", "dz-btn dz-btn-lg dz-btn-gradient", "fas fa-arrow-right"),
                    link("Parler à un expert", "#", "dz-btn dz-btn-lg dz-btn-ghost")),
                text('<i class="fas fa-check" style="color:var(--dz-success)"></i> Sans carte bancaire &nbsp; <i class="fas fa-check" style="color:var(--dz-success)"></i> Annulable à tout moment', cls="dz-small dz-reveal")),
            box("dz-glow-under",
                html(f"""
                <div style="position:relative" data-dz-reveal="zoom">
                  <div data-dz-tilt="6">{MOCK}</div>
                  <div class="dz-float-card dz-float" style="left:-28px;bottom:36px"><span class="dz-icon dz-icon-round" style="width:38px;height:38px;font-size:1rem"><i class="fas fa-bolt"></i></span><div><b>+32 % de conversions</b><span class="dz-small">ce mois-ci</span></div></div>
                  <div class="dz-float-card dz-float-slow" style="right:-18px;top:28px"><span class="dz-avatar dz-avatar-sm">JD</span><div><b>Nouveau client</b><span class="dz-small">il y a 2 min</span></div></div>
                </div>""")))),
    el="section", full=True))

HERO_TYPED = add("Hero · plein écran + texte animé", "fas fa-keyboard", box(
    "dz-hero dz-hero-full dz-section-dark dz-noise dz-center",
    html('<div class="dz-aurora"></div>'),
    box("dz-container-narrow",
        text("Studio numérique", cls="dz-eyebrow dz-reveal", block=False),
        html('<h1 class="dz-display dz-reveal">On crée des <br><span class="dz-gradient-text" data-dz-typed="sites qui vendent|apps qui plaisent|outils qui libèrent">sites qui vendent</span></h1>'),
        text("Design, développement et automatisation. Des produits rapides, beaux et pensés pour vos clients.", cls="dz-lead dz-reveal"),
        box("dz-cluster dz-reveal",
            link("Démarrer un projet", "#contact", "dz-btn dz-btn-lg dz-btn-light dz-magnetic", "fas fa-arrow-right"),
            link("Nos réalisations", "#", "dz-btn dz-btn-lg dz-btn-glow"))),
    el="section", full=True))

# ============================================================ PREUVE SOCIALE
LOGOS = add("Logos · défilement infini", "fas fa-infinity", section([
    text("Ils nous font confiance", cls="dz-small dz-center", block=True),
    html("""
    <div class="dz-marquee" style="margin-top:1.5rem" data-dz-speed="28">
      <div class="dz-marquee-track">
        <span class="dz-logo"><i class="fas fa-cube"></i> Nexora</span>
        <span class="dz-logo"><i class="fas fa-leaf"></i> Verdant</span>
        <span class="dz-logo"><i class="fas fa-bolt"></i> Voltix</span>
        <span class="dz-logo"><i class="fas fa-gem"></i> Lumia</span>
        <span class="dz-logo"><i class="fas fa-mountain"></i> Altura</span>
        <span class="dz-logo"><i class="fas fa-atom"></i> Quanta</span>
        <span class="dz-logo"><i class="fas fa-feather-alt"></i> Plume</span>
      </div>
    </div>""")], cls="dz-section-sm"))

STATS = add("Chiffres clés animés", "fas fa-sort-numeric-up", section([
    html("""
    <div class="dz-grid dz-grid-4 dz-stagger dz-center">
      <div class="dz-stat"><span class="dz-stat-value dz-gradient-text" data-dz-count="2400" data-dz-suffix="+">0</span><span class="dz-stat-label">équipes actives</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="99.9" data-dz-decimals="1" data-dz-suffix=" %">0</span><span class="dz-stat-label">de disponibilité</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="3.2" data-dz-decimals="1" data-dz-suffix=" M">0</span><span class="dz-stat-label">actions automatisées / mois</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="4.9" data-dz-decimals="1" data-dz-suffix="/5">0</span><span class="dz-stat-label">note moyenne clients</span></div>
    </div>""")], cls="dz-section-sm"))

# ============================================================ FONCTIONNALITÉS
FEATURES = add("Fonctionnalités · grille 3 colonnes", "fas fa-th-large", section([
    head("Fonctionnalités", "Tout ce qu'il faut, rien de trop", "Chaque outil a été pensé pour vous faire gagner du temps dès le premier jour."),
    box("dz-grid dz-grid-3 dz-stagger",
        feature_card("fas fa-bolt", "Ultra rapide", "Pages chargées en moins d'une seconde, même sur mobile et en 4G."),
        feature_card("fas fa-shield-alt", "Sécurisé par défaut", "Double authentification, rôles fins, données chiffrées et sauvegardes quotidiennes."),
        feature_card("fas fa-magic", "Automatisations", "Relances, e-mails, notifications : les tâches répétitives tournent toutes seules."),
        feature_card("fas fa-mobile-alt", "Pensé mobile", "Une interface fluide au doigt, installable comme une vraie application."),
        feature_card("fas fa-plug", "Connecté", "API, webhooks, WhatsApp, e-mail : branchez vos outils existants en quelques clics."),
        feature_card("fas fa-chart-line", "Pilotage en temps réel", "Tableaux de bord clairs pour décider vite, sur des chiffres à jour."))],
    cid="fonctionnalites"))

BENTO = add("Fonctionnalités · bento", "fas fa-border-all", section([
    head("Plateforme", "Une base solide pour tous vos projets", None),
    box("dz-bento dz-stagger",
        box("dz-card dz-card-brand dz-span-4 dz-row-2 dz-spotlight",
            html('<span class="dz-icon" style="background:rgba(255,255,255,.18);color:#fff"><i class="fas fa-layer-group"></i></span>'),
            text("Tout-en-un", "h3", "dz-h3"),
            text("Site, application, espace client et outils internes partagent les mêmes données. Plus de copier-coller entre dix logiciels.", cls="dz-text"),
            html('<div class="dz-progress" data-dz-value="82" style="margin-top:auto;background:rgba(255,255,255,.2)"><span style="background:#fff"></span></div><span class="dz-small" style="color:rgba(255,255,255,.8)">82 % de temps gagné en moyenne</span>')),
        box("dz-card dz-card-hover dz-span-2",
            html('<span class="dz-icon"><i class="fas fa-lock"></i></span>'),
            text("RGPD", "h4", "dz-h4"),
            text("Hébergé en France, vos données restent les vôtres.", cls="dz-text")),
        box("dz-card dz-card-hover dz-span-2",
            html('<span class="dz-icon"><i class="fas fa-sync-alt"></i></span>'),
            text("Synchro live", "h4", "dz-h4"),
            text("Chaque modification est visible partout, instantanément.", cls="dz-text")),
        box("dz-card dz-card-soft dz-span-3",
            html('<div class="dz-cluster"><div class="dz-ring" style="--v:94">94%</div><div><b class="dz-h4" style="display:block;margin:0">Satisfaction</b><span class="dz-text">sur 1 200 avis vérifiés</span></div></div>')),
        box("dz-card dz-card-hover dz-span-3 dz-border-glow",
            html('<span class="dz-icon dz-icon-gradient"><i class="fas fa-robot"></i></span>'),
            text("IA intégrée", "h4", "dz-h4"),
            text("Résumés, réponses automatiques et suggestions directement dans vos écrans.", cls="dz-text")))]))

SPLIT = add("Section · texte + visuel (alterné)", "fas fa-align-left", section([
    box("dz-split",
        box("",
            text("Automatisations", cls="dz-eyebrow", block=False),
            text("Vos process tournent pendant que vous dormez", "h2", "dz-h2"),
            text("Définissez une règle une fois. Relances clients, confirmations, rappels et rapports partent au bon moment, sans oubli.", cls="dz-lead"),
            html("""
            <ul class="dz-check-list" style="margin:1.5rem 0 2rem">
              <li>Déclencheurs sur n'importe quel événement</li>
              <li>E-mails, SMS et WhatsApp personnalisés</li>
              <li>Historique complet et reprise en cas d'erreur</li>
            </ul>"""),
            link("Découvrir", "#", "dz-btn dz-btn-soft", "fas fa-arrow-right")),
        html("""
        <div class="dz-card dz-card-glass" data-dz-reveal="right" style="gap:1rem">
          <div class="dz-cluster" style="justify-content:space-between"><b>Workflow « Nouveau lead »</b><span class="dz-badge dz-badge-success"><span class="dz-dot"></span>Actif</span></div>
          <div class="dz-timeline">
            <div><b>Formulaire reçu</b><div class="dz-small">Déclencheur</div></div>
            <div><b>Fiche client créée</b><div class="dz-small">+ attribution au commercial</div></div>
            <div><b>WhatsApp de bienvenue</b><div class="dz-small">envoyé en 3 s</div></div>
            <div><b>Relance J+2</b><div class="dz-small">si pas de réponse</div></div>
          </div>
        </div>"""))], cls="dz-section dz-section-alt"))

STEPS = add("Étapes · comment ça marche", "fas fa-list-ol", section([
    head("Comment ça marche", "Opérationnel en 3 étapes", None),
    box("dz-steps dz-stagger",
        box("dz-step", text("Créez votre espace", "h4", "dz-h4"), text("Inscription en 30 secondes, sans carte bancaire.", cls="dz-text")),
        box("dz-step", text("Importez vos données", "h4", "dz-h4"), text("Fichier Excel, CSV ou connexion directe à vos outils.", cls="dz-text")),
        box("dz-step", text("Lancez-vous", "h4", "dz-h4"), text("Invitez l'équipe, activez les automatisations, c'est parti.", cls="dz-text")))]))

# ============================================================ TARIFS
PRICING = add("Tarifs · 3 offres + bascule annuel", "fas fa-tags", section([
    head("Tarifs", "Un prix simple, sans surprise", "Commencez gratuitement, évoluez quand vous êtes prêt."),
    html("""
    <div data-dz-pricing>
      <div class="dz-center" style="margin-bottom:2.5rem">
        <div class="dz-toggle" data-dz-price-toggle="monthly">
          <button data-period="monthly">Mensuel</button>
          <button data-period="yearly">Annuel <span class="dz-badge dz-badge-success" style="margin-left:.3rem">-20 %</span></button>
        </div>
      </div>
      <div class="dz-pricing dz-stagger">
        <div class="dz-price-card">
          <div><b class="dz-h4">Découverte</b><p class="dz-small" style="margin:.3rem 0 0">Pour tester et démarrer seul.</p></div>
          <div class="dz-price"><span class="dz-price-amount">0 €</span><span class="dz-price-period">/ mois</span></div>
          <a class="dz-btn dz-btn-ghost dz-btn-block" href="#">Commencer</a>
          <ul class="dz-check-list"><li>1 utilisateur</li><li>3 projets</li><li>Support communautaire</li><li class="dz-no">Automatisations</li></ul>
        </div>
        <div class="dz-price-card dz-featured">
          <span class="dz-badge dz-ribbon" style="background:var(--dz-primary);color:#fff;border:0">Le plus choisi</span>
          <div><b class="dz-h4">Pro</b><p class="dz-small" style="margin:.3rem 0 0">Pour les équipes qui grandissent.</p></div>
          <div class="dz-price"><span class="dz-price-amount" data-monthly="29 €" data-yearly="23 €">29 €</span><span class="dz-price-period">/ utilisateur / mois</span></div>
          <a class="dz-btn dz-btn-block dz-btn-shine" href="#">Essayer 14 jours</a>
          <ul class="dz-check-list"><li>Utilisateurs illimités</li><li>Projets illimités</li><li>Automatisations</li><li>Support prioritaire</li></ul>
        </div>
        <div class="dz-price-card">
          <div><b class="dz-h4">Entreprise</b><p class="dz-small" style="margin:.3rem 0 0">Sécurité et accompagnement dédiés.</p></div>
          <div class="dz-price"><span class="dz-price-amount" data-monthly="99 €" data-yearly="79 €">99 €</span><span class="dz-price-period">/ mois</span></div>
          <a class="dz-btn dz-btn-dark dz-btn-block" href="#">Nous contacter</a>
          <ul class="dz-check-list"><li>SSO et journal d'audit</li><li>Hébergement dédié</li><li>SLA 99,9 %</li><li>Chef de projet dédié</li></ul>
        </div>
      </div>
    </div>""")], cid="tarifs"))

# ============================================================ TÉMOIGNAGES
def quote(q, name, role, initials, grad=None):
    st = f' style="background:{grad}"' if grad else ""
    return box("dz-card dz-quote dz-card-hover",
               text("★★★★★", cls="dz-stars"),
               text(q, cls="", block=True),
               html(f'<div class="dz-person"><span class="dz-avatar"{st}>{initials}</span><div><div class="dz-person-name">{name}</div><div class="dz-person-role">{role}</div></div></div>'))

TESTI = add("Témoignages · grille", "fas fa-quote-right", section([
    head("Témoignages", "Ils ont franchi le pas", None),
    box("dz-grid dz-grid-3 dz-stagger",
        quote("« On a remplacé quatre outils par un seul. L'équipe a enfin une vue claire sur les clients. »", "Amélie L.", "Directrice commerciale", "AL"),
        quote("« Mise en place en une semaine. Les relances automatiques nous ont fait gagner 30 % de chiffre. »", "Karim M.", "Gérant, agence immobilière", "KM", "linear-gradient(135deg,#f472b6,#fb923c)"),
        quote("« Beau, rapide, et nos clients adorent l'appli sur leur téléphone. »", "Sophie D.", "Fondatrice", "SD", "linear-gradient(135deg,#22d3ee,#10b981)"))],
    cls="dz-section dz-section-alt", cid="temoignages"))

WALL = add("Témoignages · mur qui défile", "fas fa-comments", section([
    head("Avis clients", "Plus de 1 200 avis 5 étoiles", None),
    html("""
    <div class="dz-marquee" data-dz-speed="45" style="--dz-gap:1.25rem">
      <div class="dz-marquee-track" style="align-items:stretch">
        <div class="dz-card" style="width:320px"><span class="dz-stars">★★★★★</span><p>Interface magnifique et super intuitive.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">LB</span><span class="dz-person-name">Lucas B.</span></div></div>
        <div class="dz-card" style="width:320px"><span class="dz-stars">★★★★★</span><p>Le support répond en quelques minutes.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">NR</span><span class="dz-person-name">Nadia R.</span></div></div>
        <div class="dz-card" style="width:320px"><span class="dz-stars">★★★★★</span><p>On a divisé par deux le temps de saisie.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">TG</span><span class="dz-person-name">Thomas G.</span></div></div>
        <div class="dz-card" style="width:320px"><span class="dz-stars">★★★★★</span><p>Enfin un outil que toute l'équipe utilise.</p><div class="dz-person"><span class="dz-avatar dz-avatar-sm">IF</span><span class="dz-person-name">Inès F.</span></div></div>
      </div>
    </div>""")]))

# ============================================================ FAQ / CTA / CONTACT
FAQ = add("FAQ · accordéon", "fas fa-question-circle", section([
    head("FAQ", "Questions fréquentes", None),
    html("""
    <div class="dz-faq">
      <details open><summary>Puis-je essayer gratuitement ?</summary><div>Oui, 14 jours complets, sans carte bancaire. Vous gardez vos données si vous continuez.</div></details>
      <details><summary>Mes données sont-elles en sécurité ?</summary><div>Hébergement en France, chiffrement, sauvegardes quotidiennes et double authentification.</div></details>
      <details><summary>Puis-je annuler à tout moment ?</summary><div>Oui, en un clic depuis votre compte. Aucun engagement.</div></details>
      <details><summary>Proposez-vous un accompagnement ?</summary><div>Oui : démarrage guidé, formation de l'équipe et support prioritaire sur les offres Pro et Entreprise.</div></details>
    </div>""")], narrow=True, cid="faq"))

CTA = add("Appel à l'action · bandeau dégradé", "fas fa-bullhorn", section([
    box("dz-cta dz-reveal",
        text("Prêt à passer à la vitesse supérieure ?", "h2", "dz-h2"),
        text("Rejoignez les équipes qui ont déjà simplifié leur quotidien.", cls="dz-lead"),
        html('<div class="dz-cluster" style="justify-content:center"><a class="dz-btn dz-btn-lg dz-btn-light dz-magnetic" href="#">Commencer gratuitement <i class="fas fa-arrow-right"></i></a><a class="dz-btn dz-btn-lg dz-btn-ghost" style="--_fg:#fff;--_bd:rgba(255,255,255,.4)" href="#">Réserver une démo</a></div>'))]))

LEAD = add("Capture de leads · zone pour ta vue Edit", "fas fa-envelope-open-text", section([
    box("dz-split",
        box("",
            text("Contact", cls="dz-eyebrow", block=False),
            text("Parlons de votre projet", "h2", "dz-h2"),
            text("Réponse sous 24 h ouvrées. Premier échange gratuit et sans engagement.", cls="dz-lead"),
            html("""
            <div class="dz-stack" style="margin-top:1.5rem">
              <div class="dz-cluster"><span class="dz-icon"><i class="fas fa-envelope"></i></span><div><b>E-mail</b><div class="dz-small">contact@exemple.fr</div></div></div>
              <div class="dz-cluster"><span class="dz-icon"><i class="fas fa-phone"></i></span><div><b>Téléphone</b><div class="dz-small">01 23 45 67 89</div></div></div>
              <div class="dz-cluster"><span class="dz-icon"><i class="fas fa-map-marker-alt"></i></span><div><b>Adresse</b><div class="dz-small">Paris, France</div></div></div>
            </div>""")),
        box("dz-card dz-shadow-lg",
            text("Écrivez-nous", "h3", "dz-h4"),
            text("⬇ Glisse ici ta vue <b>Edit</b> (table des leads). Le kit met le formulaire en forme tout seul. Supprime ce texte ensuite.", cls="dz-callout"),
            ))], cid="contact"))

NEWS = add("Newsletter · champ + bouton", "fas fa-paper-plane", section([
    box("dz-card dz-center dz-bg-mesh",
        text("Recevez nos conseils chaque mois", "h3", "dz-h3"),
        text("Pas de spam. Désinscription en un clic.", cls="dz-text"),
        text("⬇ Glisse ici une vue <b>Edit</b> avec un seul champ e-mail, et ajoute la classe <code>dz-inline-form</code> au conteneur qui l'entoure.", cls="dz-small"))],
    narrow=True, cls="dz-section-sm"))

COUNTDOWN = add("Compte à rebours · lancement", "fas fa-hourglass-half", section([
    box("dz-center",
        text("Lancement", cls="dz-eyebrow", block=False),
        text("Ouverture des inscriptions dans", "h2", "dz-h2"),
        html("""
        <div class="dz-countdown" data-dz-countdown="2026-12-31T23:59:59" data-dz-done="C'est parti !" style="margin:1.5rem 0 2rem">
          <div><span data-dz-unit="days">00</span><small>jours</small></div>
          <div><span data-dz-unit="hours">00</span><small>heures</small></div>
          <div><span data-dz-unit="minutes">00</span><small>min</small></div>
          <div><span data-dz-unit="seconds">00</span><small>sec</small></div>
        </div>"""),
        link("Être prévenu", "#", "dz-btn dz-btn-gradient dz-btn-lg", "fas fa-bell"))]))

VIDEO = add("Vidéo · section avec lecteur", "fas fa-play-circle", section([
    head("Démo", "Voyez-le en action (2 min)", None),
    html("""
    <div class="dz-video dz-glow-under" data-dz-reveal="zoom">
      <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" title="Vidéo" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>""")], narrow=True))

TEAM = add("Équipe · cartes membres", "fas fa-users", section([
    head("Équipe", "Les personnes derrière le projet", None),
    box("dz-grid dz-grid-4 dz-stagger dz-center",
        *[box("dz-card dz-card-hover dz-center",
              html(f'<span class="dz-avatar dz-avatar-lg" style="margin:0 auto;{g}">{i}</span>'),
              text(n, "h4", "dz-h4"), text(r, cls="dz-small"))
          for n, r, i, g in [("Sidy D.", "Fondateur · Data & IA", "SD", ""),
                             ("Marie K.", "Design produit", "MK", "background:linear-gradient(135deg,#f472b6,#fb923c)"),
                             ("Yanis B.", "Développement", "YB", "background:linear-gradient(135deg,#22d3ee,#10b981)"),
                             ("Léa P.", "Relation client", "LP", "background:linear-gradient(135deg,#f59e0b,#ef4444)")]])]))

COMPARE = add("Avant / après · curseur", "fas fa-adjust", section([
    head("Transformation", "Glissez pour comparer", None),
    html("""
    <div class="dz-compare" style="max-width:900px;margin:0 auto">
      <img src="https://picsum.photos/seed/avant/1200/700?grayscale" alt="Avant">
      <img src="https://picsum.photos/seed/avant/1200/700" alt="Après">
    </div>""")]))

FOOTER = add("Pied de page · 4 colonnes", "fas fa-window-minimize", box("dz-footer", html("""
<div class="dz-container">
  <div class="dz-footer-grid">
    <div class="dz-stack" style="--dz-gap:1rem">
      <a class="dz-brand" href="/"><span class="dz-brand-mark"></span>Marque</a>
      <p class="dz-text" style="max-width:34ch;margin:0">La plateforme qui simplifie le quotidien des équipes ambitieuses.</p>
      <div class="dz-socials"><a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a><a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a><a href="#" aria-label="GitHub"><i class="fab fa-github"></i></a></div>
    </div>
    <div><div class="dz-footer-title">Produit</div><ul><li><a href="#fonctionnalites">Fonctionnalités</a></li><li><a href="#tarifs">Tarifs</a></li><li><a href="#">Nouveautés</a></li></ul></div>
    <div><div class="dz-footer-title">Société</div><ul><li><a href="#">À propos</a></li><li><a href="#">Blog</a></li><li><a href="#contact">Contact</a></li></ul></div>
    <div><div class="dz-footer-title">Légal</div><ul><li><a href="#">Mentions légales</a></li><li><a href="#">Confidentialité</a></li><li><a href="#">CGV</a></li></ul></div>
  </div>
  <div class="dz-footer-bottom"><span>© 2026 Marque. Tous droits réservés.</span><span>Fait avec soin en France</span></div>
</div>"""), el="footer", full=True))

# ============================================================ APPLICATION / SAAS / INTERNE
PAGEHEAD = add("App · en-tête de page + actions", "fas fa-heading", box("dz-page-head",
    box("",
        text("Tableau de bord", cls="dz-eyebrow", block=False),
        text("Bonjour 👋", "h1", "dz-h3"),
        text("Voici ce qui s'est passé depuis votre dernière visite.", cls="dz-text")),
    box("dz-toolbar",
        link("Exporter", "#", "dz-btn dz-btn-ghost dz-btn-sm", "fas fa-download"),
        link("Nouveau", "#", "dz-btn dz-btn-sm", "fas fa-plus"))))

KPI = add("App · rangée de KPI", "fas fa-tachometer-alt", html("""
<div class="dz-grid dz-grid-4 dz-stagger">
  <div class="dz-kpi"><div class="dz-kpi-label">Chiffre d'affaires <span class="dz-trend dz-trend-up">▲ 12 %</span></div><div class="dz-kpi-value" data-dz-count="48250" data-dz-suffix=" €">0</div><div class="dz-progress dz-progress" data-dz-value="72"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Nouveaux clients <span class="dz-trend dz-trend-up">▲ 8 %</span></div><div class="dz-kpi-value" data-dz-count="128">0</div><div class="dz-progress" data-dz-value="54"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Tickets ouverts <span class="dz-trend dz-trend-down">▼ 3</span></div><div class="dz-kpi-value" data-dz-count="17">0</div><div class="dz-progress" data-dz-value="30"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Satisfaction <span class="dz-trend dz-trend-up">▲ 0,2</span></div><div class="dz-kpi-value" data-dz-count="4.8" data-dz-decimals="1" data-dz-suffix="/5">0</div><div class="dz-progress" data-dz-value="96"><span></span></div></div>
</div>"""))

VIEWCARD = add("App · carte pour une vue", "fas fa-window-maximize", box("dz-card",
    box("dz-cluster", text("Titre de la carte", "h3", "dz-h4 dz-mb-0"),
        text("12 éléments", cls="dz-badge dz-badge-neutral", block=False)),
    text("⬇ Glisse ici une vue (List, Kanban, Calendrier, Graphique…). Supprime ce texte ensuite.", cls="dz-callout")))

TWO_PANELS = add("App · deux colonnes (liste + détail)", "fas fa-columns", cols([
    box("dz-card", text("Liste", "h3", "dz-h4"), text("⬇ Vue List ici", cls="dz-callout")),
    box("dz-card", text("Détail", "h3", "dz-h4"), text("⬇ Vue Show ou Edit ici", cls="dz-callout"))],
    [5, 7], bp="lg", cls="g-4"))

EMPTY = add("App · état vide", "fas fa-inbox", box("dz-empty",
    html('<span class="dz-icon dz-icon-round"><i class="fas fa-inbox"></i></span>'),
    text("Rien pour le moment", "h3", "dz-h4 dz-mb-0"),
    text("Créez votre premier élément pour commencer.", cls="dz-text"),
    link("Créer", "#", "dz-btn dz-btn-sm", "fas fa-plus")))

ACTIVITY = add("App · fil d'activité", "fas fa-stream", box("dz-card",
    text("Activité récente", "h3", "dz-h4"),
    html("""
    <div class="dz-timeline" style="margin-top:.5rem">
      <div><b>Devis #1042 accepté</b><div class="dz-small">par Martin SARL · il y a 5 min</div></div>
      <div><b>Nouveau lead</b><div class="dz-small">formulaire du site · il y a 1 h</div></div>
      <div><b>Facture #883 payée</b><div class="dz-small">1 250 € · hier</div></div>
    </div>""")))

CALLOUTS = add("App · messages (info, succès, alerte)", "fas fa-info-circle", box("dz-stack",
    text("<b>Info :</b> la synchronisation tourne toutes les 5 minutes.", cls="dz-callout"),
    text("<b>C'est fait :</b> vos paramètres sont enregistrés.", cls="dz-callout dz-callout-success"),
    text("<b>Attention :</b> 3 factures arrivent à échéance cette semaine.", cls="dz-callout dz-callout-warning")))

BOTTOMNAV = add("Mobile · barre d'onglets en bas", "fas fa-mobile-alt", html("""
<nav class="dz-bottom-nav dz-mobile-only">
  <a href="/"><i class="fas fa-home"></i>Accueil</a>
  <a href="/page/recherche"><i class="fas fa-search"></i>Chercher</a>
  <a href="/page/nouveau"><i class="fas fa-plus-circle"></i>Ajouter</a>
  <a href="/page/notifications"><i class="fas fa-bell"></i>Alertes</a>
  <a href="/auth/settings"><i class="fas fa-user"></i>Compte</a>
</nav>"""))

FAB = add("Mobile · bouton flottant", "fas fa-plus-circle", html('<a class="dz-fab" href="#" aria-label="Ajouter"><i class="fas fa-plus"></i></a>'))

SCROLLER = add("Mobile · cartes défilantes (carrousel)", "fas fa-grip-horizontal", html("""
<div class="dz-scroller dz-grid-desktop">
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-rocket"></i></span><b class="dz-h4">Carte 1</b><p>Glissez horizontalement sur mobile.</p></div>
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-heart"></i></span><b class="dz-h4">Carte 2</b><p>Grille classique sur ordinateur.</p></div>
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-star"></i></span><b class="dz-h4">Carte 3</b><p>Accroche automatique au doigt.</p></div>
</div>"""))

THEMEBTN = add("Outil · bouton clair / sombre", "fas fa-moon", html(
    '<button class="dz-btn dz-btn-ghost dz-icon-btn dz-theme-btn" data-dz-theme-toggle aria-label="Changer de thème"><i class="fas fa-moon dz-moon"></i><i class="fas fa-sun dz-sun"></i></button>'))

CONFETTI = add("Outil · bouton avec confettis", "fas fa-birthday-cake", html(
    '<button class="dz-btn dz-btn-gradient" data-dz-confetti>Valider 🎉</button>'))

# ------------------------------------------------------------------ pages de démo
def page(name, title, desc, blocks, no_menu=False, fluid=False):
    return {"name": name, "title": title, "description": desc, "min_role": 1,
            "layout": {"above": blocks}, "fixed_states": {}, "menu_label": None,
            "attributes": {"no_menu": no_menu, "request_fluid_layout": fluid},
            "root_page_for_roles": []}

LANDING = page("dz-demo-landing", "Démo landing", "Landing complète construite avec les blocs DZ",
               [NAV, HERO_SPLIT, LOGOS, FEATURES, BENTO, SPLIT, STATS, STEPS, PRICING, TESTI, FAQ, CTA, FOOTER],
               no_menu=True, fluid=True)

AGENCY = page("dz-demo-studio", "Démo studio", "Page vitrine sombre, texte animé",
              [NAV, HERO_TYPED, LOGOS, TEAM, WALL, COUNTDOWN, LEAD, FOOTER], no_menu=True, fluid=True)

DASH = page("dz-demo-app", "Démo application", "Écran d'application / outil interne",
            [PAGEHEAD, KPI,
             cols([VIEWCARD, ACTIVITY], [8, 4], bp="lg", cls="g-4 mt-1"),
             CALLOUTS, TWO_PANELS, EMPTY, BOTTOMNAV, FAB])

CATALOGUE = page("dz-catalogue", "Catalogue du kit", "Tous les blocs DZ sur une page",
                 [b["layout"] for b in LIB if b["name"] not in ("DZ · Mobile · barre d'onglets en bas", "DZ · Mobile · bouton flottant")],
                 no_menu=True, fluid=True)

json.dump({"tables": [], "views": [], "plugins": [], "pages": [], "triggers": [], "roles": [], "library": LIB},
          open(os.path.join(OUT, "blocks.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"tables": [], "views": [], "plugins": [], "pages": [LANDING, AGENCY, DASH, CATALOGUE], "triggers": [], "roles": [], "library": []},
          open(os.path.join(OUT, "demo-pages.json"), "w"), ensure_ascii=False, indent=1)
print(len(LIB), "blocs ;", 4, "pages")
