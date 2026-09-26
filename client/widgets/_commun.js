/* Outils communs aux widgets (inclus dans chaque widget au build). */
export const register = (name, fn) => { window.DZW = window.DZW || {}; window.DZW[name] = fn; };

export const css = (id, text) => {
  if (document.getElementById("dzw-css-" + id)) return;
  const s = document.createElement("style");
  s.id = "dzw-css-" + id;
  s.textContent = text;
  document.head.appendChild(s);
};

/* h("button", {class:"x", onclick}, "texte", enfant…) */
export const h = (tag, attrs, ...kids) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null || v === false) continue;
    if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
    /* les variables CSS (--x) ne s'écrivent qu'avec setProperty */
    else if (k === "style" && typeof v === "object") for (const [sk, sv] of Object.entries(v)) { if (sk.startsWith("--")) e.style.setProperty(sk, sv); else e.style[sk] = sv; }
    else if (k === "html") e.innerHTML = v;
    else e.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat()) if (k !== undefined && k !== null && k !== false) e.append(k.nodeType ? k : document.createTextNode(String(k)));
  return e;
};
export const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/* réglage lu dans data-<nom> (JSON si possible) */
export const conf = (el, name, def) => {
  const v = el.getAttribute("data-" + name);
  if (v === null || v === "") return def;
  if (typeof def === "number") return isNaN(+v) ? def : +v;
  if (typeof def === "boolean") return v !== "false" && v !== "0" && v !== "non";
  if (typeof def === "object") { try { return JSON.parse(v); } catch (e) { return def; } }
  return v;
};

/* champ de formulaire relié (data-champ="nom") : lit / écrit sa valeur */
export const champ = (el) => {
  const name = el.getAttribute("data-champ");
  let input = null;
  if (name) {
    const form = el.closest("form");
    input = (form && form.querySelector(`[name="${CSS.escape(name)}"]`)) || document.querySelector(`[name="${CSS.escape(name)}"]`);
  }
  if (!input) input = el.querySelector("input[type=hidden],textarea.dzw-val");
  return {
    input,
    get: () => (input ? input.value : el.getAttribute("data-valeur") || ""),
    set: (v) => { if (!input) return; input.value = v; input.dispatchEvent(new Event("input", { bubbles: true })); input.dispatchEvent(new Event("change", { bubbles: true })); },
  };
};

export const csrf = () => window._sc_globalCsrf || (document.querySelector('input[name="_csrf"]') || {}).value || "";

/* lignes d'une table Saltcorn (API REST, avec la session de l'utilisateur) */
export const tableRows = async (table, where) => {
  const q = where && Object.keys(where).length ? "?" + new URLSearchParams(where).toString() : "";
  const r = await fetch(`/api/${encodeURIComponent(table)}/${q}`, { credentials: "same-origin", headers: { Accept: "application/json" } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.error) throw new Error(j.error || `HTTP ${r.status}`);
  return j.success || [];
};
export const tableSave = async (table, row, id) => {
  const r = await fetch(`/api/${encodeURIComponent(table)}/${id ? encodeURIComponent(id) : ""}`, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "CSRF-Token": csrf() }, body: JSON.stringify(row) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.error) throw new Error(j.error || `HTTP ${r.status}`);
  return j.success;
};

export const download = (data, name, type = "application/octet-stream") => {
  const blob = data instanceof Blob ? data : new Blob([data], { type });
  const a = h("a", { href: URL.createObjectURL(blob), download: name });
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
};

export const toast = (msg, kind) => { if (window.DZ && window.DZ.toast) window.DZ.toast(msg, kind); };

/* base visuelle partagée : barre d'outils, boutons, cadre */
css("base", `
.dzw{position:relative;border:1px solid var(--dz-border,#e5e7eb);border-radius:var(--dz-radius,12px);background:var(--dz-surface,#fff);overflow:hidden;color:var(--dz-text,#111827);font:inherit}
.dzw-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:8px;border-bottom:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface-2,#f9fafb)}
.dzw-bar .dzw-sp{flex:1}
.dzw-b{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);color:inherit;border-radius:8px;padding:6px 10px;font-size:.85rem;line-height:1.2;cursor:pointer;white-space:nowrap}
.dzw-b:hover{border-color:var(--dz-primary,#2563eb)}
.dzw-b.on{background:var(--dz-primary,#2563eb);border-color:var(--dz-primary,#2563eb);color:#fff}
.dzw-b:disabled{opacity:.45;cursor:default}
.dzw input[type=color]{width:34px;height:30px;border:1px solid var(--dz-border,#e5e7eb);border-radius:8px;padding:2px;background:none}
.dzw select,.dzw input[type=text],.dzw input[type=number]{border:1px solid var(--dz-border,#e5e7eb);border-radius:8px;padding:5px 8px;font-size:.85rem;background:var(--dz-surface,#fff);color:inherit}
.dzw-note{font-size:.8rem;opacity:.7;padding:6px 10px}
.dz-wg-err{padding:14px;border:1px dashed #ef4444;border-radius:10px;color:#b91c1c;font-size:.9rem}
.dz-wg-builder{padding:18px;border:2px dashed var(--dz-border,#cbd5e1);border-radius:12px;text-align:center;opacity:.8}
@media (max-width:640px){.dzw-b span.dzw-lbl{display:none}}
`);
export const btn = (icon, label, onclick, extra = {}) => h("button", { type: "button", class: "dzw-b", title: label, onclick, ...extra }, icon ? h("i", { class: icon }) : null, h("span", { class: "dzw-lbl" }, label));
