/* Tableau de bord : affiche une source de données (/dysizz/donnees/<nom>).

   <div data-dz-widget="tableau" data-source="leads-resume" data-vue="kpi" …></div>

   Vues (data-vue) :
     kpi      chiffre clé + écart avec la période précédente (source « comparer »)
     courbe   série dans le temps (source de type serie)
     barres   classement par catégorie (source agregat avec groupe)
     anneau   répartition par catégorie
     liste    lignes paginées, triables, cliquables (source de type liste)
     filtres  barre de filtres partagée par tous les blocs de la page

   Réglages communs : titre, mesure (nom de la mesure affichée), format
   (nombre | euro | pourcent | minutes | date | dateheure | oui_non), libelles (JSON clé → libellé),
   params (paramètres fixes, ex. "periode=30j"), rafraichir (secondes),
   hauteur (px), lien (liste : adresse avec {champ}, ex. "/page/lead?id={id}"),
   colonnes (liste : JSON [{champ,titre,format}]), champs (filtres : JSON).

   Les filtres vivent dans l'adresse de la page : un lien filtré se partage,
   Retour fonctionne, et changer un filtre ne recharge que les blocs. */
import { register, css, h, conf, csrf } from "./_commun.js";

css("tableau", `.dzw-tb-case{width:34px;text-align:center}.dzw-tb-case input{width:17px;height:17px;cursor:pointer;accent-color:var(--dz-primary,#2563eb)}
.dzw-tb-sel{position:sticky;top:8px;z-index:5;margin:0 0 10px;padding:10px 12px;border-radius:12px;background:color-mix(in srgb,var(--dz-primary,#2563eb) 9%,var(--dz-surface,#fff));border:1px solid color-mix(in srgb,var(--dz-primary,#2563eb) 30%,transparent)}
.dzw-tb-sel-tete{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.dzw-tb-sel button{font:inherit;font-size:.85rem;cursor:pointer;border-radius:9px;padding:6px 12px;border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);color:inherit}
.dzw-tb-sel button.ok{background:var(--dz-primary,#2563eb);color:var(--dz-on-primary,#fff);border-color:transparent;font-weight:600}
.dzw-tb-sel button.lien{border:0;background:none;text-decoration:underline;padding:6px 4px}
.dzw-tb-sel-panneau{margin-top:10px;padding-top:10px;border-top:1px solid color-mix(in srgb,var(--dz-primary,#2563eb) 25%,transparent);display:grid;gap:8px}
.dzw-tb-sel-ligne{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dzw-tb-sel-ligne select,.dzw-tb-sel-ligne input{font:inherit;font-size:.88rem;padding:7px 10px;border-radius:9px;border:1px solid var(--dz-border,#d1d5db);background:var(--dz-surface,#fff);color:inherit;min-width:180px;min-height:38px}
.dzw-tb-sel-ligne .fl{opacity:.6}.dzw-tb-sel-ligne .moins{border:0!important;background:none!important;font-size:1.1rem!important;opacity:.6}
.dzw-tb-sel-act{display:flex;gap:8px;flex-wrap:wrap}.dzw-tb-sel-msg{font-size:.85rem}
.dzw-tb-sel-groupe{margin-left:10px;font:inherit;font-size:.75rem;font-weight:500;border:0;background:none;text-decoration:underline;cursor:pointer;color:inherit;opacity:.75}
.dzw-tb{position:relative;background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e5e7eb);border-radius:var(--dz-radius,14px);padding:16px 18px;min-width:0}
.dzw-tb h3{font-size:.8rem;font-weight:600;letter-spacing:.02em;text-transform:uppercase;opacity:.68;margin:0 0 10px;display:flex;justify-content:space-between;gap:8px}
.dzw-tb h3 small{text-transform:none;letter-spacing:0;font-weight:500}
.dzw-tb-kpi b{display:block;font-size:clamp(1.7rem,3.2vw,2.4rem);line-height:1.1;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.dzw-tb-delta{display:inline-flex;align-items:center;gap:4px;margin-top:6px;font-size:.8rem;font-weight:600;padding:2px 8px;border-radius:99px;background:color-mix(in srgb,var(--dz-text,#0f172a) 6%,transparent)}
.dzw-tb-delta.up{color:#047857;background:#d1fae5}.dzw-tb-delta.down{color:#b91c1c;background:#fee2e2}
.dzw-tb-delta.inv.up{color:#b91c1c;background:#fee2e2}.dzw-tb-delta.inv.down{color:#047857;background:#d1fae5}
.dzw-tb-kpi.txt b{font-size:clamp(1.15rem,1.8vw,1.45rem)}
.dzw-tb-sous{font-size:.8rem;opacity:.65;margin-top:6px}
.dzw-tb svg{display:block;width:100%;overflow:visible}
.dzw-tb-axe{font-size:10px;fill:currentColor;opacity:.55}
.dzw-tb-bulle{position:absolute;pointer-events:none;background:var(--dz-text,#0f172a);color:var(--dz-surface,#fff);font-size:.75rem;padding:6px 9px;border-radius:8px;white-space:nowrap;transform:translate(-50%,-110%);z-index:5;box-shadow:0 8px 20px -8px rgba(0,0,0,.4)}
.dzw-tb-barres{display:grid;gap:7px}
.dzw-tb-barre{display:grid;grid-template-columns:minmax(80px,30%) 1fr auto;gap:10px;align-items:center;font-size:.85rem;cursor:default}
.dzw-tb-barre[data-cle]{cursor:pointer}
.dzw-tb-barre span:first-child{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dzw-tb-barre i{display:block;height:10px;border-radius:99px;background:var(--dz-primary,#2563eb);min-width:2px;transition:width .5s cubic-bezier(.2,.8,.2,1)}
.dzw-tb-barre b{font-variant-numeric:tabular-nums;font-weight:600}
.dzw-tb-barre:hover i{filter:brightness(1.1)}
.dzw-tb-anneau{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.dzw-tb-anneau svg{width:140px;height:140px;flex:none}
.dzw-tb-legende{display:grid;gap:4px;font-size:.82rem;flex:1;min-width:180px}
.dzw-tb-legende span{display:flex;gap:6px;align-items:center}
.dzw-tb-legende i{width:10px;height:10px;border-radius:3px;flex:none}
.dzw-tb-legende b{margin-left:auto;font-variant-numeric:tabular-nums}
.dzw-tb-table{width:100%;border-collapse:collapse;font-size:.86rem}
.dzw-tb-table th{text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;opacity:.65;font-weight:600;padding:8px 10px;border-bottom:1px solid var(--dz-border,#e5e7eb);white-space:nowrap}
.dzw-tb-table th[data-tri]{cursor:pointer;user-select:none}
.dzw-tb-table th[data-tri]:hover{opacity:1}
.dzw-tb-table th.on{opacity:1;color:var(--dz-primary,#2563eb)}
.dzw-tb-table td.nw{white-space:nowrap}
.dzw-tb-table td{padding:9px 10px;border-bottom:1px solid color-mix(in srgb,var(--dz-border,#e5e7eb) 70%,transparent);vertical-align:top}
.dzw-tb-table tr[data-href]{cursor:pointer}
.dzw-tb-table tr[data-href]:hover td{background:color-mix(in srgb,var(--dz-primary,#2563eb) 5%,transparent)}
.dzw-tb-table td.num{text-align:right;font-variant-numeric:tabular-nums}
.dzw-tb-pied{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:10px;font-size:.8rem;flex-wrap:wrap}
.dzw-tb-pied button{border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);color:inherit;border-radius:8px;padding:5px 11px;cursor:pointer;min-height:34px}
.dzw-tb-pied button:disabled{opacity:.4;cursor:default}
.dzw-tb-action{display:inline-block;padding:4px 10px;border-radius:8px;border:1px solid var(--dz-border,#e5e7eb);font-size:.8rem;text-decoration:none;color:inherit;white-space:nowrap}
.dzw-tb-action:hover{border-color:var(--dz-primary,#2563eb);color:var(--dz-primary,#2563eb)}
.dzw-tb-pastille{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.74rem;font-weight:600;background:color-mix(in srgb,var(--c,#64748b) 14%,transparent);color:var(--c,#475569);white-space:nowrap}
.dzw-tb-fiche{display:grid;grid-template-columns:minmax(120px,max-content) 1fr;gap:8px 18px;margin:0;font-size:.92rem}
.dzw-tb-fiche dt{opacity:.62;font-weight:500}.dzw-tb-fiche dd{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
.dzw-tb-fiche dd.plein{grid-column:1/-1}
@media (max-width:640px){.dzw-tb-fiche{grid-template-columns:1fr;gap:2px}.dzw-tb-fiche dd{margin-bottom:8px}}
.dzw-tb-pct{font-size:.55em;font-weight:600;opacity:.6;margin-left:6px;letter-spacing:0}
.dzw-tb[role=button]{cursor:pointer;transition:border-color .15s,box-shadow .15s}
.dzw-tb[role=button]:hover{border-color:var(--dz-primary,#2563eb)}
.dzw-tb.actif{border-color:var(--dz-primary,#2563eb);box-shadow:0 0 0 3px color-mix(in srgb,var(--dz-primary,#2563eb) 18%,transparent)}
.dzw-tb.alerte .dzw-tb-kpi b{color:#b91c1c}
.dzw-tb-note{margin:0;font-size:.86rem;opacity:.85;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.dzw-tb-bouton-lien{display:inline-flex;align-items:center;padding:9px 16px;border-radius:10px;background:var(--dz-primary,#2563eb);color:var(--dz-on-primary,#fff)!important;text-decoration:none;font-weight:600;min-height:40px}
.dzw-tb-bouton-lien.sec{background:transparent;color:inherit!important;border:1px solid var(--dz-border,#e5e7eb)}
.dzw-tb-boutons{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px}
.dzw-tb-admin{border-color:color-mix(in srgb,#b45309 45%,var(--dz-border,#e5e7eb));box-shadow:inset 0 3px 0 #b45309}
.dzw-tb-niveau{font-style:normal;font-size:.62rem;letter-spacing:.04em;margin-left:8px;padding:2px 7px;border-radius:99px;background:#fef3c7;color:#92400e;vertical-align:1px}
.dzw-tb-table tr.dzw-tb-groupe td{background:color-mix(in srgb,var(--dz-primary,#2563eb) 6%,transparent);font-weight:600;cursor:pointer;user-select:none;padding:8px 10px}
.dzw-tb-table tr.dzw-tb-groupe:hover td{background:color-mix(in srgb,var(--dz-primary,#2563eb) 11%,transparent)}
.dzw-tb-table tr.dzw-tb-groupe small{font-weight:500;opacity:.6;margin-left:6px}
.dzw-tb-table tr.dzw-tb-groupe .chev{display:inline-block;width:1em;opacity:.7}
.dzw-tb-bascule-groupes{display:flex;gap:6px;justify-content:flex-end;margin:-4px 0 6px}
.dzw-tb-bascule-groupes button{border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);color:inherit;border-radius:8px;padding:3px 10px;font-size:.78rem;cursor:pointer}
@media (max-width:640px){.dzw-tb-table tr.dzw-tb-groupe{display:block}}
.dzw-tb.dzw-tb-sansbord{border:0;background:none;padding:0}
.dzw-tb-titre .l1{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dzw-tb-titre h1{margin:0 6px 0 0;font-size:clamp(1.4rem,2.4vw,1.85rem);letter-spacing:-.02em;line-height:1.2}
.dzw-tb-titre p{margin:4px 0 0;opacity:.7;font-size:.93rem}
.dzw-tb-l.gras{font-weight:600}.dzw-tb-l.discret{opacity:.62;font-size:.82rem}.dzw-tb-l.mono{font-family:ui-monospace,Menlo,monospace;font-size:.8rem;opacity:.75}
.dzw-tb-l.alerte{color:#b45309;font-size:.8rem}
.dzw-tb-badges{display:flex;flex-wrap:wrap;gap:4px;margin-top:3px}
.dzw-tb-table tr.att td:first-child{box-shadow:inset 3px 0 0 #f59e0b}
.dzw-tb-barres.pc .dzw-tb-barre{grid-template-columns:minmax(80px,30%) 1fr auto 44px}
.dzw-tb-barre small{opacity:.6;text-align:right;font-variant-numeric:tabular-nums}
.dzw-tb-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.dzw-tb-tuile{display:flex;flex-direction:column;border:1px solid var(--dz-border,#e5e7eb);border-radius:12px;overflow:hidden;text-decoration:none;color:inherit;background:var(--dz-surface,#fff);transition:transform .15s,box-shadow .15s}
.dzw-tb-tuile:hover{transform:translateY(-2px);box-shadow:0 12px 28px -18px rgba(15,23,42,.45)}
.dzw-tb-tuile .img{height:120px;background:color-mix(in srgb,var(--dz-primary,#2563eb) 10%,transparent) center/cover no-repeat;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.6rem;color:var(--dz-primary,#2563eb)}
.dzw-tb-tuile .bd{padding:10px 12px;display:grid;gap:2px;font-size:.88rem}
.dzw-tb-tuile .tt{font-size:1.05rem;font-weight:700}
.dzw-tb-tuile .ft{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:6px;padding:8px 12px;border-top:1px solid var(--dz-border,#e5e7eb);font-size:.78rem}
.mut{opacity:.65}.mono{font-family:ui-monospace,Menlo,monospace}
.dzw-tb-puces{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;align-items:center}
.dzw-tb-puce{display:inline-flex;align-items:center;gap:4px;padding:3px 4px 3px 10px;border-radius:99px;background:color-mix(in srgb,var(--dz-primary,#2563eb) 10%,transparent);font-size:.8rem}
.dzw-tb-puce button{border:0;background:none;cursor:pointer;font-size:1rem;line-height:1;padding:2px 6px;border-radius:99px;color:inherit}
.dzw-tb-puce button:hover{background:color-mix(in srgb,var(--dz-primary,#2563eb) 20%,transparent)}
.dzw-tb-bouton{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:10px;border:1px solid var(--dz-border,#d1d5db);background:var(--dz-surface,#fff);color:inherit;cursor:pointer;font:inherit;font-size:.88rem;min-height:40px}
.dzw-tb-bouton:hover{border-color:var(--dz-primary,#2563eb)}
.dzw-tb-modale{position:fixed;inset:0;z-index:1000;background:rgba(15,23,42,.5);display:flex;align-items:center;justify-content:center;padding:20px}
.dzw-tb-modale .boite{background:var(--dz-surface,#fff);color:var(--dz-text,#0f172a);border-radius:14px;width:min(900px,100%);max-height:92vh;display:flex;flex-direction:column;overflow:hidden}
.dzw-tb-modale .tete{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid var(--dz-border,#e5e7eb)}
.dzw-tb-modale .tete button{border:1px solid var(--dz-border,#d1d5db);background:none;border-radius:8px;padding:6px 12px;cursor:pointer;color:inherit}
.dzw-tb-modale .dzw-tb-fiche{padding:12px 16px;border-bottom:1px solid var(--dz-border,#e5e7eb)}
.dzw-tb-doc{flex:1;min-height:60vh;border:0;width:100%;background:#fff}
.dzw-tb-vide,.dzw-tb-err{padding:18px 4px;text-align:center;opacity:.7;font-size:.88rem}
.dzw-tb-err{color:#b91c1c;opacity:1}
.dzw-tb-sq{border-radius:8px;background:linear-gradient(90deg,color-mix(in srgb,var(--dz-text,#0f172a) 6%,transparent) 25%,color-mix(in srgb,var(--dz-text,#0f172a) 11%,transparent) 37%,color-mix(in srgb,var(--dz-text,#0f172a) 6%,transparent) 63%);background-size:400% 100%;animation:dzwtbsq 1.3s ease infinite}
@keyframes dzwtbsq{0%{background-position:100% 50%}100%{background-position:0 50%}}
.dzw-tb.charge>*:not(h3):not(.dzw-tb-sq){opacity:.55;transition:opacity .2s}
.dzw-tb-filtres{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}
.dzw-tb-filtres label{display:grid;gap:4px;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.03em;opacity:.85}
.dzw-tb-filtres select,.dzw-tb-filtres input{font:inherit;font-size:.88rem;text-transform:none;letter-spacing:0;font-weight:400;padding:7px 10px;border:1px solid var(--dz-border,#d1d5db);border-radius:10px;background:var(--dz-surface,#fff);color:inherit;min-height:38px;min-width:130px}
.dzw-tb-filtres input[type=search]{min-width:220px}
.dzw-tb .raz{border:0;background:none;color:var(--dz-primary,#2563eb);cursor:pointer;font-size:.85rem;padding:8px 4px;min-height:38px}
.dzw-tb-periodes{display:inline-flex;border:1px solid var(--dz-border,#d1d5db);border-radius:10px;overflow:hidden}
.dzw-tb-periodes button{border:0;background:var(--dz-surface,#fff);color:inherit;padding:8px 11px;font-size:.84rem;cursor:pointer;min-height:38px}
.dzw-tb-periodes button+button{border-left:1px solid var(--dz-border,#d1d5db)}
.dzw-tb-periodes button.on{background:var(--dz-primary,#2563eb);color:#fff}
@media (max-width:640px){
  .dzw-tb{padding:14px}
  .dzw-tb-table thead{display:none}
  .dzw-tb-table tr{display:grid;grid-template-columns:1fr auto;gap:2px 12px;padding:10px 2px;border-bottom:1px solid var(--dz-border,#e5e7eb)}
  .dzw-tb-table td{border:0;padding:0}
  .dzw-tb-table td:first-child{font-weight:600}
  .dzw-tb-table td.num{text-align:right}
  .dzw-tb-filtres label,.dzw-tb-filtres select,.dzw-tb-filtres input,.dzw-tb-filtres input[type=search]{min-width:0;width:100%}
  .dzw-tb-filtres>*{flex:1 1 100%}
  .dzw-tb-periodes{display:grid;grid-template-columns:repeat(auto-fit,minmax(52px,1fr))}
  .dzw-tb-periodes button{padding:8px 2px;font-size:.72rem;white-space:nowrap}
  .dzw-tb-periodes button+button{border-left:0}
  .dzw-tb-periodes button:not(:last-child){border-right:1px solid var(--dz-border,#d1d5db)}
}`);

