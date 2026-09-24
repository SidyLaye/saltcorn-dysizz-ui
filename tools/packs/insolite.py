"""Famille « Insolite » : blocs surprenants, mémorables… et utiles.
CSS : styles/42-insolite.css — préfixe dz-in-"""
import random as _random

FAMILY = "insolite"


def _qr(seed, n=25):
    """petit motif façon QR code (décoratif), dessiné en un seul chemin SVG"""
    rnd = _random.Random(seed)
    cells = set()
    for y in range(n):
        for x in range(n):
            if rnd.random() < .47:
                cells.add((x, y))
    # trois repères carrés dans les coins
    for ox, oy in ((0, 0), (n - 7, 0), (0, n - 7)):
        for y in range(-1, 8):
            for x in range(-1, 8):
                cells.discard((ox + x, oy + y))
        for y in range(7):
            for x in range(7):
                ring = x in (0, 6) or y in (0, 6)
                core = 2 <= x <= 4 and 2 <= y <= 4
                if ring or core:
                    cells.add((ox + x, oy + y))
    d = "".join(f"M{x} {y}h1v1h-1z" for x, y in sorted(cells))
    return f'<svg class="dz-in-qr" viewBox="-1 -1 {n + 2} {n + 2}" aria-hidden="true"><path d="{d}"/></svg>'


_DOORS = [
    (1, "fas fa-mug-hot", "Café offert"), (2, "fas fa-percent", "−15 % sur tout"), (3, "fas fa-truck", "Livraison offerte"),
    (4, "fas fa-book-open", "Guide à télécharger"), (5, "fas fa-gift", "Surprise en boutique"), (6, "fas fa-cookie-bite", "Atelier biscuits"),
    (7, "fas fa-music", "Playlist d'hiver"), (8, "fas fa-ticket-alt", "2 places à gagner"), (9, None, None), (10, None, None),
    (11, None, None), (12, None, None), (13, None, None), (14, None, None), (15, None, None), (16, None, None),
    (17, None, None), (18, None, None), (19, None, None), (20, None, None), (21, None, None), (22, None, None),
    (23, None, None), (24, None, None),
]


def _advent():
    out = []
    for n, icon, txt in _DOORS:
        opened = icon is not None
        big = " dz-in-door-big" if n == 24 else (" dz-in-door-wide" if n in (6, 11, 17) else "")
        tone = " dz-in-tone-%d" % (n % 4)
        inside_icon = icon or "fas fa-star"
        inside_txt = txt or "Bientôt…"
        out.append(f"""
  <div class="dz-in-door-wrap{big}{' dz-in-open' if opened else ''}">
    <div class="dz-in-door-inside"><i class="{inside_icon}"></i><span class="dz-in-door-gift">{inside_txt}</span></div>
    <div class="dz-in-door{tone}"><span class="dz-in-door-num">{n}</span></div>
  </div>""")
    return "".join(out)


