/* Tableur : cellules, formules (=SOMME(A1:A5), =SI(B2>10;"oui";"non")…),
   copier-coller depuis Excel, import/export CSV, enregistrement dans un champ. */
import { register, css, h, conf, champ, btn, download, toast } from "./_commun.js";

css("tableur", `.dzw-tab .dzw-tab-wrap{overflow:auto;max-height:var(--h,420px)}
.dzw-tab table{min-width:100%;border-collapse:separate;border-spacing:0;font-size:.86rem;font-variant-numeric:tabular-nums}
.dzw-tab th,.dzw-tab td{border-right:1px solid var(--dz-border,#e5e7eb);border-bottom:1px solid var(--dz-border,#e5e7eb);min-width:90px;height:28px;padding:0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:260px}
.dzw-tab th{position:sticky;top:0;background:var(--dz-surface-2,#f3f4f6);font-weight:600;text-align:center;z-index:2;min-width:40px}
.dzw-tab tbody th{position:sticky;left:0;z-index:1}
.dzw-tab td{cursor:cell;background:var(--dz-surface,#fff)}
.dzw-tab td.num{text-align:right}
.dzw-tab td.b{font-weight:700}
.dzw-tab td.err{color:#dc2626}
.dzw-tab td.sel{outline:2px solid var(--dz-primary,#2563eb);outline-offset:-2px}
.dzw-tab td.rg{background:color-mix(in srgb,var(--dz-primary,#2563eb) 10%,transparent)}
.dzw-tab td input{width:100%;border:0;outline:0;font:inherit;background:transparent;padding:0;color:inherit}
.dzw-tab .dzw-tab-fx{display:flex;gap:6px;align-items:center;flex:1;min-width:220px}
.dzw-tab .dzw-tab-fx b{min-width:44px;text-align:center;font-size:.8rem;opacity:.7}
.dzw-tab .dzw-tab-fx input{flex:1}`);

const colName = (i) => { let s = ""; i++; while (i) { const m = (i - 1) % 26; s = String.fromCharCode(65 + m) + s; i = Math.floor((i - 1) / 26); } return s; };
const colIdx = (s) => [...s].reduce((a, c) => a * 26 + c.charCodeAt(0) - 64, 0) - 1;
const parseRef = (r) => { const m = /^\$?([A-Z]+)\$?(\d+)$/.exec(r); return m ? { c: colIdx(m[1]), r: +m[2] - 1 } : null; };

/* ---------- formules : analyse sans eval ---------- */
const FN = {
  SOMME: (a) => a.flat(9).filter((x) => typeof x === "number").reduce((s, x) => s + x, 0),
  MOYENNE: (a) => { const n = a.flat(9).filter((x) => typeof x === "number"); return n.length ? FN.SOMME(n) / n.length : 0; },
  MIN: (a) => Math.min(...a.flat(9).filter((x) => typeof x === "number")),
  MAX: (a) => Math.max(...a.flat(9).filter((x) => typeof x === "number")),
  NB: (a) => a.flat(9).filter((x) => typeof x === "number").length,
  NBVAL: (a) => a.flat(9).filter((x) => x !== "" && x !== null).length,
  SI: (a) => (a[0] ? a[1] : a[2] ?? ""),
  ARRONDI: (a) => { const p = 10 ** (a[1] || 0); return Math.round(a[0] * p) / p; },
  ABS: (a) => Math.abs(a[0]), RACINE: (a) => Math.sqrt(a[0]), PUISSANCE: (a) => a[0] ** a[1],
  ET: (a) => a.flat(9).every(Boolean), OU: (a) => a.flat(9).some(Boolean), NON: (a) => !a[0],
  CONCAT: (a) => a.flat(9).join(""), MAJUSCULE: (a) => String(a[0]).toUpperCase(), MINUSCULE: (a) => String(a[0]).toLowerCase(), NBCAR: (a) => String(a[0]).length,
  AUJOURDHUI: () => new Date().toISOString().slice(0, 10), MAINTENANT: () => new Date().toLocaleString("fr-FR"),
  "SOMME.SI": (a) => { const [plage, crit, somme] = a; const f = critere(crit); return plage.flat(9).reduce((s, v, i) => (f(v) ? s + (+((somme || plage).flat(9)[i]) || 0) : s), 0); },
  "NB.SI": (a) => { const f = critere(a[1]); return a[0].flat(9).filter(f).length; },
  RECHERCHEV: (a) => { const [v, plage, col] = a; const row = plage.find((r) => r[0] == v); return row ? row[col - 1] : "#N/A"; },
};
Object.assign(FN, { SUM: FN.SOMME, AVERAGE: FN.MOYENNE, COUNT: FN.NB, COUNTA: FN.NBVAL, IF: FN.SI, ROUND: FN.ARRONDI, AND: FN.ET, OR: FN.OU, NOT: FN.NON, TODAY: FN.AUJOURDHUI, SUMIF: FN["SOMME.SI"], COUNTIF: FN["NB.SI"], VLOOKUP: FN.RECHERCHEV });
const critere = (c) => { const m = /^(<=|>=|<>|<|>|=)?(.*)$/.exec(String(c)); const op = m[1] || "=", v = isNaN(+m[2]) || m[2] === "" ? m[2] : +m[2]; return (x) => ({ "=": x == v, "<>": x != v, "<": x < v, ">": x > v, "<=": x <= v, ">=": x >= v })[op]; };

