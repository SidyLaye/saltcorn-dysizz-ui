/* Scanner : lit un QR code ou un code-barres avec la caméra (ou une photo),
   remplit le champ relié, ouvre le lien ou lance une recherche. Mode « photo » :
   prend une photo et la met dans le champ. */
import { register, css, h, conf, champ, btn, toast } from "./_commun.js";

css("scanner", `.dzw-scan .dzw-scan-v{position:relative;background:#000;aspect-ratio:4/3;max-height:420px;width:100%;display:grid;place-items:center;color:#94a3b8}
.dzw-scan video,.dzw-scan img.prev{width:100%;height:100%;object-fit:cover}
.dzw-scan .cadre{position:absolute;inset:18%;border:3px solid rgba(255,255,255,.85);border-radius:16px;box-shadow:0 0 0 999px rgba(0,0,0,.35)}
.dzw-scan .res{padding:10px 12px;font-family:ui-monospace,monospace;word-break:break-all}`);

register("scanner", (el) => {
  const c = champ(el);
  const mode = conf(el, "mode", "code");
  const action = conf(el, "action", "champ");
  el.classList.add("dzw", "dzw-scan");
  el.innerHTML = "";
  const zone = h("div", { class: "dzw-scan-v" }, h("div", {}, h("i", { class: `fas ${mode === "photo" ? "fa-camera" : "fa-qrcode"} fa-2x` })));
  const res = h("div", { class: "res" });
  let stream = null, timer = null, video = null;
  const stop = () => { clearInterval(timer); timer = null; if (stream) stream.getTracks().forEach((t) => t.stop()); stream = null; startBtn.hidden = false; stopBtn.hidden = true; snapBtn.hidden = true; };
  const found = (val) => {
    stop(); res.textContent = val; navigator.vibrate && navigator.vibrate(60);
    el.dispatchEvent(new CustomEvent("dz-scan", { detail: { valeur: val }, bubbles: true }));
    if (action === "lien" && /^https?:\/\//.test(val)) { location.href = val; return; }
    if (action === "chercher") { const u = conf(el, "url", "?q={valeur}"); location.href = u.replace("{valeur}", encodeURIComponent(val)); return; }
    c.set(val); toast("Code lu", "success");
  };
  const start = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return toast("Caméra indisponible (il faut une page en https)", "warning");
    try { stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment", width: { ideal: 1280 } }, audio: false }); }
    catch (e) { return toast("Caméra refusée", "warning"); }
    video = h("video", { playsinline: true, muted: true, autoplay: true }); video.srcObject = stream;
    zone.innerHTML = ""; zone.append(video); if (mode !== "photo") zone.append(h("div", { class: "cadre" }));
    await video.play().catch(() => {});
    startBtn.hidden = true; stopBtn.hidden = false;
    if (mode === "photo") { snapBtn.hidden = false; return; }
    if (!("BarcodeDetector" in window)) { res.textContent = "Ce navigateur ne sait pas lire les codes : utilise « Depuis une photo » ou Chrome / Edge / Safari récent."; return; }
    const det = new window.BarcodeDetector({ formats: conf(el, "formats", ["qr_code", "ean_13", "ean_8", "code_128", "code_39", "upc_a", "upc_e", "data_matrix", "pdf417"]) });
    timer = setInterval(async () => { if (video.readyState < 2) return; try { const r = await det.detect(video); if (r[0]) found(r[0].rawValue); } catch (e) { /* image suivante */ } }, 250);
  };
  const snap = () => {
    const cv = document.createElement("canvas"); const max = conf(el, "taille-max", 1280); const s = Math.min(1, max / Math.max(video.videoWidth, video.videoHeight));
    cv.width = video.videoWidth * s; cv.height = video.videoHeight * s; cv.getContext("2d").drawImage(video, 0, 0, cv.width, cv.height);
    const url = cv.toDataURL("image/jpeg", 0.85); stop(); zone.innerHTML = ""; zone.append(h("img", { class: "prev", src: url, alt: "photo" })); c.set(url); toast("Photo prise", "success");
  };
  const fileIn = h("input", { type: "file", accept: "image/*", capture: "environment", style: { display: "none" }, onchange: async (e) => {
    const f = e.target.files[0]; if (!f) return; e.target.value = "";
    if (mode === "photo") { const r = new FileReader(); r.onload = () => { zone.innerHTML = ""; zone.append(h("img", { class: "prev", src: r.result, alt: "photo" })); c.set(r.result); }; r.readAsDataURL(f); return; }
    if (!("BarcodeDetector" in window)) return toast("Lecture de code non disponible dans ce navigateur", "warning");
    try { const bmp = await createImageBitmap(f); const r = await new window.BarcodeDetector().detect(bmp); if (r[0]) found(r[0].rawValue); else toast("Aucun code trouvé sur la photo", "warning"); } catch (err) { toast("Photo illisible", "warning"); }
  } });
  const startBtn = btn("fas fa-video", mode === "photo" ? "Ouvrir la caméra" : "Scanner", start);
  const stopBtn = btn("fas fa-stop", "Arrêter", stop); stopBtn.hidden = true;
  const snapBtn = btn("fas fa-camera", "Prendre la photo", snap); snapBtn.hidden = true; snapBtn.classList.add("on");
  el.append(h("div", { class: "dzw-bar" }, startBtn, snapBtn, stopBtn, fileIn, btn("fas fa-image", "Depuis une photo", () => fileIn.click())), zone, res);
  new IntersectionObserver((e) => { if (!e[0].isIntersecting && stream) stop(); }).observe(el);
});
