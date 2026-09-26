/* Formulaire : un constructeur de formulaires ET leur remplissage.
   Pour livrer à un client un outil où SES équipes créent leurs propres
   questionnaires, fiches d'inspection, demandes, inscriptions…

   data-mode="construire" (défaut) : on compose le formulaire, aperçu en direct ;
     le schéma (JSON) est enregistré dans data-champ.
   data-mode="remplir" : on remplit un formulaire décrit par data-schema (JSON)
     ou par le champ data-schema-champ ; les réponses (JSON { id: valeur })
     vont dans data-champ. Champs obligatoires et formats vérifiés en direct.

   Schéma : { v: 1, titre, intro, champs: [{ id, type, label, aide, requis, options, min, max }] }
   Types : texte, zone, nombre, email, tel, date, choix, cases, oui_non, note, section */
import { register, css, h, conf, champ, btn } from "./_commun.js";

css("formulaire", `.dzw-fo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.dzw-fo.remplir{display:block}
.dzw-fo-col{padding:14px;min-width:0}.dzw-fo-col+.dzw-fo-col{border-left:1px solid var(--dz-border,#e5e7eb);background:var(--dz-bg-soft,#f8fafc)}
.dzw-fo-col h5{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin:0 0 10px}
.dzw-fo-types{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.dzw-fo-it{display:flex;gap:8px;align-items:flex-start;border:1px solid var(--dz-border,#e5e7eb);border-radius:10px;padding:8px 10px;margin-bottom:8px;background:var(--dz-surface,#fff)}
.dzw-fo-it.sel{border-color:var(--dz-primary,#2563eb);box-shadow:0 0 0 3px color-mix(in srgb,var(--dz-primary,#2563eb) 18%,transparent)}
.dzw-fo-it .corps{flex:1;min-width:0;cursor:pointer}
.dzw-fo-it .corps b{display:block;font-size:.88rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dzw-fo-it .corps small{opacity:.6;font-size:.72rem}
.dzw-fo-it .ctl{display:flex;gap:2px}
.dzw-fo-it .ctl button{border:0;background:none;padding:4px 6px;border-radius:6px;cursor:pointer;color:inherit;opacity:.65}
.dzw-fo-it .ctl button:hover,.dzw-fo-it .ctl button:focus-visible{opacity:1;background:var(--dz-surface-2,#f1f5f9)}
.dzw-fo-edit{border:1px dashed var(--dz-border,#cbd5e1);border-radius:10px;padding:10px;margin:-2px 0 10px}
.dzw-fo-edit label{display:block;font-size:.74rem;font-weight:600;opacity:.75;margin:8px 0 3px}
.dzw-fo-edit input[type=text],.dzw-fo-edit textarea{width:100%;box-sizing:border-box}
.dzw-fo-edit textarea{border:1px solid var(--dz-border,#e5e7eb);border-radius:8px;padding:6px 8px;font:inherit;font-size:.85rem;min-height:64px;background:var(--dz-surface,#fff);color:inherit}
.dzw-fo-form{max-width:640px}
.dzw-fo-form h3{font-size:1.25rem;margin:0 0 4px}.dzw-fo-form .intro{opacity:.75;margin:0 0 16px}
.dzw-fo-q{margin-bottom:16px}
.dzw-fo-q>label,.dzw-fo-q>.lbl{display:block;font-weight:600;font-size:.92rem;margin-bottom:6px}
.dzw-fo-q .req{color:#dc2626;margin-left:3px}
.dzw-fo-q .aide{font-size:.78rem;opacity:.65;margin:-2px 0 6px}
.dzw-fo-q input[type=text],.dzw-fo-q input[type=email],.dzw-fo-q input[type=tel],.dzw-fo-q input[type=number],.dzw-fo-q input[type=date],.dzw-fo-q textarea,.dzw-fo-q select{width:100%;box-sizing:border-box;border:1px solid var(--dz-border,#d1d5db);border-radius:10px;padding:10px 12px;font:inherit;background:var(--dz-surface,#fff);color:inherit;min-height:44px}
.dzw-fo-q textarea{min-height:96px}
.dzw-fo-q input:focus-visible,.dzw-fo-q textarea:focus-visible,.dzw-fo-q select:focus-visible{outline:3px solid color-mix(in srgb,var(--dz-primary,#2563eb) 35%,transparent);border-color:var(--dz-primary,#2563eb)}
.dzw-fo-q .opts{display:grid;gap:6px}
.dzw-fo-q .opt{display:flex;gap:10px;align-items:center;border:1px solid var(--dz-border,#e5e7eb);border-radius:10px;padding:10px 12px;cursor:pointer;min-height:44px;box-sizing:border-box}
.dzw-fo-q .opt:has(input:checked){border-color:var(--dz-primary,#2563eb);background:color-mix(in srgb,var(--dz-primary,#2563eb) 7%,transparent)}
.dzw-fo-q .opt input{accent-color:var(--dz-primary,#2563eb);width:18px;height:18px;margin:0}
.dzw-fo-q .etoiles{display:flex;gap:4px}
.dzw-fo-q .etoiles button{border:0;background:none;font-size:1.6rem;line-height:1;cursor:pointer;color:color-mix(in srgb,var(--dz-text,#111827) 22%,transparent);padding:2px}
.dzw-fo-q .etoiles button.on{color:#f59e0b}
.dzw-fo-q .etoiles button:focus-visible{outline:2px solid var(--dz-primary,#2563eb);border-radius:6px}
.dzw-fo-q.err input,.dzw-fo-q.err textarea,.dzw-fo-q.err select,.dzw-fo-q.err .opt{border-color:#dc2626}
.dzw-fo-q .msg{color:#b91c1c;font-size:.8rem;margin-top:5px;display:flex;gap:6px;align-items:center}
.dzw-fo-sec{margin:22px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--dz-border,#e5e7eb)}
.dzw-fo-sec b{font-size:1.02rem}.dzw-fo-sec p{margin:4px 0 0;opacity:.7;font-size:.85rem}
.dzw-fo-bilan{display:flex;gap:8px;align-items:center;font-size:.85rem;padding:10px 12px;border-radius:10px;margin-top:6px}
.dzw-fo-bilan.ok{background:#dcfce7;color:#166534}.dzw-fo-bilan.ko{background:#fee2e2;color:#991b1b}
.dzw-fo-vide{padding:26px;text-align:center;opacity:.7;border:2px dashed var(--dz-border,#e5e7eb);border-radius:12px}
@media (max-width:760px){.dzw-fo{grid-template-columns:1fr}.dzw-fo-col+.dzw-fo-col{border-left:0;border-top:1px solid var(--dz-border,#e5e7eb)}}`);

