"""Génère assets/blocks.json (Library du builder) et packs/demo-pages.json.

Les blocs sont écrits dans le format de layout natif de Saltcorn 1.6
(container / blank / link / besides / above), pour rester modifiables au
glisser-déposer. Les widgets qui ont besoin d'une structure précise
(tarifs avec bascule, FAQ, défilement de logos, barre du bas…) sont des
éléments « HTML code », modifiables en code dans le builder.

Lancer :  python3 tools/build_packs.py
"""
import json, os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "build")
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
    LIB.append({"name": name, "icon": icon, "layout": layout})
    return layout


# ============================================================ NAVIGATION
NAV = add("Nav · landing", "fas fa-bars", html("""
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
HERO_AURORA = add("Hero · aurora", "fas fa-star", box(
    "dz-hero dz-center",
    html('<div class="dz-aurora"></div>'),
    box("dz-container-narrow",
        html('<a class="dz-announce" href="#" data-dz-reveal><strong>Nouveau</strong> Découvrez la version 2.0 <i class="fas fa-arrow-right"></i></a>'),
        text('Construisez plus vite, <em class="dz-gradient-text">sans compromis</em>', "h1", "dz-display dz-reveal", ),
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

HERO_SPLIT = add("Hero · texte + maquette", "fas fa-columns", box(
    "dz-hero dz-bg-mesh",
    box("dz-container",
        box("dz-split",
            box("dz-mobile-center",
                text('<span class="dz-dot"></span> Disponible maintenant', cls="dz-badge dz-reveal", block=False),
                text('Votre activité, <em>enfin pilotée</em> au même endroit', "h1", "dz-h1 dz-reveal"),
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

HERO_TYPED = add("Hero · texte animé", "fas fa-keyboard", box(
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
LOGOS = add("Web · logos défilants", "fas fa-infinity", section([
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

STATS = add("Web · chiffres", "fas fa-sort-numeric-up", section([
    html("""
    <div class="dz-grid dz-grid-4 dz-stagger dz-center">
      <div class="dz-stat"><span class="dz-stat-value dz-gradient-text" data-dz-count="2400" data-dz-suffix="+">0</span><span class="dz-stat-label">équipes actives</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="99.9" data-dz-decimals="1" data-dz-suffix=" %">0</span><span class="dz-stat-label">de disponibilité</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="3.2" data-dz-decimals="1" data-dz-suffix=" M">0</span><span class="dz-stat-label">actions automatisées / mois</span></div>
      <div class="dz-stat"><span class="dz-stat-value" data-dz-count="4.9" data-dz-decimals="1" data-dz-suffix="/5">0</span><span class="dz-stat-label">note moyenne clients</span></div>
    </div>""")], cls="dz-section-sm"))

# ============================================================ FONCTIONNALITÉS
FEATURES = add("Web · fonctions 3 col.", "fas fa-th-large", section([
    head("Fonctionnalités", "Tout ce qu'il faut, rien de trop", "Chaque outil a été pensé pour vous faire gagner du temps dès le premier jour."),
    box("dz-grid dz-grid-3 dz-stagger",
        feature_card("fas fa-bolt", "Ultra rapide", "Pages chargées en moins d'une seconde, même sur mobile et en 4G."),
        feature_card("fas fa-shield-alt", "Sécurisé par défaut", "Double authentification, rôles fins, données chiffrées et sauvegardes quotidiennes."),
        feature_card("fas fa-magic", "Automatisations", "Relances, e-mails, notifications : les tâches répétitives tournent toutes seules."),
        feature_card("fas fa-mobile-alt", "Pensé mobile", "Une interface fluide au doigt, installable comme une vraie application."),
        feature_card("fas fa-plug", "Connecté", "API, webhooks, WhatsApp, e-mail : branchez vos outils existants en quelques clics."),
        feature_card("fas fa-chart-line", "Pilotage en temps réel", "Tableaux de bord clairs pour décider vite, sur des chiffres à jour."))],
    cid="fonctionnalites"))

BENTO = add("Web · bento", "fas fa-border-all", section([
    head("Plateforme", "Une base solide pour tous vos projets", None),
    box("dz-bento dz-stagger",
        box("dz-card dz-card-brand dz-span-4 dz-row-2 dz-spotlight",
            html('<span class="dz-icon" style="background:color-mix(in srgb, var(--dz-on-primary) 15%, transparent);color:var(--dz-on-primary)"><i class="fas fa-layer-group"></i></span>'),
            text("Tout-en-un", "h3", "dz-h3"),
            text("Site, application, espace client et outils internes partagent les mêmes données. Plus de copier-coller entre dix logiciels.", cls="dz-text"),
            html('<div class="dz-progress" data-dz-value="82" style="margin-top:auto;background:color-mix(in srgb, var(--dz-on-primary) 20%, transparent)"><span style="background:var(--dz-on-primary)"></span></div><span class="dz-small" style="color:var(--dz-text-soft)">82 % de temps gagné en moyenne</span>')),
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

SPLIT = add("Web · texte + visuel", "fas fa-align-left", section([
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

STEPS = add("Web · étapes", "fas fa-list-ol", section([
    head("Comment ça marche", "Opérationnel en 3 étapes", None),
    box("dz-steps dz-stagger",
        box("dz-step", text("Créez votre espace", "h4", "dz-h4"), text("Inscription en 30 secondes, sans carte bancaire.", cls="dz-text")),
        box("dz-step", text("Importez vos données", "h4", "dz-h4"), text("Fichier Excel, CSV ou connexion directe à vos outils.", cls="dz-text")),
        box("dz-step", text("Lancez-vous", "h4", "dz-h4"), text("Invitez l'équipe, activez les automatisations, c'est parti.", cls="dz-text")))]))

# ============================================================ TARIFS
PRICING = add("Web · tarifs", "fas fa-tags", section([
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

TESTI = add("Web · avis (grille)", "fas fa-quote-right", section([
    head("Témoignages", "Ils ont franchi le pas", None),
    box("dz-grid dz-grid-3 dz-stagger",
        quote("« On a remplacé quatre outils par un seul. L'équipe a enfin une vue claire sur les clients. »", "Amélie L.", "Directrice commerciale", "AL"),
        quote("« Mise en place en une semaine. Les relances automatiques nous ont fait gagner 30 % de chiffre. »", "Karim M.", "Gérant, agence immobilière", "KM", "linear-gradient(135deg,#f472b6,#fb923c)"),
        quote("« Beau, rapide, et nos clients adorent l'appli sur leur téléphone. »", "Sophie D.", "Fondatrice", "SD", "linear-gradient(135deg,#22d3ee,#10b981)"))],
    cls="dz-section dz-section-alt", cid="temoignages"))

WALL = add("Web · avis défilants", "fas fa-comments", section([
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
FAQ = add("Web · FAQ", "fas fa-question-circle", section([
    head("FAQ", "Questions fréquentes", None),
    html("""
    <div class="dz-faq">
      <details open><summary>Puis-je essayer gratuitement ?</summary><div>Oui, 14 jours complets, sans carte bancaire. Vous gardez vos données si vous continuez.</div></details>
      <details><summary>Mes données sont-elles en sécurité ?</summary><div>Hébergement en France, chiffrement, sauvegardes quotidiennes et double authentification.</div></details>
      <details><summary>Puis-je annuler à tout moment ?</summary><div>Oui, en un clic depuis votre compte. Aucun engagement.</div></details>
      <details><summary>Proposez-vous un accompagnement ?</summary><div>Oui : démarrage guidé, formation de l'équipe et support prioritaire sur les offres Pro et Entreprise.</div></details>
    </div>""")], narrow=True, cid="faq"))

CTA = add("Web · appel à l'action", "fas fa-bullhorn", section([
    box("dz-cta dz-reveal",
        text("Prêt à passer à la vitesse supérieure ?", "h2", "dz-h2"),
        text("Rejoignez les équipes qui ont déjà simplifié leur quotidien.", cls="dz-lead"),
        html('<div class="dz-cluster" style="justify-content:center"><a class="dz-btn dz-btn-lg dz-btn-light dz-magnetic" href="#">Commencer gratuitement <i class="fas fa-arrow-right"></i></a><a class="dz-btn dz-btn-lg dz-btn-ghost" style="--_fg:var(--dz-on-primary);--_bd:color-mix(in srgb, var(--dz-on-primary) 40%, transparent)" href="#">Réserver une démo</a></div>'))]))

LEAD = add("Web · contact + formulaire", "fas fa-envelope-open-text", section([
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

NEWS = add("Web · newsletter", "fas fa-paper-plane", section([
    box("dz-card dz-center dz-bg-mesh",
        text("Recevez nos conseils chaque mois", "h3", "dz-h3"),
        text("Pas de spam. Désinscription en un clic.", cls="dz-text"),
        text("⬇ Glisse ici une vue <b>Edit</b> avec un seul champ e-mail, et ajoute la classe <code>dz-inline-form</code> au conteneur qui l'entoure.", cls="dz-small"))],
    narrow=True, cls="dz-section-sm"))

COUNTDOWN = add("Web · compte à rebours", "fas fa-hourglass-half", section([
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

VIDEO = add("Web · vidéo", "fas fa-play-circle", section([
    head("Démo", "Voyez-le en action (2 min)", None),
    html("""
    <div class="dz-video dz-glow-under" data-dz-reveal="zoom">
      <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" title="Vidéo" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>""")], narrow=True))

