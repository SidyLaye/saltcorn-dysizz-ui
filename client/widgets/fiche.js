/* Fiche : formulaire relié à une table Saltcorn, à la place d'une vue d'édition native.

   <div data-dz-widget="fiche" data-table="equipe"
        data-champs='["nom","role",{"section":"Rythme"},"temps","jours"]'
        data-libelles='{"role":{"negociateur":"Négociateur","assistante":"Assistant(e)"}}'
        data-si='{"jours":{"temps":"mi_temps"}}'
        data-apres="/page/personne?id={id}"></div>

   Réglages (tous facultatifs sauf data-table) :
   - data-id : id de la ligne à modifier ; sinon le paramètre d'adresse ?id= ; sans id : création.
   - data-champs : champs et ordre (défaut : tous) ; {"section":"Titre"} ouvre une section.
   - data-titres / data-aides : { champ: texte } remplacent le libellé / l'aide de la table.
   - data-libelles : { champ: { valeur: libellé } } pour les listes de choix.
   - data-si : { champ: { autre_champ: valeur | [valeurs] } } → champ montré seulement si…
   - data-valeurs : valeurs de départ d'une création ; les paramètres d'adresse qui portent le nom
     d'un champ (ex. ?personne=14) aussi.
   - data-apres : adresse après l'enregistrement ({id} et {champ} remplacés) ; défaut : page précédente.
   - data-caches : champs envoyés sans être montrés (valeur de départ ou de la ligne), ex. ["ticket"].
   - data-utilisateur : champs remplis avec l'utilisateur connecté à la création, ex. ["auteur"].
   - data-bouton (« Enregistrer »), data-titre, data-titre-nouveau, data-supprimer (true : bouton Supprimer).
   Tout est vérifié par le serveur (API Saltcorn) : droits, propriétaire, champs protégés, contrôles. */
import { register, css, h, conf, csrf } from "./_commun.js";

css("fiche", `.dzw-fi{max-width:760px;padding:22px 24px;box-sizing:border-box}
.dzw-fi,.dzw-fi p,.dzw-fi label,.dzw-fi button,.dzw-fi input,.dzw-fi select,.dzw-fi textarea{font-family:var(--dz-font-body,inherit)}
.dzw-fi h3{font-size:1.2rem;margin:0 0 14px}
.dzw-fi-sec{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;opacity:.6;font-weight:700;margin:22px 0 10px;padding-top:14px;border-top:1px solid var(--dz-border,#e5e7eb)}
.dzw-fi-q{margin-bottom:14px}
.dzw-fi-q>label,.dzw-fi-q>.lbl{display:block;font-weight:600;font-size:.9rem;margin-bottom:5px}
.dzw-fi-q .req{color:#dc2626;margin-left:3px}
.dzw-fi-q .aide{font-size:.78rem;opacity:.65;margin:4px 0 0}
.dzw-fi-q input[type=text],.dzw-fi-q input[type=email],.dzw-fi-q input[type=tel],.dzw-fi-q input[type=number],.dzw-fi-q input[type=date],.dzw-fi-q input[type=datetime-local],.dzw-fi-q textarea,.dzw-fi-q select{width:100%;box-sizing:border-box;border:1px solid var(--dz-border,#d1d5db);border-radius:10px;padding:9px 12px;font:inherit;background:var(--dz-surface,#fff);color:inherit;min-height:42px}
.dzw-fi-q textarea{min-height:96px}
.dzw-fi-q input:focus-visible,.dzw-fi-q textarea:focus-visible,.dzw-fi-q select:focus-visible{outline:3px solid color-mix(in srgb,var(--dz-primary,#2563eb) 35%,transparent);border-color:var(--dz-primary,#2563eb)}
.dzw-fi-q.err input,.dzw-fi-q.err select,.dzw-fi-q.err textarea{border-color:#dc2626}
.dzw-fi-q .msg{color:#b91c1c;font-size:.8rem;margin-top:4px}
.dzw-fi-q .ro{padding:9px 0;opacity:.85}
.dzw-fi-sw{display:inline-flex;align-items:center;gap:12px;cursor:pointer;font-weight:600}
.dzw-fi-sw input{margin-right:2px!important}
.dzw-fi-sw input{width:40px;height:22px;appearance:none;-webkit-appearance:none;border-radius:99px;background:var(--dz-border-strong,#cbd5e1);position:relative;cursor:pointer;transition:background .15s;flex:none;margin:0}
.dzw-fi-sw input::after{content:"";position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:transform .15s}
.dzw-fi-sw input:checked{background:var(--dz-primary,#2563eb)}.dzw-fi-sw input:checked::after{transform:translateX(18px)}
.dzw-fi-act{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:20px;padding-top:16px;border-top:1px solid var(--dz-border,#e5e7eb)}
.dzw-fi-act button{min-height:42px;padding:0 18px;border-radius:10px;font:inherit;font-weight:600;cursor:pointer;border:1px solid transparent}
.dzw-fi-act .ok{background:var(--dz-primary,#2563eb);color:var(--dz-on-primary,#fff)}
.dzw-fi-act .sec{background:transparent;color:inherit;border-color:var(--dz-border,#e5e7eb)}
.dzw-fi-act .suppr{background:transparent;color:#b91c1c;border-color:color-mix(in srgb,#b91c1c 35%,transparent);margin-left:auto}
.dzw-fi-act button[disabled]{opacity:.6;cursor:wait}
.dzw-fi-err{background:color-mix(in srgb,#dc2626 10%,transparent);color:#991b1b;border-radius:10px;padding:10px 12px;margin:0 0 14px;font-size:.9rem}
.dzw-fi-ok{background:color-mix(in srgb,#059669 12%,transparent);color:#065f46;border-radius:10px;padding:10px 12px;margin:0 0 14px;font-size:.9rem}
.dzw-fi-sq{height:220px;border-radius:12px;background:var(--dz-surface-2,#f1f5f9);animation:dzw-fi-p 1.2s ease-in-out infinite}
@keyframes dzw-fi-p{50%{opacity:.55}}`);