BLOCKS = [
    # ------------------------------------------------------------------ terminal
    dict(
        name="terminal",
        icon="fas fa-terminal",
        html="""
<div class="dz-split dz-in-term-split">
  <div>
    <span class="dz-eyebrow">Ligne de commande</span>
    <h2 class="dz-h2">De votre poste à la production en <em>une commande</em>.</h2>
    <p class="dz-lead">La CLI Nexora compile, teste et publie votre application. Retour arrière instantané, journaux en direct, zéro configuration.</p>
    <div class="dz-cluster">
      <a class="dz-btn" href="#"><i class="fas fa-download"></i> Installer la CLI</a>
      <a class="dz-btn dz-btn-ghost" href="#">Lire la documentation</a>
    </div>
    <div class="dz-in-term-install dz-copy-scope">
      <code class="dz-in-term-code">npm i -g @nexora/cli</code>
      <a class="dz-in-term-copy dz-copy" href="#" aria-label="Copier la commande"><i class="far fa-copy"></i></a>
    </div>
  </div>
  <div class="dz-in-term dz-reveal">
    <div class="dz-in-term-bar">
      <div class="dz-in-lights"><i class="dz-in-l1"></i><i class="dz-in-l2"></i><i class="dz-in-l3"></i></div>
      <span class="dz-in-term-title">lea@nexora — ~/boutique — zsh</span>
      <span class="dz-in-term-size">120×32</span>
    </div>
    <div class="dz-in-term-body">
      <p class="dz-in-term-line"><span class="dz-in-term-ps">~/boutique</span><span class="dz-in-term-git">main ✓</span><span class="dz-in-term-cmd">nexora deploy --prod</span></p>
      <p class="dz-in-term-out">▸ Analyse du projet… 248 modules, 3 fonctions</p>
      <p class="dz-in-term-out">▸ Tests : 412 réussis, 0 échec <span class="dz-in-term-dim">(6,8 s)</span></p>
      <p class="dz-in-term-ok">✓ Build optimisé — 184 Ko (−12 %)</p>
      <p class="dz-in-term-ok">✓ Migration de la base : 2 tables mises à jour</p>
      <p class="dz-in-term-warn">! 1 variable d'environnement obsolète : SMTP_PORT</p>
      <p class="dz-in-term-ok">✓ En ligne sur <span class="dz-in-term-link">boutique.nexora.app</span> en 21 s</p>
      <p class="dz-in-term-line"><span class="dz-in-term-ps">~/boutique</span><span class="dz-in-term-git">main ✓</span><span class="dz-in-term-cmd dz-typewriter">nexora logs --follow | nexora status | nexora rollback v2.4.1</span></p>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ fenêtre rétro
    dict(
        name="fenêtre rétro",
        icon="fas fa-window-maximize",
        html="""
<div class="dz-in-retro-stage">
  <div class="dz-in-retro dz-reveal">
    <div class="dz-in-retro-title">
      <span class="dz-in-retro-name"><i class="fas fa-save"></i> Assistant de sauvegarde</span>
      <div class="dz-in-retro-ctrls"><span class="dz-in-retro-ctrl">_</span><span class="dz-in-retro-ctrl">□</span><span class="dz-in-retro-ctrl">×</span></div>
    </div>
    <div class="dz-in-retro-menu"><span><u>F</u>ichier</span><span><u>É</u>dition</span><span><u>A</u>ffichage</span><span><u>?</u></span></div>
    <div class="dz-in-retro-body">
      <div class="dz-in-retro-msg">
        <span class="dz-in-retro-icon"><i class="fas fa-hdd"></i></span>
        <div>
          <p class="dz-in-retro-strong">Copie de vos fichiers en cours…</p>
          <p class="dz-in-retro-text">Dossier : C:\\Clients\\Atelier Lune\\Factures 2026</p>
          <p class="dz-in-retro-text">1 284 fichiers sur 1 790 — environ 2 minutes restantes</p>
        </div>
      </div>
      <div class="dz-in-retro-bar"><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i><i class="dz-in-seg"></i></div>
      <div class="dz-in-retro-fields">
        <div class="dz-in-retro-field"><span class="dz-in-retro-label">Destination</span><span class="dz-in-retro-input">Coffre-fort Nexora (chiffré)</span></div>
        <div class="dz-in-retro-field"><span class="dz-in-retro-label">Débit</span><span class="dz-in-retro-input">48,2 Mo/s</span></div>
      </div>
      <div class="dz-in-retro-actions">
        <a class="dz-in-retro-btn dz-in-retro-default" href="#">OK</a>
        <a class="dz-in-retro-btn" href="#">Annuler</a>
        <a class="dz-in-retro-btn" href="#">Détails &gt;&gt;</a>
      </div>
    </div>
    <div class="dz-in-retro-status"><span class="dz-in-retro-cell">Prêt</span><span class="dz-in-retro-cell">72 %</span><span class="dz-in-retro-cell">24/09/2026 18:42</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ carte d'embarquement
    dict(
        name="carte d'embarquement",
        icon="fas fa-plane-departure",
        html="""
<div class="dz-in-pass-wrap">
  <div class="dz-in-pass dz-reveal">
    <div class="dz-in-pass-main">
      <div class="dz-in-pass-head">
        <span class="dz-in-pass-brand"><i class="fas fa-plane"></i> Air Lune</span>
        <span class="dz-in-pass-kind">Carte d'embarquement · Économie Plus</span>
      </div>
      <div class="dz-in-pass-route">
        <div class="dz-in-pass-city">
          <span class="dz-in-pass-code">CDG</span>
          <span class="dz-in-pass-name">Paris Charles-de-Gaulle</span>
          <span class="dz-in-pass-time">08:45</span>
        </div>
        <div class="dz-in-pass-path">
          <span class="dz-in-pass-dur">5 h 40 · direct</span>
          <div class="dz-in-pass-line"><i class="fas fa-plane"></i></div>
          <span class="dz-in-pass-dur">Vol AL 718</span>
        </div>
        <div class="dz-in-pass-city dz-in-pass-to">
          <span class="dz-in-pass-code">DSS</span>
          <span class="dz-in-pass-name">Dakar Blaise-Diagne</span>
          <span class="dz-in-pass-time">13:25</span>
        </div>
      </div>
      <div class="dz-in-pass-grid">
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Passagère</span><span class="dz-in-pass-v">Camille Diallo</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Date</span><span class="dz-in-pass-v">Jeu. 12 mars 2026</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Porte</span><span class="dz-in-pass-v dz-in-pass-hl">K42</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Embarquement</span><span class="dz-in-pass-v">08:05</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Siège</span><span class="dz-in-pass-v dz-in-pass-hl">14A</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Groupe</span><span class="dz-in-pass-v">2</span></div>
      </div>
    </div>
    <div class="dz-in-pass-stub">
      <span class="dz-in-pass-k">Talon passager</span>
      <span class="dz-in-pass-mini">CDG <i class="fas fa-long-arrow-alt-right"></i> DSS</span>
      <div class="dz-in-pass-duo">
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Siège</span><span class="dz-in-pass-v">14A</span></div>
        <div class="dz-in-pass-cell"><span class="dz-in-pass-k">Porte</span><span class="dz-in-pass-v">K42</span></div>
      </div>
      <div class="dz-in-barcode"></div>
      <span class="dz-in-pass-ref">AL718 · 12MAR · 0048</span>
    </div>
  </div>
  <div class="dz-cluster dz-in-pass-actions">
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-wallet"></i> Ajouter au portefeuille</a>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-file-pdf"></i> Télécharger en PDF</a>
    <span class="dz-badge dz-badge-success"><span class="dz-dot"></span> À l'heure</span>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ ticket de concert
    dict(
        name="ticket de concert",
        icon="fas fa-ticket-alt",
        html="""
<div class="dz-in-gig-stage">
  <a class="dz-in-gig dz-reveal" href="#">
    <div class="dz-in-gig-main">
      <div class="dz-in-gig-top"><span class="dz-in-gig-tag">Tournée Marées 2026</span><span class="dz-in-gig-tag">Placement libre</span></div>
      <span class="dz-in-gig-artist">Orchestre Lunaire</span>
      <span class="dz-in-gig-sub">+ première partie : Les Saumâtres</span>
      <div class="dz-in-gig-meta">
        <div class="dz-in-gig-cell"><span class="dz-in-gig-k">Date</span><span class="dz-in-gig-v">Sam. 18 avril</span></div>
        <div class="dz-in-gig-cell"><span class="dz-in-gig-k">Portes</span><span class="dz-in-gig-v">19:30</span></div>
        <div class="dz-in-gig-cell"><span class="dz-in-gig-k">Salle</span><span class="dz-in-gig-v">Le Silo, Marseille</span></div>
      </div>
    </div>
    <div class="dz-in-gig-stub">
      <span class="dz-in-gig-admit">Entrée</span>
      <span class="dz-in-gig-price">39,00 €</span>
      <span class="dz-in-gig-num">N° 004 218</span>
      <div class="dz-in-barcode dz-in-barcode-v"></div>
    </div>
  </a>
  <p class="dz-in-gig-hint"><i class="fas fa-cut"></i> Détachez le talon : survolez le billet</p>
</div>
""",
    ),
    # ------------------------------------------------------------------ polaroids
    dict(
        name="polaroids épinglés",
        icon="fas fa-camera-retro",
        html="""
<div class="dz-section-head">
  <span class="dz-eyebrow">Coulisses</span>
  <h2 class="dz-h2">La vie de l'atelier, <em>en instantanés</em>.</h2>
</div>
<div class="dz-in-polas dz-reveal">
  <figure class="dz-in-pola dz-in-rot-1">
    <img src="https://picsum.photos/seed/atelier-seminaire/600/600" alt="Séminaire d'équipe au bord du lac">
    <figcaption class="dz-in-pola-cap">Séminaire à Annecy — juin 2026</figcaption>
  </figure>
  <figure class="dz-in-pola dz-in-rot-2 dz-in-tape">
    <img src="https://picsum.photos/seed/atelier-prototype/600/600" alt="Premier prototype sur l'établi">
    <figcaption class="dz-in-pola-cap">Le tout premier prototype ✦</figcaption>
  </figure>
  <figure class="dz-in-pola dz-in-rot-3">
    <img src="https://picsum.photos/seed/atelier-lancement/600/600" alt="Soirée de lancement">
    <figcaption class="dz-in-pola-cap">Lancement — 1 200 inscrits le 1er soir</figcaption>
  </figure>
  <figure class="dz-in-pola dz-in-rot-4 dz-in-tape">
    <img src="https://picsum.photos/seed/atelier-equipe/600/600" alt="L'équipe au complet">
    <figcaption class="dz-in-pola-cap">L'équipe au complet (enfin !)</figcaption>
  </figure>
</div>
""",
    ),
    # ------------------------------------------------------------------ post-it
    dict(
        name="mur de post-it",
        icon="fas fa-sticky-note",
        html="""
<div class="dz-in-wall">
  <div class="dz-in-wall-head">
    <div>
      <span class="dz-eyebrow">Rétrospective</span>
      <h2 class="dz-h3">Sprint 42 — du 7 au 18 septembre</h2>
    </div>
    <div class="dz-cluster">
      <div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">LM</span><span class="dz-avatar dz-avatar-sm">KB</span><span class="dz-avatar dz-avatar-sm">AN</span><span class="dz-avatar dz-avatar-sm">+4</span></div>
      <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-plus"></i> Ajouter une note</a>
    </div>
  </div>
  <div class="dz-in-wall-cols">
    <div class="dz-in-wall-col">
      <p class="dz-in-wall-title"><i class="fas fa-heart"></i> À garder <span class="dz-in-wall-count">3</span></p>
      <div class="dz-in-note dz-in-note-yellow dz-in-rot-1"><p class="dz-in-note-text">Les démos du vendredi : 15 min, pas plus. Tout le monde suit !</p><span class="dz-in-note-by">Léa · 👍 5</span></div>
      <div class="dz-in-note dz-in-note-green dz-in-rot-3"><p class="dz-in-note-text">Revue de code en binôme sur les tickets critiques.</p><span class="dz-in-note-by">Karim · 👍 3</span></div>
      <div class="dz-in-note dz-in-note-yellow dz-in-rot-2"><p class="dz-in-note-text">Le canal #entraide répond en moins d'une heure.</p><span class="dz-in-note-by">Awa · 👍 2</span></div>
    </div>
    <div class="dz-in-wall-col">
      <p class="dz-in-wall-title"><i class="fas fa-wrench"></i> À améliorer <span class="dz-in-wall-count">2</span></p>
      <div class="dz-in-note dz-in-note-pink dz-in-rot-2"><p class="dz-in-note-text">Trop de réunions le mardi : on bloque la matinée « focus ».</p><span class="dz-in-note-by">Hugo · 👍 6</span></div>
      <div class="dz-in-note dz-in-note-pink dz-in-rot-4"><p class="dz-in-note-text">Les tickets arrivent sans maquette : définir un « prêt à coder ».</p><span class="dz-in-note-by">Inès · 👍 4</span></div>
    </div>
    <div class="dz-in-wall-col">
      <p class="dz-in-wall-title"><i class="fas fa-flask"></i> À essayer <span class="dz-in-wall-count">2</span></p>
      <div class="dz-in-note dz-in-note-blue dz-in-rot-3"><p class="dz-in-note-text">Une journée sans e-mail par sprint. Rien que du chat.</p><span class="dz-in-note-by">Tom · 👍 2</span></div>
      <div class="dz-in-note dz-in-note-blue dz-in-rot-1"><p class="dz-in-note-text">Tableau des risques mis à jour chaque lundi en 5 min.</p><span class="dz-in-note-by">Léa · 👍 3</span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ platine vinyle
    dict(
        name="platine vinyle",
        icon="fas fa-record-vinyl",
        html="""
<div class="dz-in-deck">
  <div class="dz-in-plinth dz-reveal">
    <div class="dz-in-platter">
      <div class="dz-in-record"><div class="dz-in-label"><span class="dz-in-label-t">Face A</span><span class="dz-in-label-s">33 ⅓ tr/min</span></div></div>
      <div class="dz-in-sheen"></div>
    </div>
    <div class="dz-in-arm"><i class="dz-in-arm-head"></i></div>
    <div class="dz-in-deck-ctrl"><i class="dz-in-knob"></i><span class="dz-in-speed dz-in-speed-on">33</span><span class="dz-in-speed">45</span></div>
  </div>
  <div class="dz-in-now">
    <span class="dz-badge"><span class="dz-dot"></span> En écoute</span>
    <h2 class="dz-h2">Marées basses</h2>
    <p class="dz-in-now-artist">Orchestre Lunaire — album <em>Rivages</em> (2026)</p>
    <div class="dz-in-now-time"><span class="dz-mono">1:42</span><div class="dz-in-now-bar"><i class="dz-in-now-fill"></i></div><span class="dz-mono">4:08</span></div>
    <div class="dz-in-now-ctrls">
      <a class="dz-in-round" href="#" aria-label="Morceau précédent"><i class="fas fa-step-backward"></i></a>
      <a class="dz-in-round dz-in-round-main" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a>
      <a class="dz-in-round" href="#" aria-label="Morceau suivant"><i class="fas fa-step-forward"></i></a>
    </div>
    <div class="dz-in-tracks">
      <div class="dz-in-track"><span class="dz-in-track-n">A1</span><span class="dz-in-track-t">Rivages</span><span class="dz-in-track-d">3:52</span></div>
      <div class="dz-in-track dz-in-track-on"><span class="dz-in-track-n">A2</span><span class="dz-in-track-t">Marées basses</span><span class="dz-in-track-d">4:08</span></div>
      <div class="dz-in-track"><span class="dz-in-track-n">A3</span><span class="dz-in-track-t">Le phare de Kerlo</span><span class="dz-in-track-d">5:14</span></div>
      <div class="dz-in-track"><span class="dz-in-track-n">B1</span><span class="dz-in-track-t">Écume</span><span class="dz-in-track-d">3:27</span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ ticket de caisse
    dict(
        name="ticket de caisse",
        icon="fas fa-receipt",
        html="""
<div class="dz-split dz-in-receipt-split">
  <div>
    <span class="dz-eyebrow">Transparence</span>
    <h2 class="dz-h2">Chaque euro, <em>ligne par ligne</em>.</h2>
    <p class="dz-lead">Nos prix sont détaillés : produit, TVA, part reversée aux producteurs. Pas de frais cachés, jamais.</p>
    <ul class="dz-check-list">
      <li>Producteurs à moins de 150 km</li>
      <li>12 % du prix reversé à la coopérative</li>
      <li>Ticket dématérialisé envoyé par e-mail</li>
    </ul>
  </div>
  <div class="dz-in-receipt-stage">
    <div class="dz-in-receipt dz-reveal">
      <div class="dz-in-rc-head">
        <span class="dz-in-rc-shop">ÉPICERIE LUNE</span>
        <span class="dz-in-rc-small">12 rue des Tanneurs · 69001 Lyon</span>
        <span class="dz-in-rc-small">SIRET 912 384 552 00018</span>
      </div>
      <div class="dz-in-rc-meta"><span>24/09/2026 18:42</span><span>Caisse 03 · T.0482</span></div>
      <div class="dz-in-rc-rows">
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Pain de campagne 1 kg</span><span class="dz-in-rc-qty">1 ×</span><span class="dz-in-rc-price">5,80</span></div>
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Comté 18 mois</span><span class="dz-in-rc-qty">0,320 kg</span><span class="dz-in-rc-price">9,28</span></div>
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Pommes Chantecler</span><span class="dz-in-rc-qty">1,5 kg</span><span class="dz-in-rc-price">4,35</span></div>
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Jus de poire bio</span><span class="dz-in-rc-qty">2 ×</span><span class="dz-in-rc-price">7,00</span></div>
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Œufs plein air ×6</span><span class="dz-in-rc-qty">1 ×</span><span class="dz-in-rc-price">3,40</span></div>
        <div class="dz-in-rc-row dz-in-rc-promo"><span class="dz-in-rc-item">Remise fidélité −5 %</span><span class="dz-in-rc-qty"></span><span class="dz-in-rc-price">−1,49</span></div>
      </div>
      <div class="dz-in-rc-sum">
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Dont TVA 5,5 %</span><span class="dz-in-rc-qty"></span><span class="dz-in-rc-price">1,48</span></div>
        <div class="dz-in-rc-total"><span>TOTAL</span><span>28,34 €</span></div>
        <div class="dz-in-rc-row"><span class="dz-in-rc-item">Carte sans contact</span><span class="dz-in-rc-qty">•••• 4821</span><span class="dz-in-rc-price">28,34</span></div>
      </div>
      <div class="dz-in-barcode dz-in-barcode-rc"></div>
      <span class="dz-in-rc-thanks">★ Merci et à très bientôt ★</span>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ horloges
    dict(
        name="horloges du monde",
        icon="fas fa-clock",
        html="""
<div class="dz-section-head">
  <span class="dz-eyebrow">Équipe distribuée</span>
  <h2 class="dz-h2">Quatre bureaux, <em>un seul fuseau d'esprit</em>.</h2>
</div>
<div class="dz-in-clocks dz-stagger">
  <div class="dz-in-clock-card">
    <div class="dz-in-face">
      <span class="dz-in-num dz-in-n12">12</span><span class="dz-in-num dz-in-n3">3</span><span class="dz-in-num dz-in-n6">6</span><span class="dz-in-num dz-in-n9">9</span>
      <i class="dz-in-hand dz-in-hand-h" style="--a:305deg"></i><i class="dz-in-hand dz-in-hand-m" style="--a:60deg"></i><i class="dz-in-hand dz-in-hand-s" style="--a:180deg"></i><i class="dz-in-pivot"></i>
    </div>
    <div class="dz-in-clock-info"><span class="dz-in-clock-city">Paris</span><span class="dz-in-clock-meta">Siège · UTC+2</span></div>
    <span class="dz-in-clock-time">10:10</span>
  </div>
  <div class="dz-in-clock-card">
    <div class="dz-in-face">
      <span class="dz-in-num dz-in-n12">12</span><span class="dz-in-num dz-in-n3">3</span><span class="dz-in-num dz-in-n6">6</span><span class="dz-in-num dz-in-n9">9</span>
      <i class="dz-in-hand dz-in-hand-h" style="--a:245deg"></i><i class="dz-in-hand dz-in-hand-m" style="--a:60deg"></i><i class="dz-in-hand dz-in-hand-s" style="--a:180deg"></i><i class="dz-in-pivot"></i>
    </div>
    <div class="dz-in-clock-info"><span class="dz-in-clock-city">Dakar</span><span class="dz-in-clock-meta">Studio · UTC+0</span></div>
    <span class="dz-in-clock-time">08:10</span>
  </div>
  <div class="dz-in-clock-card dz-in-night">
    <div class="dz-in-face">
      <span class="dz-in-num dz-in-n12">12</span><span class="dz-in-num dz-in-n3">3</span><span class="dz-in-num dz-in-n6">6</span><span class="dz-in-num dz-in-n9">9</span>
      <i class="dz-in-hand dz-in-hand-h" style="--a:125deg"></i><i class="dz-in-hand dz-in-hand-m" style="--a:60deg"></i><i class="dz-in-hand dz-in-hand-s" style="--a:180deg"></i><i class="dz-in-pivot"></i>
    </div>
    <div class="dz-in-clock-info"><span class="dz-in-clock-city">Montréal</span><span class="dz-in-clock-meta">Support · UTC−4</span></div>
    <span class="dz-in-clock-time">04:10</span>
  </div>
  <div class="dz-in-clock-card dz-in-night">
    <div class="dz-in-face">
      <span class="dz-in-num dz-in-n12">12</span><span class="dz-in-num dz-in-n3">3</span><span class="dz-in-num dz-in-n6">6</span><span class="dz-in-num dz-in-n9">9</span>
      <i class="dz-in-hand dz-in-hand-h" style="--a:155deg"></i><i class="dz-in-hand dz-in-hand-m" style="--a:60deg"></i><i class="dz-in-hand dz-in-hand-s" style="--a:180deg"></i><i class="dz-in-pivot"></i>
    </div>
    <div class="dz-in-clock-info"><span class="dz-in-clock-city">Tokyo</span><span class="dz-in-clock-meta">R&amp;D · UTC+9</span></div>
    <span class="dz-in-clock-time">17:10</span>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ météo
    dict(
        name="widget météo",
        icon="fas fa-cloud-sun",
        html="""
<div class="dz-in-meteo">
  <div class="dz-in-sky dz-reveal">
    <div class="dz-in-sky-top">
      <div>
        <span class="dz-in-sky-place"><i class="fas fa-map-marker-alt"></i> Lyon, Croix-Rousse</span>
        <span class="dz-in-sky-date">Jeudi 24 septembre · 14:00</span>
      </div>
      <span class="dz-in-sky-live">Actualisé il y a 4 min</span>
    </div>
    <div class="dz-in-sky-now">
      <div class="dz-in-sun-art"><i class="dz-in-sun"></i><i class="fas fa-cloud dz-in-cloud"></i><i class="fas fa-cloud dz-in-cloud-2"></i></div>
      <div>
        <span class="dz-in-temp">21°</span>
        <span class="dz-in-sky-desc">Éclaircies · ressenti 19°</span>
        <span class="dz-in-sky-range">Max 23° · Min 12°</span>
      </div>
    </div>
    <div class="dz-in-sky-stats">
      <div class="dz-in-stat"><i class="fas fa-wind"></i><span class="dz-in-stat-v">14 km/h</span><span class="dz-in-stat-k">Vent NO</span></div>
      <div class="dz-in-stat"><i class="fas fa-tint"></i><span class="dz-in-stat-v">62 %</span><span class="dz-in-stat-k">Humidité</span></div>
      <div class="dz-in-stat"><i class="fas fa-umbrella"></i><span class="dz-in-stat-v">10 %</span><span class="dz-in-stat-k">Pluie</span></div>
      <div class="dz-in-stat"><i class="fas fa-sun"></i><span class="dz-in-stat-v">UV 4</span><span class="dz-in-stat-k">Modéré</span></div>
    </div>
    <div class="dz-in-hours">
      <div class="dz-in-hour dz-in-hour-now"><span class="dz-in-hour-t">Maint.</span><i class="fas fa-cloud-sun"></i><span class="dz-in-hour-v">21°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">15 h</span><i class="fas fa-sun"></i><span class="dz-in-hour-v">22°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">16 h</span><i class="fas fa-sun"></i><span class="dz-in-hour-v">23°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">17 h</span><i class="fas fa-cloud-sun"></i><span class="dz-in-hour-v">22°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">18 h</span><i class="fas fa-cloud"></i><span class="dz-in-hour-v">20°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">19 h</span><i class="fas fa-cloud-rain"></i><span class="dz-in-hour-v">18°</span></div>
      <div class="dz-in-hour"><span class="dz-in-hour-t">20 h</span><i class="fas fa-cloud-moon"></i><span class="dz-in-hour-v">16°</span></div>
    </div>
  </div>
  <div class="dz-in-week">
    <p class="dz-in-week-title">Prévisions sur 7 jours</p>
    <div class="dz-in-day"><span class="dz-in-day-n">Aujourd'hui</span><i class="fas fa-cloud-sun"></i><span class="dz-in-day-lo">12°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:10%;--w:55%"></i></div><span class="dz-in-day-hi">23°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Ven.</span><i class="fas fa-sun"></i><span class="dz-in-day-lo">13°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:15%;--w:65%"></i></div><span class="dz-in-day-hi">25°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Sam.</span><i class="fas fa-sun"></i><span class="dz-in-day-lo">15°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:25%;--w:70%"></i></div><span class="dz-in-day-hi">27°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Dim.</span><i class="fas fa-cloud-showers-heavy"></i><span class="dz-in-day-lo">11°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:5%;--w:40%"></i></div><span class="dz-in-day-hi">19°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Lun.</span><i class="fas fa-cloud-rain"></i><span class="dz-in-day-lo">10°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:0%;--w:40%"></i></div><span class="dz-in-day-hi">18°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Mar.</span><i class="fas fa-cloud"></i><span class="dz-in-day-lo">11°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:5%;--w:45%"></i></div><span class="dz-in-day-hi">20°</span></div>
    <div class="dz-in-day"><span class="dz-in-day-n">Mer.</span><i class="fas fa-cloud-sun"></i><span class="dz-in-day-lo">12°</span><div class="dz-in-range"><i class="dz-in-range-fill" style="--l:10%;--w:52%"></i></div><span class="dz-in-day-hi">22°</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ cartes à retourner
    dict(
        name="cartes à retourner",
        icon="fas fa-sync-alt",
        html="""
<div class="dz-section-head">
  <span class="dz-eyebrow">Nos engagements</span>
  <h2 class="dz-h2">Retournez les cartes.</h2>
  <p class="dz-lead">Survolez (ou touchez) chaque carte pour découvrir ce qu'il y a derrière nos promesses.</p>
</div>
<div class="dz-in-flips">
  <div class="dz-in-flip">
    <div class="dz-in-flip-inner">
      <div class="dz-in-flip-face dz-in-flip-front">
        <span class="dz-icon dz-icon-lg"><i class="fas fa-bolt"></i></span>
        <span class="dz-in-flip-kicker">01</span>
        <h3 class="dz-h3">Réponse en 2 h</h3>
        <span class="dz-in-flip-hint"><i class="fas fa-sync-alt"></i> Retourner</span>
      </div>
      <div class="dz-in-flip-face dz-in-flip-back">
        <span class="dz-in-flip-big">1 h 12</span>
        <p class="dz-in-flip-text">Délai moyen de première réponse en 2026, week-ends compris. Une vraie personne, jamais un robot.</p>
        <a class="dz-btn dz-btn-sm dz-btn-light" href="#">Écrire au support</a>
      </div>
    </div>
  </div>
  <div class="dz-in-flip">
    <div class="dz-in-flip-inner">
      <div class="dz-in-flip-face dz-in-flip-front">
        <span class="dz-icon dz-icon-lg"><i class="fas fa-leaf"></i></span>
        <span class="dz-in-flip-kicker">02</span>
        <h3 class="dz-h3">Hébergement sobre</h3>
        <span class="dz-in-flip-hint"><i class="fas fa-sync-alt"></i> Retourner</span>
      </div>
      <div class="dz-in-flip-face dz-in-flip-back">
        <span class="dz-in-flip-big">−38 %</span>
        <p class="dz-in-flip-text">d'énergie consommée depuis 2024 grâce à nos serveurs mutualisés en France, alimentés en énergie renouvelable.</p>
        <a class="dz-btn dz-btn-sm dz-btn-light" href="#">Voir le rapport</a>
      </div>
    </div>
  </div>
  <div class="dz-in-flip">
    <div class="dz-in-flip-inner">
      <div class="dz-in-flip-face dz-in-flip-front">
        <span class="dz-icon dz-icon-lg"><i class="fas fa-lock"></i></span>
        <span class="dz-in-flip-kicker">03</span>
        <h3 class="dz-h3">Vos données, chez vous</h3>
        <span class="dz-in-flip-hint"><i class="fas fa-sync-alt"></i> Retourner</span>
      </div>
      <div class="dz-in-flip-face dz-in-flip-back">
        <span class="dz-in-flip-big">100 %</span>
        <p class="dz-in-flip-text">des données chiffrées et exportables à tout moment, en un clic, dans un format ouvert.</p>
        <a class="dz-btn dz-btn-sm dz-btn-light" href="#">Notre charte</a>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ lettre
    dict(
        name="lettre à la machine",
        icon="fas fa-envelope-open-text",
        wrap="narrow",
        html="""
<div class="dz-in-airmail dz-reveal">
  <div class="dz-in-letter">
    <div class="dz-in-letter-top">
      <div class="dz-in-letter-from">
        <span class="dz-in-letter-strong">Atelier Lune</span>
        <span>4 place Sathonay</span>
        <span>69001 Lyon</span>
      </div>
      <div class="dz-in-stamp-zone">
        <div class="dz-in-postmark"><span class="dz-in-postmark-t">LYON</span><span class="dz-in-postmark-d">24·09·26</span></div>
        <div class="dz-in-stamp"><div class="dz-in-stamp-art"><i class="fas fa-feather-alt"></i><span class="dz-in-stamp-val">1,29 €</span></div></div>
      </div>
    </div>
    <span class="dz-in-airmail-tag">Par avion · Lettre prioritaire</span>
    <p class="dz-in-letter-date">Lyon, le 24 septembre 2026</p>
    <p class="dz-in-letter-p">Chère Inès,</p>
    <p class="dz-in-letter-p">Il y a dix ans, nous ouvrions l'atelier avec deux établis, une machine à écrire et beaucoup trop de café. Aujourd'hui, vous êtes 4 812 à nous faire confiance.</p>
    <p class="dz-in-letter-p">Pour fêter ça, nous vous invitons le <b>samedi 17 octobre</b> à partir de 18 h : visite des coulisses, démonstrations et petit concert dans la cour.</p>
    <p class="dz-in-letter-p dz-in-letter-close dz-typewriter">Avec toute notre gratitude, | À très vite dans la cour, | Bien fidèlement,</p>
    <p class="dz-in-letter-sign">Marion &amp; toute l'équipe</p>
    <div class="dz-cluster dz-in-letter-cta">
      <a class="dz-btn" href="#"><i class="fas fa-reply"></i> Répondre à l'invitation</a>
      <span class="dz-small">Réponse souhaitée avant le 10 octobre</span>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ carte au trésor
    dict(
        name="plan avec épingles",
        icon="fas fa-map-marked-alt",
        html="""
<div class="dz-in-mapbox">
  <div class="dz-in-map dz-reveal">
    <svg class="dz-in-map-svg" viewBox="0 0 800 500" preserveAspectRatio="none" aria-hidden="true"><path class="dz-in-river" d="M-10 380C120 330 180 420 300 360S470 220 560 250 700 330 820 260"/><path class="dz-in-route" d="M150 150C230 120 300 190 330 250S470 330 520 290 610 140 660 120"/></svg>
    <div class="dz-in-park dz-in-park-1"></div>
    <div class="dz-in-park dz-in-park-2"></div>
    <div class="dz-in-compass"><span class="dz-in-compass-n">N</span></div>
    <div class="dz-in-pin-spot dz-in-spot-1"><span class="dz-in-pin">1</span><span class="dz-in-pin-label">Départ · Place des Terreaux</span></div>
    <div class="dz-in-pin-spot dz-in-spot-2"><span class="dz-in-pin">2</span><span class="dz-in-pin-label">Atelier céramique</span></div>
    <div class="dz-in-pin-spot dz-in-spot-3"><span class="dz-in-pin">3</span><span class="dz-in-pin-label">Halle aux créateurs</span></div>
    <div class="dz-in-pin-spot dz-in-spot-4 dz-in-pin-x"><span class="dz-in-pin"><i class="fas fa-times"></i></span><span class="dz-in-pin-label">Soirée de clôture · 20 h</span></div>
    <span class="dz-in-map-scale">500 m</span>
  </div>
  <div class="dz-in-legend">
    <span class="dz-eyebrow">Parcours du festival</span>
    <h2 class="dz-h3">4 étapes, 2,8 km, <em>un trésor</em> à l'arrivée.</h2>
    <div class="dz-in-leg">
      <div class="dz-in-leg-item"><span class="dz-in-leg-n">1</span><div><p class="dz-in-leg-t">Place des Terreaux</p><p class="dz-in-leg-s">Retrait du carnet de route · 14:00</p></div></div>
      <div class="dz-in-leg-item"><span class="dz-in-leg-n">2</span><div><p class="dz-in-leg-t">Atelier céramique</p><p class="dz-in-leg-s">Démonstration de tournage · 15:30</p></div></div>
      <div class="dz-in-leg-item"><span class="dz-in-leg-n">3</span><div><p class="dz-in-leg-t">Halle aux créateurs</p><p class="dz-in-leg-s">42 exposants · goûter offert</p></div></div>
      <div class="dz-in-leg-item dz-in-leg-x"><span class="dz-in-leg-n"><i class="fas fa-times"></i></span><div><p class="dz-in-leg-t">Jardin des Chartreux</p><p class="dz-in-leg-s">Concert et tirage au sort · 20:00</p></div></div>
    </div>
    <a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-route"></i> Ouvrir l'itinéraire</a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ cartes à collectionner
    dict(
        name="cartes à collectionner",
        icon="fas fa-id-card-alt",
        html="""
<div class="dz-section-head">
  <span class="dz-eyebrow">L'équipe · Saison 2026</span>
  <h2 class="dz-h2">Collectionnez-les <em>toutes</em>.</h2>
</div>
<div class="dz-in-tcgs">
  <div class="dz-in-tcg dz-in-tcg-rare">
    <div class="dz-in-tcg-frame">
      <div class="dz-in-tcg-head"><span class="dz-in-tcg-name">Léa Moreau</span><span class="dz-in-tcg-hp">XP 12</span></div>
      <div class="dz-in-tcg-art"><span class="dz-avatar dz-avatar-lg">LM</span><span class="dz-in-tcg-type"><i class="fas fa-pen-nib"></i></span></div>
      <span class="dz-in-tcg-line">Designer produit · Rare</span>
      <div class="dz-in-tcg-move"><p class="dz-in-tcg-mt"><span class="dz-in-tcg-cost">●●</span> Prototype éclair <span class="dz-in-tcg-dmg">80</span></p><p class="dz-in-tcg-md">Transforme une idée floue en maquette cliquable en 48 h.</p></div>
      <div class="dz-in-tcg-stats"><span class="dz-in-tcg-stat">Créa <b>92</b></span><span class="dz-in-tcg-stat">Vitesse <b>78</b></span><span class="dz-in-tcg-stat">Café <b>99</b></span></div>
      <div class="dz-in-tcg-foot"><span>N° 012/150</span><span>★★★</span></div>
    </div>
  </div>
  <div class="dz-in-tcg dz-in-tcg-epic">
    <div class="dz-in-tcg-frame">
      <div class="dz-in-tcg-head"><span class="dz-in-tcg-name">Karim Benali</span><span class="dz-in-tcg-hp">XP 15</span></div>
      <div class="dz-in-tcg-art"><span class="dz-avatar dz-avatar-lg">KB</span><span class="dz-in-tcg-type"><i class="fas fa-code"></i></span></div>
      <span class="dz-in-tcg-line">Développeur back-end · Épique</span>
      <div class="dz-in-tcg-move"><p class="dz-in-tcg-mt"><span class="dz-in-tcg-cost">●●●</span> Refonte silencieuse <span class="dz-in-tcg-dmg">120</span></p><p class="dz-in-tcg-md">Divise le temps de réponse de l'API par 3 sans casser un seul test.</p></div>
      <div class="dz-in-tcg-stats"><span class="dz-in-tcg-stat">Logique <b>97</b></span><span class="dz-in-tcg-stat">Calme <b>88</b></span><span class="dz-in-tcg-stat">Jeux de mots <b>64</b></span></div>
      <div class="dz-in-tcg-foot"><span>N° 027/150</span><span>★★★★</span></div>
    </div>
  </div>
  <div class="dz-in-tcg dz-in-tcg-legend">
    <div class="dz-in-tcg-frame">
      <div class="dz-in-tcg-head"><span class="dz-in-tcg-name">Awa Ndiaye</span><span class="dz-in-tcg-hp">XP 18</span></div>
      <div class="dz-in-tcg-art"><span class="dz-avatar dz-avatar-lg">AN</span><span class="dz-in-tcg-type"><i class="fas fa-crown"></i></span></div>
      <span class="dz-in-tcg-line">Directrice des opérations · Légendaire</span>
      <div class="dz-in-tcg-move"><p class="dz-in-tcg-mt"><span class="dz-in-tcg-cost">●●●●</span> Planning parfait <span class="dz-in-tcg-dmg">180</span></p><p class="dz-in-tcg-md">Toute l'équipe gagne +1 jour de marge sur chaque livraison.</p></div>
      <div class="dz-in-tcg-stats"><span class="dz-in-tcg-stat">Vision <b>99</b></span><span class="dz-in-tcg-stat">Sang-froid <b>95</b></span><span class="dz-in-tcg-stat">Humour <b>90</b></span></div>
      <div class="dz-in-tcg-foot"><span>N° 001/150</span><span>★★★★★</span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ tableau périodique
    dict(
        name="tableau périodique d'équipe",
        icon="fas fa-atom",
        html="""
<div class="dz-in-pt-head">
  <div>
    <span class="dz-eyebrow">Qui fait quoi</span>
    <h2 class="dz-h2">Les éléments <em>de l'équipe</em>.</h2>
  </div>
  <div class="dz-in-pt-legend">
    <span class="dz-in-pt-key dz-in-cat-design">Design</span>
    <span class="dz-in-pt-key dz-in-cat-dev">Développement</span>
    <span class="dz-in-pt-key dz-in-cat-data">Données</span>
    <span class="dz-in-pt-key dz-in-cat-ops">Opérations</span>
    <span class="dz-in-pt-key dz-in-cat-sales">Commercial</span>
  </div>
</div>
<div class="dz-in-pt dz-reveal">
  <div class="dz-in-el dz-in-cat-ops"><span class="dz-in-el-z">1</span><span class="dz-in-el-m">2016</span><span class="dz-in-el-sym">An</span><span class="dz-in-el-name">Awa Ndiaye</span><span class="dz-in-el-role">Direction</span></div>
  <div class="dz-in-el dz-in-cat-design"><span class="dz-in-el-z">2</span><span class="dz-in-el-m">2018</span><span class="dz-in-el-sym">Lm</span><span class="dz-in-el-name">Léa Moreau</span><span class="dz-in-el-role">Design produit</span></div>
  <div class="dz-in-el dz-in-cat-dev"><span class="dz-in-el-z">3</span><span class="dz-in-el-m">2019</span><span class="dz-in-el-sym">Kb</span><span class="dz-in-el-name">Karim Benali</span><span class="dz-in-el-role">Back-end</span></div>
  <div class="dz-in-el dz-in-cat-dev"><span class="dz-in-el-z">4</span><span class="dz-in-el-m">2020</span><span class="dz-in-el-sym">Hr</span><span class="dz-in-el-name">Hugo Roux</span><span class="dz-in-el-role">Front-end</span></div>
  <div class="dz-in-el dz-in-cat-data"><span class="dz-in-el-z">5</span><span class="dz-in-el-m">2020</span><span class="dz-in-el-sym">Ip</span><span class="dz-in-el-name">Inès Petit</span><span class="dz-in-el-role">Analyse de données</span></div>
  <div class="dz-in-el dz-in-cat-sales"><span class="dz-in-el-z">6</span><span class="dz-in-el-m">2021</span><span class="dz-in-el-sym">Tg</span><span class="dz-in-el-name">Tom Garnier</span><span class="dz-in-el-role">Ventes</span></div>
  <div class="dz-in-el dz-in-cat-design"><span class="dz-in-el-z">7</span><span class="dz-in-el-m">2021</span><span class="dz-in-el-sym">Sf</span><span class="dz-in-el-name">Sarah Fontaine</span><span class="dz-in-el-role">Illustration</span></div>
  <div class="dz-in-el dz-in-cat-ops"><span class="dz-in-el-z">8</span><span class="dz-in-el-m">2022</span><span class="dz-in-el-sym">Md</span><span class="dz-in-el-name">Moussa Diop</span><span class="dz-in-el-role">Support client</span></div>
  <div class="dz-in-el dz-in-cat-dev"><span class="dz-in-el-z">9</span><span class="dz-in-el-m">2023</span><span class="dz-in-el-sym">Cl</span><span class="dz-in-el-name">Chloé Lambert</span><span class="dz-in-el-role">Mobile</span></div>
  <div class="dz-in-el dz-in-cat-data"><span class="dz-in-el-z">10</span><span class="dz-in-el-m">2024</span><span class="dz-in-el-sym">Nv</span><span class="dz-in-el-name">Nathan Vidal</span><span class="dz-in-el-role">IA &amp; modèles</span></div>
  <div class="dz-in-el dz-in-cat-sales"><span class="dz-in-el-z">11</span><span class="dz-in-el-m">2025</span><span class="dz-in-el-sym">Eb</span><span class="dz-in-el-name">Emma Blanc</span><span class="dz-in-el-role">Partenariats</span></div>
  <a class="dz-in-el dz-in-el-new" href="#"><span class="dz-in-el-z">12</span><span class="dz-in-el-m">2026</span><span class="dz-in-el-sym">?</span><span class="dz-in-el-name">Vous ?</span><span class="dz-in-el-role">3 postes ouverts</span></a>
</div>
""",
    ),
    # ------------------------------------------------------------------ écran de chargement
    dict(
        name="écran de chargement",
        icon="fas fa-spinner",
        wrap="narrow",
        html="""
<div class="dz-in-load dz-reveal">
  <div class="dz-in-orbit"><i class="dz-in-orbit-core"></i><i class="dz-in-orbit-ring"></i><i class="dz-in-orbit-dot dz-in-od-1"></i><i class="dz-in-orbit-dot dz-in-od-2"></i><i class="dz-in-orbit-dot dz-in-od-3"></i></div>
  <h2 class="dz-h3">Préparation de votre espace…</h2>
  <p class="dz-in-load-tip"><span class="dz-in-load-k">Astuce</span><span class="dz-typewriter">Appuyez sur Ctrl K pour tout retrouver. | Glissez un fichier n'importe où pour l'importer. | Tapez « / » dans un texte pour insérer un bloc.</span></p>
  <div class="dz-in-load-bar"><div class="dz-progress dz-progress-68"><span></span></div><span class="dz-in-load-pct">68 %</span></div>
  <div class="dz-in-load-steps">
    <div class="dz-in-load-step dz-in-done"><span class="dz-in-load-ic"><i class="fas fa-check"></i></span><span class="dz-in-load-t">Création de l'espace « Atelier Lune »</span><span class="dz-in-load-d">0,8 s</span></div>
    <div class="dz-in-load-step dz-in-done"><span class="dz-in-load-ic"><i class="fas fa-check"></i></span><span class="dz-in-load-t">Import de 1 284 contacts</span><span class="dz-in-load-d">3,1 s</span></div>
    <div class="dz-in-load-step dz-in-doing"><span class="dz-in-load-ic"><i class="dz-in-spin"></i></span><span class="dz-in-load-t">Construction des tableaux de bord</span><span class="dz-in-load-d">en cours</span></div>
    <div class="dz-in-load-step"><span class="dz-in-load-ic"><i class="fas fa-circle"></i></span><span class="dz-in-load-t">Invitation de l'équipe (6 personnes)</span><span class="dz-in-load-d">—</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ badge de conférence
    dict(
        name="badge de conférence",
        icon="fas fa-id-badge",
        html="""
<div class="dz-in-conf">
  <div class="dz-in-lanyard">
    <div class="dz-in-strap"><span class="dz-in-strap-t">SOMMET NEXORA · 2026 · SOMMET NEXORA · 2026</span></div>
    <div class="dz-in-clip"></div>
    <div class="dz-in-badge">
      <i class="dz-in-badge-hole"></i>
      <div class="dz-in-badge-top"><span class="dz-in-badge-ev">Sommet Nexora 2026</span><span class="dz-in-badge-where">Lyon · 14–15 octobre</span></div>
      <div class="dz-in-badge-body">
        <span class="dz-avatar dz-avatar-lg">AN</span>
        <span class="dz-in-badge-name">Awa Ndiaye</span>
        <span class="dz-in-badge-role">Directrice des opérations</span>
        <span class="dz-in-badge-org">Atelier Lune</span>
      </div>
      <div class="dz-in-badge-foot">
        <span class="dz-in-badge-type">Intervenante</span>
        QRCODE
      </div>
    </div>
  </div>
  <div class="dz-in-conf-info">
    <span class="dz-eyebrow">Votre badge est prêt</span>
    <h2 class="dz-h2">À très vite <em>à Lyon</em>, Awa.</h2>
    <p class="dz-lead">Présentez ce badge à l'accueil ou scannez-le depuis votre téléphone. Il donne accès à toutes les salles et au dîner des intervenants.</p>
    <div class="dz-in-conf-list">
      <div class="dz-in-conf-row"><i class="fas fa-map-marker-alt"></i><div><p class="dz-in-conf-t">Halle Tony-Garnier</p><p class="dz-in-conf-s">20 place Docteurs-Mérieux, Lyon 7e</p></div></div>
      <div class="dz-in-conf-row"><i class="fas fa-microphone"></i><div><p class="dz-in-conf-t">Votre intervention · Salle B</p><p class="dz-in-conf-s">Mercredi 14 octobre, 14:00 – 14:45</p></div></div>
      <div class="dz-in-conf-row dz-copy-scope"><i class="fas fa-wifi"></i><div><p class="dz-in-conf-t">Wi-Fi « Sommet-Invites »</p><p class="dz-in-conf-s">Mot de passe : <code class="dz-in-conf-code">lune-2026</code></p></div><a class="dz-in-conf-copy dz-copy" href="#" aria-label="Copier le mot de passe"><i class="far fa-copy"></i></a></div>
    </div>
    <div class="dz-cluster">
      <a class="dz-btn" href="#"><i class="fas fa-wallet"></i> Ajouter au portefeuille</a>
      <a class="dz-btn dz-btn-ghost" href="#"><i class="far fa-calendar-plus"></i> Agenda</a>
    </div>
  </div>
</div>
""".replace("QRCODE", _qr("badge-awa")),
    ),
    # ------------------------------------------------------------------ carte de visite
    dict(
        name="carte de visite",
        icon="fas fa-address-card",
        html="""
<div class="dz-in-bc-stage">
  <div class="dz-in-bc">
    <div class="dz-in-bc-inner">
      <div class="dz-in-bc-face dz-in-bc-front">
        <div class="dz-in-bc-logo"><i class="dz-in-bc-mark"></i><span class="dz-in-bc-brand">Atelier Lune</span></div>
        <div class="dz-in-bc-id"><span class="dz-in-bc-name">Marion Leclerc</span><span class="dz-in-bc-role">Fondatrice &amp; céramiste</span></div>
        <span class="dz-in-bc-turn"><i class="fas fa-sync-alt"></i> Survoler pour retourner</span>
      </div>
      <div class="dz-in-bc-face dz-in-bc-back">
        <div class="dz-in-bc-lines">
          <p class="dz-in-bc-line"><i class="fas fa-phone"></i> 06 12 48 30 77</p>
          <p class="dz-in-bc-line"><i class="fas fa-envelope"></i> marion@atelier-lune.fr</p>
          <p class="dz-in-bc-line"><i class="fas fa-globe"></i> atelier-lune.fr</p>
          <p class="dz-in-bc-line"><i class="fas fa-map-marker-alt"></i> 4 place Sathonay, 69001 Lyon</p>
        </div>
        QRCODE
      </div>
    </div>
  </div>
  <div class="dz-cluster dz-in-bc-actions">
    <a class="dz-btn" href="#"><i class="fas fa-user-plus"></i> Enregistrer le contact</a>
    <a class="dz-btn dz-btn-ghost" href="#"><i class="fas fa-share-alt"></i> Partager</a>
  </div>
</div>
""".replace("QRCODE", _qr("carte-marion", 21)),
    ),
    # ------------------------------------------------------------------ calendrier de l'avent
    dict(
        name="calendrier de l'avent",
        icon="fas fa-gifts",
        html="""
<div class="dz-in-advent-head">
  <div>
    <span class="dz-eyebrow">Décembre 2026</span>
    <h2 class="dz-h2">Une surprise <em>par jour</em>.</h2>
    <p class="dz-lead">Chaque matin, une nouvelle case s'ouvre : remises, ateliers, cadeaux. Survolez une case pour jeter un œil…</p>
  </div>
  <div class="dz-in-advent-count"><span class="dz-in-advent-big">8</span><span class="dz-small">cases ouvertes sur 24</span></div>
</div>
<div class="dz-in-advent">ADVENT
</div>
""".replace("ADVENT", _advent()),
    ),
    # ------------------------------------------------------------------ cartouche / fidélité
    dict(
        name="cartouche de jeu",
        icon="fas fa-gamepad",
        html="""
<div class="dz-in-cart-split">
  <div class="dz-in-cart dz-reveal">
    <div class="dz-in-cart-ridges"></div>
    <div class="dz-in-cart-label">
      <div class="dz-in-cart-art"><span class="dz-in-cart-lvl">Niv. 3</span><i class="fas fa-dragon dz-in-cart-hero"></i><span class="dz-in-cart-stars">✦ ✧ ✦</span></div>
      <div class="dz-in-cart-title"><span class="dz-in-cart-name">La Quête du Client Fidèle</span><span class="dz-in-cart-ed">Édition 2026 · 1 joueur</span></div>
    </div>
    <div class="dz-in-cart-notch"></div>
  </div>
  <div class="dz-in-quest">
    <span class="dz-eyebrow">Programme de fidélité</span>
    <h2 class="dz-h2">Niveau 3 <em>débloqué</em> !</h2>
    <p class="dz-lead">Encore 260 points pour atteindre le niveau 4 et gagner la livraison offerte à vie.</p>
    <div class="dz-in-xp"><div class="dz-in-xp-top"><span class="dz-in-xp-k">XP</span><span class="dz-mono">740 / 1 000</span></div><div class="dz-in-xp-bar"><i class="dz-in-xp-fill"></i></div></div>
    <div class="dz-in-achv">
      <div class="dz-in-ach dz-in-ach-on"><i class="fas fa-shopping-basket"></i><span class="dz-in-ach-t">Premier panier</span></div>
      <div class="dz-in-ach dz-in-ach-on"><i class="fas fa-star"></i><span class="dz-in-ach-t">5 avis laissés</span></div>
      <div class="dz-in-ach dz-in-ach-on"><i class="fas fa-user-friends"></i><span class="dz-in-ach-t">Parrain</span></div>
      <div class="dz-in-ach"><i class="fas fa-lock"></i><span class="dz-in-ach-t">Livraison à vie</span></div>
    </div>
    <a class="dz-btn" href="#"><i class="fas fa-play"></i> Continuer la partie</a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 404
    dict(
        name="page 404 en orbite",
        icon="fas fa-user-astronaut",
        wrap="full",
        html="""
<div class="dz-in-404">
  <div class="dz-in-stars"></div>
  <div class="dz-container dz-in-404-inner">
    <div class="dz-in-404-digits" aria-label="Erreur 404">
      <span class="dz-in-404-d">4</span>
      <div class="dz-in-planet"><i class="dz-in-planet-ring"></i><i class="dz-in-moon-track"></i></div>
      <span class="dz-in-404-d">4</span>
    </div>
    <i class="fas fa-user-astronaut dz-in-astro"></i>
    <h1 class="dz-h2">Cette page s'est perdue <em>en orbite</em>.</h1>
    <p class="dz-lead">Le lien est peut-être ancien, ou la page a changé d'adresse. Pas de panique : le contrôle de mission vous ramène sur Terre.</p>
    <div class="dz-cluster">
      <a class="dz-btn" href="/"><i class="fas fa-home"></i> Retour à l'accueil</a>
      <a class="dz-btn dz-btn-ghost" href="#"><i class="fas fa-life-ring"></i> Contacter le support</a>
    </div>
    <div class="dz-in-404-links">
      <a class="dz-in-404-link" href="#"><i class="fas fa-book-open"></i><span class="dz-in-404-lt">Documentation</span><i class="fas fa-arrow-right dz-in-404-go"></i></a>
      <a class="dz-in-404-link" href="#"><i class="fas fa-tags"></i><span class="dz-in-404-lt">Tarifs</span><i class="fas fa-arrow-right dz-in-404-go"></i></a>
      <a class="dz-in-404-link" href="#"><i class="fas fa-newspaper"></i><span class="dz-in-404-lt">Blog</span><i class="fas fa-arrow-right dz-in-404-go"></i></a>
    </div>
    <span class="dz-in-404-code">Code : ERR_PAGE_EN_ORBITE · réf. 7F3A-2026</span>
  </div>
</div>
""",
    ),
]
