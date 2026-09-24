"""Famille « Finance » : comptes, cartes, transactions, budgets, investissements,
trésorerie d'entreprise.  Préfixe CSS : dz-fi-  (styles/34-finance.css)"""

FAMILY = "finance"


def cat(icon, tone):
    return f'<span class="dz-fi-cat dz-fi-tone-{tone}"><i class="fas fa-{icon}"></i></span>'


BALANCE = """
<div class="dz-fi-balance">
  <div class="dz-fi-balance-top">
    <div class="dz-fi-acc-switch"><span class="dz-fi-flag">€</span><div><b>Compte courant</b><span class="dz-mono">FR76 •••• 4821</span></div><i class="fas fa-chevron-down"></i></div>
    <div class="dz-fi-balance-tools"><a class="dz-fi-iconbtn" href="#" aria-label="Masquer les montants"><i class="far fa-eye"></i></a><a class="dz-fi-iconbtn" href="#" aria-label="Notifications"><i class="far fa-bell"></i></a></div>
  </div>
  <div class="dz-fi-balance-main">
    <span class="dz-fi-label">Solde disponible</span>
    <div class="dz-fi-amount"><b class="dz-counter">12 486,30</b><span>€</span></div>
    <div class="dz-fi-balance-delta"><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 1 240,80 €</span><span class="dz-fi-muted">depuis le 1er septembre · +11,0 %</span></div>
  </div>
  <div class="dz-fi-area">
    <svg viewBox="0 0 400 110" preserveAspectRatio="none"><defs><linearGradient id="dz-fi-g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="dz-fi-stop-a"/><stop offset="1" class="dz-fi-stop-b"/></linearGradient></defs><path class="dz-fi-area-fill" fill="url(#dz-fi-g1)" d="M0,80 C30,74 50,86 80,70 S130,60 160,64 S210,40 240,48 S290,30 320,34 S370,14 400,12 L400,110 L0,110Z"/><path class="dz-fi-area-line" d="M0,80 C30,74 50,86 80,70 S130,60 160,64 S210,40 240,48 S290,30 320,34 S370,14 400,12"/><circle class="dz-fi-area-dot" cx="400" cy="12" r="4"/></svg>
    <div class="dz-fi-area-axis"><span>1 sept.</span><span>8</span><span>15</span><span>22</span><span>Auj.</span></div>
  </div>
  <div class="dz-fi-actions">
    <a class="dz-fi-action" href="#"><i class="fas fa-paper-plane"></i><span>Envoyer</span></a>
    <a class="dz-fi-action" href="#"><i class="fas fa-arrow-down"></i><span>Recevoir</span></a>
    <a class="dz-fi-action" href="#"><i class="fas fa-plus"></i><span>Alimenter</span></a>
    <a class="dz-fi-action" href="#"><i class="fas fa-exchange-alt"></i><span>Changer</span></a>
  </div>
  <div class="dz-fi-balance-foot">
    <div><span class="dz-fi-label">Entrées du mois</span><b class="dz-fi-pos">+ 4 820,00 €</b></div>
    <div><span class="dz-fi-label">Sorties du mois</span><b>− 3 579,20 €</b></div>
    <div><span class="dz-fi-label">Prochain prélèvement</span><b>Loyer · 1er oct.</b></div>
  </div>
</div>
"""

CARD = """
<div class="dz-fi-cardpage">
  <div class="dz-fi-cards">
    <div class="dz-fi-card dz-fi-card-ink">
      <div class="dz-fi-card-top"><b class="dz-fi-card-bank">Nexora</b><span class="dz-fi-card-tier">Premium</span></div>
      <div class="dz-fi-card-mid"><span class="dz-fi-chip"></span><i class="fas fa-wifi dz-fi-nfc"></i></div>
      <div class="dz-fi-card-num dz-mono">5412 7534 •••• 0418</div>
      <div class="dz-fi-card-bottom">
        <div><small>Titulaire</small><b>CAMILLE ROUVIÈRE</b></div>
        <div><small>Expire</small><b class="dz-mono">09/29</b></div>
        <span class="dz-fi-card-net"><i></i><i></i></span>
      </div>
    </div>
    <div class="dz-fi-card dz-fi-card-brand dz-fi-card-back">
      <div class="dz-fi-card-top"><b class="dz-fi-card-bank">Nexora</b><span class="dz-fi-card-tier">Virtuelle</span></div>
      <div class="dz-fi-card-num dz-mono">•••• 7720</div>
    </div>
  </div>
  <div class="dz-fi-cardctl">
    <div class="dz-fi-cardctl-head"><div><h3 class="dz-h4">Carte Premium</h3><span class="dz-fi-status dz-fi-status-ok">Active</span></div><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-eye"></i> Voir le code</a></div>
    <div class="dz-fi-limit">
      <div class="dz-fi-limit-head"><span>Plafond de paiement · 30 jours</span><b>1 842 € <small>/ 3 000 €</small></b></div>
      <div class="dz-fi-bar"><span style="width:61%"></span></div>
    </div>
    <div class="dz-fi-toggles">
      <a class="dz-fi-toggle" href="#"><span class="dz-fi-ticon"><i class="fas fa-snowflake"></i></span><div><b>Geler la carte</b><span>Bloque temporairement tous les paiements</span></div><span class="dz-fi-switch"></span></a>
      <a class="dz-fi-toggle dz-on" href="#"><span class="dz-fi-ticon"><i class="fas fa-globe-europe"></i></span><div><b>Paiements à l'étranger</b><span>Sans frais de change en zone euro</span></div><span class="dz-fi-switch"></span></a>
      <a class="dz-fi-toggle dz-on" href="#"><span class="dz-fi-ticon"><i class="fas fa-shopping-cart"></i></span><div><b>Paiements en ligne</b><span>Validation dans l'application</span></div><span class="dz-fi-switch"></span></a>
      <a class="dz-fi-toggle" href="#"><span class="dz-fi-ticon"><i class="fas fa-money-bill-wave"></i></span><div><b>Retraits d'espèces</b><span>Désactivés depuis le 12 sept.</span></div><span class="dz-fi-switch"></span></a>
    </div>
  </div>
</div>
"""