const PALETTE = ["var(--dz-primary,#2563eb)", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6", "#64748b", "#a3a3a3"];
const NF = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1 });
const NF0 = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 0 });

export const formater = (v, fmt) => {
  /* oui / non : booléen Postgres (true, 1, "t"…) ; vide = non */
  if (fmt === "oui_non") return [true, 1, "1", "t", "true", "oui"].includes(typeof v === "string" ? v.toLowerCase() : v) ? "oui" : "non";
  if (v === null || v === undefined || v === "") return "—";
  if (fmt === "date" || fmt === "dateheure") {
    const d = new Date(v);
    if (isNaN(d)) return String(v);
    return fmt === "date" ? d.toLocaleDateString("fr-FR") : d.toLocaleString("fr-FR", { day: "2-digit", month: "2-digit", year: "2-digit", hour: "2-digit", minute: "2-digit" });
  }
  if (fmt === "age") {
    const m = (Date.now() - new Date(v)) / 6e4;
    if (isNaN(m)) return String(v);
    return m < 60 ? `${Math.max(1, Math.round(m))} min` : m < 1440 ? `${Math.round(m / 60)} h` : `${Math.round(m / 1440)} j`;
  }
  if (fmt === "brut") return String(v);
  if (fmt === "heure") { const d = new Date(v); return isNaN(d) ? String(v) : `${d.toLocaleTimeString("fr-FR")}.${String(d.getMilliseconds()).padStart(3, "0")}`; }
  if (fmt === "ms") { const n = +v; return isNaN(n) ? String(v) : n < 1000 ? `${Math.round(n)} ms` : `${(n / 1000).toFixed(2)} s`; }
  if (fmt === "jour") { const d = new Date(v); return isNaN(d) ? String(v) : d.toLocaleDateString("fr-FR", { day: "2-digit", month: "2-digit", year: "2-digit" }); }
  if (fmt === "depuis") {
    const m = (Date.now() - new Date(v)) / 6e4;
    if (isNaN(m)) return String(v);
    return m < 60 ? `il y a ${Math.max(1, Math.round(m))} min` : m < 1440 ? `il y a ${Math.round(m / 60)} h` : `il y a ${Math.round(m / 1440)} j`;
  }
  const n = +v;
  if (isNaN(n)) return String(v);
  if (fmt === "euro") return NF0.format(n) + " €";
  if (fmt === "pourcent") return NF.format(n) + " %";
  if (fmt === "minutes") return n < 60 ? `${NF0.format(n)} min` : n < 1440 ? `${NF.format(n / 60)} h` : `${NF.format(n / 1440)} j`;
  return Math.abs(n) >= 100 ? NF0.format(n) : NF.format(n);
};

