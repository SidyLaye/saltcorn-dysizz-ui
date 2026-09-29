# Écrans d'application sans code propre

Un écran (tableau de bord, liste, fiche, formulaire) se construit avec dysizz-ui seul. On n'écrit ni CSS ni JavaScript dans la page, et on n'utilise pas de vue d'édition native. Tout se règle dans le tenant.

## 1. Navigation (réglages du plugin → étape « Navigation »)

| Réglage | Effet |
|---|---|
| Forme du menu | `latéral` (colonne à gauche, sous-menus), `en haut`, ou `thème` (ne rien changer). Posé sur le thème any-bootstrap-theme. |
| Afficher le nom et le logo | Coupé : la marque disparaît du menu (en haut comme sur le côté). |
| Entrée « Accueil » | Coupée par défaut : l'entrée vers `/dysizz` est retirée du menu ; l'accueil reste à son adresse. |
| Entrées admin en ambre | Dans le menu de l'administrateur, les entrées et sections au rôle 1 sont en ambre. |

L'entrée active du menu est celle dont les paramètres correspondent à l'adresse. `/page/gestion?t=equipe` n'allume que « Équipe », même quand l'onglet change sans recharger.

Les sections et sous-menus se créent dans l'éditeur de menu de Saltcorn : un en-tête (*Header*) avec des entrées dessous. Chaque entrée a un rôle minimal, et `max_role` vaut 1.

## 2. Mise en page (classes)

```html
<div class="dz-ecran">
  <div class="dz-ecran-niveau">Page réservée à l'administrateur</div>   <!-- facultatif -->
  <a class="dz-ecran-retour" href="/page/liste">← Retour</a>
  <div class="dz-ecran-titre"><h1>Titre</h1></div>
  <p class="dz-ecran-intro">Une phrase qui dit à quoi sert l'écran.</p>
  <div class="dz-ecran-grille dz-ecran-chiffres">…chiffres clés…</div>
  <div class="dz-ecran-grille dz-ecran-principale"><div class="dz-ecran-col">…</div><div class="dz-ecran-col">…</div></div>
  <p class="dz-ecran-note">Remarque discrète.</p>
  <a class="dz-ecran-bt" href="…">Action</a> <a class="dz-ecran-bt sec" href="…">Autre</a>
</div>
```

Grilles :
- `dz-ecran-chiffres` : tuiles de 170 px ;
- `dz-ecran-tuiles` : 230 px ;
- `dz-ecran-principale` : 2/3 + 1/3 ;
- `dz-ecran-moities` : deux moitiés.

Sous 980 px, tout passe sur une colonne.

## 3. Chiffres, listes, filtres, onglets : bloc « tableau »

Il lit une source de données (`/dysizz-ui/sources`). Vues :
- `kpi`, `courbe`, `barres`, `anneau` ;
- `liste` : groupée et repliable avec `grouper` / `replie` ;
- `fiche`, `grille`, `titre`, `note` ;
- `filtres` : les filtres et les onglets `boutons` vivent dans l'adresse.

Un bloc n'apparaît que pour certains onglets avec `montrer`.

## 4. Formulaires : bloc « fiche »

```html
<div data-dz-widget="fiche" data-table="absence"
     data-champs='["personne","motif","debut","fin",{"section":"Qui reçoit à sa place"},"remplacant","remplacant_adresse"]'
     data-titres='{"remplacant":"Une personne de l&#39;équipe"}'
     data-aides='{"fin":"Vide = sans date de fin"}'
     data-valeurs='{"motif":"congés"}'
     data-apres="/page/gestion?t=absences" data-supprimer="true"></div>
```

- **Création ou modification** : avec `?id=12` dans l'adresse (ou `data-id`), la fiche modifie la ligne ; sans id, elle en crée une.
- **Valeurs de départ** : les paramètres d'adresse au nom d'un champ (`?personne=14`) préremplissent la création.
- **Listes** :
  - les clés vers une autre table deviennent une liste de noms (champ de résumé, condition `where` du champ respectée) ;
  - les champs à choix deviennent une liste, avec des libellés lisibles par `data-libelles='{"champ":{"valeur":"Libellé"}}'`.
- **Champs sous condition** : `data-si='{"jours":{"temps":"mi_temps"}}'`.
- **Champs cachés** :
  - `data-caches='["ticket"]'` envoie ces champs sans les montrer (valeur de départ ou de la ligne) ;
  - `data-utilisateur='["auteur"]'` les remplit avec l'utilisateur connecté.

  Le champ propriétaire de la table est toujours rempli ainsi.
- **Sécurité** : l'écriture passe par l'API de Saltcorn, donc le serveur vérifie tout, comme pour une vue native :
  - rôle de la table, propriétaire ;
  - champs `min_role_write` (affichés en lecture seule pour qui ne peut pas les écrire) ;
  - déclencheurs Validate, Insert, Update.

  La lecture (`GET /dysizz/fiche/:table`) ne renvoie que ce que l'utilisateur peut lire.

## 5. Modifier plusieurs lignes d'un coup : réglage `selection` du bloc « tableau »

```html
<div data-dz-widget="tableau" data-source="equipe-liste" data-vue="liste" data-grouper="agence_nom"
     data-selection='{"table":"equipe","champs":["groupe","temps","jours","assistante","actif"],
                      "libelles":{"temps":{"plein":"Temps plein","mi_temps":"Temps partiel"}}}'></div>
```

Cases à cocher, « sélectionner le groupe », « Sélectionner les N résultats » (tous les résultats des filtres), puis « Modifier la sélection » : on choisit un ou plusieurs champs et leur nouvelle valeur (ou « vider ») ; chaque ligne est écrite par l'API de Saltcorn (droits vérifiés, déclencheurs lancés).

## 6. Rattacher des lignes, cocher plusieurs personnes : `membres` et `multiples` du bloc « fiche »

- `data-membres='{"table":"equipe","champ":"groupe","titre":"Qui est dans ce groupe ?","libelle":"nom","grouper":"agence_nom"}'` : dans la fiche d'un groupe, on coche ses membres (les autres lignes de `equipe` dont `groupe` vaut ce groupe).
- `data-multiples='{"personnes":{"table":"equipe","libelle":"nom","grouper":"agence_nom","si":{"role":"negociateur"}}}'` : le champ texte `personnes` (numéros "3,7,9") devient une liste à cocher.

## 7. Éditeur de pages

Une page faite en HTML se convertit en éléments natifs du builder avec `tools/html2layout.py` : titres et textes deviennent des éléments Texte, les grilles des conteneurs, et chaque bloc interactif un élément à part. Dans l'éditeur, chaque bloc dit ce qu'il montre ; ses réglages sont dans son code HTML (attributs `data-…`).
