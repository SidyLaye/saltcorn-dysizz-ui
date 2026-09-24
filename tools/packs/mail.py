"""Famille « Mail » : lecture et rédaction d'e-mails (préfixe CSS dz-ml-)."""
FAMILY = "mail"


def av(ini, c=1, size=""):
    return '<span class="dz-ml-av dz-ml-c%d%s">%s</span>' % (c, " dz-ml-av-" + size if size else "", ini)


def lab(label, t=1):
    return '<span class="dz-ml-lab dz-ml-t%d">%s</span>' % (t, label)


def row(ini, c, sender, subject, prev, time, unread=False, star=False, labels="", clip=False, active=False, count="", thumb=""):
    cls = "dz-ml-row"
    if unread:
        cls += " dz-ml-unread"
    if active:
        cls += " dz-active"
    return (
        '<a class="%s" href="#">'
        '<span class="dz-ml-star%s"><i class="%s fa-star"></i></span>'
        '%s'
        '<div class="dz-ml-row-b">'
        '<div class="dz-ml-row-top"><b class="dz-ml-from">%s%s</b>%s<time class="dz-ml-time">%s</time></div>'
        '<p class="dz-ml-subj"><b>%s</b><span> — %s</span></p>'
        '%s'
        '</div>'
        '<span class="dz-ml-hover"><i class="fas fa-archive"></i><i class="far fa-trash-alt"></i><i class="far fa-envelope-open"></i><i class="far fa-clock"></i></span>'
        '</a>'
    ) % (cls, " dz-on" if star else "", "fas" if star else "far", av(ini, c), sender,
         ' <span class="dz-ml-cnt">%s</span>' % count if count else "",
         '<i class="fas fa-paperclip dz-ml-clip"></i>' if clip else "", time, subject, prev,
         ('<div class="dz-ml-row-labs">%s%s</div>' % (labels, thumb)) if (labels or thumb) else "")


def folder(icon, name, n="", active=False, dot=""):
    return '<a class="dz-ml-fold-i%s" href="#"><i class="%s"></i><span>%s</span>%s</a>' % (
        " dz-active" if active else "", icon, name, ('<b>%s</b>' % n) if n else "")


def chip(ext, name, size, kind):
    return '<a class="dz-ml-att" href="#"><span class="dz-ml-att-ic dz-ml-f-%s">%s</span><span class="dz-ml-att-t"><b>%s</b><small>%s</small></span><i class="fas fa-download"></i></a>' % (kind, ext, name, size)


BLOCKS = []

# =====================================================================
# 1. Client mail 3 volets
# =====================================================================
BLOCKS.append(dict(
    name="client mail",
    icon="fas fa-envelope-open-text",
    html="""
<div class="dz-ml-app dz-ml-client">
  <aside class="dz-ml-folders">
    <a class="dz-btn dz-btn-sm dz-btn-block dz-ml-compose" href="#"><i class="fas fa-pen"></i> Nouveau message</a>
    """ + folder("fas fa-inbox", "Boîte de réception", "12", True) + folder("far fa-star", "Suivis", "3") + folder("far fa-clock", "En attente", "2") + folder("far fa-paper-plane", "Envoyés") + folder("far fa-file", "Brouillons", "4") + folder("fas fa-archive", "Archives") + folder("far fa-trash-alt", "Corbeille") + """
    <p class="dz-ml-flabel">Libellés</p>
    <a class="dz-ml-fold-i" href="#"><i class="dz-ml-sw dz-ml-t1"></i><span>Clients</span><b>5</b></a>
    <a class="dz-ml-fold-i" href="#"><i class="dz-ml-sw dz-ml-t2"></i><span>Factures</span></a>
    <a class="dz-ml-fold-i" href="#"><i class="dz-ml-sw dz-ml-t3"></i><span>Projet Orbe</span><b>2</b></a>
    <a class="dz-ml-fold-i" href="#"><i class="dz-ml-sw dz-ml-t4"></i><span>Newsletters</span></a>
    <div class="dz-ml-quota"><div class="dz-ml-row2"><span>Stockage</span><b>8,4 Go / 15 Go</b></div><span class="dz-ml-bar"><span style="--v:56%"></span></span></div>
  </aside>
  <section class="dz-ml-listpane">
    <div class="dz-ml-lp-head">
      <div class="dz-ml-search"><i class="fas fa-search"></i><span>Rechercher dans les messages</span><span class="dz-kbd">/</span></div>
      <div class="dz-ml-row2"><b class="dz-ml-lp-t">Boîte de réception</b><a class="dz-ml-ib" href="#" aria-label="Actualiser"><i class="fas fa-redo-alt"></i></a><a class="dz-ml-ib" href="#" aria-label="Filtrer"><i class="fas fa-filter"></i></a></div>
    </div>
    <div class="dz-ml-rows">
      <p class="dz-ml-group">Aujourd'hui</p>
""" + row("PG", 1, "Paul Garnier", "Maquettes v3 validées ✔", "On part sur la version B pour la page d'accueil, bravo à toute l'équipe !", "10:42", True, True, lab("Projet Orbe", 3), True, True, "3") \
    + row("NX", 2, "Nexora Facturation", "Votre facture de septembre", "Montant : 249,00 € TTC — prélèvement le 30/09/2026.", "09:15", True, False, lab("Factures", 2), True) \
    + row("JL", 4, "Julie Lambert", "Déjeuner jeudi ?", "Je serai à Lyon toute la journée, ça te dit un déjeuner près de Bellecour ?", "08:03") + """
      <p class="dz-ml-group">Hier</p>
""" + row("LF", 5, "Le Fil Vert", "5 plantes qui adorent l'ombre", "Notre sélection d'automne, et -15 % sur les jardinières jusqu'à dimanche.", "Hier", labels=lab("Newsletters", 4)) \
    + row("TM", 6, "Thomas Mercier", "Contrat de prestation — signature", "Voici la version finale avec les modifications de l'article 7.", "Hier", star=True, clip=True) + """
    </div>
  </section>
  <article class="dz-ml-read">
    <div class="dz-ml-rtool">
      <a class="dz-ml-ib" href="#" aria-label="Archiver"><i class="fas fa-archive"></i></a>
      <a class="dz-ml-ib" href="#" aria-label="Supprimer"><i class="far fa-trash-alt"></i></a>
      <a class="dz-ml-ib" href="#" aria-label="Marquer comme non lu"><i class="far fa-envelope"></i></a>
      <a class="dz-ml-ib" href="#" aria-label="Mettre en attente"><i class="far fa-clock"></i></a>
      <a class="dz-ml-ib" href="#" aria-label="Déplacer"><i class="far fa-folder"></i></a>
      <span class="dz-ml-rtool-n">1 sur 12</span>
      <a class="dz-ml-ib" href="#" aria-label="Précédent"><i class="fas fa-chevron-up"></i></a>
      <a class="dz-ml-ib" href="#" aria-label="Suivant"><i class="fas fa-chevron-down"></i></a>
    </div>
    <div class="dz-ml-rbody">
      <h3 class="dz-ml-rsubj">Maquettes v3 validées ✔</h3>
      <div class="dz-ml-row2 dz-ml-rlabs">""" + lab("Projet Orbe", 3) + lab("Boîte de réception", 0) + """</div>
      <div class="dz-ml-hdr">""" + av("PG", 1, "md") + """
        <div class="dz-ml-hdr-id"><p class="dz-ml-hdr-from"><b>Paul Garnier</b><span>paul@nexora.fr</span></p><p class="dz-ml-hdr-to">À moi, Hugo Mercier · Cc : Léa Fontaine</p></div>
        <time class="dz-ml-hdr-date">Aujourd'hui, 10:42</time>
      </div>
      <div class="dz-ml-content">
        <p>Bonjour Clara,</p>
        <p>Merci pour la présentation de ce matin. Après discussion avec la direction, on part sur la <b>version B</b> pour la page d'accueil : le hero plein écran et la grille produits en trois colonnes ont fait l'unanimité.</p>
        <p>Deux petits ajustements avant la mise en production :</p>
        <ul class="dz-ml-ul"><li>passer le bouton principal en « Découvrir la collection » ;</li><li>remonter le bloc avis clients juste sous le hero.</li></ul>
        <p>Bravo à toute l'équipe,<br>Paul</p>
      </div>
      <div class="dz-ml-atts">""" + chip("FIG", "accueil-v3-B.fig", "12,4 Mo", "fig") + chip("PDF", "retours-direction.pdf", "860 Ko", "pdf") + """</div>
      <div class="dz-ml-quick">
        <a class="dz-ml-qbtn" href="#"><i class="fas fa-reply"></i> Répondre</a>
        <a class="dz-ml-qbtn" href="#"><i class="fas fa-reply-all"></i> Répondre à tous</a>
        <a class="dz-ml-qbtn" href="#"><i class="fas fa-share"></i> Transférer</a>
      </div>
    </div>
  </article>
</div>
""",
))

