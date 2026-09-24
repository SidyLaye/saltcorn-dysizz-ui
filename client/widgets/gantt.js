/* Planning (Gantt) : barres par tâche sur une frise de jours, avancement,
   aujourd'hui marqué, depuis une liste JSON ou une table Saltcorn. */
import { register, css, h, conf, tableRows, esc } from "./_commun.js";

css("gantt", `.dzw-gantt .dzw-g-wrap{overflow:auto;max-height:var(--h,460px)}
.dzw-gantt .dzw-g{display:grid;grid-template-columns:minmax(140px,220px) 1fr;min-width:720px;font-size:.85rem}
.dzw-gantt .dzw-g-h{position:sticky;top:0;z-index:2;background:var(--dz-surface-2,#f8fafc);border-bottom:1px solid var(--dz-border,#e5e7eb)}
.dzw-gantt .dzw-g-days{display:grid;grid-template-columns:repeat(var(--n),minmax(26px,1fr))}
.dzw-gantt .dzw-g-days span{text-align:center;padding:4px 0;font-size:.72rem;opacity:.75;border-left:1px solid var(--dz-border,#eef0f3)}
.dzw-gantt .dzw-g-days span.we{background:rgba(148,163,184,.12)}
.dzw-gantt .dzw-g-days span.mo{font-weight:700;opacity:1}
.dzw-gantt .dzw-g-name{padding:8px 10px;border-bottom:1px solid var(--dz-border,#eef0f3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;position:sticky;left:0;background:var(--dz-surface,#fff);z-index:1}
.dzw-gantt .dzw-g-name small{display:block;opacity:.6}
.dzw-gantt .dzw-g-row{position:relative;border-bottom:1px solid var(--dz-border,#eef0f3);background-image:linear-gradient(90deg,var(--dz-border,#eef0f3) 1px,transparent 1px);background-size:calc(100% / var(--n)) 100%}
.dzw-gantt .dzw-g-bar{position:absolute;top:8px;bottom:8px;border-radius:7px;background:var(--c,#2563eb);color:#fff;font-size:.74rem;padding:0 8px;display:flex;align-items:center;overflow:hidden;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.dzw-gantt .dzw-g-bar i{position:absolute;left:0;top:0;bottom:0;background:rgba(255,255,255,.28)}
.dzw-gantt .dzw-g-bar b{position:relative;font-weight:600}
.dzw-gantt .dzw-g-bar.jalon{width:16px!important;padding:0;border-radius:3px;transform:rotate(45deg) scale(.8)}
.dzw-gantt .dzw-g-today{position:absolute;top:0;bottom:0;width:2px;background:#ef4444;z-index:1}`);

const day = (d) => { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; };
const COUL = ["#2563eb", "#16a34a", "#f59e0b", "#8b5cf6", "#ec4899", "#0ea5e9", "#ef4444"];

register("gantt", async (el) => {
  el.classList.add("dzw", "dzw-gantt");
  el.style.setProperty("--h", conf(el, "hauteur", 460) + "px");
  el.innerHTML = "";
  let taches = conf(el, "taches", []);
  const table = conf(el, "table", "");
  if (table) {
    try {
      const F = { nom: conf(el, "champ-nom", "titre"), debut: conf(el, "champ-debut", "debut"), fin: conf(el, "champ-fin", "fin"), avancement: conf(el, "champ-avancement", ""), groupe: conf(el, "champ-groupe", "") };
      taches = (await tableRows(table, conf(el, "filtre", {}))).map((r) => ({ nom: r[F.nom], debut: r[F.debut], fin: r[F.fin] || r[F.debut], avancement: F.avancement ? r[F.avancement] : null, groupe: F.groupe ? r[F.groupe] : "", lien: conf(el, "lien", "").replace(/\{id\}/g, r.id) }));
    } catch (e) { el.append(h("div", { class: "dz-wg-err" }, "Table illisible : " + e.message)); return; }
  }
  taches = taches.filter((t) => t.debut).map((t) => ({ ...t, d: day(t.debut), f: day(t.fin || t.debut) })).sort((a, b) => a.d - b.d);
  if (!taches.length) { el.append(h("div", { class: "dzw-note", style: { padding: "20px" } }, conf(el, "texte-vide", "Aucune tâche planifiée"))); return; }
  const d0 = new Date(Math.min(...taches.map((t) => t.d))); d0.setDate(d0.getDate() - 1);
  const d1 = new Date(Math.max(...taches.map((t) => t.f))); d1.setDate(d1.getDate() + 2);
  const n = Math.round((d1 - d0) / 864e5);
  const idx = (d) => Math.round((day(d) - d0) / 864e5);
  const groups = [...new Set(taches.map((t) => t.groupe || ""))];
  const grid = h("div", { class: "dzw-g", style: { "--n": n } });
  grid.style.setProperty("--n", n);
  const days = h("div", { class: "dzw-g-days" });
  for (let i = 0; i < n; i++) { const d = new Date(d0); d.setDate(d.getDate() + i); days.append(h("span", { class: [d.getDay() % 6 === 0 ? "we" : "", d.getDate() === 1 || i === 0 ? "mo" : ""].join(" "), title: d.toLocaleDateString("fr-FR") }, d.getDate() === 1 || i === 0 ? d.toLocaleDateString("fr-FR", { day: "numeric", month: "short" }) : d.getDate())); }
  grid.append(h("div", { class: "dzw-g-h dzw-g-name" }, h("b", {}, "Tâche")), h("div", { class: "dzw-g-h" }, days));
  const today = idx(new Date());
  for (const t of taches) {
    const deb = idx(t.d), dur = Math.max(1, idx(t.f) - deb + 1);
    const col = COUL[groups.indexOf(t.groupe || "") % COUL.length];
    const jalon = +t.f === +t.d && t.jalon !== false && !t.avancement;
    const bar = h(t.lien ? "a" : "div", { class: "dzw-g-bar" + (jalon ? " jalon" : ""), href: t.lien || null, style: { left: `calc(${deb} * 100% / ${n} + 2px)`, width: `calc(${dur} * 100% / ${n} - 4px)`, "--c": t.couleur || col }, title: `${t.nom} : ${t.d.toLocaleDateString("fr-FR")} → ${t.f.toLocaleDateString("fr-FR")}${t.avancement != null ? ` (${t.avancement} %)` : ""}` });
    bar.style.setProperty("--c", t.couleur || col);
    if (!jalon) { if (t.avancement != null) bar.append(h("i", { style: { width: `${Math.max(0, Math.min(100, +t.avancement))}%` } })); bar.append(h("b", {}, t.avancement != null ? `${t.avancement} %` : "")); }
    const row = h("div", { class: "dzw-g-row" }, bar);
    if (today >= 0 && today < n) row.append(h("div", { class: "dzw-g-today", style: { left: `calc(${today + 0.5} * 100% / ${n})` } }));
    grid.append(h("div", { class: "dzw-g-name", title: t.nom, html: `${esc(t.nom)}${t.groupe ? `<small>${esc(t.groupe)}</small>` : ""}` }), row);
  }
  el.append(h("div", { class: "dzw-bar" }, h("i", { class: "fas fa-stream" }), h("b", {}, conf(el, "titre", "Planning")), h("span", { class: "dzw-sp" }), h("span", { class: "dzw-note" }, `${taches.length} tâche(s)`)), h("div", { class: "dzw-g-wrap" }, grid));
});