def tx(icon, tone, name, sub, amount, pos=False, pending=False, time=""):
    cls = " dz-fi-pos" if pos else ""
    pend = '<span class="dz-fi-pending">En attente</span>' if pending else ""
    return f"""
      <a class="dz-fi-tx" href="#">{cat(icon, tone)}<div class="dz-fi-tx-main"><b>{name}</b><span>{sub}</span></div>{pend}<div class="dz-fi-tx-amt"><b class="{cls.strip()}">{amount}</b><small>{time}</small></div></a>"""


TRANSACTIONS = f"""
<div class="dz-fi-txs">
  <div class="dz-fi-txs-head">
    <div><h3 class="dz-h3">Transactions</h3><p class="dz-fi-muted">Septembre 2026 · 64 opérations</p></div>
    <div class="dz-fi-search"><i class="fas fa-search"></i><span>Rechercher un marchand, un montant…</span></div>
  </div>
  <div class="dz-chips dz-fi-txs-filters"><a class="dz-chip dz-active" href="#">Tout</a><a class="dz-chip" href="#">Dépenses</a><a class="dz-chip" href="#">Revenus</a><a class="dz-chip" href="#"><i class="fas fa-paperclip"></i> Sans justificatif</a></div>
  <div class="dz-fi-day"><span>Aujourd'hui · jeudi 24 septembre</span><b>− 72,40 €</b></div>
  <div class="dz-fi-txlist">
    {tx("shopping-basket", "green", "Primeur des Halles", "Courses · Carte •••• 0418", "− 38,90 €", time="18:42", pending=True)}
    {tx("coffee", "amber", "Café Mercure", "Restaurants · Paiement mobile", "− 4,50 €", time="08:15")}
    {tx("train", "blue", "Rail Express", "Transports · Lyon → Paris", "− 29,00 €", time="07:02")}
  </div>
  <div class="dz-fi-day"><span>Hier · mercredi 23 septembre</span><b class="dz-fi-pos">+ 2 912,60 €</b></div>
  <div class="dz-fi-txlist">
    {tx("briefcase", "primary", "Studio Kaolin SAS", "Salaire · Virement reçu", "+ 3 120,00 €", pos=True, time="10:30")}
    {tx("film", "pink", "Cinéclub+", "Abonnements · Mensuel", "− 11,99 €", time="06:00")}
    {tx("gas-pump", "red", "Station Horizon", "Carburant · Carte •••• 0418", "− 64,21 €", time="19:11")}
    {tx("user-friends", "cyan", "Léa Pommier", "Remboursement dîner", "− 131,20 €", time="12:48")}
  </div>
</div>
"""

TX_DETAIL = f"""
<div class="dz-fi-txd">
  <div class="dz-fi-txd-hero">
    <span class="dz-fi-merchant">PH</span>
    <span class="dz-fi-muted">Primeur des Halles · Lyon 2e</span>
    <div class="dz-fi-amount dz-fi-amount-md"><b>− 38,90</b><span>€</span></div>
    <span class="dz-fi-status dz-fi-status-warn">En attente de débit</span>
  </div>
  <div class="dz-fi-kv">
    <div><span>Date</span><b>Jeudi 24 sept. 2026, 18:42</b></div>
    <div><span>Moyen de paiement</span><b><i class="far fa-credit-card"></i> Carte Premium •••• 0418</b></div>
    <div><span>Catégorie</span><b><span class="dz-fi-tag dz-fi-tone-green"><i class="fas fa-shopping-basket"></i> Courses</span></b></div>
    <div><span>Lieu</span><b>12 place des Célestins, Lyon</b></div>
    <div><span>Référence</span><b class="dz-mono">TXN-8F2A-51C9</b></div>
  </div>
  <div class="dz-fi-txd-receipt">
    <span class="dz-fi-receipt-ic"><i class="fas fa-receipt"></i></span>
    <div><b>Justificatif manquant</b><span>Ajoutez une photo du ticket pour votre note de frais.</span></div>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-camera"></i> Ajouter</a>
  </div>
  <div class="dz-fi-txd-note"><span class="dz-fi-label">Note</span><p>Courses pour le brunch de dimanche avec l'équipe.</p></div>
  <div class="dz-fi-txd-actions">
    <a class="dz-fi-chipbtn" href="#"><i class="fas fa-divide"></i> Partager la dépense</a>
    <a class="dz-fi-chipbtn" href="#"><i class="fas fa-tag"></i> Recatégoriser</a>
    <a class="dz-fi-chipbtn dz-fi-chipbtn-danger" href="#"><i class="fas fa-flag"></i> Signaler</a>
  </div>
</div>
"""


def budget(icon, tone, name, spent, limit, pct, note, state=""):
    return f"""
    <div class="dz-fi-budget {state}">
      <div class="dz-fi-budget-head">{cat(icon, tone)}<div><b>{name}</b><span>{note}</span></div><div class="dz-fi-budget-amt"><b>{spent}</b><small>sur {limit}</small></div></div>
      <div class="dz-fi-bar dz-fi-bar-{tone}"><span style="width:{min(pct, 100)}%"></span></div>
    </div>"""


BUDGETS = f"""
<div class="dz-fi-budgets">
  <div class="dz-fi-budgets-head">
    <div><span class="dz-eyebrow">Budgets de septembre</span><h3 class="dz-h3">Il vous reste <em>612 €</em> pour 6 jours</h3></div>
    <div class="dz-fi-ring" style="--v:76"><b>76 %</b><small>utilisé</small></div>
  </div>
  <div class="dz-fi-budget-grid">
    {budget("shopping-basket", "green", "Courses", "412 €", "500 €", 82, "88 € restants")}
    {budget("utensils", "amber", "Restaurants", "236 €", "200 €", 118, "Dépassé de 36 €", "dz-fi-over")}
    {budget("train", "blue", "Transports", "94 €", "150 €", 63, "56 € restants")}
    {budget("film", "pink", "Loisirs", "71 €", "120 €", 59, "49 € restants")}
    {budget("tshirt", "cyan", "Shopping", "189 €", "250 €", 76, "61 € restants")}
    {budget("heartbeat", "red", "Santé", "25 €", "80 €", 31, "55 € restants")}
  </div>
</div>
"""


def goal(icon, name, saved, target, pct, when, tone):
    return f"""
    <div class="dz-fi-goal">
      <div class="dz-fi-goal-ring dz-fi-tone-{tone}" style="--v:{pct}"><i class="fas fa-{icon}"></i></div>
      <b>{name}</b>
      <div class="dz-fi-goal-amt"><b>{saved}</b><span>/ {target}</span></div>
      <div class="dz-fi-goal-foot"><span>{pct} %</span><span>{when}</span></div>
    </div>"""


