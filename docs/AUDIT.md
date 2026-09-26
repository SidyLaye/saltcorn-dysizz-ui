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

| # | Constat | Où |
|---|---|---|
| F1 | **La CI est rouge sur `main` dans les trois dépôts.** Aucune version récente n'a passé la CI. | GitHub Actions, derniers runs du 2026-09-25 |
| F2 | ui : le fichier de CI est du YAML invalide, donc la CI n'a jamais tourné (runs de 0 s). En cause : `: ` dans une commande non entre guillemets. | `dysizz-ui/.github/workflows/ci.yml:29` |
| F3 | flow : la CI construit depuis `tools/`, ce qui écrit `../src/…` dans les commentaires de `index.js`. Le fichier commité a été construit depuis la racine (`src/…`), donc le contrôle « index.js est à jour » échoue toujours. Reproduit : 0 écart depuis la racine, 1 218 lignes d'écart depuis `tools/`. | `dysizz-flow/.github/workflows/ci.yml` (étape `node build.mjs`, `working-directory: tools`) |
| F4 | me : `docs/MODULES.md` commité est en retard sur le code (la gestion `flux` du module veille n'y est pas), donc le contrôle `git diff` échoue. | `dysizz-me/docs/MODULES.md`, `dysizz-me/tools/gen-docs.cjs` |
| F5 | L'instance principale fait tourner des versions anciennes : ui 3.3.0, flow 2.0.0, me 2.0.0, alors que les dépôts sont en 3.6.2 / 2.4.0 / 2.2.1. | `pack.json` → `plugins` de la sauvegarde |
| F6 | Des versions plus récentes existent **seulement sur le PC** de Sidy (flow 2.5.0 et 2.6.0, plugin `dysizz-leads` 1.2.0), jamais poussées. Travailler dans ces dépôts avant de les pousser écraserait ce travail. | rapport de la session Cowork du 2026-09-25 |
| F7 | `dysizz-flow` donne à tout administrateur de tenant des pouvoirs sur le serveur entier : lecture de n'importe quelle variable d'environnement par son nom (`engine.js:113-118`, `expose.js:43`) et évaluation de JavaScript hors bac à sable (`blocks/transformer.js:8`). Sans risque si Sidy est le seul admin de tous les tenants ; bloquant sinon (voir Q1). | cités |
| F8 | Le kit exige *Install git plugins* pour les tenants (`README.md` §1.b). Saltcorn le refuse par défaut aux tenants : un plugin GitHub est du code arbitraire exécuté sur le serveur (`@saltcorn/server` 1.6.2, `routes/plugins.js:196-202`). | cités |
| F9 | `npm test` (dans `tools/`) pointe vers `tests/run.mjs`, qui n'existe pas dans flow ni dans ui. Les vrais points d'entrée sont `tests/run.cjs` (flow) et les commandes de la CI (ui). | `dysizz-flow/tools/package.json`, `dysizz-ui/tools/package.json` |

## QUESTIONS

1. **Les administrateurs de tenant seront-ils toujours toi ?** Ou un client, un
   associé, un utilisateur de SaaS pourra-t-il un jour être admin de son tenant ?
   La réponse décide de F7 et F8 : soit la confiance reste totale (et on le
   documente), soit flow doit se cloisonner (liste blanche de variables, formules
   en bac à sable, fonctions sensibles réservées au tenant racine) et les plugins
   passent par npm plutôt que *Install git plugins*.
2. La sauvegarde contient deux fois les pages `accueil` et `dysizz-accueil` et
   la vue `accueil_chiffres`, avec un contenu identique. Doublon en base, ou
   artefact de l'export ? (Voir H1.)
3. Le workflow `test` (vide, ouvert au public) et les 20 pages `dz-demo-*` /
   `dz-famille-*` : à garder sur l'instance principale, ou à réserver au tenant
   « modele » ?

## HYPOTHÈSES

| # | Hypothèse | Pour trancher |
|---|---|---|
| H1 | Les doublons de Q2 viennent de l'export et pas de la base. | `select name, count(*) from _sc_pages group by 1 having count(*)>1;` |
| H2 | ui : l'`index.js` commité n'est peut-être pas reproductible non plus (même mécanisme que F3), le constat restera caché tant que F2 n'est pas corrigé. | corriger F2, relancer la CI |

## Passes faites / non faites

- **Faites** : inventaire, sécurité (routes, secrets, exécution de code), tests
  et CI, sauvegarde de l'instance, exploitation (rapport privé).
- **Partielles** : architecture (vue d'ensemble, pas chaque bloc), backend
  (délais et reprises vus sur l'API et le moteur, pas bloc par bloc), données
  (tables de la sauvegarde, pas le schéma réel).
- **Non faites** : frontend et UI/UX. Il faut rendre les 390 blocs et les
  vues sur mobile et desktop (`tools/preview.mjs all`), ce qui dépend de F2.
