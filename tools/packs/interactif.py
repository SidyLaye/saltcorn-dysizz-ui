"""Famille « Interactif » : des blocs vivants, du plus simple au plus poussé.
Chaque bloc est un <div data-dz-widget="…"> réglé par ses attributs data-… ;
le code du widget n'est chargé que sur les pages qui l'utilisent.
Préfixe CSS : dz-ix- (cadre). Dans un formulaire (vue Modifier), relie un
widget à un champ avec data-champ="nom_du_champ", ou utilise directement
les « fieldviews » dz_… sur le champ."""

import html as _h

FAMILY = "interactif"
BLOCKS = []


def section(titre, texte, widget, tip=""):
    return f"""
<section class="dz-section">
  <div class="dz-container">
    <div class="dz-ix-head"><div><h2 class="dz-h3">{titre}</h2><p>{texte}</p></div></div>
    {widget}
    {f'<p class="dz-ix-tip">{tip}</p>' if tip else ''}
  </div>
</section>"""


def w(name, **data):
    attrs = "".join(f' data-{k.replace("_", "-")}="{_h.escape(str(v), quote=True)}"' for k, v in data.items())
    return f'<div data-dz-widget="{name}"{attrs}></div>'


def add(name, icon, html):
    BLOCKS.append(dict(name=name, icon=icon, wrap="none", html=html))


# ---- 3D ---------------------------------------------------------------------
add("visionneuse 3D", "fas fa-cube", section(
    "Visionneuse 3D", "Montre un objet en 3D : on le fait tourner au doigt ou à la souris. Formats : GLB, GLTF, STL, OBJ.",
    w("3d", hauteur=420, rotation="true"),
    "Mets l'adresse de ton fichier dans <code>data-src</code> (ex. un fichier déposé dans Saltcorn : /files/serve/chaise.glb)."))
add("modeleur 3D", "fas fa-drafting-compass", section(
    "Modeleur 3D", "Ajoute des formes, déplace-les, tourne-les, change leurs couleurs, importe un modèle, exporte en GLB ou en STL pour l'impression 3D.",
    w("3d", mode="modeleur", hauteur=520),
    "Dans un formulaire, ajoute <code>data-champ=\"scene\"</code> pour enregistrer la scène dans un champ texte (ou utilise le champ « dz_3d_modeleur »)."))

# ---- jeux ---------------------------------------------------------------------
JEUX = [("serpent", "Serpent", "fas fa-gamepad"), ("casse-briques", "Casse-briques", "fas fa-th"), ("2048", "2048", "fas fa-border-all"),
        ("memoire", "Mémoire", "fas fa-clone"), ("morpion", "Morpion", "fas fa-hashtag"), ("coureur", "Coureur", "fas fa-running")]
for key, label, icon in JEUX:
    add(f"jeu {label.lower()}", icon, section(f"Jeu : {label}", "Jouable au clavier, à la souris et au doigt. Le record est gardé sur l'appareil.", w("jeu", jeu=key),
        "Pour garder les scores de tout le monde : <code>data-table-scores=\"scores\"</code> (table avec les champs jeu, score, quand)."))
add("jeu quiz", "fas fa-question-circle", section(
    "Quiz", "Tes propres questions : plus on répond vite, plus on marque de points.",
    w("jeu", jeu="quiz", questions='[{"q":"Quelle est la capitale du Sénégal ?","r":["Dakar","Thiès","Kaolack","Touba"],"ok":0},{"q":"Combien font 7 × 8 ?","r":["54","56","64","58"],"ok":1},{"q":"Quel langage tourne dans le navigateur ?","r":["Python","Java","JavaScript","C"],"ok":2}]'),
    "Change les questions dans <code>data-questions</code> : q = question, r = réponses, ok = numéro de la bonne (à partir de 0)."))