GOALS = f"""
<div class="dz-fi-goals-wrap">
  <div class="dz-fi-sechead"><div><span class="dz-eyebrow">Épargne</span><h3 class="dz-h3">Mes objectifs</h3><p class="dz-fi-muted">18 450 € mis de côté · +320 € ce mois-ci grâce aux arrondis</p></div><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouvel objectif</a></div>
  <div class="dz-fi-goals">
    {goal("umbrella-beach", "Voyage au Japon", "3 720 €", "4 500 €", 83, "Avril 2027", "primary")}
    {goal("home", "Apport immobilier", "11 200 €", "30 000 €", 37, "Déc. 2028", "blue")}
    {goal("shield-alt", "Épargne de précaution", "3 000 €", "3 000 €", 100, "Atteint", "green")}
    {goal("bicycle", "Vélo électrique", "530 €", "2 100 €", 25, "Juin 2027", "amber")}
  </div>
</div>
"""

TRANSFER = """
<div class="dz-fi-transfer">
  <div class="dz-fi-transfer-head"><h3 class="dz-h4">Nouveau virement</h3><span class="dz-fi-muted">Instantané · gratuit</span></div>
  <div class="dz-fi-field"><span class="dz-fi-label">Depuis</span><div class="dz-fi-select"><span class="dz-fi-flag">€</span><div><b>Compte courant</b><span>12 486,30 € disponibles</span></div><i class="fas fa-chevron-down"></i></div></div>
  <div class="dz-fi-field"><span class="dz-fi-label">Vers</span>
    <div class="dz-fi-payees">
      <a class="dz-fi-payee dz-on" href="#"><span class="dz-avatar">LP</span><span>Léa</span></a>
      <a class="dz-fi-payee" href="#"><span class="dz-avatar">HM</span><span>Hugo</span></a>
      <a class="dz-fi-payee" href="#"><span class="dz-avatar">SB</span><span>Sarah</span></a>
      <a class="dz-fi-payee" href="#"><span class="dz-avatar">AR</span><span>Agence R.</span></a>
      <a class="dz-fi-payee dz-fi-payee-add" href="#"><span class="dz-avatar"><i class="fas fa-plus"></i></span><span>Ajouter</span></a>
    </div>
    <div class="dz-fi-iban"><i class="fas fa-university"></i><span class="dz-mono">FR76 3000 4012 •••• 9921</span><span class="dz-fi-verified"><i class="fas fa-check-circle"></i> Nom vérifié</span></div>
  </div>
  <div class="dz-fi-bigfield"><span class="dz-fi-label">Montant</span><div class="dz-fi-bigamount"><b>250,00</b><span>€</span></div><div class="dz-fi-quick"><a href="#">50 €</a><a href="#">100 €</a><a class="dz-on" href="#">250 €</a><a href="#">500 €</a></div></div>
  <div class="dz-fi-field"><span class="dz-fi-label">Motif</span><div class="dz-fi-input">Week-end à Annecy</div></div>
  <div class="dz-fi-transfer-opts"><a class="dz-fi-optpill dz-on" href="#"><i class="fas fa-bolt"></i> Maintenant</a><a class="dz-fi-optpill" href="#"><i class="far fa-calendar"></i> Programmer</a><a class="dz-fi-optpill" href="#"><i class="fas fa-redo"></i> Récurrent</a></div>
  <a class="dz-btn dz-btn-lg dz-btn-block" href="#">Envoyer 250,00 € à Léa <i class="fas fa-arrow-right"></i></a>
  <p class="dz-fi-fineprint"><i class="fas fa-lock"></i> Confirmation par empreinte ou code à l'étape suivante</p>
</div>
"""


def bill(initials, tone, name, ref, due, amount, status, scls, direction="out"):
    return f"""
      <div class="dz-fi-bill">
        <span class="dz-fi-logo dz-fi-tone-{tone}">{initials}</span>
        <div class="dz-fi-bill-main"><b>{name}</b><span class="dz-mono">{ref}</span></div>
        <div class="dz-fi-bill-due"><span>{"Échéance" if direction == "out" else "Attendu le"}</span><b>{due}</b></div>
        <span class="dz-fi-status dz-fi-status-{scls}">{status}</span>
        <b class="dz-fi-bill-amt">{amount}</b>
        <a class="dz-fi-iconbtn" href="#" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></a>
      </div>"""


BILLS = f"""
<div class="dz-fi-bills">
  <div class="dz-fi-bills-head">
    <div><h3 class="dz-h3">Factures</h3><p class="dz-fi-muted">Atelier Kaolin · septembre 2026</p></div>
    <div class="dz-fi-seg"><a class="dz-on" href="#">À payer <b>5</b></a><a href="#">À encaisser <b>8</b></a></div>
  </div>
  <div class="dz-fi-bills-sum">
    <div class="dz-fi-sum dz-fi-sum-danger"><span>En retard</span><b>2 340,00 €</b><small>2 factures</small></div>
    <div class="dz-fi-sum dz-fi-sum-warn"><span>Sous 7 jours</span><b>4 118,50 €</b><small>2 factures</small></div>
    <div class="dz-fi-sum"><span>Plus tard</span><b>960,00 €</b><small>1 facture</small></div>
  </div>
  <div class="dz-fi-billlist">
    {bill("EV", "red", "Énergie Verte Pro", "F-2026-0911", "12 sept.", "1 480,00 €", "En retard · 12 j", "bad")}
    {bill("LB", "amber", "Loyer bureaux Bellecour", "QT-09-2026", "20 sept.", "860,00 €", "En retard · 4 j", "bad")}
    {bill("NX", "blue", "Nexcloud Hébergement", "INV-44821", "28 sept.", "318,50 €", "Prélèvement auto", "info")}
    {bill("AT", "primary", "Atelier Tissage Nord", "AT-7741", "30 sept.", "3 800,00 €", "À valider", "warn")}
    {bill("CF", "green", "Cabinet Fidal &amp; Co", "H-2026-118", "15 oct.", "960,00 €", "Programmée", "ok")}
  </div>
  <div class="dz-fi-bills-foot"><span class="dz-fi-muted">3 factures sélectionnées · 3 140,00 €</span><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-paper-plane"></i> Payer la sélection</a></div>
</div>
"""