/* ── paramètres partagés : l'adresse de la page ─────────────────────────── */
const lireUrl = () => Object.fromEntries(new URLSearchParams(location.search));
const ecrireUrl = (obj) => {
  const u = new URL(location.href);
  u.search = new URLSearchParams(Object.entries(obj).filter(([, v]) => v !== "" && v != null)).toString();
  history.pushState(null, "", u);
  window.dispatchEvent(new Event("dz:filtres"));
};
window.addEventListener("popstate", () => window.dispatchEvent(new Event("dz:filtres")));

const charger = async (source, params) => {
  const r = await fetch(`/dysizz/donnees/${encodeURIComponent(source)}?${new URLSearchParams(params)}`, { credentials: "same-origin", headers: { Accept: "application/json" } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.erreur || `HTTP ${r.status}`);
  return j;
};

/* listes des filtres lues dans une source : une fois par page (la barre est redessinée à chaque filtre) */
const LISTES = new Map();
const listeSource = (source, params) => {
  const k = source + "?" + (params || "");
  if (!LISTES.has(k)) LISTES.set(k, charger(source, { par_page: 200, ...(params ? Object.fromEntries(new URLSearchParams(params)) : {}) }).catch((e) => { LISTES.delete(k); throw e; }));
  return LISTES.get(k);
};

/* libellés lus dans une autre source (ex. identifiant d'agence → nom), une fois par page */
const LIBELLES = new Map();
const libellesDe = (source, cle, champ) => {
  const k = `${source}|${cle}|${champ}`;
  if (!LIBELLES.has(k)) LIBELLES.set(k, charger(source, { par_page: 200 }).then((d) => Object.fromEntries((d.lignes || []).map((l) => [String(l[cle]), l[champ]]))).catch(() => ({})));
  return LIBELLES.get(k);
};

/* condition sur une ligne : { champ, egal | non | vide | gt | lt } ; tableau = toutes */
const vrai = (si, l) => {
  if (!si) return true;
  if (Array.isArray(si)) return si.every((x) => vrai(x, l));
  const v = l[si.champ];
  const videV = v === null || v === undefined || v === "" || v === 0 || v === "0" || v === false;
  if (si.vide !== undefined) return si.vide ? videV : !videV;
  if (si.egal !== undefined) return [].concat(si.egal).map(String).includes(String(v));
  if (si.non !== undefined) return ![].concat(si.non).map(String).includes(String(v));
  /* une comparaison ne s'applique qu'à une valeur présente */
  if (si.gt !== undefined) return v !== null && v !== undefined && v !== "" && +v > +si.gt;
  if (si.lt !== undefined) return v !== null && v !== undefined && v !== "" && +v < +si.lt;
  return !videV;
};
/* « {prenom} {nom} », « {prix|euro} », « {source|libelle} » */
/* segments séparés par « · » : un segment dont toutes les valeurs sont vides disparaît
   (« {type} · {pieces} pièces · {surface} m² » sans surface → « Maison · 4 pièces ») */
const modele = (tpl, l, o) => String(tpl ?? "").split(" · ").map((seg) => {
  let n = 0, vides = 0;
  const r = seg.replace(/\{(\w+)(?:\|(\w+))?\}/g, (_, k, f) => {
    const v = l[k];
    n++;
    if (v === null || v === undefined || v === "") { vides++; return f === "libelle" ? libelle(o, v) : ""; }
    if (f === "libelle") return libelle(o, v);
    return f ? formater(v, f) : String(v);
  });
  return n && vides === n ? "" : r;
}).filter((x) => x.trim()).join(" · ").replace(/\s+/g, " ").trim();
/* « @champ » : adresse toute faite lue dans la ligne (seulement une adresse du site, commençant par « / ») */
const lienDe = (tpl, l) => {
  const m = /^@(\w+)$/.exec(String(tpl));
  if (m) { const v = String(l[m[1]] ?? ""); return /^\/(?!\/)/.test(v) ? v : null; }
  return String(tpl).replace(/\{(\w+)\}/g, (_, k) => encodeURIComponent(l[k] ?? ""));
};

/* ── vues ──────────────────────────────────────────────────────────────── */
const vueKpi = (el, d, o) => {
  const m = o.mesure || Object.keys(d.valeurs || {})[0];
  const v = d.valeurs ? d.valeurs[m] : null;
  /* part d'un total (ex. « bien non retrouvé » sur les demandes réelles) */
  const den = o.sur && d.valeurs ? +d.valeurs[o.sur] || 0 : null;
  /* carte qui n'a rien à dire quand elle vaut zéro (ex. « lignes repliées ») */
  if (o.cacherZero && !(+v)) { el.hidden = true; return h("div", {}); }
  const kids = [h("b", {}, formater(v, o.format), den !== null ? h("span", { class: "dzw-tb-pct" }, ` ${den ? Math.round((+v / den) * 100) : 0} %`) : null)];
  if (d.precedent && d.precedent[m] != null && v != null) {
    const p = +d.precedent[m];
    const diff = +v - p;
    const pct = p ? Math.round((diff / p) * 100) : null;
    const cls = diff > 0 ? "up" : diff < 0 ? "down" : "";
    kids.push(h("span", { class: `dzw-tb-delta ${cls} ${o.inverse ? "inv" : ""}`, title: `période précédente : ${formater(p, o.format)}` },
      diff > 0 ? "▲" : diff < 0 ? "▼" : "=", pct !== null ? ` ${pct > 0 ? "+" : ""}${pct} %` : ` ${formater(diff, o.format)}`));
  }
  /* sous-titre : peut citer les autres mesures, ex. « dont {exploitables} exploitables » */
  if (o.sous) kids.push(h("div", { class: "dzw-tb-sous" }, /\{\w+/.test(o.sous) ? modele(o.sous, d.valeurs || {}, o) : o.sous));
  /* carte cliquable : pose ses filtres, ou les retire si elle est déjà active */
  if (o.clic) {
    const u = lireUrl(), actif = Object.entries(o.clic).every(([k, x]) => String(u[k] ?? "") === String(x));
    el.classList.toggle("actif", actif);
    el.classList.toggle("alerte", o.alerte !== false && +v > 0);
    el.setAttribute("role", "button"); el.tabIndex = 0;
    const go = () => { const n = { ...lireUrl(), page: "" }; for (const [k, x] of Object.entries(o.clic)) n[k] = actif ? "" : x; ecrireUrl(n); };
    el.onclick = go; el.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } };
  }
  return h("div", { class: `dzw-tb-kpi${["depuis", "date", "dateheure", "jour", "age"].includes(o.format) ? " txt" : ""}` }, kids);
};

const libelle = (o, cle) => (cle === null || cle === undefined || cle === "" ? "(vide)" : (o.libelles && o.libelles[cle]) || String(cle));

