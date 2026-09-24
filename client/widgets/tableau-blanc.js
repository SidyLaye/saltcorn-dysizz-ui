/* Tableau blanc : crayon, surligneur, formes, flèches, texte, post-it, gomme,
   déplacer, zoom, annuler/refaire, export PNG, enregistrement dans un champ. */
import { register, css, h, conf, champ, btn, download } from "./_commun.js";

css("tableau-blanc", `.dzw-tb .dzw-tb-can{position:relative;background:#fff;background-image:radial-gradient(#e2e8f0 1px,transparent 1px);background-size:20px 20px}
.dzw-tb canvas{display:block;width:100%;touch-action:none}
.dzw-tb .dzw-tb-sw{display:flex;gap:4px}
.dzw-tb .dzw-tb-sw button{width:22px;height:22px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #cbd5e1;cursor:pointer;padding:0}
.dzw-tb .dzw-tb-sw button.on{box-shadow:0 0 0 2px var(--dz-primary,#2563eb)}
.dzw-tb textarea.dzw-tb-txt{position:absolute;border:1px dashed var(--dz-primary,#2563eb);background:rgba(255,255,255,.9);font:16px system-ui,sans-serif;resize:none;outline:0;padding:2px;min-width:120px;z-index:2}`);

const COULEURS = ["#111827", "#ef4444", "#f59e0b", "#16a34a", "#2563eb", "#8b5cf6", "#ec4899"];
const POSTIT = ["#fef08a", "#bbf7d0", "#bfdbfe", "#fbcfe8", "#fed7aa"];