export const TYPES = [
  { t: "texte", label: "Texte court", icone: "fas fa-font" },
  { t: "zone", label: "Texte long", icone: "fas fa-align-left" },
  { t: "nombre", label: "Nombre", icone: "fas fa-hashtag" },
  { t: "email", label: "E-mail", icone: "fas fa-at" },
  { t: "tel", label: "Téléphone", icone: "fas fa-phone" },
  { t: "date", label: "Date", icone: "far fa-calendar" },
  { t: "choix", label: "Un choix", icone: "far fa-dot-circle", options: true },
  { t: "cases", label: "Plusieurs choix", icone: "far fa-check-square", options: true },
  { t: "oui_non", label: "Oui / non", icone: "fas fa-toggle-on" },
  { t: "note", label: "Note (étoiles)", icone: "far fa-star" },
  { t: "section", label: "Section", icone: "fas fa-heading" },
];
const typeDe = (t) => TYPES.find((x) => x.t === t) || TYPES[0];
const uid = () => "q" + Math.random().toString(36).slice(2, 7);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, TEL = /^[+0-9 ().-]{6,20}$/;

/* message d'erreur pour une réponse, ou "" */
export const erreurDe = (q, v) => {
  const vide = v === undefined || v === null || v === "" || (Array.isArray(v) && !v.length);
  if (vide) return q.requis ? "Réponse obligatoire" : "";
  if (q.type === "email" && !EMAIL.test(String(v))) return "Adresse e-mail invalide (ex. nom@domaine.fr)";
  if (q.type === "tel" && !TEL.test(String(v))) return "Numéro invalide";
  if (q.type === "nombre") { const n = +v; if (Number.isNaN(n)) return "Nombre attendu"; if (q.min !== undefined && q.min !== "" && n < +q.min) return `Au moins ${q.min}`; if (q.max !== undefined && q.max !== "" && n > +q.max) return `Au plus ${q.max}`; }
  return "";
};

