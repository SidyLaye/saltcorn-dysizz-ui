"""Famille « Compte » : connexion, inscription, double authentification,
profil, sécurité, abonnement, clés d'API, membres, audit, notifications…
CSS : styles/40-compte.css — préfixe dz-ac-"""

FAMILY = "compte"

BLOCKS = [

# ------------------------------------------------------------------ 1
dict(name="connexion", icon="fas fa-sign-in-alt", html="""
<div class="dz-ac-auth">
  <div class="dz-ac-auth-card">
    <div class="dz-ac-logo"><span class="dz-ac-logo-mark"><i class="fas fa-bolt"></i></span><span>Nexora</span></div>
    <h2 class="dz-ac-auth-title">Bon retour parmi nous</h2>
    <p class="dz-ac-auth-sub">Connectez-vous pour retrouver votre espace.</p>
    <div class="dz-ac-providers">
      <a class="dz-ac-prov" href="#"><i class="fas fa-building"></i> Authentification unique (SSO)</a>
      <a class="dz-ac-prov" href="#"><i class="fas fa-fingerprint"></i> Clé d'accès</a>
    </div>
    <div class="dz-ac-or"><span>ou avec votre e-mail</span></div>
    <div class="dz-ac-fields">
      <label class="dz-ac-field"><span class="dz-ac-label">Adresse e-mail</span><input class="dz-ac-input" type="email" placeholder="vous@entreprise.fr" value="camille@atelier-lune.fr"></label>
      <label class="dz-ac-field"><span class="dz-ac-label-row"><span class="dz-ac-label">Mot de passe</span><a class="dz-ac-link" href="#">Oublié ?</a></span><input class="dz-ac-input" type="password" placeholder="••••••••" value="motdepasse"></label>
      <label class="dz-ac-check"><input type="checkbox" checked><span>Rester connecté 30 jours</span></label>
    </div>
    <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Se connecter</a>
    <a class="dz-ac-magic" href="#"><i class="fas fa-magic"></i> Recevoir un lien de connexion par e-mail</a>
  </div>
  <p class="dz-ac-auth-alt">Pas encore de compte ? <a class="dz-ac-link" href="#">Créer un compte gratuit</a></p>
</div>
"""),

# ------------------------------------------------------------------ 2
dict(name="inscription", icon="fas fa-user-plus", html="""
<div class="dz-ac-signup">
  <div class="dz-ac-signup-pitch">
    <span class="dz-badge"><i class="fas fa-gift"></i> 14 jours offerts</span>
    <h2 class="dz-ac-pitch-title">Créez votre espace en <em>deux minutes</em></h2>
    <ul class="dz-ac-perks">
      <li><i class="fas fa-check"></i><span><b>Sans carte bancaire</b> pendant l'essai</span></li>
      <li><i class="fas fa-check"></i><span><b>Import guidé</b> de vos contacts et factures</span></li>
      <li><i class="fas fa-check"></i><span><b>Données hébergées en France</b>, chiffrées</span></li>
      <li><i class="fas fa-check"></i><span><b>Support humain</b> en moins de 2 h</span></li>
    </ul>
    <div class="dz-ac-proof"><div class="dz-avatars"><span class="dz-avatar dz-avatar-sm">IR</span><span class="dz-avatar dz-avatar-sm">MB</span><span class="dz-avatar dz-avatar-sm">JP</span><span class="dz-avatar dz-avatar-sm">+</span></div><span><b>12 400 équipes</b> nous font confiance</span></div>
  </div>
  <div class="dz-ac-auth-card">
    <h3 class="dz-ac-auth-title dz-ac-sm">Créer un compte</h3>
    <div class="dz-ac-fields">
      <div class="dz-ac-two">
        <label class="dz-ac-field"><span class="dz-ac-label">Prénom</span><input class="dz-ac-input" value="Inès"></label>
        <label class="dz-ac-field"><span class="dz-ac-label">Nom</span><input class="dz-ac-input" value="Roux"></label>
      </div>
      <label class="dz-ac-field"><span class="dz-ac-label">E-mail professionnel</span><input class="dz-ac-input" type="email" value="ines.roux@studio-pivoine.fr"></label>
      <label class="dz-ac-field"><span class="dz-ac-label">Mot de passe</span><input class="dz-ac-input" type="password" value="Pivoine-2026!"></label>
      <div class="dz-ac-strength dz-ac-strength-3"><span></span><span></span><span></span><span></span></div>
      <div class="dz-ac-rules"><span class="dz-ac-ok"><i class="fas fa-check"></i> 12 caractères</span><span class="dz-ac-ok"><i class="fas fa-check"></i> Un chiffre</span><span class="dz-ac-ok"><i class="fas fa-check"></i> Un symbole</span><span><i class="fas fa-circle"></i> Pas de mot courant</span></div>
      <label class="dz-ac-check"><input type="checkbox" checked><span>J'accepte les <a class="dz-ac-link" href="#">conditions d'utilisation</a> et la <a class="dz-ac-link" href="#">politique de confidentialité</a>.</span></label>
    </div>
    <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Créer mon espace <i class="fas fa-arrow-right"></i></a>
    <p class="dz-ac-auth-alt dz-ac-in">Déjà inscrit ? <a class="dz-ac-link" href="#">Se connecter</a></p>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 3
dict(name="écran partagé", icon="fas fa-columns", wrap="full", html="""
<div class="dz-ac-split">
  <div class="dz-ac-split-visual">
    <div class="dz-ac-logo dz-ac-logo-inv"><span class="dz-ac-logo-mark"><i class="fas fa-bolt"></i></span><span>Nexora</span></div>
    <div class="dz-ac-split-mock">
      <div class="dz-ac-mock-card"><span class="dz-ac-mock-label">Encaissé ce mois</span><b class="dz-ac-mock-val">48 250 €</b><span class="dz-ac-mock-trend"><i class="fas fa-arrow-up"></i> 18 % vs août</span><div class="dz-ac-mock-bars"><span style="--h:40%"></span><span style="--h:55%"></span><span style="--h:48%"></span><span style="--h:70%"></span><span style="--h:62%"></span><span style="--h:88%"></span><span style="--h:100%"></span></div></div>
      <div class="dz-ac-mock-toast"><i class="fas fa-check-circle"></i><span><b>Facture F-2026-0412 payée</b> Atelier Lune · 1 250 €</span></div>
    </div>
    <blockquote class="dz-ac-split-quote"><p>« Nous avons divisé par trois le temps passé sur la facturation. »</p><span>Maxime Bertin, gérant de Bertin &amp; Fils</span></blockquote>
  </div>
  <div class="dz-ac-split-form">
    <div class="dz-ac-split-inner">
      <h2 class="dz-ac-auth-title">Connexion</h2>
      <p class="dz-ac-auth-sub">Entrez vos identifiants pour continuer.</p>
      <div class="dz-ac-fields">
        <label class="dz-ac-field"><span class="dz-ac-label">E-mail</span><input class="dz-ac-input" type="email" placeholder="vous@entreprise.fr"></label>
        <label class="dz-ac-field"><span class="dz-ac-label-row"><span class="dz-ac-label">Mot de passe</span><a class="dz-ac-link" href="#">Oublié ?</a></span><input class="dz-ac-input" type="password" placeholder="••••••••"></label>
      </div>
      <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Continuer</a>
      <div class="dz-ac-or"><span>ou</span></div>
      <a class="dz-ac-prov dz-ac-prov-full" href="#"><i class="fas fa-fingerprint"></i> Se connecter avec une clé d'accès</a>
      <p class="dz-ac-legal">En continuant, vous acceptez nos <a href="#">conditions</a> et notre <a href="#">politique de confidentialité</a>.</p>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 4
dict(name="mot de passe oublié", icon="fas fa-unlock-alt", html="""
<div class="dz-ac-pair">
  <div class="dz-ac-auth-card dz-ac-center">
    <span class="dz-ac-hero-ico"><i class="fas fa-key"></i></span>
    <h2 class="dz-ac-auth-title dz-ac-sm">Mot de passe oublié ?</h2>
    <p class="dz-ac-auth-sub">Indiquez votre e-mail : nous vous enverrons un lien pour en choisir un nouveau.</p>
    <div class="dz-ac-fields"><label class="dz-ac-field"><span class="dz-ac-label">Adresse e-mail</span><input class="dz-ac-input" type="email" placeholder="vous@entreprise.fr"></label></div>
    <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Envoyer le lien</a>
    <a class="dz-ac-back" href="#"><i class="fas fa-arrow-left"></i> Retour à la connexion</a>
  </div>
  <div class="dz-ac-auth-card dz-ac-center">
    <span class="dz-ac-hero-ico dz-ac-hero-ok"><i class="fas fa-envelope-open-text"></i></span>
    <h2 class="dz-ac-auth-title dz-ac-sm">Vérifiez votre boîte mail</h2>
    <p class="dz-ac-auth-sub">Un lien a été envoyé à <b>camille@atelier-lune.fr</b>. Il reste valable 30 minutes.</p>
    <div class="dz-ac-mailhint"><i class="fas fa-info-circle"></i><span>Rien reçu ? Regardez dans les indésirables ou renvoyez le lien dans <b>0:42</b>.</span></div>
    <a class="dz-btn dz-btn-ghost dz-btn-block" href="#">Ouvrir ma messagerie</a>
    <a class="dz-ac-back" href="#">Utiliser une autre adresse</a>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 5
dict(name="code de vérification", icon="fas fa-mobile-alt", html="""
<div class="dz-ac-auth">
  <div class="dz-ac-auth-card dz-ac-center">
    <span class="dz-ac-hero-ico"><i class="fas fa-shield-alt"></i></span>
    <h2 class="dz-ac-auth-title dz-ac-sm">Vérification en deux étapes</h2>
    <p class="dz-ac-auth-sub">Saisissez le code à 6 chiffres affiché par votre application d'authentification.</p>
    <div class="dz-ac-otp">
      <input class="dz-ac-otp-cell" value="4" maxlength="1" inputmode="numeric" aria-label="Chiffre 1">
      <input class="dz-ac-otp-cell" value="8" maxlength="1" inputmode="numeric" aria-label="Chiffre 2">
      <input class="dz-ac-otp-cell" value="2" maxlength="1" inputmode="numeric" aria-label="Chiffre 3">
      <span class="dz-ac-otp-sep"></span>
      <input class="dz-ac-otp-cell dz-ac-otp-active" maxlength="1" inputmode="numeric" aria-label="Chiffre 4">
      <input class="dz-ac-otp-cell" maxlength="1" inputmode="numeric" aria-label="Chiffre 5">
      <input class="dz-ac-otp-cell" maxlength="1" inputmode="numeric" aria-label="Chiffre 6">
    </div>
    <label class="dz-ac-check dz-ac-check-c"><input type="checkbox"><span>Faire confiance à cet appareil pendant 30 jours</span></label>
    <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Vérifier</a>
    <div class="dz-ac-otp-foot"><span><i class="far fa-clock"></i> Nouveau code dans <b>0:24</b></span><a class="dz-ac-link" href="#">Utiliser un code de secours</a></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 6
dict(name="choix de la double authentification", icon="fas fa-user-lock", wrap="narrow", html="""
<div class="dz-ac-mfa">
  <div class="dz-ac-mfa-head"><span class="dz-ac-stepno">Étape 1 sur 3</span><h2 class="dz-ac-h">Protégez votre compte</h2><p class="dz-ac-desc">Choisissez comment confirmer votre identité à chaque connexion.</p></div>
  <div class="dz-ac-options">
    <a class="dz-ac-option dz-active" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-mobile-alt"></i></span><span class="dz-ac-opt-txt"><b>Application d'authentification <span class="dz-badge dz-badge-success">Recommandé</span></b><span>Un code à 6 chiffres renouvelé toutes les 30 secondes, même hors ligne.</span></span><span class="dz-ac-radio"></span></a>
    <a class="dz-ac-option" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-fingerprint"></i></span><span class="dz-ac-opt-txt"><b>Clé d'accès ou clé de sécurité</b><span>Empreinte, visage ou clé physique. Le plus sûr contre l'hameçonnage.</span></span><span class="dz-ac-radio"></span></a>
    <a class="dz-ac-option" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-sms"></i></span><span class="dz-ac-opt-txt"><b>SMS</b><span>Un code envoyé au 06 •• •• •• 42. Pratique, mais moins sûr.</span></span><span class="dz-ac-radio"></span></a>
    <a class="dz-ac-option" href="#"><span class="dz-ac-opt-ico"><i class="far fa-envelope"></i></span><span class="dz-ac-opt-txt"><b>E-mail</b><span>Un code envoyé à c•••••@atelier-lune.fr.</span></span><span class="dz-ac-radio"></span></a>
  </div>
  <div class="dz-ac-actions"><a class="dz-btn dz-btn-ghost" href="#">Plus tard</a><a class="dz-btn" href="#">Continuer <i class="fas fa-arrow-right"></i></a></div>
</div>
"""),

# ------------------------------------------------------------------ 7
dict(name="codes de secours", icon="fas fa-life-ring", wrap="narrow", html="""
<div class="dz-ac-panel dz-ac-backup dz-copy-scope">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Codes de secours</h3><p class="dz-ac-desc">Chaque code ne fonctionne qu'une fois. Conservez-les dans un endroit sûr.</p></div><span class="dz-badge dz-badge-neutral">8 sur 10 restants</span></div>
  <div class="dz-ac-panel-body">
    <div class="dz-ac-codes">
      <code>7KQ2-M9XA</code><code>P4HD-2WZN</code><code class="dz-ac-used">R8TC-6LJE</code><code>B3VY-Q7PF</code><code>N6GS-1KMR</code>
      <code>X9UE-4HTB</code><code class="dz-ac-used">D2LW-8CQA</code><code>J5ZP-3NRV</code><code>F7MK-9YDS</code><code>H1TA-5GXE</code>
    </div>
    <div class="dz-ac-warnline"><i class="fas fa-exclamation-triangle"></i><span>Ces codes ne seront plus affichés. Si vous les perdez, générez-en de nouveaux : les anciens seront désactivés.</span></div>
  </div>
  <div class="dz-ac-panel-foot">
    <div class="dz-cluster"><button class="dz-ac-btn dz-copy"><i class="far fa-copy"></i> Copier</button><a class="dz-ac-btn" href="#"><i class="fas fa-download"></i> Télécharger .txt</a><a class="dz-ac-btn" href="#"><i class="fas fa-print"></i> Imprimer</a></div>
    <a class="dz-ac-link dz-ac-danger-link" href="#"><i class="fas fa-sync-alt"></i> Régénérer</a>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 8
dict(name="profil utilisateur", icon="fas fa-id-card", wrap="narrow", html="""
<div class="dz-ac-panel">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Profil public</h3><p class="dz-ac-desc">Ces informations sont visibles par les membres de votre espace.</p></div></div>
  <div class="dz-ac-panel-body">
    <div class="dz-ac-avatar-row">
      <span class="dz-avatar dz-ac-avatar-xl">CM</span>
      <div class="dz-ac-avatar-txt"><b>Photo de profil</b><span>JPG ou PNG, 1 Mo maximum. Recadrée en cercle.</span><div class="dz-cluster"><a class="dz-ac-btn" href="#"><i class="fas fa-upload"></i> Changer</a><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Retirer</a></div></div>
    </div>
    <div class="dz-ac-form-grid">
      <label class="dz-ac-field"><span class="dz-ac-label">Prénom</span><input class="dz-ac-input" value="Camille"></label>
      <label class="dz-ac-field"><span class="dz-ac-label">Nom</span><input class="dz-ac-input" value="Moreau"></label>
      <label class="dz-ac-field dz-ac-span"><span class="dz-ac-label-row"><span class="dz-ac-label">Adresse e-mail</span><span class="dz-ac-verified"><i class="fas fa-check-circle"></i> Vérifiée</span></span><input class="dz-ac-input" type="email" value="camille@atelier-lune.fr"></label>
      <label class="dz-ac-field"><span class="dz-ac-label">Fonction</span><input class="dz-ac-input" value="Responsable contenu"></label>
      <label class="dz-ac-field"><span class="dz-ac-label">Fuseau horaire</span><select class="dz-ac-input"><option>Europe/Paris (UTC+2)</option></select></label>
      <label class="dz-ac-field dz-ac-span"><span class="dz-ac-label-row"><span class="dz-ac-label">Bio</span><span class="dz-ac-hint">96 / 160</span></span><textarea class="dz-ac-input" rows="3">J'écris la documentation et les guides. Posez-moi vos questions sur la rédaction !</textarea></label>
    </div>
  </div>
  <div class="dz-ac-panel-foot"><span class="dz-ac-hint"><i class="fas fa-circle dz-ac-dot-warn"></i> Modifications non enregistrées</span><div class="dz-cluster"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Annuler</a><a class="dz-btn dz-btn-sm" href="#">Enregistrer</a></div></div>
</div>
"""),

# ------------------------------------------------------------------ 9
dict(name="sécurité et sessions", icon="fas fa-laptop", html="""
<div class="dz-ac-sec">
  <div class="dz-ac-panel">
    <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Sessions actives</h3><p class="dz-ac-desc">Appareils actuellement connectés à votre compte.</p></div><a class="dz-ac-btn dz-ac-btn-danger" href="#"><i class="fas fa-sign-out-alt"></i> Déconnecter les autres</a></div>
    <div class="dz-ac-list">
      <div class="dz-ac-item"><span class="dz-ac-dev"><i class="fas fa-laptop"></i></span><div class="dz-ac-item-txt"><b>Ordinateur portable · Navigateur Orbe 128 <span class="dz-badge dz-badge-success">Cet appareil</span></b><span>Nantes, France · 88.124.•••.12 · Actif maintenant</span></div></div>
      <div class="dz-ac-item"><span class="dz-ac-dev"><i class="fas fa-mobile-alt"></i></span><div class="dz-ac-item-txt"><b>Téléphone · Application Nexora 4.12</b><span>Nantes, France · il y a 2 h</span></div><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Révoquer</a></div>
      <div class="dz-ac-item"><span class="dz-ac-dev"><i class="fas fa-desktop"></i></span><div class="dz-ac-item-txt"><b>Poste fixe · Navigateur Vega 119</b><span>Lyon, France · 21 sept. 2026, 09:14</span></div><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Révoquer</a></div>
      <div class="dz-ac-item"><span class="dz-ac-dev"><i class="fas fa-tablet-alt"></i></span><div class="dz-ac-item-txt"><b>Tablette · Application Nexora 4.11</b><span>Rennes, France · 12 sept. 2026, 18:40</span></div><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Révoquer</a></div>
    </div>
  </div>
  <div class="dz-ac-panel">
    <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Historique des connexions</h3><p class="dz-ac-desc">Les 30 derniers jours.</p></div><a class="dz-ac-link" href="#">Tout voir</a></div>
    <div class="dz-ac-list dz-ac-log">
      <div class="dz-ac-item"><span class="dz-ac-state dz-ac-state-ok"><i class="fas fa-check"></i></span><div class="dz-ac-item-txt"><b>Connexion réussie</b><span>Clé d'accès · Nantes</span></div><span class="dz-ac-time">Aujourd'hui, 08:52</span></div>
      <div class="dz-ac-item"><span class="dz-ac-state dz-ac-state-bad"><i class="fas fa-times"></i></span><div class="dz-ac-item-txt"><b>Mot de passe incorrect</b><span>3 tentatives · Lisbonne, Portugal</span></div><span class="dz-ac-time">Hier, 23:17</span></div>
      <div class="dz-ac-item"><span class="dz-ac-state dz-ac-state-ok"><i class="fas fa-check"></i></span><div class="dz-ac-item-txt"><b>Connexion réussie</b><span>Mot de passe + code · Lyon</span></div><span class="dz-ac-time">21 sept., 09:14</span></div>
      <div class="dz-ac-item"><span class="dz-ac-state dz-ac-state-info"><i class="fas fa-key"></i></span><div class="dz-ac-item-txt"><b>Mot de passe modifié</b><span>Depuis cet appareil</span></div><span class="dz-ac-time">18 sept., 14:02</span></div>
    </div>
    <div class="dz-ac-alert"><i class="fas fa-exclamation-circle"></i><span>Une tentative inhabituelle a été bloquée. <a class="dz-ac-link" href="#">Ce n'était pas moi</a></span></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 10
dict(name="abonnement et facturation", icon="fas fa-credit-card", html="""
<div class="dz-ac-billing">
  <div class="dz-ac-plan">
    <div class="dz-ac-plan-top"><div><span class="dz-ac-kicker">Offre actuelle</span><h3 class="dz-ac-plan-name">Équipe <span class="dz-badge">Annuel</span></h3></div><div class="dz-ac-plan-price"><b>29 €</b><span>/ membre / mois HT</span></div></div>
    <p class="dz-ac-desc">8 membres · Prochain prélèvement de <b>2 784 €</b> le 12 janvier 2027.</p>
    <div class="dz-ac-usage">
      <div class="dz-ac-meter"><div class="dz-ac-meter-top"><span>Membres</span><b>8 / 10</b></div><div class="dz-ac-bar"><span style="--v:80%"></span></div></div>
      <div class="dz-ac-meter"><div class="dz-ac-meter-top"><span>Stockage</span><b>37,4 / 50 Go</b></div><div class="dz-ac-bar"><span style="--v:75%"></span></div></div>
      <div class="dz-ac-meter dz-ac-meter-warn"><div class="dz-ac-meter-top"><span>Appels API ce mois</span><b>92 800 / 100 000</b></div><div class="dz-ac-bar"><span style="--v:93%"></span></div></div>
    </div>
    <div class="dz-cluster"><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-arrow-up"></i> Passer à l'offre Entreprise</a><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Gérer l'offre</a></div>
  </div>
  <div class="dz-ac-pay">
    <span class="dz-ac-kicker">Moyen de paiement</span>
    <div class="dz-ac-card-visual"><div class="dz-ac-card-top"><span class="dz-ac-chip"></span><i class="fas fa-wifi"></i></div><span class="dz-ac-card-num">•••• •••• •••• 4821</span><div class="dz-ac-card-bottom"><span>ATELIER LUNE SAS</span><span>09 / 28</span></div></div>
    <div class="dz-ac-pay-meta"><span><i class="far fa-envelope"></i> compta@atelier-lune.fr</span><a class="dz-ac-link" href="#">Modifier</a></div>
  </div>
  <div class="dz-ac-panel dz-ac-invoices">
    <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Factures</h3></div><a class="dz-ac-link" href="#">Tout télécharger</a></div>
    <div class="dz-ac-list">
      <div class="dz-ac-inv"><span class="dz-ac-inv-no">F-2026-0112</span><span class="dz-ac-inv-date">12 janv. 2026</span><span class="dz-ac-inv-amt">2 784,00 €</span><span class="dz-badge dz-badge-success">Payée</span><a class="dz-ac-icon" href="#" aria-label="Télécharger"><i class="fas fa-download"></i></a></div>
      <div class="dz-ac-inv"><span class="dz-ac-inv-no">F-2025-1203</span><span class="dz-ac-inv-date">3 déc. 2025</span><span class="dz-ac-inv-amt">348,00 €</span><span class="dz-badge dz-badge-success">Payée</span><a class="dz-ac-icon" href="#" aria-label="Télécharger"><i class="fas fa-download"></i></a></div>
      <div class="dz-ac-inv"><span class="dz-ac-inv-no">F-2025-0112</span><span class="dz-ac-inv-date">12 janv. 2025</span><span class="dz-ac-inv-amt">2 088,00 €</span><span class="dz-badge dz-badge-neutral">Remboursée</span><a class="dz-ac-icon" href="#" aria-label="Télécharger"><i class="fas fa-download"></i></a></div>
    </div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 11
dict(name="choix d'offre", icon="fas fa-layer-group", html="""
<div class="dz-ac-plans">
  <div class="dz-ac-plans-head">
    <div><h2 class="dz-ac-h">Changer d'offre</h2><p class="dz-ac-desc">Le changement prend effet immédiatement, au prorata.</p></div>
    <div class="dz-ac-period"><a href="#">Mensuel</a><a class="dz-active" href="#">Annuel <span>−20 %</span></a></div>
  </div>
  <div class="dz-ac-plan-grid">
    <div class="dz-ac-offer"><span class="dz-ac-offer-name">Solo</span><div class="dz-ac-offer-price"><b>9 €</b><span>/ mois</span></div><p class="dz-ac-desc">Pour les indépendants qui démarrent.</p><ul class="dz-ac-feat"><li>1 membre</li><li>Factures illimitées</li><li>5 Go de stockage</li></ul><a class="dz-btn dz-btn-ghost dz-btn-block dz-btn-sm" href="#">Rétrograder</a></div>
    <div class="dz-ac-offer dz-ac-current"><span class="dz-ac-offer-flag">Offre actuelle</span><span class="dz-ac-offer-name">Équipe</span><div class="dz-ac-offer-price"><b>29 €</b><span>/ membre / mois</span></div><p class="dz-ac-desc">Pour collaborer à plusieurs, sans limite.</p><ul class="dz-ac-feat"><li>Jusqu'à 10 membres</li><li>Rôles et permissions</li><li>50 Go de stockage</li><li>100 000 appels API</li></ul><span class="dz-ac-offer-cur"><i class="fas fa-check"></i> Votre offre</span></div>
    <div class="dz-ac-offer dz-ac-offer-hi"><span class="dz-ac-offer-flag dz-ac-flag-hi">Recommandé</span><span class="dz-ac-offer-name">Entreprise</span><div class="dz-ac-offer-price"><b>49 €</b><span>/ membre / mois</span></div><p class="dz-ac-desc">Sécurité avancée et accompagnement dédié.</p><ul class="dz-ac-feat"><li>Membres illimités</li><li>Authentification unique (SSO)</li><li>Journal d'audit 2 ans</li><li>Interlocuteur dédié</li></ul><a class="dz-btn dz-btn-block dz-btn-sm" href="#">Passer à Entreprise</a></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 12
dict(name="clés d'API", icon="fas fa-key", html="""
<div class="dz-ac-panel">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Clés d'API</h3><p class="dz-ac-desc">Ces clés donnent accès à votre espace. Ne les partagez jamais publiquement.</p></div><a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouvelle clé</a></div>
  <div class="dz-ac-newkey dz-copy-scope">
    <div class="dz-ac-newkey-txt"><b><i class="fas fa-check-circle"></i> Clé « Synchro comptable » créée</b><span>Copiez-la maintenant : elle ne sera plus affichée.</span></div>
    <div class="dz-ac-keybox"><code>nx_live_7Hq2mV9pXa4LkR8tZc3WbN6y</code><button class="dz-ac-btn dz-copy"><i class="far fa-copy"></i> Copier</button></div>
  </div>
  <div class="dz-ac-keys">
    <div class="dz-ac-key"><div class="dz-ac-key-main"><b>Synchro comptable</b><code class="dz-ac-mask">nx_live_7Hq2••••••••••••bN6y</code></div><div class="dz-ac-scopes"><span class="dz-ac-scope">factures:lecture</span><span class="dz-ac-scope">paiements:lecture</span></div><span class="dz-ac-time">Jamais utilisée</span><div class="dz-ac-key-act"><a class="dz-ac-icon" href="#" aria-label="Copier"><i class="far fa-copy"></i></a><a class="dz-ac-icon dz-ac-icon-danger" href="#" aria-label="Révoquer"><i class="far fa-trash-alt"></i></a></div></div>
    <div class="dz-ac-key"><div class="dz-ac-key-main"><b>Site vitrine</b><code class="dz-ac-mask">nx_live_Pb4k••••••••••••2sQe</code></div><div class="dz-ac-scopes"><span class="dz-ac-scope">contacts:écriture</span></div><span class="dz-ac-time">Il y a 4 min</span><div class="dz-ac-key-act"><a class="dz-ac-icon" href="#" aria-label="Copier"><i class="far fa-copy"></i></a><a class="dz-ac-icon dz-ac-icon-danger" href="#" aria-label="Révoquer"><i class="far fa-trash-alt"></i></a></div></div>
    <div class="dz-ac-key"><div class="dz-ac-key-main"><b>Tests <span class="dz-badge dz-badge-warning">Test</span></b><code class="dz-ac-mask">nx_test_9Tz1••••••••••••Lm0a</code></div><div class="dz-ac-scopes"><span class="dz-ac-scope">tout</span></div><span class="dz-ac-time">Il y a 3 jours</span><div class="dz-ac-key-act"><a class="dz-ac-icon" href="#" aria-label="Copier"><i class="far fa-copy"></i></a><a class="dz-ac-icon dz-ac-icon-danger" href="#" aria-label="Révoquer"><i class="far fa-trash-alt"></i></a></div></div>
    <div class="dz-ac-key dz-ac-revoked"><div class="dz-ac-key-main"><b>Ancienne intégration</b><code class="dz-ac-mask">nx_live_Aa81••••••••••••Qw7z</code></div><div class="dz-ac-scopes"><span class="dz-badge dz-badge-danger">Révoquée</span></div><span class="dz-ac-time">2 août 2026</span><div class="dz-ac-key-act"></div></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 13
dict(name="membres et invitations", icon="fas fa-user-friends", html="""
<div class="dz-ac-panel">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Membres de l'espace <span class="dz-ac-count">8</span></h3><p class="dz-ac-desc">Gérez qui peut accéder à « Atelier Lune » et avec quels droits.</p></div></div>
  <div class="dz-ac-invite">
    <input class="dz-ac-input" type="email" placeholder="Adresses e-mail, séparées par des virgules" aria-label="E-mails à inviter">
    <span class="dz-ac-select">Membre <i class="fas fa-chevron-down"></i></span>
    <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-paper-plane"></i> Inviter</a>
  </div>
  <div class="dz-ac-members">
    <div class="dz-ac-member"><span class="dz-avatar dz-avatar-sm">CM</span><div class="dz-ac-item-txt"><b>Camille Moreau <span class="dz-ac-you">vous</span></b><span>camille@atelier-lune.fr</span></div><span class="dz-ac-role dz-ac-role-owner"><i class="fas fa-crown"></i> Propriétaire</span><span class="dz-ac-time">Actif maintenant</span></div>
    <div class="dz-ac-member"><span class="dz-avatar dz-avatar-sm">HL</span><div class="dz-ac-item-txt"><b>Hugo Lefèvre</b><span>hugo@atelier-lune.fr</span></div><span class="dz-ac-select">Administrateur <i class="fas fa-chevron-down"></i></span><span class="dz-ac-time">Il y a 1 h</span></div>
    <div class="dz-ac-member"><span class="dz-avatar dz-avatar-sm">NB</span><div class="dz-ac-item-txt"><b>Nadia Benali</b><span>nadia@atelier-lune.fr</span></div><span class="dz-ac-select">Membre <i class="fas fa-chevron-down"></i></span><span class="dz-ac-time">Hier</span></div>
    <div class="dz-ac-member"><span class="dz-avatar dz-avatar-sm">TM</span><div class="dz-ac-item-txt"><b>Théo Martin</b><span>theo.martin@cabinet-arnaud.fr</span></div><span class="dz-ac-select">Invité · lecture <i class="fas fa-chevron-down"></i></span><span class="dz-ac-time">Il y a 6 jours</span></div>
  </div>
  <div class="dz-ac-subhead"><span>Invitations en attente</span><span class="dz-ac-count">2</span></div>
  <div class="dz-ac-members">
    <div class="dz-ac-member dz-ac-pending"><span class="dz-ac-ghost-av"><i class="far fa-envelope"></i></span><div class="dz-ac-item-txt"><b>julie.perrin@studio-pivoine.fr</b><span>Invitée par Hugo · expire dans 5 jours</span></div><span class="dz-badge dz-badge-warning">En attente</span><div class="dz-ac-key-act"><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Renvoyer</a><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Annuler</a></div></div>
    <div class="dz-ac-member dz-ac-pending"><span class="dz-ac-ghost-av"><i class="far fa-envelope"></i></span><div class="dz-ac-item-txt"><b>marc@bertin-fils.fr</b><span>Invité par vous · expire demain</span></div><span class="dz-badge dz-badge-warning">En attente</span><div class="dz-ac-key-act"><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Renvoyer</a><a class="dz-ac-btn dz-ac-btn-quiet" href="#">Annuler</a></div></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 14
dict(name="journal d'audit", icon="fas fa-clipboard-list", html="""
<div class="dz-ac-panel">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Journal d'audit</h3><p class="dz-ac-desc">Toutes les actions sensibles, conservées 2 ans.</p></div><a class="dz-ac-btn" href="#"><i class="fas fa-file-export"></i> Exporter CSV</a></div>
  <div class="dz-ac-filters">
    <div class="dz-ac-search"><i class="fas fa-search"></i><span>Rechercher un membre, une action…</span></div>
    <div class="dz-chips"><span class="dz-chip dz-active">Tout</span><span class="dz-chip">Sécurité</span><span class="dz-chip">Membres</span><span class="dz-chip">Facturation</span><span class="dz-chip">API</span></div>
  </div>
  <div class="dz-ac-audit">
    <div class="dz-ac-day">Aujourd'hui</div>
    <div class="dz-ac-event"><span class="dz-ac-ev-ico dz-ac-ev-sec"><i class="fas fa-shield-alt"></i></span><div class="dz-ac-ev-txt"><span><b>Camille Moreau</b> a activé la double authentification obligatoire</span><span class="dz-ac-ev-meta">Sécurité · 88.124.•••.12 · Nantes</span></div><span class="dz-ac-time">10:42</span></div>
    <div class="dz-ac-event"><span class="dz-ac-ev-ico dz-ac-ev-api"><i class="fas fa-key"></i></span><div class="dz-ac-ev-txt"><span><b>Hugo Lefèvre</b> a créé la clé d'API <code>Synchro comptable</code></span><span class="dz-ac-ev-meta">API · 2 permissions</span></div><span class="dz-ac-time">09:15</span></div>
    <div class="dz-ac-day">Hier</div>
    <div class="dz-ac-event"><span class="dz-ac-ev-ico dz-ac-ev-mem"><i class="fas fa-user-plus"></i></span><div class="dz-ac-ev-txt"><span><b>Hugo Lefèvre</b> a invité <b>julie.perrin@studio-pivoine.fr</b> comme Membre</span><span class="dz-ac-ev-meta">Membres</span></div><span class="dz-ac-time">17:30</span></div>
    <div class="dz-ac-event"><span class="dz-ac-ev-ico dz-ac-ev-bill"><i class="fas fa-file-invoice"></i></span><div class="dz-ac-ev-txt"><span><b>Nadia Benali</b> a modifié le moyen de paiement</span><span class="dz-ac-ev-meta">Facturation · carte se terminant par 4821</span></div><span class="dz-ac-time">11:08</span></div>
    <div class="dz-ac-event"><span class="dz-ac-ev-ico dz-ac-ev-danger"><i class="fas fa-user-minus"></i></span><div class="dz-ac-ev-txt"><span><b>Camille Moreau</b> a retiré <b>Paul Girard</b> de l'espace</span><span class="dz-ac-ev-meta">Membres · accès révoqué sur 3 appareils</span></div><span class="dz-ac-time">08:51</span></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 15
dict(name="préférences de notifications", icon="fas fa-bell", wrap="narrow", html="""
<div class="dz-ac-panel">
  <div class="dz-ac-panel-head"><div><h3 class="dz-ac-panel-title">Notifications</h3><p class="dz-ac-desc">Choisissez ce qui vous est envoyé, et par quel canal.</p></div></div>
  <div class="dz-ac-matrix">
    <div class="dz-ac-mx-head"><span>Événement</span><span>E-mail</span><span>Mobile</span><span>Appli</span></div>
    <div class="dz-ac-mx-group">Facturation</div>
    <div class="dz-ac-mx-row"><div class="dz-ac-mx-label"><b>Facture payée</b><span>Quand un client règle une facture</span></div><input class="dz-switch" type="checkbox" checked aria-label="E-mail"><input class="dz-switch" type="checkbox" checked aria-label="Mobile"><input class="dz-switch" type="checkbox" checked aria-label="Appli"></div>
    <div class="dz-ac-mx-row"><div class="dz-ac-mx-label"><b>Facture en retard</b><span>Chaque matin, la liste des retards</span></div><input class="dz-switch" type="checkbox" checked aria-label="E-mail"><input class="dz-switch" type="checkbox" aria-label="Mobile"><input class="dz-switch" type="checkbox" checked aria-label="Appli"></div>
    <div class="dz-ac-mx-group">Équipe</div>
    <div class="dz-ac-mx-row"><div class="dz-ac-mx-label"><b>Mentions</b><span>Quand quelqu'un vous cite</span></div><input class="dz-switch" type="checkbox" aria-label="E-mail"><input class="dz-switch" type="checkbox" checked aria-label="Mobile"><input class="dz-switch" type="checkbox" checked aria-label="Appli"></div>
    <div class="dz-ac-mx-row"><div class="dz-ac-mx-label"><b>Nouveau membre</b><span>Quand une invitation est acceptée</span></div><input class="dz-switch" type="checkbox" checked aria-label="E-mail"><input class="dz-switch" type="checkbox" aria-label="Mobile"><input class="dz-switch" type="checkbox" aria-label="Appli"></div>
    <div class="dz-ac-mx-group">Compte</div>
    <div class="dz-ac-mx-row"><div class="dz-ac-mx-label"><b>Alertes de sécurité <i class="fas fa-lock dz-ac-lock"></i></b><span>Toujours actives, par précaution</span></div><input class="dz-switch" type="checkbox" checked disabled aria-label="E-mail"><input class="dz-switch" type="checkbox" checked disabled aria-label="Mobile"><input class="dz-switch" type="checkbox" checked disabled aria-label="Appli"></div>
  </div>
  <div class="dz-ac-panel-foot"><div class="dz-ac-digest"><i class="far fa-moon"></i><span><b>Ne pas déranger</b> de 20:00 à 08:00 et le week-end</span></div><a class="dz-ac-link" href="#">Modifier</a></div>
</div>
"""),

# ------------------------------------------------------------------ 16
dict(name="zone de danger", icon="fas fa-exclamation-triangle", wrap="narrow", html="""
<div class="dz-ac-dangerzone">
  <h3 class="dz-ac-panel-title dz-ac-dz-title"><i class="fas fa-exclamation-triangle"></i> Zone de danger</h3>
  <div class="dz-ac-dz">
    <div class="dz-ac-dz-row"><div class="dz-ac-item-txt"><b>Exporter toutes mes données</b><span>Une archive ZIP (CSV + pièces jointes) envoyée par e-mail sous 24 h.</span></div><a class="dz-ac-btn" href="#"><i class="fas fa-download"></i> Exporter</a></div>
    <div class="dz-ac-dz-row"><div class="dz-ac-item-txt"><b>Transférer la propriété</b><span>Un autre administrateur deviendra propriétaire de l'espace.</span></div><a class="dz-ac-btn" href="#">Transférer</a></div>
    <div class="dz-ac-dz-row"><div class="dz-ac-item-txt"><b>Supprimer le compte</b><span>Votre espace, 1 284 factures et 312 contacts seront supprimés après 30 jours.</span></div><a class="dz-ac-btn dz-ac-btn-danger" href="#dz-ac-confirm">Supprimer…</a></div>
  </div>
  <div class="dz-ac-confirm" id="dz-ac-confirm">
    <div class="dz-ac-confirm-head"><span class="dz-ac-hero-ico dz-ac-hero-bad"><i class="far fa-trash-alt"></i></span><div><b>Supprimer « Atelier Lune » ?</b><span>Cette action est irréversible après le délai de 30 jours.</span></div></div>
    <ul class="dz-ac-consequences"><li>8 membres perdront immédiatement l'accès</li><li>Les 3 clés d'API actives seront révoquées</li><li>L'abonnement sera résilié sans remboursement du mois en cours</li></ul>
    <label class="dz-ac-field"><span class="dz-ac-label">Tapez <b>atelier-lune</b> pour confirmer</span><input class="dz-ac-input dz-ac-input-danger" value="atelier-lu"></label>
    <div class="dz-ac-actions"><a class="dz-btn dz-btn-ghost dz-btn-sm" href="#">Annuler</a><span class="dz-ac-btn-disabled">Supprimer définitivement</span></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 17
dict(name="changement d'espace", icon="fas fa-exchange-alt", html="""
<div class="dz-ac-ws-stage">
  <div class="dz-ac-ws-trigger"><span class="dz-ac-ws-logo dz-ac-ws-a">AL</span><div class="dz-ac-item-txt"><b>Atelier Lune</b><span>Équipe · 8 membres</span></div><i class="fas fa-chevron-down"></i></div>
  <div class="dz-ac-ws">
    <div class="dz-ac-ws-search"><i class="fas fa-search"></i><span>Rechercher un espace</span><span class="dz-kbd">⌘O</span></div>
    <div class="dz-ac-ws-label">Vos espaces</div>
    <a class="dz-ac-ws-item dz-active" href="#"><span class="dz-ac-ws-logo dz-ac-ws-a">AL</span><span class="dz-ac-item-txt"><b>Atelier Lune</b><span>Équipe · 8 membres</span></span><i class="fas fa-check"></i></a>
    <a class="dz-ac-ws-item" href="#"><span class="dz-ac-ws-logo dz-ac-ws-b">SP</span><span class="dz-ac-item-txt"><b>Studio Pivoine</b><span>Solo · 1 membre</span></span><span class="dz-ac-ws-dot">3</span></a>
    <a class="dz-ac-ws-item" href="#"><span class="dz-ac-ws-logo dz-ac-ws-c">BF</span><span class="dz-ac-item-txt"><b>Bertin &amp; Fils</b><span>Entreprise · 42 membres</span></span><span class="dz-kbd">⌘3</span></a>
    <div class="dz-ac-ws-sep"></div>
    <a class="dz-ac-ws-action" href="#"><i class="fas fa-plus"></i> Créer un espace</a>
    <a class="dz-ac-ws-action" href="#"><i class="fas fa-user-plus"></i> Rejoindre avec une invitation</a>
    <div class="dz-ac-ws-sep"></div>
    <div class="dz-ac-ws-me"><span class="dz-avatar dz-avatar-sm">CM</span><span class="dz-ac-item-txt"><b>Camille Moreau</b><span>camille@atelier-lune.fr</span></span><a class="dz-ac-icon" href="#" aria-label="Se déconnecter"><i class="fas fa-sign-out-alt"></i></a></div>
  </div>
</div>
"""),

# ------------------------------------------------------------------ 18
dict(name="bienvenue", icon="fas fa-hand-sparkles", html="""
<div class="dz-ac-welcome">
  <div class="dz-ac-welcome-head">
    <span class="dz-ac-wave">👋</span>
    <h2 class="dz-ac-h">Bienvenue, Inès !</h2>
    <p class="dz-ac-desc">Trois questions pour préparer votre espace. Vous pourrez tout changer plus tard.</p>
    <div class="dz-ac-steps"><span class="dz-ac-stepdot dz-done"></span><span class="dz-ac-stepdot dz-current"></span><span class="dz-ac-stepdot"></span></div>
  </div>
  <p class="dz-ac-q">Qu'allez-vous faire en priorité ?</p>
  <div class="dz-ac-uses">
    <a class="dz-ac-use dz-active" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-file-invoice-dollar"></i></span><b>Facturer mes clients</b><span>Devis, factures, relances</span><span class="dz-ac-use-check"><i class="fas fa-check"></i></span></a>
    <a class="dz-ac-use" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-address-book"></i></span><b>Suivre mes contacts</b><span>Fiches, historique, rappels</span><span class="dz-ac-use-check"><i class="fas fa-check"></i></span></a>
    <a class="dz-ac-use dz-active" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-chart-line"></i></span><b>Piloter ma trésorerie</b><span>Banque, prévisions, alertes</span><span class="dz-ac-use-check"><i class="fas fa-check"></i></span></a>
    <a class="dz-ac-use" href="#"><span class="dz-ac-opt-ico"><i class="fas fa-users"></i></span><b>Travailler en équipe</b><span>Tâches, rôles, partage</span><span class="dz-ac-use-check"><i class="fas fa-check"></i></span></a>
  </div>
  <div class="dz-ac-actions dz-ac-actions-between"><a class="dz-ac-back" href="#"><i class="fas fa-arrow-left"></i> Retour</a><div class="dz-cluster"><a class="dz-btn dz-btn-ghost" href="#">Passer</a><a class="dz-btn" href="#">Continuer <i class="fas fa-arrow-right"></i></a></div></div>
</div>
"""),

# ------------------------------------------------------------------ 19
dict(name="invitation reçue", icon="fas fa-envelope-open", html="""
<div class="dz-ac-auth">
  <div class="dz-ac-auth-card dz-ac-center dz-ac-invite-card">
    <div class="dz-ac-invite-logos"><span class="dz-avatar">HL</span><span class="dz-ac-invite-link"><i class="fas fa-arrow-right"></i></span><span class="dz-ac-ws-logo dz-ac-ws-a dz-ac-ws-lg">AL</span></div>
    <h2 class="dz-ac-auth-title dz-ac-sm">Hugo vous invite à rejoindre <em>Atelier Lune</em></h2>
    <p class="dz-ac-auth-sub">Vous rejoindrez l'espace en tant que <b>Membre</b> : factures, contacts et tâches partagées.</p>
    <div class="dz-ac-invite-meta">
      <div><span>Espace</span><b>Atelier Lune</b></div>
      <div><span>Membres</span><b><span class="dz-avatars"><span class="dz-avatar dz-avatar-sm">CM</span><span class="dz-avatar dz-avatar-sm">NB</span><span class="dz-avatar dz-avatar-sm">+6</span></span></b></div>
      <div><span>Expire</span><b>29 sept. 2026</b></div>
    </div>
    <a class="dz-btn dz-btn-block dz-ac-submit" href="#">Accepter l'invitation</a>
    <a class="dz-ac-back" href="#">Refuser</a>
    <p class="dz-ac-legal">Connecté en tant que julie.perrin@studio-pivoine.fr · <a href="#">Changer de compte</a></p>
  </div>
</div>
"""),

]
