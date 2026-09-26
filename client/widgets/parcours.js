/* Parcours : éditeur visuel de processus (étapes reliées par des flèches).
   Sert à construire pour un client un outil de workflow, un circuit de
   validation, un organigramme, un parcours client… Le schéma est enregistré
   en JSON dans un champ ; le bloc dysizz-flow « Exécuter un parcours » sait
   le dérouler.

   Réglages (data-…) :
     champ     nom du champ où enregistrer (sinon lecture de data-valeur)
     palette   JSON : les types d'étapes proposés (voir PALETTE ci-dessous)
     hauteur   px (défaut 520)
     lecture   "true" : consultation seule (déplacement et zoom permis)
     trace     JSON : identifiants d'étapes déjà passées (mises en valeur)
     actif     identifiant de l'étape en cours

   Format : { v: 1, noeuds: [{ id, cle, type, titre, x, y, reglages }],
              liens: [{ id, de, vers, si }] } */
import { register, css, h, conf, champ, btn, download, toast } from "./_commun.js";

css("parcours", `.dzw-pc{--pc-h:520px;display:flex;flex-direction:column}
.dzw-pc-zone{position:relative;height:var(--pc-h);overflow:hidden;touch-action:none;cursor:grab;background:var(--dz-bg-soft,#f8fafc);background-image:radial-gradient(color-mix(in srgb,var(--dz-text,#0f172a) 14%,transparent) 1px,transparent 1px);background-size:22px 22px}
.dzw-pc-zone.pan{cursor:grabbing}
.dzw-pc-calque{position:absolute;left:0;top:0;transform-origin:0 0}
.dzw-pc-svg{position:absolute;left:0;top:0;width:1px;height:1px;overflow:visible;pointer-events:none;color:var(--dz-text,#334155)}
.dzw-pc-svg path.l{fill:none;stroke:color-mix(in srgb,var(--dz-text,#334155) 45%,transparent);stroke-width:2}
.dzw-pc-svg path.hit{fill:none;stroke:transparent;stroke-width:16;pointer-events:stroke;cursor:pointer}
.dzw-pc-svg g.sel path.l{stroke:var(--dz-primary,#2563eb);stroke-width:3}
.dzw-pc-svg g.passe path.l{stroke:#16a34a;stroke-width:3}
.dzw-pc-svg text{font:600 11px system-ui,sans-serif;fill:var(--dz-text,#334155);paint-order:stroke;stroke:var(--dz-bg-soft,#f8fafc);stroke-width:4px}
.dzw-pc-n{position:absolute;width:190px;border-radius:12px;background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e2e8f0);box-shadow:0 1px 2px rgba(15,23,42,.06),0 6px 16px -8px rgba(15,23,42,.18);cursor:move;user-select:none;touch-action:none}
.dzw-pc-n:focus-visible{outline:3px solid var(--dz-primary,#2563eb);outline-offset:2px}
.dzw-pc-n.sel{border-color:var(--dz-primary,#2563eb);box-shadow:0 0 0 3px color-mix(in srgb,var(--dz-primary,#2563eb) 25%,transparent)}
.dzw-pc-n.passe{border-color:#16a34a}.dzw-pc-n.actif{box-shadow:0 0 0 4px color-mix(in srgb,#f59e0b 40%,transparent);border-color:#f59e0b}
.dzw-pc-t{display:flex;align-items:center;gap:8px;padding:10px 12px}
.dzw-pc-ic{flex:none;width:28px;height:28px;border-radius:8px;display:grid;place-items:center;color:#fff;background:var(--c,#2563eb);font-size:.8rem}
.dzw-pc-t b{font-size:.86rem;line-height:1.2;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.dzw-pc-t small{display:block;font-size:.7rem;opacity:.6;font-weight:500}
.dzw-pc-p{position:absolute;width:16px;height:16px;border-radius:50%;background:var(--dz-surface,#fff);border:2px solid var(--c,#2563eb);transform:translate(-50%,-50%);cursor:crosshair}
.dzw-pc-p.in{left:0;top:50%;cursor:default}
.dzw-pc-p.out{left:100%}
.dzw-pc-p.out:hover,.dzw-pc-p.out:focus-visible{background:var(--c,#2563eb);outline:none}
.dzw-pc-p em{position:absolute;left:14px;top:-7px;font:600 10px system-ui,sans-serif;font-style:normal;opacity:.75;white-space:nowrap}
.dzw-pc-panneau{position:absolute;right:12px;top:12px;bottom:12px;width:280px;max-width:calc(100% - 24px);background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e2e8f0);border-radius:14px;box-shadow:0 18px 40px -18px rgba(15,23,42,.35);padding:14px;overflow:auto;z-index:3;cursor:default}
.dzw-pc-panneau h4{font-size:.95rem;margin:0 0 10px;display:flex;align-items:center;gap:8px}
.dzw-pc-panneau label{display:block;font-size:.75rem;font-weight:600;opacity:.75;margin:10px 0 4px}
.dzw-pc-panneau input,.dzw-pc-panneau textarea,.dzw-pc-panneau select{width:100%;box-sizing:border-box}
.dzw-pc-panneau textarea{min-height:70px;border:1px solid var(--dz-border,#e5e7eb);border-radius:8px;padding:6px 8px;font:inherit;font-size:.85rem;background:var(--dz-surface,#fff);color:inherit}
.dzw-pc-panneau .aide{font-size:.72rem;opacity:.6;margin-top:3px}
.dzw-pc-panneau .actions{display:flex;gap:6px;margin-top:14px;flex-wrap:wrap}
.dzw-pc-alerte{display:flex;gap:8px;flex-wrap:wrap;padding:6px 10px;font-size:.78rem;border-top:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface-2,#f9fafb)}
.dzw-pc-alerte span{display:inline-flex;gap:6px;align-items:center}
.dzw-pc-alerte .ok{color:#15803d}.dzw-pc-alerte .ko{color:#b45309}
.dzw-pc-vide{position:absolute;inset:0;display:grid;place-items:center;text-align:center;pointer-events:none;opacity:.7;font-size:.9rem;padding:20px}
.dzw-pc-pal{display:flex;gap:6px;flex-wrap:wrap}
.dzw-pc-pal .dzw-b i{color:var(--c)}
@media (max-width:640px){.dzw-pc-pal .dzw-b span.dzw-lbl{display:inline;font-size:.78rem}.dzw-pc-pal .dzw-b{padding:5px 8px}.dzw-pc-panneau{left:8px;right:8px;top:auto;bottom:8px;width:auto;max-height:60%;border-radius:16px 16px 12px 12px}}
@media (prefers-reduced-motion:no-preference){.dzw-pc-calque.anim{transition:transform .25s ease}}`);

