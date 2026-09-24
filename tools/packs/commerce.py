"""Famille « Commerce » : boutique en ligne et back-office marchand.
Préfixe CSS : dz-cm-  (styles/33-commerce.css)"""

FAMILY = "commerce"


def img(seed, w=600, h=750, alt=""):
    return f'<img src="https://picsum.photos/seed/{seed}/{w}/{h}" alt="{alt}">'


def product(seed, cat, name, rate, count, price, old=None, flags=(), swatches=(), more=0, fav=False):
    fl = "".join(f'<span class="dz-cm-flag{" dz-cm-flag-sale" if f.startswith("−") else " dz-cm-flag-dark" if f == "Dernières pièces" else ""}">{f}</span>' for f in flags)
    sw = "".join(f'<span class="dz-cm-sw{" dz-on" if i == 0 else ""}" style="--c:{c}"></span>' for i, c in enumerate(swatches))
    if more:
        sw += f'<span class="dz-cm-sw-more">+{more}</span>'
    old_html = f"<s>{old}</s>" if old else ""
    return f"""
  <article class="dz-cm-product">
    <div class="dz-cm-media">
      {img(seed, alt=name)}
      <div class="dz-cm-flags">{fl}</div>
      <a class="dz-cm-fav{" dz-on" if fav else ""}" href="#" aria-label="Ajouter aux favoris"><i class="{"fas" if fav else "far"} fa-heart"></i></a>
      <a class="dz-cm-quick" href="#"><i class="fas fa-plus"></i> Ajout rapide</a>
    </div>
    <div class="dz-cm-pbody">
      <div class="dz-cm-pmeta"><span>{cat}</span><span class="dz-cm-rate"><i class="fas fa-star"></i> {rate} <small>({count})</small></span></div>
      <h3 class="dz-cm-pname">{name}</h3>
      <div class="dz-cm-swatches">{sw}</div>
      <div class="dz-cm-price{" dz-cm-price-promo" if old else ""}"><b>{price}</b>{old_html}</div>
    </div>
  </article>"""


GRID = f"""
<div class="dz-cm-shop">
  <div class="dz-cm-shop-head">
    <div>
      <span class="dz-eyebrow">Collection automne 2026</span>
      <h2 class="dz-h2">Nouveautés de la saison</h2>
      <p class="dz-cm-muted">248 articles · livraison offerte dès 60 €</p>
    </div>
    <div class="dz-cm-sort"><span class="dz-cm-sort-label">Trier par</span><a class="dz-cm-select" href="#">Pertinence <i class="fas fa-chevron-down"></i></a></div>
  </div>
  <div class="dz-cm-filterbar dz-chips">
    <a class="dz-chip dz-active" href="#">Tout</a>
    <a class="dz-chip" href="#">Maroquinerie</a>
    <a class="dz-chip" href="#">Prêt-à-porter</a>
    <a class="dz-chip" href="#">Maison</a>
    <a class="dz-chip" href="#">Accessoires</a>
    <a class="dz-chip" href="#"><i class="fas fa-tag"></i> Promotions</a>
  </div>
  <div class="dz-cm-products">
    {product("cm-cabas", "Maroquinerie", "Cabas Oléa cuir grainé", "4,8", "126", "139 €", "199 €", ("−30 %",), ("#8b5a3c", "#1f1f1f", "#c9b79c"), 2, True)}
    {product("cm-pull", "Prêt-à-porter", "Pull col rond mérinos", "4,6", "342", "89 €", None, ("Nouveau",), ("#d9cbb4", "#34435e", "#7a2e2e"), 4)}
    {product("cm-lampe", "Maison", "Lampe à poser Halo", "4,9", "58", "164 €", None, ("Dernières pièces",), ("#e7e1d6", "#2b2b2b"))}
    {product("cm-montre", "Accessoires", "Montre Aube 38 mm", "4,7", "211", "179 €", "229 €", ("−22 %", "Nouveau"), ("#b8b8b8", "#c7a261", "#1f1f1f"))}
  </div>
  <div class="dz-cm-shop-foot"><span class="dz-cm-muted">Vous avez vu 4 articles sur 248</span><div class="dz-progress" style="--v:2%"><span></span></div><a class="dz-btn dz-btn-ghost" href="#">Voir plus d'articles</a></div>
</div>
"""

PDP = f"""
<div class="dz-cm-pdp">
  <div class="dz-cm-gallery">
    <div class="dz-cm-gallery-main">
      {img("cm-pdp-1", 900, 1100, "Veste Iroise en laine bouillie, vue de face")}
      <span class="dz-cm-flag dz-cm-flag-sale dz-cm-gallery-flag">−25 %</span>
      <a class="dz-cm-zoom" href="#" aria-label="Agrandir l'image"><i class="fas fa-expand"></i></a>
    </div>
    <div class="dz-cm-thumbs">
      <a class="dz-cm-thumb dz-on" href="#">{img("cm-pdp-1", 200, 240, "Vue de face")}</a>
      <a class="dz-cm-thumb" href="#">{img("cm-pdp-2", 200, 240, "Vue de dos")}</a>
      <a class="dz-cm-thumb" href="#">{img("cm-pdp-3", 200, 240, "Détail de la matière")}</a>
      <a class="dz-cm-thumb dz-cm-thumb-more" href="#"><span>+4</span></a>
    </div>
  </div>
  <div class="dz-cm-pdp-info">
    <nav class="dz-cm-crumbs"><a href="#">Femme</a><span>/</span><a href="#">Manteaux &amp; vestes</a><span>/</span><span>Veste Iroise</span></nav>
    <div class="dz-cm-pdp-title">
      <h2 class="dz-h3">Veste Iroise en laine bouillie</h2>
      <a class="dz-cm-fav dz-cm-fav-inline" href="#" aria-label="Ajouter aux favoris"><i class="far fa-heart"></i></a>
    </div>
    <div class="dz-cm-pdp-rating"><span class="dz-cm-stars" style="--r:94%"></span><b>4,7</b><a href="#">218 avis</a><span class="dz-cm-sep"></span><span class="dz-cm-instock"><i class="fas fa-circle"></i> En stock, expédiée sous 24 h</span></div>
    <div class="dz-cm-price dz-cm-price-lg"><b>186 €</b><s>248 €</s><span class="dz-badge dz-badge-danger">Vous économisez 62 €</span></div>
    <p class="dz-cm-muted">Ou 3 × 62 € sans frais · TVA incluse</p>

    <div class="dz-cm-opt">
      <div class="dz-cm-opt-head"><b>Couleur</b><span>Bleu nuit</span></div>
      <div class="dz-cm-colors">
        <a class="dz-cm-color dz-on" href="#" style="--c:#243049" aria-label="Bleu nuit"></a>
        <a class="dz-cm-color" href="#" style="--c:#b9a584" aria-label="Sable"></a>
        <a class="dz-cm-color" href="#" style="--c:#6b2a2a" aria-label="Bordeaux"></a>
        <a class="dz-cm-color" href="#" style="--c:#3e4a38" aria-label="Kaki"></a>
      </div>
    </div>
    <div class="dz-cm-opt">
      <div class="dz-cm-opt-head"><b>Taille</b><a href="#"><i class="fas fa-ruler-horizontal"></i> Guide des tailles</a></div>
      <div class="dz-cm-sizes">
        <a class="dz-cm-size dz-off" href="#">XS</a>
        <a class="dz-cm-size" href="#">S</a>
        <a class="dz-cm-size dz-on" href="#">M</a>
        <a class="dz-cm-size" href="#">L</a>
        <a class="dz-cm-size dz-low" href="#">XL</a>
      </div>
      <p class="dz-cm-hint"><i class="fas fa-bolt"></i> Plus que 2 pièces en XL</p>
    </div>
    <div class="dz-cm-buy">
      <div class="dz-cm-qty"><a href="#" aria-label="Diminuer"><i class="fas fa-minus"></i></a><span>1</span><a href="#" aria-label="Augmenter"><i class="fas fa-plus"></i></a></div>
      <a class="dz-btn dz-btn-lg dz-cm-buy-btn" href="#"><i class="fas fa-shopping-bag"></i> Ajouter au panier</a>
    </div>
    <div class="dz-cm-perks">
      <div class="dz-cm-perk"><i class="fas fa-truck"></i><div><b>Livraison offerte</b><span>Reçue entre le 29 sept. et le 1er oct.</span></div></div>
      <div class="dz-cm-perk"><i class="fas fa-undo"></i><div><b>Retours gratuits sous 30 jours</b><span>En point relais ou en boutique</span></div></div>
      <div class="dz-cm-perk"><i class="fas fa-leaf"></i><div><b>Laine recyclée à 70 %</b><span>Tissée au Portugal, confectionnée en France</span></div></div>
    </div>
    <div class="dz-cm-acc">
      <details><summary>Description</summary><div>Coupe droite légèrement oversize, col tailleur et deux poches plaquées. La laine bouillie, dense et souple, garde sa tenue saison après saison sans jamais gratter.</div></details>
      <details><summary>Composition &amp; entretien</summary><div>70 % laine recyclée, 30 % polyamide. Doublure 100 % viscose. Nettoyage à sec ou lavage à la main à 30 °C.</div></details>
      <details><summary>Avis clients <span class="dz-badge dz-badge-neutral">218</span></summary><div>« Chaude sans être lourde, la coupe est parfaite. Je prends habituellement du M et c'est juste. » — <b>Inès, Nantes</b></div></details>
    </div>
  </div>
</div>
"""