const vueCourbe = (el, d, o) => {
  const lignes = d.lignes || [];
  if (!lignes.length) return h("div", { class: "dzw-tb-vide" }, "Aucune donnée sur la période.");
  const mesures = o.mesures || [o.mesure || Object.keys(lignes[0]).find((k) => k !== "cle")];
  /* repère à la taille réelle du bloc : le texte des axes garde sa taille sur téléphone */
  const W = Math.max(280, Math.round(el.clientWidth - 36) || 640), H = o.hauteur || 200, P = { g: 34, d: 8, h: 10, b: 22 };
  const max = Math.max(1, ...lignes.flatMap((l) => mesures.map((m) => +l[m] || 0)));
  const x = (i) => P.g + (lignes.length === 1 ? (W - P.g - P.d) / 2 : (i * (W - P.g - P.d)) / (lignes.length - 1));
  const y = (v) => H - P.b - ((+v || 0) / max) * (H - P.h - P.b);
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", `${o.titre || "Courbe"} : ${lignes.length} points, maximum ${formater(max, o.format)}`);
  const add = (tag, attrs) => { const e = document.createElementNS(ns, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); svg.appendChild(e); return e; };
  /* graduations rondes (1, 2, 5 × 10ⁿ) : jamais « 33,3 demandes » */
  const pasAxe = (() => { const brut = max / 3, p = 10 ** Math.floor(Math.log10(brut || 1)); return [1, 2, 5, 10].map((m) => m * p).find((m) => m >= brut) || brut; })();
  for (let k = 0; k * pasAxe <= max * 1.001 && k < 8; k++) {
    const v = k * pasAxe, yy = y(v);
    add("line", { x1: P.g, x2: W - P.d, y1: yy, y2: yy, stroke: "currentColor", "stroke-opacity": k ? 0.08 : 0.2 });
    add("text", { x: P.g - 6, y: yy + 3, "text-anchor": "end", class: "dzw-tb-axe" }).textContent = formater(v, o.format === "euro" ? "euro" : null);
  }
  const pas = Math.max(1, Math.ceil(lignes.length / Math.max(3, Math.floor(W / 90))));
  lignes.forEach((l, i) => {
    if (i % pas && i !== lignes.length - 1) return;
    const dt = new Date(String(l.cle).length <= 10 ? l.cle + "T12:00:00" : l.cle);
    add("text", { x: x(i), y: H - 5, "text-anchor": "middle", class: "dzw-tb-axe" }).textContent = isNaN(dt) ? String(l.cle) : dt.toLocaleDateString("fr-FR", d.par === "mois" ? { month: "short" } : { day: "2-digit", month: "2-digit" });
  });
  mesures.forEach((m, k) => {
    const c = PALETTE[k % PALETTE.length];
    const pts = lignes.map((l, i) => `${x(i)},${y(l[m])}`).join(" ");
    if (k === 0) add("polygon", { points: `${x(0)},${H - P.b} ${pts} ${x(lignes.length - 1)},${H - P.b}`, fill: c, "fill-opacity": 0.1 });
    add("polyline", { points: pts, fill: "none", stroke: c, "stroke-width": 2.2, "stroke-linejoin": "round", "stroke-linecap": "round" });
  });
  const curseur = add("line", { y1: P.h, y2: H - P.b, stroke: "currentColor", "stroke-opacity": 0, "stroke-dasharray": "3 3" });
  const wrap = h("div", { style: { position: "relative" } }, svg);
  const bulle = h("div", { class: "dzw-tb-bulle", hidden: true });
  wrap.appendChild(bulle);
  const survol = (ev) => {
    const r = svg.getBoundingClientRect();
    const px = ((ev.clientX - r.left) / r.width) * W;
    const i = Math.max(0, Math.min(lignes.length - 1, Math.round(((px - P.g) / (W - P.g - P.d)) * (lignes.length - 1))));
    const l = lignes[i];
    curseur.setAttribute("x1", x(i)); curseur.setAttribute("x2", x(i)); curseur.setAttribute("stroke-opacity", 0.35);
    const dt = new Date(String(l.cle).length <= 10 ? l.cle + "T12:00:00" : l.cle);
    bulle.hidden = false;
    bulle.textContent = `${isNaN(dt) ? l.cle : dt.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short" })} · ${mesures.map((m) => `${o.libelles && o.libelles[m] ? o.libelles[m] + " " : ""}${formater(l[m], o.format)}`).join(" · ")}`;
    bulle.style.left = `${(x(i) / W) * r.width}px`;
    bulle.style.top = `${(y(l[mesures[0]]) / H) * r.height}px`;
  };
  svg.addEventListener("pointermove", survol);
  svg.addEventListener("pointerdown", survol);
  svg.addEventListener("pointerleave", () => { bulle.hidden = true; curseur.setAttribute("stroke-opacity", 0); });
  return wrap;
};

const vueBarres = (el, d, o) => {
  const lignes = (d.lignes || []).slice(0, o.max || 12);
  if (!lignes.length) return h("div", { class: "dzw-tb-vide" }, "Aucune donnée sur la période.");
  const m = o.mesure || Object.keys(lignes[0]).find((k) => k !== "cle");
  const max = Math.max(1, ...lignes.map((l) => +l[m] || 0));
  const filtre = el.getAttribute("data-filtre");
  const tot = (d.lignes || []).reduce((x, l) => x + (+l[m] || 0), 0) || 1;
  return h("div", { class: `dzw-tb-barres${o.pourcent ? " pc" : ""}` }, lignes.map((l) => h("div", {
    class: "dzw-tb-barre", title: `${libelle(o, l.cle)} : ${formater(l[m], o.format)}`, "data-cle": filtre || o.lienBarre ? String(l.cle ?? "") : null,
    onclick: o.lienBarre ? () => (location.href = lienDe(o.lienBarre, l)) : filtre ? () => ecrireUrl({ ...lireUrl(), [filtre]: String(l.cle ?? "") }) : null,
  }, h("span", {}, libelle(o, l.cle)), h("span", {}, h("i", { style: { width: `${((+l[m] || 0) / max) * 100}%` } })), h("b", {}, formater(l[m], o.format)),
    o.pourcent ? h("small", {}, `${Math.round(((+l[m] || 0) / tot) * 100)} %`) : null)));
};

const vueAnneau = (el, d, o) => {
  /* sans groupe : chaque mesure est une part (ex. lus par gabarit / lus par l'IA) */
  const lignes = d.lignes || (d.valeurs ? Object.entries(d.valeurs).filter(([k]) => !o.mesures || o.mesures.includes(k)).map(([k, v]) => ({ cle: k, v })) : []);
  if (!d.lignes && d.valeurs) o = { ...o, mesure: "v" };
  if (!lignes.length) return h("div", { class: "dzw-tb-vide" }, "Aucune donnée sur la période.");
  const m = o.mesure || Object.keys(lignes[0]).find((k) => k !== "cle");
  const top = lignes.slice(0, 7);
  const reste = lignes.slice(7).reduce((s, l) => s + (+l[m] || 0), 0);
  if (reste) top.push({ cle: "Autres", [m]: reste });
  const tot = top.reduce((s, l) => s + (+l[m] || 0), 0) || 1;
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", "0 0 42 42");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", top.map((l) => `${libelle(o, l.cle)} ${Math.round(((+l[m] || 0) / tot) * 100)} %`).join(", "));
  let acc = 0;
  top.forEach((l, i) => {
    const part = ((+l[m] || 0) / tot) * 100;
    const c = document.createElementNS(ns, "circle");
    Object.entries({ cx: 21, cy: 21, r: 15.9155, fill: "none", stroke: PALETTE[i % PALETTE.length], "stroke-width": 6, "stroke-dasharray": `${part} ${100 - part}`, "stroke-dashoffset": 25 - acc }).forEach(([k, v]) => c.setAttribute(k, v));
    svg.appendChild(c);
    acc += part;
  });
  const t = document.createElementNS(ns, "text");
  Object.entries({ x: 21, y: 23.5, "text-anchor": "middle", "font-size": 7, "font-weight": 700, fill: "currentColor" }).forEach(([k, v]) => t.setAttribute(k, v));
  t.textContent = formater(tot, o.format);
  svg.appendChild(t);
  return h("div", { class: "dzw-tb-anneau" }, svg, h("div", { class: "dzw-tb-legende" }, top.map((l, i) => h("span", {}, h("i", { style: { background: PALETTE[i % PALETTE.length] } }), libelle(o, l.cle), h("b", {}, `${Math.round(((+l[m] || 0) / tot) * 100)} %`)))));
};

const cellule = (v, col, o, ligne) => {
  /* plusieurs lignes dans la cellule, et des badges selon la ligne */
  if (col.lignes || col.badges) {
    const out = [];
    for (const x of col.lignes || [{ champ: col.champ, format: col.format }]) {
      if (x.si && !vrai(x.si, ligne)) continue;
      /* âge en pastille : vert < 1 h, orange < 24 h, rouge au-delà */
      if (x.style === "age") {
        const m = (Date.now() - new Date(ligne[x.champ])) / 6e4;
        if (!ligne[x.champ] || isNaN(m)) continue;
        out.push(h("div", {}, h("span", { class: "dzw-tb-pastille", style: { "--c": m < 60 ? "#047857" : m < 1440 ? "#b45309" : "#b91c1c" } }, formater(ligne[x.champ], "age"))));
        continue;
      }
      const brut = x.modele === undefined ? ligne[x.champ] : null;
      if (x.modele === undefined && (brut === null || brut === undefined || brut === "") && x.vide === undefined) continue;
      let t = x.modele !== undefined ? modele(x.modele, ligne, o) : x.libelles ? libelle(o, brut) : brut === null || brut === undefined || brut === "" ? "" : formater(brut, x.format || null);
      /* texte long coupé (le message d'un acquéreur dans une liste) */
      const court = x.court || col.court;
      if (court && t && t.length > court) t = t.slice(0, court).trimEnd() + "…";
      if (!t && x.vide === undefined) continue;
      const contenu = x.lien ? h("a", { href: lienDe(x.lien, ligne), onclick: (e) => e.stopPropagation() }, t || x.vide) : t || x.vide;
      out.push(h("div", { class: `dzw-tb-l ${x.style || ""}` }, contenu));
    }
    const badges = (col.badges || []).filter((b) => vrai(b.si, ligne) && modele(b.texte, ligne, o));
    if (badges.length) out.push(h("div", { class: "dzw-tb-badges" }, badges.map((b) => h("span", { class: "dzw-tb-pastille", style: { "--c": b.couleur || "#64748b" }, title: b.aide ? modele(b.aide, ligne, o) : null }, modele(b.texte, ligne, o)))));
    return out.length ? out : "—";
  }
  if (col.pastilles) {
    const p = col.pastilles[v] || col.pastilles["*"];
    return h("span", { class: "dzw-tb-pastille", style: p && p.couleur ? { "--c": p.couleur } : null }, p && p.texte ? p.texte : v ?? "—");
  }
  if (col.bouton) return h("a", { class: "dzw-tb-action", href: String(col.lien || "#").replace(/\{(\w+)\}/g, (_, k) => encodeURIComponent(ligne[k] ?? "")), onclick: (e) => e.stopPropagation() }, col.bouton);
  if (col.libelles) return libelle(o, v);
  if (col.modele) return String(col.modele).replace(/\{(\w+)\}/g, (_, k) => (ligne[k] == null ? "" : String(ligne[k])));
  return formater(v, col.format || null);
};

