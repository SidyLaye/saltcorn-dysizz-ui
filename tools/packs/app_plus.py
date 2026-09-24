"""App (ajouts) : écrans d'application professionnels. CSS : styles/44-app-plus.css (préfixe dz-ap-)."""
FAMILY = "app"

BLOCKS = [
    # ------------------------------------------------------------------ 1
    dict(
        name="table d'administration",
        icon="fas fa-table",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel">
    <div class="dz-ap-head">
      <div class="dz-ap-head-title"><h2 class="dz-ap-title">Clients <span class="dz-ap-count">1 248</span></h2><span class="dz-ap-sub">Comptes actifs et en essai · mis à jour il y a 2 min</span></div>
      <div class="dz-ap-actions"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-download"></i> Exporter</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouveau client</a></div>
    </div>
    <div class="dz-ap-toolbar">
      <div class="dz-ap-search"><i class="fas fa-search"></i><span>Rechercher par nom, e-mail, SIREN…</span><span class="dz-kbd">/</span></div>
      <div class="dz-ap-filters">
        <span class="dz-ap-filter dz-ap-on"><b>Statut</b> Actif <i class="fas fa-times"></i></span>
        <span class="dz-ap-filter dz-ap-on"><b>Formule</b> Équipe, Entreprise <i class="fas fa-times"></i></span>
        <span class="dz-ap-filter dz-ap-add"><i class="fas fa-plus"></i> Filtre</span>
      </div>
      <div class="dz-ap-seg"><span class="dz-ap-on" aria-label="Vue tableau"><i class="fas fa-list"></i></span><span aria-label="Vue cartes"><i class="fas fa-th-large"></i></span></div>
    </div>
    <div class="dz-ap-bulk">
      <span class="dz-ap-check dz-ap-mixed"><i class="fas fa-minus"></i></span>
      <b>3 sélectionnés</b>
      <span class="dz-ap-bulk-sep"></span>
      <a class="dz-ap-bulk-act" href="#"><i class="fas fa-user-plus"></i> Assigner</a>
      <a class="dz-ap-bulk-act" href="#"><i class="fas fa-tag"></i> Étiqueter</a>
      <a class="dz-ap-bulk-act" href="#"><i class="fas fa-archive"></i> Archiver</a>
      <a class="dz-ap-bulk-act dz-ap-danger" href="#"><i class="fas fa-trash-alt"></i> Supprimer</a>
      <span class="dz-ap-bulk-close" aria-label="Annuler la sélection"><i class="fas fa-times"></i></span>
    </div>
    <div class="dz-ap-scroll">
      <div class="dz-ap-table dz-ap-t-admin">
        <div class="dz-ap-tr dz-ap-th"><span class="dz-ap-check"></span><span>Client <i class="fas fa-sort-down"></i></span><span>Statut</span><span>Formule</span><span class="dz-ap-num">MRR</span><span>Dernière activité</span><span>Responsable</span><span></span></div>
        <div class="dz-ap-tr dz-ap-sel"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">AL</span><div><b>Atelier Lune</b><span>compta@atelierlune.fr</span></div></div><span class="dz-badge dz-badge-success"><span class="dz-ap-dot"></span> Actif</span><span>Équipe</span><span class="dz-ap-num">1 240 €</span><span class="dz-ap-muted">il y a 12 min</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">IC</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr dz-ap-sel"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">KB</span><div><b>Kobalt Logistique</b><span>it@kobalt.fr</span></div></div><span class="dz-badge dz-badge-success"><span class="dz-ap-dot"></span> Actif</span><span>Entreprise</span><span class="dz-ap-num">8 900 €</span><span class="dz-ap-muted">il y a 1 h</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">MH</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr"><span class="dz-ap-check"></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">MO</span><div><b>Maison Oré</b><span>bonjour@maisonore.fr</span></div></div><span class="dz-badge dz-badge-warning"><span class="dz-ap-dot"></span> Paiement en retard</span><span>Équipe</span><span class="dz-ap-num">640 €</span><span class="dz-ap-muted">hier, 18:02</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">LS</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr dz-ap-sel"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">NP</span><div><b>Norden Partners</b><span>admin@norden.fr</span></div></div><span class="dz-badge"><span class="dz-ap-dot"></span> Essai · 6 j</span><span>Équipe</span><span class="dz-ap-num">0 €</span><span class="dz-ap-muted">il y a 3 h</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">IC</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr"><span class="dz-ap-check"></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">TS</span><div><b>Tessera Studio</b><span>hello@tessera.studio</span></div></div><span class="dz-badge dz-badge-success"><span class="dz-ap-dot"></span> Actif</span><span>Essentiel</span><span class="dz-ap-num">90 €</span><span class="dz-ap-muted">12 sept.</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">TG</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr"><span class="dz-ap-check"></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">BA</span><div><b>Brume Assurances</b><span>dsi@brume-assurances.fr</span></div></div><span class="dz-badge dz-badge-danger"><span class="dz-ap-dot"></span> Résilié</span><span>Entreprise</span><span class="dz-ap-num">—</span><span class="dz-ap-muted">2 sept.</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">MH</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
        <div class="dz-ap-tr"><span class="dz-ap-check"></span><div class="dz-ap-who"><span class="dz-avatar dz-avatar-sm">VG</span><div><b>Vertige Escalade</b><span>contact@vertige.fr</span></div></div><span class="dz-badge dz-badge-success"><span class="dz-ap-dot"></span> Actif</span><span>Équipe</span><span class="dz-ap-num">420 €</span><span class="dz-ap-muted">28 août</span><span class="dz-avatar dz-avatar-sm dz-ap-owner">LS</span><span class="dz-ap-more" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></span></div>
      </div>
    </div>
    <div class="dz-ap-foot">
      <span class="dz-ap-muted">1 – 7 sur 1 248 · <b>11 290 €</b> de MRR affiché</span>
      <div class="dz-ap-pager"><span class="dz-ap-page" aria-label="Page précédente"><i class="fas fa-chevron-left"></i></span><span class="dz-ap-page dz-ap-on">1</span><span class="dz-ap-page">2</span><span class="dz-ap-page">3</span><span class="dz-ap-page dz-ap-gap">…</span><span class="dz-ap-page">179</span><span class="dz-ap-page" aria-label="Page suivante"><i class="fas fa-chevron-right"></i></span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 2
    dict(
        name="gestionnaire de fichiers",
        icon="fas fa-folder-open",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-files">
    <div class="dz-ap-tree">
      <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-cloud-upload-alt"></i> Importer</a>
      <div class="dz-ap-tree-group">
        <span class="dz-ap-tree-item"><i class="fas fa-home"></i> Mon espace</span>
        <span class="dz-ap-tree-item dz-ap-lvl1"><i class="fas fa-chevron-down dz-ap-caret"></i><i class="fas fa-folder-open"></i> Projets</span>
        <span class="dz-ap-tree-item dz-ap-lvl2 dz-ap-on"><i class="fas fa-folder-open"></i> Refonte boutique</span>
        <span class="dz-ap-tree-item dz-ap-lvl2"><i class="fas fa-folder"></i> Salon Maison 2026</span>
        <span class="dz-ap-tree-item dz-ap-lvl1"><i class="fas fa-chevron-right dz-ap-caret"></i><i class="fas fa-folder"></i> Juridique</span>
        <span class="dz-ap-tree-item dz-ap-lvl1"><i class="fas fa-chevron-right dz-ap-caret"></i><i class="fas fa-folder"></i> Finances</span>
      </div>
      <div class="dz-ap-tree-group">
        <span class="dz-ap-tree-item"><i class="fas fa-user-friends"></i> Partagés avec moi</span>
        <span class="dz-ap-tree-item"><i class="fas fa-star"></i> Favoris</span>
        <span class="dz-ap-tree-item"><i class="fas fa-trash-alt"></i> Corbeille</span>
      </div>
      <div class="dz-ap-quota"><div class="dz-ap-quota-row"><span>Stockage</span><b>68,4 / 100 Go</b></div><div class="dz-progress"><span style="--v:68%"></span></div></div>
    </div>
    <div class="dz-ap-files-main">
      <div class="dz-ap-files-top">
        <div class="dz-ap-crumbs"><span>Mon espace</span><i class="fas fa-chevron-right"></i><span>Projets</span><i class="fas fa-chevron-right"></i><b>Refonte boutique</b></div>
        <div class="dz-ap-actions"><span class="dz-ap-sort"><i class="fas fa-sort-amount-down"></i> Modifié récemment</span><div class="dz-ap-seg"><span class="dz-ap-on" aria-label="Grille"><i class="fas fa-th-large"></i></span><span aria-label="Liste"><i class="fas fa-list"></i></span></div></div>
      </div>
      <span class="dz-ap-label">Dossiers</span>
      <div class="dz-ap-folders">
        <div class="dz-ap-folder"><i class="fas fa-folder"></i><div><b>Maquettes</b><span>24 fichiers</span></div></div>
        <div class="dz-ap-folder"><i class="fas fa-folder"></i><div><b>Photos produits</b><span>186 fichiers</span></div></div>
        <div class="dz-ap-folder"><i class="fas fa-folder"></i><div><b>Contenus</b><span>12 fichiers</span></div></div>
      </div>
      <span class="dz-ap-label">Fichiers</span>
      <div class="dz-ap-grid-files">
        <div class="dz-ap-file dz-ap-sel"><div class="dz-ap-thumb"><img class="dz-cover" src="https://picsum.photos/seed/maquette-accueil/400/300" alt="Aperçu de la maquette d'accueil"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span></div><div class="dz-ap-file-meta"><b>accueil-v3.png</b><span>2,4 Mo · Inès C.</span></div></div>
        <div class="dz-ap-file"><div class="dz-ap-thumb dz-ap-thumb-doc"><i class="fas fa-file-pdf"></i></div><div class="dz-ap-file-meta"><b>Cahier des charges.pdf</b><span>1,1 Mo · il y a 2 h</span></div></div>
        <div class="dz-ap-file"><div class="dz-ap-thumb dz-ap-thumb-sheet"><i class="fas fa-file-excel"></i></div><div class="dz-ap-file-meta"><b>Budget prévisionnel.xlsx</b><span>86 Ko · hier</span></div></div>
        <div class="dz-ap-file"><div class="dz-ap-thumb"><img class="dz-cover" src="https://picsum.photos/seed/photo-vase/400/300" alt="Photo d'un vase"></div><div class="dz-ap-file-meta"><b>vase-figuier.jpg</b><span>4,8 Mo · 18 sept.</span></div></div>
        <div class="dz-ap-file"><div class="dz-ap-thumb dz-ap-thumb-video"><i class="fas fa-play"></i><span class="dz-ap-duration">01:42</span></div><div class="dz-ap-file-meta"><b>teaser-lancement.mp4</b><span>38 Mo · 15 sept.</span></div></div>
        <div class="dz-ap-file"><div class="dz-ap-thumb dz-ap-thumb-zip"><i class="fas fa-file-archive"></i></div><div class="dz-ap-file-meta"><b>Polices.zip</b><span>12 Mo · 9 sept.</span></div></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 3
    dict(
        name="centre de notifications",
        icon="fas fa-bell",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-inbox">
    <div class="dz-ap-head">
      <div class="dz-ap-head-title"><h2 class="dz-ap-title">Notifications</h2><span class="dz-ap-sub">5 non lues</span></div>
      <div class="dz-ap-actions"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-check-double"></i> Tout marquer comme lu</a><span class="dz-ap-iconbtn" aria-label="Préférences"><i class="fas fa-cog"></i></span></div>
    </div>
    <div class="dz-ap-tabs"><span class="dz-ap-tab dz-ap-on">Toutes <b>12</b></span><span class="dz-ap-tab">Mentions <b>3</b></span><span class="dz-ap-tab">Assignées <b>2</b></span><span class="dz-ap-tab">Système</span></div>
    <div class="dz-ap-notes">
      <span class="dz-ap-day">Aujourd'hui</span>
      <div class="dz-ap-note dz-ap-unread">
        <span class="dz-avatar dz-avatar-sm">SB</span>
        <div class="dz-ap-note-body">
          <p><b>Sarah Blanc</b> demande votre validation pour <b>Devis D-2026-118</b> · 12 480 € HT</p>
          <div class="dz-ap-note-acts"><a class="dz-btn dz-btn-sm" href="#">Approuver</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Refuser</a></div>
        </div>
        <span class="dz-ap-note-time">09:42</span><span class="dz-ap-unread-dot"></span>
      </div>
      <div class="dz-ap-note dz-ap-unread">
        <span class="dz-avatar dz-avatar-sm">JF</span>
        <div class="dz-ap-note-body">
          <p><b>Julien Fabre</b> vous a mentionné dans <b>Refonte boutique</b></p>
          <blockquote class="dz-ap-note-quote">@Camille tu peux valider la version mobile avant 16 h ? Le client veut la voir demain matin.</blockquote>
        </div>
        <span class="dz-ap-note-time">08:15</span><span class="dz-ap-unread-dot"></span>
      </div>
      <div class="dz-ap-note dz-ap-unread">
        <span class="dz-ap-note-ico dz-ap-ico-ok"><i class="fas fa-euro-sign"></i></span>
        <div class="dz-ap-note-body"><p>Paiement reçu de <b>Atelier Lune</b> : 5 112,00 € pour la facture F-2026-0412</p><span class="dz-ap-chip-ctx"><i class="fas fa-receipt"></i> Facturation</span></div>
        <span class="dz-ap-note-time">07:58</span><span class="dz-ap-unread-dot"></span>
      </div>
      <span class="dz-ap-day">Hier</span>
      <div class="dz-ap-note">
        <span class="dz-avatar dz-avatar-sm">LS</span>
        <div class="dz-ap-note-body"><p><b>Léa Simon</b> a partagé un fichier avec vous</p><div class="dz-ap-note-file"><i class="fas fa-file-pdf"></i><div><b>Charte graphique v2.pdf</b><span>3,2 Mo</span></div></div></div>
        <span class="dz-ap-note-time">17:30</span>
      </div>
      <div class="dz-ap-note">
        <span class="dz-ap-note-ico dz-ap-ico-warn"><i class="fas fa-exclamation-triangle"></i></span>
        <div class="dz-ap-note-body"><p>La synchronisation avec <b>Comptalib</b> a échoué 3 fois. Le jeton d'accès a expiré.</p><a class="dz-btn dz-btn-link dz-btn-sm" href="#">Reconnecter <i class="fas fa-arrow-right"></i></a></div>
        <span class="dz-ap-note-time">14:02</span>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 4
    dict(
        name="panneau de détail latéral",
        icon="fas fa-columns",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-split">
    <div class="dz-ap-panel dz-ap-behind">
      <div class="dz-ap-head"><div class="dz-ap-head-title"><h2 class="dz-ap-title">Commandes</h2><span class="dz-ap-sub">Septembre 2026</span></div></div>
      <div class="dz-ap-rows">
        <div class="dz-ap-row"><b>#FR-20928</b><span>Hélio Santé</span><span class="dz-badge dz-badge-success">Livrée</span><span class="dz-ap-num">1 280 €</span></div>
        <div class="dz-ap-row dz-ap-sel"><b>#FR-20931</b><span>Maison Oré</span><span class="dz-badge">En préparation</span><span class="dz-ap-num">2 947 €</span></div>
        <div class="dz-ap-row"><b>#FR-20933</b><span>Germe Paysages</span><span class="dz-badge dz-badge-warning">En attente</span><span class="dz-ap-num">412 €</span></div>
        <div class="dz-ap-row"><b>#FR-20935</b><span>Alizé Voyages</span><span class="dz-badge dz-badge-success">Livrée</span><span class="dz-ap-num">860 €</span></div>
        <div class="dz-ap-row"><b>#FR-20936</b><span>Quartz Labs</span><span class="dz-badge dz-badge-neutral">Brouillon</span><span class="dz-ap-num">3 100 €</span></div>
        <div class="dz-ap-row"><b>#FR-20940</b><span>Sillage</span><span class="dz-badge dz-badge-danger">Annulée</span><span class="dz-ap-num">—</span></div>
      </div>
    </div>
    <div class="dz-ap-drawer">
      <div class="dz-ap-drawer-top">
        <div class="dz-ap-drawer-nav"><span class="dz-ap-iconbtn" aria-label="Précédente"><i class="fas fa-chevron-up"></i></span><span class="dz-ap-iconbtn" aria-label="Suivante"><i class="fas fa-chevron-down"></i></span><span class="dz-ap-muted">2 sur 48</span></div>
        <div class="dz-ap-drawer-nav"><span class="dz-ap-iconbtn" aria-label="Ouvrir en plein écran"><i class="fas fa-expand-alt"></i></span><span class="dz-ap-iconbtn" aria-label="Fermer"><i class="fas fa-times"></i></span></div>
      </div>
      <div class="dz-ap-drawer-head">
        <span class="dz-badge">En préparation</span>
        <h3 class="dz-ap-drawer-title">Commande #FR-20931</h3>
        <span class="dz-ap-muted">Passée le 21 sept. 2026 à 14:32 · via la boutique</span>
        <div class="dz-cluster"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-truck"></i> Expédier</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-print"></i> Bon de livraison</a><span class="dz-ap-iconbtn" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></span></div>
      </div>
      <div class="dz-ap-tabs"><span class="dz-ap-tab dz-ap-on">Détails</span><span class="dz-ap-tab">Activité <b>6</b></span><span class="dz-ap-tab">Fichiers <b>2</b></span></div>
      <div class="dz-ap-props">
        <span class="dz-ap-prop-k">Client</span><div class="dz-ap-prop-v dz-ap-who"><span class="dz-avatar dz-avatar-sm">MO</span><div><b>Maison Oré</b><span>Clémence Laurent</span></div></div>
        <span class="dz-ap-prop-k">Livraison</span><span class="dz-ap-prop-v">12 quai de la Fosse, 44000 Nantes</span>
        <span class="dz-ap-prop-k">Transporteur</span><span class="dz-ap-prop-v">Colis Express · 48 h</span>
        <span class="dz-ap-prop-k">Responsable</span><div class="dz-ap-prop-v dz-ap-who"><span class="dz-avatar dz-avatar-sm">IC</span><div><b>Inès Carpentier</b></div></div>
        <span class="dz-ap-prop-k">Étiquettes</span><div class="dz-ap-prop-v dz-cluster"><span class="dz-badge dz-badge-neutral">B2B</span><span class="dz-badge dz-badge-neutral">Prioritaire</span></div>
      </div>
      <div class="dz-ap-lines">
        <div class="dz-ap-line"><span class="dz-ap-line-img"></span><div><b>Vase Figuier · grès émaillé</b><span>12 × 89,00 €</span></div><b>1 068 €</b></div>
        <div class="dz-ap-line"><span class="dz-ap-line-img dz-ap-line-img-b"></span><div><b>Suspension Lin naturel</b><span>8 × 199,00 €</span></div><b>1 592 €</b></div>
        <div class="dz-ap-line dz-ap-line-total"><span>Total TTC (dont TVA 491,17 €)</span><b>2 947,00 €</b></div>
      </div>
      <div class="dz-ap-mini-timeline">
        <div class="dz-ap-tl dz-ap-done"><b>Paiement confirmé</b><span>21 sept., 14:33</span></div>
        <div class="dz-ap-tl dz-ap-now"><b>Préparation en cours</b><span>Entrepôt de Rezé · Malik H.</span></div>
        <div class="dz-ap-tl"><b>Expédition</b><span>Prévue le 24 sept.</span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 5
    dict(
        name="formulaire en sections",
        icon="fas fa-align-left",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-form-layout">
    <div class="dz-ap-form-nav">
      <span class="dz-ap-label">Fiche entreprise</span>
      <a class="dz-ap-form-link dz-ap-done" href="#generales"><i class="fas fa-check-circle"></i> Informations générales</a>
      <a class="dz-ap-form-link dz-ap-on" href="#adresse"><i class="far fa-dot-circle"></i> Adresse et facturation</a>
      <a class="dz-ap-form-link" href="#preferences"><i class="far fa-circle"></i> Préférences</a>
      <a class="dz-ap-form-link dz-ap-danger" href="#danger"><i class="fas fa-exclamation-triangle"></i> Zone sensible</a>
      <div class="dz-ap-form-progress"><span>Profil complété à 72 %</span><div class="dz-progress"><span style="--v:72%"></span></div></div>
    </div>
    <div class="dz-ap-form-sections">
      <div class="dz-ap-panel dz-ap-fsec" id="generales">
        <div class="dz-ap-fsec-head"><h3 class="dz-ap-fsec-title">Informations générales</h3><p>Ces informations apparaissent sur vos devis et factures.</p></div>
        <div class="dz-ap-fields">
          <div class="dz-ap-field"><span class="dz-ap-flabel">Raison sociale <b>*</b></span><div class="dz-ap-input">Atelier Lune SARL</div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">Nom commercial</span><div class="dz-ap-input">Atelier Lune</div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">SIRET <b>*</b></span><div class="dz-ap-input dz-ap-invalid">812 345 678 0001</div><span class="dz-ap-help dz-ap-help-err"><i class="fas fa-exclamation-circle"></i> Le SIRET doit comporter 14 chiffres.</span></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">N° de TVA intracommunautaire</span><div class="dz-ap-input dz-ap-valid">FR 32 812345678 <i class="fas fa-check-circle"></i></div><span class="dz-ap-help">Vérifié automatiquement auprès du registre européen.</span></div>
        </div>
      </div>
      <div class="dz-ap-panel dz-ap-fsec" id="adresse">
        <div class="dz-ap-fsec-head"><h3 class="dz-ap-fsec-title">Adresse et facturation</h3><p>Adresse du siège et coordonnées de facturation.</p></div>
        <div class="dz-ap-fields">
          <div class="dz-ap-field dz-ap-span"><span class="dz-ap-flabel">Adresse</span><div class="dz-ap-input dz-ap-focus">18 rue des Tanneurs<span class="dz-ap-caret-blink"></span></div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">Code postal</span><div class="dz-ap-input">69002</div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">Ville</span><div class="dz-ap-input">Lyon</div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">Délai de paiement</span><div class="dz-ap-input dz-ap-select">30 jours fin de mois <i class="fas fa-chevron-down"></i></div></div>
          <div class="dz-ap-field"><span class="dz-ap-flabel">E-mail de facturation</span><div class="dz-ap-input dz-ap-ph">compta@exemple.fr</div></div>
        </div>
      </div>
      <div class="dz-ap-panel dz-ap-fsec" id="preferences">
        <div class="dz-ap-fsec-head"><h3 class="dz-ap-fsec-title">Préférences</h3><p>Choisissez le modèle de document par défaut.</p></div>
        <div class="dz-ap-radios">
          <div class="dz-ap-radio dz-ap-on"><span class="dz-ap-radio-dot"></span><div><b>Classique</b><span>Sobre, idéal pour l'administration</span></div></div>
          <div class="dz-ap-radio"><span class="dz-ap-radio-dot"></span><div><b>Moderne</b><span>Avec votre logo en couleur</span></div></div>
          <div class="dz-ap-radio"><span class="dz-ap-radio-dot"></span><div><b>Minimal</b><span>Uniquement l'essentiel</span></div></div>
        </div>
      </div>
      <div class="dz-ap-savebar"><span><span class="dz-ap-dot-warn"></span> 3 modifications non enregistrées</span><div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Annuler</a><a class="dz-btn dz-btn-sm" href="#">Enregistrer <span class="dz-ap-kbd-in">Ctrl S</span></a></div></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 6
    dict(
        name="assistant de création",
        icon="fas fa-hat-wizard",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-wizard">
    <div class="dz-ap-wiz-side">
      <span class="dz-ap-label">Nouveau projet</span>
      <div class="dz-ap-wiz-steps">
        <div class="dz-ap-wiz-step dz-ap-done"><span class="dz-ap-wiz-dot"><i class="fas fa-check"></i></span><div><b>Nom et client</b><span>Refonte boutique · Maison Oré</span></div></div>
        <div class="dz-ap-wiz-step dz-ap-done"><span class="dz-ap-wiz-dot"><i class="fas fa-check"></i></span><div><b>Équipe</b><span>4 membres</span></div></div>
        <div class="dz-ap-wiz-step dz-ap-now"><span class="dz-ap-wiz-dot">3</span><div><b>Modèle</b><span>Structure de départ</span></div></div>
        <div class="dz-ap-wiz-step"><span class="dz-ap-wiz-dot">4</span><div><b>Budget</b><span>Forfait ou régie</span></div></div>
        <div class="dz-ap-wiz-step"><span class="dz-ap-wiz-dot">5</span><div><b>Vérification</b><span>Récapitulatif</span></div></div>
      </div>
      <div class="dz-ap-wiz-help"><i class="fas fa-life-ring"></i><span>Besoin d'aide ? Un conseiller vous répond en 2 min.</span></div>
    </div>
    <div class="dz-ap-wiz-main">
      <div class="dz-ap-wiz-head"><span class="dz-ap-muted">Étape 3 sur 5</span><h2 class="dz-ap-title-lg">Choisissez un modèle de projet</h2><p class="dz-ap-muted">Vous pourrez tout modifier ensuite. Les modèles incluent tâches, jalons et automatisations.</p></div>
      <div class="dz-ap-templates">
        <div class="dz-ap-tpl dz-ap-on"><div class="dz-ap-tpl-art dz-ap-art-a"><span></span><span></span><span></span></div><div class="dz-ap-tpl-info"><b>Site e-commerce</b><span>38 tâches · 6 jalons · 8 semaines</span></div><span class="dz-ap-tpl-check"><i class="fas fa-check"></i></span></div>
        <div class="dz-ap-tpl"><div class="dz-ap-tpl-art dz-ap-art-b"><span></span><span></span><span></span></div><div class="dz-ap-tpl-info"><b>Site vitrine</b><span>21 tâches · 4 jalons · 4 semaines</span></div><span class="dz-ap-tpl-check"><i class="fas fa-check"></i></span></div>
        <div class="dz-ap-tpl"><div class="dz-ap-tpl-art dz-ap-art-c"><span></span><span></span><span></span></div><div class="dz-ap-tpl-info"><b>Identité visuelle</b><span>16 tâches · 3 jalons · 3 semaines</span></div><span class="dz-ap-tpl-check"><i class="fas fa-check"></i></span></div>
        <div class="dz-ap-tpl dz-ap-tpl-blank"><i class="fas fa-plus"></i><b>Partir de zéro</b><span>Projet vide</span></div>
      </div>
      <div class="dz-ap-wiz-foot"><a class="dz-btn dz-btn-ghost" href="#"><i class="fas fa-arrow-left"></i> Retour</a><div class="dz-ap-wiz-bar"><span class="dz-ap-on"></span><span class="dz-ap-on"></span><span class="dz-ap-on"></span><span></span><span></span></div><a class="dz-btn" href="#">Continuer <i class="fas fa-arrow-right"></i></a></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 7
    dict(
        name="accueil d'application",
        icon="fas fa-home",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-home-head">
    <div><span class="dz-ap-muted">Jeudi 24 septembre 2026</span><h2 class="dz-ap-title-lg">Bonjour Camille</h2><p class="dz-ap-muted">Vous avez <b>4 tâches</b> aujourd'hui et <b>2 validations</b> en attente.</p></div>
    <div class="dz-ap-search dz-ap-search-lg"><i class="fas fa-search"></i><span>Rechercher ou lancer une commande…</span><span class="dz-kbd">Ctrl K</span></div>
  </div>
  <div class="dz-ap-shortcuts">
    <a class="dz-ap-shortcut" href="#"><span class="dz-ap-sc-ico dz-ap-c1"><i class="fas fa-file-invoice"></i></span><b>Nouvelle facture</b><span class="dz-kbd">F</span></a>
    <a class="dz-ap-shortcut" href="#"><span class="dz-ap-sc-ico dz-ap-c2"><i class="fas fa-user-plus"></i></span><b>Ajouter un client</b><span class="dz-kbd">C</span></a>
    <a class="dz-ap-shortcut" href="#"><span class="dz-ap-sc-ico dz-ap-c3"><i class="fas fa-tasks"></i></span><b>Créer une tâche</b><span class="dz-kbd">T</span></a>
    <a class="dz-ap-shortcut" href="#"><span class="dz-ap-sc-ico dz-ap-c4"><i class="fas fa-clock"></i></span><b>Saisir du temps</b><span class="dz-kbd">H</span></a>
  </div>
  <div class="dz-ap-home-grid">
    <div class="dz-ap-panel dz-ap-card">
      <div class="dz-ap-card-head"><h3 class="dz-ap-card-title">À faire aujourd'hui</h3><span class="dz-ap-muted">1 / 5</span></div>
      <div class="dz-ap-todos">
        <div class="dz-ap-todo dz-ap-done"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span><span class="dz-ap-todo-t">Envoyer le devis à Norden</span><span class="dz-ap-due">Fait</span></div>
        <div class="dz-ap-todo"><span class="dz-ap-check"></span><span class="dz-ap-todo-t">Valider la maquette mobile</span><span class="dz-ap-due dz-ap-due-late">16:00</span></div>
        <div class="dz-ap-todo"><span class="dz-ap-check"></span><span class="dz-ap-todo-t">Relancer Maison Oré (facture en retard)</span><span class="dz-ap-due">Aujourd'hui</span></div>
        <div class="dz-ap-todo"><span class="dz-ap-check"></span><span class="dz-ap-todo-t">Préparer le point hebdo</span><span class="dz-ap-due">17:30</span></div>
        <div class="dz-ap-todo"><span class="dz-ap-check"></span><span class="dz-ap-todo-t">Répondre à Léa sur la charte</span><span class="dz-ap-due">Demain</span></div>
      </div>
    </div>
    <div class="dz-ap-panel dz-ap-card">
      <div class="dz-ap-card-head"><h3 class="dz-ap-card-title">Agenda</h3><a class="dz-btn dz-btn-link dz-btn-sm" href="#">Tout voir</a></div>
      <div class="dz-ap-agenda">
        <div class="dz-ap-event dz-ap-past"><span class="dz-ap-ev-time">09:30</span><div class="dz-ap-ev-body"><b>Point équipe</b><span>15 min · Visio</span></div></div>
        <div class="dz-ap-event dz-ap-live"><span class="dz-ap-ev-time">11:00</span><div class="dz-ap-ev-body"><b>Atelier client Maison Oré</b><span>En cours · Salle Lumière</span></div><a class="dz-btn dz-btn-sm" href="#">Rejoindre</a></div>
        <div class="dz-ap-event"><span class="dz-ap-ev-time">14:00</span><div class="dz-ap-ev-body"><b>Revue budgets T4</b><span>1 h · Nadia, Marc</span></div></div>
      </div>
    </div>
    <div class="dz-ap-panel dz-ap-card">
      <div class="dz-ap-card-head"><h3 class="dz-ap-card-title">Activité récente</h3></div>
      <div class="dz-ap-feed">
        <div class="dz-ap-feed-item"><span class="dz-avatar dz-avatar-sm">JF</span><p><b>Julien</b> a terminé <b>Intégration panier</b></p><span class="dz-ap-muted">8 min</span></div>
        <div class="dz-ap-feed-item"><span class="dz-avatar dz-avatar-sm">SB</span><p><b>Sarah</b> a commenté <b>Devis D-118</b></p><span class="dz-ap-muted">32 min</span></div>
        <div class="dz-ap-feed-item"><span class="dz-avatar dz-avatar-sm">LS</span><p><b>Léa</b> a ajouté 12 fichiers à <b>Photos produits</b></p><span class="dz-ap-muted">1 h</span></div>
      </div>
    </div>
    <div class="dz-ap-panel dz-ap-card">
      <div class="dz-ap-card-head"><h3 class="dz-ap-card-title">Vos projets</h3></div>
      <div class="dz-ap-projs">
        <div class="dz-ap-proj"><div class="dz-ap-proj-top"><b>Refonte boutique</b><span>68 %</span></div><div class="dz-progress"><span style="--v:68%"></span></div><span class="dz-ap-muted">Livraison le 14 oct.</span></div>
        <div class="dz-ap-proj"><div class="dz-ap-proj-top"><b>Salon Maison 2026</b><span>34 %</span></div><div class="dz-progress"><span style="--v:34%"></span></div><span class="dz-ap-muted">Livraison le 2 nov.</span></div>
        <div class="dz-ap-proj"><div class="dz-ap-proj-top"><b>Identité Germe</b><span>91 %</span></div><div class="dz-progress"><span style="--v:91%"></span></div><span class="dz-ap-muted">Livraison le 30 sept.</span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 8
    dict(
        name="recherche globale",
        icon="fas fa-search",
        wrap="none",
        html="""
<div class="dz-ap-stage dz-ap-stage-dim">
  <div class="dz-ap-panel dz-ap-gsearch">
    <div class="dz-ap-gs-input"><i class="fas fa-search"></i><span class="dz-ap-gs-query">facture lune<span class="dz-ap-caret-blink"></span></span><span class="dz-kbd">Échap</span></div>
    <div class="dz-ap-gs-scopes"><span class="dz-ap-scope dz-ap-on">Tout <b>24</b></span><span class="dz-ap-scope"><i class="fas fa-file-invoice"></i> Factures <b>9</b></span><span class="dz-ap-scope"><i class="fas fa-building"></i> Clients <b>2</b></span><span class="dz-ap-scope"><i class="fas fa-file-alt"></i> Documents <b>11</b></span><span class="dz-ap-scope"><i class="fas fa-user"></i> Personnes <b>2</b></span></div>
    <div class="dz-ap-gs-body">
      <div class="dz-ap-gs-results">
        <span class="dz-ap-gs-group">Factures</span>
        <div class="dz-ap-gs-item dz-ap-on"><span class="dz-ap-gs-ico"><i class="fas fa-file-invoice"></i></span><div class="dz-ap-gs-text"><b><mark>Facture</mark> F-2026-0412 · Atelier <mark>Lune</mark></b><span>5 112,00 € · Payée le 18 sept.</span></div><span class="dz-kbd">↵</span></div>
        <div class="dz-ap-gs-item"><span class="dz-ap-gs-ico"><i class="fas fa-file-invoice"></i></span><div class="dz-ap-gs-text"><b><mark>Facture</mark> F-2026-0388 · Atelier <mark>Lune</mark></b><span>2 340,00 € · Payée le 12 août</span></div></div>
        <span class="dz-ap-gs-group">Clients</span>
        <div class="dz-ap-gs-item"><span class="dz-avatar dz-avatar-sm">AL</span><div class="dz-ap-gs-text"><b>Atelier <mark>Lune</mark></b><span>Client depuis 2023 · 14 factures</span></div></div>
        <span class="dz-ap-gs-group">Documents</span>
        <div class="dz-ap-gs-item"><span class="dz-ap-gs-ico"><i class="fas fa-file-alt"></i></span><div class="dz-ap-gs-text"><b>Conditions de <mark>facture</mark>tion 2026</b><span>Juridique · modifié par Marc D.</span></div></div>
        <div class="dz-ap-gs-item"><span class="dz-ap-gs-ico"><i class="fas fa-file-pdf"></i></span><div class="dz-ap-gs-text"><b>Contrat cadre Atelier <mark>Lune</mark>.pdf</b><span>Signé le 4 janv. 2026</span></div></div>
      </div>
      <div class="dz-ap-gs-preview">
        <div class="dz-ap-gs-pv-head"><span class="dz-badge dz-badge-success">Payée</span><span class="dz-ap-muted">F-2026-0412</span></div>
        <b class="dz-ap-gs-pv-amount">5 112,00 €</b>
        <div class="dz-ap-gs-kv"><span>Client</span><b>Atelier Lune</b></div>
        <div class="dz-ap-gs-kv"><span>Émise le</span><b>3 sept. 2026</b></div>
        <div class="dz-ap-gs-kv"><span>Échéance</span><b>3 oct. 2026</b></div>
        <div class="dz-ap-gs-kv"><span>Paiement</span><b>Virement · 18 sept.</b></div>
        <div class="dz-cluster"><a class="dz-btn dz-btn-sm" href="#">Ouvrir</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-download"></i> PDF</a></div>
      </div>
    </div>
    <div class="dz-ap-gs-foot"><span><span class="dz-kbd">↑</span><span class="dz-kbd">↓</span> naviguer</span><span><span class="dz-kbd">↵</span> ouvrir</span><span><span class="dz-kbd">Tab</span> filtrer</span><span class="dz-ap-gs-time">24 résultats en 38 ms</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 9
    dict(
        name="éditeur de texte riche",
        icon="fas fa-edit",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-editor">
    <div class="dz-ap-ed-bar">
      <div class="dz-ap-ed-group"><span class="dz-ap-tool" aria-label="Annuler"><i class="fas fa-undo"></i></span><span class="dz-ap-tool" aria-label="Rétablir"><i class="fas fa-redo"></i></span></div>
      <div class="dz-ap-ed-group"><span class="dz-ap-tool dz-ap-tool-select">Titre 2 <i class="fas fa-chevron-down"></i></span></div>
      <div class="dz-ap-ed-group"><span class="dz-ap-tool dz-ap-on" aria-label="Gras"><i class="fas fa-bold"></i></span><span class="dz-ap-tool" aria-label="Italique"><i class="fas fa-italic"></i></span><span class="dz-ap-tool" aria-label="Souligné"><i class="fas fa-underline"></i></span><span class="dz-ap-tool" aria-label="Barré"><i class="fas fa-strikethrough"></i></span></div>
      <div class="dz-ap-ed-group"><span class="dz-ap-tool" aria-label="Liste"><i class="fas fa-list-ul"></i></span><span class="dz-ap-tool" aria-label="Liste numérotée"><i class="fas fa-list-ol"></i></span><span class="dz-ap-tool" aria-label="Cases à cocher"><i class="fas fa-tasks"></i></span></div>
      <div class="dz-ap-ed-group"><span class="dz-ap-tool" aria-label="Lien"><i class="fas fa-link"></i></span><span class="dz-ap-tool" aria-label="Image"><i class="fas fa-image"></i></span><span class="dz-ap-tool" aria-label="Tableau"><i class="fas fa-table"></i></span><span class="dz-ap-tool" aria-label="Code"><i class="fas fa-code"></i></span></div>
      <span class="dz-ap-tool dz-ap-tool-ai"><i class="fas fa-magic"></i> Améliorer</span>
      <div class="dz-ap-ed-right"><div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">CL</span><span class="dz-avatar dz-avatar-sm">JF</span></div><span class="dz-ap-saved"><i class="fas fa-check"></i> Enregistré</span></div>
    </div>
    <div class="dz-ap-ed-body">
      <div class="dz-ap-doc">
        <span class="dz-ap-doc-crumb">Projets / Refonte boutique / Notes</span>
        <h1 class="dz-ap-doc-title">Compte rendu — atelier du 23 septembre</h1>
        <div class="dz-ap-doc-meta"><span class="dz-badge dz-badge-neutral">Réunion</span><span>Camille Laurent · 6 min de lecture</span></div>
        <p>L'atelier a réuni l'équipe de <b>Maison Oré</b> et la nôtre pour arbitrer les derniers choix avant le développement. <span class="dz-ap-hl">Le client souhaite ouvrir la boutique avant le salon du 2 novembre</span>, ce qui impose de figer le périmètre cette semaine.</p>
        <h2 class="dz-ap-doc-h2">Décisions</h2>
        <div class="dz-ap-doc-checks">
          <div class="dz-ap-doc-check dz-ap-done"><span class="dz-ap-check dz-ap-on"><i class="fas fa-check"></i></span><span>Paiement en trois fois sans frais dès le lancement</span></div>
          <div class="dz-ap-doc-check"><span class="dz-ap-check"></span><span>Retrait en atelier à Lyon — à confirmer par Clémence</span></div>
        </div>
        <blockquote class="dz-ap-doc-quote">« Chaque fiche produit doit raconter l'atelier, pas seulement le prix. » — Clémence</blockquote>
        <pre class="dz-ap-doc-code">livraison.delai_max = 48h   # engagement contractuel</pre>
      </div>
      <div class="dz-ap-margin">
        <div class="dz-ap-comment"><div class="dz-ap-comment-head"><span class="dz-avatar dz-avatar-sm">JF</span><b>Julien</b><span class="dz-ap-muted">10:24</span></div><p>On peut tenir le 2 novembre si les photos arrivent avant le 5 octobre.</p><span class="dz-ap-comment-reply">Répondre · Résoudre</span></div>
        <div class="dz-ap-outline"><span class="dz-ap-label">Sommaire</span><span class="dz-ap-ol-item dz-ap-on">Contexte</span><span class="dz-ap-ol-item">Décisions</span><span class="dz-ap-ol-item">Prochaines étapes</span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 10
    dict(
        name="constructeur de formulaire",
        icon="fas fa-clipboard-list",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-builder">
    <div class="dz-ap-bd-top">
      <div class="dz-ap-bd-name"><i class="fas fa-clipboard-list"></i><b>Demande de devis</b><span class="dz-badge dz-badge-neutral">Brouillon</span></div>
      <div class="dz-ap-tabs dz-ap-tabs-inline"><span class="dz-ap-tab dz-ap-on">Champs</span><span class="dz-ap-tab">Logique</span><span class="dz-ap-tab">Apparence</span><span class="dz-ap-tab">Réponses <b>128</b></span></div>
      <div class="dz-ap-actions"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-eye"></i> Aperçu</a><a class="dz-btn dz-btn-sm" href="#">Publier</a></div>
    </div>
    <div class="dz-ap-bd-body">
      <div class="dz-ap-palette">
        <span class="dz-ap-label">Ajouter un champ</span>
        <span class="dz-ap-pal"><i class="fas fa-font"></i> Texte court</span>
        <span class="dz-ap-pal"><i class="fas fa-align-left"></i> Paragraphe</span>
        <span class="dz-ap-pal"><i class="fas fa-at"></i> E-mail</span>
        <span class="dz-ap-pal"><i class="fas fa-phone"></i> Téléphone</span>
        <span class="dz-ap-pal dz-ap-drag"><i class="fas fa-list-ul"></i> Choix multiple</span>
        <span class="dz-ap-pal"><i class="fas fa-calendar-alt"></i> Date</span>
        <span class="dz-ap-pal"><i class="fas fa-star"></i> Note</span>
        <span class="dz-ap-pal"><i class="fas fa-paperclip"></i> Fichier</span>
      </div>
      <div class="dz-ap-canvas">
        <div class="dz-ap-form-card">
          <h3 class="dz-ap-fc-title">Parlons de votre projet</h3>
          <p class="dz-ap-muted">Réponse sous 48 h ouvrées.</p>
          <div class="dz-ap-bfield"><span class="dz-ap-grip"><i class="fas fa-grip-vertical"></i></span><span class="dz-ap-flabel">Nom complet <b>*</b></span><div class="dz-ap-input dz-ap-ph">Jeanne Martin</div></div>
          <div class="dz-ap-bfield dz-ap-selected"><span class="dz-ap-grip"><i class="fas fa-grip-vertical"></i></span><span class="dz-ap-bfield-tag">E-mail</span><span class="dz-ap-flabel">E-mail professionnel <b>*</b></span><div class="dz-ap-input dz-ap-ph">jeanne@entreprise.fr</div><div class="dz-ap-bfield-tools"><span aria-label="Dupliquer"><i class="far fa-copy"></i></span><span aria-label="Supprimer"><i class="far fa-trash-alt"></i></span></div></div>
          <div class="dz-ap-dropline"><span>Déposer ici</span></div>
          <div class="dz-ap-bfield"><span class="dz-ap-grip"><i class="fas fa-grip-vertical"></i></span><span class="dz-ap-flabel">Budget estimé</span><div class="dz-cluster"><span class="dz-ap-pill">&lt; 5 k€</span><span class="dz-ap-pill dz-ap-on">5 – 20 k€</span><span class="dz-ap-pill">&gt; 20 k€</span></div></div>
        </div>
      </div>
      <div class="dz-ap-inspector">
        <span class="dz-ap-label">Propriétés du champ</span>
        <div class="dz-ap-field"><span class="dz-ap-flabel">Libellé</span><div class="dz-ap-input">E-mail professionnel</div></div>
        <div class="dz-ap-field"><span class="dz-ap-flabel">Texte d'exemple</span><div class="dz-ap-input">jeanne@entreprise.fr</div></div>
        <div class="dz-ap-toggle"><span>Obligatoire</span><span class="dz-ap-switch dz-ap-on"></span></div>
        <div class="dz-ap-toggle"><span>Refuser les adresses gratuites</span><span class="dz-ap-switch dz-ap-on"></span></div>
        <div class="dz-ap-toggle"><span>Masquer si client connu</span><span class="dz-ap-switch"></span></div>
        <div class="dz-ap-field"><span class="dz-ap-flabel">Message d'erreur</span><div class="dz-ap-input">Merci d'indiquer une adresse professionnelle.</div></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 11
    dict(
        name="tableau croisé dynamique",
        icon="fas fa-th",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel">
    <div class="dz-ap-head">
      <div class="dz-ap-head-title"><h2 class="dz-ap-title">Chiffre d'affaires par région</h2><span class="dz-ap-sub">Exercice 2026 · en k€ HT</span></div>
      <div class="dz-ap-actions"><span class="dz-ap-seg"><span class="dz-ap-on">Valeurs</span><span>% du total</span><span>Écart N-1</span></span><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-download"></i> Exporter</a></div>
    </div>
    <div class="dz-ap-pivot-conf">
      <div class="dz-ap-pv-zone"><span class="dz-ap-label">Lignes</span><span class="dz-ap-token"><i class="fas fa-grip-vertical"></i> Région</span><span class="dz-ap-token"><i class="fas fa-grip-vertical"></i> Ville</span></div>
      <div class="dz-ap-pv-zone"><span class="dz-ap-label">Colonnes</span><span class="dz-ap-token"><i class="fas fa-grip-vertical"></i> Trimestre</span></div>
      <div class="dz-ap-pv-zone"><span class="dz-ap-label">Valeurs</span><span class="dz-ap-token dz-ap-token-val"><i class="fas fa-grip-vertical"></i> Somme de CA</span></div>
    </div>
    <div class="dz-ap-scroll">
      <div class="dz-ap-table dz-ap-t-pivot">
        <div class="dz-ap-tr dz-ap-th"><span>Région / ville</span><span class="dz-ap-num">T1</span><span class="dz-ap-num">T2</span><span class="dz-ap-num">T3</span><span class="dz-ap-num">T4 (prév.)</span><span class="dz-ap-num">Total</span></div>
        <div class="dz-ap-tr dz-ap-grp"><span><i class="fas fa-chevron-down"></i> Auvergne-Rhône-Alpes</span><span class="dz-ap-num dz-ap-heat" style="--a:.55">412</span><span class="dz-ap-num dz-ap-heat" style="--a:.7">468</span><span class="dz-ap-num dz-ap-heat" style="--a:.85">521</span><span class="dz-ap-num dz-ap-heat" style="--a:.95">560</span><span class="dz-ap-num dz-ap-tot">1 961</span></div>
        <div class="dz-ap-tr dz-ap-sub-row"><span>Lyon</span><span class="dz-ap-num dz-ap-heat" style="--a:.4">298</span><span class="dz-ap-num dz-ap-heat" style="--a:.5">341</span><span class="dz-ap-num dz-ap-heat" style="--a:.6">380</span><span class="dz-ap-num dz-ap-heat" style="--a:.65">402</span><span class="dz-ap-num">1 421</span></div>
        <div class="dz-ap-tr dz-ap-sub-row"><span>Grenoble</span><span class="dz-ap-num dz-ap-heat" style="--a:.12">114</span><span class="dz-ap-num dz-ap-heat" style="--a:.14">127</span><span class="dz-ap-num dz-ap-heat" style="--a:.16">141</span><span class="dz-ap-num dz-ap-heat" style="--a:.18">158</span><span class="dz-ap-num">540</span></div>
        <div class="dz-ap-tr dz-ap-grp"><span><i class="fas fa-chevron-down"></i> Pays de la Loire</span><span class="dz-ap-num dz-ap-heat" style="--a:.3">236</span><span class="dz-ap-num dz-ap-heat" style="--a:.34">258</span><span class="dz-ap-num dz-ap-heat" style="--a:.3">241</span><span class="dz-ap-num dz-ap-heat" style="--a:.42">305</span><span class="dz-ap-num dz-ap-tot">1 040</span></div>
        <div class="dz-ap-tr dz-ap-sub-row"><span>Nantes</span><span class="dz-ap-num dz-ap-heat" style="--a:.24">201</span><span class="dz-ap-num dz-ap-heat" style="--a:.27">219</span><span class="dz-ap-num dz-ap-heat" style="--a:.24">198</span><span class="dz-ap-num dz-ap-heat" style="--a:.33">256</span><span class="dz-ap-num">874</span></div>
        <div class="dz-ap-tr dz-ap-sub-row"><span>Angers</span><span class="dz-ap-num dz-ap-heat" style="--a:.05">35</span><span class="dz-ap-num dz-ap-heat" style="--a:.06">39</span><span class="dz-ap-num dz-ap-heat" style="--a:.06">43</span><span class="dz-ap-num dz-ap-heat" style="--a:.07">49</span><span class="dz-ap-num">166</span></div>
        <div class="dz-ap-tr dz-ap-grp"><span><i class="fas fa-chevron-right"></i> Hauts-de-France</span><span class="dz-ap-num dz-ap-heat" style="--a:.2">164</span><span class="dz-ap-num dz-ap-heat" style="--a:.22">179</span><span class="dz-ap-num dz-ap-heat" style="--a:.26">206</span><span class="dz-ap-num dz-ap-heat" style="--a:.3">231</span><span class="dz-ap-num dz-ap-tot">780</span></div>
        <div class="dz-ap-tr dz-ap-grp"><span><i class="fas fa-chevron-right"></i> Île-de-France</span><span class="dz-ap-num dz-ap-heat" style="--a:.62">488</span><span class="dz-ap-num dz-ap-heat" style="--a:.66">502</span><span class="dz-ap-num dz-ap-heat" style="--a:.58">471</span><span class="dz-ap-num dz-ap-heat" style="--a:.8">590</span><span class="dz-ap-num dz-ap-tot">2 051</span></div>
        <div class="dz-ap-tr dz-ap-total"><span>Total général</span><span class="dz-ap-num">1 300</span><span class="dz-ap-num">1 407</span><span class="dz-ap-num">1 439</span><span class="dz-ap-num">1 686</span><span class="dz-ap-num">5 832</span></div>
      </div>
    </div>
    <div class="dz-ap-foot"><div class="dz-ap-legend"><span>Faible</span><span class="dz-ap-legend-bar"></span><span>Élevé</span></div><span class="dz-ap-muted">Source : ventes synchronisées le 24 sept. à 08:00</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 12
    dict(
        name="erreur applicative",
        icon="fas fa-bug",
        wrap="none",
        html="""
<div class="dz-ap-stage dz-ap-stage-center">
  <div class="dz-ap-panel dz-ap-error">
    <div class="dz-ap-err-art"><span class="dz-ap-err-plug dz-ap-err-plug-a"><i class="fas fa-plug"></i></span><span class="dz-ap-err-spark"><i class="fas fa-bolt"></i></span><span class="dz-ap-err-plug dz-ap-err-plug-b"><i class="fas fa-plug"></i></span></div>
    <span class="dz-ap-err-code">Erreur 500 · Erreur interne</span>
    <h2 class="dz-ap-title-lg">Quelque chose s'est mal passé de notre côté</h2>
    <p class="dz-ap-muted">Vos données sont intactes. L'équipe technique a été prévenue automatiquement ; vous pouvez réessayer dans quelques instants.</p>
    <div class="dz-cluster dz-ap-err-acts"><a class="dz-btn" href="#"><i class="fas fa-redo"></i> Réessayer</a><a class="dz-btn dz-btn-ghost" href="#">Retour au tableau de bord</a></div>
    <details class="dz-ap-err-details">
      <summary>Détails techniques</summary>
      <div class="dz-ap-err-trace">
        <div class="dz-ap-err-kv"><span>Identifiant</span><b class="dz-mono">req_8f2c41a9e7</b><span class="dz-ap-copy dz-copy" aria-label="Copier l'identifiant"><i class="far fa-copy"></i></span></div>
        <div class="dz-ap-err-kv"><span>Horodatage</span><b class="dz-mono">2026-09-24 10:42:18 UTC+2</b></div>
        <pre class="dz-ap-err-pre">TimeoutError: la requête a dépassé 30 000 ms
  at invoices.generate (services/pdf.js:214)
  at queue.process (workers/pdf.js:48)</pre>
      </div>
    </details>
    <a class="dz-ap-err-status" href="#"><span class="dz-ap-dot-warn"></span> Incident en cours · voir la page d'état</a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 13
    dict(
        name="maintenance planifiée",
        icon="fas fa-tools",
        wrap="none",
        html="""
<div class="dz-ap-stage dz-ap-stage-center">
  <div class="dz-ap-maint">
    <div class="dz-ap-maint-art"><span class="dz-ap-gear dz-ap-gear-a"><i class="fas fa-cog"></i></span><span class="dz-ap-gear dz-ap-gear-b"><i class="fas fa-cog"></i></span></div>
    <span class="dz-badge dz-badge-warning"><span class="dz-ap-dot"></span> Maintenance en cours</span>
    <h2 class="dz-ap-title-xl">On améliore les fondations</h2>
    <p class="dz-ap-muted">Nous migrons la base de données vers une infrastructure plus rapide. L'application sera de retour à <b>23:30</b> (heure de Paris).</p>
    <div class="dz-ap-maint-count"><span class="dz-ap-muted">Retour estimé dans</span><b class="dz-countdown">2026-10-06 23:30</b></div>
    <div class="dz-ap-maint-steps">
      <div class="dz-ap-mstep dz-ap-done"><i class="fas fa-check-circle"></i><span>Sauvegarde complète</span><em>22:04</em></div>
      <div class="dz-ap-mstep dz-ap-done"><i class="fas fa-check-circle"></i><span>Copie des données</span><em>22:41</em></div>
      <div class="dz-ap-mstep dz-ap-now"><span class="dz-ap-spin"></span><span>Vérification de l'intégrité</span><em>64 %</em></div>
      <div class="dz-ap-mstep"><i class="far fa-circle"></i><span>Remise en service</span><em>—</em></div>
    </div>
    <div class="dz-ap-maint-foot"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-bell"></i> Me prévenir du retour</a><a class="dz-btn dz-btn-link dz-btn-sm" href="#">Page d'état du service</a></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 14
    dict(
        name="journaux (logs)",
        icon="fas fa-stream",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-panel dz-ap-logs">
    <div class="dz-ap-head">
      <div class="dz-ap-head-title"><h2 class="dz-ap-title">Journaux</h2><span class="dz-ap-sub">api-production · 1 264 évènements sur 1 h</span></div>
      <div class="dz-ap-actions"><span class="dz-ap-live"><span class="dz-ap-live-dot"></span> En direct</span><span class="dz-ap-range"><i class="far fa-clock"></i> Dernière heure <i class="fas fa-chevron-down"></i></span></div>
    </div>
    <div class="dz-ap-toolbar">
      <div class="dz-ap-search dz-ap-mono-search"><i class="fas fa-terminal"></i><span>service:paiements AND niveau:erreur</span></div>
      <div class="dz-ap-levels"><span class="dz-ap-lvl dz-ap-lvl-err dz-ap-on">Erreur <b>12</b></span><span class="dz-ap-lvl dz-ap-lvl-warn dz-ap-on">Avert. <b>48</b></span><span class="dz-ap-lvl dz-ap-lvl-info dz-ap-on">Info <b>1 204</b></span><span class="dz-ap-lvl dz-ap-lvl-dbg">Débogage</span></div>
    </div>
    <div class="dz-ap-histo">
      <span style="--i:30%;--w:4%;--e:0%"></span><span style="--i:36%;--w:6%;--e:0%"></span><span style="--i:34%;--w:4%;--e:2%"></span><span style="--i:42%;--w:8%;--e:0%"></span><span style="--i:40%;--w:6%;--e:0%"></span><span style="--i:38%;--w:5%;--e:0%"></span><span style="--i:46%;--w:10%;--e:6%"></span><span style="--i:60%;--w:14%;--e:12%"></span><span style="--i:52%;--w:8%;--e:4%"></span><span style="--i:44%;--w:6%;--e:0%"></span><span style="--i:40%;--w:4%;--e:0%"></span><span style="--i:42%;--w:5%;--e:0%"></span><span style="--i:38%;--w:4%;--e:0%"></span><span style="--i:44%;--w:6%;--e:2%"></span><span style="--i:48%;--w:5%;--e:0%"></span><span style="--i:46%;--w:4%;--e:0%"></span><span style="--i:50%;--w:6%;--e:0%"></span><span style="--i:42%;--w:4%;--e:0%"></span><span style="--i:40%;--w:4%;--e:0%"></span><span style="--i:45%;--w:6%;--e:0%"></span>
    </div>
    <div class="dz-ap-scroll">
      <div class="dz-ap-loglines">
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:18.204</span><span class="dz-ap-lv dz-ap-lvl-err">ERR</span><span class="dz-ap-svc">paiements</span><span class="dz-ap-msg">Échec de capture pour pi_7Hk2 : délai dépassé après 30 000 ms</span></div>
        <div class="dz-ap-log dz-ap-open"><span class="dz-ap-ts">10:42:17.981</span><span class="dz-ap-lv dz-ap-lvl-warn">WRN</span><span class="dz-ap-svc">paiements</span><span class="dz-ap-msg">Nouvelle tentative 3/3 vers la banque partenaire</span>
          <pre class="dz-ap-json">{ "commande": "FR-20931", "montant": 2947.00, "tentative": 3, "latence_ms": 29874, "region": "eu-west-3" }</pre></div>
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:16.530</span><span class="dz-ap-lv dz-ap-lvl-info">INF</span><span class="dz-ap-svc">api</span><span class="dz-ap-msg">POST /v2/commandes 201 · 184 ms · client=maison-ore</span></div>
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:15.002</span><span class="dz-ap-lv dz-ap-lvl-info">INF</span><span class="dz-ap-svc">auth</span><span class="dz-ap-msg">Connexion réussie · camille.laurent · double authentification</span></div>
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:14.771</span><span class="dz-ap-lv dz-ap-lvl-dbg">DBG</span><span class="dz-ap-svc">cache</span><span class="dz-ap-msg">Clé expirée : tarifs:equipe:v12 (ttl 3600 s)</span></div>
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:12.118</span><span class="dz-ap-lv dz-ap-lvl-err">ERR</span><span class="dz-ap-svc">webhooks</span><span class="dz-ap-msg">Réponse 503 de https://hooks.comptalib.fr/v1 · file d'attente</span></div>
        <div class="dz-ap-log"><span class="dz-ap-ts">10:42:10.640</span><span class="dz-ap-lv dz-ap-lvl-info">INF</span><span class="dz-ap-svc">factures</span><span class="dz-ap-msg">PDF généré F-2026-0413 en 612 ms</span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 15
    dict(
        name="état des intégrations",
        icon="fas fa-plug",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-int-head">
    <div><h2 class="dz-ap-title-lg">Intégrations</h2><p class="dz-ap-muted">6 connectées · 1 en erreur · dernière vérification il y a 40 s</p></div>
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Ajouter une intégration</a>
  </div>
  <div class="dz-ap-int-sum">
    <div class="dz-ap-int-stat dz-ap-ok"><i class="fas fa-check-circle"></i><b>5</b><span>Opérationnelles</span></div>
    <div class="dz-ap-int-stat dz-ap-sync"><i class="fas fa-sync-alt"></i><b>1</b><span>En synchronisation</span></div>
    <div class="dz-ap-int-stat dz-ap-err"><i class="fas fa-times-circle"></i><b>1</b><span>En erreur</span></div>
    <div class="dz-ap-int-stat"><i class="fas fa-exchange-alt"></i><b>48 210</b><span>Évènements / 24 h</span></div>
  </div>
  <div class="dz-ap-conns">
    <div class="dz-ap-conn dz-ap-conn-err">
      <span class="dz-ap-conn-ico dz-ap-h5"><i class="fas fa-book"></i></span>
      <div class="dz-ap-conn-main"><div class="dz-ap-conn-name"><b>Comptalib</b><span class="dz-badge dz-badge-danger">Erreur</span></div><span class="dz-ap-conn-desc">Jeton expiré le 23 sept. à 22:14 · 3 échecs consécutifs · 214 écritures en attente</span></div>
      <div class="dz-ap-health"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span class="dz-ap-bad"></span><span class="dz-ap-bad"></span><span class="dz-ap-bad"></span></div>
      <a class="dz-btn dz-btn-sm" href="#">Reconnecter</a>
    </div>
    <div class="dz-ap-conn">
      <span class="dz-ap-conn-ico dz-ap-h2"><i class="fas fa-credit-card"></i></span>
      <div class="dz-ap-conn-main"><div class="dz-ap-conn-name"><b>Payora</b><span class="dz-badge dz-badge-success">Connecté</span></div><span class="dz-ap-conn-desc">Paiements et remboursements · synchro il y a 2 min</span></div>
      <div class="dz-ap-health"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <span class="dz-ap-switch dz-ap-on"></span>
    </div>
    <div class="dz-ap-conn">
      <span class="dz-ap-conn-ico dz-ap-h3"><i class="fas fa-address-book"></i></span>
      <div class="dz-ap-conn-main"><div class="dz-ap-conn-name"><b>Contakt</b><span class="dz-badge">Synchronisation</span></div><span class="dz-ap-conn-desc">Import initial · 8 240 / 12 600 contacts</span><div class="dz-progress dz-ap-conn-prog"><span style="--v:65%"></span></div></div>
      <div class="dz-ap-health"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span class="dz-ap-mid"></span><span class="dz-ap-mid"></span></div>
      <span class="dz-ap-switch dz-ap-on"></span>
    </div>
    <div class="dz-ap-conn">
      <span class="dz-ap-conn-ico dz-ap-h1"><i class="fas fa-comment-dots"></i></span>
      <div class="dz-ap-conn-main"><div class="dz-ap-conn-name"><b>Parlo</b><span class="dz-badge dz-badge-success">Connecté</span></div><span class="dz-ap-conn-desc">3 canaux · 412 alertes envoyées cette semaine</span></div>
      <div class="dz-ap-health"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <span class="dz-ap-switch dz-ap-on"></span>
    </div>
    <div class="dz-ap-conn dz-ap-conn-off">
      <span class="dz-ap-conn-ico dz-ap-h4"><i class="fas fa-hdd"></i></span>
      <div class="dz-ap-conn-main"><div class="dz-ap-conn-name"><b>Nuage Drive</b><span class="dz-badge dz-badge-neutral">Désactivé</span></div><span class="dz-ap-conn-desc">Mis en pause par Marc D. le 12 sept.</span></div>
      <div class="dz-ap-health dz-ap-health-off"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <span class="dz-ap-switch"></span>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------------ 16
    dict(
        name="quotas et consommation",
        icon="fas fa-tachometer-alt",
        wrap="none",
        html="""
<div class="dz-ap-stage">
  <div class="dz-ap-usage">
    <div class="dz-ap-panel dz-ap-plan">
      <div class="dz-ap-plan-top"><span class="dz-ap-plan-ico"><i class="fas fa-gem"></i></span><div><span class="dz-ap-muted">Formule actuelle</span><h2 class="dz-ap-title">Équipe · annuel</h2></div></div>
      <div class="dz-ap-plan-price"><b>6 348 €</b><span>HT / an · renouvellement le 1er janv. 2027</span></div>
      <div class="dz-ap-plan-cycle"><div class="dz-ap-quota-row"><span>Période en cours</span><b>24 j restants</b></div><div class="dz-progress"><span style="--v:78%"></span></div><span class="dz-ap-muted">1 – 30 septembre 2026</span></div>
      <div class="dz-cluster"><a class="dz-btn dz-btn-sm" href="#">Passer à Entreprise</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Factures</a></div>
    </div>
    <div class="dz-ap-meters">
      <div class="dz-ap-callout"><i class="fas fa-exclamation-triangle"></i><div><b>Vous approchez de la limite de sièges</b><span>23 sièges sur 25 utilisés. Au-delà, les nouvelles invitations seront bloquées.</span></div><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Ajouter des sièges</a></div>
      <div class="dz-ap-meter-grid">
        <div class="dz-ap-panel dz-ap-meter"><div class="dz-ap-meter-head"><span><i class="fas fa-exchange-alt"></i> Appels d'API</span><span class="dz-ap-pct">84 %</span></div><b class="dz-ap-meter-val">842 190 <span>/ 1 M</span></b><div class="dz-ap-bar dz-ap-bar-warn"><span style="--v:84%"></span></div><span class="dz-ap-muted">Remise à zéro le 1er oct.</span></div>
        <div class="dz-ap-panel dz-ap-meter"><div class="dz-ap-meter-head"><span><i class="fas fa-database"></i> Stockage</span><span class="dz-ap-pct">68 %</span></div><b class="dz-ap-meter-val">68,4 Go <span>/ 100 Go</span></b><div class="dz-ap-bar"><span style="--v:68%"></span></div><span class="dz-ap-muted">+2,1 Go cette semaine</span></div>
        <div class="dz-ap-panel dz-ap-meter"><div class="dz-ap-meter-head"><span><i class="fas fa-users"></i> Sièges</span><span class="dz-ap-pct dz-ap-pct-crit">92 %</span></div><b class="dz-ap-meter-val">23 <span>/ 25</span></b><div class="dz-ap-bar dz-ap-bar-crit"><span style="--v:92%"></span></div><span class="dz-ap-muted">2 invitations en attente</span></div>
        <div class="dz-ap-panel dz-ap-meter"><div class="dz-ap-meter-head"><span><i class="fas fa-bolt"></i> Automatisations</span><span class="dz-ap-pct">31 %</span></div><b class="dz-ap-meter-val">3 104 <span>/ 10 000</span></b><div class="dz-ap-bar"><span style="--v:31%"></span></div><span class="dz-ap-muted">Exécutions ce mois-ci</span></div>
      </div>
      <div class="dz-ap-panel dz-ap-daily">
        <div class="dz-ap-meter-head"><span>Appels d'API par jour</span><span class="dz-ap-muted">Limite quotidienne conseillée : 40 000</span></div>
        <div class="dz-ap-daily-chart"><span class="dz-ap-limit"></span><span style="--h:42%"></span><span style="--h:48%"></span><span style="--h:36%"></span><span style="--h:30%"></span><span style="--h:52%"></span><span style="--h:58%"></span><span style="--h:61%"></span><span style="--h:55%"></span><span style="--h:66%"></span><span style="--h:72%"></span><span style="--h:40%"></span><span style="--h:34%"></span><span style="--h:70%"></span><span style="--h:78%"></span><span style="--h:84%" class="dz-ap-over"></span><span style="--h:88%" class="dz-ap-over"></span><span style="--h:74%"></span><span style="--h:69%"></span><span style="--h:46%"></span><span style="--h:38%"></span><span style="--h:76%"></span><span style="--h:81%" class="dz-ap-over"></span><span style="--h:72%"></span><span style="--h:65%"></span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
]