def cart_line(seed, name, variant, price, qty, old=None):
    return f"""
    <div class="dz-cm-line">
      <div class="dz-cm-line-img">{img(seed, 160, 200, name)}</div>
      <div class="dz-cm-line-body">
        <div class="dz-cm-line-top"><b>{name}</b><span class="dz-cm-line-price">{price}{f"<s>{old}</s>" if old else ""}</span></div>
        <span class="dz-cm-line-var">{variant}</span>
        <div class="dz-cm-line-actions">
          <div class="dz-cm-qty dz-cm-qty-sm"><a href="#" aria-label="Diminuer"><i class="fas fa-minus"></i></a><span>{qty}</span><a href="#" aria-label="Augmenter"><i class="fas fa-plus"></i></a></div>
          <a class="dz-cm-link-mute" href="#">Retirer</a>
        </div>
      </div>
    </div>"""


CART_LINES = (cart_line("cm-pdp-1", "Veste Iroise", "Bleu nuit · M", "186 €", 1, "248 €")
              + cart_line("cm-pull", "Pull mérinos", "Écru · S", "178 €", 2)
              + cart_line("cm-lampe", "Lampe Halo", "Lin · Taille unique", "164 €", 1))

DRAWER = f"""
<div class="dz-cm-storebar">
  <a class="dz-cm-logo" href="#"><span class="dz-cm-logo-mark">M</span>Maison Oriel</a>
  <nav class="dz-cm-storenav"><a href="#">Femme</a><a href="#">Homme</a><a href="#">Maison</a><a class="dz-cm-storenav-sale" href="#">Soldes</a></nav>
  <div class="dz-cm-storeicons">
    <a class="dz-cm-iconbtn" href="#" aria-label="Rechercher"><i class="fas fa-search"></i></a>
    <a class="dz-cm-iconbtn" href="#" aria-label="Favoris"><i class="far fa-heart"></i></a>
    <a class="dz-cm-cartbtn dz-open-dz-cm-cart" href="#"><i class="fas fa-shopping-bag"></i><span>Panier</span><b>4</b></a>
  </div>
</div>
<div class="dz-drawer dz-cm-drawer" id="dz-cm-cart">
  <div class="dz-cm-drawer-head">
    <h3 class="dz-h4">Votre panier <span class="dz-cm-count">4</span></h3>
    <a class="dz-cm-iconbtn dz-close" href="#" aria-label="Fermer"><i class="fas fa-times"></i></a>
  </div>
  <div class="dz-cm-ship">
    <p><i class="fas fa-truck"></i> Livraison offerte <b>débloquée</b> !</p>
    <div class="dz-cm-ship-bar"><span style="width:100%"></span></div>
  </div>
  <div class="dz-cm-drawer-lines">{CART_LINES}</div>
  <div class="dz-cm-upsell">
    <span class="dz-cm-upsell-title">Souvent achetés ensemble</span>
    <div class="dz-cm-upsell-item"><div class="dz-cm-line-img dz-cm-line-img-sm">{img("cm-bonnet", 120, 120, "Bonnet côtelé")}</div><div><b>Bonnet côtelé</b><span>39 €</span></div><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Ajouter</a></div>
  </div>
  <div class="dz-cm-drawer-foot">
    <div class="dz-cm-row"><span>Sous-total</span><b>528 €</b></div>
    <p class="dz-cm-muted">Taxes incluses. Frais de port calculés à l'étape suivante.</p>
    <a class="dz-btn dz-btn-lg dz-btn-block" href="#"><i class="fas fa-lock"></i> Commander · 528 €</a>
    <a class="dz-cm-link-mute dz-cm-center" href="#">Continuer mes achats</a>
  </div>
</div>
"""

SUMMARY_ROWS = """
    <div class="dz-cm-row"><span>Sous-total (4 articles)</span><span>590 €</span></div>
    <div class="dz-cm-row dz-cm-row-good"><span><i class="fas fa-tag"></i> AUTOMNE15</span><span>−62 €</span></div>
    <div class="dz-cm-row"><span>Livraison standard</span><span class="dz-cm-free">Offerte</span></div>
    <div class="dz-cm-row dz-cm-row-mute"><span>Dont TVA (20 %)</span><span>88 €</span></div>
    <div class="dz-cm-row dz-cm-total"><span>Total</span><b>528 €</b></div>"""

CART_PAGE = f"""
<div class="dz-cm-cartpage">
  <div class="dz-cm-cartpage-main">
    <div class="dz-cm-cartpage-head"><h2 class="dz-h3">Mon panier</h2><span class="dz-cm-muted">4 articles</span></div>
    <div class="dz-cm-shipbanner"><div class="dz-cm-ship"><p><i class="fas fa-truck"></i> Plus que <b>12 €</b> pour la livraison express offerte</p><div class="dz-cm-ship-bar"><span style="width:82%"></span></div></div></div>
    <div class="dz-cm-cartlist">
      <div class="dz-cm-cartrow">
        <div class="dz-cm-line-img dz-cm-line-img-lg">{img("cm-pdp-1", 240, 300, "Veste Iroise")}</div>
        <div class="dz-cm-cartrow-info"><b>Veste Iroise en laine bouillie</b><span>Bleu nuit · Taille M</span><span class="dz-cm-instock"><i class="fas fa-circle"></i> En stock</span><div class="dz-cm-cartrow-links"><a href="#"><i class="far fa-heart"></i> Mettre de côté</a><a href="#"><i class="far fa-trash-alt"></i> Supprimer</a></div></div>
        <div class="dz-cm-qty"><a href="#" aria-label="Diminuer"><i class="fas fa-minus"></i></a><span>1</span><a href="#" aria-label="Augmenter"><i class="fas fa-plus"></i></a></div>
        <div class="dz-cm-cartrow-price"><b>186 €</b><s>248 €</s></div>
      </div>
      <div class="dz-cm-cartrow">
        <div class="dz-cm-line-img dz-cm-line-img-lg">{img("cm-pull", 240, 300, "Pull mérinos")}</div>
        <div class="dz-cm-cartrow-info"><b>Pull col rond mérinos</b><span>Écru · Taille S</span><span class="dz-cm-instock"><i class="fas fa-circle"></i> En stock</span><div class="dz-cm-cartrow-links"><a href="#"><i class="far fa-heart"></i> Mettre de côté</a><a href="#"><i class="far fa-trash-alt"></i> Supprimer</a></div></div>
        <div class="dz-cm-qty"><a href="#" aria-label="Diminuer"><i class="fas fa-minus"></i></a><span>2</span><a href="#" aria-label="Augmenter"><i class="fas fa-plus"></i></a></div>
        <div class="dz-cm-cartrow-price"><b>178 €</b><span class="dz-cm-muted">89 € l'unité</span></div>
      </div>
      <div class="dz-cm-cartrow">
        <div class="dz-cm-line-img dz-cm-line-img-lg">{img("cm-lampe", 240, 300, "Lampe Halo")}</div>
        <div class="dz-cm-cartrow-info"><b>Lampe à poser Halo</b><span>Lin · Taille unique</span><span class="dz-cm-lowstock"><i class="fas fa-circle"></i> Plus que 3 en stock</span><div class="dz-cm-cartrow-links"><a href="#"><i class="far fa-heart"></i> Mettre de côté</a><a href="#"><i class="far fa-trash-alt"></i> Supprimer</a></div></div>
        <div class="dz-cm-qty"><a href="#" aria-label="Diminuer"><i class="fas fa-minus"></i></a><span>1</span><a href="#" aria-label="Augmenter"><i class="fas fa-plus"></i></a></div>
        <div class="dz-cm-cartrow-price"><b>164 €</b></div>
      </div>
    </div>
    <a class="dz-cm-back" href="#"><i class="fas fa-arrow-left"></i> Continuer mes achats</a>
  </div>
  <aside class="dz-cm-summary">
    <h3 class="dz-h4">Récapitulatif</h3>
    <div class="dz-cm-promo"><i class="fas fa-tag"></i><span>AUTOMNE15</span><span class="dz-badge dz-badge-success">Appliqué</span><a href="#" aria-label="Retirer le code"><i class="fas fa-times"></i></a></div>
    <div class="dz-cm-rows">{SUMMARY_ROWS}</div>
    <a class="dz-btn dz-btn-lg dz-btn-block" href="#"><i class="fas fa-lock"></i> Passer commande</a>
    <div class="dz-cm-pay"><span>CB</span><span>VISA</span><span>MC</span><span>AMEX</span><span>Virement</span></div>
    <p class="dz-cm-secure"><i class="fas fa-shield-alt"></i> Paiement chiffré et sécurisé</p>
  </aside>
</div>
"""