TEAM = add("Web · équipe", "fas fa-users", section([
    head("Équipe", "Les personnes derrière le projet", None),
    box("dz-grid dz-grid-4 dz-stagger dz-center",
        *[box("dz-card dz-card-hover dz-center",
              html(f'<span class="dz-avatar dz-avatar-lg" style="margin:0 auto;{g}">{i}</span>'),
              text(n, "h4", "dz-h4"), text(r, cls="dz-small"))
          for n, r, i, g in [("Sidy D.", "Fondateur · Data & IA", "SD", ""),
                             ("Marie K.", "Design produit", "MK", "background:linear-gradient(135deg,#f472b6,#fb923c)"),
                             ("Yanis B.", "Développement", "YB", "background:linear-gradient(135deg,#22d3ee,#10b981)"),
                             ("Léa P.", "Relation client", "LP", "background:linear-gradient(135deg,#f59e0b,#ef4444)")]])]))

COMPARE = add("Web · avant / après", "fas fa-adjust", section([
    head("Transformation", "Glissez pour comparer", None),
    html("""
    <div class="dz-compare" style="max-width:900px;margin:0 auto">
      <img src="https://picsum.photos/seed/avant/1200/700?grayscale" alt="Avant">
      <img src="https://picsum.photos/seed/avant/1200/700" alt="Après">
    </div>""")]))

