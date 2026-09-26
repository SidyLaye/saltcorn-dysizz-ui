# Audit de la base Dysizz — 2026-09-26

Portée : les trois dépôts (`dysizz-ui` 3.6.2, `dysizz-flow` 2.4.0, `dysizz-me` 2.2.1),
une sauvegarde de l'instance principale et son déploiement.

**Les dépôts sont publics.** Les constats de sécurité et d'exploitation qui
concernent une instance réelle (serveur, secrets, réglages) sont dans un rapport
**privé**, hors dépôt. Ici ne figure que ce qui est sans risque à publier.

Classement : **FAIT** (vérifié, avec citation) · **QUESTION** (peut être voulu) ·
**HYPOTHÈSE** (déduit, à vérifier).

## Ce qui est solide

- Build reproductible en un seul fichier `index.js` par plugin, vérifié par la CI
  (`tools/build.mjs`, `.github/workflows/ci.yml` des trois dépôts).
- Toutes les routes d'administration des trois plugins vérifient le rôle admin
  (`dysizz-flow/src/admin.js`, `admin2.js`, `editor.js:185-276` ;
  `dysizz-ui/src/admin/*.js` ; `dysizz-me/src/admin.js:20-176`).
- Points d'API publics bien protégés : nom filtré, limite par IP, corps limité à 1 Mo,
  comparaison en temps constant, anti-CSRF par en-tête et origine
  (`dysizz-flow/src/expose.js:17-100`).
- Coffre de secrets en AES-256-GCM, clé hors base (`dysizz-flow/src/vault.js:10-27`).
- `dysizz-me` vérifie la présence des blocs dont il dépend plutôt qu'un numéro de
  version (`dysizz-me/src/installer.js:119-132`).
- Tests locaux verts le 2026-09-26 : flow (201 blocs, 36 routes), me (13 modules,
  24 tables, 68 vues, 15 pages, 17 workflows, 228 champs).

## FAITS