CHECKOUT = """
<div class="dz-cm-checkout">
  <div class="dz-cm-checkout-main">
    <ol class="dz-cm-steps">
      <li class="dz-done"><span>Panier</span></li>
      <li class="dz-done"><span>Livraison</span></li>
      <li class="dz-current"><span>Paiement</span></li>
      <li><span>Confirmation</span></li>
    </ol>
    <section class="dz-cm-block">
      <div class="dz-cm-block-head"><span class="dz-cm-block-n dz-cm-block-ok"><i class="fas fa-check"></i></span><h3 class="dz-cm-block-title">Adresse de livraison</h3><a href="#">Modifier</a></div>
      <div class="dz-cm-block-done"><b>Camille Rouvière</b><span>14 rue des Tanneurs, 69002 Lyon · 06 12 34 56 78</span></div>
    </section>
    <section class="dz-cm-block">
      <div class="dz-cm-block-head"><span class="dz-cm-block-n dz-cm-block-ok"><i class="fas fa-check"></i></span><h3 class="dz-cm-block-title">Mode de livraison</h3><a href="#">Modifier</a></div>
      <div class="dz-cm-options">
        <a class="dz-cm-option dz-on" href="#"><span class="dz-cm-radio"></span><div><b>Standard à domicile</b><span>Mardi 29 septembre</span></div><em>Offerte</em></a>
        <a class="dz-cm-option" href="#"><span class="dz-cm-radio"></span><div><b>Express</b><span>Demain avant 13 h</span></div><em>9,90 €</em></a>
        <a class="dz-cm-option" href="#"><span class="dz-cm-radio"></span><div><b>Point relais</b><span>Tabac du Rhône · 350 m</span></div><em>Offerte</em></a>
      </div>
    </section>
    <section class="dz-cm-block dz-cm-block-active">
      <div class="dz-cm-block-head"><span class="dz-cm-block-n">3</span><h3 class="dz-cm-block-title">Paiement</h3><span class="dz-cm-lock"><i class="fas fa-lock"></i> Sécurisé</span></div>
      <div class="dz-cm-paytabs">
        <a class="dz-cm-paytab dz-on" href="#"><i class="far fa-credit-card"></i> Carte</a>
        <a class="dz-cm-paytab" href="#"><i class="fas fa-mobile-alt"></i> Mobile</a>
        <a class="dz-cm-paytab" href="#"><i class="fas fa-university"></i> Virement</a>
        <a class="dz-cm-paytab" href="#"><i class="fas fa-layer-group"></i> 3 × sans frais</a>
      </div>
      <div class="dz-cm-fields">
        <div class="dz-cm-field dz-cm-field-full"><label>Numéro de carte</label><div class="dz-cm-input dz-cm-input-focus"><span>4970 1012 3456 7890</span><i class="fab fa-cc-visa"></i></div></div>
        <div class="dz-cm-field"><label>Expiration</label><div class="dz-cm-input"><span>09 / 28</span></div></div>
        <div class="dz-cm-field"><label>Cryptogramme</label><div class="dz-cm-input"><span>•••</span><i class="far fa-question-circle"></i></div></div>
        <div class="dz-cm-field dz-cm-field-full"><label>Titulaire</label><div class="dz-cm-input"><span>Camille Rouvière</span></div></div>
      </div>
      <a class="dz-cm-check dz-on" href="#"><span class="dz-cm-box"><i class="fas fa-check"></i></span>Adresse de facturation identique à la livraison</a>
      <a class="dz-btn dz-btn-lg dz-btn-block" href="#"><i class="fas fa-lock"></i> Payer 528,00 €</a>
      <p class="dz-cm-legal">En validant, vous acceptez nos conditions générales de vente. Vos données de carte ne sont jamais stockées.</p>
    </section>
  </div>
  <aside class="dz-cm-summary dz-cm-summary-soft">
    <div class="dz-cm-summary-head"><h3 class="dz-h4">Votre commande</h3><a href="#">Modifier</a></div>
    <div class="dz-cm-mini">
      <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-pdp-1/120/150" alt="Veste Iroise"><b>1</b></div><div><b>Veste Iroise</b><span>Bleu nuit · M</span></div><span>186 €</span></div>
      <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-pull/120/150" alt="Pull mérinos"><b>2</b></div><div><b>Pull mérinos</b><span>Écru · S</span></div><span>178 €</span></div>
      <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-lampe/120/150" alt="Lampe Halo"><b>1</b></div><div><b>Lampe Halo</b><span>Lin</span></div><span>164 €</span></div>
    </div>
    <div class="dz-cm-rows">""" + SUMMARY_ROWS + """</div>
  </aside>
</div>
"""

ORDER_SUMMARY = """
<div class="dz-cm-osum">
  <div class="dz-cm-osum-head">
    <div><span class="dz-cm-kicker">Commande n° OR-24817</span><h3 class="dz-h4">Résumé de commande</h3></div>
    <span class="dz-badge dz-badge-success"><i class="fas fa-check"></i> Payée</span>
  </div>
  <div class="dz-cm-mini">
    <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-pdp-1/120/150" alt="Veste Iroise"><b>1</b></div><div><b>Veste Iroise en laine bouillie</b><span>Bleu nuit · M · réf. IRO-M-BN</span></div><span>186 €</span></div>
    <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-pull/120/150" alt="Pull mérinos"><b>2</b></div><div><b>Pull col rond mérinos</b><span>Écru · S · réf. MER-S-EC</span></div><span>178 €</span></div>
    <div class="dz-cm-mini-item"><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-lampe/120/150" alt="Lampe Halo"><b>1</b></div><div><b>Lampe à poser Halo</b><span>Lin · réf. HAL-LIN</span></div><span>164 €</span></div>
  </div>
  <div class="dz-cm-rows">""" + SUMMARY_ROWS + """</div>
  <div class="dz-cm-osum-foot">
    <div><span class="dz-cm-kicker">Livraison</span><b>Camille Rouvière</b><span>14 rue des Tanneurs, 69002 Lyon</span></div>
    <div><span class="dz-cm-kicker">Paiement</span><b><i class="far fa-credit-card"></i> Carte •••• 7890</b><span>Débitée le 24 sept. 2026</span></div>
  </div>
</div>
"""