/* ── sélection multiple et modification en lot (réglage « selection ») ─────────────────
   selection = { table, cle: "id", champs: ["temps", "groupe", …], libelles: { champ: { valeur: libellé } } }
   Cases à cocher, « tout sélectionner » (tous les résultats des filtres), puis « Modifier la sélection » :
   un ou plusieurs changements (champ → valeur, ou vider), appliqués ligne par ligne par l'API de Saltcorn
   (droits, champs protégés et déclencheurs vérifiés par le serveur). */
const cleSel = (o) => (o.selection && o.selection.cle) || "id";
const caseLigne = (l, o, etat) => {
  const id = String(l[cleSel(o)]);
  return h("input", { type: "checkbox", "aria-label": "Sélectionner", checked: etat.sel.has(id), onchange: (e) => { e.target.checked ? etat.sel.add(id) : etat.sel.delete(id); etat.majSel(); } });
};
const caseTout = (lignes, o, etat) => {
  const ids = lignes.map((l) => String(l[cleSel(o)]));
  const tous = ids.length && ids.every((x) => etat.sel.has(x));
  return h("input", { type: "checkbox", "aria-label": "Tout sélectionner sur cette page", checked: !!tous, onchange: (e) => { ids.forEach((x) => (e.target.checked ? etat.sel.add(x) : etat.sel.delete(x))); etat.majSel(); etat.relire("force"); } });
};
const selectionner = (lignes, o, etat) => { lignes.forEach((l) => etat.sel.add(String(l[cleSel(o)]))); etat.majSel(); etat.relire("force"); };

const SCHEMAS = new Map();
const schemaDe = (table, champs) => {
  const k = table + "|" + (champs || []).join(",");
  if (!SCHEMAS.has(k)) SCHEMAS.set(k, fetch(`/dysizz/fiche/${encodeURIComponent(table)}?${new URLSearchParams(champs && champs.length ? { champs: champs.join(",") } : {})}`, { credentials: "same-origin", headers: { Accept: "application/json" } })
    .then(async (r) => { const j = await r.json().catch(() => ({})); if (!r.ok) throw new Error(j.erreur || `HTTP ${r.status}`); return j; }));
  return SCHEMAS.get(k);
};
const humainSel = (v) => { const x = String(v ?? "").replace(/_/g, " "); return x.charAt(0).toUpperCase() + x.slice(1); };
/* un contrôle de valeur pour un champ décrit par /dysizz/fiche (choix, clé, oui/non, nombre, date, texte) */
const controleValeur = (c, libs) => {
  const VIDE = "__vide__";
  if (c.type === "choix" || c.type === "cle" || c.type === "oui_non") {
    const opts = c.type === "oui_non" ? [["true", "oui"], ["false", "non"]] : c.type === "choix" ? (c.options || []).map((x) => [x, (libs && libs[x]) || humainSel(x)]) : c.options || [];
    const sel = h("select", {}, h("option", { value: "" }, "— choisir —"), opts.map(([v, t]) => h("option", { value: v }, String(t))), c.requis ? null : h("option", { value: VIDE }, "(vider ce champ)"));
    return { el: sel, lire: () => (sel.value === "" ? undefined : sel.value === VIDE ? null : c.type === "oui_non" ? sel.value === "true" : c.type === "cle" && /^\d+$/.test(sel.value) ? +sel.value : sel.value) };
  }
  const inp = h("input", { type: c.type === "nombre" ? "number" : c.type === "date" ? "date" : "text", placeholder: "nouvelle valeur (vide = vider)" });
  return { el: inp, lire: () => (inp.value === "" ? (c.requis ? undefined : null) : c.type === "nombre" ? Number(inp.value) : inp.value) };
};