const tokens = (s) => {
  const out = []; let i = 0;
  const re = /\s*(?:(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)|("(?:[^"]|"")*")|(\$?[A-Z]+\$?\d+(?::\$?[A-Z]+\$?\d+)?)|([A-Z][A-Z0-9.]*)\s*\(|(<=|>=|<>|[-+*/^&=<>(),;%]))/iy;
  while (i < s.length) {
    re.lastIndex = i; const m = re.exec(s);
    if (!m) { if (/\s/.test(s[i])) { i++; continue; } throw new Error("formule invalide"); }
    i = re.lastIndex;
    if (m[1]) out.push({ t: "n", v: +m[1].replace(",", ".") }); else if (m[2]) out.push({ t: "s", v: m[2].slice(1, -1).replace(/""/g, '"') });
    else if (m[3]) out.push({ t: "ref", v: m[3].toUpperCase() }); else if (m[4]) out.push({ t: "fn", v: m[4].toUpperCase() }); else out.push({ t: "op", v: m[5] === ";" ? "," : m[5] });
  }
  return out;
};
const evalFormula = (src, get) => {
  const tk = tokens(src); let p = 0;
  const peek = () => tk[p], eat = (v) => { if (tk[p] && tk[p].v === v) { p++; return true; } return false; };
  const num = (x) => { if (typeof x === "number") return x; if (x === "" || x === null || x === undefined) return 0; if (typeof x === "boolean") return +x; const n = +String(x).replace(",", "."); if (isNaN(n)) throw new Error("#VALEUR"); return n; };
  const range = (r) => { const [a, b] = r.split(":").map(parseRef); const rows = []; for (let y = Math.min(a.r, b.r); y <= Math.max(a.r, b.r); y++) { const row = []; for (let x = Math.min(a.c, b.c); x <= Math.max(a.c, b.c); x++) row.push(get(x, y)); rows.push(row); } return rows; };
  const prim = () => {
    const t = tk[p++]; if (!t) throw new Error("formule incomplète");
    if (t.t === "n" || t.t === "s") return t.v;
    if (t.t === "ref") { if (t.v.includes(":")) return range(t.v); const r = parseRef(t.v); return get(r.c, r.r); }
    if (t.t === "fn") { const f = FN[t.v]; if (!f) throw new Error("#NOM? " + t.v); const args = []; if (!eat(")")) { do args.push(cmp()); while (eat(",")); if (!eat(")")) throw new Error("parenthèse manquante"); } return f(args); }
    if (t.v === "(") { const v = cmp(); if (!eat(")")) throw new Error("parenthèse manquante"); return v; }
    if (t.v === "-") return -num(unary()); if (t.v === "+") return num(unary());
    throw new Error("formule invalide");
  };
  const unary = () => { const v = prim(); if (eat("%")) return num(v) / 100; return v; };
  const pow = () => { let v = unary(); while (eat("^")) v = num(v) ** num(unary()); return v; };
  const mul = () => { let v = pow(); for (;;) { if (eat("*")) v = num(v) * num(pow()); else if (eat("/")) { const d = num(pow()); if (!d) throw new Error("#DIV/0!"); v = num(v) / d; } else return v; } };
  const add = () => { let v = mul(); for (;;) { if (eat("+")) v = num(v) + num(mul()); else if (eat("-")) v = num(v) - num(mul()); else return v; } };
  const cat = () => { let v = add(); while (eat("&")) v = String(v ?? "") + String(add() ?? ""); return v; };
  const cmp = () => { let v = cat(); const t = peek(); if (t && t.t === "op" && ["=", "<>", "<", ">", "<=", ">="].includes(t.v)) { p++; const w = cat(); return { "=": v == w, "<>": v != w, "<": v < w, ">": v > w, "<=": v <= w, ">=": v >= w }[t.v]; } return v; };
  const v = cmp(); if (p < tk.length) throw new Error("formule invalide");
  return v;
};

