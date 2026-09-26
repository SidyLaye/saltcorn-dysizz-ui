/* dysizz-ui — /dysizz/sante : santé et sécurité du tenant, en feux tricolores.
   Chaque point dit en mots simples ce qui ne va pas et pourquoi c'est important.
   Quand une correction est sûre, elle se fait en deux temps : « Voir ce qui va
   changer » (rien n'est écrit), puis « Appliquer ». Sinon, la marche à suivre.
   Réglages et comportements vérifiés dans le code de Saltcorn 1.6.2. */
"use strict";
const { isAdmin, esc, denied, post, VERSION } = require("../core");

const state = () => require("@saltcorn/data/db/state").getState();
const db = () => require("@saltcorn/data/db");
const cfg = (k, d) => { try { const v = state().getConfig(k, d); return v === undefined ? d : v; } catch (e) { return d; } };
const estRacine = () => { try { return db().getTenantSchema() === db().connectObj.default_schema; } catch (e) { return false; } };
const multiTenant = () => { try { return !!db().is_it_multi_tenant(); } catch (e) { return false; } };
const setConfig = (k, v) => state().setConfig(k, v);
const liste = (xs, max = 12) => `<ul class="dzs-liste">${xs.slice(0, max).map((x) => `<li>${x}</li>`).join("")}${xs.length > max ? `<li>… et ${xs.length - max} autres</li>` : ""}</ul>`;

const EN_TETES = [
  "Strict-Transport-Security: max-age=31536000; includeSubDomains",
  "X-Content-Type-Options: nosniff",
  "Referrer-Policy: strict-origin-when-cross-origin",
  "Permissions-Policy: camera=(self), microphone=(self), geolocation=(self)",
];

/* noms en double parmi les pages et les vues (lus en base, pas dans le cache) ;
   « identiques » quand toutes les copies ont le même contenu */
const doublons = async () => {
  const Page = require("@saltcorn/data/models/page"), View = require("@saltcorn/data/models/view");
  const out = [];
  const grouper = (type, lignes, contenu) => {
    const par = new Map();
    for (const l of lignes) { if (!par.has(l.name)) par.set(l.name, []); par.get(l.name).push(l); }
    for (const [nom, ls] of par) if (ls.length > 1) {
      ls.sort((a, b) => (+a.id || 0) - (+b.id || 0));
      out.push({ type, nom, lignes: ls, identiques: ls.every((l) => JSON.stringify(contenu(l)) === JSON.stringify(contenu(ls[0]))) });
    }
  };
  grouper("page", await Page.find({}), (p) => [p.title, p.min_role, p.layout, p.fixed_states]);
  grouper("vue", await View.find({}), (v) => [v.viewtemplate, v.table_id, v.min_role, v.configuration]);
  return out;
};

/* ---------- les vérifications ----------/* ---------- les vérifications ----------
   Chaque vérification renvoie { etat: "ok" | "ko" | "info", ... } ou null (sans objet ici).
   gravite : critique > important > conseil. */