CONFIRM = """
<div class="dz-cm-confirm">
  <div class="dz-cm-confirm-hero">
    <div class="dz-cm-confirm-check"><i class="fas fa-check"></i></div>
    <span class="dz-cm-kicker">Commande n° OR-24817</span>
    <h2 class="dz-h2">Merci Camille, c'est commandé !</h2>
    <p class="dz-lead">Un e-mail de confirmation vient de partir vers <b>camille.r@exemple.fr</b>. Nous vous écrirons dès que votre colis quittera l'atelier.</p>
  </div>
  <div class="dz-cm-confirm-steps">
    <div class="dz-cm-cstep dz-done"><i class="fas fa-receipt"></i><b>Commande reçue</b><span>Aujourd'hui, 14:32</span></div>
    <div class="dz-cm-cstep"><i class="fas fa-box"></i><b>Préparation</b><span>Sous 24 h</span></div>
    <div class="dz-cm-cstep"><i class="fas fa-truck"></i><b>Expédition</b><span>Vendredi 25 sept.</span></div>
    <div class="dz-cm-cstep"><i class="fas fa-home"></i><b>Livraison</b><span>Mardi 29 sept.</span></div>
  </div>
  <div class="dz-cm-confirm-grid">
    <div class="dz-cm-confirm-card"><i class="fas fa-map-marker-alt"></i><div><span class="dz-cm-kicker">Livré à</span><b>14 rue des Tanneurs</b><span>69002 Lyon</span></div></div>
    <div class="dz-cm-confirm-card"><i class="far fa-credit-card"></i><div><span class="dz-cm-kicker">Payé</span><b>528,00 €</b><span>Carte •••• 7890</span></div></div>
    <div class="dz-cm-confirm-card"><i class="fas fa-gift"></i><div><span class="dz-cm-kicker">Fidélité</span><b>+ 528 points</b><span>Soit 5 € sur votre prochaine commande</span></div></div>
  </div>
  <div class="dz-cm-confirm-actions"><a class="dz-btn" href="#"><i class="fas fa-map-marked-alt"></i> Suivre ma commande</a><a class="dz-btn dz-btn-ghost" href="#">Continuer mes achats</a></div>
</div>
"""

TRACKING = """
<div class="dz-cm-track">
  <div class="dz-cm-track-head">
    <div>
      <span class="dz-cm-kicker">Colis 1 sur 1 · Commande OR-24817</span>
      <h3 class="dz-h3">Arrive <em>demain</em>, entre 9 h et 13 h</h3>
      <p class="dz-cm-muted">Transporteur : Rapido Colis · Suivi <span class="dz-mono">RC 7719 0482 36FR</span></p>
    </div>
    <div class="dz-cm-track-eta"><span>Livraison prévue</span><b>29</b><em>sept. 2026</em></div>
  </div>
  <div class="dz-cm-track-bar">
    <div class="dz-cm-tstep dz-done"><span class="dz-cm-tdot"><i class="fas fa-check"></i></span><b>Commandée</b><small>24 sept.</small></div>
    <div class="dz-cm-tstep dz-done"><span class="dz-cm-tdot"><i class="fas fa-check"></i></span><b>Expédiée</b><small>25 sept.</small></div>
    <div class="dz-cm-tstep dz-current"><span class="dz-cm-tdot"><i class="fas fa-truck"></i></span><b>En transit</b><small>Aujourd'hui</small></div>
    <div class="dz-cm-tstep"><span class="dz-cm-tdot"><i class="fas fa-home"></i></span><b>Livrée</b><small>29 sept.</small></div>
  </div>
  <div class="dz-cm-track-body">
    <div class="dz-cm-events">
      <div class="dz-cm-event dz-now"><time>28 sept. · 06:12</time><b>En cours d'acheminement</b><span>Plateforme de Corbas (69)</span></div>
      <div class="dz-cm-event"><time>27 sept. · 21:40</time><b>Arrivé au centre de tri</b><span>Saint-Priest (69)</span></div>
      <div class="dz-cm-event"><time>25 sept. · 17:05</time><b>Pris en charge par le transporteur</b><span>Atelier Maison Oriel, Roubaix (59)</span></div>
      <div class="dz-cm-event"><time>24 sept. · 14:32</time><b>Commande confirmée</b><span>Paiement accepté</span></div>
    </div>
    <div class="dz-cm-track-side">
      <div class="dz-cm-track-parcel">
        <div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-pdp-1/120/150" alt="Veste Iroise"></div>
        <div><b>3 articles</b><span>Veste Iroise, Pull mérinos ×2, Lampe Halo</span></div>
      </div>
      <a class="dz-btn dz-btn-ghost dz-btn-block" href="#"><i class="fas fa-calendar-alt"></i> Changer le créneau</a>
      <a class="dz-btn dz-btn-ghost dz-btn-block" href="#"><i class="fas fa-map-pin"></i> Livrer en point relais</a>
      <a class="dz-cm-link-mute" href="#"><i class="far fa-question-circle"></i> Un problème avec ce colis ?</a>
    </div>
  </div>
</div>
"""


def order_row(num, date, seeds, count, total, status, cls, action):
    thumbs = "".join(f'<span class="dz-cm-stackimg">{img(s, 80, 100, "")}</span>' for s in seeds)
    return f"""
    <div class="dz-cm-order">
      <div class="dz-cm-order-thumbs">{thumbs}</div>
      <div class="dz-cm-order-info"><b>{num}</b><span>{date} · {count}</span></div>
      <span class="dz-cm-status dz-cm-status-{cls}">{status}</span>
      <b class="dz-cm-order-total">{total}</b>
      <a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">{action}</a>
    </div>"""


HISTORY = f"""
<div class="dz-cm-history">
  <div class="dz-cm-history-head">
    <div><h3 class="dz-h3">Mes commandes</h3><p class="dz-cm-muted">12 commandes depuis mars 2024 · 2 184 € au total</p></div>
    <div class="dz-chips"><a class="dz-chip dz-active" href="#">Toutes</a><a class="dz-chip" href="#">En cours <b class="dz-cm-chipcount">2</b></a><a class="dz-chip" href="#">Livrées</a><a class="dz-chip" href="#">Retours</a></div>
  </div>
  <div class="dz-cm-orders">
    {order_row("OR-24817", "24 sept. 2026", ["cm-pdp-1", "cm-pull", "cm-lampe"], "4 articles", "528,00 €", "En transit", "info", "Suivre")}
    {order_row("OR-23902", "11 sept. 2026", ["cm-montre"], "1 article", "179,00 €", "En préparation", "warn", "Détails")}
    {order_row("OR-21177", "2 août 2026", ["cm-cabas", "cm-bonnet"], "2 articles", "178,00 €", "Livrée", "ok", "Racheter")}
    {order_row("OR-19540", "18 juin 2026", ["cm-sandale"], "1 article", "95,00 €", "Remboursée", "mute", "Facture")}
  </div>
</div>
"""


def review(initials, name, city, date, stars, title, text, helpful, tag=None, photos=0):
    ph = ""
    if photos:
        ph = '<div class="dz-cm-review-photos">' + "".join(f'<span class="dz-cm-stackimg">{img(f"cm-rev{initials}{i}", 160, 160, "Photo client")}</span>' for i in range(photos)) + "</div>"
    t = f'<span class="dz-cm-review-tag">{tag}</span>' if tag else ""
    return f"""
    <article class="dz-cm-review">
      <div class="dz-cm-review-head"><span class="dz-avatar dz-avatar-sm">{initials}</span><div><b>{name}</b><span>{city} · {date}</span></div><span class="dz-cm-verified"><i class="fas fa-check-circle"></i> Achat vérifié</span></div>
      <div class="dz-cm-review-stars"><span class="dz-cm-stars" style="--r:{stars * 20}%"></span>{t}</div>
      <h4 class="dz-cm-review-title">{title}</h4>
      <p class="dz-cm-review-text">{text}</p>
      {ph}
      <div class="dz-cm-review-foot"><span>Utile ?</span><a href="#"><i class="far fa-thumbs-up"></i> {helpful}</a><a href="#"><i class="far fa-thumbs-down"></i></a></div>
    </article>"""