const barreSelection = (o, etat) => {
  const barre = h("div", { class: "dzw-tb-sel", hidden: true });
  const S = o.selection;
  let panneau = null;
  const ecrire = async (id, corps) => {
    const r = await fetch(`/api/${encodeURIComponent(S.table)}/${encodeURIComponent(id)}`, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", Accept: "application/json", "CSRF-Token": csrf() }, body: JSON.stringify(corps) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.error) throw new Error(j.error === "Not authorized" ? "non autorisé" : j.error || `HTTP ${r.status}`);
  };
  const ouvrir = async () => {
    if (panneau) { panneau.remove(); panneau = null; return; }
    panneau = h("div", { class: "dzw-tb-sel-panneau" }, h("div", { class: "dzw-tb-sq", style: { height: "60px" } }));
    barre.appendChild(panneau);
    let d;
    try { d = await schemaDe(S.table, S.champs); } catch (e) { panneau.replaceChildren(h("div", { class: "dzw-tb-err" }, `Modification impossible : ${e.message}`)); return; }
    const champs = d.champs.filter((c) => !c.lecture_seule && !c.proprietaire);
    const lignes = h("div", { class: "dzw-tb-sel-lignes" });
    const ajouter = () => {
      const choix = h("select", { "aria-label": "Champ à modifier" }, h("option", { value: "" }, "— quel champ ? —"), champs.map((c) => h("option", { value: c.nom }, (S.titres && S.titres[c.nom]) || c.libelle)));
      const place = h("span", { class: "val" });
      let ctl = null;
      choix.addEventListener("change", () => { const c = champs.find((x) => x.nom === choix.value); ctl = c ? controleValeur(c, (S.libelles || {})[c.nom] || (o.libelles && o.libelles[c.nom])) : null; place.replaceChildren(ctl ? ctl.el : ""); });
      const ligne = h("div", { class: "dzw-tb-sel-ligne" }, choix, h("span", { class: "fl" }, "→"), place, h("button", { type: "button", class: "moins", "aria-label": "Retirer ce changement", onclick: () => ligne.remove() }, "×"));
      ligne.lire = () => (choix.value && ctl ? [choix.value, ctl.lire()] : null);
      lignes.appendChild(ligne);
    };
    ajouter();
    const msg = h("div", { class: "dzw-tb-sel-msg" });
    const go = h("button", { type: "button", class: "ok" }, `Appliquer à ${etat.sel.size}`);
    go.addEventListener("click", async () => {
      const changements = [...lignes.children].map((x) => x.lire()).filter((x) => x && x[1] !== undefined);
      if (!changements.length) { msg.textContent = "Choisissez au moins un champ et sa nouvelle valeur."; return; }
      const corps = Object.fromEntries(changements);
      const ids = [...etat.sel];
      if (!confirm(`Modifier ${ids.length} ligne(s) ?`)) return;
      go.disabled = true;
      const erreurs = [];
      let fait = 0;
      for (const id of ids) {
        try { await ecrire(id, corps); fait++; } catch (e) { erreurs.push(`${id} : ${e.message}`); }
        msg.textContent = `${fait + erreurs.length} / ${ids.length}…`;
      }
      msg.textContent = erreurs.length ? `${fait} modifiée(s), ${erreurs.length} refusée(s) : ${erreurs.slice(0, 3).join(" ; ")}${erreurs.length > 3 ? "…" : ""}` : `${fait} ligne(s) modifiée(s).`;
      go.disabled = false;
      if (!erreurs.length) { etat.sel.clear(); panneau.remove(); panneau = null; etat.majSel(); }
      etat.relire("force");
      window.dispatchEvent(new Event("dz:rafraichir"));
    });
    panneau.replaceChildren(h("b", {}, "Nouvelles valeurs pour la sélection"), lignes,
      h("div", { class: "dzw-tb-sel-act" }, h("button", { type: "button", class: "sec", onclick: ajouter }, "+ un autre changement"), go), msg);
  };
  etat.majSel = () => {
    const n = etat.sel.size;
    barre.hidden = !n && !panneau;
    const tete = h("div", { class: "dzw-tb-sel-tete" },
      h("b", {}, `${n} sélectionné${n > 1 ? "s" : ""}`),
      etat.total > n ? h("button", { type: "button", class: "lien", onclick: async (e) => {
        e.target.disabled = true; e.target.textContent = "sélection…";
        const k = cleSel(o);
        for (let page = 1; page <= 10; page++) {
          const d = await charger(o.source, { ...(etat.params || {}), par_page: 200, page });
          (d.lignes || []).forEach((l) => etat.sel.add(String(l[k])));
          if (!d.lignes || d.lignes.length < 200) break;
        }
        etat.majSel(); etat.relire("force");
      } }, `Sélectionner les ${NF0.format(etat.total)} résultats`) : null,
      h("button", { type: "button", class: "ok", onclick: ouvrir }, panneau ? "Fermer" : "Modifier la sélection"),
      h("button", { type: "button", class: "lien", onclick: () => { etat.sel.clear(); if (panneau) { panneau.remove(); panneau = null; } etat.majSel(); etat.relire("force"); } }, "Tout désélectionner"));
    if (barre.firstChild && barre.firstChild.classList.contains("dzw-tb-sel-tete")) barre.firstChild.replaceWith(tete); else barre.prepend(tete);
    if (panneau) { const b = panneau.querySelector(".ok"); if (b) b.textContent = `Appliquer à ${n}`; }
  };
  return barre;
};

const vueListe = (el, d, o, etat) => {
  /* liste groupée : les lignes d'un même groupe se suivent (tri stable, l'ordre de la source est gardé dans chaque groupe) */
  const lignes = o.grouper ? (d.lignes || []).map((l, i) => [l, i]).sort((a, b) => String(a[0][o.grouper] ?? "\uffff").localeCompare(String(b[0][o.grouper] ?? "\uffff"), "fr") || a[1] - b[1]).map((x) => x[0]) : d.lignes || [];
  if (!lignes.length && o.vide) return h("div", { class: "dzw-tb-vide" }, o.vide);
  const cols = o.colonnes || (lignes[0] ? Object.keys(lignes[0]).filter((k) => k !== "id").map((k) => ({ champ: k, titre: k })) : []);
  const numeriques = new Set(cols.filter((c) => ["nombre", "euro", "pourcent", "minutes"].includes(c.format)).map((c) => c.champ));
  const table = h("table", { class: "dzw-tb-table" },
    h("thead", {}, h("tr", {}, o.selection ? h("th", { class: "dzw-tb-case" }, caseTout(lignes, o, etat)) : null, cols.map((c) => h("th", {
      "data-tri": c.tri === false || c.bouton ? null : c.champ, class: d.tri === c.champ ? "on" : null, scope: "col",
      onclick: c.tri === false || c.bouton ? null : () => { etat.tri = c.champ; etat.sens = d.tri === c.champ && d.sens === "desc" ? "asc" : "desc"; etat.page = 1; etat.relire("force"); },
    }, c.bouton ? c.titre || "" : c.titre ?? c.champ, !c.bouton && d.tri === c.champ ? (d.sens === "asc" ? " ▲" : " ▼") : "")))),
    h("tbody", {}, lignes.length ? lignes.flatMap((l, i) => {
      const href = o.lien ? lienDe(o.lien, l) : null;
      /* groupes repliables (ex. par agence) : une ligne d'en-tête quand la valeur change */
      const g = o.grouper ? String(l[o.grouper] ?? "") : null;
      const entete = o.grouper && (i === 0 || String(lignes[i - 1][o.grouper] ?? "") !== g) ? (() => {
        const n = lignes.filter((x) => String(x[o.grouper] ?? "") === g).length;
        const ferme = etat.fermes.has(g);
        return h("tr", { class: `dzw-tb-groupe${ferme ? " ferme" : ""}`, tabindex: 0, "aria-expanded": ferme ? "false" : "true",
          onclick: () => { etat.fermes.has(g) ? etat.fermes.delete(g) : etat.fermes.add(g); etat.relire("force"); },
          onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.currentTarget.click(); } } },
          h("td", { colspan: cols.length + (o.selection ? 1 : 0) }, h("span", { class: "chev" }, ferme ? "▸" : "▾"), " ", g === "" ? o.sansGroupe || "(sans)" : libelle(o, g), h("small", {}, ` ${n}`),
            o.selection ? h("button", { type: "button", class: "dzw-tb-sel-groupe", onclick: (e) => { e.stopPropagation(); selectionner(lignes.filter((x) => String(x[o.grouper] ?? "") === g), o, etat); } }, "sélectionner le groupe") : null));
      })() : null;
      if (o.grouper && etat.fermes.has(g)) return entete ? [entete] : [];
      const tr = h("tr", { class: o.attention && vrai(o.attention, l) ? "att" : null, "data-href": href, tabindex: href ? 0 : null, onclick: href ? () => (location.href = href) : null, onkeydown: href ? (e) => { if (e.key === "Enter") location.href = href; } : null },
        o.selection ? h("td", { class: "dzw-tb-case", onclick: (e) => e.stopPropagation() }, caseLigne(l, o, etat)) : null,
        cols.map((c) => h("td", { class: numeriques.has(c.champ) ? "num" : c.nowrap || c.format === "depuis" || c.format === "dateheure" ? "nw" : null, style: c.largeur ? { minWidth: c.largeur } : null, "data-titre": c.titre || c.champ }, cellule(l[c.champ], c, o, l))));
      return entete ? [entete, tr] : [tr];
    }) : h("tr", {}, h("td", { colspan: (cols.length || 1) + (o.selection ? 1 : 0), class: "dzw-tb-vide" }, o.vide || "Aucun résultat avec ces filtres."))));
  /* tout ouvrir / tout fermer quand la liste est groupée */
  const groupes = o.grouper ? [...new Set(lignes.map((x) => String(x[o.grouper] ?? "")))] : [];
  const bascule = groupes.length > 1 ? h("div", { class: "dzw-tb-bascule-groupes" },
    h("button", { type: "button", onclick: () => { etat.fermes.clear(); etat.relire("force"); } }, "Tout ouvrir"),
    h("button", { type: "button", onclick: () => { groupes.forEach((x) => etat.fermes.add(x)); etat.relire("force"); } }, "Tout fermer")) : null;
  const pages = Math.max(1, Math.ceil((d.total || 0) / (d.par_page || 50)));
  const pied = pages <= 1 && (o.titre || (d.total || 0) <= 1) ? null : h("div", { class: "dzw-tb-pied" },
    h("span", {}, `${NF0.format(d.total || 0)} résultat${d.total > 1 ? "s" : ""}`),
    pages <= 1 ? null : h("span", { style: { display: "flex", gap: "6px", alignItems: "center" } },
      h("button", { type: "button", disabled: d.page <= 1, onclick: () => { etat.page = d.page - 1; etat.relire(true); } }, "‹ Précédent"),
      h("span", {}, `${d.page} / ${pages}`),
      h("button", { type: "button", disabled: d.page >= pages, onclick: () => { etat.page = d.page + 1; etat.relire(true); } }, "Suivant ›")));
  return h("div", { style: { overflowX: "auto" } }, bascule, table, pied);
};

/* grille : une tuile par ligne (portefeuille…) — { titre, lignes[], badge, pied, image } */
const vueGrille = (el, d, o, etat) => {
  const lignes = d.lignes || [];
  if (!lignes.length) return h("div", { class: "dzw-tb-vide" }, o.vide || "Aucun résultat avec ces filtres.");
  const t = o.tuile || {};
  const grille = h("div", { class: "dzw-tb-grille" }, lignes.map((l) => {
    const href = o.lien ? lienDe(o.lien, l) : null;
    const b = (t.badges || []).filter((x) => vrai(x.si, l));
    return h(href ? "a" : "div", { class: "dzw-tb-tuile", href },
      t.image && l[t.image] ? h("div", { class: "img", style: { backgroundImage: `url("${String(l[t.image]).replace(/"/g, "")}")` } }) : h("div", { class: "img vide" }, t.initiales ? modele(t.initiales, l, o).slice(0, 2) : ""),
      h("div", { class: "bd" }, t.titre ? h("div", { class: "tt" }, modele(t.titre, l, o)) : null, (t.lignes || []).map((x) => h("div", { class: "mut" }, modele(x, l, o))).filter((e) => e.textContent)),
      h("div", { class: "ft" }, t.pied ? h("span", { class: "mono" }, modele(t.pied, l, o)) : null, b.map((x) => h("span", { class: "dzw-tb-pastille", style: { "--c": x.couleur || "#64748b" } }, modele(x.texte, l, o)))));
  }));
  const pages = Math.max(1, Math.ceil((d.total || 0) / (d.par_page || 50)));
  return h("div", {}, grille, pages <= 1 && (o.titre || (d.total || 0) <= 1) ? null : h("div", { class: "dzw-tb-pied" }, h("span", {}, `${NF0.format(d.total || 0)} résultat${d.total > 1 ? "s" : ""}`),
    pages <= 1 ? null : h("span", { style: { display: "flex", gap: "6px", alignItems: "center" } },
      h("button", { type: "button", disabled: d.page <= 1, onclick: () => { etat.page = d.page - 1; etat.relire(true); } }, "‹ Précédent"),
      h("span", {}, `${d.page} / ${pages}`),
      h("button", { type: "button", disabled: d.page >= pages, onclick: () => { etat.page = d.page + 1; etat.relire(true); } }, "Suivant ›"))));
};

/* document : ouvre un contenu HTML reçu de l'extérieur (e-mail…) dans un cadre isolé :
   aucun script, aucun formulaire, liens dans un nouvel onglet */