# =====================================================================
# 2. Liste de mails riche
# =====================================================================
BLOCKS.append(dict(
    name="liste de mails",
    icon="fas fa-list",
    html="""
<div class="dz-ml-app dz-ml-listcard">
  <div class="dz-ml-lc-head">
    <span class="dz-ml-check"></span>
    <a class="dz-ml-ib" href="#" aria-label="Actualiser"><i class="fas fa-redo-alt"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Plus"><i class="fas fa-ellipsis-v"></i></a>
    <div class="dz-ml-tabs">
      <a class="dz-ml-tab dz-active" href="#"><i class="fas fa-inbox"></i> Principale <b>8</b></a>
      <a class="dz-ml-tab" href="#"><i class="fas fa-tag"></i> Promotions <b>23</b></a>
      <a class="dz-ml-tab" href="#"><i class="far fa-bell"></i> Notifications</a>
    </div>
    <span class="dz-ml-pager">1–50 sur 1 284</span>
  </div>
  <div class="dz-ml-rows dz-ml-wide">
    <p class="dz-ml-group">Aujourd'hui</p>
""" + row("PG", 1, "Paul Garnier", "Maquettes v3 validées ✔", "On part sur la version B pour la page d'accueil, bravo à toute l'équipe !", "10:42", True, True, lab("Projet Orbe", 3), True, count="3") \
    + row("NX", 2, "Nexora Facturation", "Votre facture de septembre", "Montant : 249,00 € TTC — prélèvement le 30/09/2026.", "09:15", True, False, lab("Factures", 2), True) \
    + row("SB", 3, "Sarah Benali", "Photos du shooting", "Voici la sélection retouchée, dis-moi lesquelles tu gardes pour la newsletter.", "08:47", True, False, lab("Clients", 1), False, thumb='<span class="dz-ml-thumbs"><span class="dz-ml-thumb"><img class="dz-cover" src="https://picsum.photos/seed/shoot1/80/80" alt=""></span><span class="dz-ml-thumb"><img class="dz-cover" src="https://picsum.photos/seed/shoot2/80/80" alt=""></span><span class="dz-ml-thumb dz-ml-thumb-more">+14</span></span>') \
    + row("JL", 4, "Julie Lambert", "Déjeuner jeudi ?", "Je serai à Lyon toute la journée, ça te dit un déjeuner près de Bellecour ?", "08:03") + """
    <p class="dz-ml-group">Hier</p>
""" + row("TM", 6, "Thomas Mercier", "Contrat de prestation — signature", "Voici la version finale avec les modifications de l'article 7.", "Hier", star=True, clip=True, labels=lab("Clients", 1)) \
    + row("AR", 5, "Amandine Roux", "Re : Planning d'octobre", "Ça me va pour le 14, je bloque la salle de réunion.", "Hier", count="5") + """
    <p class="dz-ml-group">Cette semaine</p>
""" + row("BQ", 2, "Banque Horizon", "Votre relevé est disponible", "Votre relevé de compte de septembre 2026 est consultable dans votre espace.", "lun.") + """
  </div>
</div>
""",
))

# =====================================================================
# 3. Lecture d'un mail
# =====================================================================
BLOCKS.append(dict(
    name="lecture d'un mail",
    icon="far fa-envelope-open",
    html="""
<article class="dz-ml-app dz-ml-reader">
  <div class="dz-ml-rtool">
    <a class="dz-ml-ib" href="#" aria-label="Retour"><i class="fas fa-arrow-left"></i></a>
    <span class="dz-ml-sep"></span>
    <a class="dz-ml-ib" href="#" aria-label="Archiver"><i class="fas fa-archive"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Signaler"><i class="fas fa-exclamation-circle"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Supprimer"><i class="far fa-trash-alt"></i></a>
    <span class="dz-ml-sep"></span>
    <a class="dz-ml-ib" href="#" aria-label="Mettre en attente"><i class="far fa-clock"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Libellé"><i class="fas fa-tag"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Imprimer"><i class="fas fa-print"></i></a>
    <span class="dz-ml-rtool-n">3 sur 1 284</span>
  </div>
  <div class="dz-ml-rbody">
    <div class="dz-ml-row2 dz-ml-rs">
      <h2 class="dz-ml-rsubj dz-ml-rsubj-lg">Contrat de prestation — version finale à signer</h2>
      """ + lab("Clients", 1) + """
      <a class="dz-ml-ib dz-ml-push" href="#" aria-label="Suivre"><i class="fas fa-star dz-ml-staron"></i></a>
    </div>
    <div class="dz-ml-hdr">""" + av("TM", 6, "md") + """
      <div class="dz-ml-hdr-id">
        <p class="dz-ml-hdr-from"><b>Thomas Mercier</b><span>&lt;thomas.mercier@atelier-lune.fr&gt;</span><span class="dz-ml-verified"><i class="fas fa-check-circle"></i> Vérifié</span></p>
        <p class="dz-ml-hdr-to">À : Clara Vasseur · Cc : compta@studio-brume.fr</p>
      </div>
      <div class="dz-ml-hdr-r">
        <time class="dz-ml-hdr-date">mar. 22 sept. 2026, 17:08</time>
        <div class="dz-ml-row2"><a class="dz-ml-ib" href="#" aria-label="Répondre"><i class="fas fa-reply"></i></a><a class="dz-ml-ib" href="#" aria-label="Plus"><i class="fas fa-ellipsis-v"></i></a></div>
      </div>
    </div>
    <div class="dz-ml-htmlmail">
      <div class="dz-ml-hm-brand"><span class="dz-ml-hm-logo"><i class="fas fa-moon"></i></span><b>Atelier Lune</b><span>Architecture intérieure</span></div>
      <p>Bonjour Clara,</p>
      <p>Comme convenu lors de notre appel, vous trouverez ci-joint la version finale du contrat de prestation pour la refonte du site. J'ai intégré vos remarques sur <b>l'article 7</b> (propriété des maquettes) et sur l'échéancier de paiement :</p>
      <div class="dz-ml-hm-table">
        <div><span>Acompte à la signature</span><b>3 600 €</b></div>
        <div><span>Livraison des maquettes</span><b>4 800 €</b></div>
        <div><span>Mise en ligne</span><b>3 600 €</b></div>
        <div class="dz-ml-hm-total"><span>Total HT</span><b>12 000 €</b></div>
      </div>
      <p>Si tout vous convient, il vous suffit de signer électroniquement avant le <b>30 septembre</b>.</p>
      <a class="dz-ml-hm-cta" href="#">Signer le contrat</a>
      <p class="dz-ml-sig">Belle soirée,<br><b>Thomas Mercier</b><br><span>Associé · Atelier Lune · +33 4 72 18 90 44</span></p>
    </div>
    <div class="dz-ml-attzone">
      <p class="dz-ml-attzone-h"><b>3 pièces jointes</b> · 4,7 Mo <a class="dz-ml-link" href="#">Tout télécharger</a></p>
      <div class="dz-ml-previews">
        <a class="dz-ml-pv" href="#"><span class="dz-ml-pv-img dz-ml-pv-doc"><span class="dz-ml-pv-line" style="--w:70%"></span><span class="dz-ml-pv-line" style="--w:90%"></span><span class="dz-ml-pv-line" style="--w:80%"></span><span class="dz-ml-pv-line" style="--w:60%"></span><span class="dz-ml-pv-line" style="--w:85%"></span></span><span class="dz-ml-pv-cap"><i class="fas fa-file-pdf dz-ml-f-pdf-t"></i><span>contrat-final.pdf</span></span></a>
        <a class="dz-ml-pv" href="#"><span class="dz-ml-pv-img"><img class="dz-cover" src="https://picsum.photos/seed/salon-lune/320/200" alt="Aperçu salon"></span><span class="dz-ml-pv-cap"><i class="fas fa-file-image dz-ml-f-img-t"></i><span>moodboard.jpg</span></span></a>
        <a class="dz-ml-pv" href="#"><span class="dz-ml-pv-img dz-ml-pv-sheet"><span class="dz-ml-pv-grid"></span></span><span class="dz-ml-pv-cap"><i class="fas fa-file-excel dz-ml-f-xls-t"></i><span>echeancier.xlsx</span></span></a>
      </div>
    </div>
    <div class="dz-ml-replybox"><i class="fas fa-reply"></i><span>Répondre à Thomas Mercier…</span><span class="dz-ml-sugg">Parfait, je signe ce soir !</span><span class="dz-ml-sugg">Merci Thomas 🙏</span></div>
  </div>
</article>
""",
))

