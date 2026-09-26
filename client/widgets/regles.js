/* Règles : construire des conditions sans écrire de code.
   « Si le montant est supérieur à 500 ET le service est Achats, OU … »
   Sert aux filtres, aux alertes, aux conditions d'un parcours, aux droits…

   data-champs : JSON [{ nom, label, type: texte|nombre|date|choix|oui_non, options }]
   data-champ  : champ où enregistrer { v, logique, groupes: [{ logique, conditions: [{ champ, op, valeur }] }],
                 texte: phrase en français, expression: JavaScript (sur ctx) }
   L'expression est prête pour une étape « condition » du parcours (bloc Exécuter un parcours). */
import { register, css, h, conf, champ, btn } from "./_commun.js";

css("regles", `.dzw-rg{padding:0}
.dzw-rg-corps{padding:12px;display:grid;gap:10px}
.dzw-rg-gr{border:1px solid var(--dz-border,#e5e7eb);border-radius:12px;padding:10px;background:var(--dz-surface,#fff)}
.dzw-rg-gr-t{display:flex;gap:8px;align-items:center;font-size:.8rem;font-weight:600;margin-bottom:8px;flex-wrap:wrap}
.dzw-rg-c{display:grid;grid-template-columns:minmax(120px,1.2fr) minmax(120px,1fr) minmax(100px,1fr) auto;gap:6px;align-items:center;margin-bottom:6px}
.dzw-rg-c select,.dzw-rg-c input{width:100%;box-sizing:border-box;min-height:36px}
.dzw-rg-c .x{border:0;background:none;cursor:pointer;opacity:.6;padding:6px;color:inherit;border-radius:6px}
.dzw-rg-c .x:hover,.dzw-rg-c .x:focus-visible{opacity:1;background:var(--dz-surface-2,#f1f5f9)}
.dzw-rg-lien{justify-self:center;font:700 .72rem system-ui,sans-serif;letter-spacing:.06em;padding:3px 10px;border-radius:99px;border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface-2,#f8fafc);cursor:pointer;color:inherit}
.dzw-rg-lien:hover,.dzw-rg-lien:focus-visible{border-color:var(--dz-primary,#2563eb)}
.dzw-rg-phrase{padding:10px 12px;border-top:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface-2,#f9fafb);font-size:.88rem;display:flex;gap:8px;align-items:flex-start}
.dzw-rg-phrase i{margin-top:3px;opacity:.6}
.dzw-rg-code{margin:0;padding:8px 12px;font:.75rem/1.5 ui-monospace,monospace;opacity:.7;overflow-x:auto;border-top:1px dashed var(--dz-border,#e5e7eb)}
@media (max-width:640px){.dzw-rg-c{grid-template-columns:1fr 1fr}.dzw-rg-c>:nth-child(3){grid-column:1/2}}`);

export const OPS = {
  texte: [["egal", "est"], ["different", "n'est pas"], ["contient", "contient"], ["commence", "commence par"], ["vide", "est vide"], ["rempli", "est rempli"]],
  nombre: [["egal", "="], ["different", "≠"], ["sup", ">"], ["supeg", "≥"], ["inf", "<"], ["infeg", "≤"], ["vide", "est vide"], ["rempli", "est rempli"]],
  date: [["avant", "avant le"], ["apres", "après le"], ["egal", "le"], ["vide", "est vide"], ["rempli", "est rempli"]],
  choix: [["egal", "est"], ["different", "n'est pas"], ["vide", "est vide"], ["rempli", "est rempli"]],
  oui_non: [["vrai", "est oui"], ["faux", "est non"]],
};
const SANS_VALEUR = new Set(["vide", "rempli", "vrai", "faux"]);
const q = (v) => JSON.stringify(v == null ? "" : String(v));
const acc = (nom) => `ctx[${JSON.stringify(nom)}]`;