def dist(n, pct, count):
    return f'<div class="dz-cm-dist-row"><span>{n} <i class="fas fa-star"></i></span><div class="dz-cm-dist-bar"><span style="width:{pct}%"></span></div><small>{count}</small></div>'


REVIEWS = f"""
<div class="dz-cm-reviews">
  <aside class="dz-cm-reviews-score">
    <span class="dz-cm-kicker">Avis clients</span>
    <div class="dz-cm-bigscore"><b>4,7</b><span>/ 5</span></div>
    <span class="dz-cm-stars dz-cm-stars-lg" style="--r:94%"></span>
    <p class="dz-cm-muted">Basé sur 218 avis vérifiés</p>
    <div class="dz-cm-dist">
      {dist(5, 78, 170)}{dist(4, 15, 33)}{dist(3, 4, 9)}{dist(2, 2, 4)}{dist(1, 1, 2)}
    </div>
    <div class="dz-cm-fit"><span class="dz-cm-kicker">Taille</span><div class="dz-cm-fit-bar"><span style="left:46%"></span></div><div class="dz-cm-fit-legend"><small>Petit</small><small>Juste</small><small>Grand</small></div></div>
    <a class="dz-btn dz-btn-block" href="#"><i class="fas fa-pen"></i> Écrire un avis</a>
  </aside>
  <div class="dz-cm-reviews-list">
    <div class="dz-cm-reviews-filters dz-chips"><a class="dz-chip dz-active" href="#">Les plus utiles</a><a class="dz-chip" href="#"><i class="fas fa-camera"></i> Avec photos (24)</a><a class="dz-chip" href="#">5 étoiles</a><a class="dz-chip" href="#">Récents</a></div>
    {review("IM", "Inès M.", "Nantes", "12 sept. 2026", 5, "Chaude sans être lourde", "La coupe est parfaite, la matière ne gratte absolument pas. Je prends habituellement du M et c'est juste ce qu'il faut avec un pull dessous.", 42, "Taille M · Bleu nuit", 3)}
    {review("TB", "Thomas B.", "Lille", "3 sept. 2026", 4, "Belle finition, manches un peu longues", "Très belle veste, les coutures sont nettes et la couleur fidèle aux photos. Les manches tombent un peu bas pour moi (1,74 m).", 17, "Taille L · Kaki")}
  </div>
</div>
"""


def coupon(value, unit, title, cond, code, exp, cls=""):
    return f"""
    <div class="dz-cm-coupon {cls}">
      <div class="dz-cm-coupon-val"><b>{value}</b>{f"<span>{unit}</span>" if unit else ""}</div>
      <div class="dz-cm-coupon-body">
        <b>{title}</b>
        <span>{cond}</span>
        <div class="dz-cm-coupon-code"><span class="dz-mono">{code}</span><a class="dz-cm-copy dz-copy" href="#"><i class="far fa-copy"></i> Copier</a></div>
        <small><i class="far fa-clock"></i> {exp}</small>
      </div>
    </div>"""


COUPONS = f"""
<div class="dz-cm-coupons-wrap">
  <div class="dz-cm-sechead"><div><span class="dz-eyebrow">Vos avantages</span><h2 class="dz-h3">Codes promo disponibles</h2></div><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-plus"></i> Ajouter un code</a></div>
  <div class="dz-cm-coupons">
    {coupon("−15", "%", "Offre d'automne", "Sur toute la collection, dès 80 € d'achat", "AUTOMNE15", "Expire dans 6 jours", "dz-cm-coupon-hot")}
    {coupon("10", "€", "Bienvenue", "Sur votre première commande, sans minimum", "BIENVENUE10", "Valable jusqu'au 31 déc. 2026")}
    {coupon('<i class="fas fa-shipping-fast"></i>', "", "Livraison express offerte", "Membres Cercle Oriel uniquement", "EXPRESSCERCLE", "Valable jusqu'au 15 oct. 2026", "dz-cm-coupon-ship")}
  </div>
</div>
"""

CATEGORIES = f"""
<div class="dz-cm-cats-wrap">
  <div class="dz-cm-sechead"><div><span class="dz-eyebrow">Explorer</span><h2 class="dz-h2">Acheter par univers</h2></div><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Toutes les catégories <i class="fas fa-arrow-right"></i></a></div>
  <div class="dz-cm-cats">
    <a class="dz-cm-cat dz-cm-cat-xl" href="#">{img("cm-cat-femme", 900, 1000, "Femme")}<div class="dz-cm-cat-txt"><span>412 articles</span><b>Femme</b><em>Découvrir <i class="fas fa-arrow-right"></i></em></div></a>
    <a class="dz-cm-cat" href="#">{img("cm-cat-homme", 700, 500, "Homme")}<div class="dz-cm-cat-txt"><span>286 articles</span><b>Homme</b><em>Découvrir <i class="fas fa-arrow-right"></i></em></div></a>
    <a class="dz-cm-cat" href="#">{img("cm-cat-maison", 700, 500, "Maison")}<div class="dz-cm-cat-txt"><span>159 articles</span><b>Maison</b><em>Découvrir <i class="fas fa-arrow-right"></i></em></div></a>
    <a class="dz-cm-cat" href="#">{img("cm-cat-access", 700, 500, "Accessoires")}<div class="dz-cm-cat-txt"><span>97 articles</span><b>Accessoires</b><em>Découvrir <i class="fas fa-arrow-right"></i></em></div></a>
    <a class="dz-cm-cat" href="#">{img("cm-cat-beaute", 700, 500, "Beauté")}<div class="dz-cm-cat-txt"><span>64 articles</span><b>Beauté</b><em>Découvrir <i class="fas fa-arrow-right"></i></em></div></a>
  </div>
</div>
"""

SALE = """
<div class="dz-cm-sale">
  <div class="dz-cm-sale-glow"></div>
  <div class="dz-cm-sale-copy">
    <span class="dz-cm-sale-pill"><span class="dz-dot"></span> Ventes privées · en ce moment</span>
    <h2 class="dz-cm-sale-title">Jusqu'à <b>−50 %</b> sur la collection d'été</h2>
    <p>Plus de 600 pièces à prix doux, dans la limite des stocks disponibles. Livraison offerte pendant toute la durée de l'opération.</p>
    <div class="dz-cm-sale-cta"><a class="dz-btn dz-btn-lg dz-btn-light" href="#">J'en profite <i class="fas fa-arrow-right"></i></a><span class="dz-cm-sale-code">Code <b class="dz-mono">ETE50</b></span></div>
  </div>
  <div class="dz-cm-sale-timer">
    <span class="dz-cm-sale-label"><i class="far fa-clock"></i> Fin de l'opération dans</span>
    <span class="dz-countdown dz-cm-cd">2026-10-05 23:59</span>
    <div class="dz-cm-sale-stock"><div class="dz-cm-sale-stockbar"><span style="width:68%"></span></div><small>68 % des articles déjà partis</small></div>
  </div>
</div>
"""


def wish(seed, name, variant, price, old, note, cls, action):
    return f"""
    <div class="dz-cm-wish">
      <div class="dz-cm-wish-img">{img(seed, 300, 360, name)}<a class="dz-cm-fav dz-on" href="#" aria-label="Retirer des favoris"><i class="fas fa-heart"></i></a></div>
      <div class="dz-cm-wish-body">
        <b>{name}</b><span class="dz-cm-line-var">{variant}</span>
        <div class="dz-cm-price"><b>{price}</b>{f"<s>{old}</s>" if old else ""}</div>
        <span class="dz-cm-wish-note dz-cm-wish-note-{cls}">{note}</span>
        <a class="dz-btn dz-btn-sm {"dz-btn-ghost" if cls == "out" else ""} dz-btn-block" href="#">{action}</a>
      </div>
    </div>"""