const VERIFS = [
  {
    id: "2fa", gravite: "critique", titre: "Double authentification des administrateurs",
    pourquoi: "Un mot de passe seul se vole (fuite, hameçonnage, logiciel espion). Avec la double authentification, il faut aussi ton téléphone : un voleur de mot de passe reste dehors.",
    verifier: () => {
      const p = cfg("twofa_policy_by_role", {}) || {};
      return p[1] === "Mandatory" ? { etat: "ok", dit: "Obligatoire pour le rôle admin." } : { etat: "ko", dit: `Rôle admin : ${esc(p[1] || "Optional")} (non obligatoire).` };
    },
    correction: {
      quoi: () => `Politique 2FA du rôle admin : ${esc((cfg("twofa_policy_by_role", {}) || {})[1] || "Optional")} → <b>Mandatory</b>.`,
      attention: "À ta prochaine connexion, Saltcorn affichera un QR code : scanne-le avec une appli d'authentification (Google Authenticator, Microsoft Authenticator, Authy…). Garde ton téléphone à portée.",
      appliquer: async () => { const p = { ...(cfg("twofa_policy_by_role", {}) || {}) }; p[1] = "Mandatory"; await setConfig("twofa_policy_by_role", p); },
    },
  },
  {
    id: "inscriptions", gravite: "important", titre: "Inscriptions ouvertes à tout le monde",
    pourquoi: "Si l'inscription est ouverte, n'importe qui peut se créer un compte et voir ce que le rôle « user » voit. Utile pour un SaaS public, dangereux pour un outil interne ou perso.",
    verifier: () => (cfg("allow_signup", true) ? { etat: "ko", dit: "N'importe qui peut créer un compte." } : { etat: "ok", dit: "Fermées : seuls les comptes que tu crées existent." }),
    correction: {
      quoi: () => "Inscriptions : ouvertes → <b>fermées</b>. Les comptes existants ne changent pas.",
      attention: "Pour un SaaS où les clients s'inscrivent seuls, laisse ouvert et active plutôt la vérification de l'e-mail (Utilisateurs et sécurité → Paramètres).",
      appliquer: () => setConfig("allow_signup", false),
    },
  },
  {
    id: "mots_de_passe", gravite: "important", titre: "Mots de passe solides",
    pourquoi: "Un mot de passe court ou très courant (« azerty123 ») se devine en quelques minutes par un robot.",
    verifier: () => {
      const n = +cfg("min_password_length", 8) || 8, c = !!cfg("check_common_passwords", false);
      return n >= 12 && c ? { etat: "ok", dit: `${n} caractères minimum, mots de passe courants refusés.` } : { etat: "ko", dit: `${n} caractères minimum${c ? "" : ", mots de passe courants acceptés"}.` };
    },
    correction: {
      quoi: () => `Longueur minimale : ${+cfg("min_password_length", 8) || 8} → <b>12</b> ; mots de passe courants : <b>refusés</b>. Seuls les nouveaux mots de passe sont concernés.`,
      appliquer: async () => { if ((+cfg("min_password_length", 8) || 8) < 12) await setConfig("min_password_length", 12); await setConfig("check_common_passwords", true); },
    },
  },
  {
    id: "sauvegardes", gravite: "critique", titre: "Sauvegardes automatiques",
    pourquoi: "Sans sauvegarde, une panne de disque, une fausse manipulation ou un piratage efface tout, définitivement. Une sauvegarde doit être automatique, hors du serveur, et testée.",
    verifier: () => {
      const f = cfg("auto_backup_frequency", "Never"), d = cfg("auto_backup_destination", "Saltcorn files");
      if (!f || f === "Never") return { etat: "ko", dit: "Aucune sauvegarde automatique." };
      if (d === "Saltcorn files") return { etat: "ko", gravite: "important", dit: `${esc(f)}, mais gardée <b>sur le même serveur</b> : si le serveur meurt, les sauvegardes aussi.`, manuel: "Dans Paramètres → Sauvegarde, choisis une destination hors du serveur (S3, SFTP)." };
      return { etat: "ok", dit: `${esc(f)}, vers ${esc(d)}.` };
    },
    correction: {
      si: () => { const f = cfg("auto_backup_frequency", "Never"); return !f || f === "Never"; },
      quoi: () => "Sauvegarde automatique : jamais → <b>chaque jour</b> (dans les fichiers Saltcorn).",
      attention: "C'est un premier filet. Ensuite, dans Paramètres → Sauvegarde, envoie-les hors du serveur (S3 ou SFTP) et restaure-en une une fois sur une instance de test : une sauvegarde jamais restaurée ne compte pas.",
      appliquer: () => setConfig("auto_backup_frequency", "Daily"),
    },
    lien: "/admin/backup",
  },
  {
    id: "sauvegardes_chiffrees", gravite: "important", titre: "Sauvegardes chiffrées",
    pourquoi: "Une sauvegarde Saltcorn contient les mots de passe des réglages en clair (SMTP, S3…). Chiffrée, elle ne sert à rien à celui qui la trouve.",
    verifier: () => (cfg("backup_password", "") ? { etat: "ok", dit: "Les sauvegardes sont chiffrées." } : { etat: "ko", dit: "Les sauvegardes ne sont pas chiffrées." }),
    manuel: "Paramètres → Sauvegarde → « Backup password ». Choisis un mot de passe long et garde-le hors du serveur (gestionnaire de mots de passe) : sans lui, impossible de restaurer.",
    lien: "/admin/backup",
  },
  {
    id: "smtp", gravite: "important", titre: "Envoi des e-mails chiffré",
    pourquoi: "Sur le port 25 sans chiffrement, ton mot de passe de messagerie et le contenu des e-mails peuvent circuler en clair.",
    verifier: () => {
      const h = cfg("smtp_host", ""), p = +cfg("smtp_port", 25), s = !!cfg("smtp_secure", false);
      if (!h) return null;
      if (p === 465 && s) return { etat: "ok", dit: `${esc(h)}, port 465 (TLS).` };
      if (p === 587 && !s) return { etat: "ok", dit: `${esc(h)}, port 587 (STARTTLS).` };
      if (p === 465) return { etat: "ko", dit: "Port 465 sans « Force TLS » : l'envoi échouera ou restera en clair." };
      return { etat: "ko", dit: `${esc(h)}, port ${p}${s ? " avec TLS forcé" : ""}.` };
    },
    manuel: "Paramètres → E-mail : port <b>465</b> avec « Force TLS » coché (OVH : ssl0.ovh.net), ou port <b>587</b> sans le cocher. Puis envoie un e-mail de test depuis la même page.",
    lien: "/admin/email",
  },
  {
    id: "ecriture_publique", gravite: "critique", titre: "Données modifiables par des inconnus",
    pourquoi: "Rôle 100 = public (tout internet). Une table ou une vue d'édition ouverte en écriture au public laisse n'importe qui ajouter, modifier ou effacer tes données.",
    verifier: async () => {
      const Table = require("@saltcorn/data/models/table"), View = require("@saltcorn/data/models/view");
      const t = (await Table.find({})).filter((x) => +x.min_role_write >= 100 && !x.external && x.name !== "users");
      const v = (await View.find({})).filter((x) => +x.min_role >= 100 && x.viewtemplate === "Edit");
      if (!t.length && !v.length) return { etat: "ok", dit: "Aucune table ni vue d'édition n'est modifiable par le public." };
      return { etat: "ko", dit: `À vérifier : ${t.length} table(s), ${v.length} vue(s) d'édition.` + liste([...t.map((x) => `table <a href="/table/${x.id}">${esc(x.name)}</a>`), ...v.map((x) => `vue <a href="/viewedit/config/${encodeURIComponent(x.name)}">${esc(x.name)}</a>`)]) };
    },
    manuel: "Un formulaire public (contact, inscription à une liste) peut être voulu. Sinon, ouvre chaque élément et passe son rôle à « user » (80) ou « admin » (1).",
  },
  {
    id: "declencheurs_publics", gravite: "important", titre: "Actions lançables par des inconnus",
    pourquoi: "Un déclencheur ou workflow en rôle 100 peut être lancé par n'importe qui via l'adresse /api/action/… : envois d'e-mails, écritures, appels payants.",
    verifier: async () => {
      const Trigger = require("@saltcorn/data/models/trigger");
      const t = (await Trigger.find({})).filter((x) => +x.min_role >= 100);
      return t.length ? { etat: "ko", dit: `${t.length} action(s) ouverte(s) au public :` + liste(t.map((x) => `<a href="/actions/edit/${x.id}">${esc(x.name)}</a> <small>(${esc(x.when_trigger || "")})</small>`)) } : { etat: "ok", dit: "Aucune action n'est lançable par le public." };
    },
    correction: {
      quoi: async () => { const Trigger = require("@saltcorn/data/models/trigger"); const t = (await Trigger.find({})).filter((x) => +x.min_role >= 100); return `Rôle de ${t.length} action(s) : public → <b>admin</b> :` + liste(t.map((x) => esc(x.name)), 30); },
      attention: "Si une page publique utilise l'une de ces actions (un bouton « S'abonner » par exemple), elle ne marchera plus pour les visiteurs : remets-la en public à la main.",
      appliquer: async () => { const Trigger = require("@saltcorn/data/models/trigger"); for (const x of (await Trigger.find({})).filter((y) => +y.min_role >= 100)) await Trigger.update(x.id, { min_role: 1 }); },
    },
  },
  {
    id: "doublons", gravite: "important", titre: "Pages ou vues en double",
    pourquoi: "Saltcorn accepte deux pages ou deux vues du même nom. Laquelle s'affiche devient imprévisible : tu modifies l'une, le site montre l'autre.",
    verifier: async () => {
      const g = await doublons();
      const n = g.length;
      if (!n) return { etat: "ok", dit: "Aucun nom en double." };
      const auto = g.filter((x) => x.identiques).length;
      return { etat: "ko", dit: `${n} nom(s) en double${auto < n ? ` (${n - auto} avec des contenus différents : à trier à la main)` : ""} :` + liste(g.map((x) => `${x.type} <b>${esc(x.nom)}</b> × ${x.lignes.length}${x.identiques ? " (copies identiques)" : " (contenus différents)"}`)), manuel: auto < n ? "Pour les contenus différents : ouvre chaque copie, garde la bonne, supprime l'autre." : undefined };
    },
    correction: {
      si: async () => (await doublons()).some((x) => x.identiques),
      quoi: async () => "Copies identiques retirées, la plus ancienne est gardée (les liens, menus et pages d'accueil par nom continuent de marcher) :" + liste((await doublons()).filter((x) => x.identiques).map((x) => `${x.type} <b>${esc(x.nom)}</b> : ${x.lignes.length - 1} copie(s) en moins`), 30),
      attention: "Les copies aux contenus différents ne sont pas touchées.",
      appliquer: async () => { for (const x of (await doublons()).filter((y) => y.identiques)) for (const r of x.lignes.slice(1)) await r.delete(); },
    },
  },
  {
    id: "transactions", gravite: "critique", titre: "Transactions de la base de données",
    pourquoi: "Une transaction garantit « tout ou rien » : si une étape échoue, rien n'est à moitié écrit. Si elles ne marchent pas, un paiement, un stock ou un compteur peut rester incohérent sans message d'erreur.",
    verifier: async (req) => {
      const d = db();
      if (typeof d.withTransaction !== "function") return null;
      const MetaData = require("@saltcorn/data/models/metadata");
      let id = null;
      try { await d.withTransaction(async () => { const m = await MetaData.create({ type: "dz_sonde", name: `sonde_${Date.now()}`, user_id: req.user && req.user.id, body: {}, written_at: new Date() }); id = m.id; throw new Error("annulation voulue"); }); } catch (e) { /* attendu */ }
      const reste = id ? await MetaData.findOne({ id }) : null;
      if (reste) { await reste.delete(); }
      if (!reste) return { etat: "ok", dit: "Testé à l'instant : une écriture annulée a bien disparu." };
      const sous = (req.subdomains || []).join(".");
      return {
        etat: "ko",
        dit: `Testé à l'instant : une écriture qui devait être annulée est restée.${multiTenant() && estRacine() && sous ? ` Cause probable : le site principal est servi sur le sous-domaine <b>${esc(sous)}</b> alors que le multi-tenant est actif ; Saltcorn prend « ${esc(sous)} » pour un nom de tenant qui n'existe pas.` : ""}`,
        manuel: "Servir le tenant principal sur le domaine de base, ou faire de ce sous-domaine un vrai tenant (voir docs/SCALING.md §6 du kit). Les tâches de fond (planifiées, événements) ne sont pas touchées.",
      };
    },
  },
  {
    id: "cle_coffre", gravite: "important", titre: "Clé du coffre de secrets",
    pourquoi: "Le coffre de dysizz-flow chiffre tes secrets. Sans clé dédiée, il utilise le secret des sessions : si tu le changes, tous les secrets rangés deviennent illisibles.",
    verifier: () => {
      if (!(state().plugins || {})["dysizz-flow"]) return null;
      return process.env.DZF_CLE_COFFRE ? { etat: "ok", dit: "Clé dédiée présente (DZF_CLE_COFFRE)." } : { etat: "ko", dit: "Pas de clé dédiée : le coffre dépend du secret des sessions." };
    },
    manuel: "Ajoute la variable DZF_CLE_COFFRE sur le serveur (Dokploy → Environment), générée avec : openssl rand -base64 48. Garde-la aussi hors du serveur : sans elle, les secrets sont perdus.",
  },
  /* ---- réglages du serveur (tenant racine seulement) ---- */
  {
    id: "cookies", gravite: "important", racine: true, titre: "Cookies sécurisés derrière le proxy HTTPS",
    pourquoi: "Derrière un proxy HTTPS (Traefik, Dokploy), Saltcorn doit le savoir : sinon les cookies de session peuvent partir sans chiffrement, et tous les visiteurs ont la même adresse IP (la limite de tentatives de connexion bloque alors tout le monde d'un coup).",
    verifier: (req) => {
      if (cfg("force_secure_cookies", false)) return { etat: "ok", dit: "Activé." };
      const https = String((req.headers && req.headers["x-forwarded-proto"]) || req.protocol || "").includes("https");
      return https ? { etat: "ko", dit: "Le site est en HTTPS derrière un proxy, mais Saltcorn ne le sait pas." } : { etat: "info", dit: "Le site n'est pas vu en HTTPS : à activer dès qu'il l'est." };
    },
    correction: {
      quoi: () => "Force secure cookies : non → <b>oui</b> (active aussi la confiance dans le proxy pour l'adresse IP des visiteurs).",
      attention: "Prend effet au prochain redémarrage de Saltcorn (Dokploy → Redeploy). Le site doit être en HTTPS, sinon plus personne ne pourra se connecter.",
      appliquer: () => setConfig("force_secure_cookies", true),
    },
  },
  {
    id: "cors", gravite: "conseil", racine: true, titre: "Accès à l'API depuis d'autres sites (CORS)",
    pourquoi: "Ouvert par défaut dans Saltcorn : n'importe quel site web peut appeler ton API depuis le navigateur de ses visiteurs. À fermer sauf si une autre application web en a besoin.",
    verifier: () => (cfg("cors_enabled", true) ? { etat: "ko", dit: "Ouvert à tous les sites." } : { etat: "ok", dit: "Fermé." }),
    correction: {
      quoi: () => "CORS : ouvert → <b>fermé</b>.",
      attention: "Prend effet au prochain redémarrage. Si une application web externe (sur un autre domaine) appelle ton API, elle ne pourra plus le faire.",
      appliquer: () => setConfig("cors_enabled", false),
    },
  },
  {
    id: "en_tetes", gravite: "conseil", titre: "En-têtes de sécurité HTTP",
    pourquoi: "Quelques lignes envoyées avec chaque page empêchent le navigateur de rétrograder en HTTP, de deviner le type des fichiers, ou de laisser un site tiers utiliser la caméra.",
    verifier: () => {
      const h = String(cfg("custom_http_headers", "") || "").toLowerCase();
      const manque = EN_TETES.filter((l) => !h.includes(l.split(":")[0].toLowerCase()));
      return manque.length ? { etat: "ko", dit: `Il manque : ${manque.map((l) => `<code>${esc(l.split(":")[0])}</code>`).join(", ")}.` } : { etat: "ok", dit: "Présents." };
    },
    correction: {
      quoi: () => { const h = String(cfg("custom_http_headers", "") || "").toLowerCase(); return "Lignes ajoutées aux en-têtes personnalisés (les tiennes sont gardées) :" + liste(EN_TETES.filter((l) => !h.includes(l.split(":")[0].toLowerCase())).map((l) => `<code>${esc(l)}</code>`)); },
      attention: "Strict-Transport-Security oblige le HTTPS pendant un an sur ce domaine et ses sous-domaines : n'applique que si tout est déjà en HTTPS.",
      appliquer: async () => { const cur = String(cfg("custom_http_headers", "") || ""); const low = cur.toLowerCase(); const add = EN_TETES.filter((l) => !low.includes(l.split(":")[0].toLowerCase())); await setConfig("custom_http_headers", [cur.trim(), ...add].filter(Boolean).join("\n")); },
    },
  },
  {
    id: "plugins_git", gravite: "important", racine: true, titre: "Plugins GitHub installables par les tenants",
    pourquoi: "Un plugin, c'est du code qui tourne sur ton serveur. Si les tenants peuvent installer des plugins GitHub, l'admin de n'importe quel tenant peut faire exécuter le code de son choix sur le serveur de tous.",
    verifier: () => {
      if (!multiTenant()) return null;
      return cfg("tenants_install_git", false) ? { etat: "ko", dit: "Autorisé. Sans risque tant que tu es le seul admin de tous les tenants." } : { etat: "ok", dit: "Interdit (réglage par défaut de Saltcorn)." };
    },
    manuel: "Tant que tous les tenants sont à toi : acceptable. Avant de confier un tenant à quelqu'un : décoche « Install git plugins » (Paramètres → Multitenancy) et installe les plugins Dysizz depuis npm.",
    lien: "/tenant/settings",
  },
  {
    id: "versions", gravite: "conseil", titre: "Versions installées",
    pourquoi: "Savoir exactement ce qui tourne évite de corriger un problème déjà corrigé ailleurs.",
    verifier: async () => {
      const Plugin = require("@saltcorn/data/models/plugin");
      const ps = (await Plugin.find({})).filter((p) => /^dysizz/.test(p.name));
      let sc = "";
      try { sc = require("@saltcorn/data/package.json").version; } catch (e) { /* rien */ }
      return { etat: "info", dit: `Saltcorn ${esc(sc || "?")} · ` + ps.map((p) => `${esc(p.name)} ${esc(p.version || "?")}`).join(" · ") + ` · cette page : dysizz-ui ${esc(VERSION)}` };
    },
  },
];

