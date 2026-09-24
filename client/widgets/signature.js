/* Signature : on signe au doigt ou à la souris ; l'image (PNG) va dans le champ relié. */
import { register, css, h, conf, champ, btn } from "./_commun.js";

css("signature", `.dzw-sig canvas{display:block;width:100%;touch-action:none;background:#fff;cursor:crosshair}
.dzw-sig .dzw-line{position:absolute;left:24px;right:24px;bottom:58px;border-bottom:1px dashed #cbd5e1;pointer-events:none}
.dzw-sig img{display:block;max-width:100%;background:#fff}`);

register("signature", (el) => {
  const c = champ(el);
  const height = conf(el, "hauteur", 180), color = conf(el, "couleur", "#111827");
  const lecture = conf(el, "lecture", false);
  el.classList.add("dzw", "dzw-sig");
  if (lecture) { const v = c.get(); el.innerHTML = ""; el.append(v ? h("img", { src: v, alt: "signature" }) : h("div", { class: "dzw-note" }, "Pas de signature")); return; }
  const cv = h("canvas", { height });
  const status = h("span", { class: "dzw-note" }, "Signe dans le cadre");
  let drawing = false, last = null, dirty = false;
  const ctx = cv.getContext("2d");
  const fit = () => {
    const img = dirty ? cv.toDataURL() : null;
    const r = window.devicePixelRatio || 1;
    cv.width = cv.clientWidth * r; cv.height = height * r; cv.style.height = height + "px";
    ctx.setTransform(r, 0, 0, r, 0, 0);
    ctx.lineCap = ctx.lineJoin = "round"; ctx.strokeStyle = color;
    if (img) { const i = new Image(); i.onload = () => ctx.drawImage(i, 0, 0, cv.clientWidth, height); i.src = img; }
  };
  const pos = (e) => { const b = cv.getBoundingClientRect(); return { x: e.clientX - b.left, y: e.clientY - b.top, p: e.pressure || 0.5 }; };
  cv.addEventListener("pointerdown", (e) => { drawing = true; last = pos(e); cv.setPointerCapture(e.pointerId); });
  cv.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    const p = pos(e);
    ctx.lineWidth = 1.2 + p.p * 2.4;
    ctx.beginPath(); ctx.moveTo(last.x, last.y); ctx.lineTo(p.x, p.y); ctx.stroke();
    last = p; dirty = true;
  });
  const end = () => { if (!drawing) return; drawing = false; if (dirty) { c.set(cv.toDataURL("image/png")); status.textContent = "Signature enregistrée dans le formulaire"; } };
  cv.addEventListener("pointerup", end); cv.addEventListener("pointercancel", end);
  const clear = () => { ctx.clearRect(0, 0, cv.width, cv.height); dirty = false; c.set(""); status.textContent = "Signe dans le cadre"; };
  el.innerHTML = "";
  el.append(cv, h("div", { class: "dzw-line" }), h("div", { class: "dzw-bar" }, status, h("span", { class: "dzw-sp" }), btn("fas fa-eraser", "Effacer", clear)));
  fit();
  const prev = c.get();
  if (prev && prev.startsWith("data:image")) { const i = new Image(); i.onload = () => { ctx.drawImage(i, 0, 0, cv.clientWidth, height); dirty = true; }; i.src = prev; }
  new ResizeObserver(() => { if (Math.abs(cv.width / (window.devicePixelRatio || 1) - cv.clientWidth) > 2) fit(); }).observe(cv);
});
