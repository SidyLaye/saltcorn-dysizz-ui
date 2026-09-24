# Faire tenir la charge : Saltcorn en production

Guide vérifié dans le code de Saltcorn 1.6.2. Objectif : plusieurs SaaS
(un tenant chacun), des milliers d'utilisateurs, fluide et sécurisé.

## 1. Ce qui compte vraiment

| Couche | Rôle | Où ça se règle |
|---|---|---|
| Navigateur | fluidité (animations, 1er affichage) | le kit (v2.1+ : fait) |
| Traefik | HTTPS, en-têtes de sécurité, limites de débit (partagées dans Redis) | labels du compose |
| Cache (nginx) | fichiers et pages publiques servis depuis la mémoire | service `cache` du compose |
| Saltcorn | N conteneurs × N workers | variables d'environnement |
| Postgres | le vrai goulot : connexions, index | `postgresql.conf` |
| Fichiers | partagés entre conteneurs | S3 (déjà configuré chez toi) |

Saltcorn 1.6.2 **n'utilise pas Redis** : sessions, synchronisation entre
serveurs et élection du « chef » passent par Postgres, en dur dans le code.
Dans le compose, Redis sert donc là où il est le bon outil : les **limites
de débit de Traefik partagées** entre instances (option `redis` du
middleware `ratelimit`, Traefik ≥ 3.4). Il reste disponible pour tes autres
services (n8n en mode queue…). Le cache HTTP, lui, est un **nginx** en
mémoire devant Saltcorn : c'est l'outil standard pour ça, gratuit, sans
CDN.

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

## 4. Le cache HTTP (sans CDN)

Le service `cache` du compose (nginx, en mémoire) se place entre Traefik et
Saltcorn :

- **Fichiers** (`/static_assets`, `/plugins/public`, `/dysizz-ui/a`) : gardés
  30 jours, servis sans réveiller Saltcorn. Les fichiers du kit sont
  versionnés et marqués `immutable` : les navigateurs ne les redemandent
  même plus. Vérifier : en-tête `X-Cache: HIT` au 2e chargement.
- **Pages publiques** : Saltcorn pose un cookie de session sur **toutes**
  ses réponses, même aux visiteurs anonymes (et crée une ligne de session en
  base à chaque fois). Une page ne peut donc être gardée que si on ignore ce
  cookie, ce qui n'est sûr que pour une page **sans formulaire** (un
  formulaire a besoin de son jeton CSRF lié à la session). Le compose
  contient un exemple commenté (`location = /page/accueil`) : décommente-le
  par landing page, avec 5 min de cache.
- Visiteur connecté (cookie `connect.sid`) : jamais de cache.
- WebSocket (temps réel) : transmis tel quel.
- Plusieurs nœuds : nginx résout le nom `saltcorn` toutes les 10 s et
  répartit entre `primary` et toutes les copies de `web`.

Les sessions anonymes s'accumulent dans `_sc_session` : garde
« Prune session interval » (Utilisateurs et sécurité → HTTP) actif.

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

## 6. À vérifier sur ton instance : les transactions

Ton application racine est servie sur `web.allinone.ovh` alors que le
multi-tenant est actif. Saltcorn lit alors « web » comme nom de tenant ; ce
tenant n'existe pas, et sur les requêtes HTTP **les transactions ne
s'appliquent pas** (un `tryCatchInTransaction` n'annule rien, un
`forupdate` ne verrouille rien). Tout le reste marche, d'où l'invisibilité.
Les tâches de fond ne sont pas touchées.

Solutions en gardant le multi-tenant : servir la racine sur le domaine de
base (`allinone.ovh`), ou créer un vrai tenant `web` et y restaurer
l'application. Sonde de 30 secondes (déclencheur `run_js_code`, lancé par
« Test run ») :

```js
let id = null;
await tryCatchInTransaction(async () => {
  const p = await MetaData.create({ name: "probe_" + Date.now(), type: "probe", user_id: user.id, body: {} });
  id = p.id;
  throw new Error("rollback");
}, () => {});
const reste = await MetaData.findOne({ id });
if (reste) await reste.delete();
return { host: request_headers?.host, transaction_active: !reste };
```

`transaction_active: false` confirme le problème.

## 7. Monter de version

- Saltcorn 1.7 supprime l'authentification JWT (`SALTCORN_JWT_SECRET`
  devient inutile) et passe une grande partie du code en TypeScript / ESM :
  tester d'abord sur une instance jetable restaurée depuis une sauvegarde.
- Une version mineure à la fois ; désinstaller les modules inutilisés avant.
- Le kit : `index.js` est reconstruit par la CI à chaque changement ; mettre
  à jour le module, puis « Installer / mettre à jour » sur `/dysizz-ui`.

## 8. Répartir les SaaS

- Tous les tenants partagent les mêmes conteneurs : c'est efficace tant
  qu'aucun ne domine.
- Un SaaS qui grossit beaucoup → **son propre déploiement** Saltcorn
  (même image, même kit, sa propre base). Le kit s'installe pareil,
  et l'export / import de l'atelier de blocs y amène tes blocs perso.
- Surveille : temps de réponse (Traefik metrics / Uptime Kuma),
  connexions Postgres (`select count(*) from pg_stat_activity`), requêtes
  lentes (`log_min_duration_statement = 500`).

## 9. Ordre conseillé

1. Sécurité du §5 (15 min, sans risque).
2. Service `cache` + Redis (compose) ; cache des landing pages sans formulaire.
3. Index sur les tables des SaaS.
4. Passage multi-nœud quand un seul conteneur dépasse ~60 % CPU en charge.
