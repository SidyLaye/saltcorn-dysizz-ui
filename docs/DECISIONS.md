# Décisions

Une ligne par arbitrage rendu par Sidy. Une question tranchée ici n'est jamais reposée.
Vaut pour les trois dépôts (ui, flow, me).

| Date | Décision |
|---|---|
| 2026-09-23 | Saltcorn reste en **1.6.x** (image épinglée `1.6.2`). Pas de bêta en production ; la 1.7 se teste à part, sur une instance jetable. |
| 2026-09-23 | **Un tenant par cas d'usage.** Tout le kit (plugins, blocs, thème) doit être disponible pour tous les tenants à venir. |
| 2026-09-23 | Les nouveaux tenants sont créés depuis un tenant **« modele »** (réglage *New tenant template*). |
| 2026-09-23 | Les plugins sont distribués depuis **GitHub** pour l'instant ; publication npm quand ils seront stables. |
| 2026-09-26 | Le sous-domaine **`web` doit devenir le vrai tenant principal**. Le domaine de base est déjà occupé par autre chose. |
| 2026-09-26 | **La base Dysizz d'abord.** Les projets clients bâtis dessus (dont AMBS / leads immobiliers) attendent que la base soit solide et déployée. |
| 2026-09-26 | Toute correction sur une instance réelle : **analyse d'abord, puis simulation (dry-run)** qui n'écrit rien, puis seulement l'écriture. |
| 2026-09-26 | Aucun secret dans une conversation ni dans un dépôt : on ne donne que le **nom** de la variable. |
| 2026-09-26 | Sidy délègue : Claude décide par défaut, en visant le plus sûr, et note ici chaque choix (réversible). Il ne revient vers Sidy que pour ce que lui seul peut faire (mots de passe, Dokploy, DNS). |
| 2026-09-26 | *Par défaut* — **Tenants cloisonnés dans dysizz-flow** (2.4.1) : secrets du serveur jamais lisibles ; hors racine, variables d'environnement seulement si listées dans `DZF_ENV_PARTAGEES`, code JS dans le bac à sable Saltcorn. Le tenant racine garde tout son confort. Couvre « n'importe qui peut être admin d'un tenant ». |
| 2026-09-26 | *Par défaut* — **Aucune correction automatique sans aperçu** : la page Santé montre ce qui va changer, puis applique sur clic. Un mot de passe n'est jamais choisi à la place de Sidy. |
| 2026-09-26 | *Par défaut* — Les tests qui ont trouvé un vrai bug entrent dans la CI (moteur navigateur, page Santé) ; le contrôle visuel des blocs doit se faire à la vraie largeur mobile (390 px) avec les widgets démarrés. |