STATEMENT = """
<div class="dz-fi-statement">
  <div class="dz-fi-statement-head">
    <div><span class="dz-fi-label">Relevé de compte</span><h3 class="dz-h3">Août 2026</h3><span class="dz-fi-muted">Compte courant · FR76 3000 4012 0000 4821 · du 1er au 31 août</span></div>
    <div class="dz-fi-period"><a class="dz-fi-iconbtn" href="#" aria-label="Mois précédent"><i class="fas fa-chevron-left"></i></a><span>Août 2026</span><a class="dz-fi-iconbtn" href="#" aria-label="Mois suivant"><i class="fas fa-chevron-right"></i></a></div>
  </div>
  <div class="dz-fi-flow">
    <div><span>Solde au 1er août</span><b>10 912,40 €</b></div>
    <i class="fas fa-plus"></i>
    <div class="dz-fi-flow-in"><span>Crédits</span><b>+ 5 240,00 €</b></div>
    <i class="fas fa-minus"></i>
    <div class="dz-fi-flow-out"><span>Débits</span><b>− 4 906,90 €</b></div>
    <i class="fas fa-equals"></i>
    <div class="dz-fi-flow-end"><span>Solde au 31 août</span><b>11 245,50 €</b></div>
  </div>
  <div class="dz-fi-stack">
    <div class="dz-fi-stack-bar"><span class="dz-fi-bg-primary" style="width:34%"></span><span class="dz-fi-bg-green" style="width:18%"></span><span class="dz-fi-bg-blue" style="width:14%"></span><span class="dz-fi-bg-amber" style="width:12%"></span><span class="dz-fi-bg-pink" style="width:9%"></span><span class="dz-fi-bg-mute" style="width:13%"></span></div>
    <div class="dz-fi-stack-legend">
      <span><i class="dz-fi-bg-primary"></i>Logement <b>1 668 €</b></span>
      <span><i class="dz-fi-bg-green"></i>Courses <b>883 €</b></span>
      <span><i class="dz-fi-bg-blue"></i>Transports <b>687 €</b></span>
      <span><i class="dz-fi-bg-amber"></i>Restaurants <b>589 €</b></span>
      <span><i class="dz-fi-bg-pink"></i>Loisirs <b>442 €</b></span>
      <span><i class="dz-fi-bg-mute"></i>Autres <b>638 €</b></span>
    </div>
  </div>
  <div class="dz-fi-statement-foot">
    <div class="dz-fi-insight"><i class="fas fa-lightbulb"></i><span>Vous avez dépensé <b>12 % de moins</b> qu'en juillet, surtout en restaurants.</span></div>
    <div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-file-csv"></i> CSV</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-file-pdf"></i> Télécharger le PDF</a></div>
  </div>
</div>
"""

CASHFLOW = """
<div class="dz-fi-panel dz-fi-cashflow">
  <div class="dz-fi-panel-head">
    <div><span class="dz-fi-label">Flux de trésorerie</span><div class="dz-fi-amount dz-fi-amount-md"><b>+ 38 420</b><span>€</span></div><span class="dz-fi-muted">Solde net sur 6 mois · <span class="dz-fi-pos">+18 % vs période précédente</span></span></div>
    <div class="dz-fi-legend"><span><i class="dz-fi-bg-green"></i>Encaissements</span><span><i class="dz-fi-bg-red"></i>Décaissements</span><span><i class="dz-fi-bg-line"></i>Net</span></div>
  </div>
  <div class="dz-fi-chart">
    <svg viewBox="0 0 600 240" preserveAspectRatio="none">
      <g class="dz-fi-grid"><line x1="0" y1="20" x2="600" y2="20"/><line x1="0" y1="70" x2="600" y2="70"/><line x1="0" y1="120" x2="600" y2="120"/><line x1="0" y1="170" x2="600" y2="170"/><line x1="0" y1="220" x2="600" y2="220"/></g>
      <g class="dz-fi-in"><rect x="30" y="60" width="26" height="60" rx="4"/><rect x="130" y="44" width="26" height="76" rx="4"/><rect x="230" y="70" width="26" height="50" rx="4"/><rect x="330" y="36" width="26" height="84" rx="4"/><rect x="430" y="30" width="26" height="90" rx="4"/><rect x="530" y="22" width="26" height="98" rx="4"/></g>
      <g class="dz-fi-out"><rect x="60" y="120" width="26" height="52" rx="4"/><rect x="160" y="120" width="26" height="58" rx="4"/><rect x="260" y="120" width="26" height="66" rx="4"/><rect x="360" y="120" width="26" height="54" rx="4"/><rect x="460" y="120" width="26" height="60" rx="4"/><rect x="560" y="120" width="26" height="56" rx="4"/></g>
      <polyline class="dz-fi-net" points="58,112 158,102 258,136 358,90 458,90 558,78"/>
      <g class="dz-fi-netdots"><circle cx="58" cy="112" r="4"/><circle cx="158" cy="102" r="4"/><circle cx="258" cy="136" r="4"/><circle cx="358" cy="90" r="4"/><circle cx="458" cy="90" r="4"/><circle cx="558" cy="78" r="5"/></g>
    </svg>
    <div class="dz-fi-chart-x"><span>Avr.</span><span>Mai</span><span>Juin</span><span>Juil.</span><span>Août</span><span>Sept.</span></div>
  </div>
  <div class="dz-fi-cash-kpis">
    <div><span>Encaissé</span><b class="dz-fi-pos">+ 184 600 €</b></div>
    <div><span>Décaissé</span><b class="dz-fi-neg">− 146 180 €</b></div>
    <div><span>Meilleur mois</span><b>Sept. · + 9 240 €</b></div>
    <div><span>Délai moyen d'encaissement</span><b>32 jours</b></div>
  </div>
</div>
"""


def holding(sym, tone, name, qty, price, value, var, up=True):
    return f"""
      <div class="dz-fi-hold"><span class="dz-fi-logo dz-fi-tone-{tone}">{sym}</span><div class="dz-fi-hold-main"><b>{name}</b><span>{qty}</span></div><span class="dz-fi-hold-price">{price}</span><div class="dz-fi-hold-val"><b>{value}</b><span class="{"dz-fi-pos" if up else "dz-fi-neg"}"><i class="fas fa-caret-{"up" if up else "down"}"></i> {var}</span></div></div>"""