WISHLIST = f"""
<div class="dz-cm-wishlist">
  <div class="dz-cm-sechead"><div><h2 class="dz-h3">Ma liste d'envies <span class="dz-cm-count">4</span></h2><p class="dz-cm-muted">Nous vous prévenons dès qu'un prix baisse ou qu'une taille revient.</p></div><div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-share-alt"></i> Partager</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-shopping-bag"></i> Tout ajouter</a></div></div>
  <div class="dz-cm-wishgrid">
    {wish("cm-cabas", "Cabas Oléa", "Cognac", "139 €", "199 €", '<i class="fas fa-arrow-down"></i> Prix en baisse de 60 €', "drop", "Ajouter au panier")}
    {wish("cm-montre", "Montre Aube 38 mm", "Acier", "179 €", None, '<i class="fas fa-bolt"></i> Plus que 2 en stock', "low", "Ajouter au panier")}
    {wish("cm-sandale", "Mules Calanque", "Noir · 39", "95 €", None, '<i class="far fa-bell"></i> Rupture · alerte activée', "out", "Me prévenir")}
    {wish("cm-lampe", "Lampe Halo", "Lin", "164 €", None, '<i class="fas fa-check"></i> En stock', "ok", "Ajouter au panier")}
  </div>
</div>
"""


def cmp_col(seed, name, price, badge, rows, best=False):
    r = "".join(f'<div class="dz-cm-cmp-cell">{c}</div>' for c in rows)
    return f"""
    <div class="dz-cm-cmp-col{" dz-cm-cmp-best" if best else ""}">
      <div class="dz-cm-cmp-card">
        {f'<span class="dz-cm-cmp-badge">{badge}</span>' if badge else ""}
        <div class="dz-cm-cmp-img">{img(seed, 300, 300, name)}</div>
        <b>{name}</b>
        <span class="dz-cm-cmp-price">{price}</span>
        <a class="dz-btn dz-btn-sm dz-btn-block {"" if best else "dz-btn-ghost"}" href="#">Ajouter</a>
      </div>
      {r}
    </div>"""


YES = '<i class="fas fa-check-circle dz-cm-yes"></i>'
NO = '<i class="fas fa-minus-circle dz-cm-no"></i>'

COMPARE = f"""
<div class="dz-cm-compare-wrap">
  <div class="dz-cm-sechead"><div><span class="dz-eyebrow">Comparateur</span><h2 class="dz-h3">Casques sans fil : lequel choisir ?</h2></div><a class="dz-cm-check dz-on" href="#"><span class="dz-cm-box"><i class="fas fa-check"></i></span>Surligner les différences</a></div>
  <div class="dz-cm-compare">
    <div class="dz-cm-cmp-col dz-cm-cmp-labels">
      <div class="dz-cm-cmp-card dz-cm-cmp-card-empty"><span class="dz-cm-muted">3 produits comparés</span><a class="dz-cm-link-mute" href="#"><i class="fas fa-plus"></i> Ajouter un produit</a></div>
      <div class="dz-cm-cmp-cell">Note clients</div>
      <div class="dz-cm-cmp-cell">Autonomie</div>
      <div class="dz-cm-cmp-cell">Réduction de bruit</div>
      <div class="dz-cm-cmp-cell">Poids</div>
      <div class="dz-cm-cmp-cell">Charge rapide</div>
      <div class="dz-cm-cmp-cell">Garantie</div>
    </div>
    {cmp_col("cm-casque1", "Sonar Lite", "89 €", None, ['<span class="dz-cm-rate"><i class="fas fa-star"></i> 4,2</span>', "22 h", NO, "210 g", NO, "1 an"])}
    {cmp_col("cm-casque2", "Sonar Pro", "219 €", "Meilleur choix", ['<span class="dz-cm-rate"><i class="fas fa-star"></i> 4,8</span>', "<b>40 h</b>", YES, "<b>248 g</b>", YES, "<b>3 ans</b>"], True)}
    {cmp_col("cm-casque3", "Sonar Studio", "349 €", None, ['<span class="dz-cm-rate"><i class="fas fa-star"></i> 4,6</span>', "30 h", YES, "312 g", YES, "2 ans"])}
  </div>
</div>
"""


def spark(points, cls=""):
    return f'<svg class="dz-cm-spark {cls}" viewBox="0 0 100 32" preserveAspectRatio="none"><polyline points="{points}"/></svg>'


MERCHANT = f"""
<div class="dz-cm-dash">
  <div class="dz-cm-dash-head">
    <div><span class="dz-cm-kicker">Boutique Maison Oriel</span><h2 class="dz-h3">Bonjour Hugo, voici vos ventes</h2></div>
    <div class="dz-cm-seg"><a href="#">Aujourd'hui</a><a class="dz-on" href="#">7 jours</a><a href="#">30 jours</a><a href="#">12 mois</a></div>
  </div>
  <div class="dz-cm-kpis">
    <div class="dz-cm-kpi"><span class="dz-cm-kpi-label"><i class="fas fa-euro-sign"></i> Chiffre d'affaires</span><b class="dz-counter">48 250 €</b><div class="dz-cm-kpi-foot"><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 12,4 %</span>{spark("0,26 12,22 24,24 36,16 48,18 60,10 72,12 84,6 100,4")}</div></div>
    <div class="dz-cm-kpi"><span class="dz-cm-kpi-label"><i class="fas fa-shopping-bag"></i> Commandes</span><b class="dz-counter">412</b><div class="dz-cm-kpi-foot"><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 8,1 %</span>{spark("0,20 12,24 24,18 36,20 48,14 60,16 72,10 84,12 100,8")}</div></div>
    <div class="dz-cm-kpi"><span class="dz-cm-kpi-label"><i class="fas fa-receipt"></i> Panier moyen</span><b class="dz-counter">117,10 €</b><div class="dz-cm-kpi-foot"><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 3,9 %</span>{spark("0,18 12,16 24,20 36,14 48,16 60,12 72,14 84,10 100,10")}</div></div>
    <div class="dz-cm-kpi"><span class="dz-cm-kpi-label"><i class="fas fa-percentage"></i> Conversion</span><b class="dz-counter">2,84 %</b><div class="dz-cm-kpi-foot"><span class="dz-trend dz-trend-down"><i class="fas fa-arrow-down"></i> 0,3 pt</span>{spark("0,8 12,10 24,8 36,14 48,12 60,18 72,16 84,20 100,22", "dz-cm-spark-down")}</div></div>
  </div>
  <div class="dz-cm-dash-grid">
    <div class="dz-cm-panel">
      <div class="dz-cm-panel-head"><b>Ventes par jour</b><div class="dz-cm-legend"><span><i class="dz-cm-lg-a"></i>Cette semaine</span><span><i class="dz-cm-lg-b"></i>Semaine dernière</span></div></div>
      <div class="dz-cm-bars">
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:52%"></span><span class="dz-cm-bar-a" style="height:60%"></span></div><small>Lun</small></div>
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:48%"></span><span class="dz-cm-bar-a" style="height:55%"></span></div><small>Mar</small></div>
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:60%"></span><span class="dz-cm-bar-a" style="height:72%"></span></div><small>Mer</small></div>
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:55%"></span><span class="dz-cm-bar-a" style="height:64%"></span></div><small>Jeu</small></div>
        <div class="dz-cm-bar dz-cm-bar-peak"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:70%"></span><span class="dz-cm-bar-a" style="height:94%"><em>9 870 €</em></span></div><small>Ven</small></div>
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:78%"></span><span class="dz-cm-bar-a" style="height:86%"></span></div><small>Sam</small></div>
        <div class="dz-cm-bar"><div class="dz-cm-bar-pair"><span class="dz-cm-bar-b" style="height:40%"></span><span class="dz-cm-bar-a" style="height:46%"></span></div><small>Dim</small></div>
      </div>
    </div>
    <div class="dz-cm-panel">
      <div class="dz-cm-panel-head"><b>Meilleures ventes</b><a class="dz-cm-link-mute" href="#">Tout voir</a></div>
      <div class="dz-cm-top">
        <div class="dz-cm-top-row"><span class="dz-cm-top-n">1</span><div class="dz-cm-line-img dz-cm-line-img-xs">{img("cm-pdp-1", 80, 80, "")}</div><div><b>Veste Iroise</b><span>64 ventes</span></div><b>11 904 €</b></div>
        <div class="dz-cm-top-row"><span class="dz-cm-top-n">2</span><div class="dz-cm-line-img dz-cm-line-img-xs">{img("cm-pull", 80, 80, "")}</div><div><b>Pull mérinos</b><span>98 ventes</span></div><b>8 722 €</b></div>
        <div class="dz-cm-top-row"><span class="dz-cm-top-n">3</span><div class="dz-cm-line-img dz-cm-line-img-xs">{img("cm-cabas", 80, 80, "")}</div><div><b>Cabas Oléa</b><span>41 ventes</span></div><b>5 699 €</b></div>
        <div class="dz-cm-top-row"><span class="dz-cm-top-n">4</span><div class="dz-cm-line-img dz-cm-line-img-xs">{img("cm-montre", 80, 80, "")}</div><div><b>Montre Aube</b><span>27 ventes</span></div><b>4 833 €</b></div>
      </div>
    </div>
  </div>
  <div class="dz-cm-panel">
    <div class="dz-cm-panel-head"><b>Dernières commandes</b><span class="dz-badge"><span class="dz-dot"></span> En direct</span></div>
    <div class="dz-cm-feed">
      <div class="dz-cm-feed-row"><span class="dz-avatar dz-avatar-sm">CR</span><div><b>Camille Rouvière</b><span>OR-24817 · 4 articles · Lyon</span></div><span class="dz-cm-status dz-cm-status-ok">Payée</span><b>528,00 €</b><time>il y a 2 min</time></div>
      <div class="dz-cm-feed-row"><span class="dz-avatar dz-avatar-sm">NA</span><div><b>Nicolas Arnaud</b><span>OR-24816 · 1 article · Bordeaux</span></div><span class="dz-cm-status dz-cm-status-warn">À expédier</span><b>89,00 €</b><time>il y a 18 min</time></div>
      <div class="dz-cm-feed-row"><span class="dz-avatar dz-avatar-sm">LP</span><div><b>Léa Pommier</b><span>OR-24815 · 2 articles · Rennes</span></div><span class="dz-cm-status dz-cm-status-ok">Payée</span><b>318,00 €</b><time>il y a 41 min</time></div>
    </div>
  </div>
</div>
"""


