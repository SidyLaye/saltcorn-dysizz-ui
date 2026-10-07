/* dysizz-ui — bloc « fiche » : formulaire relié à une table (remplace une vue d'édition native).

   GET /dysizz/fiche/:table?id=12&champs=nom,role
     → description des champs (libellé, type, obligatoire, aide, choix, liste des lignes liées),
       valeurs de la ligne si id, et ce que l'utilisateur a le droit de faire.
   L'écriture passe par l'API de Saltcorn (POST /api/:table et /api/:table/:id) : droits de la
   table, propriétaire, champs protégés (min_role_write), déclencheurs Validate / Insert / Update,
   tout reste vérifié par le serveur, comme pour une vue native.

   Lecture : une ligne n'est renvoyée que si l'utilisateur peut la lire (rôle ou propriétaire) ;
   les listes des champs liés ne contiennent que les lignes qu'il peut lire. */
"use strict";

const MAX_OPTIONS = 500;
const SYSTEME = new Set(["id"]);

const typeDe = (f) => {
  const t = (f.type && (f.type.name || f.type)) || "String";
  if (f.is_fkey || t === "Key") return "cle";
  if (t === "Bool") return "oui_non";
  if (t === "Integer" || t === "Float" || t === "Money") return "nombre";
  if (t === "Date") return f.attributes && f.attributes.day_only === false ? "dateheure" : "date";
  if (t === "Color") return "couleur";
  if (t === "File") return "fichier";
  if (t === "String" && f.attributes && f.attributes.options) return "choix";
  if (t === "String" && f.attributes && (f.attributes.textarea || f.attributes.max_length > 300)) return "zone";
  /* textes longs par leur nom : description, message, explication, commentaire, remarque, notes */
  if (t === "String" && /^(description|message|explication|commentaire|remarques?|notes?|detail|details)$/i.test(f.name)) return "zone";
  if (t === "String" && /mail/i.test(f.name)) return "email";
  if (t === "String" && /(tel|phone)/i.test(f.name)) return "tel";
  return "texte";
};

const optionsDe = (f) => {
  const o = f.attributes && f.attributes.options;
  if (!o) return null;
  return (Array.isArray(o) ? o : String(o).split(",")).map((x) => (typeof x === "object" ? x.name ?? x.value : String(x).trim())).filter((x) => x !== "");
};

/* lignes d'une table liée que l'utilisateur peut lire, filtrées par la condition du champ (attributes.where) */
const listeLiee = async (f, user) => {
  const Table = require("@saltcorn/data/models/table");
  const ref = Table.findOne({ name: f.reftable_name });
  if (!ref) return [];
  const role = user ? user.role_id : 100;
  if (role > ref.min_role_read && !ref.ownership_field_id && !ref.ownership_formula) return [];
  const cle = f.refname || "id";
  const resume = (f.attributes && f.attributes.summary_field) || (ref.getFields().find((x) => ["nom", "name", "titre", "title", "label", "libelle", "email"].includes(x.name)) || {}).name || cle;
  let where = {};
  if (f.attributes && f.attributes.where) {
    try {
      const { jsexprToWhere } = require("@saltcorn/data/models/expression");
      where = jsexprToWhere(f.attributes.where, { user }, ref.getFields()) || {};
    } catch (e) {
      where = {};
    }
  }
  const rows = await ref.getRows(where, { forUser: user || undefined, forPublic: !user, orderBy: resume, limit: MAX_OPTIONS });
  return rows.map((r) => [r[cle], r[resume] ?? r[cle]]);
};

const route = async (req, res) => {
  try {
    const Table = require("@saltcorn/data/models/table");
    const table = Table.findOne({ name: req.params.table });
    if (!table) return res.status(404).json({ erreur: "table introuvable" });
    const user = req.user || null;
    const role = user ? user.role_id : 100;
    const proprio = table.ownership_field_id ? (table.getFields().find((f) => f.id === table.ownership_field_id) || {}).name : null;
    /* droit d'écrire : rôle, ou table avec propriétaire (le serveur vérifiera la ligne) */
    const ecrire = role <= table.min_role_write || (!!user && (!!proprio || !!table.ownership_formula));
    const lire = role <= table.min_role_read || (!!user && (!!proprio || !!table.ownership_formula));
    if (!ecrire && !lire) return res.status(403).json({ erreur: "accès refusé" });

    const voulus = String(req.query.champs || "").split(",").map((x) => x.trim()).filter(Boolean);
    const tous = table.getFields().filter((f) => !SYSTEME.has(f.name) && !f.calculated && !f.primary_key);
    const champs = voulus.length ? voulus.map((n) => tous.find((f) => f.name === n)).filter(Boolean) : tous;
    /* le champ propriétaire est toujours décrit : la fiche le remplit avec l'utilisateur à la création */
    if (proprio && !champs.some((f) => f.name === proprio)) { const f = tous.find((x) => x.name === proprio); if (f) champs.push(f); }

    let valeurs = null;
    const id = req.query.id;
    if (id !== undefined && id !== "") {
      if (!/^\d+$/.test(String(id))) return res.status(400).json({ erreur: "identifiant invalide" });
      valeurs = await table.getRow({ id: +id }, { forUser: user || undefined, forPublic: !user });
      if (!valeurs) return res.status(404).json({ erreur: "fiche introuvable ou non autorisée" });
    }

    const out = [];
    for (const f of champs) {
      const type = typeDe(f);
      const mrw = f.attributes && f.attributes.min_role_write;
      const c = {
        nom: f.name,
        libelle: f.label || f.name,
        type,
        requis: !!f.required,
        aide: f.description || "",
        lecture_seule: !!(mrw && role > +mrw),
        proprietaire: f.name === proprio,
      };
      if (type === "choix") c.options = optionsDe(f);
      if (type === "fichier") c.accept = ACCEPT;
      if (type === "cle") {
        /* la table des utilisateurs n'est pas proposée en liste : un champ propriétaire est rempli par le serveur */
        c.options = f.reftable_name === "users" && role > 1 ? [] : await listeLiee(f, user);
        c.table_liee = f.reftable_name;
      }
      if (valeurs) c.valeur = valeurs[f.name] ?? null;
      out.push(c);
    }
    res.json({ table: table.name, id: valeurs ? valeurs.id : null, droits: { ecrire, supprimer: ecrire && role <= table.min_role_write }, utilisateur: user ? user.id : null, champs: out });
  } catch (e) {
    res.status(500).json({ erreur: "lecture impossible" });
  }
};