PORTFOLIO = f"""
<div class="dz-fi-portfolio">
  <div class="dz-fi-alloc">
    <div class="dz-fi-alloc-head"><span class="dz-fi-label">Valeur du portefeuille</span><div class="dz-fi-amount dz-fi-amount-md"><b>86 912,40</b><span>€</span></div><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> + 9 486,12 € · 12,3 % sur 1 an</span></div>
    <div class="dz-fi-donut-wrap">
      <div class="dz-fi-donut"><div><b>6</b><small>classes d'actifs</small></div></div>
      <div class="dz-fi-alloc-legend">
        <span><i class="dz-fi-bg-primary"></i>Actions monde<b>42 %</b></span>
        <span><i class="dz-fi-bg-blue"></i>Obligations<b>20 %</b></span>
        <span><i class="dz-fi-bg-green"></i>ETF durables<b>16 %</b></span>
        <span><i class="dz-fi-bg-amber"></i>Immobilier<b>10 %</b></span>
        <span><i class="dz-fi-bg-pink"></i>Crypto-actifs<b>7 %</b></span>
        <span><i class="dz-fi-bg-mute"></i>Liquidités<b>5 %</b></span>
      </div>
    </div>
  </div>
  <div class="dz-fi-holds">
    <div class="dz-fi-holds-head"><b>Positions</b><div class="dz-fi-seg dz-fi-seg-sm"><a class="dz-on" href="#">Jour</a><a href="#">Mois</a><a href="#">Année</a></div></div>
    {holding("MW", "primary", "ETF Monde Large", "142 parts · PEA", "112,48 €", "15 972,16 €", "1,24 %")}
    {holding("AL", "blue", "Aéro Lumière", "38 actions", "184,20 €", "6 999,60 €", "0,86 %", False)}
    {holding("VG", "green", "Verdane Énergie", "210 actions", "41,15 €", "8 641,50 €", "2,31 %")}
    {holding("OB", "amber", "Oblig. Europe 2031", "12 titres", "982,40 €", "11 788,80 €", "0,05 %")}
    {holding("₿", "pink", "Bitcoin", "0,0842 BTC", "58 320 €", "4 910,54 €", "3,72 %", False)}
  </div>
</div>
"""


def quote(sym, price, var, up=True):
    return f'<a class="dz-fi-quote" href="#"><b>{sym}</b><span>{price}</span><em class="{"dz-fi-pos" if up else "dz-fi-neg"}"><i class="fas fa-caret-{"up" if up else "down"}"></i> {var}</em></a>'


TICKER = f"""
<div class="dz-fi-ticker">
  <span class="dz-fi-live"><span class="dz-dot"></span> Marchés · en direct</span>
  <div class="dz-marquee dz-fi-marquee">
    <div class="dz-marquee-track">
      {quote("CAC 40", "7 684,21", "0,62 %")}
      {quote("EURO STOXX 50", "4 988,10", "0,41 %")}
      {quote("EUR/USD", "1,1234", "0,18 %", False)}
      {quote("Or · once", "2 412,80 $", "0,93 %")}
      {quote("Brent", "78,42 $", "1,27 %", False)}
      {quote("BTC", "58 320 €", "3,72 %", False)}
      {quote("Verdane", "41,15 €", "2,31 %")}
      {quote("OAT 10 ans", "3,02 %", "0,04 pt")}
    </div>
  </div>
</div>
"""

QUOTE = """
<div class="dz-fi-panel dz-fi-stock">
  <div class="dz-fi-stock-head">
    <span class="dz-fi-logo dz-fi-logo-lg dz-fi-tone-green">VG</span>
    <div><h3 class="dz-h4">Verdane Énergie</h3><span class="dz-fi-muted">VRDN · Bourse de Paris · EUR</span></div>
    <a class="dz-btn dz-btn-ghost dz-btn-sm dz-fi-follow" href="#"><i class="far fa-star"></i> Suivre</a>
  </div>
  <div class="dz-fi-stock-price"><div class="dz-fi-amount"><b>41,15</b><span>€</span></div><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> + 0,93 € (2,31 %)</span><span class="dz-fi-muted"><span class="dz-dot dz-fi-livedot"></span> Marché ouvert · 15:42</span></div>
  <div class="dz-fi-seg dz-fi-seg-sm"><a href="#">1J</a><a href="#">5J</a><a class="dz-on" href="#">1M</a><a href="#">6M</a><a href="#">1A</a><a href="#">5A</a></div>
  <div class="dz-fi-stock-chart">
    <svg viewBox="0 0 500 160" preserveAspectRatio="none"><defs><linearGradient id="dz-fi-g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="dz-fi-stop-a"/><stop offset="1" class="dz-fi-stop-b"/></linearGradient></defs><line class="dz-fi-ref" x1="0" y1="96" x2="500" y2="96"/><path fill="url(#dz-fi-g2)" d="M0,110 L25,104 L50,112 L75,98 L100,102 L125,90 L150,96 L175,84 L200,92 L225,80 L250,86 L275,70 L300,76 L325,60 L350,68 L375,52 L400,58 L425,44 L450,50 L475,36 L500,30 L500,160 L0,160Z" class="dz-fi-area-fill"/><polyline class="dz-fi-area-line" points="0,110 25,104 50,112 75,98 100,102 125,90 150,96 175,84 200,92 225,80 250,86 275,70 300,76 325,60 350,68 375,52 400,58 425,44 450,50 475,36 500,30"/><circle class="dz-fi-area-dot" cx="500" cy="30" r="4"/></svg>
    <span class="dz-fi-chart-tip">41,15 €</span>
  </div>
  <div class="dz-fi-stats">
    <div><span>Ouverture</span><b>40,32 €</b></div>
    <div><span>Plus haut</span><b>41,48 €</b></div>
    <div><span>Plus bas</span><b>40,10 €</b></div>
    <div><span>Volume</span><b>1,28 M</b></div>
    <div><span>Capitalisation</span><b>8,6 Md€</b></div>
    <div><span>Rendement</span><b>3,4 %</b></div>
  </div>
  <div class="dz-fi-stock-actions"><a class="dz-btn dz-fi-btn-buy" href="#">Acheter</a><a class="dz-btn dz-btn-ghost" href="#">Vendre</a></div>
</div>
"""

