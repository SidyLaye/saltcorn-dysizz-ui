# Faire tenir la charge : Saltcorn en production

Guide vérifié dans le code de Saltcorn 1.6.2. Objectif : plusieurs SaaS
(un tenant chacun), des milliers d'utilisateurs, fluide et sécurisé.

## 1. Ce qui compte vraiment

| Couche | Rôle | Où ça se règle |
|---|---|---|
| Navigateur | fluidité (animations, 1er affichage) | le kit (v2.1+ : fait) |
| CDN | pages publiques et fichiers statiques servis sans toucher le serveur | Cloudflare (ou autre) |
| Traefik | HTTPS, répartition de charge, limites de débit | Dokploy / labels |
| Saltcorn | N conteneurs × N workers | variables d'environnement |
| Postgres | le vrai goulot : connexions, index | `postgresql.conf` |
| Fichiers | partagés entre conteneurs | S3 (déjà configuré chez toi) |

Saltcorn 1.6.2 **n'utilise pas Redis**. Sessions, synchronisation entre
serveurs et élection du « chef » passent par Postgres. Redis reste utile
à côté (n8n en mode queue, cache applicatif de tes propres services),
mais le brancher ne rend pas Saltcorn plus rapide.

## 2. Plusieurs serveurs Saltcorn (load balancing)

Saltcorn sait tourner sur plusieurs machines/conteneurs derrière un
même domaine :

- `SALTCORN_MULTI_NODE=true` : chaque nœud écoute Postgres
  (`LISTEN/NOTIFY`). Installer un module, changer un réglage ou une vue
  sur un nœud se propage aux autres.
- **Tâches planifiées** : un seul nœud les exécute. Il est élu
  automatiquement (verrou Postgres). S'il tombe, un autre prend le relais
  en ~5 s. Rien à faire.
- `SALTCORN_NWORKERS` : nombre de processus par conteneur (par défaut :
  nombre de cœurs). Mets 2 à 4 par conteneur, et plus de conteneurs
  plutôt que plus de workers.
- **Identiques sur tous les nœuds** (sinon les utilisateurs sont
  déconnectés en passant d'un nœud à l'autre) :
  `SALTCORN_SESSION_SECRET` et `SALTCORN_JWT_SECRET`. Génère-les une fois
  (`openssl rand -hex 48`) et mets-les dans les secrets Dokploy.
- **Migrations** : un seul nœud les lance au démarrage. Les autres
  démarrent avec `serve --nomigrate`.
- **Temps réel** (socket.io) : Saltcorn n'utilise que les WebSockets, pas
  de « long polling ». Pas besoin de sessions collantes (sticky) dans
  Traefik.
- **Fichiers** : S3 pour tous les nœuds (Paramètres → Fichiers). Un
  dossier local par conteneur ne marche pas à plusieurs.

Le fichier `deploy/docker-compose.scale.yml` du dépôt donne une base
prête : 1 nœud « primaire » + un service « web » à dupliquer, derrière
le même routeur Traefik.

## 3. Postgres : le point à surveiller

Chaque processus Saltcorn ouvre jusqu'à **10 connexions** (valeur par
défaut de `pg`, non réglable dans Saltcorn), plus 2 pour le multi-nœud.

```
connexions ≈ conteneurs × (NWORKERS × 10 + 2)
ex. 3 conteneurs × 4 workers → ~130   →   max_connections = 200
```

- **PgBouncer** : seulement en mode `session`. Le mode `transaction`
  casse l'écoute `LISTEN/NOTIFY` et le verrou du chef. Tant que la
  formule ci-dessus tient sous ~300, Postgres direct est plus simple.
- Réglages de base pour 8 Go de RAM : `shared_buffers=2GB`,
  `effective_cache_size=6GB`, `work_mem=16MB`,
  `maintenance_work_mem=512MB`, `random_page_cost=1.1` (SSD).
- **Index** : sur chaque champ qui sert de filtre, de tri ou de clé
  étrangère dans tes vues. Dans Saltcorn : Tables → champ → cocher
  « Unique » ou créer un index (Tables → la table → Contraintes → Index).
  C'est le gain n°1 quand une liste devient lente.