const vueDocument = (el, d, o) => {
  const l = (d.lignes || [])[0];
  if (!l) return h("div", { class: "dzw-tb-vide" }, o.vide || "Rien à afficher.");
  const ouvrir = () => {
    const html = l[o.champHtml] ? String(l[o.champHtml]) : `<pre style="white-space:pre-wrap;font:14px/1.5 system-ui">${String(l[o.champTexte] || "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]))}</pre>`;
    const fr = h("iframe", { sandbox: "", title: o.titre || "Document", class: "dzw-tb-doc" });
    fr.srcdoc = `<!doctype html><meta charset="utf-8"><base target="_blank"><meta http-equiv="Content-Security-Policy" content="script-src 'none'; object-src 'none'; form-action 'none'"><style>body{margin:0;padding:12px;font:14px/1.5 system-ui}img{max-width:100%;height:auto}</style>${html}`;
    const fermer = () => { fond.remove(); document.removeEventListener("keydown", esc); };
    const esc = (e) => { if (e.key === "Escape") fermer(); };
    const fond = h("div", { class: "dzw-tb-modale", onclick: (e) => { if (e.target === fond) fermer(); } },
      h("div", { class: "boite", role: "dialog", "aria-modal": "true" }, h("div", { class: "tete" }, h("b", {}, o.entete ? modele(o.entete, l, o) : o.titre || "Document"), h("button", { type: "button", onclick: fermer }, "Fermer")),
        (o.entetes || []).length ? h("dl", { class: "dzw-tb-fiche" }, o.entetes.flatMap((c) => [h("dt", {}, c.titre), h("dd", {}, formater(l[c.champ], c.format || null))])) : null, fr));
    document.body.appendChild(fond);
    document.addEventListener("keydown", esc);
  };
  return h("button", { type: "button", class: "dzw-tb-bouton", onclick: ouvrir }, o.bouton || "Ouvrir");
};

/* titre : en-tête d'une fiche tiré de la première ligne — grand titre, pastilles, ligne d'information */
const vueTitre = (el, d, o) => {
  const l = (d.lignes || [])[0];
  if (!l) return h("div", { class: "dzw-tb-vide" }, o.vide || "Introuvable.");
  el.classList.add("dzw-tb-sansbord");
  const b = (o.badges || []).filter((x) => vrai(x.si, l));
  return h("div", { class: "dzw-tb-titre" }, h("div", { class: "l1" }, h("h1", {}, modele(o.entete || "", l, o) || o.vide || ""),
    b.map((x) => h("span", { class: "dzw-tb-pastille", style: { "--c": x.couleur || "#64748b" }, title: x.aide ? modele(x.aide, l, o) : null }, modele(x.texte, l, o)))),
    o.sous ? h("p", {}, modele(o.sous, l, o)) : null);
};

/* fiche : la première ligne d'une liste (ou les valeurs d'un agrégat), en libellé → valeur */
const vueFiche = (el, d, o) => {
  const l = (d.lignes || [])[0] || (d.valeurs && !d.lignes ? d.valeurs : null);
  if (!l) return h("div", { class: "dzw-tb-vide" }, "Introuvable.");
  const cols = o.colonnes || Object.keys(l).filter((k) => k !== "id").map((k) => ({ champ: k, titre: k }));
  return h("dl", { class: "dzw-tb-fiche" }, cols.flatMap((c) => (c.titre === "" ? [h("dd", { class: "plein" }, cellule(l[c.champ], c, o, l))] : [h("dt", {}, c.titre ?? c.champ), h("dd", {}, cellule(l[c.champ], c, o, l))])));
};

const vueFiltres = (el, o) => {
  const url = lireUrl();
  const champs = o.champs || [];
  const bar = h("div", { class: "dzw-tb-filtres" });
  const maj = (k, v) => ecrireUrl({ ...lireUrl(), [k]: v, page: "" });
  for (const c of champs) {
    if (c.type === "periode") {
      const choix = c.choix || [["aujourdhui", "Aujourd'hui"], ["7j", "7 jours"], ["30j", "30 jours"], ["90j", "3 mois"], ["tout", "Tout"]];
      const actif = url.du || url.au ? null : url.periode ?? c.defaut ?? "";
      bar.appendChild(h("label", {}, c.titre || "Période", h("div", { class: "dzw-tb-periodes", role: "group" }, choix.map(([v, t]) => h("button", { type: "button", class: actif === v ? "on" : null, "aria-pressed": actif === v ? "true" : "false", onclick: () => ecrireUrl({ ...lireUrl(), periode: v, du: "", au: "", page: "" }) }, t)))));
    } else if (c.type === "texte") {
      const inp = h("input", { type: "search", "data-param": c.param, value: url[c.param] || "", placeholder: c.aide || "Rechercher…" });
      let t;
      inp.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => maj(c.param, inp.value.trim()), 350); });
      bar.appendChild(h("label", {}, c.titre || "Recherche", inp));
    } else if (c.type === "nombre") {
      const inp = h("input", { type: "number", "data-param": c.param, inputmode: "decimal", value: url[c.param] || "", placeholder: c.aide || "", style: { maxWidth: "120px" } });
      let t;
      inp.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => maj(c.param, inp.value.trim()), 450); });
      bar.appendChild(h("label", {}, c.titre || c.param, inp));
    } else if (c.type === "boutons") {
      const actif = url[c.param] ?? "";
      bar.appendChild(h("label", {}, c.titre ?? c.param, h("div", { class: "dzw-tb-periodes", role: "group" }, (c.options || []).map(([v, t]) => h("button", { type: "button", class: String(actif) === String(v) ? "on" : null, "aria-pressed": String(actif) === String(v) ? "true" : "false", onclick: () => maj(c.param, v) }, t)))));
    } else if (c.type === "date") {
      const inp = h("input", { type: "date", value: url[c.param] || "" });
      inp.addEventListener("change", () => ecrireUrl({ ...lireUrl(), [c.param]: inp.value, periode: "", j: "", ...Object.fromEntries(champs.filter((x) => (x.exclut || []).includes(c.param)).map((x) => [x.param, ""])), page: "" }));
      bar.appendChild(h("label", {}, c.titre || c.param, inp));
    } else {
      /* champ exclusif (ex. raccourci de période face à des dates libres) : il s'efface quand l'autre est posé */
      const libre = (c.exclut || []).some((k) => url[k]);
      const sel = h("select", { "aria-label": c.titre || c.param }, h("option", { value: "", selected: libre }, libre && c.libre ? c.libre : c.tous || "Tous"));
      const remplir = (items) => {
        for (const [v, t] of items) sel.appendChild(h("option", { value: v, selected: !libre && String(url[c.param] ?? "") === String(v) && v !== "" }, t));
      };
      if (c.options) remplir(c.options.map((x) => (Array.isArray(x) ? x : [x, (o.libelles && o.libelles[x]) || x])));
      /* liste lue dans une source : groupe (cle) ou liste (c.cle → c.champ, ex. agence → nom) */
      if (c.source) listeSource(c.source, c.params).then((d) => {
        const k = c.cle || "cle";
        const items = (d.lignes || []).filter((l) => l[k] !== null && l[k] !== undefined && l[k] !== "").map((l) => [l[k], (c.libelles && c.libelles[l[k]]) || (c.champ && l[c.champ]) || (o.libelles && o.libelles[l[k]]) || l[k]]);
        remplir(items);
        /* l'étiquette du filtre posé montre le nom, pas l'identifiant */
        const x = items.find(([v]) => String(v) === String(url[c.param] ?? ""));
        const b = x && bar.parentNode && bar.parentNode.querySelector(`[data-puce="${c.param}"]`);
        if (b) b.textContent = `${c.titre || c.param} : ${x[1]}`;
      }).catch(() => {});
      /* « Tous » sur un champ qui a une valeur par défaut : on l'écrit (« tout »), sinon le défaut reviendrait au rechargement */
      sel.addEventListener("change", () => ecrireUrl({ ...lireUrl(), [c.param]: sel.value === "" && c.defaut !== undefined ? "tout" : sel.value, ...Object.fromEntries((c.exclut || []).map((k) => [k, ""])), page: "" }));
      bar.appendChild(h("label", {}, c.titre || c.param, sel));
    }
  }
  /* rappel des filtres posés, chacun retirable d'un clic */
  const actifs = champs.filter((c) => c.type !== "boutons" && !c.garder && url[c.param] !== undefined && url[c.param] !== "" && url[c.param] !== "tout");
  const puces = actifs.length ? h("div", { class: "dzw-tb-puces" }, actifs.map((c) => {
    const v = url[c.param];
    const opt = (c.options || []).find((x) => String(Array.isArray(x) ? x[0] : x) === String(v));
    const t = opt ? (Array.isArray(opt) ? opt[1] : opt) : (o.libelles && o.libelles[v]) || v;
    return h("span", { class: "dzw-tb-puce" }, h("b", { "data-puce": c.param }, `${c.titre || c.param} : ${c.type === "nombre" && c.unite ? `${v} ${c.unite}` : t}`), h("button", { type: "button", "aria-label": `Retirer ${c.titre || c.param}`, onclick: () => maj(c.param, "") }, "×"));
  }), h("button", { type: "button", class: "raz", onclick: () => ecrireUrl(Object.fromEntries(champs.filter((c) => c.garder || c.type === "boutons").map((c) => [c.param, lireUrl()[c.param]]))) }, "Tout effacer")) : null;
  return h("div", {}, bar, puces);
};