def stock_row(seed, name, sku, cat, qty, pct, level, status, price):
    return f"""
    <div class="dz-cm-srow">
      <div class="dz-cm-scell dz-cm-sprod"><div class="dz-cm-line-img dz-cm-line-img-xs">{img(seed, 80, 80, "")}</div><div><b>{name}</b><span class="dz-mono">{sku}</span></div></div>
      <div class="dz-cm-scell dz-cm-scat">{cat}</div>
      <div class="dz-cm-scell dz-cm-sqty"><div class="dz-cm-level dz-cm-level-{level}"><span style="width:{pct}%"></span></div><b>{qty}</b></div>
      <div class="dz-cm-scell"><span class="dz-cm-status dz-cm-status-{ {"ok": "ok", "low": "warn", "out": "bad"}[level]}">{status}</span></div>
      <div class="dz-cm-scell dz-cm-sprice">{price}</div>
      <div class="dz-cm-scell dz-cm-sact"><a class="dz-cm-iconbtn" href="#" aria-label="Réapprovisionner"><i class="fas fa-redo"></i></a><a class="dz-cm-iconbtn" href="#" aria-label="Plus d'actions"><i class="fas fa-ellipsis-h"></i></a></div>
    </div>"""


STOCK = f"""
<div class="dz-cm-stock">
  <div class="dz-cm-stock-head">
    <div><h3 class="dz-h3">Inventaire</h3><p class="dz-cm-muted">1 284 références · valeur du stock 212 480 €</p></div>
    <div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-file-export"></i> Exporter</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouveau produit</a></div>
  </div>
  <div class="dz-cm-stock-stats">
    <div><span class="dz-cm-dotc dz-cm-dot-ok"></span><b>1 176</b><small>En stock</small></div>
    <div><span class="dz-cm-dotc dz-cm-dot-warn"></span><b>86</b><small>Stock faible</small></div>
    <div><span class="dz-cm-dotc dz-cm-dot-bad"></span><b>22</b><small>En rupture</small></div>
    <div><span class="dz-cm-dotc dz-cm-dot-info"></span><b>14</b><small>Commandes fournisseur</small></div>
  </div>
  <div class="dz-cm-stock-tools">
    <div class="dz-cm-searchbox"><i class="fas fa-search"></i><span>Rechercher un produit, une référence…</span><span class="dz-kbd">/</span></div>
    <div class="dz-chips"><a class="dz-chip dz-active" href="#">Tous</a><a class="dz-chip" href="#">Stock faible</a><a class="dz-chip" href="#">Rupture</a></div>
  </div>
  <div class="dz-cm-stable-wrap">
    <div class="dz-cm-stable">
      <div class="dz-cm-srow dz-cm-shead"><div class="dz-cm-scell">Produit</div><div class="dz-cm-scell">Catégorie</div><div class="dz-cm-scell">Stock</div><div class="dz-cm-scell">Statut</div><div class="dz-cm-scell">Prix</div><div class="dz-cm-scell"></div></div>
      {stock_row("cm-pdp-1", "Veste Iroise · M", "IRO-M-BN", "Manteaux", "148", 74, "ok", "En stock", "248,00 €")}
      {stock_row("cm-pull", "Pull mérinos · S", "MER-S-EC", "Mailles", "12", 14, "low", "Stock faible", "89,00 €")}
      {stock_row("cm-lampe", "Lampe Halo", "HAL-LIN", "Luminaires", "3", 6, "low", "Stock faible", "164,00 €")}
      {stock_row("cm-sandale", "Mules Calanque · 39", "CAL-39-NR", "Chaussures", "0", 0, "out", "Rupture", "95,00 €")}
      {stock_row("cm-montre", "Montre Aube 38 mm", "AUB-38-AC", "Montres", "64", 58, "ok", "En stock", "229,00 €")}
    </div>
  </div>
</div>
"""

INVOICE = """
<div class="dz-cm-invoice">
  <div class="dz-cm-invoice-top">
    <div class="dz-cm-invoice-brand"><span class="dz-cm-logo-mark">M</span><div><b>Maison Oriel SAS</b><span>18 quai de Wault, 59100 Roubaix</span><span>SIRET 912 345 678 00021 · TVA FR42 912345678</span></div></div>
    <div class="dz-cm-invoice-id"><span class="dz-cm-kicker">Facture</span><b class="dz-mono">FA-2026-04817</b><span class="dz-badge dz-badge-success"><i class="fas fa-check"></i> Acquittée</span></div>
  </div>
  <div class="dz-cm-invoice-meta">
    <div><span class="dz-cm-kicker">Facturé à</span><b>Camille Rouvière</b><span>14 rue des Tanneurs</span><span>69002 Lyon, France</span></div>
    <div><span class="dz-cm-kicker">Date d'émission</span><b>24 septembre 2026</b><span class="dz-cm-kicker dz-cm-mt">Commande</span><b>OR-24817</b></div>
    <div><span class="dz-cm-kicker">Paiement</span><b>Carte •••• 7890</b><span>Réglé le 24/09/2026</span></div>
  </div>
  <div class="dz-cm-invoice-lines">
    <div class="dz-cm-iline dz-cm-iline-head"><span>Désignation</span><span>Qté</span><span>PU HT</span><span>Total HT</span></div>
    <div class="dz-cm-iline"><span><b>Veste Iroise en laine bouillie</b><small>Bleu nuit · M · IRO-M-BN</small></span><span>1</span><span>155,00 €</span><span>155,00 €</span></div>
    <div class="dz-cm-iline"><span><b>Pull col rond mérinos</b><small>Écru · S · MER-S-EC</small></span><span>2</span><span>74,17 €</span><span>148,33 €</span></div>
    <div class="dz-cm-iline"><span><b>Lampe à poser Halo</b><small>Lin · HAL-LIN</small></span><span>1</span><span>136,67 €</span><span>136,67 €</span></div>
    <div class="dz-cm-iline"><span><b>Remise AUTOMNE15</b><small>Code promotionnel</small></span><span>1</span><span>−51,67 €</span><span>−51,67 €</span></div>
  </div>
  <div class="dz-cm-invoice-bottom">
    <div class="dz-cm-invoice-note"><span class="dz-cm-kicker">Mentions</span><p>Livraison offerte. Retours acceptés sous 30 jours. En cas de retard de paiement, indemnité forfaitaire de 40 € pour frais de recouvrement.</p></div>
    <div class="dz-cm-invoice-totals">
      <div class="dz-cm-row"><span>Total HT</span><span>388,33 €</span></div>
      <div class="dz-cm-row"><span>TVA 20 %</span><span>77,67 €</span></div>
      <div class="dz-cm-row dz-cm-total"><span>Total TTC</span><b>466,00 €</b></div>
    </div>
  </div>
  <div class="dz-cm-invoice-actions"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#"><i class="fas fa-print"></i> Imprimer</a><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-download"></i> Télécharger le PDF</a></div>
</div>
"""