- Tâches de fond lourdes (imports, e-mails de masse) : triggers
  planifiés la nuit plutôt qu'au clic.
- Sauvegardes : `pg_dump` quotidien hors du serveur (S3) + sauvegarde
  Saltcorn par tenant (Paramètres → Sauvegarde, planifiable).

## 4. CDN : le plus gros gain pour les landing pages

- Mets Cloudflare (ou équivalent) devant le domaine.
- Fichiers du kit (`/dysizz-ui/a/…`) et de Saltcorn (`/static_assets/…`) :
  déjà servis avec `Cache-Control: immutable` et versionnés. Le CDN les
  garde, le serveur ne les sert qu'une fois.
- **Pages publiques** : Utilisateurs et sécurité → HTTP →
  « Public cache TTL (minutes) ». Ne s'applique qu'aux visiteurs non
  connectés. Mets 5 à 10 min et une règle Cloudflare « Cache Everything »
  sur les chemins des landing pages : des milliers de visiteurs
  = quelques requêtes vers Saltcorn.
  Attention : une page qui contient un formulaire (contact, inscription)
  embarque un jeton CSRF. Garde-la hors cache CDN, ou le formulaire
  échouera pour les visiteurs suivants.

## 5. Sécurité : la liste à cocher

Dans le tenant principal, **Utilisateurs et sécurité → HTTP** :

- [ ] **Force secure cookies = oui**. Indispensable derrière Traefik :
      active aussi `trust proxy`. Sans ça, Saltcorn voit tous les visiteurs
      avec l'IP de Traefik, et la limite de tentatives de connexion
      (100/h par IP) bloque tout le monde d'un coup.
- [ ] **CORS = non**, sauf si une autre application appelle ton API
      depuis un navigateur.
- [ ] **Content Security Policy = Enabled**. Autorise ton domaine,
      Google Fonts et les images `data:`. Conséquence : les images
      externes (picsum, unsplash, liens S3 directs) sont bloquées.
      Téléverse les images dans Saltcorn (Fichiers).
- [ ] **Custom HTTP headers** : 
      `Strict-Transport-Security: max-age=31536000; includeSubDomains`
      et `Permissions-Policy: camera=(), microphone=(), geolocation=()`.
- [ ] Cookie SameSite = Lax (défaut) ; durée de session raisonnable.

Ailleurs :

- [ ] **2FA** obligatoire pour le rôle admin : Utilisateurs et sécurité →
      Rôles → politique 2FA.
- [ ] Longueur minimale des mots de passe ≥ 12, « mots de passe
      courants » refusés (Utilisateurs et sécurité → Paramètres de login).
- [ ] Inscriptions publiques fermées sur les tenants internes.
- [ ] Secrets (SMTP, S3, clés API) **en variables d'environnement /
      secrets Dokploy**, jamais dans une sauvegarde partagée. Ta sauvegarde
      actuelle contient des secrets en clair : change ces mots de passe et
      clés, puis garde les sauvegardes dans un stockage privé.
- [ ] Traefik : limite de débit (middleware `ratelimit`, ex. 50 req/s
      moyenne, rafale 100) et `inFlightReq` par IP sur `/auth/*`.
- [ ] Postgres non exposé sur Internet (réseau Docker interne seulement).
- [ ] Mises à jour : Saltcorn et modules testés sur un tenant de test,
      puis déployés.

## 6. Répartir les SaaS

- Tous les tenants partagent les mêmes conteneurs : c'est efficace tant
  qu'aucun ne domine.
- Un SaaS qui grossit beaucoup → **son propre déploiement** Saltcorn
  (même image, même kit, sa propre base). Le kit s'installe pareil,
  et l'export / import de l'atelier de blocs y amène tes blocs perso.
- Surveille : temps de réponse (Traefik metrics / Uptime Kuma),
  connexions Postgres (`select count(*) from pg_stat_activity`), requêtes
  lentes (`log_min_duration_statement = 500`).

## 7. Ordre conseillé

1. Sécurité du §5 (15 min, sans risque).
2. Cloudflare + cache public des landing pages.
3. Index sur les tables des SaaS.
4. Passage multi-nœud quand un seul conteneur dépasse ~60 % CPU en charge.