/* GET /dysizz/fiche/:table/lignes?champs=nom,agence_nom,groupe
   Lignes d'une table (id + les champs demandés seulement) que l'utilisateur peut lire, pour choisir des
   membres dans une fiche (ex. les personnes d'un groupe). Au plus 1000 lignes. */
const MAX_LIGNES = 1000;
const lignes = async (req, res) => {
  try {
    const Table = require("@saltcorn/data/models/table");
    const table = Table.findOne({ name: req.params.table });
    if (!table) return res.status(404).json({ erreur: "table introuvable" });
    const user = req.user || null;
    const role = user ? user.role_id : 100;
    if (role > table.min_role_read && !(user && (table.ownership_field_id || table.ownership_formula))) return res.status(403).json({ erreur: "accès refusé" });
    const noms = new Set(table.getFields().map((f) => f.name));
    const champs = String(req.query.champs || "").split(",").map((x) => x.trim()).filter((x) => noms.has(x) && x !== "id").slice(0, 12);
    const rows = await table.getRows({}, { forUser: user || undefined, forPublic: !user, orderBy: champs[0] || "id", limit: MAX_LIGNES });
    res.json({ lignes: rows.map((r) => Object.fromEntries([["id", r.id], ...champs.map((c) => [c, r[c] ?? null])])), max: MAX_LIGNES });
  } catch (e) {
    res.status(500).json({ erreur: "lecture impossible" });
  }
};

/* POST /dysizz/fiche/:table/fichier/:champ (multipart, champ « file ») — pièce jointe d'un champ Fichier.
   L'envoi de fichiers de Saltcorn est réservé aux administrateurs (min_role_upload) ; ici, quiconque peut
   écrire dans la table peut joindre un fichier à CE champ, et rien d'autre. Le fichier n'est lisible que par
   les administrateurs et par celui qui l'a envoyé (règle de /files/serve). On renvoie la valeur à écrire
   dans le champ ; l'écriture de la ligne passe ensuite par l'API, avec tous ses contrôles. */
const ENVOI_MAX = 10 * 1024 * 1024;
const EXTENSIONS = ["png", "jpg", "jpeg", "gif", "webp", "pdf", "txt", "csv", "doc", "docx", "xls", "xlsx", "odt", "ods", "zip"];
const ACCEPT = EXTENSIONS.map((x) => "." + x).join(",");
const MIMES = /^(image\/(png|jpe?g|gif|webp)|application\/pdf|text\/(plain|csv)|application\/(msword|vnd\.ms-excel|vnd\.openxmlformats-officedocument\.(wordprocessingml\.document|spreadsheetml\.sheet)|vnd\.oasis\.opendocument\.(text|spreadsheet)|zip|x-zip-compressed|octet-stream))$/;
const envoyer = async (req, res) => {
  try {
    const Table = require("@saltcorn/data/models/table");
    const table = Table.findOne({ name: req.params.table });
    if (!table) return res.status(404).json({ erreur: "table introuvable" });
    const user = req.user;
    if (!user || !user.id) return res.status(401).json({ erreur: "connexion requise" });
    const f = table.getFields().find((x) => x.name === req.params.champ);
    if (!f || typeDe(f) !== "fichier") return res.status(400).json({ erreur: "ce champ n'accepte pas de fichier" });
    const proprio = !!table.ownership_field_id || !!table.ownership_formula;
    const mrw = f.attributes && f.attributes.min_role_write;
    if (!(user.role_id <= table.min_role_write || proprio) || (mrw && user.role_id > +mrw)) return res.status(403).json({ erreur: "accès refusé" });
    const fichier = req.files && req.files.file;
    if (!fichier || Array.isArray(fichier)) return res.status(400).json({ erreur: "un seul fichier attendu" });
    if (fichier.truncated || fichier.size > ENVOI_MAX) return res.status(413).json({ erreur: "fichier trop lourd (10 Mo au plus)" });
    const ext = String(fichier.name || "").toLowerCase().split(".").pop();
    if (!EXTENSIONS.includes(ext) || !MIMES.test(String(fichier.mimetype || ""))) return res.status(415).json({ erreur: `type de fichier refusé (acceptés : ${EXTENSIONS.join(", ")})` });
    const File = require("@saltcorn/data/models/file");
    const enr = await File.from_req_files(fichier, user.id, 1);
    const valeur = File.fieldValueFromRelative ? File.fieldValueFromRelative(enr.path_to_serve) : enr.path_to_serve;
    res.json({ valeur, nom: enr.filename });
  } catch (e) {
    res.status(500).json({ erreur: "envoi impossible" });
  }
};

module.exports = { route, lignes, envoyer, typeDe, optionsDe, ENVOI_MAX, EXTENSIONS };
