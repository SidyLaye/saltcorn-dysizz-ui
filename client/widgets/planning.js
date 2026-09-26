/* Planning : semaine en glisser-déposer (rendez-vous, équipes, salles, cours…).
   Tracer sur une case vide = créer ; glisser = déplacer ; poignée du bas = allonger.
   Clavier : Entrée = modifier, Suppr = retirer, flèches = déplacer (Maj = durée).
   Sur téléphone : un jour à la fois.

   Réglages : champ, jours (5 ou 7), debut / fin (heures, défaut 8 → 19),
   pas (minutes, défaut 30), hauteur, lecture, date (semaine affichée au départ).
   Enregistré : { v: 1, evenements: [{ id, titre, date: "AAAA-MM-JJ", debut: "HH:MM", fin: "HH:MM", couleur }] } */
import { register, css, h, conf, champ, btn } from "./_commun.js";

css("planning", `.dzw-pl{--pl-h:560px}
.dzw-pl-nav{display:flex;align-items:center;gap:6px}
.dzw-pl-nav b{font-size:.92rem;min-width:170px;text-align:center}
.dzw-pl-grille{position:relative;display:grid;grid-template-columns:52px repeat(var(--n),minmax(0,1fr));height:var(--pl-h);overflow:auto}
.dzw-pl-tete{position:sticky;top:0;z-index:3;display:contents}
.dzw-pl-tete>div{position:sticky;top:0;z-index:3;background:var(--dz-surface,#fff);border-bottom:1px solid var(--dz-border,#e5e7eb);padding:6px 4px;text-align:center;font-size:.78rem}
.dzw-pl-tete>div b{display:block;font-size:1.05rem}
.dzw-pl-tete>div.auj b{color:#fff;background:var(--dz-primary,#2563eb);border-radius:99px;width:30px;height:30px;line-height:30px;margin:2px auto 0}
.dzw-pl-heures{position:relative}
.dzw-pl-heures span{position:absolute;right:6px;transform:translateY(-50%);font-size:.7rem;opacity:.55}
.dzw-pl-col{position:relative;border-left:1px solid var(--dz-border,#eef0f3);background-image:linear-gradient(var(--dz-border,#eef0f3) 1px,transparent 1px);background-size:100% var(--hh);touch-action:none;cursor:cell}
.dzw-pl-col.we{background-color:color-mix(in srgb,var(--dz-text,#0f172a) 3%,transparent)}
.dzw-pl-ev{position:absolute;left:3px;right:3px;border-radius:8px;background:var(--c,#2563eb);color:#fff;padding:4px 7px;font-size:.76rem;line-height:1.25;overflow:hidden;cursor:grab;box-shadow:0 1px 2px rgba(0,0,0,.15);touch-action:none;user-select:none}
.dzw-pl-ev:focus-visible{outline:3px solid var(--dz-text,#111827);outline-offset:1px}
.dzw-pl-ev.sel{box-shadow:0 0 0 2px var(--dz-surface,#fff),0 0 0 4px var(--c,#2563eb)}
.dzw-pl-ev b{display:block;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dzw-pl-ev small{opacity:.85}
.dzw-pl-ev .bord{position:absolute;left:0;right:0;bottom:0;height:9px;cursor:ns-resize}
.dzw-pl-ev.fantome{opacity:.55;pointer-events:none}
.dzw-pl-now{position:absolute;left:0;right:0;height:2px;background:#ef4444;z-index:2;pointer-events:none}
.dzw-pl-now::before{content:"";position:absolute;left:-4px;top:-4px;width:10px;height:10px;border-radius:50%;background:#ef4444}
.dzw-pl-pop{position:absolute;z-index:6;width:250px;background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e5e7eb);border-radius:12px;box-shadow:0 18px 40px -18px rgba(15,23,42,.4);padding:12px}
.dzw-pl-pop label{display:block;font-size:.74rem;font-weight:600;opacity:.75;margin:8px 0 3px}
.dzw-pl-pop input[type=text]{width:100%;box-sizing:border-box}
.dzw-pl-pop .coul{display:flex;gap:6px}
.dzw-pl-pop .coul button{width:24px;height:24px;border-radius:50%;border:2px solid var(--dz-surface,#fff);box-shadow:0 0 0 1px var(--dz-border,#cbd5e1);cursor:pointer;padding:0}
.dzw-pl-pop .coul button.on{box-shadow:0 0 0 2px var(--dz-text,#111827)}
.dzw-pl-pop .actions{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
.dzw-pl-jours{display:none;gap:4px;overflow-x:auto;padding:6px 8px;border-bottom:1px solid var(--dz-border,#e5e7eb)}
.dzw-pl-jours button{flex:none;border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);border-radius:10px;padding:5px 9px;font-size:.78rem;cursor:pointer;color:inherit}
.dzw-pl-jours button.on{background:var(--dz-primary,#2563eb);border-color:var(--dz-primary,#2563eb);color:#fff}
@media (max-width:640px){.dzw-pl-jours{display:flex}.dzw-pl-nav b{min-width:0}.dzw-pl-pop{left:8px!important;right:8px;width:auto}}`);