CONVERTER = """
<div class="dz-fi-convert">
  <div class="dz-fi-convert-head"><h3 class="dz-h4">Convertisseur</h3><span class="dz-fi-muted"><span class="dz-dot dz-fi-livedot"></span> Taux mis à jour il y a 12 s</span></div>
  <div class="dz-fi-cur">
    <div class="dz-fi-cur-row"><span class="dz-fi-label">Vous envoyez</span><div class="dz-fi-cur-line"><b>1 500,00</b><a class="dz-fi-cur-pick" href="#"><span class="dz-fi-flag">€</span>EUR <i class="fas fa-chevron-down"></i></a></div></div>
    <a class="dz-fi-swap" href="#" aria-label="Inverser les devises"><i class="fas fa-exchange-alt"></i></a>
    <div class="dz-fi-cur-row"><span class="dz-fi-label">Le destinataire reçoit</span><div class="dz-fi-cur-line"><b>1 685,10</b><a class="dz-fi-cur-pick" href="#"><span class="dz-fi-flag dz-fi-flag-alt">$</span>USD <i class="fas fa-chevron-down"></i></a></div></div>
  </div>
  <div class="dz-fi-rate">
    <div class="dz-fi-rate-row"><span>Taux de change</span><b class="dz-mono">1 EUR = 1,1234 USD</b></div>
    <div class="dz-fi-rate-row"><span>Frais</span><b>0,00 € <span class="dz-fi-strike">4,50 €</span></b></div>
    <div class="dz-fi-rate-row"><span>Arrivée estimée</span><b>Aujourd'hui, avant 18 h</b></div>
  </div>
  <div class="dz-fi-minichart"><svg viewBox="0 0 300 50" preserveAspectRatio="none"><polyline class="dz-fi-area-line" points="0,34 20,30 40,36 60,28 80,32 100,24 120,26 140,20 160,28 180,22 200,18 220,24 240,16 260,20 280,12 300,14"/></svg><div class="dz-fi-minichart-x"><span>30 j</span><span class="dz-fi-pos">+ 0,8 %</span></div></div>
  <a class="dz-btn dz-btn-lg dz-btn-block" href="#">Convertir et envoyer</a>
</div>
"""


def sub(initials, tone, name, plan, date, price, note="", cls=""):
    n = f'<span class="dz-fi-sub-note">{note}</span>' if note else ""
    return f"""
    <div class="dz-fi-sub {cls}"><span class="dz-fi-logo dz-fi-tone-{tone}">{initials}</span><div class="dz-fi-sub-main"><b>{name}</b><span>{plan}</span>{n}</div><div class="dz-fi-sub-date"><span>Prochain débit</span><b>{date}</b></div><b class="dz-fi-sub-price">{price}</b></div>"""


SUBS = f"""
<div class="dz-fi-subs">
  <div class="dz-fi-subs-hero">
    <div><span class="dz-fi-label">Abonnements actifs</span><div class="dz-fi-amount dz-fi-amount-md"><b>87,43</b><span>€ / mois</span></div><span class="dz-fi-muted">Soit 1 049 € par an · 7 services</span></div>
    <div class="dz-fi-cal">
      <span class="dz-fi-cal-title">Octobre</span>
      <div class="dz-fi-cal-grid"><span>1</span><span class="dz-on">2</span><span>3</span><span>4</span><span>5</span><span class="dz-on">6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span class="dz-on">12</span><span>13</span><span>14</span><span class="dz-on">15</span><span>16</span><span>17</span><span>18</span><span>19</span><span>20</span><span class="dz-on">21</span></div>
    </div>
  </div>
  <div class="dz-fi-sublist">
    {sub("CP", "pink", "Cinéclub+", "Formule Duo · mensuel", "2 oct.", "11,99 €")}
    {sub("SN", "primary", "Sonora Musique", "Famille · mensuel", "6 oct.", "17,99 €", '<i class="fas fa-arrow-up"></i> +2 € depuis août', "dz-fi-sub-up")}
    {sub("NC", "blue", "Nexcloud 2 To", "Annuel · payé mensuellement", "12 oct.", "9,99 €")}
    {sub("FG", "green", "Forme &amp; Go", "Salle de sport · engagement 12 mois", "15 oct.", "34,90 €")}
    {sub("LQ", "amber", "Le Quotidien Libre", "Numérique · non utilisé depuis 64 j", "21 oct.", "12,56 €", '<i class="fas fa-lightbulb"></i> Pensez à résilier', "dz-fi-sub-idle")}
  </div>
</div>
"""


def expense(icon, tone, name, date, who, amount, status, scls, receipt=True):
    r = '<i class="fas fa-paperclip dz-fi-clip"></i>' if receipt else '<i class="fas fa-exclamation-circle dz-fi-noclip"></i>'
    return f"""
      <div class="dz-fi-exp">{cat(icon, tone)}<div class="dz-fi-exp-main"><b>{name}</b><span>{date} · {who}</span></div>{r}<span class="dz-fi-status dz-fi-status-{scls}">{status}</span><b class="dz-fi-exp-amt">{amount}</b></div>"""


EXPENSES = f"""
<div class="dz-fi-expenses">
  <div class="dz-fi-exp-head">
    <div><span class="dz-fi-label">Note de frais · NF-2026-09-014</span><h3 class="dz-h3">Salon Maison &amp; Objet, Paris</h3><div class="dz-fi-exp-who"><span class="dz-avatar dz-avatar-sm">CR</span><span>Camille Rouvière · Direction artistique</span></div></div>
    <div class="dz-fi-exp-total"><span>Total à rembourser</span><b>642,70 €</b><span class="dz-fi-status dz-fi-status-warn">En validation</span></div>
  </div>
  <ol class="dz-fi-flowsteps"><li class="dz-done"><span>Soumise</span><small>19 sept.</small></li><li class="dz-done"><span>Manager</span><small>Hugo M. · 21 sept.</small></li><li class="dz-current"><span>Comptabilité</span><small>En cours</small></li><li><span>Remboursée</span><small>Prévu le 30 sept.</small></li></ol>
  <div class="dz-fi-explist">
    {expense("train", "blue", "Train Lyon ↔ Paris", "16 sept.", "Rail Express", "118,00 €", "Validée", "ok")}
    {expense("hotel", "primary", "Hôtel Le Marais · 2 nuits", "16–18 sept.", "Hôtel Rivoli", "384,00 €", "Validée", "ok")}
    {expense("utensils", "amber", "Dîner client · 3 couverts", "17 sept.", "Bistrot Colbert", "96,50 €", "À justifier", "warn", False)}
    {expense("taxi", "cyan", "Taxi salon → gare", "18 sept.", "Taxi Parisien", "44,20 €", "Validée", "ok")}
  </div>
  <div class="dz-fi-exp-foot"><span class="dz-fi-muted"><i class="fas fa-info-circle"></i> Plafond repas : 35 € par personne</span><div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Refuser</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-check"></i> Approuver 642,70 €</a></div></div>
</div>
"""

