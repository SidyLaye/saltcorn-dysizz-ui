"""Famille Social : publications, fil, profils, commentaires, communauté, messagerie."""
FAMILY = "social"

# ---------------------------------------------------------------- fragments
# (réutilisés dans plusieurs blocs ; chaque bloc reste autonome une fois construit)

def _post_head(av, tint, name, handle, when, verified=False, extra=""):
    v = ' <i class="fas fa-check-circle dz-so-verif"></i>' if verified else ""
    return f"""
    <header class="dz-so-post-head">
      <span class="dz-avatar dz-so-av {tint}">{av}</span>
      <div class="dz-so-who">
        <p class="dz-so-name"><b>{name}</b>{v}{extra}</p>
        <p class="dz-so-meta">{handle} · {when} · <i class="fas fa-globe-europe"></i></p>
      </div>
      <a class="dz-so-ib" href="#" aria-label="Plus d'options"><i class="fas fa-ellipsis-h"></i></a>
    </header>"""


def _actions(liked=True, likes="", saved=False):
    heart = '<a class="dz-so-act dz-so-liked" href="#"><i class="fas fa-heart"></i> J\'aime</a>' if liked else '<a class="dz-so-act" href="#"><i class="far fa-heart"></i> J\'aime</a>'
    save = '<a class="dz-so-act dz-so-act-end dz-so-saved" href="#" aria-label="Enregistré"><i class="fas fa-bookmark"></i></a>' if saved else '<a class="dz-so-act dz-so-act-end" href="#" aria-label="Enregistrer"><i class="far fa-bookmark"></i></a>'
    return f"""
    <div class="dz-so-actions">
      {heart}
      <a class="dz-so-act" href="#"><i class="far fa-comment"></i> Commenter</a>
      <a class="dz-so-act" href="#"><i class="fas fa-retweet"></i> Partager</a>
      {save}
    </div>"""