register("tableur", (el) => {
  const c = champ(el);
  const lecture = conf(el, "lecture", false);
  let data = { lignes: conf(el, "lignes", 20), colonnes: conf(el, "colonnes", 8), cellules: {}, gras: {} };
  try { const v = c.get() || el.getAttribute("data-valeur"); if (v) data = { ...data, ...JSON.parse(v) }; } catch (e) { /* vide */ }
  el.classList.add("dzw", "dzw-tab");
  el.style.setProperty("--h", conf(el, "hauteur", 420) + "px");
  el.innerHTML = "";
  const fxRef = h("b", {}, "A1"), fx = h("input", { type: "text", placeholder: "Valeur ou formule (=SOMME(A1:A5))" });
  const wrap = h("div", { class: "dzw-tab-wrap" });
  let cur = { c: 0, r: 0 }, anchor = null, editing = null, cache = {};
  const key = (x, y) => colName(x) + (y + 1);
  const raw = (x, y) => data.cellules[key(x, y)] ?? "";
  const value = (x, y, stack = new Set()) => {
    const k = key(x, y);
    if (k in cache) return cache[k];
    const s = raw(x, y);
    let v;
    if (typeof s === "string" && s.startsWith("=")) {
      if (stack.has(k)) return "#CIRC!";
      stack.add(k);
      try { v = evalFormula(s.slice(1), (cx, cy) => { const r = value(cx, cy, stack); if (typeof r === "string" && r.startsWith("#")) throw new Error(r); return r; }); } catch (e) { v = e.message.startsWith("#") ? e.message.split(" ")[0] : "#ERREUR"; }
      stack.delete(k);
    } else v = s !== "" && !isNaN(+String(s).replace(",", ".")) && /^-?[\d\s]*[.,]?\d+$/.test(String(s).trim()) ? +String(s).replace(",", ".").replace(/\s/g, "") : s;
    cache[k] = v; return v;
  };
  const fmt = (v) => (typeof v === "number" ? (Number.isInteger(v) ? v.toLocaleString("fr-FR") : v.toLocaleString("fr-FR", { maximumFractionDigits: 6 })) : typeof v === "boolean" ? (v ? "VRAI" : "FAUX") : String(v ?? ""));
  let saveT = null;
  const save = () => { clearTimeout(saveT); saveT = setTimeout(() => c.set(JSON.stringify(data)), 300); };
  const table = h("table");
  const render = () => {
    cache = {};
    const head = h("tr", {}, h("th", {}), ...[...Array(data.colonnes)].map((_, x) => h("th", {}, colName(x))));
    const body = [...Array(data.lignes)].map((_, y) => h("tr", {}, h("th", {}, y + 1), ...[...Array(data.colonnes)].map((_, x) => {
      const v = value(x, y);
      const td = h("td", { "data-x": x, "data-y": y, class: [typeof v === "number" ? "num" : "", typeof v === "string" && v.startsWith("#") && raw(x, y).startsWith?.("=") ? "err" : "", data.gras[key(x, y)] ? "b" : ""].join(" ") }, fmt(v));
      return td;
    })));
    table.innerHTML = ""; table.append(h("thead", {}, head), h("tbody", {}, ...body));
    select(cur.c, cur.r, anchor);
  };
  const cell = (x, y) => table.querySelector(`td[data-x="${x}"][data-y="${y}"]`);
  const select = (x, y, anc = null) => {
    cur = { c: Math.max(0, Math.min(data.colonnes - 1, x)), r: Math.max(0, Math.min(data.lignes - 1, y)) }; anchor = anc;
    table.querySelectorAll("td.sel,td.rg").forEach((t) => t.classList.remove("sel", "rg"));
    if (anchor) for (let yy = Math.min(anchor.r, cur.r); yy <= Math.max(anchor.r, cur.r); yy++) for (let xx = Math.min(anchor.c, cur.c); xx <= Math.max(anchor.c, cur.c); xx++) cell(xx, yy)?.classList.add("rg");
    const td = cell(cur.c, cur.r); if (td) { td.classList.add("sel"); td.scrollIntoView({ block: "nearest", inline: "nearest" }); }
    fxRef.textContent = key(cur.c, cur.r); fx.value = raw(cur.c, cur.r);
  };
  const setCell = (x, y, v) => { const k = key(x, y); if (v === "" || v === null || v === undefined) delete data.cellules[k]; else data.cellules[k] = String(v); };
  const commit = (v) => { if (lecture) return; setCell(cur.c, cur.r, v); save(); render(); };
  const edit = (initial) => {
    if (lecture) return;
    const td = cell(cur.c, cur.r); if (!td) return;
    const inp = h("input", { type: "text", value: initial !== undefined ? initial : raw(cur.c, cur.r) });
    editing = inp; td.textContent = ""; td.append(inp); inp.focus(); inp.setSelectionRange(inp.value.length, inp.value.length);
    inp.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === "Tab") { e.preventDefault(); e.stopPropagation(); editing = null; commit(inp.value); select(cur.c + (e.key === "Tab" ? (e.shiftKey ? -1 : 1) : 0), cur.r + (e.key === "Enter" ? (e.shiftKey ? -1 : 1) : 0)); wrap.focus(); }
      else if (e.key === "Escape") { editing = null; render(); wrap.focus(); }
    });
    inp.addEventListener("blur", () => { if (editing === inp) { editing = null; commit(inp.value); } });
  };
  wrap.tabIndex = 0;
  table.addEventListener("mousedown", (e) => { const td = e.target.closest("td"); if (!td || editing) return; const x = +td.dataset.x, y = +td.dataset.y; if (e.shiftKey) select(x, y, anchor || { ...cur }); else select(x, y); wrap.focus(); });
  table.addEventListener("dblclick", (e) => { if (e.target.closest("td")) edit(); });
  wrap.addEventListener("keydown", (e) => {
    if (editing) return;
    const mv = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0], Tab: [e.shiftKey ? -1 : 1, 0], Enter: [0, 1] }[e.key];
    if (mv) { e.preventDefault(); select(cur.c + mv[0], cur.r + mv[1], e.shiftKey && e.key.startsWith("Arrow") ? anchor || { ...cur } : null); return; }
    if (e.key === "F2") { e.preventDefault(); edit(); return; }
    if (e.key === "Delete" || e.key === "Backspace") { e.preventDefault(); forRange((x, y) => setCell(x, y, "")); save(); render(); return; }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); gras(); return; }
    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); edit(e.key); }
  });
  const forRange = (f) => { const a = anchor || cur; for (let y = Math.min(a.r, cur.r); y <= Math.max(a.r, cur.r); y++) for (let x = Math.min(a.c, cur.c); x <= Math.max(a.c, cur.c); x++) f(x, y); };
  /* copier / coller compatibles Excel et Google Sheets (tabulations) */
  wrap.addEventListener("copy", (e) => { if (editing) return; const a = anchor || cur; const rows = []; for (let y = Math.min(a.r, cur.r); y <= Math.max(a.r, cur.r); y++) { const r = []; for (let x = Math.min(a.c, cur.c); x <= Math.max(a.c, cur.c); x++) r.push(fmt(value(x, y))); rows.push(r.join("\t")); } e.clipboardData.setData("text/plain", rows.join("\n")); e.preventDefault(); });
  wrap.addEventListener("paste", (e) => {
    if (editing || lecture) return; e.preventDefault();
    const rows = e.clipboardData.getData("text/plain").replace(/\r/g, "").replace(/\n$/, "").split("\n").map((l) => l.split("\t"));
    data.lignes = Math.max(data.lignes, cur.r + rows.length); data.colonnes = Math.max(data.colonnes, cur.c + Math.max(...rows.map((r) => r.length)));
    rows.forEach((r, y) => r.forEach((v, x) => setCell(cur.c + x, cur.r + y, v.trim())));
    save(); render();
  });
  fx.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); commit(fx.value); select(cur.c, cur.r + 1); wrap.focus(); } });
  const gras = () => { forRange((x, y) => { const k = key(x, y); if (data.gras[k]) delete data.gras[k]; else data.gras[k] = 1; }); save(); render(); };
  const csv = () => { const rows = []; let maxY = 0, maxX = 0; for (const k of Object.keys(data.cellules)) { const r = parseRef(k); maxY = Math.max(maxY, r.r); maxX = Math.max(maxX, r.c); } for (let y = 0; y <= maxY; y++) { const r = []; for (let x = 0; x <= maxX; x++) { const v = value(x, y); const s = typeof v === "number" ? String(v).replace(".", ",") : String(v ?? ""); r.push(/[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s); } rows.push(r.join(";")); } download("﻿" + rows.join("\r\n"), "tableur.csv", "text/csv"); };
  const fileIn = h("input", { type: "file", accept: ".csv,.txt", style: { display: "none" }, onchange: async (e) => {
    const f = e.target.files[0]; if (!f) return; const t = await f.text(); const sep = (t.match(/;/g) || []).length > (t.match(/,/g) || []).length ? ";" : ",";
    const rows = t.replace(/^﻿/, "").split(/\r?\n/).filter(Boolean).map((l) => { const out = []; let cur2 = "", q = false; for (let i = 0; i < l.length; i++) { const ch = l[i]; if (q) { if (ch === '"' && l[i + 1] === '"') { cur2 += '"'; i++; } else if (ch === '"') q = false; else cur2 += ch; } else if (ch === '"') q = true; else if (ch === sep) { out.push(cur2); cur2 = ""; } else cur2 += ch; } out.push(cur2); return out; });
    data.cellules = {}; data.lignes = Math.max(20, rows.length + 5); data.colonnes = Math.max(8, ...rows.map((r) => r.length));
    rows.forEach((r, y) => r.forEach((v, x) => setCell(x, y, v))); save(); render(); e.target.value = ""; toast(`${rows.length} ligne(s) importée(s)`, "success");
  } });
  const bar = h("div", { class: "dzw-bar" }, h("div", { class: "dzw-tab-fx" }, fxRef, fx));
  if (!lecture) bar.append(btn("fas fa-bold", "Gras", gras), btn("fas fa-plus", "Ligne", () => { data.lignes++; save(); render(); }), btn("fas fa-columns", "Colonne", () => { data.colonnes++; save(); render(); }), fileIn, btn("fas fa-file-import", "Importer CSV", () => fileIn.click()));
  else fx.readOnly = true;
  bar.append(btn("fas fa-file-csv", "Exporter CSV", csv));
  wrap.append(table);
  el.append(bar, wrap);
  render();
});
export { evalFormula };