FORECAST = """
<div class="dz-fi-panel dz-fi-forecast">
  <div class="dz-fi-panel-head">
    <div><span class="dz-fi-label">Prévision de trésorerie · 6 mois</span><h3 class="dz-h3">Au 31 mars 2027 : <em>214 800 €</em></h3><span class="dz-fi-muted">Fourchette probable 176 000 € – 248 000 €</span></div>
    <div class="dz-chips"><a class="dz-chip" href="#">Prudent</a><a class="dz-chip dz-active" href="#">Central</a><a class="dz-chip" href="#">Optimiste</a></div>
  </div>
  <div class="dz-fi-chart dz-fi-chart-fc">
    <svg viewBox="0 0 600 220" preserveAspectRatio="none">
      <g class="dz-fi-grid"><line x1="0" y1="30" x2="600" y2="30"/><line x1="0" y1="90" x2="600" y2="90"/><line x1="0" y1="150" x2="600" y2="150"/><line x1="0" y1="210" x2="600" y2="210"/></g>
      <path class="dz-fi-band" d="M300,120 L360,104 L420,96 L480,80 L540,66 L600,52 L600,118 L540,124 L480,130 L420,136 L360,138 L300,120Z"/>
      <polyline class="dz-fi-hist" points="0,150 60,140 120,146 180,128 240,132 300,120"/>
      <polyline class="dz-fi-proj" points="300,120 360,121 420,116 480,105 540,95 600,85"/>
      <line class="dz-fi-today" x1="300" y1="10" x2="300" y2="210"/>
      <line class="dz-fi-threshold" x1="0" y1="180" x2="600" y2="180"/>
      <circle class="dz-fi-area-dot" cx="300" cy="120" r="5"/>
    </svg>
    <span class="dz-fi-today-label">Aujourd'hui</span>
    <span class="dz-fi-threshold-label">Seuil de sécurité · 120 000 €</span>
    <div class="dz-fi-chart-x"><span>Avr.</span><span>Juin</span><span>Août</span><span>Oct.</span><span>Déc.</span><span>Fév.</span><span>Mars</span></div>
  </div>
  <div class="dz-fi-drivers">
    <div class="dz-fi-driver"><i class="fas fa-arrow-up dz-fi-pos"></i><div><b>Contrat Maison Oriel</b><span>+ 48 000 € attendus en novembre</span></div></div>
    <div class="dz-fi-driver"><i class="fas fa-arrow-down dz-fi-neg"></i><div><b>2 recrutements</b><span>− 11 200 € / mois dès janvier</span></div></div>
    <div class="dz-fi-driver"><i class="fas fa-exclamation-triangle dz-fi-warn"></i><div><b>TVA trimestrielle</b><span>− 26 400 € le 24 octobre</span></div></div>
  </div>
</div>
"""

COMPANY = """
<div class="dz-fi-company">
  <div class="dz-fi-company-head">
    <div><span class="dz-fi-label">Atelier Kaolin SAS · exercice 2026</span><h2 class="dz-h3">Pilotage financier</h2></div>
    <div class="dz-cluster"><div class="dz-fi-seg dz-fi-seg-sm"><a href="#">Mois</a><a class="dz-on" href="#">Trimestre</a><a href="#">Année</a></div><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-download"></i> Exporter</a></div>
  </div>
  <div class="dz-fi-kpis">
    <div class="dz-fi-kpi"><span>Chiffre d'affaires T3</span><b class="dz-counter">412 800 €</b><div><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 18,2 %</span><small>vs T2</small></div></div>
    <div class="dz-fi-kpi"><span>Marge brute</span><b>62,4 %</b><div class="dz-fi-kpi-bar"><span style="width:62.4%"></span><i style="left:58%"></i></div><small class="dz-fi-muted">Objectif 58 %</small></div>
    <div class="dz-fi-kpi"><span>Burn mensuel net</span><b class="dz-counter">31 600 €</b><div><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-down"></i> 6,5 %</span><small>en baisse</small></div></div>
    <div class="dz-fi-kpi dz-fi-kpi-hl"><span>Runway</span><b>19 <small>mois</small></b><div><small>Jusqu'en avril 2028 · 598 400 € en banque</small></div></div>
  </div>
  <div class="dz-fi-company-grid">
    <div class="dz-fi-panel">
      <div class="dz-fi-panel-head"><b>Chiffre d'affaires et résultat</b><div class="dz-fi-legend"><span><i class="dz-fi-bg-primary"></i>CA</span><span><i class="dz-fi-bg-line"></i>Résultat net</span></div></div>
      <div class="dz-fi-cols">
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:48%"></span><em style="height:8%"></em></div><small>Janv.</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:52%"></span><em style="height:10%"></em></div><small>Févr.</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:61%"></span><em style="height:14%"></em></div><small>Mars</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:58%"></span><em style="height:11%"></em></div><small>Avr.</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:66%"></span><em style="height:16%"></em></div><small>Mai</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:70%"></span><em style="height:18%"></em></div><small>Juin</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:74%"></span><em style="height:20%"></em></div><small>Juil.</small></div>
        <div class="dz-fi-col"><div class="dz-fi-col-bars"><span style="height:69%"></span><em style="height:15%"></em></div><small>Août</small></div>
        <div class="dz-fi-col dz-fi-col-now"><div class="dz-fi-col-bars"><span style="height:88%"></span><em style="height:24%"></em></div><small>Sept.</small></div>
      </div>
    </div>
    <div class="dz-fi-panel">
      <div class="dz-fi-panel-head"><b>Compte de résultat · T3</b></div>
      <div class="dz-fi-pl">
        <div class="dz-fi-pl-row dz-fi-pl-strong"><span>Chiffre d'affaires</span><b>412 800 €</b></div>
        <div class="dz-fi-pl-row"><span>Coût des ventes</span><b class="dz-fi-neg">− 155 200 €</b></div>
        <div class="dz-fi-pl-row dz-fi-pl-strong"><span>Marge brute</span><b>257 600 €</b></div>
        <div class="dz-fi-pl-row"><span>Salaires et charges</span><b class="dz-fi-neg">− 168 900 €</b></div>
        <div class="dz-fi-pl-row"><span>Loyers et services</span><b class="dz-fi-neg">− 24 300 €</b></div>
        <div class="dz-fi-pl-row"><span>Marketing</span><b class="dz-fi-neg">− 18 700 €</b></div>
        <div class="dz-fi-pl-row dz-fi-pl-total"><span>EBITDA</span><b>45 700 € <small>11,1 %</small></b></div>
      </div>
    </div>
  </div>
</div>
"""