Statut au 2026-09-26 sur la branche `claude/trusting-rubin-0sgk9q` (PR #1 de chaque dépôt).

| # | Constat | Où | Statut |
|---|---|---|---|
| F1 | **La CI était rouge sur `main` dans les trois dépôts.** | GitHub Actions, runs du 2026-09-25 | ✅ verte sur la branche (flow, me ; ui en cours) |
| F2 | ui : fichier de CI en YAML invalide (`: ` dans une commande non entre guillemets), donc la CI n'avait jamais tourné. | `.github/workflows/ci.yml:29` | ✅ corrigé |
| F3 | flow : la CI construisait depuis `tools/`, ce qui écrivait `../src/…` dans `index.js` (1 218 lignes d'écart), donc « index.js est à jour » échouait toujours. | `tools/build.mjs` | ✅ `absWorkingDir` : même résultat d'où qu'on lance (flow et me) |
| F4 | me : `docs/MODULES.md` commité en retard sur le code. | `dysizz-me/docs/MODULES.md` | ✅ régénéré |
| F5 | L'instance principale fait tourner ui 3.3.0, flow 2.0.0, me 2.0.0. | sauvegarde, `pack.json` → `plugins` | ⏳ mise à jour à faire sur l'instance (`docs/DEMARRAGE.md` §4) |
| F6 | Des versions plus récentes existent **seulement sur le PC** de Sidy (flow 2.5.0 / 2.6.0, `dysizz-leads` 1.2.0), jamais poussées. | session Cowork du 2026-09-25 | ⏳ à pousser par Sidy ; la fusion avec 2.4.1 se fera au moment du push |
| F7 | flow donnait à tout admin de tenant des pouvoirs sur le serveur : lecture de n'importe quelle variable d'environnement (y compris le mot de passe de la base) et JavaScript hors bac à sable. | `engine.js`, `expose.js`, `blocks/transformer.js`, `blocks/controle.js` | ✅ flow 2.4.1 : `src/garde.js`, testé (`tests/garde.test.cjs`) |
| F8 | Le kit demande *Install git plugins* pour les tenants ; Saltcorn le refuse par défaut (un plugin GitHub est du code exécuté sur le serveur). | `README.md` §1.b ; `@saltcorn/server` 1.6.2 `routes/plugins.js:196-202` | ✅ documenté (à décocher avant de confier un tenant) et signalé par la page Santé |
| F9 | `npm test` pointait vers `tests/run.mjs`, absent (flow, ui). | `tools/package.json` | ✅ corrigé |
| F10 | Le contrôle visuel rendait **tout en 1280 px**, y compris la variante « mobile » : `BrowserContext.newPage()` n'accepte pas d'options. Le contrôle « déborde sur mobile » n'avait donc jamais rien pu détecter. | `tools/preview.mjs:70` | ✅ `setViewportSize` avant le chargement |
| F11 | Le contrôle visuel ne démarrait jamais les 10 widgets interactifs (3D, carte, Gantt, tableur, jeux…) : `window.__dzFam` absent. | `tools/preview.mjs` | ✅ réglé comme sur le site |
| F12 | **Trois effets ne marchaient pas sur le site** : le marqueur « déjà initialisé » portait le nom de l'attribut de réglage. Texte qui s'écrit : jamais animé, et « mot 1 \| mot 2 \| mot 3 » affiché en entier dans les blocs du builder (hero 400 px trop haut). Bouton Copier : copiait « 1 » ou ne réagissait pas. Effet 3D : angle ramené à 1° ou jamais démarré. | `client/dz.js` (`once`) | ✅ clés `…Init` ; test navigateur qui échoue sur l'ancien code (`tests/dz-client.test.mjs`) |
| F13 | 6 blocs flottants (bandeau cookies, palette Ctrl K, onglets du bas, barre de lecture, réglages de page, bulle de chat) signalés à tort « invisibles ». | `tools/preview.mjs` | ✅ le contrôle les photographie ou les reconnaît |
| F14 | Réglages Saltcorn ouverts par défaut : CORS actif, cookies non sécurisés derrière un proxy (et donc IP des visiteurs inconnue), pas de 2FA, pas de sauvegarde. | `@saltcorn/data` 1.6.2 `models/config.js` ; `@saltcorn/server` `app.js:123-157` | ✅ page Santé (`/dysizz/sante`) : diagnostic et correction avec aperçu |
| F15 | Pages et vues en double sur l'instance (`accueil`, `dysizz-accueil`, `accueil_chiffres`). Saltcorn n'impose pas de nom unique (`_sc_pages` : aucune contrainte) et nos installateurs vérifiaient « existe déjà ? » dans le cache du processus, parfois en retard. | `@saltcorn/data` migrations `202006240906` ; `dysizz-me/src/installer.js`, `dysizz-ui/src/hub.js` | ✅ vérification en base avant création (me 2.2.2, ui 3.7.0) ; la page Santé détecte les doublons et retire les copies identiques après aperçu |
| F16 | Débordement horizontal sur mobile : les textes pour lecteurs d'écran (`.visually-hidden`, absolute sans top/left) dans une zone qui défile élargissaient toute la page. | `styles/14-utilitaires.css`, `styles/44-app-plus.css` | ✅ ancrés à leur bloc conteneur |

## QUESTIONS

1. ~~**Les administrateurs de tenant seront-ils toujours toi ?**~~ *Tranché par défaut le
   2026-09-26 (voir DECISIONS) : on cloisonne, ça marche dans les deux cas.* Ou un client, un
   associé, un utilisateur de SaaS pourra-t-il un jour être admin de son tenant ?
   La réponse décide de F7 et F8 : soit la confiance reste totale (et on le
   documente), soit flow doit se cloisonner (liste blanche de variables, formules
   en bac à sable, fonctions sensibles réservées au tenant racine) et les plugins
   passent par npm plutôt que *Install git plugins*.
2. ~~Doublons en base ou artefact de l'export ?~~ *Très probablement en base (voir
   F15). La page Santé le dira sur l'instance et les retirera.*
3. ~~Workflow `test` et pages de démo~~ *Tranché par défaut : les pages de démo sont
   réservées à l'admin, sans risque ; le workflow `test` ouvert au public est signalé
   par la page Santé, qui le repasse en admin après aperçu.*

## HYPOTHÈSES

| # | Hypothèse | Pour trancher |
|---|---|---|
| H1 | Les doublons de Q2 viennent de l'export et pas de la base. | `select name, count(*) from _sc_pages group by 1 having count(*)>1;` |
| H2 | ~~ui : l'`index.js` commité n'est peut-être pas reproductible.~~ **Écartée** : reconstruit à l'identique, avec et sans Pillow. | — |

## Passes faites / non faites

- **Faites** : inventaire, sécurité (routes, secrets, exécution de code), tests
  et CI, sauvegarde de l'instance, exploitation (rapport privé).
- **Partielles** : architecture (vue d'ensemble, pas chaque bloc), backend
  (délais et reprises vus sur l'API et le moteur, pas bloc par bloc), données
  (tables de la sauvegarde, pas le schéma réel).
- **Faite le 2026-09-26** : rendu des 411 blocs en clair, sombre et mobile 390 px, widgets
  démarrés (`tools/preview.mjs all`), après correction de l'outil lui-même (F10, F11, F13).
- **Non faite** : relecture esthétique bloc par bloc (hiérarchie, rythme, cohérence entre
  familles) sur les planches `build/preview/*.png`.