/* le formulaire à remplir ; onChange(reponses) à chaque saisie ; renvoie { valider } */
const rendreFormulaire = (hote, schema, reponses, onChange, apercu) => {
  hote.innerHTML = "";
  const form = h("div", { class: "dzw-fo-form" });
  if (schema.titre) form.append(h("h3", {}, schema.titre));
  if (schema.intro) form.append(h("p", { class: "intro" }, schema.intro));
  const blocs = new Map();
  const maj = () => onChange && onChange(reponses);
  const montrerErreur = (q, force) => {
    const b = blocs.get(q.id); if (!b) return "";
    const e = erreurDe(q, reponses[q.id]);
    const aff = e && (force || b.dataset.touche);
    b.classList.toggle("err", !!aff);
    const m = b.querySelector(".msg"); m.hidden = !aff; m.lastChild.textContent = aff ? e : "";
    b.querySelectorAll("input,textarea,select").forEach((x) => x.setAttribute("aria-invalid", aff ? "true" : "false"));
    return e;
  };
  for (const q of schema.champs || []) {
    if (q.type === "section") { form.append(h("div", { class: "dzw-fo-sec" }, h("b", {}, q.label || "Section"), q.aide ? h("p", {}, q.aide) : null)); continue; }
    const id = `dzw-fo-${q.id}-${Math.random().toString(36).slice(2, 6)}`;
    const msg = h("div", { class: "msg", id: id + "-m", role: "alert", hidden: true }, h("i", { class: "fas fa-exclamation-circle" }), h("span", {}));
    const aide = q.aide ? h("div", { class: "aide", id: id + "-a" }, q.aide) : null;
    const desc = [aide && id + "-a", id + "-m"].filter(Boolean).join(" ");
    const b = h("div", { class: "dzw-fo-q" });
    const lbl = (tag) => h(tag, tag === "label" ? { for: id } : { class: "lbl", id: id + "-l" }, q.label || typeDe(q.type).label, q.requis ? h("span", { class: "req", "aria-hidden": "true" }, "*") : null);
    const set = (v) => { reponses[q.id] = v; b.dataset.touche = "1"; montrerErreur(q); maj(); };
    const v = reponses[q.id];
    let ctl;
    if (["texte", "email", "tel", "nombre", "date"].includes(q.type)) {
      ctl = h("input", { id, type: { texte: "text", nombre: "number" }[q.type] || q.type, value: v ?? "", "aria-describedby": desc, ...(q.requis ? { "aria-required": "true" } : {}), ...(q.type === "email" ? { autocomplete: "email", inputmode: "email" } : q.type === "tel" ? { autocomplete: "tel", inputmode: "tel" } : {}), ...(q.min !== undefined && q.min !== "" ? { min: q.min } : {}), ...(q.max !== undefined && q.max !== "" ? { max: q.max } : {}), oninput: (e) => set(q.type === "nombre" && e.target.value !== "" ? +e.target.value : e.target.value), onblur: () => { b.dataset.touche = "1"; montrerErreur(q); } });
      b.append(...[lbl("label"), aide, ctl].filter(Boolean));
    } else if (q.type === "zone") {
      ctl = h("textarea", { id, "aria-describedby": desc, ...(q.requis ? { "aria-required": "true" } : {}), oninput: (e) => set(e.target.value), onblur: () => { b.dataset.touche = "1"; montrerErreur(q); } }); ctl.value = v ?? "";
      b.append(...[lbl("label"), aide, ctl].filter(Boolean));
    } else if (q.type === "choix" || q.type === "cases" || q.type === "oui_non") {
      const opts = q.type === "oui_non" ? ["Oui", "Non"] : q.options || [];
      const multi = q.type === "cases";
      const grp = h("div", { class: "opts", role: multi ? "group" : "radiogroup", "aria-labelledby": id + "-l", "aria-describedby": desc });
      opts.forEach((o) => {
        const coche = multi ? (Array.isArray(v) && v.includes(o)) : v === o;
        grp.append(h("label", { class: "opt" }, h("input", { type: multi ? "checkbox" : "radio", name: id, value: o, ...(coche ? { checked: true } : {}), onchange: () => { if (multi) set([...grp.querySelectorAll("input:checked")].map((x) => x.value)); else set(o); } }), h("span", {}, o)));
      });
      b.append(...[lbl("div"), aide, grp].filter(Boolean));
    } else if (q.type === "note") {
      const max = +q.max || 5;
      const et = h("div", { class: "etoiles", role: "radiogroup", "aria-labelledby": id + "-l" });
      const peindre = (n) => et.querySelectorAll("button").forEach((x, i) => { x.classList.toggle("on", i < n); x.setAttribute("aria-checked", i + 1 === n ? "true" : "false"); });
      for (let i = 1; i <= max; i++) et.append(h("button", { type: "button", role: "radio", "aria-label": `${i} sur ${max}`, onclick: () => { set(i); peindre(i); }, onkeydown: (e) => { const d = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1 }[e.key]; if (d) { e.preventDefault(); const n = Math.max(1, Math.min(max, (reponses[q.id] || 0) + d)); set(n); peindre(n); et.children[n - 1].focus(); } } }, "★"));
      peindre(+v || 0);
      b.append(...[lbl("div"), aide, et].filter(Boolean));
    }
    b.append(msg);
    blocs.set(q.id, b);
    form.append(b);
  }
  if (!apercu) form.append(h("div", { class: "dzw-fo-bilan", hidden: true, "aria-live": "polite" }));
  hote.append(form);
  const valider = () => {
    const fautes = (schema.champs || []).filter((q) => q.type !== "section" && montrerErreur(q, true));
    const bil = form.querySelector(".dzw-fo-bilan");
    if (bil) { bil.hidden = false; bil.className = "dzw-fo-bilan " + (fautes.length ? "ko" : "ok"); bil.innerHTML = ""; bil.append(h("i", { class: fautes.length ? "fas fa-exclamation-triangle" : "fas fa-check-circle" }), fautes.length ? `${fautes.length} réponse(s) à corriger` : "Tout est bon"); }
    if (fautes.length) { const b = blocs.get(fautes[0].id); const f = b && b.querySelector("input,textarea,button"); if (f) f.focus(); }
    return !fautes.length;
  };
  return { valider };
};