def account(tone, icon, name, sub, amount, share):
    return f"""
    <a class="dz-fi-account" href="#"><span class="dz-fi-cat dz-fi-tone-{tone}"><i class="fas fa-{icon}"></i></span><div class="dz-fi-account-main"><b>{name}</b><span>{sub}</span></div><div class="dz-fi-account-amt"><b>{amount}</b><div class="dz-fi-bar dz-fi-bar-thin dz-fi-bar-{tone}"><span style="width:{share}%"></span></div></div></a>"""


ACCOUNTS = f"""
<div class="dz-fi-accounts">
  <div class="dz-fi-networth">
    <span class="dz-fi-label">Patrimoine net</span>
    <div class="dz-fi-amount"><b class="dz-counter">146 208</b><span>€</span></div>
    <span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> + 3 912 € ce mois-ci</span>
    <div class="dz-fi-nw-split"><div><small>Actifs</small><b>318 408 €</b></div><div><small>Dettes</small><b class="dz-fi-neg">− 172 200 €</b></div></div>
    <a class="dz-btn dz-btn-ghost dz-btn-sm dz-btn-block" href="#"><i class="fas fa-link"></i> Connecter un établissement</a>
  </div>
  <div class="dz-fi-acclist">
    <div class="dz-fi-group"><span>Comptes bancaires</span><b>18 912,80 €</b></div>
    {account("primary", "wallet", "Compte courant", "Nexora · FR76 •••• 4821", "12 486,30 €", 66)}
    {account("cyan", "user-friends", "Compte joint", "Nexora · avec Hugo M.", "6 426,50 €", 34)}
    <div class="dz-fi-group"><span>Épargne et placements</span><b>127 296,00 €</b></div>
    {account("green", "piggy-bank", "Livret A", "Banque Aubépine · 3 %", "22 950,00 €", 18)}
    {account("blue", "chart-line", "PEA", "Courtage Horizon", "86 912,40 €", 68)}
    {account("amber", "umbrella", "Assurance vie", "Mutuelle Arlequin", "17 433,60 €", 14)}
    <div class="dz-fi-group"><span>Crédits</span><b class="dz-fi-neg">− 172 200,00 €</b></div>
    {account("red", "home", "Prêt immobilier", "Banque Aubépine · 1,9 % · fin 2044", "− 172 200,00 €", 71)}
  </div>
</div>
"""

SPENDING = """
<div class="dz-fi-spending">
  <div class="dz-fi-spend-chart">
    <div class="dz-fi-spend-donut"><div><small>Dépensé en sept.</small><b>2 184 €</b><span class="dz-fi-neg"><i class="fas fa-arrow-up"></i> 6 % vs août</span></div></div>
  </div>
  <div class="dz-fi-spend-list">
    <div class="dz-fi-sechead dz-fi-sechead-tight"><h3 class="dz-h4">Dépenses par catégorie</h3><a class="dz-fi-link" href="#">Détails</a></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-primary"></i><span>Logement</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-primary" style="width:76%"></span></div><b>834 €</b><small>38 %</small></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-green"></i><span>Courses</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-green" style="width:44%"></span></div><b>412 €</b><small>19 %</small></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-amber"></i><span>Restaurants</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-amber" style="width:30%"></span></div><b>236 €</b><small>11 %</small></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-blue"></i><span>Transports</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-blue" style="width:24%"></span></div><b>194 €</b><small>9 %</small></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-pink"></i><span>Loisirs</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-pink" style="width:18%"></span></div><b>171 €</b><small>8 %</small></div>
    <div class="dz-fi-srow"><i class="dz-fi-bg-mute"></i><span>Autres</span><div class="dz-fi-bar dz-fi-bar-thin"><span class="dz-fi-bg-mute" style="width:32%"></span></div><b>337 €</b><small>15 %</small></div>
  </div>
</div>
"""

BLOCKS = [
    dict(name="solde principal", icon="fas fa-wallet", wrap="narrow", html=BALANCE),
    dict(name="carte bancaire", icon="far fa-credit-card", wrap="section", html=CARD),
    dict(name="comptes et patrimoine", icon="fas fa-university", wrap="section", html=ACCOUNTS),
    dict(name="transactions", icon="fas fa-list", wrap="narrow", html=TRANSACTIONS),
    dict(name="détail d'une transaction", icon="fas fa-receipt", wrap="narrow", html=TX_DETAIL),
    dict(name="dépenses par catégorie", icon="fas fa-chart-pie", wrap="section", html=SPENDING),
    dict(name="budgets", icon="fas fa-sliders-h", wrap="section", html=BUDGETS),
    dict(name="objectifs d'épargne", icon="fas fa-piggy-bank", wrap="section", html=GOALS),
    dict(name="virement", icon="fas fa-paper-plane", wrap="narrow", html=TRANSFER),
    dict(name="factures", icon="fas fa-file-invoice-dollar", wrap="section", html=BILLS),
    dict(name="relevé mensuel", icon="fas fa-file-alt", wrap="section", html=STATEMENT),
    dict(name="flux de trésorerie", icon="fas fa-chart-bar", wrap="section", html=CASHFLOW),
    dict(name="portefeuille", icon="fas fa-briefcase", wrap="section", html=PORTFOLIO),
    dict(name="cours en direct", icon="fas fa-stream", wrap="full", html=TICKER),
    dict(name="fiche valeur", icon="fas fa-chart-line", wrap="narrow", html=QUOTE),
    dict(name="convertisseur de devises", icon="fas fa-exchange-alt", wrap="narrow", html=CONVERTER),
    dict(name="abonnements", icon="fas fa-sync-alt", wrap="section", html=SUBS),
    dict(name="notes de frais", icon="fas fa-receipt", wrap="section", html=EXPENSES),
    dict(name="prévision", icon="fas fa-binoculars", wrap="section", html=FORECAST),
    dict(name="tableau de bord entreprise", icon="fas fa-building", wrap="section", html=COMPANY),
]
