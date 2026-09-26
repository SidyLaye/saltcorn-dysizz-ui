# Vision Dysizz

Ce que Sidy veut construire, dans ses mots, rangé. C'est la boussole de chaque
décision : une proposition qui n'y répond pas n'a pas sa place.

## Le but

Saltcorn devient la **plaque tournante** de toute sa vie, pro et perso. Tout
passe par une seule instance, et il la maîtrise à 100 %.

- **Tous les produits** : landing pages, sites web, SaaS, outils internes,
  web apps, applications mobiles, applications desktop.
- **Tous les appareils et plateformes**, sans exception.
- **Un tenant par cas d'usage** (pro, perso, chaque client, chaque SaaS). Tout ce
  qui est construit une fois est disponible pour **tous les tenants à venir**.

## Pour qui

N'importe qui doit pouvoir faire ce qu'il veut, dans tous les sens :

- le non-technicien qui n'y connaît rien et veut quelque chose d'ultra beau qui
  marche très bien : il glisse-dépose des éléments déjà prêts, sans coder ;
- le développeur qui veut prendre la main en profondeur : tout reste ouvert,
  lisible et modifiable en code ;
- et tout ce qu'il y a entre les deux, « du bébé au vieux au génie de l'informatique ».

## Le niveau attendu

- **Design** : moderne, fluide, interactif. Tous les registres : humain,
  générique, insolite, classique, jusqu'au « wow » et au « comment est-ce
  possible de faire ça ». Pas de design générique par défaut.
- **Prêt à l'emploi** : des éléments, des plugins et des workflows déjà faits,
  qu'on assemble au lieu de recoder à chaque fois.
- **Sécurité** complète, **performance** et **montée en charge** sans reproche,
  **modularité** totale.
- **Pensé pour l'avenir** : on anticipe, on prévoit, on vise toujours l'optimal.

## La méthode (mentalité ingénieur)

1. Partir simple.
2. Trouver le vrai goulot (mesuré, pas supposé).
3. Ajouter le plus petit composant qui le résout (cache, file, réplique, nœud…).
4. Recommencer quand le système grandit.

Chaque composant ajoute de la complexité : un cache peut être périmé, une file
peut livrer deux fois, une réplique peut être en retard. On n'ajoute rien
« au cas où ». Mais la base doit être saine dès le départ : une fragilité à la
fondation se paie partout ensuite. C'est pour ça que les projets clients (dont
AMBS) attendent que la base soit solide.

## Les briques actuelles

| Brique | Rôle |
|---|---|
| `dysizz-ui` | design system par tenant, blocs à glisser, vues de données, atelier, accueil `/dysizz` |
| `dysizz-flow` | blocs de workflow (façon n8n), coffre de secrets, points d'API, écouteurs |
| `dysizz-me` | modules perso (tâches, budget, santé, mails, veille…), faits uniquement avec ui + flow |
| tenant « modele » | copié à la création de chaque nouveau tenant (kit déjà installé) |