FOOTER = add("Web · pied de page", "fas fa-window-minimize", box("dz-footer", html("""
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
PAGEHEAD = add("App · en-tête", "fas fa-heading", box("dz-page-head",
    box("",
        text("Tableau de bord", cls="dz-eyebrow", block=False),
        text("Bonjour 👋", "h1", "dz-h3"),
        text("Voici ce qui s'est passé depuis votre dernière visite.", cls="dz-text")),
    box("dz-toolbar",
        link("Exporter", "#", "dz-btn dz-btn-ghost dz-btn-sm", "fas fa-download"),
        link("Nouveau", "#", "dz-btn dz-btn-sm", "fas fa-plus"))))

KPI = add("App · KPI", "fas fa-tachometer-alt", html("""
<div class="dz-grid dz-grid-4 dz-stagger">
  <div class="dz-kpi"><div class="dz-kpi-label">Chiffre d'affaires <span class="dz-trend dz-trend-up">▲ 12 %</span></div><div class="dz-kpi-value" data-dz-count="48250" data-dz-suffix=" €">0</div><div class="dz-progress dz-progress" data-dz-value="72"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Nouveaux clients <span class="dz-trend dz-trend-up">▲ 8 %</span></div><div class="dz-kpi-value" data-dz-count="128">0</div><div class="dz-progress" data-dz-value="54"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Tickets ouverts <span class="dz-trend dz-trend-down">▼ 3</span></div><div class="dz-kpi-value" data-dz-count="17">0</div><div class="dz-progress" data-dz-value="30"><span></span></div></div>
  <div class="dz-kpi"><div class="dz-kpi-label">Satisfaction <span class="dz-trend dz-trend-up">▲ 0,2</span></div><div class="dz-kpi-value" data-dz-count="4.8" data-dz-decimals="1" data-dz-suffix="/5">0</div><div class="dz-progress" data-dz-value="96"><span></span></div></div>
</div>"""))

VIEWCARD = add("App · carte + vue", "fas fa-window-maximize", box("dz-card",
    box("dz-cluster", text("Titre de la carte", "h3", "dz-h4 dz-mb-0"),
        text("12 éléments", cls="dz-badge dz-badge-neutral", block=False)),
    text("⬇ Glisse ici une vue (List, Kanban, Calendrier, Graphique…). Supprime ce texte ensuite.", cls="dz-callout")))

TWO_PANELS = add("App · liste + détail", "fas fa-columns", cols([
    box("dz-card", text("Liste", "h3", "dz-h4"), text("⬇ Vue List ici", cls="dz-callout")),
    box("dz-card", text("Détail", "h3", "dz-h4"), text("⬇ Vue Show ou Edit ici", cls="dz-callout"))],
    [5, 7], bp="lg", cls="g-4"))

EMPTY = add("App · état vide", "fas fa-inbox", box("dz-empty",
    html('<span class="dz-icon dz-icon-round"><i class="fas fa-inbox"></i></span>'),
    text("Rien pour le moment", "h3", "dz-h4 dz-mb-0"),
    text("Créez votre premier élément pour commencer.", cls="dz-text"),
    link("Créer", "#", "dz-btn dz-btn-sm", "fas fa-plus")))

ACTIVITY = add("App · activité", "fas fa-stream", box("dz-card",
    text("Activité récente", "h3", "dz-h4"),
    html("""
    <div class="dz-timeline" style="margin-top:.5rem">
      <div><b>Devis #1042 accepté</b><div class="dz-small">par Martin SARL · il y a 5 min</div></div>
      <div><b>Nouveau lead</b><div class="dz-small">formulaire du site · il y a 1 h</div></div>
      <div><b>Facture #883 payée</b><div class="dz-small">1 250 € · hier</div></div>
    </div>""")))

CALLOUTS = add("App · messages", "fas fa-info-circle", box("dz-stack",
    text("<b>Info :</b> la synchronisation tourne toutes les 5 minutes.", cls="dz-callout"),
    text("<b>C'est fait :</b> vos paramètres sont enregistrés.", cls="dz-callout dz-callout-success"),
    text("<b>Attention :</b> 3 factures arrivent à échéance cette semaine.", cls="dz-callout dz-callout-warning")))

BOTTOMNAV = add("Mobile · onglets bas", "fas fa-mobile-alt", html("""
<nav class="dz-bottom-nav dz-mobile-only">
  <a href="/"><i class="fas fa-home"></i>Accueil</a>
  <a href="/page/recherche"><i class="fas fa-search"></i>Chercher</a>
  <a href="/page/nouveau"><i class="fas fa-plus-circle"></i>Ajouter</a>
  <a href="/page/notifications"><i class="fas fa-bell"></i>Alertes</a>
  <a href="/auth/settings"><i class="fas fa-user"></i>Compte</a>
</nav>"""))

FAB = add("Mobile · bouton flottant", "fas fa-plus-circle", html('<a class="dz-fab" href="#" aria-label="Ajouter"><i class="fas fa-plus"></i></a>'))

SCROLLER = add("Mobile · cartes glissées", "fas fa-grip-horizontal", html("""
<div class="dz-scroller dz-grid-desktop">
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-rocket"></i></span><b class="dz-h4">Carte 1</b><p>Glissez horizontalement sur mobile.</p></div>
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-heart"></i></span><b class="dz-h4">Carte 2</b><p>Grille classique sur ordinateur.</p></div>
  <div class="dz-card dz-card-hover"><span class="dz-icon"><i class="fas fa-star"></i></span><b class="dz-h4">Carte 3</b><p>Accroche automatique au doigt.</p></div>
</div>"""))

THEMEBTN = add("Outil · clair/sombre", "fas fa-moon", html(
    '<button class="dz-btn dz-btn-ghost dz-icon-btn dz-theme-btn" data-dz-theme-toggle aria-label="Changer de thème"><i class="fas fa-moon dz-moon"></i><i class="fas fa-sun dz-sun"></i></button>'))

CONFETTI = add("Outil · confettis", "fas fa-birthday-cake", html(
    '<button class="dz-btn dz-btn-gradient" data-dz-confetti>Valider 🎉</button>'))

# ============================================================ v2 : NOUVEAUX BLOCS
def img(url, cls="", alt=""):
    """Élément Image natif (cliquer dessus dans le builder pour téléverser la sienne)."""
    return {"type": "image", "srctype": "URL", "url": url, "alt": alt, "customClass": cls, "style": {}}


def pic(seed, w=900, h=700):
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def floatcard(title, sub, css, icon=None, avatar=None, cls="dz-float"):
    lead = (html(f'<span class="dz-icon dz-icon-round" style="width:38px;height:38px;font-size:1rem"><i class="{icon}"></i></span>') if icon
            else html(f'<span class="dz-avatar dz-avatar-sm">{avatar}</span>') if avatar else None)
    return box(f"dz-float-card {cls}", lead, box("", text(f"<b>{title}</b>", block=True), text(sub, cls="dz-small")), customCSS=css)


ROUND_BADGE = """
<div class="dz-badge-round" data-icon="✦" style="{pos}">
  <svg viewBox="0 0 120 120" aria-hidden="true"><circle class="dz-badge-bg" cx="60" cy="60" r="58"/><defs><path id="dzc{uid}" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0"/></defs>
  <text><textPath href="#dzc{uid}">{txt}</textPath></text></svg>
</div>"""


def round_badge(txt, pos, uid):
    return html(ROUND_BADGE.format(txt=txt, pos=pos, uid=uid))


TOPBAR = add("Web · bandeau d'annonce", "fas fa-bullhorn", html("""
<div class="dz-topbar"><span>🎉 Nouvelle version disponible — <a href="#">voir les nouveautés →</a></span><button data-dz-dismiss aria-label="Fermer">✕</button></div>"""))

PORTRAIT_VIS = add("Visuel · portrait + cartes", "fas fa-user-circle", box(
    "dz-portrait-wrap dz-reveal",
    img(pic("portrait-pro", 800, 1000), "dz-portrait", "Portrait"),
    floatcard("12 ans d'expérience", "+180 projets livrés", "left:-18px;bottom:64px", icon="fas fa-award"),
    floatcard("Disponible", "pour nouveaux projets", "right:-10px;top:36px", avatar="✓", cls="dz-float-slow"),
    round_badge("Disponible · 2026 · Paris · Remote · ", "right:-26px;bottom:-18px", "p1")))

HERO_PORTRAIT = add("Hero · portrait (présentation)", "fas fa-id-badge", box(
    "dz-hero",
    box("dz-container",
        box("dz-split",
            box("dz-mobile-center",
                text("Consultant data & IA · Paris", cls="dz-eyebrow", block=False),
                text("J'aide les équipes à <em>transformer leurs données</em> en décisions.", "h1", "dz-h1 dz-split-text"),
                text("Pipelines, tableaux de bord et automatisations sur mesure. Du cadrage à la mise en production, en restant simple à maintenir.", cls="dz-lead dz-reveal"),
                box("dz-cluster dz-reveal",
                    link("Prendre rendez-vous", "#contact", "dz-btn dz-btn-lg dz-magnetic", "fas fa-calendar"),
                    link("Voir mes projets", "#projets", "dz-btn dz-btn-lg dz-btn-ghost")),
                html("""
                <div class="dz-cluster dz-reveal" style="margin-top:2rem;--dz-gap:2rem">
                  <div class="dz-stat"><span class="dz-stat-value" data-dz-count="180" data-dz-suffix="+" style="font-size:2rem">0</span><span class="dz-stat-label">projets</span></div>
                  <div class="dz-stat"><span class="dz-stat-value" data-dz-count="4.9" data-dz-decimals="1" style="font-size:2rem">0</span><span class="dz-stat-label">note clients</span></div>
                  <div class="dz-stat"><span class="dz-stat-value" data-dz-count="12" style="font-size:2rem">0</span><span class="dz-stat-label">ans d'expérience</span></div>
                </div>""")),
            PORTRAIT_VIS)),
    el="section", full=True))

HERO_EDITO = add("Hero · éditorial (grand titre)", "fas fa-heading", section([
    html('<div class="dz-cluster" style="justify-content:space-between;margin-bottom:2.5rem"><span class="dz-index">01</span><span class="dz-small">Studio indépendant — depuis 2014</span><span class="dz-small">Paris · Dakar · Remote</span></div>'),
    text("Des marques <em>nettes</em>, des sites <em>rapides</em>, des outils qu'on a envie d'ouvrir.", "h1", "dz-display dz-split-text"),
    box("dz-split", text("Nous concevons et construisons des produits numériques pour les équipes qui veulent aller vite sans sacrifier la qualité.", cls="dz-lead dz-reveal"),
        box("dz-cluster dz-reveal", link("Démarrer un projet", "#contact", "dz-btn dz-btn-lg", "fas fa-arrow-right"), link("Réalisations", "#projets", "dz-btn dz-btn-lg dz-btn-link"))),
], cls="dz-hero"))

HERO_APP = add("Hero · app mobile (téléphone)", "fas fa-mobile-alt", box(
    "dz-hero dz-bg-mesh",
    box("dz-container",
        box("dz-split",
            box("dz-mobile-center",
                text("App iOS & Android", cls="dz-eyebrow", block=False),
                text("Votre entreprise, <em>dans leur poche</em>.", "h1", "dz-h1"),
                text("Réservations, suivi, messages et paiements. Une application simple, rapide et à votre image.", cls="dz-lead"),
                html("""
                <div class="dz-cluster">
                  <a class="dz-btn dz-btn-dark dz-btn-lg" href="#"><i class="fab fa-apple"></i> App Store</a>
                  <a class="dz-btn dz-btn-dark dz-btn-lg" href="#"><i class="fab fa-google-play"></i> Google Play</a>
                </div>""")),
            box("dz-portrait-wrap", box("dz-phone dz-tilt-on dz-reveal", img(pic("app-screen", 600, 1300), "", "Capture de l'application")),
                floatcard("Réservé ✓", "Samedi 10:30", "left:-10px;top:30%", icon="fas fa-check"),
                floatcard("Nouveau message", "Julie · il y a 1 min", "right:-14px;bottom:22%", avatar="JB", cls="dz-float-slow")))),
    el="section", full=True))

PHONE = add("Visuel · téléphone", "fas fa-mobile", box("dz-phone dz-reveal", img(pic("phone-shot", 600, 1300), "", "Capture")))
BROWSER = add("Visuel · navigateur", "fas fa-window-maximize", box("dz-browser dz-reveal", img(pic("web-shot", 1400, 900), "", "Capture du site")))
LAPTOP = add("Visuel · ordinateur portable", "fas fa-laptop", box("dz-laptop dz-reveal", box("", img(pic("laptop-shot", 1400, 900), "", "Capture"))))
WINDOW = add("App · fenêtre de bureau", "fas fa-desktop", html("""
<div class="dz-window dz-reveal"><div class="dz-window-bar"><i></i><i></i><i></i>Mon application — Tableau de bord</div>
<img src="https://picsum.photos/seed/desktop-app/1400/860" alt="" style="display:block;width:100%"></div>"""))

MARQUEE_XL = add("Web · texte géant défilant", "fas fa-text-width", box("dz-section-sm", html("""
<div class="dz-marquee dz-marquee-xl" data-dz-speed="40">
  <div class="dz-marquee-track">
    <span>Stratégie</span><span class="dz-sep">✦</span><span>Design</span><span class="dz-sep">✦</span><span>Développement</span><span class="dz-sep">✦</span><span>Automatisation</span><span class="dz-sep">✦</span>
  </div>
</div>"""), el="section", full=True))

WORDS = add("Web · manifeste mot à mot", "fas fa-align-center", section([
    text("Notre approche", cls="dz-eyebrow", block=False),
    text("On ne vend pas des sites. On construit des outils qui font gagner du temps, qu'on garde simples à faire évoluer, et qu'on mesure sur ce qui compte vraiment pour vous : des clients en plus, des heures en moins.", cls="dz-words dz-words-reveal"),
], narrow=True))


def stack_card(n, title, body, seed, cls=""):
    return box(f"dz-card {cls}", box("dz-split",
        box("", text(f"{n:02d}", cls="dz-index", block=False), text(title, "h3", "dz-h2"), text(body, cls="dz-lead")),
        img(pic(seed, 900, 700), "dz-rounded-lg", title)), style={"padding": "clamp(1.5rem,4vw,3rem)"})

STACK = add("Web · cartes empilées", "fas fa-layer-group", section([
    head("Méthode", "Trois étapes, zéro surprise", None),
    box("dz-stack-cards",
        stack_card(1, "Cadrer", "Un atelier pour comprendre vos objectifs, vos données et vos contraintes. Vous repartez avec un plan clair et chiffré.", "step-1"),
        stack_card(2, "Construire", "Des livraisons courtes, visibles chaque semaine. Vous testez tôt, on ajuste vite.", "step-2", "dz-card-soft"),
        stack_card(3, "Faire grandir", "Mesure, formation de l'équipe et améliorations continues. L'outil évolue avec vous.", "step-3")),
]))

HSCROLL = add("Web · galerie horizontale", "fas fa-arrows-alt-h", box("", html("""
<div data-dz-hscroll>
  <div class="dz-hscroll-sticky">
    <div class="dz-hscroll-track">
      <div class="dz-hpanel" style="width:min(80vw,420px);aspect-ratio:auto;background:none;border:0;display:flex;flex-direction:column;justify-content:center">
        <span class="dz-index">02</span><h2 class="dz-h2">Projets <em>récents</em></h2><p class="dz-lead">Faites défiler : la galerie avance à l'horizontale.</p>
      </div>
      <figure class="dz-hpanel"><img src="https://picsum.photos/seed/h1/1200/900" alt=""><figcaption><b>Refonte e-commerce</b><span>2026</span></figcaption></figure>
      <figure class="dz-hpanel"><img src="https://picsum.photos/seed/h2/1200/900" alt=""><figcaption><b>App de réservation</b><span>2026</span></figcaption></figure>
      <figure class="dz-hpanel"><img src="https://picsum.photos/seed/h3/1200/900" alt=""><figcaption><b>Tableau de bord BI</b><span>2025</span></figcaption></figure>
      <figure class="dz-hpanel"><img src="https://picsum.photos/seed/h4/1200/900" alt=""><figcaption><b>Identité de marque</b><span>2025</span></figcaption></figure>
    </div>
  </div>
</div>"""), el="section", full=True, cid="projets"))

TABS_V = add("Web · onglets + visuel (auto)", "fas fa-columns", section([
    head("Produit", "Tout votre quotidien, <em>au même endroit</em>", None),
    html("""
<div class="dz-tabs dz-tabs-v" data-dz-autoplay="6">
  <div class="dz-tabs-nav">
    <button data-tab="t1" aria-selected="true"><b>Suivi des clients</b><span>Toutes les infos, l'historique et les relances au même endroit.</span></button>
    <button data-tab="t2"><b>Automatisations</b><span>Les tâches répétitives partent toutes seules, au bon moment.</span></button>
    <button data-tab="t3"><b>Tableaux de bord</b><span>Des chiffres à jour pour décider vite.</span></button>
  </div>
  <div>
    <div class="dz-tab-panel" data-tab="t1"><img src="https://picsum.photos/seed/tab-1/1200/850" alt="" style="width:100%;display:block"></div>
    <div class="dz-tab-panel" data-tab="t2" hidden><img src="https://picsum.photos/seed/tab-2/1200/850" alt="" style="width:100%;display:block"></div>
    <div class="dz-tab-panel" data-tab="t3" hidden><img src="https://picsum.photos/seed/tab-3/1200/850" alt="" style="width:100%;display:block"></div>
  </div>
</div>""")]))

CTABLE = add("Web · tableau comparatif", "fas fa-table", section([
    head("Comparatif", "Pourquoi nous plutôt qu'un autre ?", None),
    html("""
<div class="dz-table-wrap"><table class="dz-ctable">
  <thead><tr><th></th><th class="dz-us">Nous</th><th>Agence classique</th><th>Freelance</th></tr></thead>
  <tbody>
    <tr><td>Livraison en moins de 4 semaines</td><td class="dz-us"><span class="dz-yes"></span></td><td><span class="dz-no"></span></td><td><span class="dz-yes"></span></td></tr>
    <tr><td>Design sur mesure</td><td class="dz-us"><span class="dz-yes"></span></td><td><span class="dz-yes"></span></td><td><span class="dz-no"></span></td></tr>
    <tr><td>Automatisations incluses</td><td class="dz-us"><span class="dz-yes"></span></td><td><span class="dz-no"></span></td><td><span class="dz-no"></span></td></tr>
    <tr><td>Vous restez propriétaire</td><td class="dz-us"><span class="dz-yes"></span></td><td><span class="dz-no"></span></td><td><span class="dz-yes"></span></td></tr>
    <tr><td>Support après la mise en ligne</td><td class="dz-us"><span class="dz-yes"></span></td><td><span class="dz-yes"></span></td><td><span class="dz-no"></span></td></tr>
  </tbody>
</table></div>""")], narrow=True))

ORBIT = add("Web · intégrations (orbite)", "fas fa-atom", section([
    box("dz-split",
        box("", text("Intégrations", cls="dz-eyebrow", block=False),
            text("Branché sur <em>les outils que vous utilisez déjà</em>", "h2", "dz-h2"),
            text("WhatsApp, e-mail, agendas, paiements, tableurs : les données circulent toutes seules entre vos outils.", cls="dz-lead"),
            link("Voir toutes les intégrations", "#", "dz-btn dz-btn-ghost", "fas fa-plug")),
        html("""
<div class="dz-orbit">
  <div class="dz-orbit-ring dz-r2"><span style="--a:0deg"><i class="fab fa-whatsapp"></i></span><span style="--a:72deg"><i class="fab fa-google"></i></span><span style="--a:144deg"><i class="fab fa-stripe-s"></i></span><span style="--a:216deg"><i class="fab fa-slack"></i></span><span style="--a:288deg"><i class="fab fa-github"></i></span></div>
  <div class="dz-orbit-ring dz-r1"><span style="--a:30deg"><i class="fas fa-envelope"></i></span><span style="--a:150deg"><i class="fas fa-calendar"></i></span><span style="--a:270deg"><i class="fas fa-table"></i></span></div>
  <div class="dz-orbit-center"><i class="fas fa-bolt"></i></div>
</div>"""))]))


def slide(q, name, role, ini):
    return f'<div class="dz-card dz-quote"><span class="dz-stars">★★★★★</span><blockquote>{q}</blockquote><div class="dz-person"><span class="dz-avatar">{ini}</span><div><div class="dz-person-name">{name}</div><div class="dz-person-role">{role}</div></div></div></div>'

SLIDER = add("Web · avis en carrousel", "fas fa-images", section([
    head("Avis", "Ce qu'en disent <em>nos clients</em>", None, left=True),
    html('<div data-dz-slider="6"><div class="dz-slider-track">' + "".join([
        slide("« On a remplacé quatre outils par un seul. L'équipe a enfin une vue claire. »", "Amélie L.", "Directrice commerciale", "AL"),
        slide("« Mise en place en une semaine. Les relances automatiques ont changé notre mois. »", "Karim M.", "Gérant, agence immobilière", "KM"),
        slide("« Beau, rapide, et nos clients adorent l'appli sur leur téléphone. »", "Sophie D.", "Fondatrice", "SD"),
        slide("« Un vrai partenaire : à l'écoute, rapide, et pédagogue. »", "Thomas G.", "DAF", "TG"),
        slide("« Le tableau de bord nous fait gagner une demi-journée par semaine. »", "Inès F.", "Responsable ops", "IF")]) + '</div></div>')]))


def work(seed, title, sub, tags):
    return f'<a class="dz-work" href="#" data-tags="{tags}"><img src="https://picsum.photos/seed/{seed}/900/700" alt="" loading="lazy"><div class="dz-work-info"><div><b>{title}</b><small>{sub}</small></div><span class="dz-arrow-circle">→</span></div></a>'

PORTFOLIO = add("Web · portfolio filtrable", "fas fa-th", section([
    head("Réalisations", "Quelques <em>projets</em>", None, left=True),
    html("""
<div class="dz-filters dz-chips" data-dz-filter="#dz-works">
  <button class="dz-chip" data-filter="*">Tout</button><button class="dz-chip" data-filter="web">Sites</button><button class="dz-chip" data-filter="app">Applications</button><button class="dz-chip" data-filter="data">Data</button>
</div>
<div class="dz-grid dz-grid-3" id="dz-works">""" + work("w1", "Maison Lune", "Site vitrine & réservation", "web") + work("w2", "Fleet Ops", "Application de suivi", "app") + work("w3", "Pulse BI", "Tableaux de bord", "data") + work("w4", "Atelier Nomade", "E-commerce", "web") + work("w5", "Agenda Pro", "App mobile", "app") + work("w6", "Lead Score", "Scoring & automatisation", "data") + "</div>")], cid="projets"))


def post(seed, cat, title, date):
    return f'<a class="dz-post" href="#"><div class="dz-post-img"><img src="https://picsum.photos/seed/{seed}/800/500" alt="" loading="lazy"></div><div class="dz-post-meta"><span class="dz-badge dz-badge-neutral">{cat}</span><span>{date}</span></div><h3>{title}</h3></a>'

BLOG = add("Web · articles de blog", "fas fa-newspaper", section([
    box("dz-page-head", text("Le journal", "h2", "dz-h2 dz-mb-0"), link("Tous les articles", "#", "dz-btn dz-btn-ghost dz-btn-sm", "fas fa-arrow-right")),
    html('<div class="dz-grid dz-grid-3">' + post("b1", "Méthode", "Comment cadrer un projet data en une journée", "12 sept. 2026") + post("b2", "Produit", "Cinq automatisations qui font gagner une journée par semaine", "3 sept. 2026") + post("b3", "Cas client", "De l'Excel partagé à l'application métier en 3 semaines", "28 août 2026") + "</div>")]))

LOGO_GRID = add("Web · grille de logos", "fas fa-border-all", section([
    text("Ils nous font confiance", cls="dz-eyebrow dz-center", block=True),
    html('<div class="dz-logo-grid">' + "".join(f'<div><span class="dz-logo"><i class="fas fa-{i}"></i> {n}</span></div>' for i, n in [("cube", "Nexora"), ("leaf", "Verdant"), ("bolt", "Voltix"), ("gem", "Lumia"), ("mountain", "Altura"), ("atom", "Quanta"), ("feather-alt", "Plume"), ("anchor", "Port")]) + "</div>")], cls="dz-section-sm"))

FOOTER_XL = add("Web · pied de page géant", "fas fa-font", box("dz-footer", html("""
<div class="dz-container">
  <div class="dz-split" style="align-items:end">
    <div><span class="dz-eyebrow">Un projet ?</span><h2 class="dz-h2" style="margin:0">Parlons-en <em>autour d'un café</em>.</h2></div>
    <div class="dz-cluster" style="justify-content:flex-end"><a class="dz-btn dz-btn-lg" href="mailto:contact@exemple.fr">contact@exemple.fr</a></div>
  </div>
  <div class="dz-footer-bottom"><span>© 2026 Marque</span><div class="dz-socials"><a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a><a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a><a href="#" aria-label="GitHub"><i class="fab fa-github"></i></a></div><span>Mentions légales · Confidentialité</span></div>
</div>
<div class="dz-wordmark">Marque</div>"""), el="footer", full=True))

PAGE404 = add("Web · page 404", "fas fa-question", section([
    box("dz-center", text("404", cls="dz-huge dz-split-text"), text("Cette page s'est <em>perdue en chemin</em>.", "h2", "dz-h3"),
        text("Le lien est peut-être ancien, ou la page a changé d'adresse.", cls="dz-lead"),
        box("dz-cluster", link("Retour à l'accueil", "/", "dz-btn dz-btn-lg", "fas fa-home")))], cls="dz-hero dz-hero-full"))

COOKIE = add("Web · bandeau cookies", "fas fa-cookie-bite", html("""
<div class="dz-cookie" data-dz-cookie>
  <div><b>Cookies</b><br>On utilise uniquement des cookies utiles au bon fonctionnement du site et à la mesure d'audience.</div>
  <div class="dz-cluster"><button class="dz-btn dz-btn-sm" data-accept>Accepter</button><button class="dz-btn dz-btn-sm dz-btn-ghost" data-refuse>Refuser</button><a class="dz-small" href="#">En savoir plus</a></div>
</div>"""))

# ---------- applications
APP_SIDE = """
<aside class="dz-side">
  <a class="dz-brand" href="/"><span class="dz-brand-mark"></span>Marque</a>
  <div class="dz-search" data-dz-cmdk-open style="margin:0 .2rem .5rem"><i class="fas fa-search"></i><span>Rechercher…</span><span class="dz-kbd">Ctrl K</span></div>
  <div class="dz-side-label">Général</div>
  <a class="dz-side-item dz-active" href="#"><i class="fas fa-home"></i>Tableau de bord</a>
  <a class="dz-side-item" href="#"><i class="fas fa-users"></i>Clients<span class="dz-count">128</span></a>
  <a class="dz-side-item" href="#"><i class="fas fa-file-invoice"></i>Factures</a>
  <a class="dz-side-item" href="#"><i class="fas fa-inbox"></i>Messages<span class="dz-count">4</span></a>
  <div class="dz-side-label">Outils</div>
  <a class="dz-side-item" href="#"><i class="fas fa-bolt"></i>Automatisations</a>
  <a class="dz-side-item" href="#"><i class="fas fa-chart-pie"></i>Rapports</a>
  <a class="dz-side-item" href="#"><i class="fas fa-cog"></i>Réglages</a>
  <div class="dz-side-foot"><span class="dz-avatar dz-avatar-sm">SD</span><div style="line-height:1.2"><b style="font-size:.88rem">Sidy</b><div class="dz-small">Admin</div></div></div>
</aside>"""
APP_TOP = """
<header class="dz-app-top">
  <button class="dz-btn dz-btn-ghost dz-icon-btn dz-only-mobile" data-dz-open="#dz-mobile-side" aria-label="Menu"><i class="fas fa-bars"></i></button>
  <div class="dz-search" data-dz-cmdk-open><i class="fas fa-search"></i><span>Rechercher un client, une facture…</span><span class="dz-kbd">Ctrl K</span></div>
  <div class="dz-cluster" style="margin-left:auto;--dz-gap:.4rem">
    <button class="dz-btn dz-btn-ghost dz-icon-btn dz-theme-btn" data-dz-theme-toggle aria-label="Thème"><i class="fas fa-moon dz-moon"></i><i class="fas fa-sun dz-sun"></i></button>
    <button class="dz-btn dz-btn-ghost dz-icon-btn" data-dz-open="#dz-notif-drawer" aria-label="Notifications" data-dz-tip="Notifications"><i class="fas fa-bell"></i></button>
    <span class="dz-avatar dz-avatar-sm">SD</span>
  </div>
</header>"""

CMDK = add("App · palette de commandes (Ctrl K)", "fas fa-terminal", html("""
<div data-dz-cmdk class="dz-cmdk">
  <div class="dz-cmdk-box">
    <input placeholder="Tapez une commande ou cherchez…" aria-label="Recherche">
    <div class="dz-cmdk-list">
      <div class="dz-cmdk-group">Aller à</div>
      <a href="/"><i class="fas fa-home"></i>Accueil</a>
      <a href="#" data-keywords="clients contacts"><i class="fas fa-users"></i>Clients</a>
      <a href="#" data-keywords="facture paiement"><i class="fas fa-file-invoice"></i>Factures</a>
      <div class="dz-cmdk-group">Actions</div>
      <a href="#" data-keywords="ajouter nouveau"><i class="fas fa-plus"></i>Nouveau client</a>
      <a href="#" data-dz-theme-toggle><i class="fas fa-adjust"></i>Changer de thème</a>
      <div class="dz-cmdk-empty" hidden>Aucun résultat</div>
    </div>
    <div class="dz-cmdk-foot"><span><span class="dz-kbd">↑↓</span> naviguer</span><span><span class="dz-kbd">Entrée</span> ouvrir</span><span><span class="dz-kbd">Échap</span> fermer</span></div>
  </div>
</div>"""))

NOTIF_DRAWER = """
<div class="dz-drawer" id="dz-notif-drawer" style="padding:0">
  <div class="dz-notifs" style="border:0;border-radius:0">
    <div class="dz-notifs-head"><b>Notifications</b><button class="dz-btn dz-btn-ghost dz-btn-sm" data-dz-close>Fermer</button></div>
    <div class="dz-notif dz-unread"><span class="dz-avatar dz-avatar-sm">JB</span><div><b>Julie</b> a accepté le devis #1042<time>il y a 5 min</time></div></div>
    <div class="dz-notif dz-unread"><span class="dz-icon" style="width:32px;height:32px;font-size:.8rem"><i class="fas fa-bolt"></i></span><div>Automatisation <b>Relance J+2</b> exécutée (12 envois)<time>il y a 1 h</time></div></div>
    <div class="dz-notif"><span class="dz-avatar dz-avatar-sm">KM</span><div><b>Karim</b> vous a mentionné<time>hier</time></div></div>
  </div>
</div>
<div class="dz-drawer dz-left" id="dz-mobile-side" style="padding:0">""" + APP_SIDE.replace('class="dz-side"', 'class="dz-side" style="display:flex;position:relative;height:100%;border:0"') + "</div>"

APP_SHELL = add("App · coquille (menu + barre)", "fas fa-columns", box(
    "dz-app",
    html(APP_SIDE),
    box("dz-app-main",
        html(APP_TOP + NOTIF_DRAWER),
        box("dz-app-body",
            text("⬇ Glisse ici les blocs « App » (en-tête, KPI, cartes) et tes vues Saltcorn. Supprime ce texte ensuite.", cls="dz-callout"))),
    full=True))

SETTINGS = add("App · page de réglages", "fas fa-sliders-h", html("""
<div class="dz-settings">
  <nav class="dz-settings-nav"><a class="dz-active" href="#">Profil</a><a href="#">Compte</a><a href="#">Notifications</a><a href="#">Facturation</a><a href="#">Sécurité</a></nav>
  <div>
    <h2 class="dz-h3">Notifications</h2><p class="dz-text">Choisissez comment et quand vous êtes prévenu.</p>
    <div class="dz-setting"><div><b>E-mails de résumé</b><p>Un récapitulatif chaque lundi matin.</p></div><div style="justify-self:end"><input type="checkbox" class="dz-switch" checked></div></div>
    <div class="dz-setting"><div><b>Nouveaux leads</b><p>Alerte immédiate sur WhatsApp.</p></div><div style="justify-self:end"><input type="checkbox" class="dz-switch" checked></div></div>
    <div class="dz-setting"><div><b>Double authentification</b><p>Code demandé à chaque connexion.</p></div><div style="justify-self:end"><input type="checkbox" class="dz-switch"></div></div>
    <div class="dz-setting"><div><b>Langue</b><p>Langue de l'interface.</p></div><select class="form-select"><option>Français</option><option>English</option></select></div>
  </div>
</div>"""))

PROFILE = add("App · en-tête de profil", "fas fa-user", html("""
<div class="dz-profile">
  <div class="dz-profile-cover"></div>
  <div class="dz-profile-body">
    <span class="dz-avatar">SD</span>
    <div><h2 class="dz-h3" style="margin:0">Sidy D.</h2><div class="dz-small">Data Engineer · Paris</div></div>
    <div class="dz-profile-stats"><div><b>128</b><span>clients</span></div><div><b>42</b><span>projets</span></div><div><b>4,9</b><span>note</span></div></div>
    <div class="dz-cluster" style="--dz-gap:.5rem"><a class="dz-btn dz-btn-sm" href="#">Message</a><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Modifier</a></div>
  </div>
</div>"""))

STEPPER = add("App · étapes (assistant)", "fas fa-list-ol", html("""
<div class="dz-card" style="gap:1.5rem">
  <ol class="dz-stepper"><li class="dz-done">Compte</li><li class="dz-current">Entreprise</li><li>Équipe</li><li>Terminé</li></ol>
  <div><h3 class="dz-h4">Votre entreprise</h3><p class="dz-text">⬇ Glisse ici la vue Edit de l'étape.</p></div>
  <div class="dz-cluster" style="justify-content:space-between"><a class="dz-btn dz-btn-ghost" href="#">← Retour</a><a class="dz-btn" href="#">Continuer →</a></div>
</div>"""))

CHIPS = add("App · filtres (puces)", "fas fa-tags", html("""
<div class="dz-chips" data-dz-toggle><button class="dz-chip" aria-pressed="true">Tous</button><button class="dz-chip">Actifs</button><button class="dz-chip">En attente</button><button class="dz-chip">Archivés</button><button class="dz-chip"><i class="fas fa-plus"></i> Filtre</button></div>"""))

NOTIFS = add("App · notifications", "fas fa-bell", html("""
<div class="dz-notifs">
  <div class="dz-notifs-head"><b>Notifications</b><a class="dz-small" href="#">Tout marquer comme lu</a></div>
  <div class="dz-notif dz-unread"><span class="dz-avatar dz-avatar-sm">JB</span><div><b>Julie</b> a accepté le devis #1042<time>il y a 5 min</time></div></div>
  <div class="dz-notif dz-unread"><span class="dz-icon" style="width:32px;height:32px;font-size:.8rem"><i class="fas fa-bolt"></i></span><div>Automatisation <b>Relance J+2</b> exécutée<time>il y a 1 h</time></div></div>
  <div class="dz-notif"><span class="dz-avatar dz-avatar-sm">KM</span><div><b>Karim</b> vous a mentionné dans <b>Projet Lune</b><time>hier</time></div></div>
</div>"""))

CHAT = add("App · discussion (chat)", "fas fa-comments", html("""
<div class="dz-card" style="padding:0;gap:0">
  <div class="dz-notifs-head" style="display:flex;justify-content:space-between;align-items:center;padding:1rem 1.2rem;border-bottom:1px solid var(--dz-border)"><div class="dz-person"><span class="dz-avatar dz-avatar-sm">JB</span><div><b>Julie B.</b><div class="dz-small"><span class="dz-dot" style="color:var(--dz-success);display:inline-block"></span> en ligne</div></div></div><i class="fas fa-ellipsis-h"></i></div>
  <div class="dz-chat">
    <div class="dz-msg">Bonjour ! Le devis est bien reçu, merci 🙏<time>10:12</time></div>
    <div class="dz-msg dz-me">Parfait. On peut démarrer lundi ?<time>10:14</time></div>
    <div class="dz-msg">Oui, lundi 9h ça me va.<time>10:15</time></div>
    <div class="dz-typing"><i></i><i></i><i></i></div>
  </div>
  <div class="dz-composer"><input placeholder="Écrire un message…"><button class="dz-btn dz-icon-btn" aria-label="Envoyer"><i class="fas fa-paper-plane"></i></button></div>
</div>"""))

CHECKLIST = add("App · check-list d'accueil", "fas fa-tasks", html("""
<div class="dz-card">
  <div class="dz-cluster" style="justify-content:space-between"><h3 class="dz-h4">Bien démarrer</h3><span class="dz-small">2 / 4</span></div>
  <div class="dz-progress" data-dz-value="50"><span></span></div>
  <div class="dz-checklist"><a class="dz-check dz-done" href="#">Créer votre compte</a><a class="dz-check dz-done" href="#">Importer vos clients</a><a class="dz-check" href="#">Inviter votre équipe</a><a class="dz-check" href="#">Activer une automatisation</a></div>
</div>"""))

DROPZONE = add("App · zone de dépôt", "fas fa-cloud-upload-alt", html("""
<div class="dz-dropzone"><span class="dz-icon dz-icon-lg"><i class="fas fa-cloud-upload-alt"></i></span><b>Glissez vos fichiers ici</b><span class="dz-small">PDF, images ou Excel — 20 Mo max.</span><span class="dz-small">(pour l'envoi réel, utilise un champ Fichier dans une vue Edit)</span></div>"""))

# ---------- mobile
APPBAR = add("Mobile · barre d'app + grand titre", "fas fa-mobile-alt", html("""
<div class="dz-appbar"><a href="javascript:history.back()" aria-label="Retour"><i class="fas fa-chevron-left"></i></a><div class="dz-appbar-title">Réservations</div><button aria-label="Ajouter" data-dz-open="#dz-sheet-new"><i class="fas fa-plus"></i></button></div>
<h1 class="dz-largetitle">Réservations</h1>"""))

IOSLIST = add("Mobile · liste type réglages", "fas fa-list", html("""
<div class="dz-ios-head">Compte</div>
<div class="dz-ios-list">
  <a class="dz-cell dz-chev" href="#"><span class="dz-cell-icon" style="--c:#2d7ff9"><i class="fas fa-user"></i></span><span class="dz-cell-label">Profil</span></a>
  <a class="dz-cell dz-chev" href="#"><span class="dz-cell-icon" style="--c:#ff9f0a"><i class="fas fa-bell"></i></span><span class="dz-cell-label">Notifications</span><span class="dz-cell-value">Activées</span></a>
  <label class="dz-cell"><span class="dz-cell-icon" style="--c:#30d158"><i class="fas fa-moon"></i></span><span class="dz-cell-label">Mode sombre</span><input type="checkbox" class="dz-switch" data-dz-theme-toggle></label>
</div>
<div class="dz-ios-head">Aide</div>
<div class="dz-ios-list">
  <a class="dz-cell dz-chev" href="#"><span class="dz-cell-icon" style="--c:#8e8e93"><i class="fas fa-question"></i></span><span class="dz-cell-label">Centre d'aide</span></a>
  <a class="dz-cell dz-chev" href="#"><span class="dz-cell-icon" style="--c:#ff375f"><i class="fas fa-heart"></i></span><span class="dz-cell-label">Nous noter</span></a>
</div>"""))

SHEET = add("Mobile · feuille du bas", "fas fa-window-restore", html("""
<button class="dz-btn" data-dz-open="#dz-sheet-new"><i class="fas fa-plus"></i> Nouvelle réservation</button>
<div class="dz-sheet" id="dz-sheet-new">
  <h3 class="dz-h4">Nouvelle réservation</h3>
  <p class="dz-text">⬇ Glisse ici ta vue Edit.</p>
  <div class="dz-cluster" style="margin-top:1rem"><button class="dz-btn dz-btn-block" data-dz-close>Valider</button></div>
</div>"""))

DRAWER = add("Outil · tiroir latéral", "fas fa-bars", html("""
<button class="dz-btn dz-btn-ghost" data-dz-open="#dz-drawer-demo"><i class="fas fa-filter"></i> Filtres</button>
<div class="dz-drawer" id="dz-drawer-demo">
  <div class="dz-cluster" style="justify-content:space-between;margin-bottom:1rem"><h3 class="dz-h4" style="margin:0">Filtres</h3><button class="dz-btn dz-btn-ghost dz-icon-btn" data-dz-close aria-label="Fermer">✕</button></div>
  <p class="dz-text">⬇ Glisse ici une vue Filter.</p>
</div>"""))

STORIES = add("Mobile · stories", "fas fa-circle-notch", html('<div class="dz-stories">' + "".join(
    f'<a class="dz-story{" dz-seen" if i > 3 else ""}" href="#"><span><img src="https://picsum.photos/seed/st{i}/120/120" alt=""></span>{n}</a>'
    for i, n in enumerate(["Nouveautés", "Promo", "Équipe", "Coulisses", "Avis", "Atelier"])) + "</div>"))

# ------------------------------------------------------------------ pages de démo
def page(name, title, desc, blocks, no_menu=False, fluid=False):
    return {"name": name, "title": title, "description": desc, "min_role": 1,
            "layout": {"above": blocks}, "fixed_states": {}, "menu_label": None,
            "attributes": {"no_menu": no_menu, "request_fluid_layout": fluid},
            "root_page_for_roles": []}

LANDING = page("dz-demo-landing", "Démo landing SaaS", "Landing complète construite avec les blocs du kit",
               [TOPBAR, NAV, HERO_SPLIT, LOGOS, WORDS, FEATURES, TABS_V, STACK, BENTO, ORBIT, STATS, PRICING, CTABLE, SLIDER, FAQ, CTA, FOOTER, COOKIE],
               no_menu=True, fluid=True)

PORTRAIT_PAGE = page("dz-demo-portrait", "Démo présentation perso", "Site de présentation d'une personne (consultant, freelance, coach)",
                     [NAV, HERO_PORTRAIT, MARQUEE_XL, WORDS, PORTFOLIO, HSCROLL, SLIDER, BLOG, LEAD, FOOTER_XL],
                     no_menu=True, fluid=True)

AGENCY = page("dz-demo-studio", "Démo studio", "Vitrine d'agence, grand titre éditorial",
              [NAV, HERO_EDITO, MARQUEE_XL, STACK, LOGO_GRID, TEAM, WALL, COUNTDOWN, FOOTER_XL], no_menu=True, fluid=True)

DASH = page("dz-demo-app", "Démo application", "Application web : menu latéral, barre, palette Ctrl K, KPI, cartes",
            [box("dz-app", html(APP_SIDE), box("dz-app-main", html(APP_TOP + NOTIF_DRAWER),
                 box("dz-app-body", PAGEHEAD, CHECKLIST, KPI, cols([VIEWCARD, NOTIFS], [8, 4], bp="lg", cls="g-4"),
                     CHIPS, cols([CHAT, ACTIVITY], [7, 5], bp="lg", cls="g-4"), SETTINGS, CALLOUTS, EMPTY)), full=True),
             CMDK], no_menu=True, fluid=True)

MOBILE = page("dz-demo-mobile", "Démo app mobile", "Écrans mobiles : barre d'app, stories, listes, feuille, onglets",
              [box("dz-container-narrow", APPBAR, STORIES, box("", SCROLLER, style={"padding": "1rem"}), IOSLIST, SHEET, BOTTOMNAV, FAB)],
              no_menu=True)

PAGE404_PAGE = page("dz-404", "Page introuvable", "Modèle de page 404", [NAV, PAGE404], no_menu=True, fluid=True)

CATALOGUE = page("dz-catalogue", "Catalogue du kit", "Tous les blocs du kit sur une page",
                 [b["layout"] for b in LIB if b["name"] not in ("Mobile · onglets bas", "Mobile · bouton flottant", "App · coquille (menu + barre)", "App · palette de commandes (Ctrl K)", "Web · bandeau cookies", "Web · page 404")],
                 no_menu=True, fluid=True)


# ---- blocs écrits à la main : blocks/*.html (voir blocks/README.md) ----
# En-tête facultatif en première ligne :
# <!-- name: Web · Mon bloc | icon: fas fa-star | wrap: section -->
# puis le HTML ; <style>…</style> et <script>…</script> sont gardés tels quels.
import glob, re as _re
for f in sorted(glob.glob(os.path.join(HERE, "..", "blocks", "*.html"))):
    src = open(f, encoding="utf-8").read()
    meta = {"name": "Code · " + os.path.splitext(os.path.basename(f))[0].replace("-", " "), "icon": "fas fa-code", "wrap": "none"}
    m = _re.match(r"\s*<!--(.*?)-->", src, _re.S)
    if m:
        for part in m.group(1).split("|"):
            if ":" in part:
                k, v = part.split(":", 1); meta[k.strip()] = v.strip()
        src = src[m.end():].strip()
    body = src
    if meta["wrap"] == "section": body = f'<section class="dz-section"><div class="dz-container">{src}</div></section>'
    if meta["wrap"] == "full": body = f'<section class="dz-section dz-flush">{src}</section>'
    LIB.append({"name": meta["name"], "icon": meta["icon"], "layout": {"type": "blank", "isHTML": True, "contents": body}})

# ---- familles : blocs historiques (renommés) + modules tools/packs/*.py ----
import sys as _sys, importlib
_sys.path.insert(0, HERE)
from families import FAMILIES, ORDER, prefix
OLD_PREFIX = {"Web · ": ("site", ""), "Hero · ": ("site", "hero "), "Nav · ": ("site", "menu "), "Visuel · ": ("site", "visuel "),
              "App · ": ("app", ""), "Mobile · ": ("mobile", ""), "Outil · ": ("outils", ""), "Code · ": ("outils", "")}
PREVIOUS = []
for b in LIB:
    for op, (fam, extra) in OLD_PREFIX.items():
        if b["name"].startswith(op):
            PREVIOUS.append(b["name"])
            b["family"] = fam
            b["name"] = prefix(fam) + extra + b["name"][len(op):]
            break
    else:
        b.setdefault("family", "outils")


def wrap_html(h, wrap):
    h = textwrap.dedent(h).strip()
    if wrap == "section":
        return f'<section class="dz-section"><div class="dz-container">{h}</div></section>'
    if wrap == "narrow":
        return f'<section class="dz-section"><div class="dz-container-narrow">{h}</div></section>'
    if wrap == "full":
        return f'<section class="dz-section dz-flush">{h}</section>'
    if wrap == "app":
        return f'<div class="dz-app-pad">{h}</div>'
    return h


for mod_file in sorted(glob.glob(os.path.join(HERE, "packs", "*.py"))):
    mod_name = os.path.splitext(os.path.basename(mod_file))[0]
    if mod_name.startswith("_"):
        continue
    mod = importlib.import_module("packs." + mod_name)
    fam = mod.FAMILY
    assert fam in FAMILIES, f"famille inconnue : {fam} ({mod_file})"
    for blk in mod.BLOCKS:
        name = prefix(fam) + blk["name"]
        assert not any(x["name"] == name for x in LIB), f"nom en double : {name}"
        seg = {"type": "blank", "isHTML": True, "contents": wrap_html(blk["html"], blk.get("wrap", "section"))}
        if blk.get("raw"):
            seg["dz_raw"] = True
        LIB.append({"name": name, "icon": blk.get("icon", FAMILIES[fam][1]), "layout": seg, "family": fam})

# ---- conversion en éléments natifs du builder (modifiables sans code) ----
from html2layout import convert_layout
RAW_OUT = {"library": [dict(b) for b in LIB]}
json.dump(RAW_OUT, open(os.path.join(OUT, "blocks.raw.json"), "w"), ensure_ascii=False)
for b in LIB:
    b["layout"] = convert_layout(b["layout"])
for P_ in [LANDING, PORTRAIT_PAGE, AGENCY, DASH, MOBILE, PAGE404_PAGE, CATALOGUE]:
    P_["layout"] = convert_layout(P_["layout"])

LIB.sort(key=lambda b: (ORDER.index(b["family"]), b["name"]))
fam_index = {f: {"label": FAMILIES[f][0], "icon": FAMILIES[f][1], "description": FAMILIES[f][2],
                 "blocks": [b["name"] for b in LIB if b["family"] == f]} for f in ORDER}
library = [{"name": b["name"], "icon": b["icon"], "layout": b["layout"]} for b in LIB]

# ---- page dz-catalogue : l'index de TOUTES les familles (générée) ----
from html import escape as _esc
_cards = "".join(
    f'<a class="dz-card dz-card-hover dz-card-link" href="/page/dz-famille-{k}">'
    f'<span class="dz-icon"><i class="{v["icon"]}"></i></span>'
    f'<h3 class="dz-h4">{_esc(v["label"])} <span class="dz-badge dz-badge-neutral">{len(v["blocks"])} blocs</span></h3>'
    f'<p class="dz-text">{_esc(v["description"])}</p></a>'
    for k, v in fam_index.items() if v["blocks"])
CATALOGUE["layout"] = convert_layout({"type": "blank", "isHTML": True, "contents": f"""
<section class="dz-section"><div class="dz-container">
  <div class="dz-section-head"><span class="dz-eyebrow">Catalogue</span>
    <h1 class="dz-h1">Les {len(LIB)} blocs du kit</h1>
    <p class="dz-lead">{sum(1 for v in fam_index.values() if v["blocks"])} familles. Clique sur une famille pour ouvrir sa page de démo (modifiable dans l'éditeur). Tout voir d'un coup : <a href="/dysizz-ui/galerie?f=all">galerie complète</a> (admin).</p></div>
  <div class="dz-grid dz-grid-3">{_cards}</div>
</div></section>"""})
# ---- une page de démo par famille : tous ses blocs, modifiables dans le builder ----
import re as _re
_FIXED = _re.compile(r"dz-(nav|cookie|bottom-nav|bottomnav|fab|cmdk|drawer|sheet|to-top|scroll-progress|topbar)\b")
_fam_nav = "".join(f'<a class="dz-chip" href="/page/dz-famille-{k}">{_esc(v["label"])}</a>'
                   for k, v in fam_index.items() if v["blocks"])
FAMILY_PAGES = []
for k, v in fam_index.items():
    if not v["blocks"]:
        continue
    head_html = f"""<section class="dz-section dz-demo-head"><div class="dz-container">
  <div class="dz-section-head"><span class="dz-eyebrow"><a href="/page/dz-catalogue">Catalogue</a> · famille</span>
    <h1 class="dz-h1">{_esc(v["label"])}</h1>
    <p class="dz-lead">{_esc(v["description"])} — {len(v["blocks"])} blocs. Ouvre cette page dans l'éditeur pour modifier ou copier un bloc.</p></div>
  <div class="dz-demo-fams">{_fam_nav}</div>
</div></section>"""
    blocks = [convert_layout({"type": "blank", "isHTML": True, "contents": head_html})]
    for b in LIB:
        if b["family"] != k:
            continue
        fixed = bool(_FIXED.search(json.dumps(b["layout"])))
        label = text(_esc(b["name"]) + (' <span class="dz-demo-note">élément fixe ou qui s\'ouvre au clic : montré dans un cadre</span>' if fixed else ""),
                     )
        blocks.append(box("dz-demo-label", label))
        blocks.append(box("dz-demo-frame", b["layout"]) if fixed else b["layout"])
    FAMILY_PAGES.append(page(f"dz-famille-{k}", f"Famille · {v['label']}", f"Tous les blocs de la famille {v['label']}",
                             blocks, no_menu=True, fluid=True))

json.dump({"tables": [], "views": [], "plugins": [], "pages": [], "triggers": [], "roles": [], "library": library,
           "families": fam_index, "previous": PREVIOUS},
          open(os.path.join(OUT, "blocks.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"tables": [], "views": [], "plugins": [], "pages": [LANDING, PORTRAIT_PAGE, AGENCY, DASH, MOBILE, PAGE404_PAGE, CATALOGUE] + FAMILY_PAGES, "triggers": [], "roles": [], "library": []},
          open(os.path.join(OUT, "demo-pages.json"), "w"), ensure_ascii=False, indent=1)
print(len(LIB), "blocs ;", sum(1 for f in fam_index.values() if f["blocks"]), "familles ;", 7 + len(FAMILY_PAGES), "pages")