BLOCKS = [
    # ------------------------------------------------------------ 1. publication
    dict(
        name="publication",
        icon="far fa-newspaper",
        wrap="section",
        html=f"""
<article class="dz-so-post dz-so-solo">
  {_post_head("CL", "dz-so-av-2", "Camille Laurent", "@camille.atelier", "il y a 2 h", verified=True)}
  <p class="dz-so-text">Premier four de la saison : 42 bols émaillés à la main, tous différents 🔥 Merci à celles et ceux qui sont venus à l'atelier samedi, vous avez été incroyables. Prochaine session le 14 mars, inscriptions ouvertes demain à 9 h. <a href="#">#céramique</a> <a href="#">#faitmain</a> <a href="#">@atelier.lune</a></p>
  <div class="dz-so-media"><img src="https://picsum.photos/seed/ceramique/1200/800" alt="Bols en céramique émaillés posés sur une étagère en bois"><span class="dz-so-media-count">1 / 4</span></div>
  <div class="dz-so-stats">
    <div class="dz-so-reacts"><span class="dz-so-emo">❤️</span><span class="dz-so-emo">👏</span><span class="dz-so-emo">😍</span><span class="dz-so-rc">Léa, Karim et 482 autres</span></div>
    <span class="dz-so-sub">36 commentaires · 12 partages</span>
  </div>
  {_actions(liked=True)}
  <div class="dz-so-cmt-preview">
    <div class="dz-so-cmt">
      <span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">KM</span>
      <div class="dz-so-cmt-main">
        <div class="dz-so-bubble"><p class="dz-so-cmt-who"><b>Karim Mansour</b></p><p class="dz-so-cmt-text">Le vert céladon du troisième est sublime. Tu gardes la recette de l'émail ? 😄</p></div>
        <p class="dz-so-cmt-bar"><span>1 h</span><a href="#">J'aime</a><a href="#">Répondre</a><span class="dz-so-cmt-likes">❤️ 18</span></p>
      </div>
    </div>
    <div class="dz-so-composer-row">
      <span class="dz-avatar dz-avatar-sm dz-so-av">MO</span>
      <div class="dz-so-field"><span class="dz-so-ph">Écrire un commentaire…</span><span class="dz-so-field-tools"><i class="far fa-smile"></i><i class="far fa-image"></i><i class="fas fa-at"></i></span></div>
    </div>
  </div>
</article>
""",
    ),
    # ------------------------------------------------------------ 2. fil d'actualité
    dict(
        name="fil d'actualité",
        icon="fas fa-stream",
        wrap="section",
        html=f"""
<div class="dz-so-feed-layout">
  <div class="dz-so-feed">
    <div class="dz-so-compose">
      <div class="dz-so-compose-top">
        <span class="dz-avatar dz-so-av">MO</span>
        <div class="dz-so-compose-field"><span>Quoi de neuf, Maëlle ?</span></div>
      </div>
      <div class="dz-so-compose-bar">
        <div class="dz-so-compose-tools">
          <a class="dz-so-tool dz-so-tool-photo" href="#"><i class="fas fa-image"></i> Photo</a>
          <a class="dz-so-tool dz-so-tool-poll" href="#"><i class="fas fa-poll-h"></i> Sondage</a>
          <a class="dz-so-tool dz-so-tool-event" href="#"><i class="fas fa-calendar-day"></i> Événement</a>
        </div>
        <a class="dz-btn dz-btn-sm" href="#">Publier</a>
      </div>
    </div>
    <div class="dz-so-feed-filter">
      <nav class="dz-so-seg"><a class="dz-so-seg-item dz-active" href="#">Pour vous</a><a class="dz-so-seg-item" href="#">Abonnements</a><a class="dz-so-seg-item" href="#">Récents</a></nav>
      <a class="dz-so-new" href="#"><i class="fas fa-arrow-up"></i> 6 nouvelles publications</a>
    </div>
    <article class="dz-so-post">
      {_post_head("TD", "dz-so-av-3", "Théo Dubois", "@theo.codes", "12 min", verified=False, extra=' <span class="dz-so-tag">Nouveau membre</span>')}
      <p class="dz-so-text">Trois mois après le lancement, notre appli de covoiturage rural dépasse les 2 000 trajets partagés 🚗 Le plus beau retour : une habitante de 83 ans qui va de nouveau au marché chaque mardi. <a href="#">#mobilité</a> <a href="#">#ruralité</a></p>
      <div class="dz-so-linkcard">
        <div class="dz-so-linkcard-img"><img src="https://picsum.photos/seed/route/600/400" alt="Route de campagne au lever du soleil"></div>
        <div class="dz-so-linkcard-body"><span class="dz-so-linkcard-host">blog.rouleensemble.fr</span><b>2 000 trajets : ce que nous avons appris</b><span class="dz-so-linkcard-desc">Retour d'expérience sur trois mois de covoiturage solidaire entre 14 villages du Perche.</span></div>
      </div>
      <div class="dz-so-stats">
        <div class="dz-so-reacts"><span class="dz-so-emo">👍</span><span class="dz-so-emo">🎉</span><span class="dz-so-rc">214</span></div>
        <span class="dz-so-sub">18 commentaires</span>
      </div>
      {_actions(liked=False)}
    </article>
    <article class="dz-so-post">
      {_post_head("AF", "dz-so-av-5", "Amina Fofana", "@amina.f", "1 h", verified=True)}
      <p class="dz-so-text">Carnet de voyage : quatre jours à pied sur les crêtes du Vercors, 68 km et beaucoup trop de fromage.</p>
      <div class="dz-so-mosaic">
        <img src="https://picsum.photos/seed/vercors1/800/800" alt="Crête rocheuse au coucher du soleil">
        <img src="https://picsum.photos/seed/vercors2/600/400" alt="Tente plantée dans une prairie">
        <div class="dz-so-mosaic-more"><img src="https://picsum.photos/seed/vercors3/600/400" alt="Randonneurs sur un sentier"><span>+ 9</span></div>
      </div>
      <div class="dz-so-stats">
        <div class="dz-so-reacts"><span class="dz-so-emo">❤️</span><span class="dz-so-emo">😮</span><span class="dz-so-rc">1,2 k</span></div>
        <span class="dz-so-sub">94 commentaires · 31 partages</span>
      </div>
      {_actions(liked=True, saved=True)}
    </article>
  </div>
  <aside class="dz-so-feed-side">
    <div class="dz-so-panel">
      <p class="dz-so-panel-title">Tendances pour vous</p>
      <a class="dz-so-trend-mini" href="#"><span>Culture · Tendance</span><b>#NuitDesMusées</b><span>12,4 k publications</span></a>
      <a class="dz-so-trend-mini" href="#"><span>Sport · En direct</span><b>Marathon de Lyon</b><span>8 210 publications</span></a>
      <a class="dz-so-trend-mini" href="#"><span>Tech · Tendance</span><b>#IAfrugale</b><span>3 905 publications</span></a>
    </div>
    <div class="dz-so-panel">
      <p class="dz-so-panel-title">Suggestions</p>
      <div class="dz-so-sugg"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">JR</span><div><b>Jules Roche</b><span>Photographe · Nantes</span></div><a class="dz-so-follow" href="#">Suivre</a></div>
      <div class="dz-so-sugg"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">SP</span><div><b>Sarah Petit</b><span>12 amis en commun</span></div><a class="dz-so-follow" href="#">Suivre</a></div>
    </div>
  </aside>
</div>
""",
    ),
    # ------------------------------------------------------------ 3. sondage
    dict(
        name="publication avec sondage",
        icon="fas fa-poll-h",
        wrap="section",
        html=f"""
<article class="dz-so-post dz-so-solo">
  {_post_head("LB", "dz-so-av-6", "Collectif Les Bricoleurs", "@lesbricoleurs", "hier", verified=True, extra=' <span class="dz-so-tag">Groupe</span>')}
  <p class="dz-so-text">On prépare le programme du printemps 🌱 Quel atelier voulez-vous voir en premier ? Le résultat sera annoncé dimanche soir.</p>
  <div class="dz-so-poll">
    <div class="dz-so-opt dz-so-opt-win dz-so-opt-mine" style="--v:46%"><span class="dz-so-opt-fill"></span><span class="dz-so-opt-label"><i class="fas fa-check-circle"></i> Réparer son vélo</span><b>46 %</b></div>
    <div class="dz-so-opt" style="--v:28%"><span class="dz-so-opt-fill"></span><span class="dz-so-opt-label">Menuiserie de base</span><b>28 %</b></div>
    <div class="dz-so-opt" style="--v:17%"><span class="dz-so-opt-fill"></span><span class="dz-so-opt-label">Électricité domestique</span><b>17 %</b></div>
    <div class="dz-so-opt" style="--v:9%"><span class="dz-so-opt-fill"></span><span class="dz-so-opt-label">Couture et retouches</span><b>9 %</b></div>
    <p class="dz-so-poll-foot"><span><b>1 348 votes</b></span><span>·</span><span><i class="far fa-clock"></i> encore 2 jours</span><span>·</span><a href="#">Annuler mon vote</a></p>
  </div>
  <div class="dz-so-stats">
    <div class="dz-so-reacts"><span class="dz-so-emo">👍</span><span class="dz-so-emo">🔧</span><span class="dz-so-rc">312</span></div>
    <span class="dz-so-sub">57 commentaires</span>
  </div>
  {_actions(liked=False)}
</article>
""",
    ),
    # ------------------------------------------------------------ 4. commentaires imbriqués
    dict(
        name="fil de commentaires",
        icon="far fa-comments",
        wrap="narrow",
        html="""
<div class="dz-so-thread">
  <div class="dz-so-thread-head">
    <h3 class="dz-so-thread-title">Commentaires <span class="dz-so-count">128</span></h3>
    <nav class="dz-so-seg dz-so-seg-sm"><a class="dz-so-seg-item dz-active" href="#">Les plus pertinents</a><a class="dz-so-seg-item" href="#">Récents</a></nav>
  </div>
  <div class="dz-so-composer-row dz-so-composer-lg">
    <span class="dz-avatar dz-avatar-sm dz-so-av">MO</span>
    <div class="dz-so-field"><span class="dz-so-ph">Ajouter un commentaire…</span><span class="dz-so-field-tools"><i class="far fa-smile"></i><i class="fas fa-paperclip"></i></span></div>
  </div>
  <div class="dz-so-cmt">
    <span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">NB</span>
    <div class="dz-so-cmt-main">
      <div class="dz-so-bubble dz-so-bubble-pin"><p class="dz-so-cmt-who"><b>Nadia Benali</b> <span class="dz-so-tag dz-so-tag-brand">Autrice</span> <span class="dz-so-pin"><i class="fas fa-thumbtack"></i> Épinglé</span></p><p class="dz-so-cmt-text">Merci pour toutes vos questions ! Je réponds à tout le monde ce soir. Le fichier des mesures est dans le lien en bio, version PDF et tableur.</p></div>
      <p class="dz-so-cmt-bar"><span>3 h</span><a class="dz-so-on" href="#">J'aime</a><a href="#">Répondre</a><span class="dz-so-cmt-likes">❤️ 👍 86</span></p>
      <div class="dz-so-replies">
        <div class="dz-so-cmt dz-so-reply">
          <span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">PG</span>
          <div class="dz-so-cmt-main">
            <div class="dz-so-bubble"><p class="dz-so-cmt-who"><b>Paul Garnier</b></p><p class="dz-so-cmt-text"><a href="#">@Nadia Benali</a> le tableur marche aussi pour des planches de 18 mm ?</p></div>
            <p class="dz-so-cmt-bar"><span>2 h</span><a href="#">J'aime</a><a href="#">Répondre</a><span class="dz-so-cmt-likes">👍 4</span></p>
          </div>
        </div>
        <div class="dz-so-cmt dz-so-reply">
          <span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">NB</span>
          <div class="dz-so-cmt-main">
            <div class="dz-so-bubble"><p class="dz-so-cmt-who"><b>Nadia Benali</b> <span class="dz-so-tag dz-so-tag-brand">Autrice</span></p><p class="dz-so-cmt-text">Oui, il suffit de changer l'épaisseur en cellule B2, tout se recalcule 🙂</p></div>
            <p class="dz-so-cmt-bar"><span>1 h</span><a href="#">J'aime</a><a href="#">Répondre</a><span class="dz-so-cmt-likes">❤️ 12</span></p>
          </div>
        </div>
        <a class="dz-so-more" href="#"><i class="fas fa-reply fa-flip-vertical"></i> Voir 8 autres réponses</a>
      </div>
    </div>
  </div>
  <div class="dz-so-cmt">
    <span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">EV</span>
    <div class="dz-so-cmt-main">
      <div class="dz-so-bubble"><p class="dz-so-cmt-who"><b>Élise Vasseur</b> <span class="dz-so-tag">Top contributrice</span></p><p class="dz-so-cmt-text">Astuce pour les débutants : poncez au grain 120 avant d'huiler, puis 240 entre les deux couches. Le résultat est vraiment plus doux au toucher.</p></div>
      <p class="dz-so-cmt-bar"><span>5 h</span><a href="#">J'aime</a><a href="#">Répondre</a><span class="dz-so-cmt-likes">👍 41</span></p>
    </div>
  </div>
  <div class="dz-so-cmt dz-so-cmt-deleted">
    <span class="dz-so-av-ghost"><i class="fas fa-user-slash"></i></span>
    <div class="dz-so-cmt-main">
      <div class="dz-so-bubble"><p class="dz-so-cmt-text">Ce commentaire a été supprimé par son auteur.</p></div>
    </div>
  </div>
  <a class="dz-so-loadmore" href="#">Afficher 124 commentaires de plus <i class="fas fa-chevron-down"></i></a>
</div>
""",
    ),
    # ------------------------------------------------------------ 5. profil public
    dict(
        name="profil public",
        icon="fas fa-id-badge",
        wrap="section",
        html="""
<div class="dz-so-profile">
  <div class="dz-so-cover"><img src="https://picsum.photos/seed/couverture/1600/500" alt="Photo de couverture : atelier de photographie"><a class="dz-so-cover-edit" href="#"><i class="fas fa-camera"></i> Modifier la couverture</a></div>
  <div class="dz-so-pbody">
    <div class="dz-so-pid">
      <div class="dz-so-bigav"><span class="dz-avatar dz-so-av">IM</span><span class="dz-so-online"></span></div>
      <div class="dz-so-pactions">
        <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-user-plus"></i> Suivre</a>
        <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-envelope"></i> Message</a>
        <a class="dz-so-ib dz-so-ib-bd" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a>
      </div>
    </div>
    <div class="dz-so-pinfo">
      <h2 class="dz-so-pname">Inès Moreau <i class="fas fa-check-circle dz-so-verif"></i></h2>
      <p class="dz-so-phandle">@ines.moreau <span class="dz-so-tag">Vous suit</span></p>
      <p class="dz-so-bio">Photographe culinaire et autrice de « Tables d'hiver ». Je partage mes lumières du matin, mes ratés et mes recettes du dimanche 🍋</p>
      <p class="dz-so-pmeta"><span><i class="fas fa-map-marker-alt"></i> Bordeaux</span><span><i class="fas fa-link"></i> <a href="#">inesmoreau.studio</a></span><span><i class="far fa-calendar"></i> Membre depuis mars 2021</span></p>
      <div class="dz-so-pstats">
        <a class="dz-so-pstat" href="#"><b>1 284</b><span>publications</span></a>
        <a class="dz-so-pstat" href="#"><b>48,6 k</b><span>abonnés</span></a>
        <a class="dz-so-pstat" href="#"><b>612</b><span>abonnements</span></a>
      </div>
      <div class="dz-so-mutual"><div class="dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">AB</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">RT</span></div><span>Suivie par <b>Léa Chevalier</b>, <b>Arthur Blanc</b> et 23 autres personnes que vous connaissez</span></div>
    </div>
    <div class="dz-so-highlights">
      <a class="dz-so-hl" href="#"><span class="dz-so-hl-ring"><img src="https://picsum.photos/seed/hl1/200/200" alt=""></span><span>Recettes</span></a>
      <a class="dz-so-hl" href="#"><span class="dz-so-hl-ring"><img src="https://picsum.photos/seed/hl2/200/200" alt=""></span><span>Coulisses</span></a>
      <a class="dz-so-hl" href="#"><span class="dz-so-hl-ring"><img src="https://picsum.photos/seed/hl3/200/200" alt=""></span><span>Voyages</span></a>
      <a class="dz-so-hl" href="#"><span class="dz-so-hl-ring"><img src="https://picsum.photos/seed/hl4/200/200" alt=""></span><span>Livre</span></a>
      <a class="dz-so-hl dz-so-hl-new" href="#"><span class="dz-so-hl-ring"><i class="fas fa-plus"></i></span><span>Nouveau</span></a>
    </div>
  </div>
  <nav class="dz-so-ptabs"><a class="dz-so-ptab dz-active" href="#"><i class="fas fa-th"></i> Publications</a><a class="dz-so-ptab" href="#"><i class="far fa-comment-dots"></i> Réponses</a><a class="dz-so-ptab" href="#"><i class="far fa-image"></i> Médias</a><a class="dz-so-ptab" href="#"><i class="far fa-heart"></i> J'aime</a></nav>
</div>
""",
    ),
    # ------------------------------------------------------------ 6. membres à suivre
    dict(
        name="membres à suivre",
        icon="fas fa-user-plus",
        wrap="section",
        html="""
<div class="dz-so-block-head">
  <div><h2 class="dz-so-h">Personnes à suivre</h2><p class="dz-so-hsub">D'après vos centres d'intérêt et vos abonnements</p></div>
  <a class="dz-so-textlink" href="#">Tout voir <i class="fas fa-arrow-right"></i></a>
</div>
<div class="dz-so-members">
  <div class="dz-so-member">
    <div class="dz-so-member-cover dz-so-cv-1"></div>
    <a class="dz-so-member-x" href="#" aria-label="Masquer la suggestion"><i class="fas fa-times"></i></a>
    <span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-2">LC</span>
    <b class="dz-so-member-name">Léa Chevalier</b>
    <span class="dz-so-member-role">Illustratrice jeunesse · Lille</span>
    <div class="dz-so-member-mutual"><div class="dz-avatars"><span class="dz-avatar dz-so-av dz-so-av-4 dz-so-av-xs">A</span><span class="dz-avatar dz-so-av dz-so-av-5 dz-so-av-xs">K</span></div><span>8 abonnés en commun</span></div>
    <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-user-plus"></i> Suivre</a>
  </div>
  <div class="dz-so-member">
    <div class="dz-so-member-cover dz-so-cv-2"></div>
    <a class="dz-so-member-x" href="#" aria-label="Masquer la suggestion"><i class="fas fa-times"></i></a>
    <span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-4">YK</span>
    <b class="dz-so-member-name">Yanis Kaci <i class="fas fa-check-circle dz-so-verif"></i></b>
    <span class="dz-so-member-role">Développeur · Rennes</span>
    <div class="dz-so-member-mutual"><div class="dz-avatars"><span class="dz-avatar dz-so-av dz-so-av-2 dz-so-av-xs">L</span></div><span>Suivi par Léa C.</span></div>
    <a class="dz-btn dz-btn-sm dz-btn-block dz-btn-ghost" href="#"><i class="fas fa-check"></i> Abonné</a>
  </div>
  <div class="dz-so-member">
    <div class="dz-so-member-cover dz-so-cv-3"></div>
    <a class="dz-so-member-x" href="#" aria-label="Masquer la suggestion"><i class="fas fa-times"></i></a>
    <span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-5">MR</span>
    <b class="dz-so-member-name">Manon Richard</b>
    <span class="dz-so-member-role">Cheffe · Marseille</span>
    <div class="dz-so-member-mutual"><div class="dz-avatars"><span class="dz-avatar dz-so-av dz-so-av-3 dz-so-av-xs">T</span><span class="dz-avatar dz-so-av dz-so-av-6 dz-so-av-xs">J</span><span class="dz-avatar dz-so-av dz-so-av-xs">S</span></div><span>21 abonnés en commun</span></div>
    <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-user-plus"></i> Suivre</a>
  </div>
  <div class="dz-so-member">
    <div class="dz-so-member-cover dz-so-cv-4"></div>
    <a class="dz-so-member-x" href="#" aria-label="Masquer la suggestion"><i class="fas fa-times"></i></a>
    <span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-6">OG</span>
    <b class="dz-so-member-name">Oscar Gauthier</b>
    <span class="dz-so-member-role">Musicien · Toulouse</span>
    <div class="dz-so-member-mutual"><span class="dz-so-new-badge">Nouveau sur la plateforme</span></div>
    <a class="dz-btn dz-btn-sm dz-btn-block" href="#"><i class="fas fa-user-plus"></i> Suivre</a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 7. forum
    dict(
        name="forum (sujets)",
        icon="fas fa-comments",
        wrap="section",
        html="""
<div class="dz-so-forum">
  <aside class="dz-so-forum-side">
    <a class="dz-btn dz-btn-block" href="#"><i class="fas fa-pen"></i> Nouveau sujet</a>
    <p class="dz-so-side-label">Catégories</p>
    <a class="dz-so-cat dz-active" href="#"><span class="dz-so-cat-dot dz-so-c1"></span>Tous les sujets<span class="dz-so-cat-n">2 481</span></a>
    <a class="dz-so-cat" href="#"><span class="dz-so-cat-dot dz-so-c2"></span>Entraide<span class="dz-so-cat-n">912</span></a>
    <a class="dz-so-cat" href="#"><span class="dz-so-cat-dot dz-so-c3"></span>Idées et retours<span class="dz-so-cat-n">438</span></a>
    <a class="dz-so-cat" href="#"><span class="dz-so-cat-dot dz-so-c4"></span>Vitrine des projets<span class="dz-so-cat-n">276</span></a>
    <a class="dz-so-cat" href="#"><span class="dz-so-cat-dot dz-so-c5"></span>Annonces<span class="dz-so-cat-n">54</span></a>
  </aside>
  <div class="dz-so-forum-main">
    <div class="dz-so-forum-bar">
      <nav class="dz-so-seg"><a class="dz-so-seg-item dz-active" href="#"><i class="fas fa-fire"></i> Populaires</a><a class="dz-so-seg-item" href="#">Récents</a><a class="dz-so-seg-item" href="#">Sans réponse</a></nav>
      <div class="dz-so-searchbox"><i class="fas fa-search"></i><span>Rechercher un sujet</span><span class="dz-kbd">/</span></div>
    </div>
    <div class="dz-so-topics">
      <div class="dz-so-topic dz-so-topic-pinned">
        <div class="dz-so-vote"><a class="dz-so-vote-up dz-active" href="#" aria-label="Voter pour"><i class="fas fa-caret-up"></i></a><b>248</b></div>
        <div class="dz-so-topic-main">
          <p class="dz-so-topic-flags"><span class="dz-so-flag dz-so-flag-pin"><i class="fas fa-thumbtack"></i> Épinglé</span><span class="dz-so-flag dz-so-flag-c5">Annonces</span></p>
          <a class="dz-so-topic-title" href="#">Feuille de route 2026 : ce qui arrive ce printemps</a>
          <p class="dz-so-topic-meta"><span class="dz-avatar dz-so-av dz-so-av-xs">É</span><span>Équipe Nexora</span><span class="dz-so-tag dz-so-tag-brand">Staff</span><span>· 3 j</span></p>
        </div>
        <div class="dz-so-topic-stats"><span><b>96</b> réponses</span><span><b>4,1 k</b> vues</span></div>
        <div class="dz-so-topic-last dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">KM</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">LC</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">+</span></div>
      </div>
      <div class="dz-so-topic">
        <div class="dz-so-vote"><a class="dz-so-vote-up" href="#" aria-label="Voter pour"><i class="fas fa-caret-up"></i></a><b>87</b></div>
        <div class="dz-so-topic-main">
          <p class="dz-so-topic-flags"><span class="dz-so-flag dz-so-flag-ok"><i class="fas fa-check"></i> Résolu</span><span class="dz-so-flag dz-so-flag-c2">Entraide</span></p>
          <a class="dz-so-topic-title" href="#">Comment exporter mes données au format tableur sans perdre les accents ?</a>
          <p class="dz-so-topic-meta"><span class="dz-avatar dz-so-av dz-so-av-2 dz-so-av-xs">H</span><span>Hugo Martin</span><span>· 5 h</span><span class="dz-so-hash">#export</span><span class="dz-so-hash">#encodage</span></p>
        </div>
        <div class="dz-so-topic-stats"><span><b>14</b> réponses</span><span><b>620</b> vues</span></div>
        <div class="dz-so-topic-last dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">SB</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">HM</span></div>
      </div>
      <div class="dz-so-topic">
        <div class="dz-so-vote"><a class="dz-so-vote-up" href="#" aria-label="Voter pour"><i class="fas fa-caret-up"></i></a><b>52</b></div>
        <div class="dz-so-topic-main">
          <p class="dz-so-topic-flags"><span class="dz-so-flag dz-so-flag-hot"><i class="fas fa-fire"></i> Tendance</span><span class="dz-so-flag dz-so-flag-c3">Idées et retours</span></p>
          <a class="dz-so-topic-title" href="#">Proposition : un mode hors ligne pour l'application mobile</a>
          <p class="dz-so-topic-meta"><span class="dz-avatar dz-so-av dz-so-av-4 dz-so-av-xs">C</span><span>Clara Noël</span><span>· 1 j</span><span class="dz-so-hash">#mobile</span></p>
        </div>
        <div class="dz-so-topic-stats"><span><b>38</b> réponses</span><span><b>1,9 k</b> vues</span></div>
        <div class="dz-so-topic-last dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">YK</span><span class="dz-avatar dz-avatar-sm dz-so-av">CN</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">+</span></div>
      </div>
      <div class="dz-so-topic">
        <div class="dz-so-vote"><a class="dz-so-vote-up" href="#" aria-label="Voter pour"><i class="fas fa-caret-up"></i></a><b>9</b></div>
        <div class="dz-so-topic-main">
          <p class="dz-so-topic-flags"><span class="dz-so-flag dz-so-flag-new">Nouveau</span><span class="dz-so-flag dz-so-flag-c4">Vitrine des projets</span></p>
          <a class="dz-so-topic-title" href="#">J'ai construit un suivi de ruches connectées avec la plateforme</a>
          <p class="dz-so-topic-meta"><span class="dz-avatar dz-so-av dz-so-av-6 dz-so-av-xs">B</span><span>Bastien Leroy</span><span>· 40 min</span></p>
        </div>
        <div class="dz-so-topic-stats"><span><b>0</b> réponse</span><span><b>31</b> vues</span></div>
        <div class="dz-so-topic-last"><span class="dz-so-noreply">Soyez le premier</span></div>
      </div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 8. serveur de discussion
    dict(
        name="serveur de discussion",
        icon="fas fa-server",
        wrap="section",
        html="""
<div class="dz-so-server">
  <nav class="dz-so-rail">
    <a class="dz-so-rail-home" href="#" aria-label="Messages privés"><i class="fas fa-comment-dots"></i></a>
    <span class="dz-so-rail-sep"></span>
    <a class="dz-so-rail-srv dz-active" href="#">AL</a>
    <a class="dz-so-rail-srv dz-so-rs-2" href="#">PX<span class="dz-so-rail-badge">3</span></a>
    <a class="dz-so-rail-srv dz-so-rs-3" href="#">JV</a>
    <a class="dz-so-rail-add" href="#" aria-label="Rejoindre un serveur"><i class="fas fa-plus"></i></a>
  </nav>
  <aside class="dz-so-chans">
    <div class="dz-so-chans-head"><b>Atelier Lune</b><i class="fas fa-chevron-down"></i></div>
    <div class="dz-so-chans-list">
      <p class="dz-so-chan-cat"><i class="fas fa-chevron-down"></i> Général</p>
      <a class="dz-so-chan" href="#"><i class="fas fa-hashtag"></i> annonces</a>
      <a class="dz-so-chan dz-active" href="#"><i class="fas fa-hashtag"></i> discussion</a>
      <a class="dz-so-chan dz-so-chan-unread" href="#"><i class="fas fa-hashtag"></i> entraide<span class="dz-so-chan-n">12</span></a>
      <a class="dz-so-chan" href="#"><i class="fas fa-hashtag"></i> vos-créations</a>
      <p class="dz-so-chan-cat"><i class="fas fa-chevron-down"></i> Salons vocaux</p>
      <a class="dz-so-chan" href="#"><i class="fas fa-volume-up"></i> Café du matin</a>
      <div class="dz-so-voice"><span class="dz-avatar dz-so-av dz-so-av-3 dz-so-av-xs dz-so-speaking">N</span><span>Nadia</span></div>
      <div class="dz-so-voice"><span class="dz-avatar dz-so-av dz-so-av-5 dz-so-av-xs">T</span><span>Théo</span><i class="fas fa-microphone-slash"></i></div>
      <a class="dz-so-chan" href="#"><i class="fas fa-volume-up"></i> Atelier en direct</a>
    </div>
    <div class="dz-so-me"><span class="dz-avatar dz-avatar-sm dz-so-av">MO</span><div><b>Maëlle</b><span>En ligne</span></div><i class="fas fa-microphone"></i><i class="fas fa-headphones"></i><i class="fas fa-cog"></i></div>
  </aside>
  <main class="dz-so-room">
    <div class="dz-so-room-head"><i class="fas fa-hashtag"></i><b>discussion</b><span class="dz-so-room-topic">Parlez de tout, sauf de politique 🙂</span><div class="dz-so-room-tools"><i class="fas fa-bell"></i><i class="fas fa-thumbtack"></i><i class="fas fa-user-friends"></i></div></div>
    <div class="dz-so-room-msgs">
      <div class="dz-so-daysep"><span>Aujourd'hui</span></div>
      <div class="dz-so-m">
        <span class="dz-avatar dz-so-av dz-so-av-3">NB</span>
        <div class="dz-so-m-body">
          <p class="dz-so-m-head"><b class="dz-so-role-mod">Nadia Benali</b><span class="dz-so-tag dz-so-tag-brand">Modo</span><time>09:12</time></p>
          <p class="dz-so-m-text">Bonjour tout le monde ! Le live « émaillage » commence à 18 h dans <a href="#">#atelier-en-direct</a> 🎨</p>
          <p class="dz-so-m-text">Pensez à préparer vos pièces biscuitées.</p>
          <div class="dz-so-m-reacts"><span class="dz-so-r dz-so-r-on">🎉 14</span><span class="dz-so-r">🔥 6</span><span class="dz-so-r">🙌 3</span><span class="dz-so-r dz-so-r-add"><i class="far fa-smile"></i></span></div>
        </div>
      </div>
      <div class="dz-so-m">
        <span class="dz-avatar dz-so-av dz-so-av-4">KM</span>
        <div class="dz-so-m-body">
          <p class="dz-so-m-head"><b>Karim Mansour</b><time>09:20</time></p>
          <p class="dz-so-m-text">Top ! Quelqu'un a un conseil pour éviter les bulles sur le blanc satiné ?</p>
          <a class="dz-so-m-thread" href="#"><span class="dz-avatars"><span class="dz-avatar dz-so-av dz-so-av-5 dz-so-av-xs">É</span><span class="dz-avatar dz-so-av dz-so-av-3 dz-so-av-xs">N</span></span><b>5 réponses</b><span>Dernière il y a 4 min</span></a>
        </div>
      </div>
      <div class="dz-so-m dz-so-m-mention">
        <span class="dz-avatar dz-so-av dz-so-av-5">ÉV</span>
        <div class="dz-so-m-body">
          <p class="dz-so-m-head"><b>Élise Vasseur</b><time>09:34</time></p>
          <p class="dz-so-m-text"><span class="dz-so-mention">@Maëlle</span> tu nous montres ta théière terminée ?</p>
        </div>
      </div>
      <div class="dz-so-typing"><span class="dz-typing"><i></i><i></i><i></i></span><span><b>Théo</b> est en train d'écrire…</span></div>
    </div>
    <div class="dz-so-room-compose"><i class="fas fa-plus-circle"></i><span>Envoyer un message dans #discussion</span><i class="fas fa-gift"></i><i class="far fa-smile"></i></div>
  </main>
  <aside class="dz-so-people">
    <p class="dz-so-people-cat">Modération — 2</p>
    <div class="dz-so-person"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">NB</span><span class="dz-so-st dz-so-st-on"></span></span><div><b class="dz-so-role-mod">Nadia Benali</b><span>Anime le live à 18 h</span></div></div>
    <div class="dz-so-person"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">JR</span><span class="dz-so-st dz-so-st-idle"></span></span><div><b class="dz-so-role-mod">Jules Roche</b><span>Absent</span></div></div>
    <p class="dz-so-people-cat">En ligne — 38</p>
    <div class="dz-so-person"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">KM</span><span class="dz-so-st dz-so-st-on"></span></span><div><b>Karim Mansour</b></div></div>
    <div class="dz-so-person"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">ÉV</span><span class="dz-so-st dz-so-st-dnd"></span></span><div><b>Élise Vasseur</b><span>Ne pas déranger</span></div></div>
    <div class="dz-so-person"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av">MO</span><span class="dz-so-st dz-so-st-on"></span></span><div><b>Maëlle O.</b></div></div>
    <p class="dz-so-people-cat">Hors ligne — 212</p>
    <div class="dz-so-person dz-so-off"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">PG</span></span><div><b>Paul Garnier</b></div></div>
  </aside>
</div>
""",
    ),
    # ------------------------------------------------------------ 9. notifications
    dict(
        name="notifications sociales",
        icon="fas fa-bell",
        wrap="narrow",
        html="""
<div class="dz-so-notifs">
  <div class="dz-so-notifs-head">
    <h3 class="dz-so-thread-title">Notifications <span class="dz-so-count dz-so-count-hot">5</span></h3>
    <a class="dz-so-textlink" href="#"><i class="fas fa-check-double"></i> Tout marquer comme lu</a>
  </div>
  <nav class="dz-so-underline"><a class="dz-so-ul-item dz-active" href="#">Tout</a><a class="dz-so-ul-item" href="#">Mentions <span class="dz-so-count">2</span></a><a class="dz-so-ul-item" href="#">Abonnés</a><a class="dz-so-ul-item" href="#">Groupes</a></nav>
  <p class="dz-so-ngroup">Aujourd'hui</p>
  <div class="dz-so-n dz-so-n-unread">
    <span class="dz-so-nav"><span class="dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">KM</span></span><span class="dz-so-nbadge dz-so-nb-like"><i class="fas fa-heart"></i></span></span>
    <p class="dz-so-ntext dz-so-ntext-t"><b>Léa Chevalier</b>, <b>Karim Mansour</b> et 46 autres ont aimé votre photo « Brouillard sur la Garonne ».<time>il y a 8 min</time></p>
    <span class="dz-so-nthumb"><img src="https://picsum.photos/seed/garonne/160/160" alt="Miniature de la photo"></span>
  </div>
  <div class="dz-so-n dz-so-n-unread">
    <span class="dz-so-nav"><span class="dz-avatar dz-so-av dz-so-av-3">TD</span><span class="dz-so-nbadge dz-so-nb-mention"><i class="fas fa-at"></i></span></span>
    <div class="dz-so-nmain"><p class="dz-so-ntext"><b>Théo Dubois</b> vous a mentionnée dans un commentaire<time>il y a 32 min</time></p><p class="dz-so-nquote">« <span>@Maëlle</span> c'est exactement le rendu dont je parlais hier, bravo ! »</p><p class="dz-so-nactions"><a href="#"><i class="fas fa-reply"></i> Répondre</a><a href="#"><i class="far fa-heart"></i> J'aime</a></p></div>
  </div>
  <div class="dz-so-n dz-so-n-unread">
    <span class="dz-so-nav"><span class="dz-avatar dz-so-av dz-so-av-5">AF</span><span class="dz-so-nbadge dz-so-nb-follow"><i class="fas fa-user-plus"></i></span></span>
    <p class="dz-so-ntext"><b>Amina Fofana</b> a commencé à vous suivre<time>il y a 2 h</time></p>
    <a class="dz-btn dz-btn-sm" href="#">Suivre en retour</a>
  </div>
  <p class="dz-so-ngroup">Cette semaine</p>
  <div class="dz-so-n">
    <span class="dz-so-nav"><span class="dz-avatar dz-so-av dz-so-av-6">LB</span><span class="dz-so-nbadge dz-so-nb-group"><i class="fas fa-users"></i></span></span>
    <p class="dz-so-ntext"><b>Les Bricoleurs</b> ont accepté votre demande d'adhésion. Bienvenue parmi 3 412 membres !<time>mardi</time></p>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Voir le groupe</a>
  </div>
  <div class="dz-so-n">
    <span class="dz-so-nav"><span class="dz-so-nsys"><i class="fas fa-trophy"></i></span></span>
    <p class="dz-so-ntext">Nouveau badge débloqué : <b>Plume d'or</b> — 100 réponses utiles dans le forum 🎉<time>lundi</time></p>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 10. réactions
    dict(
        name="réactions emoji",
        icon="far fa-smile-beam",
        wrap="section",
        html="""
<div class="dz-so-react-demo">
  <div class="dz-so-react-left">
    <p class="dz-so-eyebrow">Réagir à une publication</p>
    <div class="dz-so-picker">
      <a class="dz-so-pick" href="#" aria-label="J'aime"><span>👍</span></a>
      <a class="dz-so-pick dz-so-pick-on" href="#" aria-label="J'adore"><span>❤️</span></a>
      <a class="dz-so-pick" href="#" aria-label="Haha"><span>😂</span></a>
      <a class="dz-so-pick" href="#" aria-label="Waouh"><span>😮</span></a>
      <a class="dz-so-pick" href="#" aria-label="Soutien"><span>🤗</span></a>
      <a class="dz-so-pick" href="#" aria-label="Bravo"><span>👏</span></a>
      <a class="dz-so-pick dz-so-pick-more" href="#" aria-label="Plus d'emoji"><i class="fas fa-plus"></i></a>
    </div>
    <div class="dz-so-chipsr">
      <a class="dz-so-r dz-so-r-on" href="#">❤️ 128</a><a class="dz-so-r" href="#">👏 64</a><a class="dz-so-r" href="#">😂 22</a><a class="dz-so-r" href="#">🔥 9</a><a class="dz-so-r dz-so-r-add" href="#" aria-label="Ajouter une réaction"><i class="far fa-smile"></i><i class="fas fa-plus dz-so-r-plus"></i></a>
    </div>
    <p class="dz-so-hint">Survolez un emoji : il grossit. Cliquez sur une pastille pour ajouter ou retirer votre réaction.</p>
  </div>
  <div class="dz-so-whoreact">
    <div class="dz-so-whoreact-head"><b>Réactions</b><a class="dz-so-ib" href="#" aria-label="Fermer"><i class="fas fa-times"></i></a></div>
    <nav class="dz-so-underline"><a class="dz-so-ul-item dz-active" href="#">Tout 223</a><a class="dz-so-ul-item" href="#">❤️ 128</a><a class="dz-so-ul-item" href="#">👏 64</a><a class="dz-so-ul-item" href="#">😂 22</a></nav>
    <div class="dz-so-wr"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><span class="dz-so-wr-emo">❤️</span></span><div><b>Léa Chevalier</b><span>Illustratrice</span></div><a class="dz-so-follow dz-so-follow-on" href="#">Abonné</a></div>
    <div class="dz-so-wr"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">KM</span><span class="dz-so-wr-emo">👏</span></span><div><b>Karim Mansour</b><span>3 amis en commun</span></div><a class="dz-so-follow" href="#">Suivre</a></div>
    <div class="dz-so-wr"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">AF</span><span class="dz-so-wr-emo">😂</span></span><div><b>Amina Fofana</b><span>Voyageuse</span></div><a class="dz-so-follow" href="#">Suivre</a></div>
    <div class="dz-so-wr"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">JR</span><span class="dz-so-wr-emo">❤️</span></span><div><b>Jules Roche</b><span>Photographe</span></div><a class="dz-so-follow" href="#">Suivre</a></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 11. tendances
    dict(
        name="hashtags tendances",
        icon="fas fa-hashtag",
        wrap="narrow",
        html="""
<div class="dz-so-trends">
  <div class="dz-so-trends-head">
    <h3 class="dz-so-thread-title"><i class="fas fa-bolt dz-so-ico-hot"></i> Tendances</h3>
    <nav class="dz-so-seg dz-so-seg-sm"><a class="dz-so-seg-item dz-active" href="#">France</a><a class="dz-so-seg-item" href="#">Monde</a><a class="dz-so-seg-item" href="#">Pour vous</a></nav>
  </div>
  <a class="dz-so-trend" href="#"><span class="dz-so-rank">1</span><div class="dz-so-trend-main"><span class="dz-so-trend-cat">Culture · Tendance</span><b>#NuitDesMusées</b><span class="dz-so-trend-n">48,2 k publications</span></div><span class="dz-so-spark dz-so-spark-up"><i style="--h:30%"></i><i style="--h:42%"></i><i style="--h:38%"></i><i style="--h:60%"></i><i style="--h:74%"></i><i style="--h:100%"></i></span><span class="dz-so-delta dz-so-delta-up"><i class="fas fa-arrow-up"></i> 312 %</span></a>
  <a class="dz-so-trend" href="#"><span class="dz-so-rank">2</span><div class="dz-so-trend-main"><span class="dz-so-trend-cat">Sport · <span class="dz-so-live-mini">● En direct</span></span><b>Marathon de Lyon</b><span class="dz-so-trend-n">31,7 k publications</span></div><span class="dz-so-spark dz-so-spark-up"><i style="--h:20%"></i><i style="--h:26%"></i><i style="--h:48%"></i><i style="--h:70%"></i><i style="--h:88%"></i><i style="--h:96%"></i></span><span class="dz-so-delta dz-so-delta-up"><i class="fas fa-arrow-up"></i> 180 %</span></a>
  <a class="dz-so-trend" href="#"><span class="dz-so-rank">3</span><div class="dz-so-trend-main"><span class="dz-so-trend-cat">Technologie · Tendance</span><b>#IAfrugale</b><span class="dz-so-trend-n">12,9 k publications</span></div><span class="dz-so-spark"><i style="--h:60%"></i><i style="--h:64%"></i><i style="--h:58%"></i><i style="--h:66%"></i><i style="--h:70%"></i><i style="--h:68%"></i></span><span class="dz-so-delta"><i class="fas fa-minus"></i> stable</span></a>
  <a class="dz-so-trend" href="#"><span class="dz-so-rank">4</span><div class="dz-so-trend-main"><span class="dz-so-trend-cat">Cuisine · Tendance</span><b>#RecettesDeSaison</b><span class="dz-so-trend-n">9 480 publications</span></div><span class="dz-so-spark dz-so-spark-up"><i style="--h:18%"></i><i style="--h:22%"></i><i style="--h:30%"></i><i style="--h:44%"></i><i style="--h:50%"></i><i style="--h:62%"></i></span><span class="dz-so-delta dz-so-delta-up"><i class="fas fa-arrow-up"></i> 64 %</span></a>
  <a class="dz-so-trend" href="#"><span class="dz-so-rank">5</span><div class="dz-so-trend-main"><span class="dz-so-trend-cat">Environnement</span><b>#VéloAuTravail</b><span class="dz-so-trend-n">6 115 publications</span></div><span class="dz-so-spark dz-so-spark-down"><i style="--h:90%"></i><i style="--h:84%"></i><i style="--h:70%"></i><i style="--h:62%"></i><i style="--h:48%"></i><i style="--h:40%"></i></span><span class="dz-so-delta dz-so-delta-down"><i class="fas fa-arrow-down"></i> 22 %</span></a>
  <a class="dz-so-trends-more" href="#">Afficher plus de tendances</a>
</div>
""",
    ),
    # ------------------------------------------------------------ 12. galerie de posts
    dict(
        name="galerie de publications",
        icon="fas fa-th",
        wrap="section",
        html="""
<div class="dz-so-gridwrap">
  <nav class="dz-so-ptabs dz-so-ptabs-center"><a class="dz-so-ptab dz-active" href="#"><i class="fas fa-th"></i> Publications</a><a class="dz-so-ptab" href="#"><i class="fas fa-film"></i> Vidéos</a><a class="dz-so-ptab" href="#"><i class="far fa-bookmark"></i> Enregistrées</a><a class="dz-so-ptab" href="#"><i class="fas fa-user-tag"></i> Identifiée</a></nav>
  <div class="dz-so-pgrid">
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g1/600/600" alt="Tarte aux citrons meringuée"><span class="dz-so-tile-ico"><i class="fas fa-clone"></i></span><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 2 481</span><span><i class="fas fa-comment"></i> 96</span></span></a>
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g2/600/600" alt="Marché aux légumes du samedi"><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 1 204</span><span><i class="fas fa-comment"></i> 38</span></span></a>
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g3/600/600" alt="Préparation de pâtes fraîches"><span class="dz-so-tile-ico"><i class="fas fa-play"></i></span><span class="dz-so-tile-views"><i class="fas fa-play"></i> 18,4 k</span><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 3 920</span><span><i class="fas fa-comment"></i> 214</span></span></a>
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g4/600/600" alt="Table dressée pour un dîner d'hiver"><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 860</span><span><i class="fas fa-comment"></i> 17</span></span></a>
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g5/600/600" alt="Pain au levain sortant du four"><span class="dz-so-tile-ico"><i class="fas fa-clone"></i></span><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 5 012</span><span><i class="fas fa-comment"></i> 301</span></span></a>
    <a class="dz-so-tile" href="#"><img src="https://picsum.photos/seed/g6/600/600" alt="Café et croissant en terrasse"><span class="dz-so-tile-over"><span><i class="fas fa-heart"></i> 742</span><span><i class="fas fa-comment"></i> 12</span></span></a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 13. événements
    dict(
        name="événements de la communauté",
        icon="fas fa-calendar-check",
        wrap="section",
        html="""
<div class="dz-so-block-head">
  <div><h2 class="dz-so-h">Événements à venir</h2><p class="dz-so-hsub">Rencontres, ateliers et lives organisés par les membres</p></div>
  <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-plus"></i> Créer un événement</a>
</div>
<div class="dz-so-events">
  <article class="dz-so-event dz-so-event-feat">
    <div class="dz-so-event-img"><img src="https://picsum.photos/seed/meetup/900/500" alt="Salle de conférence pleine lors d'une rencontre"><span class="dz-so-event-date"><b>14</b><span>mars</span></span><span class="dz-so-event-type"><i class="fas fa-map-marker-alt"></i> Sur place</span></div>
    <div class="dz-so-event-body">
      <p class="dz-so-event-when">Samedi 14 mars 2026 · 10:00 – 17:30</p>
      <h3 class="dz-so-event-title">Rencontre annuelle des makers de Nouvelle-Aquitaine</h3>
      <p class="dz-so-event-where"><i class="fas fa-map-pin"></i> La Fabrique, 12 quai des Chartrons, Bordeaux</p>
      <div class="dz-so-event-foot">
        <div class="dz-so-going"><div class="dz-avatars"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">NB</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">KM</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-5">+</span></div><span><b>184 participants</b> · 32 places restantes</span></div>
        <div class="dz-so-event-cta"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-check"></i> Je participe</a><a class="dz-so-ib dz-so-ib-bd" href="#" aria-label="Partager"><i class="fas fa-share"></i></a></div>
      </div>
    </div>
  </article>
  <div class="dz-so-event-list">
    <a class="dz-so-event-row" href="#"><span class="dz-so-cal"><span>MAR</span><b>19</b></span><div><p class="dz-so-event-when">Jeu. 19 mars · 18:30 · <span class="dz-so-online-tag">En ligne</span></p><b class="dz-so-event-rt">Live : bien photographier ses créations</b><span class="dz-so-event-sub">Animé par Inès Moreau · 412 inscrits</span></div><i class="fas fa-chevron-right"></i></a>
    <a class="dz-so-event-row" href="#"><span class="dz-so-cal"><span>MAR</span><b>28</b></span><div><p class="dz-so-event-when">Sam. 28 mars · 14:00 · Lyon</p><b class="dz-so-event-rt">Repair café du printemps</b><span class="dz-so-event-sub">Les Bricoleurs · 67 participants</span></div><i class="fas fa-chevron-right"></i></a>
    <a class="dz-so-event-row" href="#"><span class="dz-so-cal"><span>AVR</span><b>04</b></span><div><p class="dz-so-event-when">Sam. 4 avril · 09:00 · <span class="dz-so-online-tag">En ligne</span></p><b class="dz-so-event-rt">Hackathon « Outils pour associations »</b><span class="dz-so-event-sub">48 h · 23 équipes inscrites</span></div><i class="fas fa-chevron-right"></i></a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 14. classement
    dict(
        name="classement des contributeurs",
        icon="fas fa-trophy",
        wrap="narrow",
        html="""
<div class="dz-so-board">
  <div class="dz-so-board-head">
    <div><h3 class="dz-so-thread-title">Classement des contributeurs</h3><p class="dz-so-hsub">Points gagnés en mars 2026 · mis à jour il y a 5 min</p></div>
    <nav class="dz-so-seg dz-so-seg-sm"><a class="dz-so-seg-item" href="#">Semaine</a><a class="dz-so-seg-item dz-active" href="#">Mois</a><a class="dz-so-seg-item" href="#">Toujours</a></nav>
  </div>
  <div class="dz-so-podium">
    <div class="dz-so-pod dz-so-pod-2"><span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-4">KM</span><b>Karim M.</b><span class="dz-so-pts">3 840 pts</span><div class="dz-so-pod-step"><span>2</span></div></div>
    <div class="dz-so-pod dz-so-pod-1"><span class="dz-so-crown"><i class="fas fa-crown"></i></span><span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-3">NB</span><b>Nadia B.</b><span class="dz-so-pts">4 915 pts</span><div class="dz-so-pod-step"><span>1</span></div></div>
    <div class="dz-so-pod dz-so-pod-3"><span class="dz-avatar dz-avatar-lg dz-so-av dz-so-av-5">ÉV</span><b>Élise V.</b><span class="dz-so-pts">3 102 pts</span><div class="dz-so-pod-step"><span>3</span></div></div>
  </div>
  <div class="dz-so-ranks">
    <div class="dz-so-rk"><span class="dz-so-rk-n">4</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">JR</span><div class="dz-so-rk-who"><b>Jules Roche</b><span>142 réponses · 38 solutions</span></div><span class="dz-so-rk-move dz-so-up"><i class="fas fa-caret-up"></i> 3</span><b class="dz-so-rk-pts">2 760</b></div>
    <div class="dz-so-rk"><span class="dz-so-rk-n">5</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><div class="dz-so-rk-who"><b>Léa Chevalier</b><span>98 réponses · 21 solutions</span></div><span class="dz-so-rk-move dz-so-down"><i class="fas fa-caret-down"></i> 1</span><b class="dz-so-rk-pts">2 415</b></div>
    <div class="dz-so-rk"><span class="dz-so-rk-n">6</span><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">YK</span><div class="dz-so-rk-who"><b>Yanis Kaci</b><span>77 réponses · 30 solutions</span></div><span class="dz-so-rk-move"><i class="fas fa-minus"></i></span><b class="dz-so-rk-pts">2 180</b></div>
    <div class="dz-so-rk dz-so-rk-me"><span class="dz-so-rk-n">24</span><span class="dz-avatar dz-avatar-sm dz-so-av">MO</span><div class="dz-so-rk-who"><b>Vous</b><span>Plus que 140 pts pour entrer dans le top 20</span></div><span class="dz-so-rk-move dz-so-up"><i class="fas fa-caret-up"></i> 9</span><b class="dz-so-rk-pts">980</b></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 15. badges
    dict(
        name="badges et succès",
        icon="fas fa-medal",
        wrap="section",
        html="""
<div class="dz-so-level">
  <div class="dz-so-level-ring"><span class="dz-so-level-n">12</span><span>niveau</span></div>
  <div class="dz-so-level-main">
    <p class="dz-so-eyebrow">Votre progression</p>
    <h3 class="dz-so-h">Artisane confirmée</h3>
    <div class="dz-so-xp"><span class="dz-so-xp-fill" style="--v:68%"></span></div>
    <p class="dz-so-xp-legend"><span><b>6 820</b> / 10 000 XP</span><span>Prochain niveau : <b>Maîtresse d'atelier</b></span></p>
  </div>
  <div class="dz-so-level-stats"><div><b>14</b><span>badges</span></div><div><b>🔥 23</b><span>jours de suite</span></div></div>
</div>
<div class="dz-so-badges">
  <div class="dz-so-badge dz-so-bd-gold"><span class="dz-so-medal"><i class="fas fa-feather-alt"></i></span><b>Plume d'or</b><span>100 réponses utiles</span><span class="dz-so-bd-date">Obtenu le 2 mars</span></div>
  <div class="dz-so-badge dz-so-bd-brand"><span class="dz-so-medal"><i class="fas fa-seedling"></i></span><b>Mentor</b><span>A aidé 25 nouveaux membres</span><span class="dz-so-bd-date">Obtenu le 18 févr.</span></div>
  <div class="dz-so-badge dz-so-bd-accent"><span class="dz-so-medal"><i class="fas fa-fire"></i></span><b>Assiduité</b><span>30 jours d'affilée</span><span class="dz-so-bd-date">Obtenu le 9 janv.</span></div>
  <div class="dz-so-badge dz-so-bd-rare"><span class="dz-so-medal"><i class="fas fa-gem"></i></span><b>Pionnière</b><span>Membre de la première heure</span><span class="dz-so-bd-rarity">Rare · 2 % des membres</span></div>
  <div class="dz-so-badge dz-so-locked"><span class="dz-so-medal"><i class="fas fa-lock"></i></span><b>Organisatrice</b><span>Créer 5 événements</span><div class="dz-so-bd-prog"><span style="--v:60%"></span></div><span class="dz-so-bd-date">3 / 5</span></div>
  <div class="dz-so-badge dz-so-locked"><span class="dz-so-medal"><i class="fas fa-lock"></i></span><b>Influence</b><span>1 000 abonnés</span><div class="dz-so-bd-prog"><span style="--v:84%"></span></div><span class="dz-so-bd-date">842 / 1 000</span></div>
</div>
""",
    ),
    # ------------------------------------------------------------ 16. parrainage
    dict(
        name="invitation parrainage",
        icon="fas fa-gift",
        wrap="section",
        html="""
<div class="dz-so-refer">
  <div class="dz-so-refer-main">
    <span class="dz-so-refer-gift"><i class="fas fa-gift"></i></span>
    <p class="dz-so-eyebrow">Programme de parrainage</p>
    <h2 class="dz-so-refer-title">Invitez vos proches, gagnez <em>1 mois offert</em> chacun</h2>
    <p class="dz-so-refer-lead">Pour chaque ami qui rejoint la communauté avec votre lien, vous recevez tous les deux un mois de l'offre Plus. Sans limite.</p>
    <div class="dz-so-copy dz-copy-scope"><i class="fas fa-link"></i><code class="dz-so-code">nexora.fr/r/maelle-7K2Q</code><a class="dz-btn dz-btn-sm dz-copy" href="#"><i class="far fa-copy"></i> Copier</a></div>
    <div class="dz-so-share">
      <a class="dz-so-share-btn" href="#"><i class="fas fa-envelope"></i> E-mail</a>
      <a class="dz-so-share-btn" href="#"><i class="fas fa-sms"></i> SMS</a>
      <a class="dz-so-share-btn" href="#"><i class="fas fa-qrcode"></i> QR code</a>
      <a class="dz-so-share-btn" href="#"><i class="fas fa-share-alt"></i> Autre</a>
    </div>
  </div>
  <div class="dz-so-refer-side">
    <div class="dz-so-refer-goal">
      <div class="dz-so-refer-goal-top"><b>3 amis sur 5</b><span>Palier suivant : badge « Ambassadrice »</span></div>
      <div class="dz-so-steps"><span class="dz-so-stp dz-done"><i class="fas fa-check"></i></span><span class="dz-so-stp-line dz-done"></span><span class="dz-so-stp dz-done"><i class="fas fa-check"></i></span><span class="dz-so-stp-line dz-done"></span><span class="dz-so-stp dz-done"><i class="fas fa-check"></i></span><span class="dz-so-stp-line"></span><span class="dz-so-stp">4</span><span class="dz-so-stp-line"></span><span class="dz-so-stp dz-so-stp-gift"><i class="fas fa-gift"></i></span></div>
    </div>
    <div class="dz-so-invited">
      <div class="dz-so-inv"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">SP</span><div><b>Sarah Petit</b><span>Inscrite le 3 mars</span></div><span class="dz-badge dz-badge-success">+1 mois</span></div>
      <div class="dz-so-inv"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">HM</span><div><b>Hugo Martin</b><span>Inscrit le 27 févr.</span></div><span class="dz-badge dz-badge-success">+1 mois</span></div>
      <div class="dz-so-inv"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-6">cl</span><div><b>clara.n@…</b><span>Invitation envoyée hier</span></div><span class="dz-badge dz-badge-warning">En attente</span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 17. messages privés
    dict(
        name="messages privés",
        icon="fas fa-paper-plane",
        wrap="section",
        html="""
<div class="dz-so-dm">
  <aside class="dz-so-dm-list">
    <div class="dz-so-dm-list-head"><b>Messages</b><a class="dz-so-ib" href="#" aria-label="Nouveau message"><i class="far fa-edit"></i></a></div>
    <div class="dz-so-searchbox dz-so-searchbox-full"><i class="fas fa-search"></i><span>Rechercher</span></div>
    <a class="dz-so-conv dz-active" href="#"><span class="dz-so-pav"><span class="dz-avatar dz-so-av dz-so-av-2">LC</span><span class="dz-so-st dz-so-st-on"></span></span><div class="dz-so-conv-main"><p class="dz-so-conv-top"><b>Léa Chevalier</b><time>10:42</time></p><span class="dz-so-conv-last">Tu es dispo samedi pour le shooting ?</span></div></a>
    <a class="dz-so-conv dz-so-conv-unread" href="#"><span class="dz-so-pav"><span class="dz-avatar dz-so-av dz-so-av-4">KM</span><span class="dz-so-st dz-so-st-on"></span></span><div class="dz-so-conv-main"><p class="dz-so-conv-top"><b>Karim Mansour</b><time>09:15</time></p><span class="dz-so-conv-last">J'ai envoyé la facture 📎</span></div><span class="dz-so-unread-n">2</span></a>
    <a class="dz-so-conv" href="#"><span class="dz-so-pav"><span class="dz-avatar dz-so-av dz-so-av-6">LB</span></span><div class="dz-so-conv-main"><p class="dz-so-conv-top"><b>Les Bricoleurs</b><time>hier</time></p><span class="dz-so-conv-last">Paul : on garde la date du 28 ?</span></div></a>
    <a class="dz-so-conv" href="#"><span class="dz-so-pav"><span class="dz-avatar dz-so-av dz-so-av-5">AF</span></span><div class="dz-so-conv-main"><p class="dz-so-conv-top"><b>Amina Fofana</b><time>lun.</time></p><span class="dz-so-conv-last">Vous : Merci pour les photos !</span></div></a>
  </aside>
  <section class="dz-so-dm-chat">
    <div class="dz-so-dm-head"><span class="dz-so-pav"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-2">LC</span><span class="dz-so-st dz-so-st-on"></span></span><div><b>Léa Chevalier</b><span>En ligne</span></div><div class="dz-so-dm-tools"><a class="dz-so-ib" href="#" aria-label="Appel"><i class="fas fa-phone"></i></a><a class="dz-so-ib" href="#" aria-label="Appel vidéo"><i class="fas fa-video"></i></a><a class="dz-so-ib" href="#" aria-label="Infos"><i class="fas fa-info-circle"></i></a></div></div>
    <div class="dz-so-dm-msgs">
      <div class="dz-so-daysep"><span>Aujourd'hui</span></div>
      <div class="dz-so-bub">Coucou ! J'ai vu ta série sur les marchés, la lumière est dingue ✨</div>
      <div class="dz-so-bub dz-so-bub-cont">Tu es dispo samedi pour le shooting ?</div>
      <div class="dz-so-bub dz-so-me">Merci 🥰 Oui samedi c'est parfait, plutôt le matin ?</div>
      <div class="dz-so-bub dz-so-me dz-so-bub-cont dz-so-bub-react">Je peux apporter le réflecteur et deux objectifs.<span class="dz-so-bub-emo">❤️</span></div>
      <div class="dz-so-bub-img dz-so-me"><img src="https://picsum.photos/seed/marche/600/400" alt="Étals de fruits au marché"></div>
      <p class="dz-so-seen"><span>Vu à 10:44</span></p>
      <div class="dz-typing"><i></i><i></i><i></i></div>
    </div>
    <div class="dz-so-dm-compose"><a class="dz-so-ib" href="#" aria-label="Joindre"><i class="fas fa-plus"></i></a><div class="dz-so-field"><span class="dz-so-ph">Votre message…</span><span class="dz-so-field-tools"><i class="far fa-smile"></i></span></div><a class="dz-so-send" href="#" aria-label="Envoyer"><i class="fas fa-paper-plane"></i></a></div>
  </section>
</div>
""",
    ),
    # ------------------------------------------------------------ 18. communauté
    dict(
        name="page de communauté",
        icon="fas fa-users",
        wrap="section",
        html="""
<div class="dz-so-group">
  <div class="dz-so-group-banner"><img src="https://picsum.photos/seed/atelierbois/1600/420" alt="Établi d'atelier de menuiserie"></div>
  <div class="dz-so-group-head">
    <span class="dz-so-group-ico"><i class="fas fa-tools"></i></span>
    <div class="dz-so-group-id">
      <h2 class="dz-so-pname">Les Bricoleurs</h2>
      <p class="dz-so-group-meta"><span><i class="fas fa-globe-europe"></i> Groupe public</span><span><b>3 412</b> membres</span><span class="dz-so-online-now"><span class="dz-so-st dz-so-st-on"></span> <b>128</b> en ligne</span></p>
    </div>
    <div class="dz-so-pactions"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-user-plus"></i> Rejoindre</a><a class="dz-so-ib dz-so-ib-bd" href="#" aria-label="Notifications"><i class="far fa-bell"></i></a></div>
  </div>
  <nav class="dz-so-ptabs"><a class="dz-so-ptab dz-active" href="#">Discussion</a><a class="dz-so-ptab" href="#">Événements</a><a class="dz-so-ptab" href="#">Fichiers</a><a class="dz-so-ptab" href="#">Membres</a><a class="dz-so-ptab" href="#">À propos</a></nav>
  <div class="dz-so-group-body">
    <div class="dz-so-group-col">
      <div class="dz-so-panel">
        <p class="dz-so-panel-title">À propos</p>
        <p class="dz-so-panel-text">Entraide entre bricoleurs amateurs : réparations, astuces, prêt d'outils et repair cafés dans toute la France. Bienveillance obligatoire, conseils gratuits.</p>
        <p class="dz-so-panel-row"><i class="fas fa-history"></i> Créé en mai 2022 · <b>+86 membres</b> cette semaine</p>
      </div>
      <div class="dz-so-panel">
        <p class="dz-so-panel-title">Règles du groupe</p>
        <ol class="dz-so-rules"><li><b>Restez bienveillants</b><span>Aucune question n'est bête.</span></li><li><b>Pas de publicité</b><span>Les annonces vont dans « Petites annonces ».</span></li><li><b>Sécurité d'abord</b><span>Coupez le courant avant toute intervention.</span></li></ol>
      </div>
    </div>
    <div class="dz-so-group-col">
      <div class="dz-so-panel">
        <p class="dz-so-panel-title">Modération</p>
        <div class="dz-so-sugg"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-4">PG</span><div><b>Paul Garnier</b><span>Administrateur</span></div><span class="dz-so-tag dz-so-tag-brand">Admin</span></div>
        <div class="dz-so-sugg"><span class="dz-avatar dz-avatar-sm dz-so-av dz-so-av-3">NB</span><div><b>Nadia Benali</b><span>Modératrice</span></div><span class="dz-so-tag">Modo</span></div>
      </div>
      <div class="dz-so-panel dz-so-panel-accent">
        <p class="dz-so-panel-title"><i class="fas fa-thumbtack"></i> Annonce épinglée</p>
        <p class="dz-so-panel-text">Repair café géant le <b>28 mars à Lyon</b> : on cherche encore 6 bénévoles électriciens !</p>
        <a class="dz-so-textlink" href="#">Je me porte volontaire <i class="fas fa-arrow-right"></i></a>
      </div>
    </div>
  </div>
</div>
""",
    ),
]