register("tableau", (el) => {
  const o = {
    source: conf(el, "source", ""), vue: conf(el, "vue", "kpi"), titre: conf(el, "titre", ""), mesure: conf(el, "mesure", ""),
    mesures: conf(el, "mesures", null), format: conf(el, "format", ""), libelles: conf(el, "libelles", {}), params: conf(el, "params", ""),
    rafraichir: conf(el, "rafraichir", 0), hauteur: conf(el, "hauteur", 0), lien: conf(el, "lien", ""), colonnes: conf(el, "colonnes", null),
    champs: conf(el, "champs", []), sous: conf(el, "sous", ""), inverse: conf(el, "inverse", false), max: conf(el, "max", 12), ignorer: conf(el, "ignorer", ""),
    libellesSource: conf(el, "libelles-source", ""), libellesCle: conf(el, "libelles-cle", "id"), libellesChamp: conf(el, "libelles-champ", "nom"),
    sur: conf(el, "sur", ""), clic: conf(el, "clic", null), alerte: conf(el, "alerte", true), attention: conf(el, "attention", null), vide: conf(el, "vide", ""),
    tuile: conf(el, "tuile", null), bascule: conf(el, "bascule", null), masquerRefus: conf(el, "masquer-refus", false), lienBarre: conf(el, "lien-barre", ""),
    pourcent: conf(el, "pourcent", false), champHtml: conf(el, "champ-html", ""), champTexte: conf(el, "champ-texte", ""), bouton: conf(el, "bouton", ""),
    entete: conf(el, "entete", ""), entetes: conf(el, "entetes", []), grouper: conf(el, "grouper", ""), selection: conf(el, "selection", null), boutons: conf(el, "boutons", []), sansGroupe: conf(el, "sans-groupe", ""), replie: conf(el, "replie", false), badges: conf(el, "badges", []), cacherZero: conf(el, "cacher-zero", false), montrer: conf(el, "montrer", null),
  };
  /* bascule grille / tableau selon un paramètre de l'adresse : { param, vues: { "": "grille", "t": "liste" } } */
  const vueDe = () => (o.bascule ? o.bascule.vues[lireUrl()[o.bascule.param] ?? ""] || o.vue : o.vue);
  const avecLibelles = async () => { if (o.libellesSource) o.libelles = { ...(await libellesDe(o.libellesSource, o.libellesCle, o.libellesChamp)), ...o.libelles }; };
  el.classList.add("dzw-tb");
  /* niveau d'accès affiché : un bloc réservé à l'administrateur a sa couleur et son étiquette */
  const niveau = conf(el, "niveau", "");
  if (niveau === "admin") el.classList.add("dzw-tb-admin");
  el.innerHTML = "";
  const titre = o.titre ? h("h3", {}, h("span", {}, o.titre, niveau === "admin" ? h("em", { class: "dzw-tb-niveau" }, "Administrateur") : null), h("small", {})) : null;
  if (titre) el.appendChild(titre);
  /* onglets : bloc affiché seulement pour certaines valeurs d'un paramètre ({ param: "t", valeurs: ["envois"], defaut: "sante" }) */
  const visible = () => !o.montrer || [].concat(o.montrer.valeurs || []).map(String).includes(String(lireUrl()[o.montrer.param] ?? o.montrer.defaut ?? ""));
  /* note : un texte et un bouton-lien, sans source (aide d'un onglet, « Ajouter… ») */
  if (o.vue === "note") {
    const montrer = () => { el.hidden = !visible(); };
    montrer();
    window.addEventListener("dz:filtres", montrer);
    el.classList.add("dzw-tb-sansbord");
    const lien = o.lien && /^\/(?!\/)/.test(o.lien) ? o.lien : null;
    /* plusieurs boutons : [["/view/x", "Ajouter"], ["/page/y", "Autre", "sec"]] ; liens internes seulement */
    const boutons = (Array.isArray(o.boutons) ? o.boutons : []).filter((b) => Array.isArray(b) && /^\/(?!\/)/.test(String(b[0])) && b[1])
      .map((b) => h("a", { class: "dzw-tb-bouton-lien" + (b[2] === "sec" ? " sec" : ""), href: b[0] }, String(b[1])));
    if (boutons.length) el.appendChild(h("p", { class: "dzw-tb-boutons" }, ...boutons));
    if (o.sous || (lien && o.bouton)) el.appendChild(h("p", { class: "dzw-tb-note" }, lien && o.bouton ? h("a", { class: "dzw-tb-bouton-lien", href: lien }, o.bouton) : null, o.sous || ""));
    return;
  }
  if (o.vue === "filtres") {
    const montrer = () => { el.hidden = !visible(); };
    montrer();
    window.addEventListener("dz:filtres", montrer);
    /* valeurs par défaut (ex. période 30 jours) posées dans l'adresse avant que les autres blocs lisent */
    const u = lireUrl(), manque = o.champs.filter((c) => c.defaut !== undefined && u[c.param] === undefined && !(c.exclut || []).some((k) => u[k]));
    if (manque.length) { const n = new URL(location.href); for (const c of manque) n.searchParams.set(c.param, c.defaut); history.replaceState(null, "", n); }
    /* la barre suit l'adresse : onglet, liste ou date changés ici ou ailleurs (clic sur un chiffre,
       retour arrière) sont redessinés ; une saisie en cours garde le focus et le curseur */
    let barre = null;
    const dessiner = () => {
      const f = document.activeElement, p = f && barre && barre.contains(f) && f.dataset.param ? { param: f.dataset.param, pos: f.selectionStart } : null;
      const n = vueFiltres(el, o);
      if (barre) barre.replaceWith(n); else el.appendChild(n);
      barre = n;
      if (p) { const i = n.querySelector(`[data-param="${p.param}"]`); if (i) { i.focus(); try { i.setSelectionRange(p.pos, p.pos); } catch (e) { /* champ sans curseur */ } } }
    };
    avecLibelles().then(() => { dessiner(); window.addEventListener("dz:filtres", dessiner); });
    return;
  }
  if (!o.source) { el.appendChild(h("div", { class: "dzw-tb-err" }, "Réglage « source » manquant.")); return; }
  const corps = h("div", {}, h("div", { class: "dzw-tb-sq", style: { height: ["kpi", "titre"].includes(o.vue) ? "44px" : `${o.hauteur || 160}px` } }));
  el.appendChild(corps);
  const ignorer = new Set(String(o.ignorer).split(",").map((s) => s.trim()).filter(Boolean));
  const etat = { page: 0, tri: "", sens: "", n: 0, fermes: new Set(), sel: new Set(), majSel: () => {} };
  /* sélection multiple : barre hors de la liste (elle survit aux actualisations) */
  if (o.selection && o.selection.table) el.insertBefore(barreSelection(o, etat), corps);
  etat.relire = async (defiler) => {
    if (!visible()) { el.hidden = true; etat.dernier = null; return; }
    const n = ++etat.n;
    const url = Object.fromEntries(Object.entries(lireUrl()).filter(([k]) => !ignorer.has(k)));
    /* paramètres fixes, avec {x} remplacé par le paramètre x de l'adresse (ex. "ticket={id}") */
    const fixes = String(o.params || "").replace(/\{(\w+)\}/g, (_, k) => encodeURIComponent(lireUrl()[k] ?? ""));
    const p = { ...url, ...Object.fromEntries(new URLSearchParams(fixes)) };
    if (["liste", "grille"].includes(vueDe())) {
      if (etat.page) p.page = etat.page; else if (url.page) etat.page = +url.page;
      if (etat.tri) { p.tri = etat.tri; p.sens = etat.sens; }
    }
    el.classList.add("charge");
    try {
      const [d] = await Promise.all([charger(o.source, p), avecLibelles()]);
      if (n !== etat.n) return;
      etat.params = p; etat.total = d.total || 0;
      const v = vueDe();
      /* actualisation : rien n'est redessiné si rien n'a changé (pas de clignotement, sélection gardée) */
      const cle = v + "|" + JSON.stringify({ ...d, ms: 0, cache: 0 });
      if (defiler !== "force" && etat.dernier === cle) return;
      etat.dernier = cle;
      el.hidden = false;
      /* repliée : chaque nouvelle agence arrive fermée ; un petit résultat (recherche, filtre) reste ouvert */
      if (o.grouper && o.replie) {
        const ls = d.lignes || [];
        etat.vus = etat.vus || new Set();
        if (ls.length <= 15) for (const l of ls) etat.fermes.delete(String(l[o.grouper] ?? ""));
        else for (const l of ls) { const g = String(l[o.grouper] ?? ""); if (!etat.vus.has(g)) etat.fermes.add(g); }
        for (const l of ls) etat.vus.add(String(l[o.grouper] ?? ""));
      }
      const vue = { kpi: vueKpi, courbe: vueCourbe, barres: vueBarres, anneau: vueAnneau, liste: vueListe, fiche: vueFiche, grille: vueGrille, document: vueDocument, titre: vueTitre }[v] || vueKpi;
      corps.replaceChildren(vue(el, d, o, etat));
      if (titre && d.type === "liste" && ["liste", "grille"].includes(v) && (d.total || 0) !== 1) titre.querySelector("small").textContent = `${NF0.format(d.total || 0)}`;
      if (defiler === true) el.scrollIntoView({ block: "start", behavior: "smooth" });
    } catch (e) {
      if (n !== etat.n) return;
      /* bloc réservé à un rôle supérieur : on le retire au lieu d'afficher une erreur */
      if (o.masquerRefus && /refus/.test(e.message)) { el.hidden = true; return; }
      etat.dernier = null;
      corps.replaceChildren(h("div", { class: "dzw-tb-err" }, `Lecture impossible : ${e.message}`));
    } finally { if (n === etat.n) el.classList.remove("charge"); }
  };
  window.addEventListener("dz:filtres", () => { etat.page = 0; etat.relire("force"); });
  window.addEventListener("dz:rafraichir", () => etat.relire());
  /* actualisation périodique : onglet visible seulement, jamais deux lectures en même temps */
  if (o.rafraichir >= 10) setInterval(() => { if (!document.hidden && !el.classList.contains("charge")) etat.relire(); }, o.rafraichir * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden && o.rafraichir >= 10) etat.relire(); });
  etat.relire();
});
