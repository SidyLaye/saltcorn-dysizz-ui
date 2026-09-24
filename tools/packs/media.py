"""Famille Média : vidéo, musique, podcast, galeries, visionneuse, streaming."""
FAMILY = "media"

P = "https://picsum.photos/seed/"


def _wave(n=64, played=26, seed=7):
    """forme d'onde : barres de hauteurs pseudo-aléatoires (générées une fois, écrites en clair)"""
    import math
    out = []
    for i in range(n):
        h = 22 + 70 * abs(math.sin(i * 0.53 + seed) * math.cos(i * 0.21 + seed / 3))
        h = int(max(14, min(100, h)))
        cls = ' class="dz-md-on"' if i < played else ""
        out.append(f'<i{cls} style="--h:{h}%"></i>')
    return "".join(out)


def _eq(n=5, cls="dz-md-eq"):
    return f'<span class="{cls}">' + "<i></i>" * n + "</span>"


BLOCKS = [
    # ------------------------------------------------------------ 1. lecteur vidéo habillé
    dict(
        name="lecteur vidéo",
        icon="fas fa-play-circle",
        wrap="section",
        html=f"""
<div class="dz-md-player">
  <img src="{P}montagne/1600/900" alt="Image de la vidéo : lever de soleil sur un col alpin">
  <div class="dz-md-player-top">
    <div class="dz-md-player-title"><b>Traversée des Écrins — épisode 3</b><span>Studio Altitude · 4K HDR</span></div>
    <div class="dz-md-player-tr"><a class="dz-md-cbtn" href="#" aria-label="Regarder plus tard"><i class="far fa-clock"></i></a><a class="dz-md-cbtn" href="#" aria-label="Partager"><i class="fas fa-share"></i></a></div>
  </div>
  <a class="dz-md-bigplay" href="#" aria-label="Lire la vidéo"><i class="fas fa-play"></i></a>
  <div class="dz-md-player-bottom">
    <div class="dz-md-scrub">
      <span class="dz-md-scrub-buf" style="--v:58%"></span><span class="dz-md-scrub-play" style="--v:34%"></span>
      <span class="dz-md-chap" style="--at:18%"></span><span class="dz-md-chap" style="--at:47%"></span><span class="dz-md-chap" style="--at:76%"></span>
      <span class="dz-md-knob" style="--v:34%"></span>
      <span class="dz-md-preview" style="--v:52%"><img src="{P}col/320/180" alt=""><b>18:42 · Le refuge</b></span>
    </div>
    <div class="dz-md-controls">
      <a class="dz-md-cbtn dz-md-cbtn-lg" href="#" aria-label="Lecture"><i class="fas fa-play"></i></a>
      <a class="dz-md-cbtn" href="#" aria-label="Suivant"><i class="fas fa-step-forward"></i></a>
      <div class="dz-md-vol"><a class="dz-md-cbtn" href="#" aria-label="Volume"><i class="fas fa-volume-up"></i></a><span class="dz-md-vol-bar"><span style="--v:70%"></span></span></div>
      <span class="dz-md-time"><b>12:47</b> / 37:15</span>
      <span class="dz-md-chapname">· Montée vers le col</span>
      <span class="dz-md-grow"></span>
      <span class="dz-md-hd">4K</span>
      <a class="dz-md-cbtn" href="#" aria-label="Sous-titres"><i class="fas fa-closed-captioning"></i></a>
      <a class="dz-md-cbtn" href="#" aria-label="Réglages"><i class="fas fa-cog"></i></a>
      <a class="dz-md-cbtn" href="#" aria-label="Image dans l'image"><i class="fas fa-clone"></i></a>
      <a class="dz-md-cbtn" href="#" aria-label="Plein écran"><i class="fas fa-expand"></i></a>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 2. vidéo HTML5
    dict(
        name="vidéo html5",
        icon="fas fa-film",
        wrap="narrow",
        html=f"""
<figure class="dz-md-vcard">
  <div class="dz-md-vframe"><video controls preload="none" playsinline poster="{P}atelier/1280/720"><source src="/files/serve/presentation.mp4" type="video/mp4"></video></div>
  <figcaption class="dz-md-vcap">
    <div class="dz-md-vcap-main">
      <span class="dz-md-kicker"><i class="fas fa-film"></i> Film de présentation</span>
      <b>Dans les coulisses de l'Atelier Lune</b>
      <span>2 min 48 · sous-titres français et anglais · publié le 12 février 2026</span>
    </div>
    <div class="dz-md-vcap-act"><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-download"></i> Télécharger</a></div>
  </figcaption>
</figure>
""",
    ),
    # ------------------------------------------------------------ 3. page vidéo
    dict(
        name="page vidéo",
        icon="fas fa-tv",
        wrap="section",
        html=f"""
<div class="dz-md-watch">
  <div class="dz-md-watch-main">
    <div class="dz-md-player dz-md-player-sm">
      <img src="{P}cuisine/1600/900" alt="Image de la vidéo : chef en cuisine">
      <a class="dz-md-bigplay" href="#" aria-label="Lire la vidéo"><i class="fas fa-play"></i></a>
      <div class="dz-md-player-bottom">
        <div class="dz-md-scrub"><span class="dz-md-scrub-buf" style="--v:40%"></span><span class="dz-md-scrub-play" style="--v:22%"></span><span class="dz-md-chap" style="--at:12%"></span><span class="dz-md-chap" style="--at:38%"></span><span class="dz-md-chap" style="--at:71%"></span><span class="dz-md-knob" style="--v:22%"></span></div>
        <div class="dz-md-controls"><a class="dz-md-cbtn" href="#" aria-label="Lecture"><i class="fas fa-play"></i></a><span class="dz-md-time"><b>5:31</b> / 24:08</span><span class="dz-md-grow"></span><a class="dz-md-cbtn" href="#" aria-label="Sous-titres"><i class="fas fa-closed-captioning"></i></a><a class="dz-md-cbtn" href="#" aria-label="Plein écran"><i class="fas fa-expand"></i></a></div>
      </div>
    </div>
    <h2 class="dz-md-wtitle">Pâte feuilletée inversée : la méthode pas à pas (sans stress)</h2>
    <div class="dz-md-wbar">
      <div class="dz-md-channel"><span class="dz-avatar dz-md-av">CM</span><div><b>Cuisine de Margaux <i class="fas fa-check-circle dz-md-verif"></i></b><span>412 k abonnés</span></div><a class="dz-btn dz-btn-sm dz-btn-dark" href="#">S'abonner</a></div>
      <div class="dz-md-wactions">
        <div class="dz-md-pill"><a class="dz-md-pill-part dz-md-on" href="#"><i class="fas fa-thumbs-up"></i> 18 k</a><a class="dz-md-pill-part" href="#" aria-label="Je n'aime pas"><i class="far fa-thumbs-down"></i></a></div>
        <a class="dz-md-pill dz-md-pill-part" href="#"><i class="fas fa-share"></i> Partager</a>
        <a class="dz-md-pill dz-md-pill-part" href="#"><i class="fas fa-download"></i> Télécharger</a>
      </div>
    </div>
    <div class="dz-md-desc">
      <p class="dz-md-desc-meta"><b>284 512 vues · il y a 3 jours</b> <a href="#">#pâtisserie</a> <a href="#">#feuilletage</a></p>
      <p class="dz-md-desc-text">On attaque le grand classique : le feuilletage inversé, plus croustillant et plus régulier. Tous les temps de repos sont indiqués, la recette imprimable est en lien.</p>
      <p class="dz-md-chap-title">Chapitres</p>
      <div class="dz-md-chapters">
        <a class="dz-md-ch" href="#"><span class="dz-md-ch-img"><img src="{P}ch1/320/180" alt=""></span><b>Le beurre manié</b><span>0:00</span></a>
        <a class="dz-md-ch dz-active" href="#"><span class="dz-md-ch-img"><img src="{P}ch2/320/180" alt=""></span><b>La détrempe</b><span>2:54</span></a>
        <a class="dz-md-ch" href="#"><span class="dz-md-ch-img"><img src="{P}ch3/320/180" alt=""></span><b>Tours simples et doubles</b><span>9:10</span></a>
        <a class="dz-md-ch" href="#"><span class="dz-md-ch-img"><img src="{P}ch4/320/180" alt=""></span><b>Cuisson et dégustation</b><span>17:08</span></a>
      </div>
    </div>
  </div>
  <aside class="dz-md-upnext">
    <div class="dz-md-upnext-head"><b>À suivre</b><span class="dz-md-autoplay">Lecture auto <span class="dz-md-toggle"></span></span></div>
    <a class="dz-md-sugg" href="#"><span class="dz-md-thumb"><img src="{P}s1/480/270" alt=""><span class="dz-md-dur">14:22</span></span><div><b>Croissants maison : la recette complète en 3 jours</b><span>Cuisine de Margaux</span><span>1,2 M vues · il y a 1 an</span></div></a>
    <a class="dz-md-sugg" href="#"><span class="dz-md-thumb"><img src="{P}s2/480/270" alt=""><span class="dz-md-dur">8:05</span></span><div><b>Réussir sa crème pâtissière à chaque fois</b><span>Le Fournil de Paul</span><span>96 k vues · il y a 2 mois</span></div></a>
    <a class="dz-md-sugg" href="#"><span class="dz-md-thumb"><img src="{P}s3/480/270" alt=""><span class="dz-md-dur">21:40</span><span class="dz-md-thumb-prog" style="--v:62%"></span></span><div><b>Galette des rois : frangipane et dorure parfaite</b><span>Cuisine de Margaux</span><span>530 k vues · il y a 8 mois</span></div></a>
    <a class="dz-md-sugg" href="#"><span class="dz-md-thumb"><img src="{P}s4/480/270" alt=""><span class="dz-md-dur dz-md-dur-live">EN DIRECT</span></span><div><b>Atelier du dimanche : on répond à vos questions</b><span>Cuisine de Margaux</span><span>2 104 spectateurs</span></div></a>
  </aside>
</div>
""",
    ),
    # ------------------------------------------------------------ 4. lecteur audio
    dict(
        name="lecteur audio",
        icon="fas fa-music",
        wrap="section",
        html=f"""
<div class="dz-md-music">
  <div class="dz-md-music-art dz-md-art dz-md-art-2"><span class="dz-md-art-t">Nuits<br>Blanches</span><span class="dz-md-art-s">Élio Varenne</span></div>
  <div class="dz-md-music-main">
    <div class="dz-md-music-head">
      <div><span class="dz-md-kicker">{_eq(4, "dz-md-eq dz-md-eq-sm")} En cours de lecture</span><h3 class="dz-md-music-title">Lumière d'août</h3><p class="dz-md-music-artist"><a href="#">Élio Varenne</a> · Nuits Blanches · 2026</p></div>
      <a class="dz-md-heart dz-md-on" href="#" aria-label="Retirer des favoris"><i class="fas fa-heart"></i></a>
    </div>
    <div class="dz-md-seek"><span class="dz-md-seek-fill" style="--v:41%"></span><span class="dz-md-knob" style="--v:41%"></span></div>
    <p class="dz-md-seek-t"><span>1:38</span><span>-2:21</span></p>
    <div class="dz-md-transport">
      <a class="dz-md-tbtn dz-md-on" href="#" aria-label="Aléatoire"><i class="fas fa-random"></i></a>
      <a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Précédent"><i class="fas fa-step-backward"></i></a>
      <a class="dz-md-play" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a>
      <a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Suivant"><i class="fas fa-step-forward"></i></a>
      <a class="dz-md-tbtn" href="#" aria-label="Répéter"><i class="fas fa-redo"></i></a>
    </div>
    <div class="dz-md-music-foot">
      <a class="dz-md-mini" href="#"><i class="fas fa-list-ul"></i> File d'attente</a>
      <a class="dz-md-mini" href="#"><i class="fas fa-align-left"></i> Paroles</a>
      <div class="dz-md-vol"><i class="fas fa-volume-down"></i><span class="dz-md-vol-bar"><span style="--v:64%"></span></span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 5. liste de lecture
    dict(
        name="liste de lecture",
        icon="fas fa-list-ol",
        wrap="section",
        html=f"""
<div class="dz-md-pl">
  <div class="dz-md-pl-head">
    <div class="dz-md-pl-cover dz-md-art dz-md-art-1"><span class="dz-md-art-t">Focus<br>matinal</span></div>
    <div class="dz-md-pl-info">
      <span class="dz-md-kicker">Playlist publique</span>
      <h2 class="dz-md-pl-title">Focus matinal</h2>
      <p class="dz-md-pl-desc">Piano, électro douce et ambiances pour bien démarrer la journée. Mise à jour chaque lundi.</p>
      <p class="dz-md-pl-meta"><span class="dz-avatar dz-md-av dz-md-av-xs">NX</span><b>Nexora Radio</b><span>· 12 480 j'aime · 42 titres, 2 h 51</span></p>
    </div>
  </div>
  <div class="dz-md-pl-bar">
    <a class="dz-md-play dz-md-play-lg" href="#" aria-label="Lire la playlist"><i class="fas fa-play"></i></a>
    <a class="dz-md-tbtn dz-md-tbtn-md dz-md-on" href="#" aria-label="Aléatoire"><i class="fas fa-random"></i></a>
    <a class="dz-md-heart dz-md-on" href="#" aria-label="Enregistrée"><i class="fas fa-heart"></i></a>
    <a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Télécharger"><i class="fas fa-arrow-circle-down"></i></a>
    <a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Plus"><i class="fas fa-ellipsis-h"></i></a>
    <span class="dz-md-grow"></span>
    <span class="dz-md-sort">Trier : date d'ajout <i class="fas fa-list"></i></span>
  </div>
  <div class="dz-md-tracks">
    <div class="dz-md-tr dz-md-tr-head"><span>#</span><span>Titre</span><span class="dz-md-col-album">Album</span><span class="dz-md-col-date">Ajouté le</span><span class="dz-md-col-dur"><i class="far fa-clock"></i></span></div>
    <div class="dz-md-tr"><span class="dz-md-tn">1</span><div class="dz-md-tt"><span class="dz-md-tt-art dz-md-art dz-md-art-3"></span><div><b>Aube sur Loire</b><span>Clara Vidal</span></div></div><span class="dz-md-col-album">Rives</span><span class="dz-md-col-date">2 mars 2026</span><span class="dz-md-col-dur">3:42</span></div>
    <div class="dz-md-tr dz-md-tr-on"><span class="dz-md-tn">{_eq(4, "dz-md-eq dz-md-eq-sm")}</span><div class="dz-md-tt"><span class="dz-md-tt-art dz-md-art dz-md-art-2"></span><div><b>Lumière d'août</b><span>Élio Varenne</span></div></div><span class="dz-md-col-album">Nuits Blanches</span><span class="dz-md-col-date">2 mars 2026</span><span class="dz-md-col-dur">3:59</span></div>
    <div class="dz-md-tr"><span class="dz-md-tn">3</span><div class="dz-md-tt"><span class="dz-md-tt-art dz-md-art dz-md-art-4"></span><div><b>Papier calque</b><span>Les Ondes Douces <span class="dz-md-e">E</span></span></div></div><span class="dz-md-col-album">Papier calque</span><span class="dz-md-col-date">24 févr. 2026</span><span class="dz-md-col-dur">4:15</span></div>
    <div class="dz-md-tr"><span class="dz-md-tn">4</span><div class="dz-md-tt"><span class="dz-md-tt-art dz-md-art dz-md-art-5"></span><div><b>Respirer lentement</b><span>Maya Solène, Hugo T.</span></div></div><span class="dz-md-col-album">Intérieurs</span><span class="dz-md-col-date">17 févr. 2026</span><span class="dz-md-col-dur">2:58</span></div>
    <div class="dz-md-tr"><span class="dz-md-tn">5</span><div class="dz-md-tt"><span class="dz-md-tt-art dz-md-art dz-md-art-6"></span><div><b>Quai numéro 9</b><span>Clara Vidal</span></div></div><span class="dz-md-col-album">Rives</span><span class="dz-md-col-date">10 févr. 2026</span><span class="dz-md-col-dur">5:07</span></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 6. rangées streaming
    dict(
        name="rangées de vignettes",
        icon="fas fa-th-large",
        wrap="section",
        html=f"""
<div class="dz-md-rows">
  <div class="dz-md-rowblock">
    <div class="dz-md-rowhead"><h3 class="dz-md-rowtitle">Reprendre la lecture</h3><a class="dz-md-rowlink" href="#">Tout voir <i class="fas fa-chevron-right"></i></a></div>
    <div class="dz-md-rail">
      <a class="dz-md-card" href="#"><span class="dz-md-thumb"><img src="{P}r1/640/360" alt=""><span class="dz-md-thumb-prog" style="--v:72%"></span><span class="dz-md-hoverplay"><i class="fas fa-play"></i></span></span><b>Les Veilleurs</b><span>S2 · É4 « Marée basse » · 18 min restantes</span></a>
      <a class="dz-md-card" href="#"><span class="dz-md-thumb"><img src="{P}r2/640/360" alt=""><span class="dz-md-thumb-prog" style="--v:35%"></span><span class="dz-md-hoverplay"><i class="fas fa-play"></i></span></span><b>Brume</b><span>Film · 1 h 04 restante</span></a>
      <a class="dz-md-card" href="#"><span class="dz-md-thumb"><img src="{P}r3/640/360" alt=""><span class="dz-md-thumb-prog" style="--v:90%"></span><span class="dz-md-hoverplay"><i class="fas fa-play"></i></span></span><b>Cuisines du monde</b><span>É7 « Oaxaca » · 4 min restantes</span></a>
      <a class="dz-md-card" href="#"><span class="dz-md-thumb"><img src="{P}r4/640/360" alt=""><span class="dz-md-thumb-prog" style="--v:12%"></span><span class="dz-md-hoverplay"><i class="fas fa-play"></i></span></span><b>Le Dernier Phare</b><span>Documentaire · 52 min restantes</span></a>
      <a class="dz-md-card" href="#"><span class="dz-md-thumb"><img src="{P}r5/640/360" alt=""><span class="dz-md-thumb-prog" style="--v:48%"></span><span class="dz-md-hoverplay"><i class="fas fa-play"></i></span></span><b>Ligne 13</b><span>S1 · É2 · 27 min restantes</span></a>
    </div>
  </div>
  <div class="dz-md-rowblock">
    <div class="dz-md-rowhead"><h3 class="dz-md-rowtitle">Top 10 en France aujourd'hui</h3></div>
    <div class="dz-md-rail dz-md-rail-top">
      <a class="dz-md-top" href="#"><span class="dz-md-topn">1</span><span class="dz-md-poster"><img src="{P}p1/400/600" alt="Affiche"><span class="dz-md-new">Nouvel épisode</span></span></a>
      <a class="dz-md-top" href="#"><span class="dz-md-topn">2</span><span class="dz-md-poster"><img src="{P}p2/400/600" alt="Affiche"></span></a>
      <a class="dz-md-top" href="#"><span class="dz-md-topn">3</span><span class="dz-md-poster"><img src="{P}p3/400/600" alt="Affiche"><span class="dz-md-new">Récemment ajouté</span></span></a>
      <a class="dz-md-top" href="#"><span class="dz-md-topn">4</span><span class="dz-md-poster"><img src="{P}p4/400/600" alt="Affiche"></span></a>
      <a class="dz-md-top" href="#"><span class="dz-md-topn">5</span><span class="dz-md-poster"><img src="{P}p5/400/600" alt="Affiche"></span></a>
      <a class="dz-md-top" href="#"><span class="dz-md-topn">6</span><span class="dz-md-poster"><img src="{P}p6/400/600" alt="Affiche"></span></a>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 7. héro film / série
    dict(
        name="héro film et série",
        icon="fas fa-video",
        wrap="full",
        html=f"""
<div class="dz-md-hero">
  <div class="dz-md-hero-bg"><img src="{P}falaise/1920/1080" alt=""></div>
  <div class="dz-md-hero-in">
    <span class="dz-md-hero-badge"><span class="dz-md-hero-n">N°1</span> Série la plus regardée cette semaine</span>
    <h1 class="dz-md-hero-logo">Les Veilleurs</h1>
    <p class="dz-md-hero-meta"><span class="dz-md-match">98 % pour vous</span><span>2026</span><span class="dz-md-rating">16+</span><span>2 saisons</span><span class="dz-md-hd">HD</span><span class="dz-md-hd">5.1</span></p>
    <p class="dz-md-hero-syn">Sur une île bretonne coupée du monde par la tempête, une garde-côte découvre que les signaux du vieux phare ne s'adressent pas aux bateaux. Qui les envoie, et pour qui ?</p>
    <div class="dz-md-hero-cta">
      <a class="dz-md-hero-play" href="#"><i class="fas fa-play"></i> Lecture</a>
      <a class="dz-md-hero-more" href="#"><i class="fas fa-info-circle"></i> Plus d'infos</a>
      <a class="dz-md-round" href="#" aria-label="Ajouter à ma liste"><i class="fas fa-plus"></i></a>
      <a class="dz-md-round" href="#" aria-label="J'aime"><i class="far fa-thumbs-up"></i></a>
    </div>
    <p class="dz-md-hero-cast"><span>Avec :</span> Anna Keraudren, Malik Benhadj, Solène Arnaud · <span>Genres :</span> Thriller, Mystère</p>
  </div>
  <div class="dz-md-hero-side"><a class="dz-md-round dz-md-round-sm" href="#" aria-label="Couper le son"><i class="fas fa-volume-mute"></i></a><span class="dz-md-rating dz-md-rating-side">16+</span></div>
</div>
""",
    ),
    # ------------------------------------------------------------ 8. épisodes de podcast
    dict(
        name="épisodes de podcast",
        icon="fas fa-podcast",
        wrap="section",
        html="""
<div class="dz-md-pod">
  <aside class="dz-md-pod-show">
    <div class="dz-md-pod-cover dz-md-art dz-md-art-3"><i class="fas fa-microphone-alt"></i><span class="dz-md-art-t">Les Petits<br>Matins</span></div>
    <h2 class="dz-md-pod-name">Les Petits Matins</h2>
    <p class="dz-md-pod-host">Par Léna Morel · Société · Hebdomadaire</p>
    <p class="dz-md-pod-rate"><span class="dz-stars">★★★★★</span><b>4,9</b><span>(3 812 avis)</span></p>
    <div class="dz-md-pod-cta"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> S'abonner</a><a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Partager"><i class="fas fa-share-alt"></i></a><a class="dz-md-tbtn dz-md-tbtn-md" href="#" aria-label="Flux RSS"><i class="fas fa-rss"></i></a></div>
    <p class="dz-md-pod-about">Chaque lundi, une rencontre avec celles et ceux qui changent leur quartier : 40 minutes de conversation, sans détour.</p>
  </aside>
  <div class="dz-md-eps">
    <div class="dz-md-eps-head"><h3 class="dz-md-rowtitle">Épisodes <span class="dz-md-count">148</span></h3><nav class="dz-md-seg"><a class="dz-md-seg-i dz-active" href="#">Tous</a><a class="dz-md-seg-i" href="#">Non écoutés</a><a class="dz-md-seg-i" href="#">Téléchargés</a></nav></div>
    <div class="dz-md-ep dz-md-ep-new">
      <a class="dz-md-ep-play" href="#" aria-label="Écouter"><i class="fas fa-play"></i></a>
      <div class="dz-md-ep-main"><p class="dz-md-ep-date"><span class="dz-md-newtag">Nouveau</span> Lundi 16 mars 2026 · Épisode 148</p><b class="dz-md-ep-title">Nadia, boulangère de nuit : « Le quartier dort, moi je le nourris »</b><p class="dz-md-ep-desc">Trois heures du matin, rue des Tanneurs. Nadia nous ouvre son fournil et raconte vingt ans de nuits blanches.</p></div>
      <div class="dz-md-ep-side"><span class="dz-md-ep-dur">42 min</span><a class="dz-md-tbtn" href="#" aria-label="Télécharger"><i class="fas fa-arrow-circle-down"></i></a></div>
    </div>
    <div class="dz-md-ep dz-md-ep-playing">
      <a class="dz-md-ep-play dz-md-on" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a>
      <div class="dz-md-ep-main"><p class="dz-md-ep-date">Lundi 9 mars 2026 · Épisode 147</p><b class="dz-md-ep-title">Le jardin partagé qui a remplacé un parking</b><p class="dz-md-ep-desc">Comment 60 voisins ont convaincu la mairie, et ce qu'ils récoltent aujourd'hui.</p><div class="dz-md-ep-prog"><span style="--v:38%"></span></div></div>
      <div class="dz-md-ep-side"><span class="dz-md-ep-dur dz-md-ep-left">23 min restantes</span><a class="dz-md-tbtn dz-md-on" href="#" aria-label="Téléchargé"><i class="fas fa-check-circle"></i></a></div>
    </div>
    <div class="dz-md-ep dz-md-ep-done">
      <a class="dz-md-ep-play" href="#" aria-label="Réécouter"><i class="fas fa-redo"></i></a>
      <div class="dz-md-ep-main"><p class="dz-md-ep-date">Lundi 2 mars 2026 · Épisode 146</p><b class="dz-md-ep-title">Réparer plutôt que jeter : une journée au repair café</b><p class="dz-md-ep-desc">Grille-pain, vélos et machines à coudre : rencontre avec les bénévoles de Montreuil.</p></div>
      <div class="dz-md-ep-side"><span class="dz-md-ep-dur"><i class="fas fa-check"></i> Écouté</span><a class="dz-md-tbtn" href="#" aria-label="Télécharger"><i class="fas fa-arrow-circle-down"></i></a></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 9. podcast + transcription
    dict(
        name="podcast avec transcription",
        icon="fas fa-closed-captioning",
        wrap="narrow",
        html=f"""
<div class="dz-md-tx">
  <div class="dz-md-tx-player">
    <div class="dz-md-tx-art dz-md-art dz-md-art-3"><i class="fas fa-microphone-alt"></i></div>
    <div class="dz-md-tx-info"><span class="dz-md-kicker">Les Petits Matins · Épisode 147</span><b>Le jardin partagé qui a remplacé un parking</b></div>
    <div class="dz-md-tx-ctrl">
      <a class="dz-md-tbtn" href="#" aria-label="Reculer de 15 secondes"><i class="fas fa-undo"></i></a>
      <a class="dz-md-play" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a>
      <a class="dz-md-tbtn" href="#" aria-label="Avancer de 30 secondes"><i class="fas fa-redo"></i></a>
      <span class="dz-md-speed">1,25×</span>
    </div>
    <div class="dz-md-wave">{_wave(72, 27)}</div>
    <p class="dz-md-seek-t dz-md-tx-t"><span>16:12</span><span>-26:31</span></p>
  </div>
  <div class="dz-md-tx-head"><b>Transcription</b><span class="dz-md-tx-auto"><i class="fas fa-magic"></i> Générée automatiquement</span><div class="dz-md-tx-search"><i class="fas fa-search"></i><span>Rechercher dans l'épisode</span></div></div>
  <div class="dz-md-tx-body">
    <div class="dz-md-line"><a class="dz-md-ts" href="#">15:40</a><div><b class="dz-md-spk dz-md-spk-1">Léna</b><p>Et concrètement, le premier jour, vous êtes arrivés avec quoi ? Des pelles ?</p></div></div>
    <div class="dz-md-line"><a class="dz-md-ts" href="#">15:47</a><div><b class="dz-md-spk dz-md-spk-2">Joseph</b><p>Des pelles, des palettes et beaucoup d'optimisme. On était onze. Il pleuvait, évidemment.</p></div></div>
    <div class="dz-md-line dz-md-line-on"><a class="dz-md-ts" href="#">16:05</a><div><b class="dz-md-spk dz-md-spk-2">Joseph</b><p>Et puis la gardienne de l'immeuble d'en face est descendue avec du café pour tout le monde. <span class="dz-md-mark">C'est là que j'ai compris que ça allait marcher.</span> Le quartier avait envie de ce lieu.</p></div></div>
    <div class="dz-md-line"><a class="dz-md-ts" href="#">16:31</a><div><b class="dz-md-spk dz-md-spk-1">Léna</b><p>Aujourd'hui, combien de parcelles ?</p></div></div>
    <div class="dz-md-line dz-md-line-future"><a class="dz-md-ts" href="#">16:34</a><div><b class="dz-md-spk dz-md-spk-2">Joseph</b><p>Quarante-deux, plus un verger de douze arbres et une ruche que les enfants de l'école surveillent de très près.</p></div></div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 10. galerie maçonnerie
    dict(
        name="galerie maçonnerie",
        icon="fas fa-th",
        wrap="section",
        html=f"""
<div class="dz-md-gal-head">
  <div><h2 class="dz-md-h">Carnet de route</h2><p class="dz-md-hsub">86 photos · Islande, Écosse et îles Féroé · 2025</p></div>
  <div class="dz-md-filters"><a class="dz-md-filter dz-active" href="#">Tout</a><a class="dz-md-filter" href="#">Paysages</a><a class="dz-md-filter" href="#">Portraits</a><a class="dz-md-filter" href="#">Nuit</a></div>
</div>
<div class="dz-md-masonry">
  <a class="dz-md-mitem dz-md-tall" href="#"><img src="{P}m1/600/900" alt="Cascade dans un canyon"><span class="dz-md-mcap"><b>Skógafoss, 6 h du matin</b><span><i class="fas fa-heart"></i> 842</span></span></a>
  <a class="dz-md-mitem dz-md-wide" href="#"><img src="{P}m2/600/400" alt="Plage de sable noir"><span class="dz-md-mcap"><b>Reynisfjara</b><span><i class="fas fa-heart"></i> 516</span></span></a>
  <a class="dz-md-mitem dz-md-sq" href="#"><img src="{P}m3/600/600" alt="Cheval islandais"><span class="dz-md-mcap"><b>Crinière au vent</b><span><i class="fas fa-heart"></i> 1 204</span></span></a>
  <a class="dz-md-mitem dz-md-wide" href="#"><img src="{P}m4/600/400" alt="Aurores boréales"><span class="dz-md-mcap"><b>Aurores sur Kirkjufell</b><span><i class="fas fa-heart"></i> 2 390</span></span></a>
  <a class="dz-md-mitem dz-md-tall" href="#"><img src="{P}m5/600/900" alt="Phare sur une falaise"><span class="dz-md-mcap"><b>Phare de Neist Point</b><span><i class="fas fa-heart"></i> 688</span></span></a>
  <a class="dz-md-mitem dz-md-sq" href="#"><img src="{P}m6/600/600" alt="Village de pêcheurs"><span class="dz-md-mcap"><b>Gjógv</b><span><i class="fas fa-heart"></i> 431</span></span></a>
  <a class="dz-md-mitem dz-md-wide" href="#"><img src="{P}m7/600/400" alt="Route dans la brume"><span class="dz-md-mcap"><b>Route 1, brume</b><span><i class="fas fa-heart"></i> 377</span></span></a>
  <a class="dz-md-mitem dz-md-tall" href="#"><img src="{P}m8/600/900" alt="Portrait d'un pêcheur"><span class="dz-md-mcap"><b>Einar, pêcheur</b><span><i class="fas fa-heart"></i> 954</span></span></a>
</div>
""",
    ),
    # ------------------------------------------------------------ 11. visionneuse
    dict(
        name="galerie avec visionneuse",
        icon="fas fa-images",
        wrap="section",
        html=f"""
<div class="dz-md-viewer">
  <div class="dz-md-stage">
    <div class="dz-md-stage-img dz-zoomable"><img src="{P}v3/1600/1000" alt="Marché flottant au petit matin"></div>
    <a class="dz-md-nav dz-md-nav-prev" href="#" aria-label="Photo précédente"><i class="fas fa-chevron-left"></i></a>
    <a class="dz-md-nav dz-md-nav-next" href="#" aria-label="Photo suivante"><i class="fas fa-chevron-right"></i></a>
    <span class="dz-md-counter">3 / 12</span>
    <span class="dz-md-zoomhint"><i class="fas fa-search-plus"></i> Cliquer pour agrandir</span>
  </div>
  <aside class="dz-md-vinfo">
    <span class="dz-md-kicker">Série « Mékong »</span>
    <h3 class="dz-md-vtitle">Marché flottant, 5 h 40</h3>
    <p class="dz-md-vtext">Les barques arrivent avant le lever du soleil ; tout se négocie à voix basse, dans la brume du fleuve.</p>
    <div class="dz-md-exif">
      <span><i class="fas fa-camera"></i> Hybride plein format</span>
      <span><i class="fas fa-dot-circle"></i> 35 mm · f/2,0</span>
      <span><i class="fas fa-stopwatch"></i> 1/250 s · ISO 800</span>
      <span><i class="fas fa-map-marker-alt"></i> Cái Răng, Vietnam</span>
    </div>
    <div class="dz-md-vact"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-download"></i> Original</a><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-heart"></i> 318</a></div>
  </aside>
  <div class="dz-md-thumbs">
    <a class="dz-md-tn-i" href="#"><img src="{P}v1/300/200" alt="Miniature 1"></a>
    <a class="dz-md-tn-i" href="#"><img src="{P}v2/300/200" alt="Miniature 2"></a>
    <a class="dz-md-tn-i dz-active" href="#"><img src="{P}v3/300/200" alt="Miniature 3"></a>
    <a class="dz-md-tn-i" href="#"><img src="{P}v4/300/200" alt="Miniature 4"></a>
    <a class="dz-md-tn-i" href="#"><img src="{P}v5/300/200" alt="Miniature 5"></a>
    <a class="dz-md-tn-i" href="#"><img src="{P}v6/300/200" alt="Miniature 6"></a>
    <a class="dz-md-tn-i dz-md-tn-more" href="#"><img src="{P}v7/300/200" alt="Miniature 7"><span>+ 6</span></a>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 12. mur polaroid
    dict(
        name="mur de photos polaroid",
        icon="fas fa-camera-retro",
        wrap="section",
        html=f"""
<div class="dz-md-wall">
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol1/500/500" alt="Pique-nique au bord du lac"></span><figcaption>Lac d'Annecy, juillet ☀️</figcaption></figure>
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol2/500/500" alt="Anniversaire de Lou"></span><figcaption>Les 30 ans de Lou 🎂</figcaption></figure>
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol3/500/500" alt="Randonnée en montagne"></span><figcaption>Le GR20, étape 4</figcaption></figure>
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol4/500/500" alt="Chat endormi au soleil"></span><figcaption>Pistache, en plein travail</figcaption></figure>
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol5/500/500" alt="Concert en plein air"></span><figcaption>Festival des Nuits, 2025</figcaption></figure>
  <figure class="dz-md-pola"><span class="dz-md-pola-img"><img src="{P}pol6/500/500" alt="Crêpes du dimanche"></span><figcaption>Dimanche crêpes 🥞</figcaption></figure>
</div>
""",
    ),
    # ------------------------------------------------------------ 13. médiathèque
    dict(
        name="bibliothèque de médias",
        icon="fas fa-photo-video",
        wrap="section",
        html=f"""
<div class="dz-md-lib">
  <aside class="dz-md-lib-side">
    <a class="dz-btn dz-btn-block dz-btn-sm" href="#"><i class="fas fa-cloud-upload-alt"></i> Importer</a>
    <p class="dz-md-side-label">Bibliothèque</p>
    <a class="dz-md-folder dz-active" href="#"><i class="fas fa-layer-group"></i> Tous les médias<span>1 284</span></a>
    <a class="dz-md-folder" href="#"><i class="far fa-image"></i> Images<span>912</span></a>
    <a class="dz-md-folder" href="#"><i class="fas fa-film"></i> Vidéos<span>148</span></a>
    <a class="dz-md-folder" href="#"><i class="fas fa-music"></i> Audio<span>96</span></a>
    <a class="dz-md-folder" href="#"><i class="far fa-file-pdf"></i> Documents<span>128</span></a>
    <p class="dz-md-side-label">Dossiers</p>
    <a class="dz-md-folder" href="#"><i class="fas fa-folder dz-md-f1"></i> Campagne printemps<span>24</span></a>
    <a class="dz-md-folder" href="#"><i class="fas fa-folder dz-md-f2"></i> Site web 2026<span>61</span></a>
    <a class="dz-md-folder" href="#"><i class="fas fa-folder dz-md-f3"></i> Réseaux sociaux<span>133</span></a>
    <div class="dz-md-storage"><p><b>38,4 Go</b> sur 50 Go</p><div class="dz-md-storage-bar"><span class="dz-md-sb-img" style="--v:48%"></span><span class="dz-md-sb-vid" style="--v:22%"></span><span class="dz-md-sb-aud" style="--v:7%"></span></div><p class="dz-md-storage-leg"><span class="dz-md-lg-img">Images</span><span class="dz-md-lg-vid">Vidéos</span><span class="dz-md-lg-aud">Audio</span></p></div>
  </aside>
  <div class="dz-md-lib-main">
    <div class="dz-md-lib-bar">
      <div class="dz-md-search"><i class="fas fa-search"></i><span>Rechercher un fichier, une étiquette…</span></div>
      <div class="dz-md-filters"><a class="dz-md-filter dz-active" href="#">Récents</a><a class="dz-md-filter" href="#"><i class="fas fa-tag"></i> Étiquettes</a><a class="dz-md-filter" href="#"><i class="fas fa-sort-amount-down"></i> Taille</a></div>
      <div class="dz-md-viewsw"><a class="dz-md-vs dz-active" href="#" aria-label="Grille"><i class="fas fa-th-large"></i></a><a class="dz-md-vs" href="#" aria-label="Liste"><i class="fas fa-list"></i></a></div>
    </div>
    <div class="dz-md-selbar"><span><i class="fas fa-check-square"></i> <b>2 éléments sélectionnés</b> · 14,2 Mo</span><span class="dz-md-selact"><a href="#"><i class="fas fa-download"></i> Télécharger</a><a href="#"><i class="fas fa-folder-open"></i> Déplacer</a><a class="dz-md-danger" href="#"><i class="far fa-trash-alt"></i> Supprimer</a></span></div>
    <div class="dz-md-files">
      <div class="dz-md-file dz-md-sel"><span class="dz-md-file-prev"><img src="{P}f1/400/300" alt=""><span class="dz-md-check"><i class="fas fa-check"></i></span></span><b>visuel-printemps-v3.jpg</b><span>JPG · 2 400 × 1 600 · 3,8 Mo</span></div>
      <div class="dz-md-file dz-md-sel"><span class="dz-md-file-prev"><img src="{P}f2/400/300" alt=""><span class="dz-md-check"><i class="fas fa-check"></i></span><span class="dz-md-ftype"><i class="fas fa-play"></i> 1:12</span></span><b>teaser-lancement.mp4</b><span>MP4 · 1080p · 10,4 Mo</span></div>
      <div class="dz-md-file"><span class="dz-md-file-prev dz-md-file-audio"><span class="dz-md-mwave">{_wave(22, 0, 3)}</span><span class="dz-md-check"></span><span class="dz-md-ftype"><i class="fas fa-music"></i> 3:42</span></span><b>jingle-radio.wav</b><span>WAV · 44,1 kHz · 36 Mo</span></div>
      <div class="dz-md-file"><span class="dz-md-file-prev"><img src="{P}f4/400/300" alt=""><span class="dz-md-check"></span></span><b>equipe-atelier.png</b><span>PNG · 1 920 × 1 280 · 2,1 Mo</span></div>
      <div class="dz-md-file"><span class="dz-md-file-prev dz-md-file-doc"><i class="far fa-file-pdf"></i><span class="dz-md-check"></span></span><b>charte-graphique.pdf</b><span>PDF · 24 pages · 8,7 Mo</span></div>
      <div class="dz-md-file dz-md-file-up"><span class="dz-md-file-prev"><img src="{P}f6/400/300" alt=""><span class="dz-md-upl"><span class="dz-md-upl-ring"></span><b>64 %</b></span></span><b>shooting-produit-12.raw</b><span>Envoi en cours · 28 s restantes</span></div>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 14. stories et reels
    dict(
        name="stories et reels",
        icon="fas fa-mobile-alt",
        wrap="section",
        html=f"""
<div class="dz-md-storyzone">
  <div class="dz-md-story">
    <img src="{P}story/720/1280" alt="Story : terrasse de café au soleil">
    <div class="dz-md-story-top">
      <div class="dz-md-segs"><span class="dz-md-seg-done"></span><span class="dz-md-seg-now"></span><span></span><span></span></div>
      <div class="dz-md-story-who"><span class="dz-md-story-av dz-md-art dz-md-art-1">IM</span><b>ines.moreau</b><span>2 h</span><span class="dz-md-grow"></span><i class="fas fa-pause"></i><i class="fas fa-volume-up"></i><i class="fas fa-ellipsis-h"></i></div>
    </div>
    <span class="dz-md-sticker">☕ Le meilleur flat white de Bordeaux</span>
    <div class="dz-md-story-bottom"><div class="dz-md-reply"><span>Répondre à ines.moreau…</span></div><i class="far fa-heart"></i><i class="far fa-paper-plane"></i></div>
  </div>
  <div class="dz-md-reels">
    <div class="dz-md-rowhead"><h3 class="dz-md-rowtitle"><i class="fas fa-bolt dz-md-ico"></i> Reels populaires</h3><a class="dz-md-rowlink" href="#">Tout voir <i class="fas fa-chevron-right"></i></a></div>
    <div class="dz-md-reelgrid">
      <a class="dz-md-reel" href="#"><img src="{P}reel1/360/640" alt=""><span class="dz-md-reel-views"><i class="fas fa-play"></i> 1,4 M</span><span class="dz-md-reel-cap">Le pli parfait en 10 secondes 🧺</span></a>
      <a class="dz-md-reel" href="#"><img src="{P}reel2/360/640" alt=""><span class="dz-md-reel-views"><i class="fas fa-play"></i> 862 k</span><span class="dz-md-reel-cap">Recette : granola maison</span></a>
      <a class="dz-md-reel" href="#"><img src="{P}reel3/360/640" alt=""><span class="dz-md-reel-views"><i class="fas fa-play"></i> 318 k</span><span class="dz-md-reel-cap">Avant / après du salon ✨</span></a>
      <a class="dz-md-reel" href="#"><img src="{P}reel4/360/640" alt=""><span class="dz-md-reel-views"><i class="fas fa-play"></i> 96 k</span><span class="dz-md-reel-cap">Balade à vélo, Canal du Midi</span></a>
    </div>
  </div>
</div>
""",
    ),
    # ------------------------------------------------------------ 15. direct
    dict(
        name="direct avec discussion",
        icon="fas fa-broadcast-tower",
        wrap="section",
        html=f"""
<div class="dz-md-live">
  <div class="dz-md-live-main">
    <div class="dz-md-player dz-md-player-live">
      <img src="{P}concert/1600/900" alt="Concert en direct sur une scène éclairée">
      <div class="dz-md-player-top"><span class="dz-md-livebadge"><span class="dz-md-livedot"></span> EN DIRECT</span><span class="dz-md-viewers"><i class="fas fa-eye"></i> 12 486</span><span class="dz-md-grow"></span><span class="dz-md-uptime">1:24:07</span></div>
      <div class="dz-md-player-bottom"><div class="dz-md-controls"><a class="dz-md-cbtn" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a><a class="dz-md-cbtn" href="#" aria-label="Volume"><i class="fas fa-volume-up"></i></a><span class="dz-md-golive"><span class="dz-md-livedot"></span> Direct</span><span class="dz-md-grow"></span><span class="dz-md-hd">1080p60</span><a class="dz-md-cbtn" href="#" aria-label="Plein écran"><i class="fas fa-expand"></i></a></div></div>
    </div>
    <div class="dz-md-live-info">
      <span class="dz-avatar dz-md-av dz-md-live-av">OS</span>
      <div class="dz-md-live-txt"><b class="dz-md-live-title">Orchestre de la Saône — Nuit des Musées, concert intégral</b><span>Orchestre de la Saône · Musique classique · <span class="dz-md-tagline">Français</span></span></div>
      <div class="dz-md-live-cta"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-heart"></i> Suivre</a><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-share"></i></a></div>
    </div>
  </div>
  <aside class="dz-md-livechat">
    <div class="dz-md-livechat-head"><b>Discussion en direct</b><span><i class="fas fa-users"></i> 3 204</span></div>
    <div class="dz-md-pinned"><i class="fas fa-thumbtack"></i><span><b>Orchestre de la Saône</b> Programme complet et bis à retrouver dans la description 🎻</span></div>
    <div class="dz-md-livemsgs">
      <p class="dz-md-lm"><b class="dz-md-u1">claire_b</b> Ce solo de violoncelle 😭😭</p>
      <p class="dz-md-lm"><b class="dz-md-u2">Tom.L</b> On entend super bien même au casque</p>
      <p class="dz-md-lm dz-md-lm-don"><span class="dz-md-don">💛 5,00 €</span><b class="dz-md-u3">Mamie Josette</b> Bravo à mon petit-fils au 2e rang des violons !</p>
      <p class="dz-md-lm"><b class="dz-md-u4">hugo_music</b> Quelqu'un a le nom du morceau ?</p>
      <p class="dz-md-lm"><b class="dz-md-u5">Modération</b> <span class="dz-md-modtag">MOD</span> Symphonie n° 7, 2e mouvement 🙂</p>
      <p class="dz-md-lm"><b class="dz-md-u1">Sabrina</b> Salut depuis Montréal 👋</p>
    </div>
    <div class="dz-md-livecompose"><div class="dz-md-search"><span>Envoyer un message…</span><i class="far fa-smile"></i></div><a class="dz-md-send" href="#" aria-label="Envoyer"><i class="fas fa-paper-plane"></i></a></div>
  </aside>
</div>
""",
    ),
    # ------------------------------------------------------------ 16. égaliseur
    dict(
        name="égaliseur animé",
        icon="fas fa-sliders-h",
        wrap="narrow",
        html="""
<div class="dz-md-eqcard">
  <div class="dz-md-eqcard-head">
    <div><span class="dz-md-kicker">Sortie audio · Enceinte du salon</span><h3 class="dz-md-music-title">Égaliseur</h3></div>
    <div class="dz-md-presets"><a class="dz-md-filter" href="#">Plat</a><a class="dz-md-filter dz-active" href="#">Voix</a><a class="dz-md-filter" href="#">Basses +</a><a class="dz-md-filter" href="#">Soirée</a></div>
  </div>
  <div class="dz-md-visu"><i style="--h:96%"></i><i style="--h:100%"></i><i style="--h:92%"></i><i style="--h:74%"></i><i style="--h:49%"></i><i style="--h:21%"></i><i style="--h:35%"></i><i style="--h:59%"></i><i style="--h:76%"></i><i style="--h:84%"></i><i style="--h:82%"></i><i style="--h:71%"></i><i style="--h:53%"></i><i style="--h:31%"></i><i style="--h:20%"></i><i style="--h:41%"></i><i style="--h:57%"></i><i style="--h:67%"></i><i style="--h:68%"></i><i style="--h:63%"></i><i style="--h:51%"></i><i style="--h:35%"></i><i style="--h:18%"></i><i style="--h:26%"></i><i style="--h:40%"></i><i style="--h:50%"></i><i style="--h:53%"></i><i style="--h:51%"></i><i style="--h:44%"></i><i style="--h:34%"></i><i style="--h:22%"></i><i style="--h:18%"></i></div>
  <div class="dz-md-bands">
    <div class="dz-md-band" style="--v:62%"><span class="dz-md-db">+3</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">60 Hz</span></div>
    <div class="dz-md-band" style="--v:55%"><span class="dz-md-db">+1</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">150 Hz</span></div>
    <div class="dz-md-band" style="--v:44%"><span class="dz-md-db">−1</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">400 Hz</span></div>
    <div class="dz-md-band" style="--v:70%"><span class="dz-md-db">+5</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">1 kHz</span></div>
    <div class="dz-md-band" style="--v:76%"><span class="dz-md-db">+6</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">2,4 kHz</span></div>
    <div class="dz-md-band" style="--v:58%"><span class="dz-md-db">+2</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">6 kHz</span></div>
    <div class="dz-md-band" style="--v:40%"><span class="dz-md-db">−2</span><span class="dz-md-track"><span class="dz-md-thumbk"></span></span><span class="dz-md-hz">15 kHz</span></div>
  </div>
  <div class="dz-md-eqcard-foot"><span><i class="fas fa-headphones"></i> Amélioration des dialogues activée</span><a class="dz-md-rowlink" href="#">Réinitialiser</a></div>
</div>
""",
    ),
    # ------------------------------------------------------------ 17. albums
    dict(
        name="albums",
        icon="fas fa-compact-disc",
        wrap="section",
        html="""
<div class="dz-md-rowhead dz-md-rowhead-lg"><div><h2 class="dz-md-h">Nouveautés de la semaine</h2><p class="dz-md-hsub">Sorties du vendredi 13 mars 2026</p></div><a class="dz-md-rowlink" href="#">Tout voir <i class="fas fa-chevron-right"></i></a></div>
<div class="dz-md-albums">
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-2"><span class="dz-md-art-t">Nuits<br>Blanches</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span></span><b>Nuits Blanches</b><span>Élio Varenne · 2026</span></a>
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-1"><span class="dz-md-art-t">Rives</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span></span><b>Rives</b><span>Clara Vidal · 2026</span></a>
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-3"><span class="dz-md-art-t">SOLEIL<br>NOIR</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span><span class="dz-md-e dz-md-e-cover">E</span></span><b>Soleil noir</b><span>Kaïs &amp; les Nomades · EP</span></a>
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-4"><span class="dz-md-art-t">Papier<br>calque</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span></span><b>Papier calque</b><span>Les Ondes Douces · 2026</span></a>
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-5"><span class="dz-md-art-t">Intérieurs</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span></span><b>Intérieurs</b><span>Maya Solène · 2026</span></a>
  <a class="dz-md-album" href="#"><span class="dz-md-cover dz-md-art dz-md-art-6"><span class="dz-md-art-t">Quai 9</span><span class="dz-md-cover-play"><i class="fas fa-play"></i></span></span><b>Quai 9 (live)</b><span>Clara Vidal · Live</span></a>
</div>
""",
    ),
    # ------------------------------------------------------------ 18. avant / après
    dict(
        name="avant après",
        icon="fas fa-columns",
        wrap="section",
        html=f"""
<div class="dz-md-ba">
  <div class="dz-md-ba-head">
    <div><span class="dz-md-kicker">Restauration photo</span><h2 class="dz-md-h">Faites glisser pour comparer</h2></div>
    <div class="dz-md-filters"><a class="dz-md-filter dz-active" href="#">Colorisation</a><a class="dz-md-filter" href="#">Netteté</a><a class="dz-md-filter" href="#">Rayures</a></div>
  </div>
  <div class="dz-md-ba-frame">
    <div class="dz-compare dz-md-compare"><img class="dz-cover dz-md-before" src="{P}ancien/1600/900" alt="Photo d'origine, jaunie et abîmée"><img class="dz-cover dz-md-after" src="{P}ancien/1600/900" alt="Photo restaurée et colorisée"></div>
    <span class="dz-md-ba-label dz-md-ba-l">Avant · 1962</span>
    <span class="dz-md-ba-label dz-md-ba-r">Après</span>
  </div>
  <p class="dz-md-ba-foot"><span><i class="fas fa-magic"></i> Traitement en 14 s</span><span><i class="fas fa-expand"></i> 4 800 × 2 700 px</span><span><i class="fas fa-shield-alt"></i> Traitée sur nos serveurs en France</span></p>
</div>
""",
    ),
    # ------------------------------------------------------------ 19. mini-lecteur
    dict(
        name="mini lecteur",
        icon="fas fa-headphones",
        wrap="section",
        html=f"""
<div class="dz-md-dock">
  <div class="dz-md-dock-now">
    <span class="dz-md-dock-art dz-md-art dz-md-art-2"></span>
    <div class="dz-md-dock-txt"><b>Lumière d'août</b><span>Élio Varenne</span></div>
    <a class="dz-md-heart dz-md-on" href="#" aria-label="Favori"><i class="fas fa-heart"></i></a>
  </div>
  <div class="dz-md-dock-center">
    <div class="dz-md-transport dz-md-transport-sm">
      <a class="dz-md-tbtn dz-md-on" href="#" aria-label="Aléatoire"><i class="fas fa-random"></i></a>
      <a class="dz-md-tbtn" href="#" aria-label="Précédent"><i class="fas fa-step-backward"></i></a>
      <a class="dz-md-play dz-md-play-sm" href="#" aria-label="Pause"><i class="fas fa-pause"></i></a>
      <a class="dz-md-tbtn" href="#" aria-label="Suivant"><i class="fas fa-step-forward"></i></a>
      <a class="dz-md-tbtn" href="#" aria-label="Répéter"><i class="fas fa-redo"></i></a>
    </div>
    <div class="dz-md-dock-seek"><span>1:38</span><div class="dz-md-seek"><span class="dz-md-seek-fill" style="--v:41%"></span><span class="dz-md-knob" style="--v:41%"></span></div><span>3:59</span></div>
  </div>
  <div class="dz-md-dock-right">
    <a class="dz-md-tbtn" href="#" aria-label="Paroles"><i class="fas fa-microphone-alt"></i></a>
    <a class="dz-md-tbtn" href="#" aria-label="File d'attente"><i class="fas fa-list-ul"></i></a>
    <a class="dz-md-tbtn dz-md-on" href="#" aria-label="Appareil : enceinte du salon"><i class="fas fa-broadcast-tower"></i></a>
    <div class="dz-md-vol"><i class="fas fa-volume-up"></i><span class="dz-md-vol-bar"><span style="--v:64%"></span></span></div>
  </div>
  <span class="dz-md-dock-device"><i class="fas fa-broadcast-tower"></i> Lecture sur Enceinte du salon</span>
</div>
""",
    ),
]
