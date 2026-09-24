# Les 8 vues maison

Elles s'utilisent comme n'importe quelle vue Saltcorn : Vues → Créer une vue → choisis le modèle. Les champs en JSON sont écrits à la main dans la configuration de la vue.

## DZ Indicateurs

Une rangée de chiffres. Chaque tuile :

| Clé | Rôle |
|---|---|
| `label`, `icon` | texte et icône Font Awesome (`fas fa-fire`) |
| `table` | la table à compter |
| `stat` | `count` (défaut), `sum`, `avg`, `min`, `max` |
| `field` | le champ additionné (pour sum, avg…) |
| `where` | filtre Saltcorn : `{"statut":"fait"}`, `{"not":{"statut":"fait"}}`, `{"or":[{…},{…}]}`, `{"statut":{"in":["a","b"]}}` |
| `period` | `{"field":"date","range":"month"}` — plages : today, overdue, next7, next30, last7, last30, month, last_month, year |
| `format` | `eur`, `xof`, `dec`, `pct` |
| `tone` | `primary`, `success`, `warning`, `danger`, `info` |
| `href` | lien au clic |
| `id` + `expr` | une tuile avec `"expr":"budget - depense"` calcule à partir des tuiles qui ont ces `id` |
| `optional` | `true` : la tuile disparaît si la table n'existe pas (module non installé) |
| `hidden` | `true` : calculée (pour une `expr`) mais pas affichée |

## DZ Tableau

Kanban sur une table. Réglages : champ des colonnes (un champ à choix), ordre des colonnes, champ du titre, infos sous le titre (`echeance,priorite,projet.nom`), tri, colonne « terminé » (on n'y montre que les dernières cartes), vue ouverte au clic, vue d'ajout (le champ de la colonne est prérempli), filtre JSON.

Glisser une carte modifie la ligne comme un formulaire le ferait : les déclencheurs « Update » de la table s'exécutent. La vue suit aussi l'état de la page (`?domaine=Maison`).

## DZ Répartition

Barres d'un total par groupe. Réglages : champ de regroupement (souvent une clé), champ additionné (vide = compter), champ date + période, et dans la table liée : libellé, objectif (la barre passe au rouge au-delà), couleur, icône. Filtres JSON sur les lignes et sur les groupes.

## DZ À venir

Frise des prochains jours. Chaque source :

| Clé | Rôle |
|---|---|
| `table`, `date`, `titre`, `sous_titre` | d'où viennent les éléments |
| `icon`, `tone`, `libelle` | apparence |
| `where` | filtre Saltcorn |
| `vue` | vue ouverte en fenêtre au clic |
| `retard` | `true` : montre aussi ce qui est passé, en rouge, sur « Aujourd'hui » |

Une source dont la table n'existe pas est ignorée.

## DZ Graphique

L'évolution d'une valeur dans le temps : courbe, aire ou barres. Réglages : champ date, champ valeur (vide = compter les lignes), calcul (somme, moyenne, max, min, compter), période, pas (heure, jour, semaine, mois) et, en option, « une courbe par » un champ (jusqu'à 8 séries). Sur Postgres, le regroupement est fait par la base : même des millions de lignes restent rapides. Idéal avec la table `dzf_mesures` de dysizz-flow (champ date `quand`, valeur `valeur`, une courbe par `nom`).

## DZ Calendrier

Un mois en grille. Réglages : champ date, champ titre, couleur par ligne (facultatif), vue de modification (clic sur un élément) et vue d'ajout (clic sur un jour, date pré-remplie). Navigation avec `?dz_mois=AAAA-MM`. Sur téléphone, les éléments deviennent des petites barres de couleur.

## DZ Journal

Un fil d'événements groupé par jour : logs, erreurs, historique d'activité. Le niveau (ok, info, attention, erreur, ou un booléen) colore chaque ligne et donne des filtres ; une recherche filtre instantanément. Marche tel quel sur `dzf_journal` (date `quand`, message `message`, niveau `ok`, source `bloc`, détail `duree_ms`).

## DZ Statut

L'état de tes services en un coup d'œil : un bandeau (« Tout fonctionne », « 2 en panne ») et une tuile par ligne, les pannes en premier. Reconnaît ok / up / lent / panne / erreur / expiré et les booléens. Fait pour la table de sites du modèle « Surveillance de sites » de dysizz-flow.
