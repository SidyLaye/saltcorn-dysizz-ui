/* Document : éditeur par blocs (façon Notion) pour wikis, comptes rendus,
   procédures, fiches, bases de connaissance livrées à un client.

   Clavier : Entrée = nouveau bloc, « / » en début de bloc = changer de type,
   Retour arrière sur un bloc vide = le retirer, Alt+↑/↓ = déplacer le bloc,
   Ctrl+B / Ctrl+I = gras / italique, Ctrl+K = lien.
   Enregistré dans data-champ : { v: 1, blocs: [{ t, html, fait }] }.
   Le HTML est nettoyé (gras, italique, souligné, code, lien http(s) seulement).
   data-lecture="true" : affichage seul. */
import { register, css, h, conf, champ } from "./_commun.js";

css("document", `.dzw-doc{padding:0}
.dzw-doc-corps{padding:18px 18px 18px 44px;min-height:var(--doc-h,260px);font-size:1rem;line-height:1.65}
.dzw-doc.lecture .dzw-doc-corps{padding:18px}
.dzw-doc-b{position:relative;margin:2px 0;border-radius:6px}
.dzw-doc-b>[contenteditable]{outline:none;min-height:1.6em;padding:2px 4px;border-radius:6px;overflow-wrap:anywhere}
.dzw-doc-b>[contenteditable]:focus{background:color-mix(in srgb,var(--dz-primary,#2563eb) 5%,transparent)}
.dzw-doc-b>[contenteditable]:empty::before{content:attr(data-ph);opacity:.4;pointer-events:none}
.dzw-doc-b .poignee{position:absolute;left:-30px;top:3px;width:22px;height:22px;border:0;background:none;border-radius:5px;opacity:0;cursor:pointer;color:inherit;display:grid;place-items:center}
.dzw-doc-b:hover .poignee,.dzw-doc-b:focus-within .poignee,.dzw-doc-b .poignee:focus-visible{opacity:.55}
.dzw-doc-b .poignee:hover{opacity:1;background:var(--dz-surface-2,#f1f5f9)}
.dzw-doc-b.t-h1>[contenteditable]{font-size:1.75rem;font-weight:800;line-height:1.25;margin-top:.6em}
.dzw-doc-b.t-h2>[contenteditable]{font-size:1.35rem;font-weight:700;line-height:1.3;margin-top:.5em}
.dzw-doc-b.t-h3>[contenteditable]{font-size:1.1rem;font-weight:700;margin-top:.4em}
.dzw-doc-b.t-puce,.dzw-doc-b.t-num,.dzw-doc-b.t-tache{display:flex;gap:8px;align-items:flex-start}
.dzw-doc-b .marque{flex:none;min-width:1.4em;text-align:right;opacity:.7;padding-top:2px}
.dzw-doc-b.t-tache input{margin-top:.45em;width:17px;height:17px;accent-color:var(--dz-primary,#2563eb)}
.dzw-doc-b.t-tache.fait>[contenteditable]{text-decoration:line-through;opacity:.55}
.dzw-doc-b.t-puce>[contenteditable],.dzw-doc-b.t-num>[contenteditable],.dzw-doc-b.t-tache>[contenteditable]{flex:1}
.dzw-doc-b.t-citation>[contenteditable]{border-left:3px solid var(--dz-primary,#2563eb);padding-left:14px;font-style:italic;opacity:.85}
.dzw-doc-b.t-code>[contenteditable]{font:.88rem/1.55 ui-monospace,monospace;background:var(--dz-surface-2,#f1f5f9);padding:10px 12px;white-space:pre-wrap}
.dzw-doc-b.t-encadre>[contenteditable]{background:color-mix(in srgb,#f59e0b 12%,transparent);border:1px solid color-mix(in srgb,#f59e0b 35%,transparent);padding:10px 12px 10px 38px}
.dzw-doc-b.t-encadre::before{content:"💡";position:absolute;left:12px;top:10px}
.dzw-doc-b.t-separateur{padding:10px 0}.dzw-doc-b.t-separateur hr{margin:0;border:0;border-top:1px solid var(--dz-border,#e5e7eb)}
.dzw-doc-b a{color:var(--dz-primary,#2563eb);text-decoration:underline}
.dzw-doc-b code{font-family:ui-monospace,monospace;font-size:.88em;background:var(--dz-surface-2,#f1f5f9);padding:1px 5px;border-radius:4px}
.dzw-doc-menu{position:absolute;z-index:5;width:250px;max-height:300px;overflow:auto;background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e5e7eb);border-radius:12px;box-shadow:0 16px 40px -16px rgba(15,23,42,.35);padding:6px}
.dzw-doc-menu button{display:flex;gap:10px;align-items:center;width:100%;border:0;background:none;padding:7px 9px;border-radius:8px;text-align:left;cursor:pointer;color:inherit;font-size:.88rem}
.dzw-doc-menu button i{width:18px;text-align:center;opacity:.6}
.dzw-doc-menu button.on,.dzw-doc-menu button:hover{background:var(--dz-surface-2,#f1f5f9)}
.dzw-doc-menu small{display:block;opacity:.55;font-size:.72rem}
.dzw-doc-aide{font-size:.75rem;opacity:.55;padding:6px 18px;border-top:1px solid var(--dz-border,#e5e7eb)}
@media (max-width:640px){.dzw-doc-corps{padding:14px 12px 14px 34px}.dzw-doc-b .poignee{left:-28px;opacity:.4}}`);