add("jeu à coder soi-même", "fas fa-gamepad", section(
    "Mon propre jeu", "Le mini-moteur de jeux est à toi : une scène avec debut, maj (logique, 60 fois par seconde) et dessin. Exemple : attrape les étoiles.",
    """<div data-dz-widget="jeu" data-jeu="perso" data-titre="Attrape les étoiles" data-aide="Déplace le panier avec la souris ou les flèches." data-largeur="480" data-hauteur="360"><script type="text/dz-jeu">
let panier, etoiles, temps;
return {
  debut(j) { panier = { x: 200, y: 330, w: 80, h: 14 }; etoiles = []; temps = 30; },
  maj(j, dt) {
    if (j.touche("gauche")) panier.x -= 400 * dt;
    if (j.touche("droite")) panier.x += 400 * dt;
    if (j.souris.x) panier.x += (j.souris.x - panier.w / 2 - panier.x) * 0.3;
    if (Math.random() < 0.04) etoiles.push({ x: j.hasard(10, 470), y: -10, v: j.hasard(90, 220) });
    for (const e of etoiles) {
      e.y += e.v * dt;
      if (j.collision({ x: e.x - 8, y: e.y - 8, w: 16, h: 16 }, panier)) { e.prise = true; j.points(1); j.son(900, 0.05); }
    }
    etoiles = etoiles.filter((e) => !e.prise && e.y < 380);
    temps -= dt; if (temps <= 0) j.gagne("Temps écoulé !");
  },
  dessin(j) {
    j.fond("#0f172a");
    etoiles.forEach((e) => j.texte("★", e.x, e.y, { taille: 22, couleur: "#facc15" }));
    j.rect(panier.x, panier.y, panier.w, panier.h, "#38bdf8", 6);
    j.texte(Math.ceil(temps) + " s", 450, 20, { taille: 16, align: "right" });
  },
};
</script></div>""",
    "Outils du moteur : j.touche/j.appui (haut, bas, gauche, droite, espace), j.souris, j.rect, j.rond, j.texte, j.collision, j.son, j.points, j.fin, j.gagne."))

# ---- données et outils ---------------------------------------------------------
add("carte avec points", "fas fa-map-marked-alt", section(
    "Carte", "Des lieux sur une carte OpenStreetMap, avec recherche d'adresse et « ma position ».",
    w("carte", hauteur=400, points='[{"lat":14.6937,"lon":-17.4441,"titre":"Dakar","texte":"Bureau principal","couleur":"#2563eb"},{"lat":48.8566,"lon":2.3522,"titre":"Paris","texte":"Agence","couleur":"#16a34a"},{"lat":45.764,"lon":4.8357,"titre":"Lyon","texte":"Entrepôt","couleur":"#f59e0b"}]'),
    "Depuis une table : <code>data-table=\"clients\" data-champ-position=\"position\" data-champ-titre=\"nom\" data-lien=\"/view/client?id={id}\"</code>."))
add("choisir une position", "fas fa-map-pin", section(
    "Choisir une position", "Clique sur la carte ou cherche une adresse : la position « lat,lon » va dans le champ du formulaire.",
    w("carte", mode="choisir", hauteur=340, champ="position")))
add("tableur", "fas fa-table", section(
    "Tableur", "Cellules, formules en français ou en anglais (=SOMME(A1:A5), =SI(B2>10;\"oui\";\"non\"), =MOYENNE…), copier-coller depuis Excel, import et export CSV.",
    w("tableur", hauteur=420, valeur='{"lignes":12,"colonnes":5,"cellules":{"A1":"Poste","B1":"Janvier","C1":"Février","D1":"Mars","E1":"Total","A2":"Loyer","B2":"850","C2":"850","D2":"850","E2":"=SOMME(B2:D2)","A3":"Courses","B3":"320","C3":"295","D3":"340","E3":"=SOMME(B3:D3)","A4":"Transport","B4":"75","C4":"75","D4":"90","E4":"=SOMME(B4:D4)","A5":"Total","B5":"=SOMME(B2:B4)","C5":"=SOMME(C2:C4)","D5":"=SOMME(D2:D4)","E5":"=SOMME(E2:E4)"},"gras":{"A1":1,"B1":1,"C1":1,"D1":1,"E1":1,"A5":1,"E5":1}}'),
    "Dans un formulaire : <code>data-champ=\"donnees\"</code> enregistre le tableau (JSON) dans un champ texte."))
# ---- Parcours (processus, workflows clients) -----------------------------------
import json as _json
_NDF = {"v": 1, "noeuds": [
    {"id": "d", "cle": "debut", "type": "debut", "titre": "Note de frais déposée", "x": 0, "y": 120},
    {"id": "c", "cle": "condition", "type": "condition", "titre": "Plus de 500 € ?", "x": 260, "y": 110, "reglages": {"expression": "ctx.montant > 500"}},
    {"id": "v", "cle": "validation", "type": "attente", "titre": "Accord du manager", "x": 520, "y": 20, "reglages": {"qui": "Manager"}},
    {"id": "p", "cle": "etape", "type": "etape", "titre": "Paiement par la compta", "x": 780, "y": 120, "reglages": {"responsable": "Comptabilité"}},
    {"id": "f", "cle": "fin", "type": "fin", "titre": "Remboursé", "x": 1040, "y": 120}],
  "liens": [{"id": "l1", "de": "d", "vers": "c"}, {"id": "l2", "de": "c", "vers": "v", "si": "oui"}, {"id": "l3", "de": "c", "vers": "p", "si": "non"},
            {"id": "l4", "de": "v", "vers": "p"}, {"id": "l5", "de": "p", "vers": "f"}]}
