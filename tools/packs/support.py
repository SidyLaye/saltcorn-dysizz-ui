"""Famille « Support » : relation client multicanale (préfixe CSS dz-sp-)."""
FAMILY = "support"

# ------------------------------------------------------------------ aides
CH = {
    "web": ("fas fa-globe", "Site web"),
    "mail": ("fas fa-envelope", "E-mail"),
    "wa": ("fab fa-whatsapp", "WhatsApp"),
    "sms": ("fas fa-sms", "SMS"),
}


def av(ini, c=1, size="", pres=""):
    cls = "dz-sp-av dz-sp-c%d" % c
    if size:
        cls += " dz-sp-av-" + size
    if pres:
        cls += " dz-sp-" + pres
    return '<span class="%s">%s</span>' % (cls, ini)


def ch(kind):
    icon, label = CH[kind]
    return '<span class="dz-sp-ch dz-sp-ch-%s" aria-label="%s"><i class="%s"></i></span>' % (kind, label, icon)


def avch(ini, c, kind, size=""):
    return '<div class="dz-sp-avwrap">%s%s</div>' % (av(ini, c, size), ch(kind))


def conv(ini, c, kind, name, time, prev, status, tags="", who="", n="", extra="", state=""):
    meta = '<span class="dz-sp-st dz-sp-st-%s">%s</span>' % status
    meta += tags
    if who:
        meta += '<span class="dz-sp-who">%s</span>' % who
    right = '<span class="dz-sp-n">%s</span>' % n if n else ""
    return (
        '<a class="dz-sp-conv%s" href="#">%s'
        '<div class="dz-sp-conv-body">'
        '<div class="dz-sp-conv-top"><b class="dz-sp-conv-name">%s</b><time class="dz-sp-time">%s</time></div>'
        '<p class="dz-sp-conv-prev">%s</p>'
        '%s'
        '<div class="dz-sp-conv-meta">%s%s</div>'
        '</div></a>'
    ) % (state, avch(ini, c, kind), name, time, prev, extra, meta, right)


def tag(label, t=1):
    return '<span class="dz-sp-tag dz-sp-t%d">%s</span>' % (t, label)


BLOCKS = []

# =====================================================================
# 1. Écran complet 3 colonnes
# =====================================================================
BLOCKS.append(dict(
    name="boîte de réception",
    icon="fas fa-inbox",
    html="""
<div class="dz-sp-app dz-sp-desk">
  <aside class="dz-sp-list">
    <div class="dz-sp-listhead">
      <div class="dz-sp-row">
        <h3 class="dz-sp-title">Conversations</h3>
        <span class="dz-sp-pill">24</span>
        <a class="dz-sp-ib dz-sp-push" href="#" aria-label="Filtrer"><i class="fas fa-sliders-h"></i></a>
        <a class="dz-sp-ib" href="#" aria-label="Nouvelle conversation"><i class="fas fa-pen"></i></a>
      </div>
      <div class="dz-sp-seg">
        <a class="dz-sp-seg-i dz-active" href="#">Mes <b>8</b></a>
        <a class="dz-sp-seg-i" href="#">Non assignées <b>5</b></a>
        <a class="dz-sp-seg-i" href="#">Toutes <b>24</b></a>
      </div>
    </div>
    <div class="dz-sp-convs">
""" + conv("CL", 1, "wa", "Camille Laurent", "14:21", "Super, merci ! Est-ce que je dois renvoyer l'ancienne ?", ("open", "Ouverte"), tag("Casse transport", 3), "IM", "2", state=" dz-active dz-sp-unread") + conv("JP", 4, "mail", "Julien Petit", "14:05", "Re : Facture FA-2026-0912 — erreur sur la TVA intracommunautaire", ("open", "Ouverte"), tag("Facturation", 2), "IM", "1", state=" dz-sp-unread") + conv("NH", 3, "web", "Nadia Haddad", "13:48", "Vous : Je vous envoie le lien de suivi dès que le colis part.", ("pending", "En attente"), tag("Livraison", 1), "IM") + conv("MO", 5, "sms", "Marc Olivier", "12:30", "Parfait, je serai là jeudi entre 9 h et 12 h.", ("snoozed", "Reportée"), "", "IM") + conv("LF", 6, "web", "Léa Fontaine", "11:02", "Est-ce que la suspension Nébula existe en laiton brossé ?", ("open", "Ouverte"), tag("Avant-vente", 4), "IM") + conv("HM", 2, "mail", "Hugo Mercier", "Hier", "Merci pour le remboursement, c'est bien reçu.", ("resolved", "Résolue"), "", "IM", state=" dz-sp-done") + """
    </div>
  </aside>

  <section class="dz-sp-thread">
    <header class="dz-sp-thead">
      <a class="dz-sp-ib dz-sp-back" href="#" aria-label="Retour"><i class="fas fa-chevron-left"></i></a>
      """ + avch("CL", 1, "wa") + """
      <div class="dz-sp-thead-id">
        <b class="dz-sp-thead-name">Camille Laurent</b>
        <span class="dz-sp-thead-sub">via WhatsApp · #C-48213 · ouverte il y a 9 min</span>
      </div>
      <div class="dz-sp-thead-act">
        <a class="dz-sp-assign" href="#">""" + av("IM", 2, "xs") + """<span>Inès Morel</span><i class="fas fa-chevron-down"></i></a>
        <a class="dz-sp-ib" href="#" aria-label="Reporter"><i class="far fa-clock"></i></a>
        <a class="dz-btn dz-btn-sm dz-sp-resolve" href="#"><i class="fas fa-check"></i> Résoudre</a>
      </div>
    </header>

    <div class="dz-sp-msgs">
      <div class="dz-sp-day"><span>Aujourd'hui</span></div>
      <div class="dz-sp-msg">""" + av("CL", 1, "sm") + """
        <div class="dz-sp-msg-col">
          <p class="dz-sp-bubble">Bonjour ! J'ai reçu ma commande <b>#ML-20418</b> ce matin mais l'abat-jour de la lampe Orbe est fêlé 😕</p>
          <div class="dz-sp-shot"><img class="dz-cover" src="https://picsum.photos/seed/lampe-orbe/480/300" alt="Photo de l'abat-jour fêlé"></div>
          <span class="dz-sp-meta">14:12</span>
        </div>
      </div>
      <p class="dz-sp-sys"><i class="fas fa-user-check"></i> Assignée à <b>Inès Morel</b> par la règle « Livraisons abîmées » · 14:13</p>
      <div class="dz-sp-msg dz-sp-out">
        <div class="dz-sp-msg-col">
          <p class="dz-sp-bubble">Bonjour Camille, merci pour la photo et désolée pour ce désagrément ! Je vérifie tout de suite le stock pour vous envoyer un remplacement.</p>
          <span class="dz-sp-meta">Inès · 14:16 · <i class="fas fa-check-double"></i> Lu</span>
        </div>
      </div>
      <div class="dz-sp-note">
        <div class="dz-sp-note-head"><i class="fas fa-lock"></i><b>Note privée</b><span>Karim Benali · 14:18</span></div>
        <p class="dz-sp-note-body"><span class="dz-sp-mention">@Inès</span> stock OK à l'entrepôt de Lyon, on peut expédier en express sans frais. Pense au bon de retour transporteur.</p>
      </div>
      <div class="dz-sp-msg">""" + av("CL", 1, "sm") + """
        <div class="dz-sp-msg-col">
          <p class="dz-sp-bubble">Super, merci ! Est-ce que je dois renvoyer l'ancienne ?</p>
          <span class="dz-sp-meta">14:21</span>
        </div>
      </div>
    </div>

    <div class="dz-sp-reply">
      <div class="dz-sp-rtabs">
        <a class="dz-sp-rtab dz-active" href="#">Répondre</a>
        <a class="dz-sp-rtab" href="#">Note privée</a>
        <span class="dz-sp-rhint"><i class="far fa-clock"></i> Fenêtre WhatsApp : 23 h 51 restantes</span>
      </div>
      <p class="dz-sp-rtext">Pas besoin, Camille : gardez l'abat-jour, notre transporteur ne le reprendra pas. Le nouveau part ce soir en express<span class="dz-sp-caret"></span></p>
      <div class="dz-sp-rbar">
        <a class="dz-sp-ib" href="#" aria-label="Émoji"><i class="far fa-smile"></i></a>
        <a class="dz-sp-ib" href="#" aria-label="Joindre un fichier"><i class="fas fa-paperclip"></i></a>
        <a class="dz-sp-ib" href="#" aria-label="Réponses types"><i class="fas fa-bolt"></i></a>
        <a class="dz-sp-ib" href="#" aria-label="Reformuler"><i class="fas fa-magic"></i></a>
        <span class="dz-sp-rkbd dz-sp-push"><span class="dz-kbd">⌘</span><span class="dz-kbd">↵</span></span>
        <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-paper-plane"></i> Envoyer</a>
      </div>
    </div>
  </section>

  <aside class="dz-sp-side">
    <div class="dz-sp-sidehead">
      """ + av("CL", 1, "lg") + """
      <b class="dz-sp-side-name">Camille Laurent</b>
      <span class="dz-sp-side-sub">Architecte d'intérieur · Atelier Lune</span>
      <div class="dz-sp-row dz-sp-center">
        <span class="dz-badge">Client VIP</span>
        <span class="dz-badge dz-badge-neutral">Lyon · 14:32</span>
      </div>
    </div>
    <div class="dz-sp-sect">
      <h4 class="dz-sp-sect-t">Coordonnées</h4>
      <p class="dz-sp-kv"><i class="far fa-envelope"></i><span>camille@atelier-lune.fr</span></p>
      <p class="dz-sp-kv"><i class="fas fa-phone-alt"></i><span>+33 6 42 18 77 05</span></p>
      <p class="dz-sp-kv"><i class="fas fa-map-marker-alt"></i><span>12 rue Mercière, 69002 Lyon</span></p>
    </div>
    <div class="dz-sp-sect">
      <h4 class="dz-sp-sect-t">Attributs</h4>
      <div class="dz-sp-attrs">
        <span>Client depuis</span><b>mars 2023</b>
        <span>Commandes</span><b>7</b>
        <span>Total dépensé</span><b>2 184 €</b>
        <span>Satisfaction</span><b>★ 4,9</b>
      </div>
    </div>
    <div class="dz-sp-sect">
      <h4 class="dz-sp-sect-t">Conversations précédentes <span class="dz-sp-mute">3</span></h4>
      <a class="dz-sp-prev" href="#"><i class="fas fa-envelope"></i><span>Devis 12 appliques Halo</span><time>août</time></a>
      <a class="dz-sp-prev" href="#"><i class="fas fa-globe"></i><span>Délai suspension Nébula</span><time>juin</time></a>
      <a class="dz-sp-prev" href="#"><i class="fab fa-whatsapp"></i><span>Changement d'adresse</span><time>févr.</time></a>
    </div>
    <div class="dz-sp-sect">
      <h4 class="dz-sp-sect-t">Notes</h4>
      <p class="dz-sp-sidenote">Préfère être contactée sur WhatsApp. Commande souvent pour ses chantiers : proposer la remise pro.</p>
    </div>
  </aside>
</div>
""",
))