register("formulaire", (el) => {
  const c = champ(el);
  const mode = conf(el, "mode", "construire");
  el.classList.add("dzw", "dzw-fo");
  el.innerHTML = "";

  if (mode === "remplir") {
    el.classList.add("remplir");
    const sc = el.getAttribute("data-schema-champ");
    let schema = conf(el, "schema", null);
    if (!schema && sc) { const i = document.querySelector(`[name="${CSS.escape(sc)}"]`); try { schema = JSON.parse(i ? i.value : ""); } catch (e) { schema = null; } }
    if (!schema || !Array.isArray(schema.champs)) { el.append(h("div", { class: "dzw-fo-vide" }, "Aucun formulaire à afficher.")); return; }
    let rep = {}; try { rep = JSON.parse(c.get() || "{}") || {}; } catch (e) { rep = {}; }
    const col = h("div", { class: "dzw-fo-col" }); el.append(col);
    const f = rendreFormulaire(col, schema, rep, (r) => c.set(JSON.stringify(r)));
    /* à l'envoi du formulaire Saltcorn : on bloque tant qu'il reste des erreurs */
    const form = el.closest("form");
    if (form) form.addEventListener("submit", (e) => { if (!f.valider()) { e.preventDefault(); e.stopImmediatePropagation(); } }, true);
    el.dzFormulaire = { valider: f.valider, reponses: () => ({ ...rep }) };
    return;
  }

  let schema = { v: 1, titre: "", intro: "", champs: [] };
  try { const v = c.get(); if (v) { const d = JSON.parse(v); if (d && Array.isArray(d.champs)) schema = { v: 1, titre: d.titre || "", intro: d.intro || "", champs: d.champs }; } } catch (e) { /* vide */ }
  let sel = null; let t = null;
  const sauver = () => { clearTimeout(t); t = setTimeout(() => c.set(JSON.stringify(schema)), 250); apercu(); };
  const gauche = h("div", { class: "dzw-fo-col" }), droite = h("div", { class: "dzw-fo-col", "aria-label": "Aperçu" });
  el.append(gauche, droite);
  const apercuRep = {};
  const apercu = () => { droite.innerHTML = ""; droite.append(h("h5", {}, "Aperçu : ce que verront les personnes")); const hote = h("div"); droite.append(hote); if (!schema.champs.length && !schema.titre) hote.append(h("div", { class: "dzw-fo-vide" }, "L'aperçu apparaîtra ici.")); else rendreFormulaire(hote, schema, apercuRep, null, true); };
  const liste = h("div", { role: "list" });
  const rendre = () => {
    gauche.innerHTML = "";
    const titre = h("input", { type: "text", value: schema.titre, placeholder: "Titre du formulaire", "aria-label": "Titre du formulaire", style: { width: "100%", fontWeight: "700", fontSize: "1rem", marginBottom: "6px" }, oninput: (e) => { schema.titre = e.target.value; sauver(); } });
    const intro = h("input", { type: "text", value: schema.intro, placeholder: "Phrase d'introduction (facultatif)", "aria-label": "Introduction", style: { width: "100%", marginBottom: "12px" }, oninput: (e) => { schema.intro = e.target.value; sauver(); } });
    gauche.append(h("h5", {}, "Construire"), titre, intro, h("div", { class: "dzw-fo-types", role: "toolbar", "aria-label": "Ajouter une question" }, ...TYPES.map((x) => btn(x.icone, x.label, () => ajouter(x.t), { class: "dzw-b garde" }))), liste);
    liste.innerHTML = "";
    if (!schema.champs.length) liste.append(h("div", { class: "dzw-fo-vide" }, "Choisis un type de question ci-dessus pour commencer."));
    schema.champs.forEach((q, i) => {
      const d = typeDe(q.type);
      const it = h("div", { class: "dzw-fo-it" + (sel === q.id ? " sel" : ""), role: "listitem" },
        h("i", { class: d.icone, style: { marginTop: "4px", opacity: ".6" } }),
        h("div", { class: "corps", tabindex: 0, role: "button", "aria-expanded": sel === q.id ? "true" : "false", onclick: () => { sel = sel === q.id ? null : q.id; rendre(); }, onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sel = sel === q.id ? null : q.id; rendre(); } } }, h("b", {}, q.label || d.label, q.requis ? " *" : ""), h("small", {}, d.label)),
        h("div", { class: "ctl" },
          h("button", { type: "button", title: "Monter", "aria-label": "Monter", disabled: i === 0, onclick: () => bouger(i, -1) }, h("i", { class: "fas fa-arrow-up" })),
          h("button", { type: "button", title: "Descendre", "aria-label": "Descendre", disabled: i === schema.champs.length - 1, onclick: () => bouger(i, 1) }, h("i", { class: "fas fa-arrow-down" })),
          h("button", { type: "button", title: "Dupliquer", "aria-label": "Dupliquer", onclick: () => { schema.champs.splice(i + 1, 0, { ...JSON.parse(JSON.stringify(q)), id: uid() }); sauver(); rendre(); } }, h("i", { class: "far fa-copy" })),
          h("button", { type: "button", title: "Supprimer", "aria-label": "Supprimer", onclick: () => { schema.champs.splice(i, 1); if (sel === q.id) sel = null; sauver(); rendre(); } }, h("i", { class: "fas fa-trash" }))));
      liste.append(it);
      if (sel === q.id) liste.append(editeur(q));
    });
  };
  const editeur = (q) => {
    const d = typeDe(q.type);
    const box = h("div", { class: "dzw-fo-edit" });
    const txt = (lab, cle, ph) => [h("label", {}, lab), h("input", { type: "text", value: q[cle] ?? "", placeholder: ph || "", oninput: (e) => { q[cle] = e.target.value; sauver(); const b = box.previousSibling && box.previousSibling.querySelector("b"); if (b && cle === "label") b.textContent = q.label || d.label; } })];
    box.append(...txt(q.type === "section" ? "Titre de la section" : "Question", "label"), ...txt(q.type === "section" ? "Texte sous le titre" : "Aide (facultatif)", "aide"));
    if (d.options) { const ta = h("textarea", { oninput: (e) => { q.options = e.target.value.split("\n").map((x) => x.trim()).filter(Boolean); sauver(); } }); ta.value = (q.options || []).join("\n"); box.append(h("label", {}, "Réponses possibles (une par ligne)"), ta); }
    if (q.type === "nombre") box.append(...txt("Minimum", "min"), ...txt("Maximum", "max"));
    if (q.type === "note") box.append(...txt("Nombre d'étoiles", "max", "5"));
    if (q.type !== "section") box.append(h("label", { style: { display: "flex", gap: "8px", alignItems: "center", fontSize: ".85rem", opacity: 1 } }, h("input", { type: "checkbox", ...(q.requis ? { checked: true } : {}), onchange: (e) => { q.requis = e.target.checked; sauver(); rendre(); } }), "Réponse obligatoire"));
    return box;
  };
  const ajouter = (t) => { const d = typeDe(t); const q = { id: uid(), type: t, label: t === "section" ? "Nouvelle section" : "", ...(d.options ? { options: ["Option 1", "Option 2"] } : {}) }; schema.champs.push(q); sel = q.id; sauver(); rendre(); const f = liste.querySelector(".dzw-fo-edit input"); if (f) f.focus(); };
  const bouger = (i, d) => { const j = i + d; if (j < 0 || j >= schema.champs.length) return; [schema.champs[i], schema.champs[j]] = [schema.champs[j], schema.champs[i]]; sauver(); rendre(); };
  rendre(); apercu();
  el.dzFormulaire = { schema: () => JSON.parse(JSON.stringify(schema)) };
});