/* expression JavaScript d'une condition (sûre : noms et valeurs toujours entre guillemets) */
export const exprDe = (c, f) => {
  const a = acc(c.champ), t = (f && f.type) || "texte", v = c.valeur;
  const num = (x) => (x === "" || x == null || Number.isNaN(+x) ? "NaN" : String(+x));
  switch (c.op) {
    case "vide": return `(${a} === undefined || ${a} === null || ${a} === "")`;
    case "rempli": return `!(${a} === undefined || ${a} === null || ${a} === "")`;
    case "vrai": return `(${a} === true || ${a} === "true" || ${a} === "Oui" || ${a} === 1)`;
    case "faux": return `!(${a} === true || ${a} === "true" || ${a} === "Oui" || ${a} === 1)`;
    case "contient": return `String(${a} ?? "").toLowerCase().includes(${q(String(v).toLowerCase())})`;
    case "commence": return `String(${a} ?? "").toLowerCase().startsWith(${q(String(v).toLowerCase())})`;
    case "sup": return `Number(${a}) > ${num(v)}`; case "supeg": return `Number(${a}) >= ${num(v)}`;
    case "inf": return `Number(${a}) < ${num(v)}`; case "infeg": return `Number(${a}) <= ${num(v)}`;
    case "avant": return `new Date(${a}) < new Date(${q(v)})`; case "apres": return `new Date(${a}) > new Date(${q(v)})`;
    case "different": return t === "nombre" ? `Number(${a}) !== ${num(v)}` : `String(${a} ?? "") !== ${q(v)}`;
    default: return t === "nombre" ? `Number(${a}) === ${num(v)}` : t === "date" ? `String(${a} ?? "").slice(0, 10) === ${q(v)}` : `String(${a} ?? "") === ${q(v)}`;
  }
};
export const compiler = (doc, champs) => {
  const fOf = (n) => champs.find((x) => x.nom === n);
  const gs = doc.groupes.map((g) => g.conditions.filter((c) => c.champ && c.op)).map((cs, i) => ({ cs, logique: doc.groupes[i].logique }));
  const exGr = gs.filter((g) => g.cs.length).map((g) => "(" + g.cs.map((c) => exprDe(c, fOf(c.champ))).join(g.logique === "ou" ? " || " : " && ") + ")");
  const expression = exGr.length ? exGr.join(doc.logique === "ou" ? " || " : " && ") : "true";
  const phrase = (c) => { const f = fOf(c.champ) || { label: c.champ }; const op = (OPS[f.type || "texte"] || OPS.texte).find((o) => o[0] === c.op); return `${f.label || c.champ} ${op ? op[1] : c.op}${SANS_VALEUR.has(c.op) ? "" : ` « ${c.valeur ?? ""} »`}`; };
  const txtGr = gs.filter((g) => g.cs.length).map((g) => g.cs.map(phrase).join(g.logique === "ou" ? " ou " : " et "));
  const texte = txtGr.length ? "Si " + (txtGr.length > 1 ? txtGr.map((t) => `(${t})`).join(doc.logique === "ou" ? " ou " : " et ") : txtGr[0]) : "Toujours vrai (aucune condition)";
  return { expression, texte };
};