export const TYPES = [
  { t: "p", label: "Texte", icone: "fas fa-paragraph", aide: "Paragraphe simple" },
  { t: "h1", label: "Grand titre", icone: "fas fa-heading", aide: "Titre de page" },
  { t: "h2", label: "Titre", icone: "fas fa-heading", aide: "Titre de section" },
  { t: "h3", label: "Sous-titre", icone: "fas fa-heading", aide: "Petit titre" },
  { t: "puce", label: "Liste à puces", icone: "fas fa-list-ul", aide: "• élément" },
  { t: "num", label: "Liste numérotée", icone: "fas fa-list-ol", aide: "1. élément" },
  { t: "tache", label: "Case à cocher", icone: "far fa-check-square", aide: "À faire / fait" },
  { t: "citation", label: "Citation", icone: "fas fa-quote-left", aide: "Mise en avant" },
  { t: "encadre", label: "Encadré", icone: "far fa-lightbulb", aide: "Astuce, attention" },
  { t: "code", label: "Code", icone: "fas fa-code", aide: "Texte à chasse fixe" },
  { t: "separateur", label: "Séparateur", icone: "fas fa-minus", aide: "Ligne horizontale" },
];
const PH = { p: "Écris, ou tape « / » pour choisir un type de bloc", h1: "Grand titre", h2: "Titre", h3: "Sous-titre", puce: "Élément", num: "Élément", tache: "À faire", citation: "Citation", encadre: "Astuce ou point d'attention", code: "Code" };

/* nettoyage : seulement b, strong, i, em, u, code, br, a[href http(s)/mailto] */
export const nettoyer = (html) => {
  const tpl = document.createElement("template");
  tpl.innerHTML = String(html || "");
  const OK = new Set(["B", "STRONG", "I", "EM", "U", "CODE", "BR", "A"]);
  const marcher = (n) => {
    for (const k of [...n.childNodes]) {
      if (k.nodeType === 3) continue;
      if (k.nodeType !== 1 || !OK.has(k.tagName)) { if (k.nodeType === 1 && !/^(SCRIPT|STYLE|IFRAME|OBJECT|EMBED|TEMPLATE)$/.test(k.tagName)) { marcher(k); k.replaceWith(...k.childNodes); } else k.remove(); continue; }
      for (const a of [...k.attributes]) if (!(k.tagName === "A" && a.name === "href")) k.removeAttribute(a.name);
      if (k.tagName === "A") { const href = k.getAttribute("href") || ""; if (!/^(https?:|mailto:)/i.test(href)) k.removeAttribute("href"); else { k.setAttribute("target", "_blank"); k.setAttribute("rel", "noopener noreferrer"); } }
      marcher(k);
    }
  };
  marcher(tpl.content);
  const d = document.createElement("div"); d.append(tpl.content); return d.innerHTML;
};