const humain = (v) => { const s = String(v ?? "").replace(/_/g, " "); return s.charAt(0).toUpperCase() + s.slice(1); };
const modele = (t, row) => String(t || "").replace(/\{(\w+)\}/g, (_, k) => encodeURIComponent(row[k] ?? ""));
const jour = (v) => { if (!v) return ""; const d = new Date(v); return isNaN(d) ? String(v).slice(0, 10) : new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); };
const jourHeure = (v) => { if (!v) return ""; const d = new Date(v); return isNaN(d) ? "" : new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 16); };

register("fiche", async (el) => {
  const table = conf(el, "table", "");
  el.classList.add("dzw", "dzw-fi");
  el.innerHTML = "";
  if (!table) { el.appendChild(h("div", { class: "dzw-fi-err" }, "Réglage « table » manquant.")); return; }
  const url = Object.fromEntries(new URLSearchParams(location.search));
  const idConf = conf(el, "id", "");
  const id = String(idConf || url.id || "").replace(/\{(\w+)\}/g, (_, k) => url[k] ?? "");
  const plan = conf(el, "champs", []);
  const caches = new Set(conf(el, "caches", []));
  const moi = new Set(conf(el, "utilisateur", []));
  const noms = [...new Set([...plan.filter((x) => typeof x === "string"), ...(plan.length ? [...caches, ...moi] : [])])];
  const titres = conf(el, "titres", {}), aides = conf(el, "aides", {}), libelles = conf(el, "libelles", {}), si = conf(el, "si", {});
  const depart = { ...conf(el, "valeurs", {}) };
  el.appendChild(h("div", { class: "dzw-fi-sq" }));

  let d;
  try {
    const q = new URLSearchParams({ ...(id ? { id } : {}), ...(noms.length ? { champs: noms.join(",") } : {}) });
    const r = await fetch(`/dysizz/fiche/${encodeURIComponent(table)}?${q}`, { credentials: "same-origin", headers: { Accept: "application/json" } });
    d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(d.erreur || `HTTP ${r.status}`);
  } catch (e) {
    el.innerHTML = "";
    el.appendChild(h("div", { class: "dzw-fi-err" }, `Fiche impossible à ouvrir : ${e.message}`));
    return;
  }
  const creation = !d.id;
  const parNom = Object.fromEntries(d.champs.map((c) => [c.nom, c]));
  /* valeurs de départ d'une création : data-valeurs, puis paramètres d'adresse au nom d'un champ */
  if (creation) for (const c of d.champs) if (url[c.nom] !== undefined && c.nom !== "id") depart[c.nom] = url[c.nom];

  el.innerHTML = "";
  const titre = creation ? conf(el, "titre-nouveau", conf(el, "titre", "")) : conf(el, "titre", "");
  if (titre) el.appendChild(h("h3", {}, titre));
  const alerte = h("div", { hidden: true });
  el.appendChild(alerte);
  const form = h("form", { novalidate: true });
  el.appendChild(form);

  const ctrls = {};
  const valeurDe = (c) => (creation ? depart[c.nom] ?? null : c.valeur);
  const lib = (c, v) => (libelles[c.nom] && libelles[c.nom][v]) || humain(v);

  const blocChamp = (c) => {
    const v = valeurDe(c);
    const label = titres[c.nom] || c.libelle;
    const wrap = h("div", { class: "dzw-fi-q", "data-champ": c.nom });
    const idc = `dzw-fi-${table}-${c.nom}`;
    const aide = aides[c.nom] || c.aide;
    if (c.lecture_seule) {
      const affiche = c.type === "cle" ? ((c.options || []).find(([k]) => String(k) === String(v)) || [])[1] ?? v : c.type === "choix" ? lib(c, v) : c.type === "oui_non" ? (v ? "oui" : "non") : c.type === "date" ? jour(v) : v;
      wrap.append(h("div", { class: "lbl" }, label), h("div", { class: "ro" }, affiche === null || affiche === undefined || affiche === "" ? "—" : String(affiche)));
      return wrap;
    }
    let input;
    if (c.type === "oui_non") {
      input = h("input", { type: "checkbox", id: idc, checked: creation ? v === true || v === "true" || v === "on" : !!v });
      wrap.append(h("label", { class: "dzw-fi-sw", for: idc }, input, label));
    } else {
      if (c.type === "choix" || c.type === "cle") {
        input = h("select", { id: idc }, h("option", { value: "" }, c.requis ? "— choisir —" : "—"));
        for (const o of c.type === "choix" ? (c.options || []).map((x) => [x, lib(c, x)]) : c.options || []) input.appendChild(h("option", { value: o[0], selected: v !== null && v !== undefined && String(v) === String(o[0]) }, String(o[1])));
      } else if (c.type === "zone") input = h("textarea", { id: idc }, v ?? "");
      else if (c.type === "nombre") input = h("input", { type: "number", id: idc, step: "any", value: v ?? "" });
      else if (c.type === "date") input = h("input", { type: "date", id: idc, value: jour(v) });
      else if (c.type === "dateheure") input = h("input", { type: "datetime-local", id: idc, value: jourHeure(v) });
      else if (c.type === "couleur") input = h("input", { type: "color", id: idc, value: v || "#000000" });
      else input = h("input", { type: c.type === "email" ? "email" : c.type === "tel" ? "tel" : "text", id: idc, value: v ?? "" });
      wrap.append(h("label", { for: idc }, label, c.requis ? h("span", { class: "req", "aria-hidden": "true" }, "*") : null), input);
    }
    if (aide) wrap.appendChild(h("p", { class: "aide" }, aide));
    ctrls[c.nom] = { c, input, wrap };
    return wrap;
  };

  /* champ propriétaire (ex. demandeur) : rempli avec l'utilisateur, jamais montré.
     data-caches : champs envoyés sans être montrés (ex. le ticket d'une réponse, pris dans l'adresse) */
  const cache = new Set([...d.champs.filter((c) => c.proprietaire).map((c) => c.nom), ...[...moi].filter((n) => parNom[n])]);
  const ordre = plan.length ? plan : d.champs.map((c) => c.nom);
  for (const x of ordre) {
    if (x && typeof x === "object" && x.section) { form.appendChild(h("div", { class: "dzw-fi-sec" }, x.section)); continue; }
    const c = parNom[x];
    if (!c || cache.has(c.nom) || caches.has(c.nom)) continue;
    form.appendChild(blocChamp(c));
  }

  /* champs montrés sous condition (ex. jours travaillés seulement à temps partiel) */
  const valeurCtrl = (nom) => { const k = ctrls[nom]; if (!k) return (parNom[nom] || {}).valeur; return k.input.type === "checkbox" ? k.input.checked : k.input.value; };
  const conditions = () => {
    for (const [nom, cond] of Object.entries(si || {})) {
      const k = ctrls[nom];
      if (!k) continue;
      const ok = Object.entries(cond).every(([autre, attendu]) => [].concat(attendu).map(String).includes(String(valeurCtrl(autre) ?? "")));
      k.wrap.hidden = !ok;
    }
  };
  form.addEventListener("change", conditions);
  conditions();

  const lireValeur = (k) => {
    const { c, input } = k;
    if (c.type === "oui_non") return input.checked;
    const s = input.value;
    if (s === "") return null;
    if (c.type === "nombre") return Number(s);
    if (c.type === "cle") return /^\d+$/.test(s) ? Number(s) : s;
    return s;
  };

  const montrer = (cls, texte) => { alerte.className = cls; alerte.textContent = texte; alerte.hidden = !texte; if (texte) alerte.scrollIntoView({ block: "nearest", behavior: "smooth" }); };
  const appel = async (adresse, corps) => {
    const r = await fetch(adresse, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", Accept: "application/json", "CSRF-Token": csrf() }, body: JSON.stringify(corps || {}) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.error) throw new Error(j.error === "Not authorized" ? "vous n'avez pas le droit de faire cette modification" : j.error || `HTTP ${r.status}`);
    return j;
  };

  const act = h("div", { class: "dzw-fi-act" });
  const ok = h("button", { type: "submit", class: "ok" }, conf(el, "bouton", "Enregistrer"));
  act.appendChild(ok);
  act.appendChild(h("button", { type: "button", class: "sec", onclick: () => history.back() }, "Annuler"));
  if (!creation && conf(el, "supprimer", false) && d.droits && d.droits.supprimer) {
    act.appendChild(h("button", { type: "button", class: "suppr", onclick: async () => {
      if (!confirm("Supprimer cette fiche ? C'est définitif.")) return;
      try { await appel(`/api/${encodeURIComponent(table)}/delete/${d.id}`); location.href = conf(el, "apres-suppression", "") || document.referrer || "/"; } catch (e) { montrer("dzw-fi-err", `Suppression impossible : ${e.message}`); }
    } }, "Supprimer"));
  }
  if (d.droits && !d.droits.ecrire) { ok.disabled = true; ok.title = "Lecture seule"; }
  form.appendChild(act);

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    montrer("", "");
    const corps = {};
    let manque = 0;
    for (const k of Object.values(ctrls)) {
      k.wrap.classList.remove("err");
      const m = k.wrap.querySelector(".msg"); if (m) m.remove();
      if (k.wrap.hidden) continue;
      const v = lireValeur(k);
      if (k.c.requis && (v === null || v === "") && k.c.type !== "oui_non") {
        manque++; k.wrap.classList.add("err"); k.wrap.appendChild(h("div", { class: "msg" }, "À remplir"));
        continue;
      }
      corps[k.c.nom] = v;
    }
    if (creation) for (const nom of cache) if (d.utilisateur) corps[nom] = d.utilisateur;
    for (const nom of caches) if (parNom[nom]) { const v = creation ? depart[nom] : parNom[nom].valeur; if (v !== undefined && v !== null && v !== "") corps[nom] = /^\d+$/.test(String(v)) && ["cle", "nombre"].includes(parNom[nom].type) ? Number(v) : v; }
    if (manque) { montrer("dzw-fi-err", manque > 1 ? `${manque} champs à remplir.` : "Un champ à remplir."); return; }
    ok.disabled = true;
    try {
      const j = await appel(creation ? `/api/${encodeURIComponent(table)}/` : `/api/${encodeURIComponent(table)}/${d.id}`, corps);
      const nid = creation ? j.success : d.id;
      const apres = conf(el, "apres", "");
      if (apres && /^\/(?!\/)/.test(apres)) { location.href = modele(apres, { ...corps, id: nid }); return; }
      if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { history.back(); return; }
      montrer("dzw-fi-ok", "Enregistré.");
    } catch (e) {
      montrer("dzw-fi-err", `Enregistrement impossible : ${e.message}`);
    } finally {
      ok.disabled = false;
    }
  });
});