export const PALETTE = [
  { cle: "debut", type: "debut", label: "Début", icone: "fas fa-play", couleur: "#16a34a", entree: false },
  { cle: "etape", type: "etape", label: "Étape", icone: "fas fa-circle", couleur: "#2563eb", champs: [{ nom: "description", label: "Ce qu'il faut faire", type: "zone" }, { nom: "responsable", label: "Qui s'en charge" }] },
  { cle: "condition", type: "condition", label: "Condition", icone: "fas fa-code-branch", couleur: "#f59e0b", branches: ["oui", "non"], champs: [{ nom: "expression", label: "Condition", aide: "Ex. ctx.montant > 500 (ctx = les données du parcours)" }] },
  { cle: "validation", type: "attente", label: "Validation", icone: "fas fa-user-check", couleur: "#8b5cf6", champs: [{ nom: "qui", label: "Qui valide" }, { nom: "consigne", label: "Consigne", type: "zone" }] },
  { cle: "fin", type: "fin", label: "Fin", icone: "fas fa-flag-checkered", couleur: "#ef4444", sortie: false },
];
const W = 190;
const uid = (p) => p + Math.random().toString(36).slice(2, 8);

register("parcours", (el) => {
  const c = champ(el);
  const lecture = conf(el, "lecture", false);
  const pal = (() => { const p = conf(el, "palette", null); return Array.isArray(p) && p.length ? p : PALETTE; })();
  const defOf = (n) => pal.find((p) => p.cle === n.cle) || pal.find((p) => p.type === n.type) || { cle: n.cle, type: n.type, label: n.type, icone: "fas fa-circle", couleur: "#64748b" };
  let doc = { v: 1, noeuds: [], liens: [] };
  try { const v = c.get(); if (v) { const d = JSON.parse(v); if (d && Array.isArray(d.noeuds)) doc = { v: 1, noeuds: d.noeuds, liens: d.liens || [] }; } } catch (e) { /* vide */ }
  const trace = new Set(conf(el, "trace", []));
  const actif = conf(el, "actif", "");
  const cam = { x: 0, y: 0, z: 1 };
  let sel = null; /* { n: noeud } ou { l: lien } */
  const hist = [JSON.stringify(doc)]; let hi = 0; let saveT = null;

  el.classList.add("dzw", "dzw-pc");
  el.style.setProperty("--pc-h", conf(el, "hauteur", 520) + "px");
  el.innerHTML = "";
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("class", "dzw-pc-svg");
  const calque = h("div", { class: "dzw-pc-calque" }, svg);
  const vide = h("div", { class: "dzw-pc-vide" }, lecture ? "Parcours vide." : "Ajoute une première étape avec les boutons du haut, puis relie-les en tirant le rond de droite vers l'étape suivante.");
  const zone = h("div", { class: "dzw-pc-zone", role: "application", "aria-label": "Parcours : étapes et liens" }, calque, vide);
  const alerte = h("div", { class: "dzw-pc-alerte", "aria-live": "polite" });
  const panneau = h("div", { class: "dzw-pc-panneau", hidden: true });
  zone.append(panneau);

  /* ---- enregistrement, historique ---- */
  const commit = () => { hist.splice(hi + 1); hist.push(JSON.stringify(doc)); hi = hist.length - 1; if (hist.length > 100) { hist.shift(); hi--; } clearTimeout(saveT); saveT = setTimeout(() => c.set(JSON.stringify(doc)), 250); verifier(); };
  const undo = (d) => { const i = hi + d; if (i < 0 || i >= hist.length) return; hi = i; doc = JSON.parse(hist[i]); sel = null; c.set(JSON.stringify(doc)); rendre(); };

  /* ---- géométrie ---- */
  const els = new Map();
  const hauteurDe = (n) => (els.get(n.id) ? els.get(n.id).offsetHeight : 56);
  const branchesDe = (n) => (defOf(n).branches || [null]);
  const portSortie = (n, si) => { const b = branchesDe(n); const i = Math.max(0, b.indexOf(si ?? null)); const H = hauteurDe(n); return { x: n.x + W, y: n.y + (b.length > 1 ? (H * (i + 1)) / (b.length + 1) : H / 2) }; };
  const portEntree = (n) => ({ x: n.x, y: n.y + hauteurDe(n) / 2 });
  const courbe = (a, b) => { const dx = Math.max(40, Math.abs(b.x - a.x) / 2); return `M${a.x},${a.y} C${a.x + dx},${a.y} ${b.x - dx},${b.y} ${b.x},${b.y}`; };
  const appliquerCam = () => { calque.style.transform = `translate(${-cam.x * cam.z}px,${-cam.y * cam.z}px) scale(${cam.z})`; };
  const versMonde = (e) => { const r = zone.getBoundingClientRect(); return { x: (e.clientX - r.left) / cam.z + cam.x, y: (e.clientY - r.top) / cam.z + cam.y }; };
  const cadrer = (anim) => {
    if (!doc.noeuds.length) { cam.x = -40; cam.y = -40; cam.z = 1; appliquerCam(); return; }
    const x1 = Math.min(...doc.noeuds.map((n) => n.x)) - 40, y1 = Math.min(...doc.noeuds.map((n) => n.y)) - 40;
    const x2 = Math.max(...doc.noeuds.map((n) => n.x + W)) + 40, y2 = Math.max(...doc.noeuds.map((n) => n.y + hauteurDe(n))) + 40;
    /* lisible d'abord : jamais sous 55 % ; si tout ne tient pas, on part du début (à gauche) et on fait glisser */
    const r = zone.getBoundingClientRect(); const z = Math.max(0.55, Math.min(1.2, Math.min(r.width / (x2 - x1), r.height / (y2 - y1))));
    cam.z = z;
    cam.x = r.width / z >= x2 - x1 ? x1 - (r.width / z - (x2 - x1)) / 2 : (() => { const d = doc.noeuds.find((n) => n.type === "debut") || doc.noeuds[0]; return d.x - 40; })();
    cam.y = r.height / z >= y2 - y1 ? y1 - (r.height / z - (y2 - y1)) / 2 : y1;
    calque.classList.toggle("anim", !!anim); appliquerCam(); setTimeout(() => calque.classList.remove("anim"), 300);
  };

  /* ---- dessin ---- */
  const liensSvg = () => {
    svg.innerHTML = "";
    for (const l of doc.liens) {
      const a = doc.noeuds.find((n) => n.id === l.de), b = doc.noeuds.find((n) => n.id === l.vers);
      if (!a || !b) continue;
      const p = portSortie(a, l.si), q = portEntree(b), d = courbe(p, q);
      const g = document.createElementNS(svg.namespaceURI, "g");
      if (sel && sel.l === l) g.classList.add("sel");
      if (trace.has(a.id) && (trace.has(b.id) || b.id === actif)) g.classList.add("passe");
      const path = document.createElementNS(svg.namespaceURI, "path"); path.setAttribute("d", d); path.setAttribute("class", "l"); path.setAttribute("marker-end", "url(#dzw-pc-fl)");
      const hit = document.createElementNS(svg.namespaceURI, "path"); hit.setAttribute("d", d); hit.setAttribute("class", "hit");
      if (!lecture) hit.addEventListener("pointerdown", (e) => { e.stopPropagation(); choisir({ l }); });
      g.append(path, hit);
      if (l.si) { const t = document.createElementNS(svg.namespaceURI, "text"); t.setAttribute("x", (p.x + q.x) / 2); t.setAttribute("y", (p.y + q.y) / 2 - 4); t.setAttribute("text-anchor", "middle"); t.textContent = l.si; g.append(t); }
      svg.append(g);
    }
    const defs = document.createElementNS(svg.namespaceURI, "defs");
    defs.innerHTML = '<marker id="dzw-pc-fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor" opacity=".55"/></marker>';
    svg.prepend(defs);
  };
  const noeudEl = (n) => {
    const d = defOf(n);
    const e = h("div", { class: "dzw-pc-n", tabindex: 0, role: "button", "aria-label": `${d.label} : ${n.titre || d.label}`, style: { left: n.x + "px", top: n.y + "px", "--c": d.couleur || "#2563eb" } },
      h("div", { class: "dzw-pc-t" }, h("span", { class: "dzw-pc-ic" }, h("i", { class: d.icone || "fas fa-circle" })), h("div", {}, h("small", {}, d.label), h("b", {}, n.titre || d.label))));
    if (d.entree !== false) e.append(h("span", { class: "dzw-pc-p in", "aria-hidden": "true" }));
    if (d.sortie !== false) {
      const bs = branchesDe(n);
      bs.forEach((si, i) => {
        const relie = doc.liens.some((l) => l.de === n.id && (l.si ?? null) === (si ?? null));
        const p = h("span", { class: "dzw-pc-p out", tabindex: lecture ? -1 : 0, title: lecture ? "" : "Tirer vers l'étape suivante", style: { top: bs.length > 1 ? `${((i + 1) * 100) / (bs.length + 1)}%` : "50%" } }, si && !relie ? h("em", {}, si) : null);
        if (!lecture) p.addEventListener("pointerdown", (ev) => { ev.stopPropagation(); tirer(ev, n, si); });
        e.append(p);
      });
    }
    if (n.id === actif) e.classList.add("actif"); else if (trace.has(n.id)) e.classList.add("passe");
    if (sel && sel.n === n) e.classList.add("sel");
    e.addEventListener("pointerdown", (ev) => { ev.stopPropagation(); choisir({ n }); if (lecture) return; deplacer(ev, n, e); });
    e.addEventListener("keydown", (ev) => {
      if (lecture) return;
      const pas = ev.shiftKey ? 40 : 10, m = { ArrowLeft: [-pas, 0], ArrowRight: [pas, 0], ArrowUp: [0, -pas], ArrowDown: [0, pas] }[ev.key];
      if (m) { ev.preventDefault(); n.x += m[0]; n.y += m[1]; e.style.left = n.x + "px"; e.style.top = n.y + "px"; liensSvg(); clearTimeout(e._t); e._t = setTimeout(commit, 400); }
      else if (ev.key === "Enter") { ev.preventDefault(); choisir({ n }); const f = panneau.querySelector("input,textarea"); if (f) f.focus(); }
    });
    return e;
  };
  function rendre() {
    calque.querySelectorAll(".dzw-pc-n").forEach((x) => x.remove()); els.clear();
    for (const n of doc.noeuds) { const e = noeudEl(n); els.set(n.id, e); calque.append(e); }
    liensSvg(); vide.hidden = doc.noeuds.length > 0; panneauRendre(); verifier();
  }

  /* ---- interactions ---- */
  const choisir = (s) => { sel = s; els.forEach((e, id) => e.classList.toggle("sel", !!(s && s.n && s.n.id === id))); liensSvg(); panneauRendre(); };
  const deplacer = (ev, n, e) => {
    const p0 = versMonde(ev), x0 = n.x, y0 = n.y; let bouge = false;
    e.setPointerCapture(ev.pointerId);
    const mv = (m) => { const p = versMonde(m); const nx = Math.round((x0 + p.x - p0.x) / 10) * 10, ny = Math.round((y0 + p.y - p0.y) / 10) * 10; if (nx !== n.x || ny !== n.y) { bouge = true; n.x = nx; n.y = ny; e.style.left = nx + "px"; e.style.top = ny + "px"; liensSvg(); } };
    const fin = () => { e.removeEventListener("pointermove", mv); e.removeEventListener("pointerup", fin); e.removeEventListener("pointercancel", fin); if (bouge) commit(); };
    e.addEventListener("pointermove", mv); e.addEventListener("pointerup", fin); e.addEventListener("pointercancel", fin);
  };
  const tirer = (ev, n, si) => {
    /* le panneau ne doit pas cacher l'étape visée pendant qu'on tire la flèche */
    panneau.hidden = true;
    const tmp = document.createElementNS(svg.namespaceURI, "path"); tmp.setAttribute("class", "l"); tmp.setAttribute("stroke-dasharray", "6 5"); svg.append(tmp);
    const a = portSortie(n, si);
    const mv = (m) => tmp.setAttribute("d", courbe(a, versMonde(m)));
    const fin = (u) => {
      window.removeEventListener("pointermove", mv); window.removeEventListener("pointerup", fin); tmp.remove();
      const cible = document.elementFromPoint(u.clientX, u.clientY); const ne = cible && cible.closest(".dzw-pc-n");
      const b = ne && doc.noeuds.find((x) => els.get(x.id) === ne);
      if (!b || b.id === n.id) { liensSvg(); panneauRendre(); return; }
      if (defOf(b).entree === false) { toast("Le début ne peut pas recevoir de flèche", "warning"); liensSvg(); return; }
      if (doc.liens.some((l) => l.de === n.id && l.vers === b.id && (l.si ?? null) === (si ?? null))) { liensSvg(); return; }
      doc.liens = doc.liens.filter((l) => !(si && l.de === n.id && l.si === si)); /* une branche = une flèche */
      const l = { id: uid("l"), de: n.id, vers: b.id, ...(si ? { si } : {}) }; doc.liens.push(l); commit(); rendre(); choisir({ l });
    };
    window.addEventListener("pointermove", mv); window.addEventListener("pointerup", fin);
  };
  const ajouter = (d) => {
    const r = zone.getBoundingClientRect();
    const decal = doc.noeuds.length % 6 * 24;
    const n = { id: uid("n"), cle: d.cle, type: d.type, ...(d.bloc ? { bloc: d.bloc } : {}), titre: d.label, x: Math.round((cam.x + r.width / cam.z / 2 - W / 2 + decal) / 10) * 10, y: Math.round((cam.y + r.height / cam.z / 3 + decal) / 10) * 10, reglages: { ...(d.reglages || {}) } };
    /* relie automatiquement à l'étape choisie, pour aller vite */
    const prec = sel && sel.n && defOf(sel.n).sortie !== false && !(defOf(sel.n).branches || []).length ? sel.n : null;
    doc.noeuds.push(n);
    if (prec && d.entree !== false) { n.x = prec.x + W + 70; n.y = prec.y; doc.liens.push({ id: uid("l"), de: prec.id, vers: n.id }); }
    commit(); rendre(); choisir({ n }); els.get(n.id).focus({ preventScroll: true });
  };
  const supprimer = () => {
    if (!sel) return;
    if (sel.n) { const id = sel.n.id; doc.noeuds = doc.noeuds.filter((x) => x.id !== id); doc.liens = doc.liens.filter((l) => l.de !== id && l.vers !== id); }
    else if (sel.l) doc.liens = doc.liens.filter((l) => l !== sel.l);
    sel = null; commit(); rendre(); zone.focus();
  };

  /* ---- panneau de réglages ---- */
  function panneauRendre() {
    panneau.innerHTML = "";
    if (!sel || lecture) { panneau.hidden = true; return; }
    panneau.hidden = false;
    if (sel.l) {
      const l = sel.l, a = doc.noeuds.find((x) => x.id === l.de), b = doc.noeuds.find((x) => x.id === l.vers);
      panneau.append(h("h4", {}, h("i", { class: "fas fa-long-arrow-alt-right" }), "Flèche"), h("p", { class: "aide" }, `${a ? a.titre : "?"} → ${b ? b.titre : "?"}`));
      const bs = a ? branchesDe(a).filter(Boolean) : [];
      if (bs.length) panneau.append(h("label", {}, "Quand"), h("select", { onchange: (e) => { l.si = e.target.value; commit(); liensSvg(); } }, ...bs.map((x) => h("option", { value: x, ...(x === l.si ? { selected: true } : {}) }, x))));
      panneau.append(h("div", { class: "actions" }, btn("fas fa-trash", "Supprimer la flèche", supprimer), btn("fas fa-times", "Fermer", () => choisir(null))));
      return;
    }
    const n = sel.n, d = defOf(n);
    panneau.append(h("h4", {}, h("span", { class: "dzw-pc-ic", style: { "--c": d.couleur } }, h("i", { class: d.icone })), d.label));
    const titre = h("input", { type: "text", value: n.titre || "", "aria-label": "Nom de l'étape", oninput: (e) => { n.titre = e.target.value; const b = els.get(n.id).querySelector("b"); if (b) b.textContent = n.titre || d.label; clearTimeout(titre._t); titre._t = setTimeout(commit, 400); } });
    panneau.append(h("label", {}, "Nom"), titre);
    for (const f of d.champs || []) {
      const v = (n.reglages || {})[f.nom] ?? "";
      const maj = (val) => { n.reglages = { ...(n.reglages || {}), [f.nom]: val }; clearTimeout(panneau._t); panneau._t = setTimeout(commit, 400); };
      let input;
      if (f.type === "zone") { input = h("textarea", { oninput: (e) => maj(e.target.value) }); input.value = v; }
      else if (f.type === "liste") input = h("select", { onchange: (e) => maj(e.target.value) }, ...(f.options || []).map((o) => h("option", { value: o, ...(o === v ? { selected: true } : {}) }, o)));
      else if (f.type === "nombre") input = h("input", { type: "number", value: v, oninput: (e) => maj(e.target.value === "" ? "" : +e.target.value) });
      else if (f.type === "case") input = h("input", { type: "checkbox", style: { width: "auto" }, ...(v ? { checked: true } : {}), onchange: (e) => maj(e.target.checked) });
      else input = h("input", { type: "text", value: v, oninput: (e) => maj(e.target.value) });
      panneau.append(h("label", {}, f.label || f.nom), input, f.aide ? h("div", { class: "aide" }, f.aide) : null);
    }
    panneau.append(h("div", { class: "actions" }, btn("fas fa-trash", "Supprimer l'étape", supprimer), btn("fas fa-times", "Fermer", () => choisir(null))));
  }

  /* ---- contrôle du schéma (en clair, pour tous) ---- */
  function verifier() {
    alerte.innerHTML = "";
    if (!doc.noeuds.length) { alerte.hidden = true; return; }
    alerte.hidden = false;
    const msgs = [];
    const debuts = doc.noeuds.filter((n) => n.type === "debut");
    if (!debuts.length) msgs.push("Il manque une étape « Début »");
    if (debuts.length > 1) msgs.push("Plusieurs « Début » : un seul sera suivi");
    const vus = new Set(); const pile = debuts.map((n) => n.id);
    while (pile.length) { const id = pile.pop(); if (vus.has(id)) continue; vus.add(id); doc.liens.filter((l) => l.de === id).forEach((l) => pile.push(l.vers)); }
    const isoles = doc.noeuds.filter((n) => !vus.has(n.id));
    if (debuts.length && isoles.length) msgs.push(`${isoles.length} étape(s) jamais atteinte(s)`);
    const conds = doc.noeuds.filter((n) => (defOf(n).branches || []).length > 1 && branchesDe(n).some((b) => !doc.liens.some((l) => l.de === n.id && l.si === b)));
    if (conds.length) msgs.push(`${conds.length} condition(s) sans flèche pour chaque réponse`);
    alerte.append(msgs.length ? h("span", { class: "ko" }, h("i", { class: "fas fa-exclamation-triangle" }), msgs.join(" · ")) : h("span", { class: "ok" }, h("i", { class: "fas fa-check-circle" }), `Parcours complet : ${doc.noeuds.length} étapes, ${doc.liens.length} flèches`));
  }

  /* ---- déplacement de la vue, zoom ---- */
  const zoomer = (f, cx, cy) => { const r = zone.getBoundingClientRect(); const px = cx ?? r.width / 2, py = cy ?? r.height / 2; const wx = px / cam.z + cam.x, wy = py / cam.z + cam.y; cam.z = Math.max(0.25, Math.min(2.5, cam.z * f)); cam.x = wx - px / cam.z; cam.y = wy - py / cam.z; appliquerCam(); };
  const pointeurs = new Map(); let pinch = null, pan = null;
  zone.addEventListener("pointerdown", (e) => {
    if (panneau.contains(e.target)) return;
    pointeurs.set(e.pointerId, e);
    if (pointeurs.size === 2) { const [a, b] = [...pointeurs.values()]; pinch = { d: Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY), z: cam.z }; pan = null; return; }
    choisir(null); zone.setPointerCapture(e.pointerId); zone.classList.add("pan"); pan = { sx: e.clientX, sy: e.clientY, cx: cam.x, cy: cam.y };
  });
  zone.addEventListener("pointermove", (e) => {
    if (pointeurs.has(e.pointerId)) pointeurs.set(e.pointerId, e);
    if (pinch && pointeurs.size === 2) { const [a, b] = [...pointeurs.values()]; const f = (Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY) / pinch.d) * pinch.z / cam.z; zoomer(f); return; }
    if (pan) { cam.x = pan.cx - (e.clientX - pan.sx) / cam.z; cam.y = pan.cy - (e.clientY - pan.sy) / cam.z; appliquerCam(); }
  });
  const lacher = (e) => { pointeurs.delete(e.pointerId); if (pointeurs.size < 2) pinch = null; pan = null; zone.classList.remove("pan"); };
  zone.addEventListener("pointerup", lacher); zone.addEventListener("pointercancel", lacher);
  zone.addEventListener("wheel", (e) => { if (!e.ctrlKey && !e.metaKey && !conf(el, "molette", false)) return; e.preventDefault(); const r = zone.getBoundingClientRect(); zoomer(e.deltaY < 0 ? 1.1 : 0.9, e.clientX - r.left, e.clientY - r.top); }, { passive: false });
  zone.tabIndex = 0;
  el.addEventListener("keydown", (e) => {
    if (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) { if (e.key === "Escape") choisir(null); return; }
    if (lecture) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); undo(e.shiftKey ? 1 : -1); }
    else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") { e.preventDefault(); undo(1); }
    else if ((e.key === "Delete" || e.key === "Backspace") && sel) { e.preventDefault(); supprimer(); }
    else if (e.key === "Escape") choisir(null);
  });

  /* ---- barre d'outils ---- */
  const barre = h("div", { class: "dzw-bar" });
  if (!lecture) barre.append(h("div", { class: "dzw-pc-pal", role: "toolbar", "aria-label": "Ajouter une étape" }, ...pal.map((d) => btn(d.icone || "fas fa-plus", d.label, () => ajouter(d), { style: { "--c": d.couleur } }))));
  barre.append(h("span", { class: "dzw-sp" }));
  if (!lecture) barre.append(btn("fas fa-undo", "Annuler", () => undo(-1)), btn("fas fa-redo", "Refaire", () => undo(1)));
  barre.append(btn("fas fa-search-plus", "Zoom +", () => zoomer(1.2)), btn("fas fa-search-minus", "Zoom −", () => zoomer(1 / 1.2)), btn("fas fa-expand", "Tout voir", () => cadrer(true)), btn("fas fa-download", "Exporter", () => download(JSON.stringify(doc, null, 2), "parcours.json", "application/json")));
  el.append(barre, zone, alerte);
  rendre();
  requestAnimationFrame(() => { liensSvg(); cadrer(false); });
  /* API pour les pages : lire le schéma, le remplacer, recadrer */
  el.dzParcours = { lire: () => JSON.parse(JSON.stringify(doc)), ecrire: (d) => { doc = { v: 1, noeuds: d.noeuds || [], liens: d.liens || [] }; commit(); rendre(); cadrer(true); }, cadrer: () => cadrer(true) };
});
