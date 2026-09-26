# Mettre une instance Dysizz en sécurité, pas à pas

Pour quelqu'un qui n'est pas développeur. Compte une heure la première fois.
Chaque étape dit **où cliquer** et **comment vérifier** que c'est bon.

Ce que la machine fait toute seule est dans la page **Santé et sécurité** du kit
(`/dysizz/sante`). Ce guide couvre le reste : ce qui se passe hors de Saltcorn
(serveur, Dokploy, mots de passe) et que personne ne peut faire à ta place.

---

## 1. Changer les secrets qui ont circulé (15 min)

Un secret qui a été collé dans une conversation, un e-mail, une capture ou une
sauvegarde partagée est à considérer comme connu. On le remplace.

Génère chaque nouvelle valeur ainsi (terminal du serveur ou ton PC) :

```bash
openssl rand -base64 48 | tr -d '/+=' | cut -c1-48
```

Dans l'ordre, du plus grave au moins grave :

| Secret | Où le changer | Effet |
|---|---|---|
| `SALTCORN_SESSION_SECRET` | Dokploy → ton service → **Environment**, puis **Redeploy** | Tout le monde est déconnecté, c'est normal. |
| Mot de passe de la boîte mail (`DZ_MAIL_PASSWORD`, SMTP) | D'abord chez l'hébergeur de la boîte (OVH…), puis dans Dokploy et dans Saltcorn → Paramètres → E-mail | Envoie un e-mail de test depuis cette page. |
| Clés S3, clés d'API (IA, CRM…) | Chez le fournisseur (révoquer l'ancienne), puis dans le coffre `/dysizz-flow/coffre` | L'ancienne clé ne marche plus nulle part. |
| `REDIS_PASSWORD` | Dokploy → Environment, puis Redeploy | Rien de visible. |
| `POSTGRES_PASSWORD` | **Attention**, voir juste en dessous | Rien de visible si c'est fait dans l'ordre. |

**Postgres** : la base garde l'ancien mot de passe tant qu'on ne le change pas
dedans. Changer seulement Dokploy empêcherait Saltcorn de démarrer. Dans l'ordre :

```bash
docker exec -it saltcorn-db psql -U postgres -c "ALTER USER postgres PASSWORD 'NOUVELLE_VALEUR';"
```

puis mettre la même valeur dans Dokploy → Environment, puis Redeploy.

**La clé du coffre (`DZF_CLE_COFFRE`)** : ne la change pas à la légère, elle
chiffre les secrets rangés dans le coffre. Pour la changer : note d'abord les
secrets du coffre, change la clé, redéploie, puis range-les à nouveau.
Dans tous les cas, **garde-la hors du serveur** (gestionnaire de mots de passe) :
sans elle, les secrets du coffre sont perdus.

✅ Vérifier : tu te reconnectes, un e-mail de test part, la page Santé ne signale
plus « Clé du coffre ».

## 2. Mettre Dokploy en HTTPS (10 min)

Si l'adresse de ton panneau Dokploy est une IP avec `:3000` et que le navigateur
dit « Non sécurisé », ton mot de passe Dokploy passe en clair sur le réseau. Or
Dokploy contrôle tout le serveur.

1. Crée un sous-domaine pour le panneau (ex. `panel.ton-domaine`) qui pointe vers le serveur.
2. Dokploy → **Settings → Web Server** → Domain : ce sous-domaine, **HTTPS** avec Let's Encrypt.
3. Ouvre le panneau par cette adresse, vérifie le cadenas.
4. Ensuite seulement, ferme l'accès direct au port 3000 avec le **pare-feu de ton
   hébergeur** (ex. Hetzner Cloud → Firewalls : n'autoriser que 22, 80 et 443).
   Un `ufw` sur le serveur ne suffit pas : Docker le contourne pour les ports qu'il publie.
5. Si ta version de Dokploy le propose (Profile), active la double authentification.

✅ Vérifier : `http://IP:3000` ne répond plus, `https://panel.ton-domaine` affiche le cadenas.

## 3. Sauvegardes qui survivent à la mort du serveur (15 min)

1. Saltcorn → **Paramètres → Sauvegarde** :
   - **Backup password** : un mot de passe long, gardé hors du serveur. Les sauvegardes
     contiennent des mots de passe en clair, chiffrées elles ne servent à rien à un voleur.
   - **Auto backup frequency** : Daily.
   - **Destination** : S3 (ou SFTP), **pas** « Saltcorn files » qui reste sur le même serveur.
2. Dokploy → ton service → **Volume Backups** : planifie aussi la sauvegarde du volume
   Postgres vers un stockage externe.
3. **Une fois par mois**, restaure la dernière sauvegarde sur une instance jetable et
   ouvre deux ou trois pages. Une sauvegarde jamais restaurée ne compte pas.

✅ Vérifier : la page Santé dit « Sauvegardes automatiques : Daily, vers S3 » et
« Sauvegardes chiffrées ».

## 4. Faire tourner les dernières versions (5 min)

1. Si tu as travaillé sur ton PC, **pousse tout** avant d'installer quoi que ce soit :
   dans chaque dossier de plugin, `git status` puis `git push`.
2. Saltcorn → **Paramètres → Modules** → pour `dysizz-ui`, `dysizz-flow`, `dysizz-me` :
   **Upgrade** ou **Reload** selon ce que propose la ligne du module.
3. Ouvre `/dysizz-ui` et clique « Installer / mettre à jour » pour rafraîchir les blocs.

✅ Vérifier : la page Santé, carte « Versions installées », affiche les bons numéros.

## 5. Passer la page Santé au vert (10 min)

Ouvre `/dysizz/sante` dans **chaque tenant**. Pour chaque carte rouge ou orange :

- bouton **« Voir ce qui va changer »** : rien n'est encore modifié, lis l'aperçu ;
- bouton **« Appliquer »** si l'aperçu te convient ;
- sinon suis la marche à suivre affichée sur la carte.

Deux réglages ne prennent effet qu'après un **Redeploy** dans Dokploy : cookies
sécurisés et CORS. Applique-les, puis redéploie une fois pour les deux.

Pour la double authentification : garde ton téléphone à portée, un QR code
s'affichera à la connexion suivante.

## 6. Avant de confier un tenant à quelqu'un d'autre

Tant que tu es le seul administrateur de tous les tenants, tout va bien. Le jour
où un client, un associé ou l'utilisateur d'un SaaS devient **admin** d'un tenant :

- dans le tenant racine, **Paramètres → Multitenancy**, décoche *Install git plugins* ;
- installe les plugins Dysizz depuis npm plutôt que GitHub ;
- sur le serveur, ne mets dans `DZF_ENV_PARTAGEES` que les variables que tous les
  tenants peuvent lire (jamais un mot de passe à toi) ; chaque tenant range ses
  propres secrets dans son coffre `/dysizz-flow/coffre`.

dysizz-flow 2.4.1 et plus empêche déjà un admin de tenant de lire les secrets du
serveur ou d'exécuter du code hors du bac à sable. Ces trois réglages ferment le reste.