/* ---------- exécution ---------- */
const evaluer = async (req) => {
  const racine = estRacine();
  const out = [];
  for (const v of VERIFS) {
    if (v.racine && !racine) continue;
    let r;
    try { r = await v.verifier(req); } catch (e) { r = { etat: "info", dit: `Vérification impossible : ${esc(e.message)}` }; }
    if (!r) continue;
    const fixable = !!(v.correction && r.etat === "ko" && (!v.correction.si || (await v.correction.si())));
    out.push({ ...v, ...r, gravite: r.gravite || v.gravite, fixable, manuel: r.manuel || v.manuel });
  }
  return out;
};

const RANG = { critique: 0, important: 1, conseil: 2 };
const pl = (n, un, plusieurs) => `${n} ${n > 1 ? plusieurs : un}`;
const COULEUR = { ok: "#1e7145", ko_critique: "#b91d47", ko_important: "#e3a21a", ko_conseil: "#2d89ef", info: "#6b7280" };
const ICONE = { ok: "fa-check-circle", ko: "fa-exclamation-triangle", info: "fa-info-circle" };

const page = async (req, res, extra = "") => {
  const rs = await evaluer(req);
  const ko = rs.filter((r) => r.etat === "ko").sort((a, b) => RANG[a.gravite] - RANG[b.gravite]);
  const ok = rs.filter((r) => r.etat === "ok"), info = rs.filter((r) => r.etat === "info");
  const nCrit = ko.filter((r) => r.gravite === "critique").length;
  const score = Math.round((100 * ok.length) / Math.max(1, ok.length + ko.length));
  const csrf = req.csrfToken ? req.csrfToken() : "";
  const q = req.query || {};
  const carte = (r) => {
    const col = r.etat === "ko" ? COULEUR[`ko_${r.gravite}`] : COULEUR[r.etat];
    return `<div class="dzs-carte" style="--c:${col}">
  <div class="dzs-tete"><i class="fas ${ICONE[r.etat]}"></i><b>${esc(r.titre)}</b>${r.etat === "ko" ? `<span class="dzs-gravite">${esc(r.gravite)}</span>` : ""}</div>
  <div class="dzs-dit">${r.dit}</div>
  ${r.etat !== "ok" ? `<details><summary>Pourquoi c'est important</summary><p>${esc(r.pourquoi)}</p></details>` : ""}
  ${r.etat === "ko" && r.manuel && !r.fixable ? `<div class="dzs-manuel"><i class="fas fa-hand-point-right"></i> ${r.manuel}</div>` : ""}
  <div class="dzs-actions">
    ${r.fixable ? `<form method="post" action="/dysizz/sante/corriger"><input type="hidden" name="_csrf" value="${esc(csrf)}"><input type="hidden" name="id" value="${esc(r.id)}"><button class="btn btn-sm btn-primary">Voir ce qui va changer</button></form>` : ""}
    ${r.lien ? `<a class="btn btn-sm btn-outline-secondary" href="${esc(r.lien)}">Ouvrir le réglage</a>` : ""}
  </div>
</div>`;
  };
  const html = `
<style>
.dzs{max-width:980px;margin:0 auto;padding:1rem 0 3rem}
.dzs-resume{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap;padding:1.2rem;border:1px solid var(--dz-border,#ddd);border-radius:var(--dz-radius,12px);background:var(--dz-surface,#fff);margin:1rem 0 1.5rem}
.dzs-score{font-weight:800;font-size:2.8rem;line-height:1;font-family:var(--dz-font-display);color:${nCrit ? COULEUR.ko_critique : ko.length ? COULEUR.ko_important : COULEUR.ok}}
.dzs-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:.9rem}
.dzs-carte{border:1px solid var(--dz-border,#ddd);border-left:5px solid var(--c);border-radius:var(--dz-radius,12px);padding:1rem;background:var(--dz-surface,#fff)}
.dzs-tete{display:flex;gap:.55rem;align-items:center}.dzs-tete i{color:var(--c)}
.dzs-gravite{margin-left:auto;font-weight:600;font-size:.7rem;line-height:1;font-family:var(--dz-font-mono),monospace;text-transform:uppercase;color:var(--c);border:1px solid var(--c);border-radius:99px;padding:.25rem .5rem}
.dzs-dit{margin:.5rem 0;color:var(--dz-text-soft,inherit)}.dzs-liste{margin:.4rem 0 0 1rem;padding:0}
.dzs-carte details{margin:.3rem 0;color:var(--dz-text-mute,#666)}.dzs-carte summary{cursor:pointer}
.dzs-manuel{background:color-mix(in srgb,var(--c) 9%,transparent);border-radius:8px;padding:.6rem .75rem;margin:.5rem 0}
.dzs-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.5rem}.dzs-actions form{margin:0}
.dzs-apercu{border:2px solid ${COULEUR.ko_conseil};border-radius:var(--dz-radius,12px);padding:1.1rem;margin:1rem 0;background:var(--dz-surface,#fff)}
.dzs h2{font-size:1.15rem;margin:1.8rem 0 .8rem}
</style>
<div class="dzs">
  <span class="dz-eyebrow">Dysizz · santé et sécurité · ${estRacine() ? "tenant racine" : "tenant"}</span>
  <h1 class="dz-h2">Santé et sécurité</h1>
  <p class="dz-lead">Tout est vérifié à l'ouverture de cette page. Rien n'est modifié sans ton accord : chaque correction montre d'abord ce qui va changer.</p>
  ${q.ok ? `<div class="alert alert-success">${esc(q.ok)}</div>` : ""}${q.err ? `<div class="alert alert-danger">${esc(q.err)}</div>` : ""}
  ${extra}
  <div class="dzs-resume"><div><div class="dzs-score">${score} %</div><small>score de sécurité</small></div><div>${ko.length ? `<b>${pl(ko.length, "point à traiter", "points à traiter")}</b>${nCrit ? `, dont <b>${pl(nCrit, "critique", "critiques")}</b>` : ""}. Commence par le haut.` : "<b>Tout est en ordre.</b> Reviens ici après chaque changement important (domaine, version, nouveau tenant)."}<br><small>${pl(ok.length, "point en ordre", "points en ordre")} · ${pl(info.length, "information", "informations")}</small></div></div>
  ${ko.length ? `<h2>À traiter</h2><div class="dzs-grille">${ko.map(carte).join("")}</div>` : ""}
  ${info.length ? `<h2>Pour information</h2><div class="dzs-grille">${info.map(carte).join("")}</div>` : ""}
  ${ok.length ? `<h2>En ordre</h2><div class="dzs-grille">${ok.map(carte).join("")}</div>` : ""}
</div>`;
  res.sendWrap("Santé et sécurité", { above: [{ type: "blank", contents: html }] });
};

const santePage = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  return page(req, res);
};

/* POST : sans « confirmer », montre ce qui va changer (rien n'est écrit) ; avec, applique. */
const corriger = async (req, res) => {
  if (!isAdmin(req)) return denied(res);
  const b = post(req);
  const v = VERIFS.find((x) => x.id === String(b.id || ""));
  if (!v || !v.correction || (v.racine && !estRacine())) return res.redirect("/dysizz/sante?err=" + encodeURIComponent("Correction inconnue."));
  let r;
  try { r = await v.verifier(req); } catch (e) { r = null; }
  if (!r || r.etat !== "ko" || (v.correction.si && !(await v.correction.si()))) return res.redirect("/dysizz/sante?ok=" + encodeURIComponent(`« ${v.titre} » : déjà en ordre, rien à faire.`));
  const csrf = req.csrfToken ? req.csrfToken() : "";
  if (String(b.confirmer || "") !== "1") {
    const quoi = await v.correction.quoi();
    const apercu = `<div class="dzs-apercu"><b>Aperçu : ${esc(v.titre)}</b><p style="margin:.5rem 0">${quoi}</p>${v.correction.attention ? `<p class="text-warning-emphasis"><i class="fas fa-exclamation-circle"></i> ${esc(v.correction.attention)}</p>` : ""}<p><small>Rien n'a encore été modifié.</small></p><div class="dzs-actions"><form method="post" action="/dysizz/sante/corriger"><input type="hidden" name="_csrf" value="${esc(csrf)}"><input type="hidden" name="id" value="${esc(v.id)}"><input type="hidden" name="confirmer" value="1"><button class="btn btn-primary">Appliquer</button></form><a class="btn btn-outline-secondary" href="/dysizz/sante">Annuler</a></div></div>`;
    return page(req, res, apercu);
  }
  try {
    await v.correction.appliquer();
    try { state().log(2, `[dysizz-ui] santé : correction « ${v.id} » appliquée par ${req.user && req.user.email}`); } catch (e) { /* rien */ }
    return res.redirect("/dysizz/sante?ok=" + encodeURIComponent(`« ${v.titre} » : corrigé.`));
  } catch (e) {
    return res.redirect("/dysizz/sante?err=" + encodeURIComponent(`« ${v.titre} » : échec (${e.message}). Rien d'autre n'a été modifié.`));
  }
};

module.exports = { santePage, corriger, VERIFS, evaluer };