register("regles", (el) => {
  const c = champ(el);
  const champs = conf(el, "champs", [{ nom: "montant", label: "Montant", type: "nombre" }, { nom: "service", label: "Service", type: "choix", options: ["Achats", "Ventes", "RH"] }, { nom: "urgent", label: "Urgent", type: "oui_non" }]);
  let doc = { v: 1, logique: "et", groupes: [{ logique: "et", conditions: [] }] };
  try { const v = c.get(); if (v) { const d = JSON.parse(v); if (d && Array.isArray(d.groupes)) doc = { v: 1, logique: d.logique || "et", groupes: d.groupes }; } } catch (e) { /* vide */ }
  el.classList.add("dzw", "dzw-rg");
  el.innerHTML = "";
  const corps = h("div", { class: "dzw-rg-corps" }), phraseEl = h("div", { class: "dzw-rg-phrase", "aria-live": "polite" }), codeEl = h("pre", { class: "dzw-rg-code" });
  let t = null;
  const sauver = () => { const r = compiler(doc, champs); phraseEl.innerHTML = ""; phraseEl.append(h("i", { class: "fas fa-comment-alt" }), h("span", {}, r.texte)); codeEl.textContent = r.expression; clearTimeout(t); t = setTimeout(() => c.set(JSON.stringify({ ...doc, ...r })), 200); };
  const bascule = (obj, cle) => h("button", { type: "button", class: "dzw-rg-lien", title: "Changer ET / OU", onclick: () => { obj[cle] = obj[cle] === "ou" ? "et" : "ou"; rendre(); } }, obj[cle] === "ou" ? "OU" : "ET");
  const ligne = (g, cnd) => {
    const f = champs.find((x) => x.nom === cnd.champ) || champs[0] || { type: "texte" };
    const ops = OPS[f.type || "texte"] || OPS.texte;
    if (!ops.some((o) => o[0] === cnd.op)) cnd.op = ops[0][0];
    const selChamp = h("select", { "aria-label": "Champ", onchange: (e) => { cnd.champ = e.target.value; cnd.valeur = ""; rendre(); } }, ...champs.map((x) => h("option", { value: x.nom, ...(x.nom === f.nom ? { selected: true } : {}) }, x.label || x.nom)));
    cnd.champ = f.nom;
    const selOp = h("select", { "aria-label": "Opérateur", onchange: (e) => { cnd.op = e.target.value; rendre(); } }, ...ops.map((o) => h("option", { value: o[0], ...(o[0] === cnd.op ? { selected: true } : {}) }, o[1])));
    let val;
    if (SANS_VALEUR.has(cnd.op)) val = h("span", {});
    else if (f.type === "choix") val = h("select", { "aria-label": "Valeur", onchange: (e) => { cnd.valeur = e.target.value; sauver(); } }, h("option", { value: "" }, "…"), ...(f.options || []).map((o) => h("option", { value: o, ...(o === cnd.valeur ? { selected: true } : {}) }, o)));
    else val = h("input", { type: f.type === "nombre" ? "number" : f.type === "date" ? "date" : "text", value: cnd.valeur ?? "", "aria-label": "Valeur", oninput: (e) => { cnd.valeur = e.target.value; sauver(); } });
    const x = h("button", { type: "button", class: "x", title: "Retirer", "aria-label": "Retirer la condition", onclick: () => { g.conditions = g.conditions.filter((y) => y !== cnd); rendre(); } }, h("i", { class: "fas fa-times" }));
    return h("div", { class: "dzw-rg-c" }, selChamp, selOp, val, x);
  };
  const rendre = () => {
    corps.innerHTML = "";
    doc.groupes.forEach((g, gi) => {
      if (gi) corps.append(bascule(doc, "logique"));
      const box = h("div", { class: "dzw-rg-gr", role: "group", "aria-label": `Groupe ${gi + 1}` });
      box.append(h("div", { class: "dzw-rg-gr-t" }, h("span", {}, doc.groupes.length > 1 ? `Groupe ${gi + 1}` : "Conditions"), g.conditions.length > 1 ? h("span", { style: { opacity: ".6", fontWeight: 400 } }, "reliées par") : null, g.conditions.length > 1 ? bascule(g, "logique") : null));
      g.conditions.forEach((cnd) => box.append(ligne(g, cnd)));
      if (!g.conditions.length) box.append(h("div", { style: { opacity: ".6", fontSize: ".85rem", marginBottom: "6px" } }, "Aucune condition : toujours vrai."));
      box.append(h("div", { style: { display: "flex", gap: "6px", flexWrap: "wrap" } }, btn("fas fa-plus", "Ajouter une condition", () => { g.conditions.push({ champ: (champs[0] || {}).nom, op: "", valeur: "" }); rendre(); const s = corps.querySelectorAll(`[aria-label="Groupe ${gi + 1}"] select[aria-label="Champ"]`); if (s.length) s[s.length - 1].focus(); }, { class: "dzw-b garde" }), doc.groupes.length > 1 ? btn("fas fa-trash", "Retirer le groupe", () => { doc.groupes.splice(gi, 1); rendre(); }, { class: "dzw-b garde" }) : null));
      corps.append(box);
    });
    corps.append(h("div", {}, btn("fas fa-layer-group", "Ajouter un groupe (OU…)", () => { doc.groupes.push({ logique: "et", conditions: [{ champ: (champs[0] || {}).nom, op: "", valeur: "" }] }); if (doc.groupes.length === 2) doc.logique = "ou"; rendre(); }, { class: "dzw-b garde" })));
    sauver();
  };
  el.append(corps, phraseEl);
  /* l'expression JavaScript : pour les développeurs seulement (data-code="true") */
  if (conf(el, "code", false)) el.append(codeEl);
  rendre();
  el.dzRegles = { lire: () => ({ ...doc, ...compiler(doc, champs) }) };
});