register("tableau-blanc", (el) => {
  const c = champ(el);
  const H = conf(el, "hauteur", 480);
  el.classList.add("dzw", "dzw-tb");
  el.innerHTML = "";
  let objs = [];
  try { const v = c.get(); if (v) objs = JSON.parse(v).objets || []; } catch (e) { /* vide */ }
  const cam = { x: 0, y: 0, z: 1 };
  let tool = "crayon", couleur = COULEURS[0], epaisseur = 3, courant = null, sel = null, drag = null;
  const hist = [JSON.stringify(objs)]; let hi = 0;
  const cv = h("canvas", { height: H });
  const zone = h("div", { class: "dzw-tb-can" }, cv);
  const g = cv.getContext("2d");
  const fit = () => { const r = window.devicePixelRatio || 1; cv.width = cv.clientWidth * r; cv.height = H * r; cv.style.height = H + "px"; draw(); };
  const toWorld = (e) => { const b = cv.getBoundingClientRect(); return { x: (e.clientX - b.left) / cam.z + cam.x, y: (e.clientY - b.top) / cam.z + cam.y }; };
  let saveT = null;
  const commit = () => { hist.splice(hi + 1); hist.push(JSON.stringify(objs)); hi = hist.length - 1; if (hist.length > 80) { hist.shift(); hi--; } clearTimeout(saveT); saveT = setTimeout(() => c.set(JSON.stringify({ v: 1, objets: objs })), 300); };
  const undo = (d) => { const i = hi + d; if (i < 0 || i >= hist.length) return; hi = i; objs = JSON.parse(hist[i]); sel = null; c.set(JSON.stringify({ v: 1, objets: objs })); draw(); };
  const bbox = (o) => {
    if (o.t === "trait") { const xs = o.p.map((p) => p[0]), ys = o.p.map((p) => p[1]); return { x: Math.min(...xs), y: Math.min(...ys), w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys) }; }
    if (o.t === "texte") { g.font = `${o.taille || 18}px system-ui,sans-serif`; const lines = o.txt.split("\n"); return { x: o.x, y: o.y, w: Math.max(...lines.map((l) => g.measureText(l).width)), h: lines.length * (o.taille || 18) * 1.3 }; }
    return { x: Math.min(o.x, o.x + o.w), y: Math.min(o.y, o.y + o.h), w: Math.abs(o.w), h: Math.abs(o.h) };
  };
  const wrapText = (t, maxW) => { const out = []; for (const para of t.split("\n")) { let l = ""; for (const w of para.split(" ")) { if (g.measureText(l + w).width > maxW && l) { out.push(l.trim()); l = ""; } l += w + " "; } out.push(l.trim()); } return out; };
  const paint = (o) => {
    g.save(); g.strokeStyle = g.fillStyle = o.c; g.lineWidth = o.e || 3; g.lineCap = g.lineJoin = "round";
    if (o.t === "trait") { g.globalAlpha = o.surligneur ? 0.35 : 1; if (o.surligneur) g.lineWidth = (o.e || 3) * 5; g.beginPath(); o.p.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y))); g.stroke(); }
    else if (o.t === "rect") g.strokeRect(o.x, o.y, o.w, o.h);
    else if (o.t === "ellipse") { g.beginPath(); g.ellipse(o.x + o.w / 2, o.y + o.h / 2, Math.abs(o.w / 2), Math.abs(o.h / 2), 0, 0, Math.PI * 2); g.stroke(); }
    else if (o.t === "fleche") { const x2 = o.x + o.w, y2 = o.y + o.h, a = Math.atan2(o.h, o.w), L = 10 + (o.e || 3) * 2; g.beginPath(); g.moveTo(o.x, o.y); g.lineTo(x2, y2); g.stroke(); g.beginPath(); g.moveTo(x2, y2); g.lineTo(x2 - L * Math.cos(a - 0.45), y2 - L * Math.sin(a - 0.45)); g.lineTo(x2 - L * Math.cos(a + 0.45), y2 - L * Math.sin(a + 0.45)); g.closePath(); g.fill(); }
    else if (o.t === "postit") { g.shadowColor = "rgba(0,0,0,.15)"; g.shadowBlur = 8; g.shadowOffsetY = 3; g.fillStyle = o.fond; g.fillRect(o.x, o.y, o.w, o.h); g.shadowColor = "transparent"; g.fillStyle = "#1f2937"; g.font = "15px system-ui,sans-serif"; g.textBaseline = "top"; wrapText(o.txt || "", o.w - 16).forEach((l, i) => g.fillText(l, o.x + 8, o.y + 8 + i * 20)); }
    else if (o.t === "texte") { g.font = `${o.taille || 18}px system-ui,sans-serif`; g.textBaseline = "top"; o.txt.split("\n").forEach((l, i) => g.fillText(l, o.x, o.y + i * (o.taille || 18) * 1.3)); }
    g.restore();
  };
  function draw() {
    const r = window.devicePixelRatio || 1;
    g.setTransform(r, 0, 0, r, 0, 0); g.clearRect(0, 0, cv.width, cv.height);
    g.setTransform(r * cam.z, 0, 0, r * cam.z, -cam.x * cam.z * r, -cam.y * cam.z * r);
    objs.forEach(paint); if (courant) paint(courant);
    if (sel) { const b = bbox(sel); g.save(); g.strokeStyle = "#2563eb"; g.setLineDash([5, 4]); g.lineWidth = 1 / cam.z; g.strokeRect(b.x - 6, b.y - 6, b.w + 12, b.h + 12); g.restore(); }
  }
  const hit = (p) => { for (let i = objs.length - 1; i >= 0; i--) { const b = bbox(objs[i]); const m = 8 / cam.z; if (p.x >= b.x - m && p.x <= b.x + b.w + m && p.y >= b.y - m && p.y <= b.y + b.h + m) return objs[i]; } return null; };
  const move = (o, dx, dy) => { if (o.t === "trait") o.p = o.p.map(([x, y]) => [x + dx, y + dy]); else { o.x += dx; o.y += dy; } };
  const editText = (o) => {
    const ta = h("textarea", { class: "dzw-tb-txt", rows: 3, style: { left: (o.x - cam.x) * cam.z + "px", top: (o.y - cam.y) * cam.z + "px", width: (o.w ? o.w * cam.z : 220) + "px", background: o.fond || "rgba(255,255,255,.9)" } });
    ta.value = o.txt || ""; zone.append(ta); ta.focus();
    const done = () => { o.txt = ta.value; ta.remove(); if (!o.txt.trim() && o.t === "texte") objs = objs.filter((x) => x !== o); commit(); draw(); };
    ta.addEventListener("blur", done); ta.addEventListener("keydown", (e) => { if (e.key === "Escape" || (e.key === "Enter" && (e.ctrlKey || e.metaKey))) ta.blur(); });
  };
  let pointers = new Map(), pinch = null;
  cv.addEventListener("pointerdown", (e) => {
    cv.setPointerCapture(e.pointerId); pointers.set(e.pointerId, e);
    if (pointers.size === 2) { const [a, b] = [...pointers.values()]; pinch = { d: Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY), z: cam.z }; courant = null; return; }
    const p = toWorld(e);
    if (tool === "main" || e.button === 1) { drag = { pan: true, sx: e.clientX, sy: e.clientY, cx: cam.x, cy: cam.y }; return; }
    if (tool === "choisir") { sel = hit(p); drag = sel ? { o: sel, last: p } : { pan: true, sx: e.clientX, sy: e.clientY, cx: cam.x, cy: cam.y }; draw(); return; }
    if (tool === "gomme") { const o = hit(p); if (o) { objs = objs.filter((x) => x !== o); commit(); draw(); } drag = { gomme: true }; return; }
    if (tool === "texte") { const o = { t: "texte", x: p.x, y: p.y, c: couleur, taille: 14 + epaisseur * 2, txt: "" }; objs.push(o); editText(o); return; }
    if (tool === "postit") { const o = { t: "postit", x: p.x, y: p.y, w: 170, h: 150, fond: POSTIT[objs.filter((x) => x.t === "postit").length % POSTIT.length], c: "#1f2937", txt: "" }; objs.push(o); draw(); editText(o); return; }
    if (tool === "crayon" || tool === "surligneur") courant = { t: "trait", p: [[p.x, p.y]], c: couleur, e: epaisseur, surligneur: tool === "surligneur" };
    else courant = { t: tool, x: p.x, y: p.y, w: 0, h: 0, c: couleur, e: epaisseur };
  });
  cv.addEventListener("pointermove", (e) => {
    if (pointers.has(e.pointerId)) pointers.set(e.pointerId, e);
    if (pinch && pointers.size === 2) { const [a, b] = [...pointers.values()]; const d = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY); cam.z = Math.max(0.2, Math.min(4, pinch.z * d / pinch.d)); draw(); return; }
    const p = toWorld(e);
    if (drag && drag.pan) { cam.x = drag.cx - (e.clientX - drag.sx) / cam.z; cam.y = drag.cy - (e.clientY - drag.sy) / cam.z; draw(); return; }
    if (drag && drag.o) { move(drag.o, p.x - drag.last.x, p.y - drag.last.y); drag.last = p; drag.moved = true; draw(); return; }
    if (drag && drag.gomme && e.buttons) { const o = hit(p); if (o) { objs = objs.filter((x) => x !== o); draw(); drag.changed = true; } return; }
    if (!courant) return;
    if (courant.t === "trait") courant.p.push([p.x, p.y]); else { courant.w = p.x - courant.x; courant.h = p.y - courant.y; }
    draw();
  });
  const up = (e) => {
    pointers.delete(e.pointerId); if (pointers.size < 2) pinch = null;
    if (drag) { if (drag.moved || drag.changed) commit(); drag = null; return; }
    if (courant) { if (courant.t !== "trait" || courant.p.length > 1) { if (courant.t === "trait") courant.p = courant.p.filter((_, i, a) => i % 2 === 0 || i === a.length - 1); objs.push(courant); commit(); } courant = null; draw(); }
  };
  cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
  cv.addEventListener("dblclick", (e) => { const o = hit(toWorld(e)); if (o && (o.t === "postit" || o.t === "texte")) editText(o); });
  cv.addEventListener("wheel", (e) => { if (!e.ctrlKey && !e.metaKey && !conf(el, "molette", true)) return; e.preventDefault(); const p = toWorld(e); const z = Math.max(0.2, Math.min(4, cam.z * (e.deltaY < 0 ? 1.1 : 0.9))); cam.x = p.x - (p.x - cam.x) * (cam.z / z); cam.y = p.y - (p.y - cam.y) * (cam.z / z); cam.z = z; draw(); }, { passive: false });
  el.tabIndex = 0;
  el.addEventListener("keydown", (e) => {
    if (e.target.tagName === "TEXTAREA") return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); undo(e.shiftKey ? 1 : -1); }
    else if ((e.key === "Delete" || e.key === "Backspace") && sel) { objs = objs.filter((x) => x !== sel); sel = null; commit(); draw(); }
  });
  const tools = {}; const setTool = (t) => { tool = t; sel = t === "choisir" ? sel : null; Object.entries(tools).forEach(([k, b]) => b.classList.toggle("on", k === t)); cv.style.cursor = { main: "grab", choisir: "default", texte: "text" }[t] || "crosshair"; draw(); };
  [["choisir", "fas fa-mouse-pointer", "Choisir / déplacer"], ["main", "fas fa-hand-paper", "Se déplacer"], ["crayon", "fas fa-pen", "Crayon"], ["surligneur", "fas fa-highlighter", "Surligneur"], ["rect", "far fa-square", "Rectangle"], ["ellipse", "far fa-circle", "Ellipse"], ["fleche", "fas fa-long-arrow-alt-right", "Flèche"], ["texte", "fas fa-font", "Texte"], ["postit", "fas fa-sticky-note", "Post-it"], ["gomme", "fas fa-eraser", "Gomme"]].forEach(([k, i, l]) => (tools[k] = btn(i, l, () => setTool(k))));
  const sw = h("div", { class: "dzw-tb-sw" }, ...COULEURS.map((col, i) => { const b = h("button", { type: "button", title: col, style: { background: col }, class: i ? "" : "on", onclick: () => { couleur = col; sw.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b)); if (sel && sel.t !== "postit") { sel.c = col; commit(); draw(); } } }); return b; }));
  const ep = h("select", { title: "Épaisseur", onchange: (e) => (epaisseur = +e.target.value) }, ...[[2, "fin"], [3, "moyen"], [6, "épais"], [10, "très épais"]].map(([v, l]) => h("option", { value: v, ...(v === 3 ? { selected: true } : {}) }, l)));
  el.append(h("div", { class: "dzw-bar" }, ...Object.values(tools), sw, ep, h("span", { class: "dzw-sp" }), btn("fas fa-undo", "Annuler", () => undo(-1)), btn("fas fa-redo", "Refaire", () => undo(1)), btn("fas fa-search-plus", "Zoom +", () => { cam.z = Math.min(4, cam.z * 1.2); draw(); }), btn("fas fa-search-minus", "Zoom −", () => { cam.z = Math.max(0.2, cam.z / 1.2); draw(); }), btn("fas fa-image", "PNG", () => exportPng()), btn("fas fa-trash", "Tout effacer", () => { if (confirmClear()) { objs = []; sel = null; commit(); draw(); } })), zone);
  const confirmClear = () => objs.length === 0 || window.confirm("Effacer tout le tableau ?");
  const exportPng = () => {
    if (!objs.length) return;
    const bs = objs.map(bbox); const x1 = Math.min(...bs.map((b) => b.x)), y1 = Math.min(...bs.map((b) => b.y)), x2 = Math.max(...bs.map((b) => b.x + b.w)), y2 = Math.max(...bs.map((b) => b.y + b.h));
    const m = 30, s = 2, W = cv.width, HH = cv.height, sc = { ...cam };
    cv.width = (x2 - x1 + 2 * m) * s; cv.height = (y2 - y1 + 2 * m) * s;
    g.setTransform(s, 0, 0, s, (-x1 + m) * s, (-y1 + m) * s); g.fillStyle = "#fff"; g.fillRect(x1 - m, y1 - m, x2 - x1 + 2 * m, y2 - y1 + 2 * m); const keep = sel; sel = null; objs.forEach(paint);
    cv.toBlob((bl) => { download(bl, "tableau.png", "image/png"); cv.width = W; cv.height = HH; Object.assign(cam, sc); sel = keep; draw(); });
  };
  setTool("crayon");
  new ResizeObserver(fit).observe(cv);
  fit();
});