# =====================================================================
# 4. Fil de discussion replié / déplié
# =====================================================================
def folded(ini, c, name, prev, date):
    return '<details class="dz-ml-msgf"><summary class="dz-ml-msgf-s">%s<b>%s</b><span class="dz-ml-msgf-p">%s</span><time>%s</time></summary><p class="dz-ml-msgf-body">%s</p></details>' % (av(ini, c, "sm"), name, prev, date, prev)


BLOCKS.append(dict(
    name="fil de discussion",
    icon="fas fa-comments",
    html="""
<div class="dz-ml-app dz-ml-thread">
  <div class="dz-ml-thread-head">
    <h3 class="dz-ml-rsubj">Re : Planning du lancement de la collection d'automne</h3>
    <div class="dz-ml-row2"><span class="dz-ml-pill">7 messages</span><span class="dz-avatars">""" + av("AR", 5, "sm") + av("PG", 1, "sm") + av("CV", 2, "sm") + av("LF", 3, "sm") + """</span><a class="dz-ml-link dz-ml-push" href="#"><i class="fas fa-expand-alt"></i> Tout déplier</a></div>
  </div>
  <div class="dz-ml-msgs">
""" + folded("AR", 5, "Amandine Roux", "Bonjour à tous, voici le rétroplanning proposé pour le lancement du 14 octobre…", "15 sept.") \
    + folded("PG", 1, "Paul Garnier", "Ça me paraît jouable, sauf pour le shooting qu'il faudrait avancer d'une semaine.", "15 sept.") + """
    <a class="dz-ml-more" href="#"><span>3 messages plus anciens</span></a>
""" + folded("LF", 3, "Léa Fontaine", "Je peux livrer les textes produits le 2, pas avant. Ça vous va ?", "20 sept.") + """
    <div class="dz-ml-msgx">
      <div class="dz-ml-hdr">""" + av("CV", 2, "md") + """
        <div class="dz-ml-hdr-id"><p class="dz-ml-hdr-from"><b>Clara Vasseur</b><span>à Amandine, Paul, Léa</span></p></div>
        <time class="dz-ml-hdr-date">Hier, 18:20</time>
      </div>
      <div class="dz-ml-content">
        <p>Parfait pour moi. Je récapitule les dates clés :</p>
        <ul class="dz-ml-ul"><li><b>2 oct.</b> — textes produits (Léa)</li><li><b>6 oct.</b> — shooting en studio</li><li><b>14 oct.</b> — mise en ligne et envoi de la newsletter</li></ul>
        <p>Je mets à jour le calendrier partagé ce soir.</p>
      </div>
      <p class="dz-ml-quoted"><span>···</span></p>
    </div>
    <div class="dz-ml-msgx dz-ml-msgx-last">
      <div class="dz-ml-hdr">""" + av("AR", 5, "md") + """
        <div class="dz-ml-hdr-id"><p class="dz-ml-hdr-from"><b>Amandine Roux</b><span>à moi, Paul, Léa</span></p></div>
        <time class="dz-ml-hdr-date">10:05 (il y a 2 h)</time>
      </div>
      <div class="dz-ml-content"><p>Top, merci Clara ! Je réserve le studio pour le 6. 📸</p></div>
      <div class="dz-ml-quick"><a class="dz-ml-qbtn" href="#"><i class="fas fa-reply"></i> Répondre</a><a class="dz-ml-qbtn" href="#"><i class="fas fa-reply-all"></i> Répondre à tous</a><a class="dz-ml-qbtn" href="#"><i class="fas fa-share"></i> Transférer</a></div>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 5. Fenêtre de rédaction
# =====================================================================
BLOCKS.append(dict(
    name="rédaction",
    icon="fas fa-pen-fancy",
    html="""
<div class="dz-ml-composewrap">
<div class="dz-ml-app dz-ml-compose-win">
  <div class="dz-ml-cw-bar"><b>Nouveau message</b><span class="dz-ml-cw-saved"><i class="fas fa-check"></i> Brouillon enregistré</span><a class="dz-ml-ib" href="#" aria-label="Réduire"><i class="fas fa-minus"></i></a><a class="dz-ml-ib" href="#" aria-label="Plein écran"><i class="fas fa-expand-alt"></i></a><a class="dz-ml-ib" href="#" aria-label="Fermer"><i class="fas fa-times"></i></a></div>
  <div class="dz-ml-cw-field"><span class="dz-ml-cw-k">À</span><div class="dz-ml-recips"><span class="dz-ml-recip">""" + av("PG", 1, "xs") + """<span>Paul Garnier</span><i class="fas fa-times"></i></span><span class="dz-ml-recip">""" + av("LF", 3, "xs") + """<span>Léa Fontaine</span><i class="fas fa-times"></i></span><span class="dz-ml-typing">ama<span class="dz-ml-caret"></span></span></div><span class="dz-ml-cw-cc">Cc Cci</span></div>
  <div class="dz-ml-suggest">
    <a class="dz-ml-sug dz-active" href="#">""" + av("AR", 5, "sm") + """<span><b>Amandine Roux</b><small>amandine.roux@studio-brume.fr</small></span><span class="dz-kbd">↵</span></a>
    <a class="dz-ml-sug" href="#">""" + av("AM", 6, "sm") + """<span><b>Amaury Martin</b><small>a.martin@nexora.fr</small></span></a>
  </div>
  <div class="dz-ml-cw-field"><span class="dz-ml-cw-k">Objet</span><b class="dz-ml-cw-subj">Lancement collection d'automne — récap &amp; prochaines étapes</b></div>
  <div class="dz-ml-fmt">
    <a class="dz-ml-ib" href="#" aria-label="Annuler"><i class="fas fa-undo"></i></a>
    <span class="dz-ml-sep"></span>
    <a class="dz-ml-ib dz-ml-on" href="#" aria-label="Gras"><i class="fas fa-bold"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Italique"><i class="fas fa-italic"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Souligné"><i class="fas fa-underline"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Couleur"><i class="fas fa-font"></i></a>
    <span class="dz-ml-sep"></span>
    <a class="dz-ml-ib" href="#" aria-label="Liste à puces"><i class="fas fa-list-ul"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Liste numérotée"><i class="fas fa-list-ol"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Lien"><i class="fas fa-link"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Image"><i class="far fa-image"></i></a>
  </div>
  <div class="dz-ml-cw-body">
    <p>Bonjour à tous,</p>
    <p>Merci pour cette réunion efficace ! Voici ce que nous avons décidé :</p>
    <ul class="dz-ml-ul"><li>Mise en ligne le <b>14 octobre</b> à 9 h</li><li>Newsletter envoyée à <b>18 200 abonnés</b> le jour même</li></ul>
    <p>Je vous joins le planning détaillé.</p>
    <p class="dz-ml-cw-sig">— <br>Clara Vasseur · Directrice de projet · Studio Brume</p>
  </div>
  <div class="dz-ml-cw-att">""" + chip("PDF", "planning-lancement.pdf", "320 Ko", "pdf") + """</div>
  <div class="dz-ml-cw-foot">
    <div class="dz-ml-send"><a class="dz-ml-send-main" href="#"><i class="fas fa-paper-plane"></i> Envoyer</a><a class="dz-ml-send-more" href="#" aria-label="Programmer l'envoi"><i class="fas fa-chevron-down"></i></a></div>
    <a class="dz-ml-ib" href="#" aria-label="Joindre"><i class="fas fa-paperclip"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Émoji"><i class="far fa-smile"></i></a>
    <a class="dz-ml-ib" href="#" aria-label="Signature"><i class="fas fa-signature"></i></a>
    <a class="dz-ml-ib dz-ml-push" href="#" aria-label="Supprimer le brouillon"><i class="far fa-trash-alt"></i></a>
    <div class="dz-ml-sched">
      <p class="dz-ml-sched-h">Programmer l'envoi</p>
      <a class="dz-ml-sched-i" href="#"><span>Demain matin</span><time>ven. 25 sept., 08:00</time></a>
      <a class="dz-ml-sched-i dz-active" href="#"><span>Lundi matin</span><time>lun. 28 sept., 08:00</time></a>
      <a class="dz-ml-sched-i" href="#"><span>Choisir une date et une heure</span><i class="far fa-calendar-alt"></i></a>
    </div>
  </div>
</div>
</div>
""",
))

# =====================================================================
# 6. Newsletter dans un cadre
# =====================================================================
BLOCKS.append(dict(
    name="aperçu newsletter",
    icon="far fa-newspaper",
    html="""
<div class="dz-ml-preview">
  <div class="dz-ml-pvbar">
    <div class="dz-ml-pvmeta"><p><span>De</span><b>Le Fil Vert &lt;bonjour@lefilvert.fr&gt;</b></p><p><span>Objet</span><b>🍂 5 plantes qui adorent l'ombre (et -15 %)</b></p><p><span>Pré-en-tête</span><b>Notre sélection d'automne pour les coins sombres…</b></p></div>
    <div class="dz-ml-dev"><a class="dz-ml-devb dz-active" href="#"><i class="fas fa-desktop"></i> Ordinateur</a><a class="dz-ml-devb" href="#"><i class="fas fa-mobile-alt"></i> Mobile</a><a class="dz-ml-devb" href="#"><i class="fas fa-moon"></i> Sombre</a></div>
  </div>
  <div class="dz-ml-canvas">
    <div class="dz-ml-nl">
      <p class="dz-ml-nl-top">Voir la version en ligne</p>
      <div class="dz-ml-nl-brand"><i class="fas fa-seedling"></i><b>le fil vert</b></div>
      <div class="dz-ml-nl-hero"><img class="dz-cover" src="https://picsum.photos/seed/fougere/1200/560" alt="Fougères en pot"></div>
      <div class="dz-ml-nl-pad">
        <p class="dz-ml-nl-kick">Sélection d'automne</p>
        <h3 class="dz-ml-nl-h">5 plantes qui adorent l'ombre</h3>
        <p class="dz-ml-nl-p">Un couloir sans fenêtre, une chambre plein nord ? Ces cinq variétés s'y plaisent vraiment — et demandent très peu d'entretien.</p>
        <a class="dz-ml-nl-btn" href="#">Découvrir la sélection</a>
      </div>
      <div class="dz-ml-nl-prods">
        <div class="dz-ml-nl-prod"><span class="dz-ml-nl-img"><img class="dz-cover" src="https://picsum.photos/seed/calathea/300/300" alt="Calathea"></span><b>Calathea Orbifolia</b><span>24,90 €</span></div>
        <div class="dz-ml-nl-prod"><span class="dz-ml-nl-img"><img class="dz-cover" src="https://picsum.photos/seed/aspidistra/300/300" alt="Aspidistra"></span><b>Aspidistra</b><span>19,90 €</span></div>
        <div class="dz-ml-nl-prod"><span class="dz-ml-nl-img"><img class="dz-cover" src="https://picsum.photos/seed/zamioculcas/300/300" alt="Zamioculcas"></span><b>Zamioculcas</b><span>29,90 €</span></div>
      </div>
      <div class="dz-ml-nl-promo"><b>-15 % sur les jardinières</b><span>avec le code <span class="dz-ml-code">OMBRE15</span> jusqu'au 4 octobre</span></div>
      <div class="dz-ml-nl-foot"><div class="dz-ml-nl-soc"><i class="fab fa-instagram"></i><i class="fab fa-pinterest"></i><i class="fab fa-youtube"></i></div><p>Le Fil Vert · 8 quai des Plantes, 44000 Nantes</p><p>Vous recevez cet e-mail car vous êtes inscrit·e à notre lettre. <u>Se désinscrire</u> · <u>Préférences</u></p></div>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 7. Confirmation de commande (transactionnel)
# =====================================================================
BLOCKS.append(dict(
    name="confirmation de commande",
    icon="fas fa-receipt",
    html="""
<div class="dz-ml-canvas dz-ml-canvas-solo">
  <div class="dz-ml-tx">
    <div class="dz-ml-tx-brand"><span class="dz-ml-hm-logo"><i class="fas fa-lightbulb"></i></span><b>Maison Lumen</b></div>
    <div class="dz-ml-tx-hero">
      <span class="dz-ml-tx-ok"><i class="fas fa-check"></i></span>
      <h3 class="dz-ml-tx-h">Merci Camille, votre commande est confirmée !</h3>
      <p class="dz-ml-tx-p">Commande <b>#ML-20418</b> passée le 12 septembre 2026. Nous vous préviendrons dès son expédition.</p>
    </div>
    <div class="dz-ml-track">
      <div class="dz-ml-tk dz-done"><span></span><b>Confirmée</b><small>12 sept.</small></div>
      <div class="dz-ml-tk dz-cur"><span></span><b>Préparation</b><small>en cours</small></div>
      <div class="dz-ml-tk"><span></span><b>Expédiée</b><small>—</small></div>
      <div class="dz-ml-tk"><span></span><b>Livrée</b><small>15–16 sept.</small></div>
    </div>
    <div class="dz-ml-items">
      <div class="dz-ml-item"><span class="dz-ml-item-img"><img class="dz-cover" src="https://picsum.photos/seed/orbe-lamp/160/160" alt="Lampe Orbe"></span><div class="dz-ml-item-t"><b>Lampe Orbe · opaline</b><span>Quantité : 1</span></div><b class="dz-ml-item-p">249,00 €</b></div>
      <div class="dz-ml-item"><span class="dz-ml-item-img"><img class="dz-cover" src="https://picsum.photos/seed/halo-appl/160/160" alt="Applique Halo"></span><div class="dz-ml-item-t"><b>Applique Halo · laiton</b><span>Quantité : 2</span></div><b class="dz-ml-item-p">158,00 €</b></div>
    </div>
    <div class="dz-ml-sum">
      <div><span>Sous-total</span><b>407,00 €</b></div>
      <div><span>Remise pro (PRO12)</span><b class="dz-ml-green">−48,84 €</b></div>
      <div><span>Livraison express</span><b>30,84 €</b></div>
      <div class="dz-ml-sum-total"><span>Total TTC</span><b>389,00 €</b></div>
    </div>
    <div class="dz-ml-tx-cols">
      <div><p class="dz-ml-tx-k">Livraison</p><p class="dz-ml-tx-v">Camille Laurent<br>12 rue Mercière<br>69002 Lyon</p></div>
      <div><p class="dz-ml-tx-k">Paiement</p><p class="dz-ml-tx-v">Carte •••• 4417<br>Débitée le 12/09/2026</p></div>
    </div>
    <a class="dz-ml-nl-btn dz-ml-tx-btn" href="#">Suivre ma commande</a>
    <p class="dz-ml-tx-foot">Une question ? Répondez simplement à cet e-mail ou écrivez-nous au 04 78 60 21 90.<br>Maison Lumen SAS · 3 place des Terreaux, 69001 Lyon</p>
  </div>
</div>
""",
))

# =====================================================================
# 8. Réinitialisation du mot de passe
# =====================================================================
BLOCKS.append(dict(
    name="mot de passe oublié",
    icon="fas fa-key",
    html="""
<div class="dz-ml-canvas dz-ml-canvas-solo">
  <div class="dz-ml-tx dz-ml-tx-narrow">
    <div class="dz-ml-tx-brand dz-ml-tx-center"><span class="dz-ml-hm-logo"><i class="fas fa-cube"></i></span><b>Nexora</b></div>
    <div class="dz-ml-tx-hero">
      <span class="dz-ml-tx-key"><i class="fas fa-lock"></i></span>
      <h3 class="dz-ml-tx-h">Réinitialisez votre mot de passe</h3>
      <p class="dz-ml-tx-p">Bonjour Clara, nous avons reçu une demande de réinitialisation pour le compte <b>clara@studio-brume.fr</b>. Cliquez sur le bouton ci-dessous pour choisir un nouveau mot de passe.</p>
      <a class="dz-ml-nl-btn" href="#">Choisir un nouveau mot de passe</a>
      <p class="dz-ml-tx-small">Ce lien expire dans <b>30 minutes</b> et ne peut être utilisé qu'une fois.</p>
    </div>
    <div class="dz-ml-tx-code"><span>Ou saisissez ce code dans l'application</span><b class="dz-ml-otp">482 913</b></div>
    <div class="dz-ml-tx-sec"><i class="fas fa-shield-alt"></i><p>Demande effectuée le 24 sept. 2026 à 09:12 depuis <b>Lyon, France</b> (navigateur sur macOS). Ce n'était pas vous ? <u>Sécurisez votre compte</u>.</p></div>
    <p class="dz-ml-tx-foot">Nexora ne vous demandera jamais votre mot de passe par e-mail.<br>Nexora SAS · 42 rue du Faubourg, 75010 Paris</p>
  </div>
</div>
""",
))

# =====================================================================
# 9. Tri rapide
# =====================================================================
BLOCKS.append(dict(
    name="tri rapide",
    icon="fas fa-layer-group",
    html="""
<div class="dz-ml-triage">
  <div class="dz-ml-tri-head"><p class="dz-ml-kicker">Tri rapide</p><div class="dz-ml-tri-prog"><span class="dz-ml-bar"><span style="--v:35%"></span></span><b>7 / 20</b></div></div>
  <div class="dz-ml-stack">
    <span class="dz-ml-stack-bg dz-ml-stack-2"></span>
    <span class="dz-ml-stack-bg dz-ml-stack-1"></span>
    <div class="dz-ml-app dz-ml-tcard">
      <div class="dz-ml-hdr">""" + av("NX", 2, "md") + """<div class="dz-ml-hdr-id"><p class="dz-ml-hdr-from"><b>Nexora Facturation</b><span>facturation@nexora.fr</span></p><p class="dz-ml-hdr-to">Aujourd'hui, 09:15</p></div>""" + lab("Factures", 2) + """</div>
      <h3 class="dz-ml-rsubj">Votre facture de septembre est disponible</h3>
      <p class="dz-ml-tcard-p">Bonjour Clara, votre facture n° NX-2026-0918 d'un montant de <b>249,00 € TTC</b> est disponible. Elle sera prélevée le 30/09/2026 sur le compte se terminant par 0412.</p>
      <div class="dz-ml-ai"><i class="fas fa-magic"></i><span><b>Résumé :</b> facture mensuelle, rien à faire — prélèvement automatique.</span></div>
      """ + chip("PDF", "NX-2026-0918.pdf", "96 Ko", "pdf") + """
    </div>
  </div>
  <div class="dz-ml-tri-act">
    <a class="dz-ml-ta dz-ml-ta-arch" href="#"><i class="fas fa-archive"></i><span>Archiver</span><span class="dz-kbd">E</span></a>
    <a class="dz-ml-ta dz-ml-ta-later" href="#"><i class="far fa-clock"></i><span>Plus tard</span><span class="dz-kbd">H</span></a>
    <a class="dz-ml-ta dz-ml-ta-reply" href="#"><i class="fas fa-reply"></i><span>Répondre</span><span class="dz-kbd">R</span></a>
    <a class="dz-ml-ta dz-ml-ta-del" href="#"><i class="far fa-trash-alt"></i><span>Supprimer</span><span class="dz-kbd">#</span></a>
  </div>
</div>
""",
))

# =====================================================================
# 10. Pièces jointes
# =====================================================================
def fileline(ext, kind, name, size, frm, date):
    return '<a class="dz-ml-fl" href="#"><span class="dz-ml-att-ic dz-ml-f-%s">%s</span><div class="dz-ml-fl-t"><b>%s</b><span>%s · %s</span></div><span class="dz-ml-fl-size">%s</span><span class="dz-ml-fl-act"><i class="far fa-eye"></i><i class="fas fa-download"></i></span></a>' % (kind, ext, name, frm, date, size)


BLOCKS.append(dict(
    name="pièces jointes",
    icon="fas fa-paperclip",
    html="""
<div class="dz-ml-app dz-ml-files">
  <div class="dz-ml-files-head">
    <div class="dz-ml-grow"><h3 class="dz-ml-title">Pièces jointes</h3><p class="dz-ml-sub">148 fichiers reçus ce mois-ci · 312 Mo</p></div>
    <div class="dz-ml-tabs"><a class="dz-ml-tab dz-active" href="#">Tous</a><a class="dz-ml-tab" href="#">Documents</a><a class="dz-ml-tab" href="#">Images</a><a class="dz-ml-tab" href="#">Tableurs</a></div>
  </div>
  <div class="dz-ml-fls">
""" + fileline("PDF", "pdf", "contrat-final.pdf", "1,2 Mo", "Thomas Mercier", "22 sept.") \
    + fileline("JPG", "img", "shooting-automne-selection.zip", "84,6 Mo", "Sarah Benali", "24 sept.") \
    + fileline("XLS", "xls", "echeancier-2026.xlsx", "48 Ko", "Thomas Mercier", "22 sept.") \
    + fileline("DOC", "doc", "textes-produits-v2.docx", "212 Ko", "Léa Fontaine", "20 sept.") \
    + fileline("FIG", "fig", "accueil-v3-B.fig", "12,4 Mo", "Paul Garnier", "24 sept.") \
    + fileline("MP4", "vid", "teaser-collection.mp4", "38,1 Mo", "Amandine Roux", "18 sept.") + """
  </div>
  <div class="dz-ml-files-foot"><i class="fas fa-cloud"></i><span>Les fichiers de plus de 25 Mo sont envoyés sous forme de lien de partage.</span><a class="dz-ml-link dz-ml-push" href="#">Tout télécharger (.zip)</a></div>
</div>
""",
))

# =====================================================================
# 11. Signature
# =====================================================================
BLOCKS.append(dict(
    name="signature",
    icon="fas fa-signature",
    html="""
<div class="dz-ml-app dz-ml-sigs">
  <aside class="dz-ml-siglist">
    <p class="dz-ml-flabel">Mes signatures</p>
    <a class="dz-ml-sigi dz-active" href="#"><b>Professionnelle</b><span>Par défaut · nouveaux messages</span></a>
    <a class="dz-ml-sigi" href="#"><b>Réponse courte</b><span>Réponses et transferts</span></a>
    <a class="dz-ml-sigi" href="#"><b>Anglais</b><span>Clients internationaux</span></a>
    <a class="dz-ml-addsig" href="#"><i class="fas fa-plus"></i> Nouvelle signature</a>
  </aside>
  <div class="dz-ml-sigmain">
    <div class="dz-ml-row2"><h3 class="dz-ml-title">Professionnelle</h3><span class="dz-ml-pill dz-ml-push">Aperçu</span></div>
    <div class="dz-ml-sigcard">
      <span class="dz-ml-sigphoto">CV</span>
      <div class="dz-ml-sigtxt">
        <b class="dz-ml-sig-n">Clara Vasseur</b>
        <span class="dz-ml-sig-r">Directrice de projet · Studio Brume</span>
        <span class="dz-ml-sig-l"><i class="fas fa-phone-alt"></i> +33 6 71 04 28 93</span>
        <span class="dz-ml-sig-l"><i class="fas fa-globe"></i> studio-brume.fr</span>
        <div class="dz-ml-sig-soc"><i class="fab fa-linkedin-in"></i><i class="fab fa-instagram"></i><i class="fab fa-behance"></i></div>
      </div>
      <div class="dz-ml-sigban"><i class="fas fa-award"></i><span>Lauréat du prix Design Numérique 2026 — <u>voir le projet</u></span></div>
    </div>
    <div class="dz-ml-sigopts">
      <div class="dz-ml-opt"><span>Insérer avant le texte cité dans les réponses</span><span class="dz-ml-toggle dz-on"></span></div>
      <div class="dz-ml-opt"><span>Ajouter le séparateur « -- »</span><span class="dz-ml-toggle"></span></div>
      <div class="dz-ml-opt"><span>Signature pour les réponses</span><a class="dz-ml-select" href="#">Réponse courte <i class="fas fa-chevron-down"></i></a></div>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 12. Message d'absence
# =====================================================================
BLOCKS.append(dict(
    name="message d'absence",
    icon="fas fa-umbrella-beach",
    html="""
<div class="dz-ml-app dz-ml-ooo">
  <div class="dz-ml-ooo-head">
    <span class="dz-ml-ooo-ic"><i class="fas fa-umbrella-beach"></i></span>
    <div class="dz-ml-grow"><h3 class="dz-ml-title">Réponse automatique d'absence</h3><p class="dz-ml-sub">Activée du 19 au 27 octobre 2026</p></div>
    <span class="dz-ml-toggle dz-on"></span>
  </div>
  <div class="dz-ml-ooo-body">
    <div class="dz-ml-dates">
      <div class="dz-ml-date"><span>Premier jour</span><b><i class="far fa-calendar"></i> lun. 19 oct. 2026</b></div>
      <i class="fas fa-arrow-right dz-ml-date-arrow"></i>
      <div class="dz-ml-date"><span>Dernier jour</span><b><i class="far fa-calendar"></i> mar. 27 oct. 2026</b></div>
    </div>
    <div class="dz-ml-cw-field dz-ml-ooo-f"><span class="dz-ml-cw-k">Objet</span><b class="dz-ml-cw-subj">Absente jusqu'au 27 octobre</b></div>
    <div class="dz-ml-ooo-msg">
      <p>Bonjour,</p>
      <p>Je suis en congés jusqu'au <b>mardi 27 octobre</b> inclus, avec un accès limité à mes e-mails. Pour toute urgence concernant un projet en cours, vous pouvez contacter <b>Amandine Roux</b> (amandine.roux@studio-brume.fr).</p>
      <p>Belle journée,<br>Clara</p>
    </div>
    <div class="dz-ml-sigopts">
      <div class="dz-ml-opt"><span>Répondre uniquement à mes contacts</span><span class="dz-ml-toggle"></span></div>
      <div class="dz-ml-opt"><span>Réponse différente pour l'extérieur de Studio Brume</span><span class="dz-ml-toggle dz-on"></span></div>
      <div class="dz-ml-opt"><span>Refuser les nouvelles invitations d'agenda</span><span class="dz-ml-toggle dz-on"></span></div>
    </div>
  </div>
  <div class="dz-ml-ooo-foot"><span class="dz-ml-sub"><i class="fas fa-info-circle"></i> Chaque expéditeur reçoit la réponse une seule fois tous les 4 jours.</span><a class="dz-btn dz-btn-sm dz-ml-push" href="#">Enregistrer</a></div>
</div>
""",
))

# =====================================================================
# 13. Règles et filtres
# =====================================================================
def rule(on, name, cond, acts, n):
    return '<div class="dz-ml-rule"><span class="dz-ml-grip"><i class="fas fa-grip-vertical"></i></span><div class="dz-ml-grow"><b class="dz-ml-rule-n">%s</b><p class="dz-ml-rule-c"><span class="dz-ml-if">SI</span>%s</p><p class="dz-ml-rule-c"><span class="dz-ml-then">ALORS</span>%s</p></div><span class="dz-ml-rule-cnt">%s</span><span class="dz-ml-toggle%s"></span></div>' % (name, cond, acts, n, " dz-on" if on else "")


T = lambda s: '<span class="dz-ml-tok">' + s + '</span>'

BLOCKS.append(dict(
    name="règles et filtres",
    icon="fas fa-filter",
    html="""
<div class="dz-ml-app dz-ml-rules">
  <div class="dz-ml-files-head">
    <div class="dz-ml-grow"><h3 class="dz-ml-title">Règles et filtres</h3><p class="dz-ml-sub">Appliquées dans l'ordre à chaque message entrant. Glissez pour réorganiser.</p></div>
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouvelle règle</a>
  </div>
""" + rule(True, "Factures fournisseurs", "l'objet contient " + T("facture") + " ou la pièce jointe est un " + T("PDF"), "appliquer " + lab("Factures", 2) + " · transférer à " + T("compta@studio-brume.fr") + " · archiver", "412 ×") \
    + rule(True, "Clients prioritaires", "l'expéditeur est dans " + T("Groupe · Clients"), "marquer comme " + T("★ suivi") + " · notification sur mobile", "96 ×") \
    + rule(True, "Newsletters", "l'en-tête contient " + T("List-Unsubscribe"), "appliquer " + lab("Newsletters", 4) + " · ignorer la boîte de réception", "1 208 ×") \
    + rule(False, "Notifications d'outils", "l'expéditeur finit par " + T("@notifications.nexora.fr"), "marquer comme lu · déplacer vers " + T("Outils"), "0 ×") + """
</div>
""",
))

# =====================================================================
# 14. Recherche avancée
# =====================================================================
BLOCKS.append(dict(
    name="recherche avancée",
    icon="fas fa-search-plus",
    html="""
<div class="dz-ml-adv">
  <div class="dz-ml-app dz-ml-advbox">
    <div class="dz-ml-advbar"><i class="fas fa-search"></i><span class="dz-ml-q"><span class="dz-ml-op">de:</span>thomas <span class="dz-ml-op">a:</span>pj contrat<span class="dz-ml-caret"></span></span><a class="dz-ml-ib" href="#" aria-label="Effacer"><i class="fas fa-times"></i></a></div>
    <div class="dz-ml-advgrid">
      <div class="dz-ml-af"><span>De</span><b>Thomas Mercier <i class="fas fa-times"></i></b></div>
      <div class="dz-ml-af"><span>À</span><em>Adresse ou nom</em></div>
      <div class="dz-ml-af"><span>Objet</span><em>Contient les mots…</em></div>
      <div class="dz-ml-af"><span>Contient</span><b>contrat</b></div>
      <div class="dz-ml-af"><span>Date</span><b>30 derniers jours <i class="fas fa-chevron-down"></i></b></div>
      <div class="dz-ml-af"><span>Dossier</span><b>Tous les messages <i class="fas fa-chevron-down"></i></b></div>
    </div>
    <div class="dz-ml-row2 dz-ml-advchips">
      <a class="dz-ml-chip dz-active" href="#"><i class="fas fa-paperclip"></i> Avec pièce jointe</a>
      <a class="dz-ml-chip" href="#"><i class="far fa-star"></i> Suivis</a>
      <a class="dz-ml-chip" href="#"><i class="far fa-envelope"></i> Non lus</a>
      <a class="dz-ml-chip" href="#"><i class="fas fa-weight-hanging"></i> &gt; 5 Mo</a>
      <a class="dz-ml-chip" href="#"><i class="fas fa-tag"></i> Libellé</a>
    </div>
    <div class="dz-ml-row2 dz-ml-advfoot"><a class="dz-ml-link" href="#"><i class="far fa-bookmark"></i> Enregistrer la recherche</a><a class="dz-btn dz-btn-sm dz-btn-ghost dz-ml-push" href="#">Réinitialiser</a><a class="dz-btn dz-btn-sm" href="#">Rechercher</a></div>
  </div>
  <div class="dz-ml-app dz-ml-advres">
    <p class="dz-ml-advres-h"><b>4 résultats</b> · triés par pertinence</p>
    <a class="dz-ml-hit" href="#">""" + av("TM", 6, "sm") + """<div class="dz-ml-grow"><p class="dz-ml-hit-t"><b>Contrat de prestation — version finale</b><time>22 sept.</time></p><p class="dz-ml-hit-p">…ci-joint la version finale du <mark class="dz-ml-mark">contrat</mark> de prestation pour la refonte…</p><span class="dz-ml-hit-f"><i class="fas fa-file-pdf dz-ml-f-pdf-t"></i> <mark class="dz-ml-mark">contrat</mark>-final.pdf</span></div></a>
    <a class="dz-ml-hit" href="#">""" + av("TM", 6, "sm") + """<div class="dz-ml-grow"><p class="dz-ml-hit-t"><b>Re : Article 7 du contrat</b><time>18 sept.</time></p><p class="dz-ml-hit-p">…je propose de reformuler la clause de propriété du <mark class="dz-ml-mark">contrat</mark> ainsi…</p><span class="dz-ml-hit-f"><i class="fas fa-file-word dz-ml-f-doc-t"></i> <mark class="dz-ml-mark">contrat</mark>-annotations.docx</span></div></a>
    <a class="dz-ml-hit" href="#">""" + av("TM", 6, "sm") + """<div class="dz-ml-grow"><p class="dz-ml-hit-t"><b>Premier jet du <mark class="dz-ml-mark">contrat</mark></b><time>9 sept.</time></p><p class="dz-ml-hit-p">…voici une première version, n'hésitez pas à annoter directement…</p><span class="dz-ml-hit-f"><i class="fas fa-file-pdf dz-ml-f-pdf-t"></i> <mark class="dz-ml-mark">contrat</mark>-v1.pdf</span></div></a>
  </div>
</div>
""",
))

# =====================================================================
# 15. Notification de nouveau mail
# =====================================================================
BLOCKS.append(dict(
    name="notification nouveau mail",
    icon="far fa-bell",
    html="""
<div class="dz-ml-nstage">
  <div class="dz-ml-desk">
    <div class="dz-ml-notif">
      <div class="dz-ml-notif-app"><span class="dz-ml-notif-logo"><i class="fas fa-envelope"></i></span><span>Courrier</span><time>maintenant</time></div>
      <div class="dz-ml-notif-b">""" + av("PG", 1, "md") + """<div class="dz-ml-grow"><b>Paul Garnier</b><p class="dz-ml-notif-s">Maquettes v3 validées ✔</p><p class="dz-ml-notif-p">On part sur la version B pour la page d'accueil, bravo à toute l'équipe !</p></div></div>
      <div class="dz-ml-notif-act"><a href="#">Répondre</a><a href="#">Archiver</a><a href="#">Marquer comme lu</a></div>
    </div>
    <div class="dz-ml-notif dz-ml-notif-grp">
      <div class="dz-ml-notif-app"><span class="dz-ml-notif-logo"><i class="fas fa-envelope"></i></span><span>Courrier · 3 nouveaux messages</span><time>2 min</time></div>
      <p class="dz-ml-notif-line"><b>Nexora Facturation</b> Votre facture de septembre</p>
      <p class="dz-ml-notif-line"><b>Sarah Benali</b> Photos du shooting</p>
    </div>
  </div>
  <div class="dz-ml-phone">
    <p class="dz-ml-ph-time">09:41</p>
    <p class="dz-ml-ph-date">jeudi 24 septembre</p>
    <div class="dz-ml-ph-n">
      <div class="dz-ml-notif-app"><span class="dz-ml-notif-logo"><i class="fas fa-envelope"></i></span><span>COURRIER</span><time>maintenant</time></div>
      <b>Julie Lambert</b>
      <p class="dz-ml-notif-s">Déjeuner jeudi ?</p>
      <p class="dz-ml-notif-p">Je serai à Lyon toute la journée, ça te dit un déjeuner près de Bellecour ?</p>
    </div>
    <div class="dz-ml-ph-n dz-ml-ph-n2"><div class="dz-ml-notif-app"><span class="dz-ml-notif-logo"><i class="fas fa-envelope"></i></span><span>COURRIER</span><time>9 min</time></div><b>Thomas Mercier</b><p class="dz-ml-notif-s">Contrat de prestation — signature</p></div>
  </div>
</div>
""",
))

# =====================================================================
# 16. Statistiques de campagne
# =====================================================================
def link(url, clicks, pct):
    return '<div class="dz-ml-lk"><span class="dz-ml-lk-u">%s</span><span class="dz-ml-bar"><span style="--v:%s%%"></span></span><b>%s</b></div>' % (url, pct, clicks)


BLOCKS.append(dict(
    name="statistiques de campagne",
    icon="fas fa-chart-line",
    html="""
<div class="dz-ml-stats">
  <div class="dz-ml-row2 dz-ml-st-head">
    <div class="dz-ml-grow"><p class="dz-ml-kicker">Campagne · envoyée le 14 oct. 2026 à 09:00</p><h3 class="dz-ml-h">🍂 5 plantes qui adorent l'ombre</h3></div>
    <span class="dz-ml-sent"><i class="fas fa-check-circle"></i> Envoyée à 18 204 contacts</span>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-download"></i> Rapport</a>
  </div>
  <div class="dz-ml-kpis">
    <div class="dz-ml-kpi"><span>Délivrés</span><b>99,2 %</b><small>18 058 e-mails</small></div>
    <div class="dz-ml-kpi dz-ml-kpi-main"><span>Taux d'ouverture</span><b>47,8 %</b><small><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 6,1 pts</span> vs moyenne</small></div>
    <div class="dz-ml-kpi"><span>Taux de clic</span><b>8,9 %</b><small>1 607 clics uniques</small></div>
    <div class="dz-ml-kpi"><span>Ventes générées</span><b>12 480 €</b><small>214 commandes</small></div>
    <div class="dz-ml-kpi"><span>Désinscriptions</span><b>0,18 %</b><small>33 contacts</small></div>
  </div>
  <div class="dz-ml-stgrid">
    <div class="dz-ml-app dz-ml-panel">
      <div class="dz-ml-row2"><h4 class="dz-ml-panel-t">Ouvertures et clics · 48 premières heures</h4><div class="dz-ml-legend dz-ml-push"><span><i class="dz-ml-lg1"></i> Ouvertures</span><span><i class="dz-ml-lg2"></i> Clics</span></div></div>
      <div class="dz-ml-chart">
        <svg viewBox="0 0 600 200" preserveAspectRatio="none" class="dz-ml-svg"><path class="dz-ml-area" d="M0 196 C40 190 60 40 100 30 C140 22 170 90 220 110 C270 130 300 120 340 140 C400 160 470 172 600 182 L600 200 L0 200 Z"/><path class="dz-ml-line1" d="M0 196 C40 190 60 40 100 30 C140 22 170 90 220 110 C270 130 300 120 340 140 C400 160 470 172 600 182"/><path class="dz-ml-line2" d="M0 198 C40 196 60 150 100 146 C140 142 170 168 220 172 C270 176 300 174 340 180 C400 186 470 190 600 194"/></svg>
        <div class="dz-ml-xaxis"><span>9 h</span><span>12 h</span><span>18 h</span><span>J+1</span><span>J+2</span></div>
      </div>
    </div>
    <div class="dz-ml-app dz-ml-panel">
      <h4 class="dz-ml-panel-t">Liens les plus cliqués</h4>
      """ + link("Découvrir la sélection", "824", 100) + link("Calathea Orbifolia", "391", 47) + link("Code OMBRE15", "236", 29) + link("Zamioculcas", "112", 14) + link("Instagram", "44", 5) + """
      <div class="dz-ml-devsplit"><span><i class="fas fa-mobile-alt"></i> Mobile <b>68 %</b></span><span><i class="fas fa-desktop"></i> Ordinateur <b>29 %</b></span><span><i class="fas fa-tablet-alt"></i> Tablette <b>3 %</b></span></div>
    </div>
  </div>
</div>
""",
))

# =====================================================================
# 17. Inbox zéro
# =====================================================================
BLOCKS.append(dict(
    name="inbox zéro",
    icon="fas fa-mug-hot",
    html="""
<div class="dz-ml-app dz-ml-zero">
  <div class="dz-ml-zero-art">
    <span class="dz-ml-sun"></span>
    <span class="dz-ml-ray dz-ml-ray1"></span><span class="dz-ml-ray dz-ml-ray2"></span><span class="dz-ml-ray dz-ml-ray3"></span>
    <span class="dz-ml-env"><i class="fas fa-envelope-open"></i></span>
    <span class="dz-ml-spark dz-ml-sp1"><i class="fas fa-star"></i></span><span class="dz-ml-spark dz-ml-sp2"><i class="fas fa-star"></i></span><span class="dz-ml-spark dz-ml-sp3"><i class="fas fa-star"></i></span>
  </div>
  <h3 class="dz-ml-h">Boîte de réception vide ✨</h3>
  <p class="dz-ml-sub dz-ml-zero-p">Vous avez traité les 46 messages d'aujourd'hui. Profitez-en pour souffler : le prochain rappel est prévu à 14:00.</p>
  <div class="dz-ml-zero-stats">
    <div><b>31</b><span>archivés</span></div>
    <div><b>9</b><span>réponses</span></div>
    <div><b>6</b><span>reportés</span></div>
    <div><b>🔥 12</b><span>jours de série</span></div>
  </div>
  <div class="dz-ml-row2 dz-ml-zero-act"><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-clock"></i> Voir les messages reportés</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-pen"></i> Nouveau message</a></div>
</div>
""",
))

# =====================================================================
# 18. Annuler l'envoi / envoi programmé
# =====================================================================
BLOCKS.append(dict(
    name="envoi programmé",
    icon="far fa-paper-plane",
    html="""
<div class="dz-ml-sendstage">
  <div class="dz-ml-app dz-ml-schedlist">
    <div class="dz-ml-files-head"><div class="dz-ml-grow"><h3 class="dz-ml-title">Programmés</h3><p class="dz-ml-sub">3 messages partiront automatiquement</p></div></div>
    <div class="dz-ml-sq"><span class="dz-ml-sq-when"><b>28</b><span>sept.</span></span><div class="dz-ml-grow"><b>Relance devis — Brasserie Sillon</b><p>À : julien.petit@brasserie-sillon.fr</p></div><span class="dz-ml-sq-t"><i class="far fa-clock"></i> lun. 08:00</span></div>
    <div class="dz-ml-sq"><span class="dz-ml-sq-when"><b>30</b><span>sept.</span></span><div class="dz-ml-grow"><b>Bilan du mois — équipe</b><p>À : equipe@studio-brume.fr</p></div><span class="dz-ml-sq-t"><i class="far fa-clock"></i> mer. 17:30</span></div>
    <div class="dz-ml-sq"><span class="dz-ml-sq-when"><b>14</b><span>oct.</span></span><div class="dz-ml-grow"><b>C'est le grand jour 🍂</b><p>À : Paul Garnier, Léa Fontaine +2</p></div><span class="dz-ml-sq-t"><i class="far fa-clock"></i> mer. 09:00</span></div>
  </div>
  <div class="dz-ml-undo">
    <i class="fas fa-paper-plane"></i>
    <span>Message envoyé à <b>Paul Garnier</b></span>
    <a class="dz-ml-undo-a" href="#">Annuler</a>
    <a class="dz-ml-undo-a" href="#">Afficher</a>
    <span class="dz-ml-undo-ring"><b>7</b></span>
  </div>
  <div class="dz-ml-undo dz-ml-undo-2">
    <i class="far fa-clock"></i>
    <span>Envoi programmé <b>lundi 28 sept. à 08:00</b></span>
    <a class="dz-ml-undo-a" href="#">Modifier</a>
  </div>
</div>
""",
))
