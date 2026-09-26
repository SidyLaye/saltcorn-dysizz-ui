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