register("document", (el) => {
  const c = champ(el);
  const lecture = conf(el, "lecture", false);
  let blocs = [];
  try { const v = c.get(); if (v) { const d = JSON.parse(v); if (d && Array.isArray(d.blocs)) blocs = d.blocs; } } catch (e) { /* vide */ }
  if (!blocs.length) blocs = [{ t: "p", html: "" }];
  el.classList.add("dzw", "dzw-doc");
  if (lecture) el.classList.add("lecture");
  el.style.setProperty("--doc-h", conf(el, "hauteur", 260) + "px");
  el.innerHTML = "";
  const corps = h("div", { class: "dzw-doc-corps", role: "document" });
  el.append(corps);
  if (!lecture) el.append(h("div", { class: "dzw-doc-aide" }, "« / » pour changer de type · Entrée pour un nouveau bloc · Alt+↑/↓ pour déplacer · Ctrl+B, Ctrl+I, Ctrl+K"));
  let t = null, menu = null;
  const sauver = () => { clearTimeout(t); t = setTimeout(() => c.set(JSON.stringify({ v: 1, blocs: blocs.map((b) => ({ t: b.t, html: b.t === "separateur" ? "" : nettoyer(b.html), ...(b.t === "tache" ? { fait: !!b.fait } : {}) })) })), 300); };
  const ed = (i) => corps.children[i] && corps.children[i].querySelector("[contenteditable]");
  const focusFin = (e, debut) => { if (!e) return; e.focus(); const r = document.createRange(); r.selectNodeContents(e); r.collapse(!!debut); const s = getSelection(); s.removeAllRanges(); s.addRange(r); };
  const numero = (i) => { let n = 1; for (let k = i - 1; k >= 0 && blocs[k].t === "num"; k--) n++; return n; };

  const blocEl = (b, i) => {
    const w = h("div", { class: `dzw-doc-b t-${b.t}${b.fait ? " fait" : ""}` });
    if (b.t === "separateur") { w.append(h("hr")); if (!lecture) w.append(poignee(i)); w.tabIndex = lecture ? -1 : 0; w.addEventListener("keydown", (e) => { if (e.key === "Backspace" || e.key === "Delete") { e.preventDefault(); retirer(i); } }); return w; }
    const e = h("div", { contenteditable: lecture ? "false" : "true", "data-ph": lecture ? "" : PH[b.t] || "", role: "textbox", "aria-multiline": b.t === "code" ? "true" : "false", "aria-label": (TYPES.find((x) => x.t === b.t) || TYPES[0]).label });
    e.innerHTML = nettoyer(b.html);
    if (b.t === "puce") w.append(h("span", { class: "marque", "aria-hidden": "true" }, "•"));
    if (b.t === "num") w.append(h("span", { class: "marque", "aria-hidden": "true" }, numero(i) + "."));
    if (b.t === "tache") w.append(h("input", { type: "checkbox", "aria-label": "Fait", ...(b.fait ? { checked: true } : {}), ...(lecture ? { disabled: true } : {}), onchange: (x) => { b.fait = x.target.checked; w.classList.toggle("fait", b.fait); sauver(); } }));
    w.append(e);
    if (lecture) return w;
    w.append(poignee(i));
    e.addEventListener("input", () => { b.html = e.innerHTML; if (e.textContent === "/" ) ouvrirMenu(i, e); else if (menu && !e.textContent.startsWith("/")) fermerMenu(); else if (menu) filtrerMenu(e.textContent.slice(1)); sauver(); });
    e.addEventListener("paste", (x) => { x.preventDefault(); const txt = (x.clipboardData || window.clipboardData).getData("text/plain"); document.execCommand("insertText", false, txt); });
    e.addEventListener("keydown", (x) => {
      if (menu && ["ArrowDown", "ArrowUp", "Enter", "Escape"].includes(x.key)) { x.preventDefault(); menuTouche(x.key); return; }
      const idx = [...corps.children].indexOf(w);
      if (x.key === "Enter" && !x.shiftKey && b.t !== "code") {
        x.preventDefault();
        /* liste vide + Entrée : on sort de la liste */
        if (["puce", "num", "tache"].includes(b.t) && !e.textContent.trim()) { b.t = "p"; rendre(); focusFin(ed(idx)); return; }
        const s = getSelection(); let reste = "";
        if (s.rangeCount) { const r = s.getRangeAt(0); const r2 = r.cloneRange(); r2.selectNodeContents(e); r2.setStart(r.endContainer, r.endOffset); const frag = r2.extractContents(); const d = document.createElement("div"); d.append(frag); reste = d.innerHTML; b.html = e.innerHTML; }
        const nt = ["puce", "num", "tache"].includes(b.t) ? b.t : "p";
        blocs.splice(idx + 1, 0, { t: nt, html: reste }); sauver(); rendre(); focusFin(ed(idx + 1), true);
      } else if (x.key === "Backspace" && !e.textContent && !e.querySelector("br+*")) {
        if (b.t !== "p") { x.preventDefault(); b.t = "p"; rendre(); focusFin(ed(idx)); return; }
        if (blocs.length > 1) { x.preventDefault(); retirer(idx); }
      } else if (x.altKey && (x.key === "ArrowUp" || x.key === "ArrowDown")) {
        x.preventDefault(); const j = idx + (x.key === "ArrowUp" ? -1 : 1); if (j < 0 || j >= blocs.length) return;
        [blocs[idx], blocs[j]] = [blocs[j], blocs[idx]]; sauver(); rendre(); focusFin(ed(j));
      } else if (x.key === "ArrowUp" && idx > 0 && caretAuDebut(e)) { x.preventDefault(); focusFin(ed(idx - 1)); }
      else if (x.key === "ArrowDown" && idx < blocs.length - 1 && caretALaFin(e)) { x.preventDefault(); focusFin(ed(idx + 1), true); }
      else if ((x.ctrlKey || x.metaKey) && ["b", "i", "u"].includes(x.key.toLowerCase())) { x.preventDefault(); document.execCommand({ b: "bold", i: "italic", u: "underline" }[x.key.toLowerCase()]); }
      else if ((x.ctrlKey || x.metaKey) && x.key.toLowerCase() === "k") { x.preventDefault(); const url = window.prompt("Adresse du lien (https://…)"); if (url && /^(https?:|mailto:)/i.test(url.trim())) document.execCommand("createLink", false, url.trim()); }
    });
    return w;
  };
  const caretAuDebut = (e) => { const s = getSelection(); if (!s.rangeCount) return false; const r = s.getRangeAt(0).cloneRange(); r.selectNodeContents(e); r.setEnd(s.getRangeAt(0).startContainer, s.getRangeAt(0).startOffset); return r.toString().length === 0; };
  const caretALaFin = (e) => { const s = getSelection(); if (!s.rangeCount) return false; const r = s.getRangeAt(0).cloneRange(); r.selectNodeContents(e); r.setStart(s.getRangeAt(0).endContainer, s.getRangeAt(0).endOffset); return r.toString().length === 0; };
  const poignee = (i) => h("button", { type: "button", class: "poignee", title: "Changer le type", "aria-label": "Changer le type du bloc", onclick: (e) => { e.stopPropagation(); ouvrirMenu(i, corps.children[i], true); } }, h("i", { class: "fas fa-grip-vertical" }));
  const retirer = (idx) => { blocs.splice(idx, 1); if (!blocs.length) blocs.push({ t: "p", html: "" }); sauver(); rendre(); focusFin(ed(Math.max(0, idx - 1))); };

  /* ---- menu « / » ---- */
  let menuIdx = 0, menuBloc = 0, menuListe = TYPES;
  const ouvrirMenu = (i, ancre, depuisPoignee) => {
    fermerMenu(); menuBloc = i; menuIdx = 0; menuListe = TYPES;
    menu = h("div", { class: "dzw-doc-menu", role: "listbox", "aria-label": "Type de bloc" });
    const r = ancre.getBoundingClientRect(), rr = el.getBoundingClientRect();
    menu.style.left = Math.max(8, Math.min(r.left - rr.left, rr.width - 258)) + "px"; menu.style.top = r.bottom - rr.top + 4 + "px";
    el.append(menu); peindreMenu();
    menu.dataset.poignee = depuisPoignee ? "1" : "";
    setTimeout(() => document.addEventListener("pointerdown", dehors), 0);
  };
  const dehors = (e) => { if (menu && !menu.contains(e.target)) fermerMenu(); };
  const fermerMenu = () => { if (menu) { menu.remove(); menu = null; document.removeEventListener("pointerdown", dehors); } };
  const filtrerMenu = (q) => { const s = q.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); menuListe = TYPES.filter((x) => (x.label + " " + x.t).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").includes(s)); menuIdx = 0; peindreMenu(); };
  const peindreMenu = () => { menu.innerHTML = ""; if (!menuListe.length) { menu.append(h("div", { style: { padding: "8px", opacity: ".6", fontSize: ".85rem" } }, "Aucun type trouvé")); return; } menuListe.forEach((x, k) => menu.append(h("button", { type: "button", role: "option", class: k === menuIdx ? "on" : "", "aria-selected": k === menuIdx ? "true" : "false", onclick: () => choisirType(x.t) }, h("i", { class: x.icone }), h("span", {}, x.label, h("small", {}, x.aide))))); };
  const menuTouche = (k) => { if (k === "Escape") return fermerMenu(); if (k === "Enter") return menuListe[menuIdx] && choisirType(menuListe[menuIdx].t); menuIdx = (menuIdx + (k === "ArrowDown" ? 1 : -1) + menuListe.length) % menuListe.length; peindreMenu(); };
  const choisirType = (tp) => {
    const b = blocs[menuBloc]; const poig = menu && menu.dataset.poignee; fermerMenu();
    if (!poig) b.html = String(b.html || "").replace(/^\s*\/[^<]*/, "");
    b.t = tp;
    if (tp === "separateur") { b.html = ""; blocs.splice(menuBloc + 1, 0, { t: "p", html: "" }); sauver(); rendre(); focusFin(ed(menuBloc + 1)); return; }
    sauver(); rendre(); focusFin(ed(menuBloc));
  };

  const rendre = () => { corps.innerHTML = ""; blocs.forEach((b, i) => corps.append(blocEl(b, i))); };
  rendre();
  el.dzDocument = { lire: () => JSON.parse(JSON.stringify({ v: 1, blocs })), texte: () => corps.innerText };
});