const COULEURS = ["#2563eb", "#16a34a", "#f59e0b", "#8b5cf6", "#ec4899", "#0ea5e9", "#ef4444", "#475569"];
const JOURS = ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."];
const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const lundi = (d) => { const x = new Date(d); x.setHours(0, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; };
const min = (hm) => { const [a, b] = String(hm || "0:0").split(":").map(Number); return a * 60 + (b || 0); };
const hm = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
const uid = () => "e" + Math.random().toString(36).slice(2, 8);

register("planning", (el) => {
  const c = champ(el);
  const lecture = conf(el, "lecture", false);
  const nj = conf(el, "jours", 7) === 5 ? 5 : 7;
  const H0 = conf(el, "debut", 8) * 60, H1 = conf(el, "fin", 19) * 60, PAS = Math.max(5, conf(el, "pas", 30));
  let evs = [];
  try { const v = c.get(); if (v) { const d = JSON.parse(v); if (d && Array.isArray(d.evenements)) evs = d.evenements; } } catch (e) { /* vide */ }
  let semaine = lundi(conf(el, "date", "") ? new Date(conf(el, "date", "")) : new Date());
  let jourMobile = Math.max(0, Math.min(nj - 1, (new Date().getDay() + 6) % 7));
  let sel = null, pop = null, t = null;
  el.classList.add("dzw", "dzw-pl");
  el.style.setProperty("--pl-h", conf(el, "hauteur", 560) + "px");
  el.innerHTML = "";
  const sauver = () => { clearTimeout(t); t = setTimeout(() => c.set(JSON.stringify({ v: 1, evenements: evs })), 250); };
  const mobile = () => el.clientWidth < 640;
  const titreNav = h("b", { "aria-live": "polite" });
  const jours = h("div", { class: "dzw-pl-jours", role: "tablist", "aria-label": "Jour affiché" });
  const grille = h("div", { class: "dzw-pl-grille" });
  const aide = h("div", { class: "dzw-note" }, lecture ? "" : "Trace sur une case vide pour créer · glisse pour déplacer · tire le bas pour allonger · Entrée pour modifier");
  const nav = (d) => { semaine = new Date(semaine); semaine.setDate(semaine.getDate() + d * 7); fermer(); rendre(); };
  el.append(h("div", { class: "dzw-bar" }, h("div", { class: "dzw-pl-nav" }, btn("fas fa-chevron-left", "Semaine précédente", () => nav(-1)), titreNav, btn("fas fa-chevron-right", "Semaine suivante", () => nav(1))), btn("far fa-calendar-check", "Aujourd'hui", () => { semaine = lundi(new Date()); jourMobile = (new Date().getDay() + 6) % 7; if (jourMobile >= nj) jourMobile = 0; fermer(); rendre(); })), jours, grille, aide);

  const joursAffiches = () => { const tous = Array.from({ length: nj }, (_, i) => { const d = new Date(semaine); d.setDate(d.getDate() + i); return d; }); return mobile() ? [tous[jourMobile]] : tous; };

  function rendre() {
    const js = joursAffiches();
    const f = (d) => d.toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
    const fin = new Date(semaine); fin.setDate(fin.getDate() + nj - 1);
    titreNav.textContent = `${f(semaine)} – ${f(fin)} ${fin.getFullYear()}`;
    jours.innerHTML = "";
    Array.from({ length: nj }, (_, i) => { const d = new Date(semaine); d.setDate(d.getDate() + i); jours.append(h("button", { type: "button", role: "tab", class: i === jourMobile ? "on" : "", "aria-selected": i === jourMobile ? "true" : "false", onclick: () => { jourMobile = i; fermer(); rendre(); } }, `${JOURS[d.getDay()]} ${d.getDate()}`)); });
    grille.innerHTML = "";
    grille.style.setProperty("--n", js.length);
    const pm = Math.max(0.5, (parseFloat(getComputedStyle(el).getPropertyValue("--pl-h")) - 44) / (H1 - H0));
    grille.style.setProperty("--hh", 60 * pm + "px");
    const tete = h("div", { class: "dzw-pl-tete" }, h("div", {}));
    const auj = iso(new Date());
    js.forEach((d) => tete.append(h("div", { class: iso(d) === auj ? "auj" : "" }, JOURS[d.getDay()], h("b", {}, d.getDate()))));
    grille.append(tete);
    const heures = h("div", { class: "dzw-pl-heures", style: { height: (H1 - H0) * pm + "px" } });
    for (let m = Math.floor(H0 / 60) * 60 + 60; m < H1; m += 60) heures.append(h("span", { style: { top: (m - H0) * pm + "px" } }, `${m / 60} h`));
    grille.append(heures);
    js.forEach((d) => {
      const date = iso(d);
      const col = h("div", { class: "dzw-pl-col" + (d.getDay() === 0 || d.getDay() === 6 ? " we" : ""), style: { height: (H1 - H0) * pm + "px" }, "data-date": date, role: "group", "aria-label": d.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" }) });
      if (date === auj) { const n = new Date(); const mm = n.getHours() * 60 + n.getMinutes(); if (mm >= H0 && mm <= H1) col.append(h("div", { class: "dzw-pl-now", style: { top: (mm - H0) * pm + "px" } })); }
      evs.filter((e) => e.date === date).forEach((e) => col.append(evEl(e, pm)));
      if (!lecture) col.addEventListener("pointerdown", (x) => creer(x, col, pm));
      grille.append(col);
    });
  }
  const evEl = (e, pm) => {
    const a = Math.max(H0, min(e.debut)), b = Math.min(H1, Math.max(min(e.fin), a + PAS));
    const ev = h("div", { class: "dzw-pl-ev" + (sel === e.id ? " sel" : ""), tabindex: 0, role: "button", "aria-label": `${e.titre || "Sans titre"}, ${e.debut} à ${e.fin}`, style: { top: (a - H0) * pm + "px", height: Math.max(18, (b - a) * pm - 2) + "px", "--c": e.couleur || COULEURS[0] } },
      h("b", {}, e.titre || "Sans titre"), h("small", {}, `${e.debut} – ${e.fin}`));
    if (lecture) return ev;
    const bord = h("span", { class: "bord", "aria-hidden": "true" }); ev.append(bord);
    ev.addEventListener("pointerdown", (x) => { x.stopPropagation(); glisser(x, e, ev, pm, x.target === bord); });
    ev.addEventListener("keydown", (x) => {
      if (x.key === "Enter") { x.preventDefault(); ouvrir(e, ev); return; }
      if (x.key === "Delete" || x.key === "Backspace") { x.preventDefault(); evs = evs.filter((y) => y !== e); sauver(); rendre(); return; }
      const d = { ArrowUp: -PAS, ArrowDown: PAS }[x.key], j = { ArrowLeft: -1, ArrowRight: 1 }[x.key];
      if (d) { x.preventDefault(); if (x.shiftKey) e.fin = hm(Math.max(min(e.debut) + PAS, Math.min(H1, min(e.fin) + d))); else { const du = min(e.fin) - min(e.debut); const nd = Math.max(H0, Math.min(H1 - du, min(e.debut) + d)); e.debut = hm(nd); e.fin = hm(nd + du); } sauver(); sel = e.id; rendre(); focusEv(e); }
      else if (j) { x.preventDefault(); const dt = new Date(e.date); dt.setDate(dt.getDate() + j); e.date = iso(dt); if (mobile()) jourMobile = Math.max(0, Math.min(nj - 1, jourMobile + j)); sauver(); sel = e.id; rendre(); focusEv(e); }
    });
    return ev;
  };
  const focusEv = (e) => { const i = evs.indexOf(e); const all = [...grille.querySelectorAll(".dzw-pl-ev")]; const ev = all.find((x) => x.getAttribute("aria-label").startsWith(e.titre || "Sans titre")); if (ev) ev.focus(); return i; };
  const minuteDe = (col, y, pm) => { const r = col.getBoundingClientRect(); return Math.max(H0, Math.min(H1, H0 + Math.round((y - r.top) / pm / PAS) * PAS)); };

  const creer = (x, col, pm) => {
    if (x.button !== 0 && x.pointerType === "mouse") return;
    fermer();
    const m0 = minuteDe(col, x.clientY, pm);
    const e = { id: uid(), titre: "", date: col.dataset.date, debut: hm(m0), fin: hm(Math.min(H1, m0 + PAS * 2)), couleur: COULEURS[evs.length % COULEURS.length] };
    const g = evEl(e, pm); g.classList.add("fantome"); col.append(g);
    col.setPointerCapture(x.pointerId);
    let bouge = false;
    const mv = (m) => { const mm = minuteDe(col, m.clientY, pm); if (mm !== m0) bouge = true; const a = Math.min(m0, mm), b = Math.max(m0 + PAS, mm); e.debut = hm(a); e.fin = hm(Math.max(a + PAS, b)); g.style.top = (a - H0) * pm + "px"; g.style.height = (min(e.fin) - a) * pm - 2 + "px"; g.querySelector("small").textContent = `${e.debut} – ${e.fin}`; };
    const up = () => { col.removeEventListener("pointermove", mv); col.removeEventListener("pointerup", up); col.removeEventListener("pointercancel", up); g.remove(); if (!bouge && x.pointerType === "touch") return; /* au doigt : un simple toucher fait défiler, pas de création */ evs.push(e); sel = e.id; sauver(); rendre(); const ev = [...grille.querySelectorAll(".dzw-pl-ev")].find((z) => z.getAttribute("aria-label").startsWith("Sans titre, " + e.debut)); if (ev) ouvrir(e, ev); };
    col.addEventListener("pointermove", mv); col.addEventListener("pointerup", up); col.addEventListener("pointercancel", up);
  };
  const glisser = (x, e, ev, pm, allonger) => {
    fermer(); sel = e.id; grille.querySelectorAll(".dzw-pl-ev.sel").forEach((y) => y.classList.remove("sel")); ev.classList.add("sel");
    ev.setPointerCapture(x.pointerId);
    const y0 = x.clientY, a0 = min(e.debut), b0 = min(e.fin), date0 = e.date; let bouge = false;
    const mv = (m) => {
      const dm = Math.round((m.clientY - y0) / pm / PAS) * PAS;
      if (allonger) { e.fin = hm(Math.max(a0 + PAS, Math.min(H1, b0 + dm))); }
      else {
        const du = b0 - a0, nd = Math.max(H0, Math.min(H1 - du, a0 + dm)); e.debut = hm(nd); e.fin = hm(nd + du);
        const cible = document.elementsFromPoint(m.clientX, m.clientY).find((z) => z.classList && z.classList.contains("dzw-pl-col"));
        if (cible && cible.dataset.date !== e.date) { e.date = cible.dataset.date; cible.append(ev); }
      }
      if (dm || e.date !== date0) bouge = true;
      ev.style.top = (min(e.debut) - H0) * pm + "px"; ev.style.height = Math.max(18, (min(e.fin) - min(e.debut)) * pm - 2) + "px"; ev.querySelector("small").textContent = `${e.debut} – ${e.fin}`;
    };
    const up = () => { ev.removeEventListener("pointermove", mv); ev.removeEventListener("pointerup", up); ev.removeEventListener("pointercancel", up); if (bouge) { sauver(); rendre(); } else ouvrir(e, ev); };
    ev.addEventListener("pointermove", mv); ev.addEventListener("pointerup", up); ev.addEventListener("pointercancel", up);
  };

  /* ---- fenêtre de modification ---- */
  const fermer = () => { if (pop) { pop.remove(); pop = null; document.removeEventListener("pointerdown", dehors, true); } };
  const dehors = (x) => { if (pop && !pop.contains(x.target)) fermer(); };
  const ouvrir = (e, ev) => {
    fermer(); sel = e.id;
    const r = ev.getBoundingClientRect(), rr = el.getBoundingClientRect();
    const titre = h("input", { type: "text", value: e.titre || "", placeholder: "Titre", "aria-label": "Titre", oninput: (x) => { e.titre = x.target.value; sauver(); }, onkeydown: (x) => { if (x.key === "Enter") { x.preventDefault(); fermer(); rendre(); } } });
    const heure = (lab, cle) => h("input", { type: "time", step: PAS * 60, value: e[cle], "aria-label": lab, onchange: (x) => { e[cle] = x.target.value; if (min(e.fin) <= min(e.debut)) e.fin = hm(min(e.debut) + PAS); sauver(); } });
    pop = h("div", { class: "dzw-pl-pop", role: "dialog", "aria-label": "Modifier le créneau" },
      h("label", {}, "Titre"), titre,
      h("label", {}, "Horaires"), h("div", { style: { display: "flex", gap: "6px", alignItems: "center" } }, heure("Début", "debut"), "→", heure("Fin", "fin")),
      h("label", {}, "Couleur"), h("div", { class: "coul" }, ...COULEURS.map((col) => h("button", { type: "button", title: col, "aria-label": `Couleur ${col}`, class: (e.couleur || COULEURS[0]) === col ? "on" : "", style: { background: col }, onclick: (x) => { e.couleur = col; pop.querySelectorAll(".coul button").forEach((b) => b.classList.toggle("on", b === x.currentTarget)); sauver(); } }))),
      h("div", { class: "actions" }, btn("fas fa-check", "OK", () => { fermer(); rendre(); }), btn("fas fa-trash", "Supprimer", () => { evs = evs.filter((y) => y !== e); fermer(); sauver(); rendre(); })));
    pop.style.left = Math.max(8, Math.min(r.right - rr.left + 8, rr.width - 258)) + "px";
    pop.style.top = Math.max(8, Math.min(r.top - rr.top, rr.height - 280)) + "px";
    el.append(pop); titre.focus();
    pop.addEventListener("keydown", (x) => { if (x.key === "Escape") { fermer(); rendre(); } });
    setTimeout(() => document.addEventListener("pointerdown", dehors, true), 0);
  };

  rendre();
  new ResizeObserver(() => { if (!pop) rendre(); }).observe(el);
  el.dzPlanning = { lire: () => JSON.parse(JSON.stringify(evs)), ecrire: (l) => { evs = l || []; sauver(); rendre(); } };
});
