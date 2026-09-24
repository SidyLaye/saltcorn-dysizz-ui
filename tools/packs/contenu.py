"""Famille « Contenu » : articles, documentation, base de connaissances,
journal des versions, feuille de route, encadrés, glossaire, FAQ, légal…
CSS : styles/38-contenu.css — préfixe dz-ct-"""

FAMILY = "contenu"

BLOCKS = [

# ------------------------------------------------------------------ 1
dict(name="article de blog", icon="fas fa-feather-alt", wrap="narrow", html="""
<article class="dz-ct-article">
  <header class="dz-ct-head">
    <nav class="dz-ct-crumbs"><a href="#">Journal</a><i class="fas fa-chevron-right"></i><a href="#">Produit</a></nav>
    <div class="dz-ct-kicker"><span class="dz-ct-cat">Guide pratique</span><span class="dz-ct-meta"><i class="far fa-clock"></i> 8 min de lecture</span></div>
    <h1 class="dz-ct-title">Écrire une documentation que vos clients <em>liront vraiment</em></h1>
    <p class="dz-ct-dek">Après avoir réécrit 340 pages d'aide en six mois, nous avons divisé par deux les demandes au support. Voici la méthode, pas à pas.</p>
    <div class="dz-ct-byline">
      <span class="dz-avatar">CM</span>
      <div class="dz-ct-byline-txt"><b>Camille Moreau</b><span>Responsable contenu · Publié le 12 mars 2026</span></div>
      <div class="dz-ct-share">
        <a class="dz-ct-iconbtn" href="#" aria-label="Copier le lien"><i class="fas fa-link"></i></a>
        <a class="dz-ct-iconbtn" href="#" aria-label="Partager par e-mail"><i class="far fa-envelope"></i></a>
        <a class="dz-ct-iconbtn" href="#" aria-label="Enregistrer"><i class="far fa-bookmark"></i></a>
      </div>
    </div>
  </header>
  <figure class="dz-ct-cover">
    <img src="https://picsum.photos/seed/ct-cover/1600/900" alt="Bureau avec carnet ouvert et tasse de café">
    <figcaption>L'équipe contenu réunie à l'atelier de Nantes, en février 2026.</figcaption>
  </figure>
  <div class="dz-ct-prose">
    <p class="dz-ct-dropcap">Une bonne page d'aide ne se lit pas : elle se <b>parcourt</b>. Vos lecteurs arrivent avec une question précise, souvent pressés, parfois agacés. Ils cherchent un titre, une capture, une commande à copier, puis repartent.</p>
    <p>Nous avons donc cessé d'écrire des manuels et commencé à écrire des <a href="#">réponses</a>. Trois principes ont tout changé.</p>
    <h2>1. Une page, une question</h2>
    <p>Chaque article répond à une seule question, formulée comme le client la poserait. « Configurer les webhooks » devient « Recevoir une alerte quand une facture est payée ».</p>
    <blockquote class="dz-ct-bq"><p>Si le titre ne peut pas être tapé tel quel dans la barre de recherche, c'est qu'il est mal écrit.</p><cite>Léa Garnier, rédactrice technique</cite></blockquote>
    <h2>2. Montrer avant d'expliquer</h2>
    <ul>
      <li><b>Une capture par étape</b>, recadrée sur l'essentiel.</li>
      <li>Les boutons écrits exactement comme à l'écran : <code>Enregistrer</code>, pas « valider ».</li>
      <li>Un exemple réel plutôt qu'une définition abstraite.</li>
    </ul>
    <div class="dz-ct-note"><i class="fas fa-lightbulb"></i><div><b>Astuce</b><p>Relisez chaque article sur mobile avant de le publier : 58 % de nos lecteurs y arrivent depuis un téléphone.</p></div></div>
    <h2>3. Mesurer, puis réécrire</h2>
    <p>Chaque page porte un petit sondage « Cet article vous a-t-il aidé ? ». Sous 70 % de réponses positives, la page repart en réécriture.</p>
    <figure class="dz-ct-fig">
      <img src="https://picsum.photos/seed/ct-chart/1400/700" alt="Tableau de suivi des pages d'aide">
      <figcaption><b>Figure 2.</b> Taux de satisfaction par page, avant et après réécriture.</figcaption>
    </figure>
    <p>Résultat : <mark>−48 % de demandes au support</mark> et un temps moyen de résolution passé de 11 à 4 minutes.</p>
  </div>
  <footer class="dz-ct-foot">
    <div class="dz-ct-tags"><a href="#">#documentation</a><a href="#">#support</a><a href="#">#rédaction</a></div>
    <div class="dz-ct-react"><a class="dz-ct-pill" href="#"><i class="far fa-heart"></i> 214</a><a class="dz-ct-pill" href="#"><i class="far fa-comment"></i> 36</a></div>
  </footer>
</article>
"""),

# ------------------------------------------------------------------ 2
dict(name="liste d'articles", icon="fas fa-newspaper", html="""
<div class="dz-ct-blog">
  <div class="dz-ct-blog-head">
    <div><span class="dz-eyebrow">Le journal</span><h2 class="dz-h2">Idées, méthodes et <em>coulisses</em></h2></div>
    <nav class="dz-ct-seg"><a class="dz-active" href="#">Tout</a><a href="#">Produit</a><a href="#">Méthode</a><a href="#">Équipe</a><a href="#">Clients</a></nav>
  </div>
  <a class="dz-ct-feature" href="#">
    <div class="dz-ct-feature-img"><img class="dz-cover" src="https://picsum.photos/seed/ct-feat/1400/900" alt="Atelier lumineux"></div>
    <div class="dz-ct-feature-body">
      <div class="dz-ct-kicker"><span class="dz-ct-cat">À la une</span><span class="dz-ct-meta">12 min</span></div>
      <h3 class="dz-ct-feature-title">Comment nous avons repensé l'accueil des nouveaux clients en trente jours</h3>
      <p class="dz-ct-feature-dek">Entretiens, prototypes jetables et un tableau de bord partagé : le récit complet d'un chantier mené à quatre.</p>
      <div class="dz-ct-mini-by"><span class="dz-avatar dz-avatar-sm">NB</span><span><b>Nadia Benali</b> · 18 sept. 2026</span></div>
    </div>
  </a>
  <div class="dz-ct-posts">
    <a class="dz-ct-post" href="#"><div class="dz-ct-post-img"><img class="dz-cover" src="https://picsum.photos/seed/ct-p1/800/500" alt="Carnet de notes"></div><span class="dz-ct-cat">Méthode</span><h4 class="dz-ct-post-title">Le guide de style en 12 règles que toute l'équipe applique</h4><span class="dz-ct-post-meta">Hugo Lefèvre · 5 min</span></a>
    <a class="dz-ct-post" href="#"><div class="dz-ct-post-img"><img class="dz-cover" src="https://picsum.photos/seed/ct-p2/800/500" alt="Écran de travail"></div><span class="dz-ct-cat">Produit</span><h4 class="dz-ct-post-title">Nouveautés de septembre : exports planifiés et vues partagées</h4><span class="dz-ct-post-meta">Camille Moreau · 3 min</span></a>
    <a class="dz-ct-post" href="#"><div class="dz-ct-post-img"><img class="dz-cover" src="https://picsum.photos/seed/ct-p3/800/500" alt="Réunion d'équipe"></div><span class="dz-ct-cat">Clients</span><h4 class="dz-ct-post-title">Atelier Lune a réduit ses relances de 60 % en un trimestre</h4><span class="dz-ct-post-meta">Inès Roux · 7 min</span></a>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 3
dict(name="page de documentation", icon="fas fa-book", html="""
<div class="dz-ct-docs">
  <aside class="dz-ct-docs-nav">
    <div class="dz-ct-docs-search"><i class="fas fa-search"></i><span>Rechercher</span><span class="dz-kbd">⌘K</span></div>
    <p class="dz-ct-docs-group">Premiers pas</p>
    <a class="dz-ct-docs-link" href="#">Introduction</a>
    <a class="dz-ct-docs-link" href="#">Installation</a>
    <a class="dz-ct-docs-link" href="#">Authentification</a>
    <p class="dz-ct-docs-group">Guides</p>
    <a class="dz-ct-docs-link" href="#">Importer des contacts</a>
    <a class="dz-ct-docs-link dz-active" href="#">Recevoir des webhooks</a>
    <a class="dz-ct-docs-link" href="#">Pagination</a>
    <a class="dz-ct-docs-link" href="#">Limites de débit</a>
    <p class="dz-ct-docs-group">Référence</p>
    <a class="dz-ct-docs-link" href="#"><span class="dz-ct-verb dz-ct-v-get">GET</span> /factures</a>
    <a class="dz-ct-docs-link" href="#"><span class="dz-ct-verb dz-ct-v-post">POST</span> /webhooks</a>
    <a class="dz-ct-docs-link" href="#"><span class="dz-ct-verb dz-ct-v-del">DEL</span> /webhooks/:id</a>
  </aside>
  <div class="dz-ct-docs-main">
    <nav class="dz-ct-crumbs"><a href="#">Docs</a><i class="fas fa-chevron-right"></i><a href="#">Guides</a><i class="fas fa-chevron-right"></i><span>Webhooks</span></nav>
    <h1 class="dz-ct-docs-title">Recevoir des webhooks</h1>
    <p class="dz-ct-docs-lead">Soyez prévenu en temps réel quand un événement se produit dans votre espace : facture payée, contact créé, tâche terminée.</p>
    <div class="dz-ct-docs-meta"><span><i class="far fa-clock"></i> 6 min</span><span><i class="fas fa-code-branch"></i> API v3</span><span><i class="far fa-calendar"></i> Mis à jour le 2 sept. 2026</span></div>
    <div class="dz-ct-prose dz-ct-prose-sm">
      <h2>Créer un point de réception</h2>
      <p>Déclarez l'URL qui recevra les événements. Elle doit répondre <code>200</code> en moins de 5 secondes.</p>
      <div class="dz-ct-code dz-copy-scope">
        <div class="dz-ct-code-bar"><span class="dz-ct-code-file"><i class="fas fa-terminal"></i> Terminal</span><button class="dz-ct-copy dz-copy"><i class="far fa-copy"></i> Copier</button></div>
        <pre class="dz-ct-pre"><code><span class="dz-ct-l"><span class="dz-ct-fn">curl</span> -X POST https://api.nexora.fr/v3/webhooks \\</span>
<span class="dz-ct-l">  -H <span class="dz-ct-str">"Authorization: Bearer $CLE_API"</span> \\</span>
<span class="dz-ct-l">  -d <span class="dz-ct-str">'{"url": "https://exemple.fr/hooks", "events": ["facture.payee"]}'</span></span></code></pre>
      </div>
      <div class="dz-ct-callout dz-ct-warn"><i class="fas fa-exclamation-triangle"></i><div><b>Vérifiez la signature</b><p>Chaque requête contient l'en-tête <code>X-Nexora-Signature</code>. Refusez toute requête dont la signature ne correspond pas.</p></div></div>
      <h2>Réessais automatiques</h2>
      <p>En cas d'échec, l'envoi est retenté 8 fois sur 24 heures, avec un délai croissant.</p>
    </div>
    <div class="dz-ct-helpful"><span>Cette page vous a-t-elle aidé ?</span><div class="dz-cluster"><a class="dz-ct-pill" href="#"><i class="far fa-thumbs-up"></i> Oui</a><a class="dz-ct-pill" href="#"><i class="far fa-thumbs-down"></i> Non</a></div></div>
    <div class="dz-ct-pager">
      <a class="dz-ct-pager-link" href="#"><span>Précédent</span><b><i class="fas fa-arrow-left"></i> Importer des contacts</b></a>
      <a class="dz-ct-pager-link dz-ct-next" href="#"><span>Suivant</span><b>Pagination <i class="fas fa-arrow-right"></i></b></a>
    </div>
  </div>
  <aside class="dz-ct-docs-toc">
    <p class="dz-ct-toc-label">Sur cette page</p>
    <a class="dz-ct-toc-link dz-active" href="#">Créer un point de réception</a>
    <a class="dz-ct-toc-link dz-ct-toc-sub" href="#">Format de la requête</a>
    <a class="dz-ct-toc-link dz-ct-toc-sub" href="#">Vérifier la signature</a>
    <a class="dz-ct-toc-link" href="#">Réessais automatiques</a>
    <a class="dz-ct-toc-link" href="#">Liste des événements</a>
    <div class="dz-ct-toc-foot"><a href="#"><i class="far fa-edit"></i> Modifier cette page</a><a href="#"><i class="far fa-comment-dots"></i> Signaler un problème</a></div>
  </aside>
</div>
"""),

# ------------------------------------------------------------------ 4
dict(name="base de connaissances", icon="fas fa-life-ring", html="""
<div class="dz-ct-kb">
  <div class="dz-ct-kb-hero">
    <span class="dz-eyebrow">Centre d'aide</span>
    <h2 class="dz-h2">Bonjour, comment pouvons-nous <em>vous aider</em> ?</h2>
    <label class="dz-ct-kb-search"><i class="fas fa-search"></i><input type="search" placeholder="Rechercher un article, ex. « exporter mes factures »"><span class="dz-kbd">/</span></label>
    <div class="dz-ct-kb-pop"><span>Populaire :</span><a href="#">Changer de mot de passe</a><a href="#">Ajouter un membre</a><a href="#">Facture en PDF</a><a href="#">Supprimer mon compte</a></div>
  </div>
  <div class="dz-ct-kb-grid">
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-rocket"></i></span><h3 class="dz-ct-kb-title">Bien démarrer</h3><p class="dz-ct-kb-desc">Créer son espace, inviter l'équipe, importer ses données.</p><span class="dz-ct-kb-count">24 articles</span></a>
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-file-invoice"></i></span><h3 class="dz-ct-kb-title">Facturation</h3><p class="dz-ct-kb-desc">Devis, factures, relances et moyens de paiement.</p><span class="dz-ct-kb-count">31 articles</span></a>
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-users"></i></span><h3 class="dz-ct-kb-title">Équipe et rôles</h3><p class="dz-ct-kb-desc">Permissions, invitations et espaces partagés.</p><span class="dz-ct-kb-count">17 articles</span></a>
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-plug"></i></span><h3 class="dz-ct-kb-title">Intégrations</h3><p class="dz-ct-kb-desc">Connecter votre agenda, votre banque et vos outils.</p><span class="dz-ct-kb-count">42 articles</span></a>
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-shield-alt"></i></span><h3 class="dz-ct-kb-title">Sécurité</h3><p class="dz-ct-kb-desc">Double authentification, sessions et journal d'audit.</p><span class="dz-ct-kb-count">12 articles</span></a>
    <a class="dz-ct-kb-cat" href="#"><span class="dz-ct-kb-ico"><i class="fas fa-code"></i></span><h3 class="dz-ct-kb-title">Développeurs</h3><p class="dz-ct-kb-desc">API, webhooks, clés et limites de débit.</p><span class="dz-ct-kb-count">38 articles</span></a>
  </div>
  <div class="dz-ct-kb-bottom">
    <div class="dz-ct-kb-list">
      <h3 class="dz-ct-kb-sub">Articles les plus consultés</h3>
      <a class="dz-ct-kb-row" href="#"><i class="far fa-file-alt"></i><span>Importer ses contacts depuis un tableur</span><span class="dz-ct-kb-views">3,2 k vues</span></a>
      <a class="dz-ct-kb-row" href="#"><i class="far fa-file-alt"></i><span>Personnaliser le modèle de facture</span><span class="dz-ct-kb-views">2,8 k vues</span></a>
      <a class="dz-ct-kb-row" href="#"><i class="far fa-file-alt"></i><span>Activer la double authentification</span><span class="dz-ct-kb-views">2,1 k vues</span></a>
      <a class="dz-ct-kb-row" href="#"><i class="far fa-file-alt"></i><span>Comprendre les rôles et permissions</span><span class="dz-ct-kb-views">1,9 k vues</span></a>
    </div>
    <div class="dz-ct-kb-contact">
      <div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">LG</span><span class="dz-avatar dz-avatar-sm">TM</span><span class="dz-avatar dz-avatar-sm">SA</span></div>
      <h3 class="dz-ct-kb-sub">Vous ne trouvez pas ?</h3>
      <p class="dz-ct-kb-desc">Notre équipe répond en moyenne en 2 h, du lundi au vendredi.</p>
      <a class="dz-btn dz-btn-sm" href="#"><i class="far fa-comment-dots"></i> Écrire au support</a>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 5
dict(name="journal des versions", icon="fas fa-history", wrap="narrow", html="""
<div class="dz-ct-log">
  <div class="dz-ct-log-head">
    <div><span class="dz-eyebrow">Nouveautés</span><h2 class="dz-h2">Journal des versions</h2><p class="dz-lead">Tout ce qui change dans l'application, chaque semaine.</p></div>
    <a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-rss"></i> S'abonner</a>
  </div>
  <div class="dz-ct-rel">
    <div class="dz-ct-rel-side"><span class="dz-ct-ver">v4.12</span><span class="dz-ct-rel-date">18 sept. 2026</span></div>
    <div class="dz-ct-rel-body">
      <h3 class="dz-ct-rel-title">Exports planifiés et vues partagées</h3>
      <img class="dz-ct-rel-img" src="https://picsum.photos/seed/ct-rel/1200/560" alt="Aperçu des exports planifiés">
      <ul class="dz-ct-changes">
        <li><span class="dz-ct-tag dz-ct-new">Nouveau</span><span>Planifiez un export CSV chaque lundi à 8 h, envoyé à qui vous voulez.</span></li>
        <li><span class="dz-ct-tag dz-ct-new">Nouveau</span><span>Partagez une vue filtrée avec un lien en lecture seule.</span></li>
        <li><span class="dz-ct-tag dz-ct-imp">Amélioré</span><span>La recherche retrouve désormais les pièces jointes PDF.</span></li>
        <li><span class="dz-ct-tag dz-ct-fix">Corrigé</span><span>Les montants négatifs s'affichaient sans signe dans les exports.</span></li>
      </ul>
    </div>
  </div>
  <div class="dz-ct-rel">
    <div class="dz-ct-rel-side"><span class="dz-ct-ver">v4.11</span><span class="dz-ct-rel-date">4 sept. 2026</span></div>
    <div class="dz-ct-rel-body">
      <h3 class="dz-ct-rel-title">Relances automatiques plus fines</h3>
      <ul class="dz-ct-changes">
        <li><span class="dz-ct-tag dz-ct-imp">Amélioré</span><span>Choisissez le ton de chaque relance : cordial, ferme ou dernier rappel.</span></li>
        <li><span class="dz-ct-tag dz-ct-imp">Amélioré</span><span>Tableau de bord 40 % plus rapide sur les grands espaces.</span></li>
        <li><span class="dz-ct-tag dz-ct-fix">Corrigé</span><span>Le fuseau horaire n'était pas pris en compte dans les rappels.</span></li>
      </ul>
    </div>
  </div>
  <div class="dz-ct-rel">
    <div class="dz-ct-rel-side"><span class="dz-ct-ver">v4.10</span><span class="dz-ct-rel-date">21 août 2026</span></div>
    <div class="dz-ct-rel-body">
      <h3 class="dz-ct-rel-title">Mode hors ligne sur mobile</h3>
      <ul class="dz-ct-changes">
        <li><span class="dz-ct-tag dz-ct-new">Nouveau</span><span>Consultez et modifiez vos fiches sans réseau, synchronisées au retour.</span></li>
        <li><span class="dz-ct-tag dz-ct-fix">Corrigé</span><span>Double notification à l'ouverture de l'application.</span></li>
      </ul>
    </div>
  </div>
  <a class="dz-ct-more" href="#">Voir les versions précédentes <i class="fas fa-arrow-down"></i></a>
</div>
"""),

# ------------------------------------------------------------------ 6
dict(name="feuille de route", icon="fas fa-road", html="""
<div class="dz-ct-road">
  <div class="dz-ct-road-head">
    <div><span class="dz-eyebrow">Feuille de route publique</span><h2 class="dz-h2">Ce que nous <em>construisons</em></h2></div>
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Proposer une idée</a>
  </div>
  <div class="dz-ct-road-cols">
    <div class="dz-ct-road-col">
      <div class="dz-ct-road-colhead"><span class="dz-ct-road-dot dz-ct-road-plan"></span><b>Prévu</b><span class="dz-ct-road-n">3</span></div>
      <div class="dz-ct-idea"><a class="dz-ct-vote" href="#"><i class="fas fa-chevron-up"></i><b>312</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Signature électronique des devis</h4><p class="dz-ct-idea-desc">Faire signer un devis sans quitter l'application.</p><div class="dz-ct-idea-meta"><span class="dz-ct-label">Facturation</span><span><i class="far fa-comment"></i> 48</span></div></div></div>
      <div class="dz-ct-idea"><a class="dz-ct-vote" href="#"><i class="fas fa-chevron-up"></i><b>187</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Thème à fort contraste</h4><p class="dz-ct-idea-desc">Pour une meilleure lisibilité en plein soleil.</p><div class="dz-ct-idea-meta"><span class="dz-ct-label">Accessibilité</span><span><i class="far fa-comment"></i> 21</span></div></div></div>
      <div class="dz-ct-idea"><a class="dz-ct-vote" href="#"><i class="fas fa-chevron-up"></i><b>96</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Import depuis un agenda partagé</h4><div class="dz-ct-idea-meta"><span class="dz-ct-label">Intégrations</span><span><i class="far fa-comment"></i> 9</span></div></div></div>
    </div>
    <div class="dz-ct-road-col">
      <div class="dz-ct-road-colhead"><span class="dz-ct-road-dot dz-ct-road-prog"></span><b>En cours</b><span class="dz-ct-road-n">2</span></div>
      <div class="dz-ct-idea"><a class="dz-ct-vote dz-ct-voted" href="#"><i class="fas fa-chevron-up"></i><b>428</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Application de bureau</h4><p class="dz-ct-idea-desc">Notifications natives et raccourcis clavier globaux.</p><div class="dz-progress"><span style="--v:65%"></span></div><div class="dz-ct-idea-meta"><span class="dz-ct-label">Plateforme</span><span>Bêta en octobre</span></div></div></div>
      <div class="dz-ct-idea"><a class="dz-ct-vote" href="#"><i class="fas fa-chevron-up"></i><b>254</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Automatisations conditionnelles</h4><p class="dz-ct-idea-desc">« Si… alors… sinon » dans vos scénarios.</p><div class="dz-progress"><span style="--v:30%"></span></div><div class="dz-ct-idea-meta"><span class="dz-ct-label">Automatisation</span><span>T4 2026</span></div></div></div>
    </div>
    <div class="dz-ct-road-col">
      <div class="dz-ct-road-colhead"><span class="dz-ct-road-dot dz-ct-road-done"></span><b>Livré</b><span class="dz-ct-road-n">3</span></div>
      <div class="dz-ct-idea dz-ct-idea-done"><a class="dz-ct-vote" href="#"><i class="fas fa-check"></i><b>391</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Exports planifiés</h4><div class="dz-ct-idea-meta"><span class="dz-ct-label">Données</span><span>v4.12 · sept.</span></div></div></div>
      <div class="dz-ct-idea dz-ct-idea-done"><a class="dz-ct-vote" href="#"><i class="fas fa-check"></i><b>276</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Mode hors ligne mobile</h4><div class="dz-ct-idea-meta"><span class="dz-ct-label">Mobile</span><span>v4.10 · août</span></div></div></div>
      <div class="dz-ct-idea dz-ct-idea-done"><a class="dz-ct-vote" href="#"><i class="fas fa-check"></i><b>148</b></a><div class="dz-ct-idea-body"><h4 class="dz-ct-idea-title">Double authentification par clé</h4><div class="dz-ct-idea-meta"><span class="dz-ct-label">Sécurité</span><span>v4.8 · juil.</span></div></div></div>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 7
dict(name="code à onglets", icon="fas fa-code", wrap="narrow", html="""
<div class="dz-ct-codetabs">
  <div class="dz-ct-codetabs-head"><h3 class="dz-ct-codetabs-title">Créer une facture</h3><span class="dz-ct-verb dz-ct-v-post">POST</span><span class="dz-ct-endpoint">/v3/factures</span></div>
  <div class="dz-ct-code dz-tabs">
    <div class="dz-ct-code-bar">
      <div class="dz-tabs-nav dz-ct-langs"><button data-tab="js" aria-selected="true">JavaScript</button><button data-tab="py">Python</button><button data-tab="sh">cURL</button></div>
      <span class="dz-ct-code-hint">Réponse : 201</span>
    </div>
    <div class="dz-tab-panel dz-copy-scope" data-tab="js"><button class="dz-ct-copy dz-ct-copy-float" data-dz-copy aria-label="Copier le code"><i class="far fa-copy"></i></button><pre class="dz-ct-pre dz-ct-numbered"><code><span class="dz-ct-l"><span class="dz-ct-kw">import</span> { Nexora } <span class="dz-ct-kw">from</span> <span class="dz-ct-str">"@nexora/sdk"</span>;</span><span class="dz-ct-l"> </span><span class="dz-ct-l"><span class="dz-ct-kw">const</span> client = <span class="dz-ct-kw">new</span> <span class="dz-ct-fn">Nexora</span>(process.env.CLE_API);</span><span class="dz-ct-l"> </span><span class="dz-ct-l"><span class="dz-ct-kw">const</span> facture = <span class="dz-ct-kw">await</span> client.factures.<span class="dz-ct-fn">creer</span>({</span><span class="dz-ct-l">  client: <span class="dz-ct-str">"cli_8Hq2"</span>,</span><span class="dz-ct-l">  lignes: [{ libelle: <span class="dz-ct-str">"Atelier UX"</span>, montant: <span class="dz-ct-num">1250</span> }],</span><span class="dz-ct-l">  echeance: <span class="dz-ct-str">"2026-10-31"</span>, <span class="dz-ct-com">// 30 jours fin de mois</span></span><span class="dz-ct-l">});</span></code></pre></div>
    <div class="dz-tab-panel dz-copy-scope" data-tab="py" hidden><button class="dz-ct-copy dz-ct-copy-float" data-dz-copy aria-label="Copier le code"><i class="far fa-copy"></i></button><pre class="dz-ct-pre dz-ct-numbered"><code><span class="dz-ct-l"><span class="dz-ct-kw">from</span> nexora <span class="dz-ct-kw">import</span> Nexora</span><span class="dz-ct-l"> </span><span class="dz-ct-l">client = <span class="dz-ct-fn">Nexora</span>(os.environ[<span class="dz-ct-str">"CLE_API"</span>])</span><span class="dz-ct-l">facture = client.factures.<span class="dz-ct-fn">creer</span>(</span><span class="dz-ct-l">    client=<span class="dz-ct-str">"cli_8Hq2"</span>,</span><span class="dz-ct-l">    lignes=[{<span class="dz-ct-str">"libelle"</span>: <span class="dz-ct-str">"Atelier UX"</span>, <span class="dz-ct-str">"montant"</span>: <span class="dz-ct-num">1250</span>}],</span><span class="dz-ct-l">    echeance=<span class="dz-ct-str">"2026-10-31"</span>,  <span class="dz-ct-com"># 30 jours fin de mois</span></span><span class="dz-ct-l">)</span></code></pre></div>
    <div class="dz-tab-panel dz-copy-scope" data-tab="sh" hidden><button class="dz-ct-copy dz-ct-copy-float" data-dz-copy aria-label="Copier le code"><i class="far fa-copy"></i></button><pre class="dz-ct-pre dz-ct-numbered"><code><span class="dz-ct-l"><span class="dz-ct-fn">curl</span> https://api.nexora.fr/v3/factures \\</span><span class="dz-ct-l">  -H <span class="dz-ct-str">"Authorization: Bearer $CLE_API"</span> \\</span><span class="dz-ct-l">  -d client=cli_8Hq2 \\</span><span class="dz-ct-l">  -d <span class="dz-ct-str">"lignes[0][libelle]=Atelier UX"</span> \\</span><span class="dz-ct-l">  -d <span class="dz-ct-str">"lignes[0][montant]=1250"</span></span></code></pre></div>
  </div>
  <p class="dz-ct-codetabs-foot"><i class="fas fa-info-circle"></i> Les montants sont exprimés en euros, hors taxes.</p>
</div>
"""),

# ------------------------------------------------------------------ 8
dict(name="encadrés", icon="fas fa-info-circle", wrap="narrow", html="""
<div class="dz-ct-callouts">
  <div class="dz-ct-callout dz-ct-info"><i class="fas fa-info-circle"></i><div><b>Note</b><p>Les modifications sont enregistrées automatiquement toutes les 30 secondes.</p></div></div>
  <div class="dz-ct-callout dz-ct-tip"><i class="fas fa-lightbulb"></i><div><b>Astuce</b><p>Appuyez sur <span class="dz-kbd">⌘</span> <span class="dz-kbd">K</span> pour ouvrir la recherche depuis n'importe quel écran.</p></div></div>
  <div class="dz-ct-callout dz-ct-warn"><i class="fas fa-exclamation-triangle"></i><div><b>Attention</b><p>Changer la devise d'un espace recalcule tous les devis en cours. Prévenez vos collègues avant.</p></div></div>
  <div class="dz-ct-callout dz-ct-danger"><i class="fas fa-skull-crossbones"></i><div><b>Danger</b><p>La suppression d'un espace est définitive après 30 jours. Aucune restauration n'est possible ensuite.</p><a class="dz-ct-callout-link" href="#">Exporter mes données d'abord <i class="fas fa-arrow-right"></i></a></div></div>
</div>
"""),

# ------------------------------------------------------------------ 9
dict(name="glossaire", icon="fas fa-spell-check", wrap="narrow", html="""
<div class="dz-ct-gloss">
  <div class="dz-ct-gloss-head"><span class="dz-eyebrow">Lexique</span><h2 class="dz-h2">Glossaire</h2><p class="dz-lead">Les mots de la facturation et de la gestion, expliqués simplement.</p></div>
  <nav class="dz-ct-az"><a href="#">A</a><a href="#">B</a><a href="#">C</a><a href="#">D</a><a href="#">E</a><span>F</span><span>G</span><a href="#">H</a><span>I</span><span>J</span><a href="#">K</a><span>L</span><a href="#">M</a><span>N</span><span>O</span><a href="#">P</a><span>Q</span><a href="#">R</a><a href="#">S</a><a href="#">T</a><span>U</span><span>V</span><span>W</span><span>X</span><span>Y</span><span>Z</span></nav>
  <div class="dz-ct-gl-group">
    <span class="dz-ct-gl-letter">A</span>
    <dl class="dz-ct-gl-list">
      <div class="dz-ct-gl-item"><dt>Acompte</dt><dd>Somme versée à la commande, déduite ensuite de la facture finale. À ne pas confondre avec les arrhes.</dd></div>
      <div class="dz-ct-gl-item"><dt>Avoir</dt><dd>Document qui annule tout ou partie d'une facture déjà émise. <a href="#">Créer un avoir</a></dd></div>
    </dl>
  </div>
  <div class="dz-ct-gl-group">
    <span class="dz-ct-gl-letter">E</span>
    <dl class="dz-ct-gl-list">
      <div class="dz-ct-gl-item"><dt>Échéance</dt><dd>Date limite de paiement. Par défaut, 30 jours après l'émission de la facture.</dd></div>
      <div class="dz-ct-gl-item"><dt>Escompte <span class="dz-ct-gl-alias">syn. remise pour paiement anticipé</span></dt><dd>Réduction accordée à un client qui paie avant la date d'échéance.</dd></div>
    </dl>
  </div>
  <div class="dz-ct-gl-group">
    <span class="dz-ct-gl-letter">T</span>
    <dl class="dz-ct-gl-list">
      <div class="dz-ct-gl-item"><dt>TVA intracommunautaire</dt><dd>Numéro qui identifie une entreprise assujettie à la TVA dans l'Union européenne. Il figure sur chaque facture B2B.</dd></div>
    </dl>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 10
dict(name="faq par catégories", icon="fas fa-question-circle", html="""
<div class="dz-ct-faq">
  <aside class="dz-ct-faq-side">
    <span class="dz-eyebrow">FAQ</span>
    <h2 class="dz-ct-faq-title">Questions fréquentes</h2>
    <nav class="dz-ct-faq-nav">
      <a class="dz-active" href="#"><i class="fas fa-rocket"></i> Démarrage <span>6</span></a>
      <a href="#"><i class="fas fa-credit-card"></i> Paiement <span>8</span></a>
      <a href="#"><i class="fas fa-users"></i> Équipe <span>5</span></a>
      <a href="#"><i class="fas fa-shield-alt"></i> Sécurité <span>7</span></a>
      <a href="#"><i class="fas fa-database"></i> Données <span>4</span></a>
    </nav>
    <div class="dz-ct-faq-help"><b>Encore une question ?</b><span>Réponse sous 2 h en semaine.</span><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Nous écrire</a></div>
  </aside>
  <div class="dz-ct-faq-main">
    <div class="dz-ct-faq-cat"><span class="dz-ct-kb-ico"><i class="fas fa-rocket"></i></span><div><h3 class="dz-ct-faq-h">Démarrage</h3><p class="dz-small">Les premières questions de nos nouveaux clients.</p></div></div>
    <div class="dz-ct-acc">
      <details><summary>Combien de temps faut-il pour tout configurer ?</summary><div><p>Comptez une vingtaine de minutes : création de l'espace, import de vos contacts, personnalisation du modèle de facture. L'assistant d'accueil vous guide étape par étape.</p></div></details>
      <details><summary>Puis-je importer mes données depuis un autre logiciel ?</summary><div><p>Oui, depuis n'importe quel fichier CSV ou tableur. Nos modèles d'import reconnaissent automatiquement les colonnes les plus courantes.</p></div></details>
      <details><summary>L'essai gratuit nécessite-t-il une carte bancaire ?</summary><div><p>Non. Vous profitez de 14 jours sans engagement. Nous vous prévenons 3 jours avant la fin de l'essai.</p></div></details>
      <details><summary>Y a-t-il une application mobile ?</summary><div><p>Oui, pour téléphone et tablette, avec un mode hors ligne complet.</p></div></details>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 11
dict(name="fiche auteur", icon="fas fa-user-edit", wrap="narrow", html="""
<div class="dz-ct-author">
  <div class="dz-ct-author-top">
    <span class="dz-avatar dz-ct-author-av">LG</span>
    <div class="dz-ct-author-id">
      <span class="dz-ct-author-kick">Écrit par</span>
      <h3 class="dz-ct-author-name">Léa Garnier</h3>
      <span class="dz-ct-author-role">Rédactrice technique · Lyon</span>
    </div>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-plus"></i> Suivre</a>
  </div>
  <p class="dz-ct-author-bio">Ancienne développeuse, Léa transforme depuis huit ans les sujets techniques en guides limpides. Elle anime chaque mois l'atelier « Écrire pour être compris ».</p>
  <div class="dz-ct-author-stats"><div><b>64</b><span>articles</span></div><div><b>12,4 k</b><span>lecteurs</span></div><div><b>4,9</b><span>note moyenne</span></div></div>
  <div class="dz-ct-author-latest">
    <span class="dz-ct-toc-label">Ses derniers articles</span>
    <a class="dz-ct-author-post" href="#"><span>Rédiger des messages d'erreur utiles</span><span class="dz-ct-meta">6 min</span></a>
    <a class="dz-ct-author-post" href="#"><span>Les captures d'écran qui aident vraiment</span><span class="dz-ct-meta">4 min</span></a>
    <a class="dz-ct-author-post" href="#"><span>Un glossaire partagé pour toute l'équipe</span><span class="dz-ct-meta">7 min</span></a>
  </div>
  <div class="dz-ct-author-social"><a class="dz-ct-iconbtn" href="#" aria-label="Site personnel"><i class="fas fa-globe"></i></a><a class="dz-ct-iconbtn" href="#" aria-label="E-mail"><i class="far fa-envelope"></i></a><a class="dz-ct-iconbtn" href="#" aria-label="Flux RSS"><i class="fas fa-rss"></i></a></div>
</div>
"""),

# ------------------------------------------------------------------ 12
dict(name="lettre éditoriale", icon="fas fa-envelope-open-text", wrap="narrow", html="""
<div class="dz-ct-letter">
  <div class="dz-ct-letter-mast">
    <span class="dz-ct-letter-no">N° 42</span>
    <span class="dz-ct-letter-name">La Lettre du jeudi</span>
    <span class="dz-ct-letter-date">24 sept. 2026</span>
  </div>
  <div class="dz-ct-letter-body">
    <h2 class="dz-ct-letter-title">Ralentir pour <em>mieux livrer</em></h2>
    <p>Chers lecteurs,</p>
    <p>Cette semaine, nous avons repoussé une sortie. Deux jours seulement, mais deux jours qui nous ont évité un mois de correctifs. Je voulais vous raconter pourquoi — et ce que cela change pour vous.</p>
    <p>Au sommaire : les coulisses de cette décision, trois nouveautés discrètes et l'entretien d'une cliente qui gère 400 factures par mois.</p>
    <div class="dz-ct-letter-sign"><span class="dz-avatar dz-avatar-sm">AB</span><div><b>Antoine Bernard</b><span>Cofondateur</span></div></div>
  </div>
  <ol class="dz-ct-letter-toc">
    <li><a href="#"><b>Pourquoi nous avons repoussé la v4.13</b><span>Coulisses · 4 min</span></a></li>
    <li><a href="#"><b>Trois nouveautés que vous avez peut-être manquées</b><span>Produit · 2 min</span></a></li>
    <li><a href="#"><b>« 400 factures par mois sans stress »</b><span>Entretien · 6 min</span></a></li>
  </ol>
  <div class="dz-ct-letter-sub">
    <div><b>Recevez la lettre chaque jeudi</b><span>8 400 abonnés · Désinscription en un clic</span></div>
    <div class="dz-ct-letter-form"><input type="email" placeholder="vous@exemple.fr" aria-label="Adresse e-mail"><a class="dz-btn dz-btn-sm" href="#">S'abonner</a></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 13
dict(name="table des matières", icon="fas fa-list-ol", wrap="narrow", html="""
<div class="dz-ct-toc">
  <div class="dz-ct-toc-top">
    <div><span class="dz-eyebrow">Guide complet</span><h2 class="dz-ct-toc-title">Réussir sa facturation en 2026</h2></div>
    <div class="dz-ct-toc-progress"><span class="dz-ring dz-ct-ring" style="--v:40">40 %</span><div><b>2 chapitres sur 5</b><span>≈ 22 min restantes</span></div></div>
  </div>
  <ol class="dz-ct-toc-list">
    <li class="dz-ct-toc-item dz-ct-read"><a href="#"><span class="dz-ct-toc-n">01</span><span class="dz-ct-toc-txt"><b>Les mentions obligatoires</b><span>Numérotation, TVA, pénalités de retard</span></span><span class="dz-ct-toc-time"><i class="fas fa-check"></i> Lu</span></a></li>
    <li class="dz-ct-toc-item dz-ct-read"><a href="#"><span class="dz-ct-toc-n">02</span><span class="dz-ct-toc-txt"><b>Devis, acompte et facture finale</b><span>Le bon enchaînement, sans oubli</span></span><span class="dz-ct-toc-time"><i class="fas fa-check"></i> Lu</span></a></li>
    <li class="dz-ct-toc-item dz-ct-current"><a href="#"><span class="dz-ct-toc-n">03</span><span class="dz-ct-toc-txt"><b>La facture électronique obligatoire</b><span>Calendrier, formats et plateformes agréées</span></span><span class="dz-ct-toc-time">9 min</span></a></li>
    <li class="dz-ct-toc-item"><a href="#"><span class="dz-ct-toc-n">04</span><span class="dz-ct-toc-txt"><b>Relancer sans froisser</b><span>Modèles de messages et bon tempo</span></span><span class="dz-ct-toc-time">7 min</span></a></li>
    <li class="dz-ct-toc-item"><a href="#"><span class="dz-ct-toc-n">05</span><span class="dz-ct-toc-txt"><b>Suivre sa trésorerie</b><span>Les 4 indicateurs à regarder chaque lundi</span></span><span class="dz-ct-toc-time">6 min</span></a></li>
  </ol>
</div>
"""),

# ------------------------------------------------------------------ 14
dict(name="citation mise en valeur", icon="fas fa-quote-right", html="""
<div class="dz-ct-quotes">
  <figure class="dz-ct-pull">
    <span class="dz-ct-pull-mark">“</span>
    <blockquote class="dz-ct-pull-text">On ne lit plus nos pages d'aide : on les <em>utilise</em>. C'est exactement ce que nous voulions.</blockquote>
    <figcaption class="dz-ct-pull-by"><span class="dz-avatar">SA</span><div><b>Sofia Amrani</b><span>Directrice du service client, Atelier Lune</span></div></figcaption>
  </figure>
  <div class="dz-ct-quote-side">
    <blockquote class="dz-ct-aside-q"><p>« La clarté est la politesse de celui qui écrit. »</p><cite>Proverbe de rédaction</cite></blockquote>
    <div class="dz-ct-stat-q"><b>−48 %</b><p>de demandes au support après la réécriture du centre d'aide.</p><span>Étude interne · 2026</span></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 15
dict(name="à faire, à éviter", icon="fas fa-check-double", html="""
<div class="dz-ct-dodont">
  <div class="dz-ct-dd-head"><span class="dz-eyebrow">Guide de style</span><h2 class="dz-h2">Écrire un message d'erreur</h2></div>
  <div class="dz-ct-dd-grid">
    <div class="dz-ct-dd dz-ct-do">
      <div class="dz-ct-dd-example"><div class="dz-ct-dd-toast"><i class="fas fa-exclamation-circle"></i><div><b>Le paiement n'a pas abouti</b><span>Votre carte a expiré en août. Mettez-la à jour pour réessayer.</span></div></div></div>
      <div class="dz-ct-dd-label"><i class="fas fa-check-circle"></i> À faire</div>
      <ul class="dz-ct-dd-list"><li>Dire ce qui s'est passé, en mots simples</li><li>Donner la cause si on la connaît</li><li>Proposer une action concrète</li></ul>
    </div>
    <div class="dz-ct-dd dz-ct-dont">
      <div class="dz-ct-dd-example"><div class="dz-ct-dd-toast"><i class="fas fa-exclamation-circle"></i><div><b>Erreur 402 : PAYMENT_FAILED</b><span>Une erreur inattendue est survenue.</span></div></div></div>
      <div class="dz-ct-dd-label"><i class="fas fa-times-circle"></i> À éviter</div>
      <ul class="dz-ct-dd-list"><li>Afficher un code technique seul</li><li>Rester vague : « inattendue »</li><li>Laisser la personne sans issue</li></ul>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 16
dict(name="étapes de tutoriel", icon="fas fa-shoe-prints", wrap="narrow", html="""
<div class="dz-ct-tuto">
  <div class="dz-ct-tuto-head">
    <span class="dz-eyebrow">Tutoriel</span>
    <h2 class="dz-h2">Connecter votre banque</h2>
    <div class="dz-ct-tuto-meta"><span class="dz-ct-label"><i class="far fa-clock"></i> 10 min</span><span class="dz-ct-label"><i class="fas fa-signal"></i> Débutant</span><span class="dz-ct-label"><i class="fas fa-user-lock"></i> Rôle administrateur</span></div>
  </div>
  <ol class="dz-ct-steps">
    <li class="dz-ct-step dz-ct-done"><div class="dz-ct-step-body"><h3 class="dz-ct-step-title">Ouvrir les réglages de trésorerie</h3><p>Dans le menu de gauche, choisissez <b>Réglages</b> puis <b>Trésorerie</b>.</p></div></li>
    <li class="dz-ct-step dz-ct-done"><div class="dz-ct-step-body"><h3 class="dz-ct-step-title">Choisir votre établissement</h3><p>Tapez le nom de votre banque. Plus de 300 établissements européens sont disponibles.</p></div></li>
    <li class="dz-ct-step dz-ct-now"><div class="dz-ct-step-body"><h3 class="dz-ct-step-title">Autoriser l'accès en lecture</h3><p>Vous êtes redirigé vers votre banque. Validez avec votre code habituel : nous n'avons jamais accès à vos identifiants.</p><div class="dz-ct-callout dz-ct-info"><i class="fas fa-shield-alt"></i><div><p>L'autorisation est valable 180 jours. Nous vous prévenons 7 jours avant son expiration.</p></div></div></div></li>
    <li class="dz-ct-step"><div class="dz-ct-step-body"><h3 class="dz-ct-step-title">Rapprocher les premières opérations</h3><p>Les 90 derniers jours sont importés. Validez les correspondances proposées en un clic.</p></div></li>
  </ol>
  <div class="dz-ct-tuto-end"><i class="fas fa-flag-checkered"></i><div><b>Et ensuite ?</b><span>Programmez des relances automatiques pour les factures en retard.</span></div><a class="dz-btn dz-btn-sm" href="#">Tutoriel suivant <i class="fas fa-arrow-right"></i></a></div>
</div>
"""),

# ------------------------------------------------------------------ 17
dict(name="page légale", icon="fas fa-balance-scale", html="""
<div class="dz-ct-legal">
  <aside class="dz-ct-legal-side">
    <p class="dz-ct-toc-label">Sommaire</p>
    <a class="dz-ct-toc-link dz-active" href="#">1. Objet</a>
    <a class="dz-ct-toc-link" href="#">2. Accès au service</a>
    <a class="dz-ct-toc-link" href="#">3. Tarifs et paiement</a>
    <a class="dz-ct-toc-link" href="#">4. Données personnelles</a>
    <a class="dz-ct-toc-link" href="#">5. Responsabilité</a>
    <a class="dz-ct-toc-link" href="#">6. Résiliation</a>
    <a class="dz-ct-toc-link" href="#">7. Droit applicable</a>
    <div class="dz-ct-toc-foot"><a href="#"><i class="fas fa-file-pdf"></i> Télécharger en PDF</a><a href="#"><i class="fas fa-history"></i> Versions précédentes</a></div>
  </aside>
  <div class="dz-ct-legal-main">
    <span class="dz-ct-legal-upd"><i class="far fa-calendar-check"></i> En vigueur depuis le 1er septembre 2026</span>
    <h1 class="dz-ct-docs-title">Conditions générales d'utilisation</h1>
    <div class="dz-ct-tldr">
      <b class="dz-ct-tldr-title"><i class="fas fa-bolt"></i> En bref</b>
      <ul>
        <li>Vous restez propriétaire de toutes vos données.</li>
        <li>Vous pouvez résilier à tout moment, sans frais.</li>
        <li>Vos données sont hébergées en France.</li>
      </ul>
      <span class="dz-ct-tldr-note">Ce résumé ne remplace pas le texte complet ci-dessous.</span>
    </div>
    <div class="dz-ct-legal-art">
      <h2 class="dz-ct-legal-h"><span>1.</span> Objet</h2>
      <p>Les présentes conditions encadrent l'utilisation du service Nexora, édité par Nexora SAS, 14 rue des Tanneurs, 44000 Nantes, immatriculée au RCS de Nantes sous le numéro 912 345 678.</p>
      <h2 class="dz-ct-legal-h"><span>2.</span> Accès au service</h2>
      <p>Le service est accessible 24 h/24, sauf interruption pour maintenance. Nous nous engageons sur une disponibilité de <b>99,9 %</b> par mois civil.</p>
      <p class="dz-ct-legal-sub"><b>2.1</b> Toute maintenance planifiée est annoncée au moins 72 heures à l'avance.</p>
      <h2 class="dz-ct-legal-h"><span>3.</span> Tarifs et paiement</h2>
      <p>Les tarifs sont indiqués en euros hors taxes. L'abonnement est payable d'avance, mensuellement ou annuellement.</p>
    </div>
    <div class="dz-ct-legal-contact"><i class="far fa-envelope"></i><span>Une question sur ce document ? <a href="#">juridique@nexora.fr</a></span></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 18
dict(name="fiche recette", icon="fas fa-utensils", html="""
<div class="dz-ct-recipe">
  <div class="dz-ct-recipe-media">
    <img class="dz-cover" src="https://picsum.photos/seed/ct-tarte/1000/1100" alt="Tarte fine aux poireaux sur une planche">
    <span class="dz-ct-recipe-badge"><i class="fas fa-leaf"></i> Végétarien</span>
  </div>
  <div class="dz-ct-recipe-body">
    <span class="dz-eyebrow">Fiche pratique · Saison d'automne</span>
    <h2 class="dz-ct-recipe-title">Tarte fine aux poireaux et comté</h2>
    <div class="dz-ct-recipe-rate"><span class="dz-ct-stars">★★★★★</span><span>4,8 · 326 avis</span></div>
    <div class="dz-ct-recipe-facts">
      <div><i class="far fa-clock"></i><b>20 min</b><span>Préparation</span></div>
      <div><i class="fas fa-fire-alt"></i><b>35 min</b><span>Cuisson</span></div>
      <div><i class="fas fa-user-friends"></i><b>4 pers.</b><span>Portions</span></div>
      <div><i class="fas fa-signal"></i><b>Facile</b><span>Difficulté</span></div>
    </div>
    <div class="dz-ct-recipe-cols">
      <div>
        <h3 class="dz-ct-recipe-h">Ingrédients</h3>
        <ul class="dz-ct-ingr">
          <li class="dz-ct-got"><span>Pâte feuilletée</span><b>1 rouleau</b></li>
          <li class="dz-ct-got"><span>Poireaux</span><b>3</b></li>
          <li><span>Comté affiné</span><b>120 g</b></li>
          <li><span>Crème épaisse</span><b>15 cl</b></li>
          <li><span>Œufs</span><b>2</b></li>
          <li><span>Thym frais</span><b>3 brins</b></li>
        </ul>
      </div>
      <div>
        <h3 class="dz-ct-recipe-h">Préparation</h3>
        <ol class="dz-ct-method">
          <li>Émincez les poireaux et faites-les fondre 10 min à feu doux.</li>
          <li>Battez œufs, crème et la moitié du comté râpé.</li>
          <li>Garnissez la pâte, parsemez du reste de comté et du thym.</li>
          <li>Enfournez 35 min à 190 °C, jusqu'à ce que le dessus soit doré.</li>
        </ol>
      </div>
    </div>
    <div class="dz-ct-callout dz-ct-tip"><i class="fas fa-lightbulb"></i><div><b>Le conseil du chef</b><p>Précuisez la pâte 8 min à blanc : elle restera croustillante sous la garniture.</p></div></div>
  </div>
</div>
"""),

]