REASSURE = """
<div class="dz-cm-reassure">
  <div class="dz-cm-rs"><span class="dz-cm-rs-icon"><i class="fas fa-truck"></i></span><div><b>Livraison offerte</b><span>Dès 60 € d'achat, en 48 h</span></div></div>
  <div class="dz-cm-rs"><span class="dz-cm-rs-icon"><i class="fas fa-undo"></i></span><div><b>30 jours pour changer d'avis</b><span>Retours gratuits et simples</span></div></div>
  <div class="dz-cm-rs"><span class="dz-cm-rs-icon"><i class="fas fa-lock"></i></span><div><b>Paiement sécurisé</b><span>CB, virement ou 3 × sans frais</span></div></div>
  <div class="dz-cm-rs"><span class="dz-cm-rs-icon"><i class="fas fa-headset"></i></span><div><b>Conseil personnalisé</b><span>Du lundi au samedi, 9 h – 19 h</span></div></div>
</div>
"""

HERO_PRODUCT = """
<div class="dz-cm-hero">
  <div class="dz-cm-hero-copy">
    <span class="dz-badge"><i class="fas fa-award"></i> Élu produit de l'année 2026</span>
    <h2 class="dz-h1">Le sac <em>Oléa</em>, cousu main à Roubaix</h2>
    <p class="dz-lead">Cuir pleine fleur tanné végétal, doublure en lin, 14 heures de travail par pièce. Il se patine avec vous, et se répare à vie.</p>
    <div class="dz-cm-hero-buy">
      <div class="dz-cm-price dz-cm-price-lg"><b>199 €</b></div>
      <a class="dz-btn dz-btn-lg" href="#"><i class="fas fa-shopping-bag"></i> Ajouter au panier</a>
      <a class="dz-btn dz-btn-lg dz-btn-ghost" href="#">Voir les détails</a>
    </div>
    <div class="dz-cm-hero-proof"><div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">AL</span><span class="dz-avatar dz-avatar-sm">MB</span><span class="dz-avatar dz-avatar-sm">JP</span></div><span><span class="dz-cm-stars" style="--r:96%"></span> <b>4,8</b> · 1 240 clientes conquises</span></div>
  </div>
  <div class="dz-cm-hero-visual">
    <div class="dz-cm-hero-img"><img src="https://picsum.photos/seed/cm-hero-sac/900/1000" alt="Sac Oléa en cuir cognac"></div>
    <div class="dz-cm-hero-tag dz-cm-hero-tag-a"><i class="fas fa-leaf"></i><div><b>Tannage végétal</b><span>Sans chrome</span></div></div>
    <div class="dz-cm-hero-tag dz-cm-hero-tag-b"><i class="fas fa-tools"></i><div><b>Réparable à vie</b><span>Atelier inclus</span></div></div>
  </div>
</div>
"""

RETURN = """
<div class="dz-cm-return">
  <div class="dz-cm-return-head"><span class="dz-cm-kicker">Commande OR-21177 · livrée le 5 août</span><h3 class="dz-h3">Retourner un article</h3><p class="dz-cm-muted">Sélectionnez les articles à renvoyer. Le remboursement est émis dès réception, sous 3 jours ouvrés.</p></div>
  <div class="dz-cm-return-items">
    <a class="dz-cm-return-item dz-on" href="#"><span class="dz-cm-box"><i class="fas fa-check"></i></span><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-cabas/120/150" alt="Cabas Oléa"></div><div><b>Cabas Oléa cuir grainé</b><span>Cognac · 139,00 €</span></div><span class="dz-cm-return-reason">Ne me convient pas <i class="fas fa-chevron-down"></i></span></a>
    <a class="dz-cm-return-item" href="#"><span class="dz-cm-box"><i class="fas fa-check"></i></span><div class="dz-cm-line-img dz-cm-line-img-sm"><img src="https://picsum.photos/seed/cm-bonnet/120/150" alt="Bonnet côtelé"></div><div><b>Bonnet côtelé</b><span>Gris chiné · 39,00 €</span></div><span class="dz-cm-return-reason dz-cm-return-reason-mute">Motif du retour <i class="fas fa-chevron-down"></i></span></a>
  </div>
  <div class="dz-cm-return-sub"><b>Mode de retour</b></div>
  <div class="dz-cm-options dz-cm-options-row">
    <a class="dz-cm-option dz-on" href="#"><span class="dz-cm-radio"></span><div><b>Point relais</b><span>QR code, sans imprimante</span></div><em>Gratuit</em></a>
    <a class="dz-cm-option" href="#"><span class="dz-cm-radio"></span><div><b>En boutique</b><span>Échange immédiat</span></div><em>Gratuit</em></a>
  </div>
  <div class="dz-cm-return-foot"><div><span class="dz-cm-muted">Remboursement estimé</span><b>139,00 €</b></div><a class="dz-btn" href="#">Valider le retour <i class="fas fa-arrow-right"></i></a></div>
</div>
"""

BLOCKS = [
    dict(name="grille de produits", icon="fas fa-th", wrap="section", html=GRID),
    dict(name="fiche produit", icon="fas fa-tshirt", wrap="section", html=PDP),
    dict(name="produit vedette", icon="fas fa-gem", wrap="section", html=HERO_PRODUCT),
    dict(name="panier latéral", icon="fas fa-shopping-bag", wrap="section", html=DRAWER),
    dict(name="page panier", icon="fas fa-shopping-cart", wrap="section", html=CART_PAGE),
    dict(name="tunnel de paiement", icon="fas fa-credit-card", wrap="section", html=CHECKOUT),
    dict(name="résumé de commande", icon="fas fa-list-alt", wrap="narrow", html=ORDER_SUMMARY),
    dict(name="confirmation de commande", icon="fas fa-check-circle", wrap="narrow", html=CONFIRM),
    dict(name="suivi de livraison", icon="fas fa-truck", wrap="section", html=TRACKING),
    dict(name="historique des commandes", icon="fas fa-history", wrap="section", html=HISTORY),
    dict(name="retour d'article", icon="fas fa-undo", wrap="narrow", html=RETURN),
    dict(name="avis clients", icon="fas fa-star-half-alt", wrap="section", html=REVIEWS),
    dict(name="codes promo", icon="fas fa-ticket-alt", wrap="section", html=COUPONS),
    dict(name="catégories en tuiles", icon="fas fa-th-large", wrap="section", html=CATEGORIES),
    dict(name="bannière soldes", icon="fas fa-percent", wrap="section", html=SALE),
    dict(name="liste de souhaits", icon="fas fa-heart", wrap="section", html=WISHLIST),
    dict(name="comparateur", icon="fas fa-balance-scale", wrap="section", html=COMPARE),
    dict(name="réassurance", icon="fas fa-shield-alt", wrap="section", html=REASSURE),
    dict(name="tableau de bord marchand", icon="fas fa-store", wrap="section", html=MERCHANT),
    dict(name="gestion de stock", icon="fas fa-boxes", wrap="section", html=STOCK),
    dict(name="facture", icon="fas fa-file-invoice", wrap="narrow", html=INVOICE),
]
