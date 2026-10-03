# Actualisation des blocs de données

Les tableaux disposant de `data-rafraichir` sont relus périodiquement. Le signal
Saltcorn `dynamic_update` portant `dzf_lecture:true` déclenche une relecture groupée
après 750 ms, avec une seule connexion partagée par page.

Chaque source reste contrôlée selon le rôle et les tables accessibles. Le signal
ne contient aucune ligne. `_dz_frais=1` ignore un résultat en cache, sans changer
la validation ou les contrôles d'accès et sans multiplier les clés de cache.

Une saisie ou une sélection de texte dans le bloc empêche son remplacement
automatique. L'onglet caché n'est pas relu ; son retour déclenche une vérification.
Les pages déjà ouvertes doivent être rechargées après installation du module.