# =====================================================================
# 2. Fil de conversation seul
# =====================================================================
BLOCKS.append(dict(
    name="fil de conversation",
    icon="far fa-comments",
    html="""
<div class="dz-sp-app dz-sp-threadcard">
  <header class="dz-sp-thead">
    """ + avch("JP", 4, "mail") + """
    <div class="dz-sp-thead-id">
      <b class="dz-sp-thead-name">Facture FA-2026-0912 — erreur de TVA</b>
      <span class="dz-sp-thead-sub">Julien Petit · julien.petit@brasserie-sillon.fr · #C-48207</span>
    </div>
    <div class="dz-sp-thead-act">
      <span class="dz-badge dz-badge-warning"><i class="fas fa-hourglass-half"></i> SLA 42 min</span>
      <a class="dz-sp-ib" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a>
    </div>
  </header>
  <div class="dz-sp-msgs">
    <div class="dz-sp-msg">""" + av("JP", 4, "sm") + """
      <div class="dz-sp-msg-col">
        <p class="dz-sp-bubble">Bonjour, notre numéro de TVA intracommunautaire n'apparaît pas sur la facture ci-jointe, du coup la TVA a été appliquée à 20 %. Pouvez-vous la corriger ?</p>
        <a class="dz-sp-file" href="#"><span class="dz-sp-file-ic dz-sp-pdf">PDF</span><span class="dz-sp-file-t"><b>FA-2026-0912.pdf</b><small>184 Ko</small></span><i class="fas fa-download"></i></a>
        <span class="dz-sp-meta">Mardi 09:41</span>
      </div>
    </div>
    <p class="dz-sp-sys"><i class="fas fa-tag"></i> <b>Système</b> a ajouté l'étiquette « Facturation » · 09:41</p>
    <p class="dz-sp-sys"><i class="fas fa-user-check"></i> <b>Karim Benali</b> a assigné la conversation à <b>Inès Morel</b> · 09:52</p>
    <div class="dz-sp-msg dz-sp-out">
      <div class="dz-sp-msg-col">
        <p class="dz-sp-bubble">Bonjour Julien, merci pour votre retour. Pouvez-vous me confirmer votre numéro de TVA (FR + 11 chiffres) ? J'émets l'avoir et la facture corrigée dans la foulée.</p>
        <span class="dz-sp-meta">Inès · 09:58 · <i class="fas fa-check-double"></i> Ouvert</span>
      </div>
      """ + av("IM", 2, "sm") + """
    </div>
    <div class="dz-sp-msg">""" + av("JP", 4, "sm") + """
      <div class="dz-sp-msg-col">
        <p class="dz-sp-bubble">Bien sûr : FR 42 853 219 004. Merci pour la rapidité !</p>
        <span class="dz-sp-meta">10:07</span>
      </div>
    </div>
    <div class="dz-sp-note">
      <div class="dz-sp-note-head"><i class="fas fa-lock"></i><b>Note privée</b><span>Inès Morel · 10:10</span></div>
      <p class="dz-sp-note-body">Numéro vérifié sur le registre européen ✔ — <span class="dz-sp-mention">@Compta</span> merci de générer l'avoir AV-2026-0331 (−212,40 €).</p>
    </div>
    <div class="dz-sp-msg">""" + av("JP", 4, "sm") + """
      <div class="dz-typing"><i></i><i></i><i></i></div>
    </div>
  </div>
  <div class="dz-sp-reply dz-sp-reply-note">
    <div class="dz-sp-canned">
      <p class="dz-sp-canned-h"><i class="fas fa-bolt"></i> Réponses types · « /fact »</p>
      <a class="dz-sp-canned-i dz-active" href="#"><span class="dz-mono">/facture-corrigee</span><span class="dz-sp-canned-t">Voici votre facture corrigée et l'avoir correspondant…</span><span class="dz-kbd">↵</span></a>
      <a class="dz-sp-canned-i" href="#"><span class="dz-mono">/facture-duplicata</span><span class="dz-sp-canned-t">Vous trouverez en pièce jointe le duplicata de…</span></a>
      <a class="dz-sp-canned-i" href="#"><span class="dz-mono">/facture-delai</span><span class="dz-sp-canned-t">Nos factures sont émises sous 48 h après…</span></a>
    </div>
    <div class="dz-sp-rtabs">
      <a class="dz-sp-rtab" href="#">Répondre</a>
      <a class="dz-sp-rtab dz-active dz-sp-rtab-note" href="#"><i class="fas fa-lock"></i> Note privée</a>
      <span class="dz-sp-rhint">Visible uniquement par l'équipe</span>
    </div>
    <p class="dz-sp-rtext">/fact<span class="dz-sp-caret"></span></p>
    <div class="dz-sp-rbar">
      <a class="dz-sp-ib" href="#" aria-label="Mentionner"><i class="fas fa-at"></i></a>
      <a class="dz-sp-ib" href="#" aria-label="Joindre un fichier"><i class="fas fa-paperclip"></i></a>
      <a class="dz-sp-ib" href="#" aria-label="Réponses types"><i class="fas fa-bolt"></i></a>
      <a class="dz-btn dz-btn-sm dz-sp-notebtn dz-sp-push" href="#"><i class="fas fa-lock"></i> Ajouter la note</a>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 3. Liste des conversations avec filtres
# =====================================================================
def row(ini, c, kind, name, sub, prev, tags, who_ini, who_c, time, status, state="", sla=""):
    return (
        '<a class="dz-sp-lrow%s" href="#">'
        '<span class="dz-sp-check"></span>'
        '%s'
        '<div class="dz-sp-lrow-who"><b>%s</b><span>%s</span></div>'
        '<p class="dz-sp-lrow-prev">%s</p>'
        '<div class="dz-sp-lrow-tags">%s</div>'
        '<div class="dz-sp-lrow-end">%s<span class="dz-sp-st dz-sp-st-%s">%s</span>%s<time class="dz-sp-time">%s</time></div>'
        '</a>'
    ) % (state, avch(ini, c, kind), name, sub, prev, tags, sla, status[0], status[1], av(who_ini, who_c, "xs") if who_ini else '<span class="dz-sp-av dz-sp-av-xs dz-sp-av-empty"><i class="fas fa-user-plus"></i></span>', time)


BLOCKS.append(dict(
    name="liste des conversations",
    icon="fas fa-stream",
    html="""
<div class="dz-sp-app dz-sp-lwrap">
  <div class="dz-sp-lhead">
    <div class="dz-sp-row">
      <h3 class="dz-sp-title">Boîte partagée</h3>
      <span class="dz-sp-pill">31</span>
      <div class="dz-sp-field dz-sp-push"><i class="fas fa-search"></i><span>Rechercher un client, un n° de commande…</span><span class="dz-kbd">/</span></div>
    </div>
    <div class="dz-sp-row dz-sp-lfilters">
      <div class="dz-sp-tabs">
        <a class="dz-sp-tab dz-active" href="#">Mes conversations <b>8</b></a>
        <a class="dz-sp-tab" href="#">Non assignées <b>5</b></a>
        <a class="dz-sp-tab" href="#">Toutes <b>31</b></a>
        <a class="dz-sp-tab" href="#">Mentions <b>2</b></a>
      </div>
      <div class="dz-sp-row dz-sp-push">
        <a class="dz-sp-drop" href="#"><i class="fas fa-filter"></i> Ouvertes <i class="fas fa-chevron-down"></i></a>
        <a class="dz-sp-drop" href="#"><i class="fas fa-sort-amount-down"></i> Plus anciennes d'abord <i class="fas fa-chevron-down"></i></a>
      </div>
    </div>
  </div>
  <div class="dz-sp-lbulk">
    <span class="dz-sp-check dz-sp-checked"></span>
    <b>2 sélectionnées</b>
    <a class="dz-sp-bulk" href="#"><i class="fas fa-user-plus"></i> Assigner</a>
    <a class="dz-sp-bulk" href="#"><i class="fas fa-tag"></i> Étiqueter</a>
    <a class="dz-sp-bulk" href="#"><i class="far fa-clock"></i> Reporter</a>
    <a class="dz-sp-bulk" href="#"><i class="fas fa-check"></i> Résoudre</a>
  </div>
  <div class="dz-sp-lrows">
""" + row("YR", 3, "wa", "Yanis Rahmani", "+33 7 81 22 04 19", "<b>Colis bloqué en relais depuis 6 jours</b> — le point relais dit ne rien avoir reçu…", tag("Livraison", 1) + tag("Urgent", 5), "", 0, "14:32", ("open", "Ouverte"), " dz-sp-unread dz-sp-sel", '<span class="dz-sp-sla dz-sp-sla-late"><i class="fas fa-fire"></i> −12 min</span>') \
    + row("CL", 1, "wa", "Camille Laurent", "Atelier Lune", "<b>Abat-jour fêlé à la réception</b> — Super, merci ! Est-ce que je dois renvoyer l'ancienne ?", tag("Casse transport", 3), "IM", 2, "14:21", ("open", "Ouverte"), " dz-sp-unread dz-sp-sel", '<span class="dz-sp-sla dz-sp-sla-soon"><i class="fas fa-hourglass-half"></i> 18 min</span>') \
    + row("JP", 4, "mail", "Julien Petit", "Brasserie Sillon", "<b>Re : Facture FA-2026-0912</b> — Bien sûr : FR 42 853 219 004. Merci pour la rapidité !", tag("Facturation", 2), "IM", 2, "10:07", ("open", "Ouverte"), "", '<span class="dz-sp-sla"><i class="far fa-clock"></i> 2 h 40</span>') \
    + row("LF", 6, "web", "Léa Fontaine", "Visiteuse · Paris", "<b>Question avant achat</b> — Est-ce que la suspension Nébula existe en laiton brossé ?", tag("Avant-vente", 4), "SL", 5, "11:02", ("pending", "En attente")) \
    + row("MO", 5, "sms", "Marc Olivier", "+33 6 11 90 72 38", "<b>Créneau de livraison</b> — Parfait, je serai là jeudi entre 9 h et 12 h.", "", "KB", 1, "Hier", ("snoozed", "Reportée"), " dz-sp-dim") + """
  </div>
  <div class="dz-sp-lfoot"><span>1–5 sur 31</span><div class="dz-sp-row"><a class="dz-sp-ib" href="#" aria-label="Page précédente"><i class="fas fa-chevron-left"></i></a><a class="dz-sp-ib" href="#" aria-label="Page suivante"><i class="fas fa-chevron-right"></i></a></div></div>
</div>
""",
))

# =====================================================================
# 4. Fiche contact détaillée
# =====================================================================
BLOCKS.append(dict(
    name="fiche contact",
    icon="far fa-address-card",
    html="""
<div class="dz-sp-contact">
  <div class="dz-sp-app dz-sp-chead">
    <div class="dz-sp-chead-band"></div>
    <div class="dz-sp-chead-body">
      """ + av("CL", 1, "xl", "on") + """
      <div class="dz-sp-chead-id">
        <h3 class="dz-sp-h">Camille Laurent</h3>
        <p class="dz-sp-chead-sub">Architecte d'intérieur chez <b>Atelier Lune</b> · Lyon, France · 14:32 heure locale</p>
        <div class="dz-sp-row">""" + tag("VIP", 3) + tag("Professionnel", 4) + tag("Newsletter", 1) + """<a class="dz-sp-addtag" href="#"><i class="fas fa-plus"></i> Étiquette</a></div>
      </div>
      <div class="dz-sp-row dz-sp-chead-act">
        <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-edit"></i> Modifier</a>
        <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-comment-medical"></i> Nouvelle conversation</a>
      </div>
    </div>
    <div class="dz-sp-cstats">
      <div class="dz-sp-cstat"><span>Conversations</span><b>12</b><small>2 ouvertes</small></div>
      <div class="dz-sp-cstat"><span>Satisfaction moyenne</span><b>4,9 <i class="fas fa-star"></i></b><small>sur 9 avis</small></div>
      <div class="dz-sp-cstat"><span>1re réponse moyenne</span><b>6 min</b><small>objectif 15 min</small></div>
      <div class="dz-sp-cstat"><span>Chiffre d'affaires</span><b>2 184 €</b><small>7 commandes</small></div>
    </div>
  </div>
  <div class="dz-sp-cgrid">
    <div class="dz-sp-app dz-sp-cpanel">
      <h4 class="dz-sp-sect-t">Coordonnées</h4>
      <div class="dz-sp-fields">
        <div class="dz-sp-fieldrow"><span>E-mail</span><b>camille@atelier-lune.fr</b></div>
        <div class="dz-sp-fieldrow"><span>Téléphone</span><b>+33 6 42 18 77 05</b></div>
        <div class="dz-sp-fieldrow"><span>WhatsApp</span><b>+33 6 42 18 77 05 <i class="fas fa-check-circle dz-sp-ok"></i></b></div>
        <div class="dz-sp-fieldrow"><span>Adresse</span><b>12 rue Mercière, 69002 Lyon</b></div>
        <div class="dz-sp-fieldrow"><span>Langue</span><b>Français</b></div>
      </div>
      <h4 class="dz-sp-sect-t">Attributs personnalisés</h4>
      <div class="dz-sp-fields">
        <div class="dz-sp-fieldrow"><span>Segment</span><b>Prescripteur</b></div>
        <div class="dz-sp-fieldrow"><span>Remise pro</span><b>12 %</b></div>
        <div class="dz-sp-fieldrow"><span>Commercial</span><b>Théo Garnier</b></div>
        <div class="dz-sp-fieldrow"><span>Consentement SMS</span><b>Oui · 04/03/2023</b></div>
      </div>
    </div>
    <div class="dz-sp-app dz-sp-cpanel">
      <div class="dz-sp-row"><h4 class="dz-sp-sect-t">Commandes récentes</h4><a class="dz-sp-link dz-sp-push" href="#">Tout voir</a></div>
      <div class="dz-sp-orders">
        <div class="dz-sp-order"><span class="dz-sp-order-ic"><i class="fas fa-box"></i></span><div class="dz-sp-order-t"><b>#ML-20418</b><span>Lampe Orbe, 2 appliques Halo</span></div><span class="dz-badge dz-badge-warning">Litige</span><b class="dz-sp-order-p">389,00 €</b></div>
        <div class="dz-sp-order"><span class="dz-sp-order-ic"><i class="fas fa-box"></i></span><div class="dz-sp-order-t"><b>#ML-19877</b><span>12 appliques Halo · devis pro</span></div><span class="dz-badge dz-badge-success">Livrée</span><b class="dz-sp-order-p">1 056,00 €</b></div>
        <div class="dz-sp-order"><span class="dz-sp-order-ic"><i class="fas fa-box"></i></span><div class="dz-sp-order-t"><b>#ML-18402</b><span>Suspension Nébula laiton</span></div><span class="dz-badge dz-badge-success">Livrée</span><b class="dz-sp-order-p">429,00 €</b></div>
      </div>
      <h4 class="dz-sp-sect-t">Conversations</h4>
      <a class="dz-sp-prev" href="#">""" + ch("wa") + """<span>Abat-jour fêlé à la réception</span><span class="dz-sp-st dz-sp-st-open">Ouverte</span></a>
      <a class="dz-sp-prev" href="#">""" + ch("mail") + """<span>Devis 12 appliques Halo</span><span class="dz-sp-st dz-sp-st-resolved">Résolue</span></a>
      <a class="dz-sp-prev" href="#">""" + ch("web") + """<span>Délai suspension Nébula</span><span class="dz-sp-st dz-sp-st-resolved">Résolue</span></a>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 5. Réponses types
# =====================================================================
def canned(short, title, body, cat, uses, who, c, active=False):
    return (
        '<a class="dz-sp-cr%s" href="#">'
        '<div class="dz-sp-cr-top"><span class="dz-sp-short">%s</span><b>%s</b><span class="dz-sp-cr-cat">%s</span></div>'
        '<p class="dz-sp-cr-body">%s</p>'
        '<div class="dz-sp-cr-foot">%s<span>%s</span><span class="dz-sp-push"><i class="fas fa-chart-line"></i> %s utilisations</span></div>'
        '</a>'
    ) % (" dz-active" if active else "", short, title, cat, body, av(who, c, "xs"), "Modifiée par " + {"IM": "Inès", "KB": "Karim", "SL": "Sofia"}[who], uses)


V = lambda s: '<span class="dz-sp-var">' + s + '</span>'

BLOCKS.append(dict(
    name="réponses types",
    icon="fas fa-bolt",
    html="""
<div class="dz-sp-app dz-sp-canlib">
  <aside class="dz-sp-cannav">
    <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-plus"></i> Nouvelle réponse</a>
    <p class="dz-sp-navlabel">Dossiers</p>
    <a class="dz-sp-navi dz-active" href="#"><i class="fas fa-layer-group"></i><span>Toutes</span><b>48</b></a>
    <a class="dz-sp-navi" href="#"><i class="fas fa-truck"></i><span>Livraison</span><b>14</b></a>
    <a class="dz-sp-navi" href="#"><i class="fas fa-undo-alt"></i><span>Retours &amp; remboursements</span><b>11</b></a>
    <a class="dz-sp-navi" href="#"><i class="fas fa-file-invoice"></i><span>Facturation</span><b>9</b></a>
    <a class="dz-sp-navi" href="#"><i class="fas fa-lightbulb"></i><span>Conseils produit</span><b>8</b></a>
    <a class="dz-sp-navi" href="#"><i class="fas fa-hand-sparkles"></i><span>Formules de politesse</span><b>6</b></a>
    <p class="dz-sp-navlabel">Variables</p>
    <div class="dz-sp-row dz-sp-vars">""" + V("{{contact.prénom}}") + V("{{commande.numéro}}") + V("{{agent.prénom}}") + V("{{suivi.lien}}") + """</div>
  </aside>
  <div class="dz-sp-canmain">
    <div class="dz-sp-row">
      <div class="dz-sp-field dz-sp-grow"><i class="fas fa-search"></i><span>Rechercher par titre, raccourci ou contenu</span></div>
      <a class="dz-sp-drop" href="#"><i class="fas fa-sort"></i> Les plus utilisées <i class="fas fa-chevron-down"></i></a>
    </div>
    <div class="dz-sp-crs">
""" + canned("/suivi", "Envoyer le lien de suivi", "Bonjour " + V("{{contact.prénom}}") + ", votre commande " + V("{{commande.numéro}}") + " est en route ! Vous pouvez suivre le colis ici : " + V("{{suivi.lien}}") + ". Belle journée, " + V("{{agent.prénom}}"), "Livraison", "1 284", "IM", 2, True) \
    + canned("/casse", "Colis abîmé : remplacement", "Je suis vraiment désolé(e) pour ce désagrément. Pas besoin de nous renvoyer l'article : un remplacement part aujourd'hui en express, sans frais pour vous.", "Retours", "342", "KB", 1) \
    + canned("/remb", "Remboursement effectué", "Votre remboursement de " + V("{{remboursement.montant}}") + " a été émis ce jour. Il apparaîtra sur votre relevé sous 3 à 5 jours ouvrés.", "Retours", "596", "SL", 5) \
    + canned("/pro", "Présenter l'offre professionnelle", "Pour vos chantiers, notre programme pro vous donne 12 % de remise, un interlocuteur dédié et des délais garantis. Voulez-vous que je vous ouvre un compte ?", "Conseils", "121", "IM", 2) + """
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 6. Widget de chat pour site
# =====================================================================
BLOCKS.append(dict(
    name="widget de chat",
    icon="far fa-comment-dots",
    html="""
<div class="dz-sp-wstage">
  <div class="dz-sp-wsite">
    <span class="dz-sp-wsite-l" style="--w:38%"></span>
    <span class="dz-sp-wsite-l" style="--w:62%"></span>
    <span class="dz-sp-wsite-l" style="--w:54%"></span>
    <div class="dz-sp-wsite-cards"><span></span><span></span><span></span></div>
  </div>
  <div class="dz-sp-proactive">
    """ + av("SL", 5, "sm", "on") + """
    <p><b>Sofia</b> · Besoin d'aide pour choisir la bonne ampoule pour votre lampe ?</p>
  </div>
  <div class="dz-sp-widget">
    <div class="dz-sp-whead">
      <div class="dz-sp-row">
        <span class="dz-sp-wlogo"><i class="fas fa-lightbulb"></i></span>
        <div class="dz-avatars dz-sp-wteam">""" + av("IM", 2, "sm") + av("KB", 1, "sm") + av("SL", 5, "sm") + """</div>
        <a class="dz-sp-ib dz-sp-wclose dz-sp-push" href="#" aria-label="Réduire"><i class="fas fa-chevron-down"></i></a>
      </div>
      <p class="dz-sp-whello">Bonjour Léa 👋</p>
      <p class="dz-sp-wsub">Comment pouvons-nous vous aider ?</p>
    </div>
    <div class="dz-sp-wbody">
      <a class="dz-sp-wcard dz-sp-wsend" href="#">
        <div><b>Envoyez-nous un message</b><span class="dz-sp-wonline"><i class="dz-sp-live"></i> Réponse en moins de 5 min</span></div>
        <i class="fas fa-paper-plane"></i>
      </a>
      <div class="dz-sp-wcard">
        <div class="dz-sp-field"><i class="fas fa-search"></i><span>Rechercher dans l'aide</span></div>
        <a class="dz-sp-wlink" href="#"><span>Suivre ma commande</span><i class="fas fa-chevron-right"></i></a>
        <a class="dz-sp-wlink" href="#"><span>Retourner un article sous 30 jours</span><i class="fas fa-chevron-right"></i></a>
        <a class="dz-sp-wlink" href="#"><span>Quelle ampoule pour ma lampe ?</span><i class="fas fa-chevron-right"></i></a>
      </div>
      <div class="dz-sp-wcard dz-sp-whours">
        <i class="far fa-clock"></i>
        <div><b>Ouvert · lun–ven 9 h – 19 h</b><span>Samedi 10 h – 16 h · fermé le dimanche</span></div>
      </div>
    </div>
    <nav class="dz-sp-wnav">
      <a class="dz-active" href="#"><i class="fas fa-home"></i><span>Accueil</span></a>
      <a href="#"><i class="far fa-comments"></i><span>Messages</span></a>
      <a href="#"><i class="far fa-question-circle"></i><span>Aide</span></a>
    </nav>
    <p class="dz-sp-wpow">Assistance Maison Lumen</p>
  </div>
  <a class="dz-sp-launch" href="#" aria-label="Fermer le chat"><i class="fas fa-times"></i></a>
</div>
""",
))

# =====================================================================
# 7. Enquête de satisfaction
# =====================================================================
BLOCKS.append(dict(
    name="enquête de satisfaction",
    icon="far fa-smile",
    html="""
<div class="dz-sp-csat">
  <div class="dz-sp-app dz-sp-csat-card">
    <div class="dz-sp-csat-agent">""" + av("IM", 2, "lg", "on") + """<div><b>Inès Morel</b><span>Conversation résolue · #C-48213</span></div></div>
    <h3 class="dz-sp-h">Comment s'est passé votre échange ?</h3>
    <p class="dz-sp-csat-sub">Votre avis nous aide à améliorer notre service. Cela prend 10 secondes.</p>
    <div class="dz-sp-faces">
      <a class="dz-sp-face" href="#"><span class="dz-sp-emo">😞</span><span>Très déçu</span></a>
      <a class="dz-sp-face" href="#"><span class="dz-sp-emo">🙁</span><span>Déçu</span></a>
      <a class="dz-sp-face" href="#"><span class="dz-sp-emo">😐</span><span>Correct</span></a>
      <a class="dz-sp-face" href="#"><span class="dz-sp-emo">🙂</span><span>Bien</span></a>
      <a class="dz-sp-face dz-active" href="#"><span class="dz-sp-emo">😍</span><span>Excellent</span></a>
    </div>
    <div class="dz-sp-reasons">
      <p class="dz-sp-csat-q">Qu'avez-vous le plus apprécié ?</p>
      <div class="dz-sp-row">
        <a class="dz-sp-reason dz-active" href="#"><i class="fas fa-check"></i> Rapidité</a>
        <a class="dz-sp-reason dz-active" href="#"><i class="fas fa-check"></i> Solution trouvée</a>
        <a class="dz-sp-reason" href="#">Amabilité</a>
        <a class="dz-sp-reason" href="#">Clarté</a>
      </div>
    </div>
    <p class="dz-sp-textarea">Remplacement reçu en 24 h, rien à dire, merci Inès !</p>
    <a class="dz-btn dz-btn-block" href="#">Envoyer mon avis</a>
  </div>
  <div class="dz-sp-app dz-sp-csat-mail">
    <p class="dz-sp-csat-kicker">Par e-mail · 5 étoiles</p>
    <h3 class="dz-sp-h">Votre demande #C-48207 est résolue</h3>
    <p class="dz-sp-csat-sub">Bonjour Julien, notez l'aide reçue en un clic :</p>
    <div class="dz-sp-stars">
      <a class="dz-sp-star dz-on" href="#" aria-label="1 étoile"><i class="fas fa-star"></i></a>
      <a class="dz-sp-star dz-on" href="#" aria-label="2 étoiles"><i class="fas fa-star"></i></a>
      <a class="dz-sp-star dz-on" href="#" aria-label="3 étoiles"><i class="fas fa-star"></i></a>
      <a class="dz-sp-star dz-on" href="#" aria-label="4 étoiles"><i class="fas fa-star"></i></a>
      <a class="dz-sp-star" href="#" aria-label="5 étoiles"><i class="fas fa-star"></i></a>
    </div>
    <div class="dz-sp-row dz-sp-stars-l"><span>Pas du tout satisfait</span><span class="dz-sp-push">Très satisfait</span></div>
    <div class="dz-sp-thanks"><i class="fas fa-heart"></i><div><b>Merci, c'est noté !</b><span>4 étoiles · Inès sera ravie de le lire.</span></div></div>
  </div>
</div>
""",
))

# =====================================================================
# 8. Résultats de satisfaction
# =====================================================================
def dist(stars, pct, n):
    return '<div class="dz-sp-dist"><span class="dz-sp-dist-l">%s <i class="fas fa-star"></i></span><span class="dz-sp-bar"><span style="--v:%s%%"></span></span><b>%s %%</b><small>%s</small></div>' % (stars, pct, pct, n)


def comment(ini, c, name, stars, text, agent, when):
    st = '<i class="fas fa-star"></i>' * stars + '<i class="fas fa-star dz-sp-soff"></i>' * (5 - stars)
    return '<div class="dz-sp-rev">%s<div class="dz-sp-rev-b"><div class="dz-sp-rev-top"><b>%s</b><span class="dz-sp-rev-st">%s</span><time>%s</time></div><p>%s</p><span class="dz-sp-rev-ag">Avec %s</span></div></div>' % (av(ini, c, "sm"), name, st, when, text, agent)


BLOCKS.append(dict(
    name="résultats de satisfaction",
    icon="fas fa-star-half-alt",
    html="""
<div class="dz-sp-res">
  <div class="dz-sp-app dz-sp-res-score">
    <p class="dz-sp-kicker">Satisfaction · 30 derniers jours</p>
    <div class="dz-sp-res-big"><b class="dz-counter">94 %</b><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 3,2 pts</span></div>
    <p class="dz-sp-res-sub">de réponses positives sur <b>1 128 avis</b> · taux de réponse 38 %</p>
    <div class="dz-sp-res-dist">""" + dist(5, 81, "914") + dist(4, 13, "147") + dist(3, 4, "41") + dist(2, 1, "15") + dist(1, 1, "11") + """</div>
    <div class="dz-sp-res-agents">
      <p class="dz-sp-sect-t">Par agent</p>
      <div class="dz-sp-agrow">""" + av("IM", 2, "xs") + """<span>Inès Morel</span><span class="dz-sp-bar"><span style="--v:97%"></span></span><b>97 %</b></div>
      <div class="dz-sp-agrow">""" + av("SL", 5, "xs") + """<span>Sofia Lemaire</span><span class="dz-sp-bar"><span style="--v:95%"></span></span><b>95 %</b></div>
      <div class="dz-sp-agrow">""" + av("KB", 1, "xs") + """<span>Karim Benali</span><span class="dz-sp-bar"><span style="--v:91%"></span></span><b>91 %</b></div>
      <div class="dz-sp-agrow">""" + av("TG", 6, "xs") + """<span>Théo Garnier</span><span class="dz-sp-bar"><span style="--v:88%"></span></span><b>88 %</b></div>
    </div>
  </div>
  <div class="dz-sp-app dz-sp-res-feed">
    <div class="dz-sp-row"><h3 class="dz-sp-title">Derniers commentaires</h3>
      <div class="dz-sp-tabs dz-sp-push"><a class="dz-sp-tab dz-active" href="#">Tous</a><a class="dz-sp-tab" href="#">Positifs</a><a class="dz-sp-tab" href="#">Négatifs <b>6</b></a></div>
    </div>
""" + comment("CL", 1, "Camille Laurent", 5, "Remplacement reçu en 24 h, rien à dire, merci Inès !", "Inès Morel", "il y a 12 min") \
    + comment("JP", 4, "Julien Petit", 4, "Facture corrigée très vite. Dommage qu'il ait fallu la demander.", "Inès Morel", "il y a 1 h") \
    + comment("YR", 3, "Yanis Rahmani", 2, "Toujours pas de colis au point relais, j'attends une vraie solution.", "Karim Benali", "il y a 3 h") \
    + comment("LF", 6, "Léa Fontaine", 5, "Conseils super précis sur le choix des ampoules. Je recommande !", "Sofia Lemaire", "hier") + """
  </div>
</div>
""",
))

# =====================================================================
# 9. Tableau de bord support
# =====================================================================
def daybar(d, a, b, today=False):
    return '<div class="dz-sp-col%s"><div class="dz-sp-colbars"><span class="dz-sp-in" style="--h:%s%%"></span><span class="dz-sp-res2" style="--h:%s%%"></span></div><span class="dz-sp-coll">%s</span></div>' % (" dz-sp-today" if today else "", a, b, d)


BLOCKS.append(dict(
    name="tableau de bord",
    icon="fas fa-chart-bar",
    html="""
<div class="dz-sp-dash">
  <div class="dz-sp-row dz-sp-dash-head">
    <div><p class="dz-sp-kicker">Support · Maison Lumen</p><h3 class="dz-sp-h">Vue d'ensemble</h3></div>
    <div class="dz-sp-tabs dz-sp-push"><a class="dz-sp-tab" href="#">Aujourd'hui</a><a class="dz-sp-tab dz-active" href="#">7 jours</a><a class="dz-sp-tab" href="#">30 jours</a></div>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-download"></i> Exporter</a>
  </div>
  <div class="dz-sp-kpis">
    <div class="dz-sp-kpi"><span class="dz-sp-kpi-l"><i class="far fa-comments"></i> Conversations ouvertes</span><b class="dz-sp-kpi-v">128</b><span class="dz-trend dz-trend-down"><i class="fas fa-arrow-up"></i> 14 % vs sem. passée</span></div>
    <div class="dz-sp-kpi"><span class="dz-sp-kpi-l"><i class="fas fa-reply"></i> 1re réponse (médiane)</span><b class="dz-sp-kpi-v">4 min 12 s</b><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-down"></i> 38 s</span></div>
    <div class="dz-sp-kpi"><span class="dz-sp-kpi-l"><i class="fas fa-check-double"></i> Temps de résolution</span><b class="dz-sp-kpi-v">3 h 40</b><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-down"></i> 22 min</span></div>
    <div class="dz-sp-kpi"><span class="dz-sp-kpi-l"><i class="far fa-smile"></i> Satisfaction</span><b class="dz-sp-kpi-v">94 %</b><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 3,2 pts</span></div>
  </div>
  <div class="dz-sp-dgrid">
    <div class="dz-sp-app dz-sp-panel">
      <div class="dz-sp-row"><h4 class="dz-sp-panel-t">Volume de conversations</h4>
        <div class="dz-sp-legend dz-sp-push"><span><i class="dz-sp-lg1"></i> Reçues</span><span><i class="dz-sp-lg2"></i> Résolues</span></div></div>
      <div class="dz-sp-chart">
        <div class="dz-sp-grid"><span>300</span><span>200</span><span>100</span><span>0</span></div>
        <div class="dz-sp-cols">""" + daybar("Jeu", 62, 58) + daybar("Ven", 74, 70) + daybar("Sam", 38, 41) + daybar("Dim", 22, 25) + daybar("Lun", 92, 80) + daybar("Mar", 84, 86) + daybar("Mer", 70, 52, True) + """</div>
      </div>
    </div>
    <div class="dz-sp-app dz-sp-panel">
      <h4 class="dz-sp-panel-t">Par canal</h4>
      <div class="dz-sp-donutwrap">
        <div class="dz-sp-donut"><b>1 486</b><span>conversations</span></div>
        <div class="dz-sp-chlist">
          <div class="dz-sp-chrow">""" + ch("wa") + """<span>WhatsApp</span><b>41 %</b></div>
          <div class="dz-sp-chrow">""" + ch("mail") + """<span>E-mail</span><b>28 %</b></div>
          <div class="dz-sp-chrow">""" + ch("web") + """<span>Chat du site</span><b>23 %</b></div>
          <div class="dz-sp-chrow">""" + ch("sms") + """<span>SMS</span><b>8 %</b></div>
        </div>
      </div>
    </div>
    <div class="dz-sp-app dz-sp-panel">
      <h4 class="dz-sp-panel-t">Respect des SLA</h4>
      <div class="dz-sp-sla-big"><b>92,4 %</b><span>objectif 90 %</span></div>
      <div class="dz-sp-bar dz-sp-bar-lg"><span style="--v:92%"></span></div>
      <div class="dz-sp-slarows">
        <div class="dz-sp-fieldrow"><span><i class="dz-sp-dotc dz-sp-ok"></i> Dans les délais</span><b>1 373</b></div>
        <div class="dz-sp-fieldrow"><span><i class="dz-sp-dotc dz-sp-warn"></i> À risque</span><b>61</b></div>
        <div class="dz-sp-fieldrow"><span><i class="dz-sp-dotc dz-sp-bad"></i> Dépassés</span><b>52</b></div>
      </div>
    </div>
    <div class="dz-sp-app dz-sp-panel">
      <h4 class="dz-sp-panel-t">Heures de pointe</h4>
      <div class="dz-sp-heat">
        <span class="dz-sp-heat-l">Lun</span><i style="--o:.2"></i><i style="--o:.55"></i><i style="--o:.9"></i><i style="--o:.7"></i><i style="--o:.8"></i><i style="--o:.45"></i>
        <span class="dz-sp-heat-l">Mar</span><i style="--o:.15"></i><i style="--o:.6"></i><i style="--o:.75"></i><i style="--o:.65"></i><i style="--o:.95"></i><i style="--o:.4"></i>
        <span class="dz-sp-heat-l">Mer</span><i style="--o:.2"></i><i style="--o:.5"></i><i style="--o:.8"></i><i style="--o:.55"></i><i style="--o:.7"></i><i style="--o:.3"></i>
        <span class="dz-sp-heat-l">Jeu</span><i style="--o:.1"></i><i style="--o:.45"></i><i style="--o:.6"></i><i style="--o:.5"></i><i style="--o:.6"></i><i style="--o:.25"></i>
        <span class="dz-sp-heat-l"></span><span class="dz-sp-heat-x">8 h</span><span class="dz-sp-heat-x">10 h</span><span class="dz-sp-heat-x">12 h</span><span class="dz-sp-heat-x">14 h</span><span class="dz-sp-heat-x">16 h</span><span class="dz-sp-heat-x">18 h</span>
      </div>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 10. Statut des agents
# =====================================================================
def agent(ini, c, pres, name, team, status, st_cls, load, cap, since, msg=""):
    pct = int(100 * load / cap) if cap else 0
    return (
        '<div class="dz-sp-agent">%s'
        '<div class="dz-sp-agent-id"><b>%s</b><span>%s</span></div>'
        '<span class="dz-sp-pres dz-sp-pres-%s">%s</span>'
        '<div class="dz-sp-agent-load"><span class="dz-sp-bar"><span style="--v:%d%%"></span></span><small>%d / %d conversations</small></div>'
        '<span class="dz-sp-agent-since">%s</span>'
        '</div>'
    ) % (av(ini, c, "", pres), name, team + (" · " + msg if msg else ""), st_cls, status, pct, load, cap, since)


BLOCKS.append(dict(
    name="statut des agents",
    icon="fas fa-user-clock",
    html="""
<div class="dz-sp-agents">
  <div class="dz-sp-app dz-sp-agents-list">
    <div class="dz-sp-row dz-sp-agents-head">
      <h3 class="dz-sp-title">Équipe en direct</h3>
      <div class="dz-sp-row dz-sp-push dz-sp-agents-sum">
        <span class="dz-sp-pres dz-sp-pres-on">5 en ligne</span>
        <span class="dz-sp-pres dz-sp-pres-busy">2 occupés</span>
        <span class="dz-sp-pres dz-sp-pres-away">1 absent</span>
      </div>
    </div>
""" + agent("IM", 2, "on", "Inès Morel", "Clients premium", "En ligne", "on", 4, 6, "depuis 3 h 12") \
    + agent("KB", 1, "busy", "Karim Benali", "Livraisons", "Occupé", "busy", 6, 6, "en appel · 18 min", "capacité atteinte") \
    + agent("SL", 5, "on", "Sofia Lemaire", "Avant-vente", "En ligne", "on", 2, 5, "depuis 1 h 40") \
    + agent("TG", 6, "away", "Théo Garnier", "Comptes pros", "Absent", "away", 1, 4, "pause déjeuner · retour 14:30") \
    + agent("AR", 4, "on", "Amandine Roux", "Livraisons", "En ligne", "on", 3, 6, "depuis 52 min") \
    + agent("BN", 3, "off", "Bastien Noël", "Nuit & week-end", "Hors ligne", "off", 0, 5, "reprend à 20:00") + """
  </div>
  <div class="dz-sp-app dz-sp-mystatus">
    <div class="dz-sp-row">""" + av("IM", 2, "lg", "on") + """<div class="dz-sp-agent-id"><b>Inès Morel</b><span>inès@maison-lumen.fr</span></div></div>
    <p class="dz-sp-navlabel">Mon statut</p>
    <a class="dz-sp-opt dz-active" href="#"><i class="dz-sp-dotc dz-sp-ok"></i><span>En ligne</span><small>Reçoit de nouvelles conversations</small><i class="fas fa-check dz-sp-push"></i></a>
    <a class="dz-sp-opt" href="#"><i class="dz-sp-dotc dz-sp-warn"></i><span>Occupé</span><small>Pas de nouvelle assignation</small></a>
    <a class="dz-sp-opt" href="#"><i class="dz-sp-dotc dz-sp-mute"></i><span>Absent</span><small>Pendant 30 min, 1 h, aujourd'hui…</small></a>
    <p class="dz-sp-navlabel">Message d'état</p>
    <p class="dz-sp-textarea">🎧 Focus sur les litiges livraison jusqu'à 16 h</p>
    <div class="dz-sp-fieldrow"><span>Assignation automatique</span><span class="dz-sp-toggle dz-on"></span></div>
    <div class="dz-sp-fieldrow"><span>Sons de notification</span><span class="dz-sp-toggle"></span></div>
  </div>
</div>
""",
))

# =====================================================================
# 11. Tickets avec SLA
# =====================================================================
def ticket(num, subj, req, pri, pri_cls, status, st, who, c, sla, sla_cls, sla_v, chan):
    return (
        '<a class="dz-sp-trow" href="#">'
        '<span class="dz-sp-tnum">%s</span>'
        '<div class="dz-sp-tsubj">%s<div><b>%s</b><span>%s</span></div></div>'
        '<span class="dz-sp-pri dz-sp-pri-%s">%s</span>'
        '<span class="dz-sp-st dz-sp-st-%s">%s</span>'
        '<span class="dz-sp-tassign">%s</span>'
        '<div class="dz-sp-tsla dz-sp-tsla-%s"><span class="dz-sp-tsla-v">%s</span><span class="dz-sp-bar"><span style="--v:%s%%"></span></span></div>'
        '</a>'
    ) % (num, ch(chan), subj, req, pri_cls, pri, st, status, av(who, c, "xs") + "<span>" + {"IM": "Inès M.", "KB": "Karim B.", "SL": "Sofia L.", "TG": "Théo G.", "AR": "Amandine R."}[who] + "</span>", sla_cls, sla, sla_v)


BLOCKS.append(dict(
    name="tickets",
    icon="fas fa-ticket-alt",
    html="""
<div class="dz-sp-app dz-sp-tickets">
  <div class="dz-sp-row dz-sp-tickets-head">
    <h3 class="dz-sp-title">Tickets</h3>
    <div class="dz-sp-tabs">
      <a class="dz-sp-tab dz-active" href="#">SLA à risque <b>7</b></a>
      <a class="dz-sp-tab" href="#">Ouverts <b>64</b></a>
      <a class="dz-sp-tab" href="#">En attente client <b>23</b></a>
      <a class="dz-sp-tab" href="#">Résolus</a>
    </div>
    <a class="dz-btn dz-btn-sm dz-sp-push" href="#"><i class="fas fa-plus"></i> Ticket</a>
  </div>
  <div class="dz-sp-tscroll">
    <div class="dz-sp-ttable">
      <div class="dz-sp-trow dz-sp-thead-row">
        <span>N°</span><span>Sujet</span><span>Priorité</span><span>Statut</span><span>Assigné</span><span>Échéance SLA</span>
      </div>
""" + ticket("#4821", "Colis bloqué en point relais", "Yanis Rahmani", "Urgente", "urgent", "Ouvert", "open", "KB", 1, "Dépassé de 12 min", "late", 100, "wa") \
    + ticket("#4817", "Remboursement non reçu après retour", "Élise Marchand", "Haute", "high", "Ouvert", "open", "AR", 4, "18 min", "soon", 86, "mail") \
    + ticket("#4815", "Abat-jour fêlé à la réception", "Camille Laurent", "Haute", "high", "Ouvert", "open", "IM", 2, "42 min", "soon", 72, "wa") \
    + ticket("#4809", "Erreur de TVA sur facture", "Julien Petit", "Normale", "normal", "En attente", "pending", "IM", 2, "2 h 40", "ok", 38, "mail") \
    + ticket("#4802", "Compatibilité variateur Nébula", "Léa Fontaine", "Basse", "low", "Ouvert", "open", "SL", 5, "6 h 05", "ok", 14, "web") \
    + ticket("#4798", "Modifier l'adresse de livraison", "Marc Olivier", "Normale", "normal", "Ouvert", "open", "TG", 6, "1 h 10", "soon", 64, "sms") + """
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 12. Règle d'automatisation
# =====================================================================
BLOCKS.append(dict(
    name="règle d'automatisation",
    icon="fas fa-project-diagram",
    html="""
<div class="dz-sp-app dz-sp-rule">
  <div class="dz-sp-row dz-sp-rule-head">
    <span class="dz-sp-rule-ic"><i class="fas fa-robot"></i></span>
    <div class="dz-sp-grow"><h3 class="dz-sp-title">Prioriser les clients VIP en attente</h3><p class="dz-sp-rule-sub">Modifiée par Karim Benali le 18 sept. 2026 · déclenchée <b>214 fois</b> en 30 jours</p></div>
    <span class="dz-sp-row dz-sp-rule-on"><span class="dz-sp-toggle dz-on"></span> Active</span>
  </div>
  <div class="dz-sp-flow">
    <div class="dz-sp-step">
      <span class="dz-sp-step-k dz-sp-k-when">Quand</span>
      <div class="dz-sp-step-card"><i class="fas fa-bolt"></i><span>Un message client arrive <b>sans réponse depuis 10 min</b></span></div>
    </div>
    <div class="dz-sp-step">
      <span class="dz-sp-step-k dz-sp-k-if">Si</span>
      <div class="dz-sp-conds">
        <div class="dz-sp-cond"><span class="dz-sp-tok">Contact › Segment</span><span class="dz-sp-op">est</span><span class="dz-sp-val">VIP</span></div>
        <span class="dz-sp-and">ET</span>
        <div class="dz-sp-cond"><span class="dz-sp-tok">Canal</span><span class="dz-sp-op">est l'un de</span><span class="dz-sp-val">WhatsApp</span><span class="dz-sp-val">E-mail</span></div>
        <span class="dz-sp-and">ET</span>
        <div class="dz-sp-cond"><span class="dz-sp-tok">Heure</span><span class="dz-sp-op">pendant</span><span class="dz-sp-val">Heures d'ouverture</span></div>
        <a class="dz-sp-addcond" href="#"><i class="fas fa-plus"></i> Ajouter une condition</a>
      </div>
    </div>
    <div class="dz-sp-step">
      <span class="dz-sp-step-k dz-sp-k-then">Alors</span>
      <div class="dz-sp-actions">
        <div class="dz-sp-action"><span class="dz-sp-action-n">1</span><i class="fas fa-users"></i><span>Assigner à l'équipe <b>Clients premium</b> (au moins chargé)</span></div>
        <div class="dz-sp-action"><span class="dz-sp-action-n">2</span><i class="fas fa-flag"></i><span>Définir la priorité sur <b>Haute</b></span></div>
        <div class="dz-sp-action"><span class="dz-sp-action-n">3</span><i class="fas fa-tag"></i><span>Ajouter l'étiquette <b>VIP en attente</b></span></div>
        <div class="dz-sp-action"><span class="dz-sp-action-n">4</span><i class="far fa-bell"></i><span>Notifier <b>@Karim Benali</b> sur l'appli mobile</span></div>
      </div>
    </div>
  </div>
  <div class="dz-sp-row dz-sp-rule-foot">
    <span class="dz-sp-mute"><i class="fas fa-info-circle"></i> Les règles s'exécutent dans l'ordre ; celle-ci est n° 2 sur 9.</span>
    <a class="dz-btn dz-btn-sm dz-btn-ghost dz-sp-push" href="#">Tester sur une conversation</a>
    <a class="dz-btn dz-btn-sm" href="#">Enregistrer</a>
  </div>
</div>
""",
))

# =====================================================================
# 13. Centre d'aide
# =====================================================================
def cat(icon, title, desc, n, c):
    return '<a class="dz-sp-hcat" href="#"><span class="dz-sp-hcat-ic dz-sp-c%d"><i class="%s"></i></span><b>%s</b><p>%s</p><span class="dz-sp-hcat-n">%s articles <i class="fas fa-arrow-right"></i></span></a>' % (c, icon, title, desc, n)


BLOCKS.append(dict(
    name="centre d'aide",
    icon="far fa-life-ring",
    html="""
<div class="dz-sp-help">
  <div class="dz-sp-hhero">
    <p class="dz-sp-kicker">Centre d'aide Maison Lumen</p>
    <h2 class="dz-sp-hh">Bonjour, comment pouvons-nous vous aider ?</h2>
    <div class="dz-sp-hsearch"><i class="fas fa-search"></i><span>Rechercher : « retour », « ampoule », « facture »…</span><span class="dz-kbd">⌘K</span></div>
    <div class="dz-sp-row dz-sp-hpop"><span>Recherches fréquentes :</span><a href="#">Suivre ma commande</a><a href="#">Délais de livraison</a><a href="#">Garantie 5 ans</a></div>
  </div>
  <div class="dz-sp-hcats">""" + cat("fas fa-truck", "Commandes &amp; livraison", "Suivi, délais, points relais et livraisons abîmées.", 18, 1) \
    + cat("fas fa-undo-alt", "Retours &amp; remboursements", "30 jours pour changer d'avis, étiquette offerte.", 12, 3) \
    + cat("fas fa-lightbulb", "Choisir et installer", "Ampoules, variateurs, fixation au plafond.", 24, 6) \
    + cat("fas fa-shield-alt", "Garantie &amp; SAV", "Pièces détachées et réparations sous 5 ans.", 9, 5) \
    + cat("fas fa-file-invoice", "Paiement &amp; factures", "Moyens de paiement, TVA, paiement en 3 fois.", 11, 4) \
    + cat("fas fa-briefcase", "Espace professionnels", "Remises pro, devis et commandes en volume.", 7, 2) + """</div>
  <div class="dz-sp-hbottom">
    <div class="dz-sp-app dz-sp-hpopular">
      <h3 class="dz-sp-title">Articles populaires</h3>
      <a class="dz-sp-hart" href="#"><i class="far fa-file-alt"></i><span>Comment suivre mon colis en temps réel ?</span><small>2 min</small></a>
      <a class="dz-sp-hart" href="#"><i class="far fa-file-alt"></i><span>Mon article est arrivé abîmé : que faire ?</span><small>3 min</small></a>
      <a class="dz-sp-hart" href="#"><i class="far fa-file-alt"></i><span>Quelle ampoule choisir pour une lampe à variateur ?</span><small>4 min</small></a>
      <a class="dz-sp-hart" href="#"><i class="far fa-file-alt"></i><span>Retourner un article : étapes et délais</span><small>2 min</small></a>
    </div>
    <div class="dz-sp-app dz-sp-hcontact">
      <div class="dz-avatars">""" + av("IM", 2, "sm") + av("SL", 5, "sm") + av("KB", 1, "sm") + """</div>
      <h3 class="dz-sp-title">Vous ne trouvez pas ?</h3>
      <p class="dz-sp-res-sub">Notre équipe répond en moyenne en <b>4 min</b>, du lundi au samedi.</p>
      <a class="dz-btn dz-btn-sm" href="#"><i class="far fa-comment-dots"></i> Discuter avec nous</a>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 14. Article d'aide
# =====================================================================
BLOCKS.append(dict(
    name="article d'aide",
    icon="far fa-file-alt",
    html="""
<div class="dz-sp-art">
  <aside class="dz-sp-art-toc">
    <p class="dz-sp-navlabel">Dans cet article</p>
    <a class="dz-sp-toc dz-active" href="#">Avant de commencer</a>
    <a class="dz-sp-toc" href="#">1. Déclarer le dommage</a>
    <a class="dz-sp-toc" href="#">2. Choisir la solution</a>
    <a class="dz-sp-toc" href="#">3. Recevoir le remplacement</a>
    <a class="dz-sp-toc" href="#">Questions fréquentes</a>
  </aside>
  <article class="dz-sp-art-body">
    <p class="dz-sp-crumb"><a href="#">Centre d'aide</a><i class="fas fa-chevron-right"></i><a href="#">Commandes &amp; livraison</a><i class="fas fa-chevron-right"></i><span>Article abîmé</span></p>
    <h2 class="dz-sp-hh">Mon article est arrivé abîmé : que faire ?</h2>
    <div class="dz-sp-row dz-sp-art-meta">""" + av("SL", 5, "sm") + """<span>Par <b>Sofia Lemaire</b> · mis à jour le 12 sept. 2026 · 3 min de lecture</span></div>
    <p class="dz-sp-art-lead">Pas d'inquiétude : chaque luminaire est assuré pendant le transport. Vous n'avez rien à avancer et, dans la plupart des cas, vous n'avez même pas besoin de nous renvoyer le produit.</p>
    <div class="dz-callout dz-callout-warning"><p class="dz-sp-art-call"><b>Important :</b> signalez le dommage dans les <b>7 jours</b> suivant la livraison et gardez l'emballage d'origine jusqu'à la clôture du dossier.</p></div>
    <h3 class="dz-sp-art-h">1. Déclarer le dommage</h3>
    <div class="dz-sp-steps">
      <div class="dz-sp-stepl"><span>1</span><p>Prenez <b>2 ou 3 photos</b> : le produit, l'emballage et l'étiquette du colis.</p></div>
      <div class="dz-sp-stepl"><span>2</span><p>Ouvrez <b>Mon compte › Commandes</b>, puis « Signaler un problème » sur la commande concernée.</p></div>
      <div class="dz-sp-stepl"><span>3</span><p>Joignez vos photos : un conseiller vous répond en moins d'une heure ouvrée.</p></div>
    </div>
    <figure class="dz-sp-fig"><img class="dz-cover" src="https://picsum.photos/seed/colis-lumen/960/420" alt="Déclaration d'un colis abîmé depuis l'espace client"><figcaption class="dz-sp-figcap">Le bouton « Signaler un problème » dans votre espace client.</figcaption></figure>
    <div class="dz-sp-helpful">
      <b>Cet article vous a-t-il aidé ?</b>
      <div class="dz-sp-row"><a class="dz-sp-reason" href="#"><i class="far fa-thumbs-up"></i> Oui</a><a class="dz-sp-reason" href="#"><i class="far fa-thumbs-down"></i> Non</a></div>
      <span class="dz-sp-mute">412 personnes ont trouvé cet article utile</span>
    </div>
  </article>
</div>
""",
))

# =====================================================================
# 15. Étiquettes et équipes
# =====================================================================
def label(name, t, desc, n):
    return '<div class="dz-sp-lab"><span class="dz-sp-lab-sw dz-sp-t%d"></span><div class="dz-sp-lab-t"><b>%s</b><span>%s</span></div><span class="dz-sp-lab-n">%s</span><a class="dz-sp-ib" href="#" aria-label="Modifier"><i class="fas fa-pen"></i></a></div>' % (t, name, desc, n)


def team(icon, c, name, desc, members, open_, hours, auto):
    return (
        '<div class="dz-sp-team">'
        '<div class="dz-sp-row"><span class="dz-sp-team-ic dz-sp-c%d"><i class="%s"></i></span><div class="dz-sp-grow"><b>%s</b><span class="dz-sp-team-d">%s</span></div></div>'
        '<div class="dz-sp-row"><div class="dz-avatars">%s</div><span class="dz-sp-mute dz-sp-push">%d ouvertes</span></div>'
        '<div class="dz-sp-team-foot"><span><i class="far fa-clock"></i> %s</span><span class="dz-sp-row"><span class="dz-sp-toggle%s"></span> Auto</span></div>'
        '</div>'
    ) % (c, icon, name, desc, members, open_, hours, " dz-on" if auto else "")


BLOCKS.append(dict(
    name="étiquettes et équipes",
    icon="fas fa-tags",
    html="""
<div class="dz-sp-lt">
  <div class="dz-sp-app dz-sp-labels">
    <div class="dz-sp-row"><h3 class="dz-sp-title">Étiquettes</h3><span class="dz-sp-pill">12</span><a class="dz-btn dz-btn-sm dz-btn-ghost dz-sp-push" href="#"><i class="fas fa-plus"></i> Nouvelle</a></div>
""" + label("Livraison", 1, "Retards, suivi, point relais", "486") + label("Facturation", 2, "Factures, TVA, avoirs", "213") + label("Casse transport", 3, "Colis abîmés à la réception", "97") + label("Avant-vente", 4, "Questions avant achat", "342") + label("Urgent", 5, "À traiter en priorité", "38") + label("Retour", 6, "Demandes de retour sous 30 jours", "154") + """
  </div>
  <div class="dz-sp-teams">
    <div class="dz-sp-row"><h3 class="dz-sp-title">Équipes</h3><a class="dz-sp-link dz-sp-push" href="#">Gérer</a></div>
    <div class="dz-sp-teamgrid">""" + team("fas fa-crown", 3, "Clients premium", "VIP et comptes pros", av("IM", 2, "sm") + av("TG", 6, "sm"), 14, "9 h – 19 h", True) \
    + team("fas fa-truck", 1, "Livraisons", "Suivi, casse, relais", av("KB", 1, "sm") + av("AR", 4, "sm") + av("BN", 3, "sm"), 41, "8 h – 20 h", True) \
    + team("fas fa-lightbulb", 6, "Avant-vente", "Conseil produit", av("SL", 5, "sm") + av("IM", 2, "sm"), 9, "9 h – 18 h", False) \
    + team("fas fa-moon", 4, "Nuit &amp; week-end", "Astreinte", av("BN", 3, "sm"), 3, "20 h – 8 h", True) + """</div>
  </div>
</div>
""",
))

# =====================================================================
# 16. Boîtes de réception par canal
# =====================================================================
def inbox(kind, name, addr, open_, resp, members, state="ok", state_l="Connecté"):
    return (
        '<a class="dz-sp-ibox" href="#">'
        '<div class="dz-sp-row">%s<span class="dz-sp-ibox-st dz-sp-ibox-%s">%s</span></div>'
        '<b class="dz-sp-ibox-n">%s</b><span class="dz-sp-ibox-a">%s</span>'
        '<div class="dz-sp-ibox-stats"><div><b>%s</b><span>ouvertes</span></div><div><b>%s</b><span>1re réponse</span></div></div>'
        '<div class="dz-sp-row"><div class="dz-avatars">%s</div><span class="dz-sp-link dz-sp-push">Réglages <i class="fas fa-arrow-right"></i></span></div>'
        '</a>'
    ) % (ch(kind).replace("dz-sp-ch ", "dz-sp-ch dz-sp-ch-lg "), state, state_l, name, addr, open_, resp, members)


BLOCKS.append(dict(
    name="boîtes par canal",
    icon="fas fa-inbox",
    html="""
<div class="dz-sp-inboxes">
  <div class="dz-sp-row dz-sp-dash-head">
    <div><h3 class="dz-sp-h">Boîtes de réception</h3><p class="dz-sp-res-sub">Chaque canal arrive dans la même boîte partagée, avec ses propres règles et horaires.</p></div>
    <a class="dz-btn dz-btn-sm dz-sp-push" href="#"><i class="fas fa-plus"></i> Connecter un canal</a>
  </div>
  <div class="dz-sp-iboxes">""" + inbox("web", "Chat du site", "maison-lumen.fr · widget", 38, "2 min", av("SL", 5, "sm") + av("IM", 2, "sm") + av("AR", 4, "sm")) \
    + inbox("mail", "Service client", "bonjour@maison-lumen.fr", 52, "38 min", av("KB", 1, "sm") + av("IM", 2, "sm")) \
    + inbox("wa", "WhatsApp", "+33 4 78 60 21 90 · vérifié", 29, "4 min", av("IM", 2, "sm") + av("KB", 1, "sm") + av("TG", 6, "sm")) \
    + inbox("sms", "SMS livraison", "+33 6 44 02 18 55", 9, "12 min", av("AR", 4, "sm"), "warn", "Crédits : 8 %") + """
    <a class="dz-sp-ibox dz-sp-ibox-add" href="#"><span class="dz-sp-ibox-plus"><i class="fas fa-plus"></i></span><b>Ajouter une boîte</b><span class="dz-sp-ibox-a">Formulaire, réseau social, API…</span></a>
  </div>
</div>
""",
))

# =====================================================================
# 17. Notification d'assignation
# =====================================================================
BLOCKS.append(dict(
    name="notification d'assignation",
    icon="far fa-bell",
    html="""
<div class="dz-sp-nstage">
  <div class="dz-sp-toast dz-sp-toast-main">
    <div class="dz-sp-toast-head"><span class="dz-sp-toast-ic"><i class="fas fa-user-check"></i></span><b>Nouvelle conversation pour vous</b><time>à l'instant</time><a class="dz-sp-ib" href="#" aria-label="Fermer"><i class="fas fa-times"></i></a></div>
    <div class="dz-sp-toast-body">
      """ + avch("YR", 3, "wa") + """
      <div class="dz-sp-grow"><b>Yanis Rahmani</b><p>« Colis bloqué en relais depuis 6 jours, le point relais dit ne rien avoir reçu… »</p>
        <div class="dz-sp-row">""" + tag("Livraison", 1) + tag("Urgent", 5) + """<span class="dz-sp-sla dz-sp-sla-soon"><i class="fas fa-hourglass-half"></i> Répondre sous 15 min</span></div>
      </div>
    </div>
    <div class="dz-sp-toast-act"><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Plus tard</a><a class="dz-btn dz-btn-sm" href="#">Ouvrir la conversation <span class="dz-kbd">O</span></a></div>
    <span class="dz-sp-toast-timer"></span>
  </div>
  <div class="dz-sp-toast dz-sp-toast-mini">
    <span class="dz-sp-toast-ic dz-sp-c3"><i class="fas fa-at"></i></span>
    <p><b>Karim Benali</b> vous a mentionnée dans une note sur <b>#C-48213</b></p>
    <time>2 min</time>
  </div>
  <div class="dz-sp-toast dz-sp-toast-mini">
    <span class="dz-sp-toast-ic dz-sp-c7"><i class="fas fa-fire"></i></span>
    <p>SLA dépassé : <b>#4821</b> attend une réponse depuis 27 min</p>
    <time>5 min</time>
  </div>
</div>
""",
))

# =====================================================================
# 18. Macros
# =====================================================================
def macro(icon, c, name, steps, uses, active=False):
    chips = "".join('<span class="dz-sp-mstep"><i class="%s"></i> %s</span>' % s for s in steps)
    return '<div class="dz-sp-macro%s"><span class="dz-sp-team-ic dz-sp-c%d"><i class="%s"></i></span><div class="dz-sp-grow"><b>%s</b><div class="dz-sp-msteps">%s</div></div><span class="dz-sp-mute">%s</span><a class="dz-btn dz-btn-sm dz-btn-soft" href="#"><i class="fas fa-play"></i> Lancer</a></div>' % (" dz-active" if active else "", c, icon, name, chips, uses)


BLOCKS.append(dict(
    name="macros",
    icon="fas fa-magic",
    html="""
<div class="dz-sp-app dz-sp-macros">
  <div class="dz-sp-row dz-sp-macros-head">
    <div class="dz-sp-grow"><h3 class="dz-sp-title">Macros</h3><p class="dz-sp-res-sub">Enchaînez plusieurs actions en un clic, depuis n'importe quelle conversation.</p></div>
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouvelle macro</a>
  </div>
""" + macro("fas fa-box-open", 3, "Colis abîmé → remplacement express", [("fas fa-tag", "Étiquette Casse transport"), ("fas fa-reply", "Réponse /casse"), ("fas fa-flag", "Priorité haute"), ("fas fa-check", "Résoudre")], "342 ×", True) \
    + macro("fas fa-undo-alt", 1, "Retour accepté", [("fas fa-reply", "Réponse /retour-ok"), ("fas fa-paperclip", "Joindre l'étiquette"), ("far fa-clock", "Reporter 5 jours")], "218 ×") \
    + macro("fas fa-user-tie", 6, "Transférer aux comptes pros", [("fas fa-users", "Équipe Comptes pros"), ("fas fa-lock", "Note privée"), ("fas fa-tag", "Étiquette Pro")], "96 ×") \
    + macro("fas fa-moon", 4, "Hors horaires", [("fas fa-reply", "Réponse /demain"), ("far fa-clock", "Reporter à 9 h")], "57 ×") + """
  <div class="dz-sp-mrun"><i class="fas fa-check-circle"></i><span>Macro « Colis abîmé » appliquée à <b>#C-48213</b> : 4 actions effectuées.</span><a class="dz-sp-link dz-sp-push" href="#">Annuler</a></div>
</div>
""",
))

# =====================================================================
# 19. Historique d'un contact
# =====================================================================
def ev(icon, c, title, detail, time, extra=""):
    return '<div class="dz-sp-ev"><span class="dz-sp-ev-ic dz-sp-c%d"><i class="%s"></i></span><div class="dz-sp-ev-b"><div class="dz-sp-ev-top"><b>%s</b><time>%s</time></div><p>%s</p>%s</div></div>' % (c, icon, title, time, detail, extra)


BLOCKS.append(dict(
    name="historique du contact",
    icon="fas fa-history",
    html="""
<div class="dz-sp-app dz-sp-hist">
  <div class="dz-sp-row dz-sp-hist-head">
    """ + av("CL", 1, "", "on") + """
    <div class="dz-sp-grow"><h3 class="dz-sp-title">Historique de Camille Laurent</h3><p class="dz-sp-res-sub">Client depuis mars 2023 · 43 événements</p></div>
    <div class="dz-sp-tabs"><a class="dz-sp-tab dz-active" href="#">Tout</a><a class="dz-sp-tab" href="#">Conversations</a><a class="dz-sp-tab" href="#">Commandes</a><a class="dz-sp-tab" href="#">Notes</a></div>
  </div>
  <div class="dz-sp-tl">
    <p class="dz-sp-tl-day">Aujourd'hui</p>
""" + ev("fab fa-whatsapp", 5, "Conversation WhatsApp ouverte", "« J'ai reçu ma commande #ML-20418 mais l'abat-jour est fêlé »", "14:12", '<div class="dz-sp-row">' + tag("Casse transport", 3) + '<span class="dz-sp-st dz-sp-st-open">Ouverte</span></div>') \
    + ev("fas fa-truck", 4, "Commande #ML-20418 livrée", "Colissimo Pro · signée par C. Laurent", "09:47") + """
    <p class="dz-sp-tl-day">12 septembre 2026</p>
""" + ev("fas fa-shopping-bag", 1, "Commande #ML-20418 passée", "Lampe Orbe, 2 appliques Halo · <b>389,00 €</b> · code PRO12", "18:30") \
    + ev("far fa-eye", 6, "A consulté 6 pages", "Suspension Nébula, Lampe Orbe, Guide des ampoules…", "18:12") + """
    <p class="dz-sp-tl-day">28 août 2026</p>
""" + ev("fas fa-star", 6, "Avis de satisfaction : 5/5", "« Devis reçu en une heure, parfait pour mon chantier. »", "16:05", '<div class="dz-sp-row">' + av("TG", 6, "xs") + '<span class="dz-sp-mute">Théo Garnier</span></div>') \
    + ev("fas fa-lock", 3, "Note privée de Théo Garnier", "Accord remise pro 12 % validé par la direction pour 2026.", "15:40") + """
  </div>
</div>
""",
))

# =====================================================================
# 20. File d'attente en direct
# =====================================================================
def q(ini, c, kind, name, msg, wait, cls, pct, pos):
    return '<div class="dz-sp-q"><span class="dz-sp-q-pos">%s</span>%s<div class="dz-sp-q-b"><b>%s</b><p>%s</p></div><div class="dz-sp-q-wait dz-sp-tsla-%s"><b>%s</b><span class="dz-sp-bar"><span style="--v:%s%%"></span></span></div><a class="dz-btn dz-btn-sm dz-btn-soft" href="#">Prendre</a></div>' % (pos, avch(ini, c, kind), name, msg, cls, wait, pct)


BLOCKS.append(dict(
    name="file d'attente",
    icon="fas fa-users",
    html="""
<div class="dz-sp-app dz-sp-queue">
  <div class="dz-sp-queue-head">
    <div class="dz-sp-row"><span class="dz-sp-live-dot"></span><h3 class="dz-sp-title">File d'attente en direct</h3><span class="dz-sp-pill">5 en attente</span></div>
    <div class="dz-sp-qstats">
      <div><span>Attente moyenne</span><b>3 min 48 s</b></div>
      <div><span>Plus longue</span><b class="dz-sp-bad-t">11 min 02 s</b></div>
      <div><span>Agents disponibles</span><b>3 / 8</b></div>
      <div><span>Abandons aujourd'hui</span><b>2,1 %</b></div>
    </div>
  </div>
""" + q("YR", 3, "wa", "Yanis Rahmani", "Colis bloqué en relais depuis 6 jours…", "11:02", "late", 100, 1) \
    + q("EM", 4, "web", "Élise Marchand", "Bonjour, mon remboursement n'est toujours pas arrivé", "6:40", "soon", 70, 2) \
    + q("PG", 6, "web", "Paul Guérin", "Visiteur · page Lampe Orbe · « Livrez-vous en Belgique ? »", "2:15", "ok", 30, 3) \
    + q("AB", 1, "sms", "Aurélie Barbier", "OK pour jeudi, pouvez-vous confirmer le créneau ?", "0:52", "ok", 10, 4) + """
</div>
""",
))