add("éditeur de parcours", "fas fa-project-diagram", section(
    "Éditeur de parcours", "Construis un processus en quelques clics : ajoute des étapes, relie-les en tirant le rond de droite, règle chaque étape dans le panneau. Au doigt comme à la souris, avec annuler, zoom et contrôle du schéma.",
    w("parcours", hauteur=460, valeur=_json.dumps(_NDF, ensure_ascii=False)),
    "Dans un formulaire, mets l'affichage « dz_parcours_saisie » sur un champ texte : le schéma y est enregistré. Le bloc dysizz-flow « Exécuter un parcours » le déroule pour de vrai."))
add("suivi d'un parcours", "fas fa-route", section(
    "Où en est le dossier ?", "Le même parcours en lecture seule : les étapes déjà passées sont en vert, l'étape en cours en orange.",
    w("parcours", hauteur=340, lecture="true", valeur=_json.dumps(_NDF, ensure_ascii=False), trace='["d","c","v"]', actif="v")))

add("tableau blanc", "fas fa-chalkboard", section(
    "Tableau blanc", "Dessine, écris, pose des post-it, fais des schémas. Zoom à la molette ou en pinçant, export en image.",
    w("tableau-blanc", hauteur=480)))
add("signature", "fas fa-signature", section(
    "Signature", "Signer un devis, un bon de livraison, une décharge… au doigt ou à la souris.",
    w("signature", hauteur=180, champ="signature"),
    "La signature (image) va dans le champ <code>signature</code> du formulaire."))
add("chat IA", "fas fa-robot", section(
    "Assistant IA", "Pose une question : l'assistant cherche dans tes données et répond.",
    w("chat-ia", url="/dzf/api/assistant", titre="Assistant", hauteur=460, suggestions='["Qu\'est-ce que j\'ai à faire aujourd\'hui ?","Résume mes tâches en retard"]'),
    "Installe le modèle « Assistant IA pour tes pages » dans dysizz-flow (Catalogue) : il crée l'adresse /dzf/api/assistant."))
add("chat IA en bulle", "fas fa-comment-dots", w("chat-ia", url="/dzf/api/assistant", flottant="true", titre="Assistant"))
add("portefeuille crypto", "fab fa-ethereum", section(
    "Portefeuille", "Connexion avec MetaMask, Rabby, Coinbase Wallet… : adresse, solde, preuve de propriété (signature) et paiement.",
    w("portefeuille", paiement="true"),
    "Pour vérifier la signature côté serveur : bloc flow « Blockchain : signer / vérifier un message »."))
add("planning (Gantt)", "fas fa-stream", section(
    "Planning", "Les tâches sur une frise de jours, avec l'avancement et le jour d'aujourd'hui.",
    w("gantt", taches='[{"nom":"Cadrage","debut":"2026-09-21","fin":"2026-09-25","avancement":100,"groupe":"Préparation"},{"nom":"Maquettes","debut":"2026-09-24","fin":"2026-10-02","avancement":60,"groupe":"Design"},{"nom":"Développement","debut":"2026-09-30","fin":"2026-10-16","avancement":20,"groupe":"Technique"},{"nom":"Recette","debut":"2026-10-15","fin":"2026-10-21","avancement":0,"groupe":"Technique"},{"nom":"Mise en ligne","debut":"2026-10-22","fin":"2026-10-22","groupe":"Livraison"}]'),
    "Depuis une table : <code>data-table=\"taches\" data-champ-nom=\"titre\" data-champ-debut=\"debut\" data-champ-fin=\"echeance\"</code>."))
add("scanner QR / code-barres", "fas fa-qrcode", section(
    "Scanner", "Lis un QR code ou un code-barres avec la caméra du téléphone, ou depuis une photo.",
    w("scanner", champ="code"),
    "Options : <code>data-action=\"lien\"</code> ouvre l'adresse lue ; <code>data-action=\"chercher\" data-url=\"/view/produits?code={valeur}\"</code>."))
add("prendre une photo", "fas fa-camera", section(
    "Photo", "Prends une photo avec la caméra (ticket, compteur, colis…) : elle va dans le champ du formulaire.",
    w("scanner", mode="photo", champ="photo")))
