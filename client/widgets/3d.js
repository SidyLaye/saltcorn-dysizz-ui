/* 3D : visionneuse de modèles (GLB, GLTF, STL, OBJ) et petit modeleur
   (formes, déplacer / tourner / agrandir, couleurs, import, export GLB/STL,
   enregistrement de la scène dans un champ). Moteur : three.js. */
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
import { GLTFExporter } from "three/examples/jsm/exporters/GLTFExporter.js";
import { STLExporter } from "three/examples/jsm/exporters/STLExporter.js";
import { register, css, h, conf, champ, btn, download, toast } from "./_commun.js";

css("3d", `.dzw-3d .dzw-3d-view{position:relative;width:100%;background:radial-gradient(circle at 50% 30%,#f8fafc,#e2e8f0)}
[data-bs-theme=dark] .dzw-3d .dzw-3d-view{background:radial-gradient(circle at 50% 30%,#1e293b,#0f172a)}
.dzw-3d canvas{display:block;width:100%;height:100%;outline:none;touch-action:none}
.dzw-3d .dzw-3d-side{position:absolute;right:8px;top:8px;display:flex;flex-direction:column;gap:6px;background:rgba(255,255,255,.9);border:1px solid #e5e7eb;border-radius:10px;padding:8px;font-size:.8rem;min-width:150px;color:#111827}
.dzw-3d .dzw-3d-side label{display:flex;justify-content:space-between;align-items:center;gap:8px}
.dzw-3d .dzw-3d-side input[type=range]{width:80px}
.dzw-3d .dzw-3d-hint{position:absolute;left:10px;bottom:8px;font-size:.75rem;opacity:.65;pointer-events:none}
.dzw-3d .dzw-3d-load{position:absolute;inset:0;display:grid;place-items:center;font-size:.9rem;opacity:.7}`);

const FORMES = {
  cube: () => new THREE.BoxGeometry(1, 1, 1),
  sphere: () => new THREE.SphereGeometry(0.6, 48, 32),
  cylindre: () => new THREE.CylinderGeometry(0.5, 0.5, 1, 48),
  cone: () => new THREE.ConeGeometry(0.55, 1, 48),
  tore: () => new THREE.TorusGeometry(0.5, 0.18, 24, 64),
  plan: () => new THREE.PlaneGeometry(2, 2),
  capsule: () => new THREE.CapsuleGeometry(0.35, 0.6, 8, 24),
  anneau: () => new THREE.TorusKnotGeometry(0.4, 0.13, 128, 16),
};
const PALETTE = ["#2563eb", "#16a34a", "#f59e0b", "#ef4444", "#8b5cf6", "#0ea5e9", "#ec4899", "#64748b"];

const charger = (url, type) => new Promise((resolve, reject) => {
  const ext = (type || String(url).split("?")[0].split(".").pop() || "").toLowerCase();
  const done = (o) => resolve(o);
  if (ext === "stl") new STLLoader().load(url, (g) => { g.computeVertexNormals(); done(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: "#94a3b8", metalness: 0.1, roughness: 0.6 }))); }, undefined, reject);
  else if (ext === "obj") new OBJLoader().load(url, done, undefined, reject);
  else new GLTFLoader().load(url, (g) => done(g.scene), undefined, reject);
});
/* centre et met à l'échelle un objet pour qu'il tienne dans ~2 unités */
const cadrer = (obj, taille = 2) => {
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3()).length() || 1;
  const c = box.getCenter(new THREE.Vector3());
  obj.position.sub(c);
  const s = taille / size; obj.scale.multiplyScalar(s); obj.position.multiplyScalar(s);
  obj.position.y += (box.getSize(new THREE.Vector3()).y * s) / 2;
};

register("3d", (el) => {
  const mode = conf(el, "mode", "visionneuse");
  const H = conf(el, "hauteur", 420);
  const c = champ(el);
  el.classList.add("dzw", "dzw-3d");
  el.innerHTML = "";
  const view = h("div", { class: "dzw-3d-view", style: { height: H + "px" } });
  const bar = h("div", { class: "dzw-bar" });
  if (mode === "modeleur") el.append(bar);
  el.append(view);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  view.append(renderer.domElement);
  renderer.domElement.tabIndex = 0;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.01, 1000);
  camera.position.set(3, 2.4, 3.6);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.4));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2);
  sun.position.set(4, 8, 5); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
  scene.add(sun);
  const sol = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.18 }));
  sol.rotation.x = -Math.PI / 2; sol.receiveShadow = true; scene.add(sol);
  const grid = new THREE.GridHelper(20, 40, 0x94a3b8, 0xcbd5e1);
  grid.material.transparent = true; grid.material.opacity = 0.5;
  if (mode === "modeleur" || conf(el, "grille", false)) scene.add(grid);
  const contenu = new THREE.Group(); contenu.name = "contenu"; scene.add(contenu);

  const orbit = new OrbitControls(camera, renderer.domElement);
  orbit.enableDamping = true; orbit.target.set(0, 0.5, 0);
  orbit.autoRotate = mode !== "modeleur" && conf(el, "rotation", true);
  orbit.autoRotateSpeed = 1.2;

  const resize = () => { const w = view.clientWidth, hh = view.clientHeight; renderer.setSize(w, hh, false); camera.aspect = w / hh; camera.updateProjectionMatrix(); };
  new ResizeObserver(resize).observe(view); resize();
  let visible = true;
  new IntersectionObserver((e) => { visible = e[0].isIntersecting; }).observe(view);
  renderer.setAnimationLoop(() => { if (!visible) return; orbit.update(); renderer.render(scene, camera); });

  const loading = (on, txt = "Chargement du modèle…") => { let l = view.querySelector(".dzw-3d-load"); if (on && !l) view.append(h("div", { class: "dzw-3d-load" }, txt)); if (!on && l) l.remove(); };
  const ajouterModele = async (url, type) => {
    loading(true);
    try { const o = await charger(url, type); o.traverse((m) => { if (m.isMesh) { m.castShadow = m.receiveShadow = true; } }); cadrer(o); contenu.add(o); return o; }
    catch (e) { toast("Modèle illisible : " + (e.message || e), "danger"); } finally { loading(false); }
  };
  const restaurer = (json) => {
    try {
      const data = typeof json === "string" ? JSON.parse(json) : json;
      const g = new THREE.ObjectLoader().parse(data);
      contenu.clear(); [...g.children].forEach((ch) => contenu.add(ch));
      return true;
    } catch (e) { return false; }
  };

  /* ---------- visionneuse ---------- */
  if (mode !== "modeleur") {
    const src = conf(el, "src", "") || c.get();
    if (src && /^\s*\{/.test(src)) restaurer(src);
    else if (src) ajouterModele(src);
    else { const m = new THREE.Mesh(new THREE.TorusKnotGeometry(0.5, 0.17, 160, 24), new THREE.MeshStandardMaterial({ color: conf(el, "couleur", "#2563eb"), metalness: 0.35, roughness: 0.3 })); m.position.y = 0.8; m.castShadow = true; contenu.add(m); }
    view.append(h("div", { class: "dzw-3d-hint" }, "Glisse pour tourner · molette ou pincer pour zoomer"));
    return;
  }

  /* ---------- modeleur ---------- */
  const gizmo = new TransformControls(camera, renderer.domElement);
  gizmo.addEventListener("dragging-changed", (e) => { orbit.enabled = !e.value; if (!e.value) snapshot(); });
  scene.add(gizmo.getHelper ? gizmo.getHelper() : gizmo);
  let sel = null;
  const side = h("div", { class: "dzw-3d-side", style: { display: "none" } });
  view.append(side, h("div", { class: "dzw-3d-hint" }, "Clic : choisir · G déplacer · R tourner · S taille · Suppr · Ctrl+Z"));
  const history = []; let hIndex = -1;
  const snapshot = () => { history.splice(hIndex + 1); history.push(JSON.stringify(contenu.toJSON())); if (history.length > 40) history.shift(); hIndex = history.length - 1; sauver(); };
  const undo = (dir = -1) => { const i = hIndex + dir; if (i < 0 || i >= history.length) return; hIndex = i; choisir(null); restaurer(history[i]); sauver(false); };
  let saveT = null;
  const sauver = (debounce = true) => { if (!c.input) return; clearTimeout(saveT); saveT = setTimeout(() => c.set(JSON.stringify(contenu.toJSON())), debounce ? 400 : 0); };

  const matOf = (o) => { let m = null; o.traverse((x) => { if (!m && x.isMesh) m = Array.isArray(x.material) ? x.material[0] : x.material; }); return m; };
  const panneau = () => {
    side.innerHTML = "";
    if (!sel) { side.style.display = "none"; return; }
    side.style.display = "flex";
    const m = matOf(sel);
    const row = (label, input) => h("label", {}, label, input);
    side.append(h("b", {}, sel.name || "Objet"));
    const name = h("input", { type: "text", value: sel.name || "", oninput: (e) => { sel.name = e.target.value; sauver(); } });
    side.append(row("Nom", name));
    if (m && m.color) {
      side.append(row("Couleur", h("input", { type: "color", value: "#" + m.color.getHexString(), oninput: (e) => { m.color.set(e.target.value); sauver(); }, onchange: snapshot })));
      side.append(row("Métal", h("input", { type: "range", min: 0, max: 1, step: 0.05, value: m.metalness ?? 0, oninput: (e) => { m.metalness = +e.target.value; }, onchange: snapshot })));
      side.append(row("Rugosité", h("input", { type: "range", min: 0, max: 1, step: 0.05, value: m.roughness ?? 0.5, oninput: (e) => { m.roughness = +e.target.value; }, onchange: snapshot })));
      side.append(row("Opacité", h("input", { type: "range", min: 0.1, max: 1, step: 0.05, value: m.opacity ?? 1, oninput: (e) => { m.opacity = +e.target.value; m.transparent = m.opacity < 1; }, onchange: snapshot })));
      side.append(row("Fil de fer", h("input", { type: "checkbox", ...(m.wireframe ? { checked: true } : {}), onchange: (e) => { m.wireframe = e.target.checked; snapshot(); } })));
    }
  };
  const choisir = (o) => { sel = o; if (o) gizmo.attach(o); else gizmo.detach(); panneau(); };
  const ajouter = (forme) => {
    const m = new THREE.Mesh(FORMES[forme](), new THREE.MeshStandardMaterial({ color: PALETTE[contenu.children.length % PALETTE.length], metalness: 0.1, roughness: 0.45, side: forme === "plan" ? THREE.DoubleSide : THREE.FrontSide }));
    m.name = forme.charAt(0).toUpperCase() + forme.slice(1) + " " + (contenu.children.length + 1);
    m.castShadow = m.receiveShadow = true;
    m.position.set((Math.random() - 0.5) * 1.5, forme === "plan" ? 0.01 : 0.6, (Math.random() - 0.5) * 1.5);
    if (forme === "plan") m.rotation.x = -Math.PI / 2;
    contenu.add(m); choisir(m); snapshot();
  };
  const dupliquer = () => { if (!sel) return; const o = sel.clone(); o.traverse((x) => { if (x.isMesh) x.material = x.material.clone(); }); o.position.x += 0.4; o.name = (sel.name || "Objet") + " (copie)"; contenu.add(o); choisir(o); snapshot(); };
  const supprimer = () => { if (!sel) return; const o = sel; choisir(null); o.removeFromParent(); snapshot(); };
  const modeBtns = {};
  const setMode = (m) => { gizmo.setMode(m); Object.entries(modeBtns).forEach(([k, b]) => b.classList.toggle("on", k === m)); };

  /* clic : sélection (le haut de la hiérarchie sous « contenu ») */
  const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(); let down = null;
  renderer.domElement.addEventListener("pointerdown", (e) => { down = [e.clientX, e.clientY]; });
  renderer.domElement.addEventListener("pointerup", (e) => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5 || gizmo.dragging) return;
    const b = renderer.domElement.getBoundingClientRect();
    ptr.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1);
    ray.setFromCamera(ptr, camera);
    const hit = ray.intersectObjects(contenu.children, true)[0];
    let o = hit ? hit.object : null;
    while (o && o.parent && o.parent !== contenu) o = o.parent;
    choisir(o);
  });
  renderer.domElement.addEventListener("keydown", (e) => {
    const k = e.key.toLowerCase();
    if ((e.ctrlKey || e.metaKey) && k === "z") { e.preventDefault(); undo(e.shiftKey ? 1 : -1); }
    else if ((e.ctrlKey || e.metaKey) && k === "d") { e.preventDefault(); dupliquer(); }
    else if (k === "g" || k === "t") setMode("translate"); else if (k === "r") setMode("rotate"); else if (k === "s") setMode("scale");
    else if (k === "delete" || k === "backspace") supprimer(); else if (k === "escape") choisir(null);
  });

  const fileIn = h("input", { type: "file", accept: ".glb,.gltf,.stl,.obj", style: { display: "none" }, onchange: async (e) => {
    const f = e.target.files[0]; if (!f) return;
    const url = URL.createObjectURL(f);
    const o = await ajouterModele(url, f.name.split(".").pop());
    URL.revokeObjectURL(url); e.target.value = "";
    if (o) { o.name = f.name; choisir(o); snapshot(); }
  } });
  const sel_forme = h("select", { onchange: (e) => { if (e.target.value) ajouter(e.target.value); e.target.value = ""; } }, h("option", { value: "" }, "+ Ajouter une forme"), ...Object.keys(FORMES).map((f) => h("option", { value: f }, f)));
  modeBtns.translate = btn("fas fa-arrows-alt", "Déplacer", () => setMode("translate"));
  modeBtns.rotate = btn("fas fa-sync-alt", "Tourner", () => setMode("rotate"));
  modeBtns.scale = btn("fas fa-expand-arrows-alt", "Taille", () => setMode("scale"));
  const snapBtn = btn("fas fa-magnet", "Aimanter", () => { const on = !snapBtn.classList.contains("on"); snapBtn.classList.toggle("on", on); gizmo.setTranslationSnap(on ? 0.25 : null); gizmo.setRotationSnap(on ? Math.PI / 12 : null); gizmo.setScaleSnap(on ? 0.25 : null); });
  const exporter = (fmt) => {
    choisir(null);
    if (fmt === "stl") return download(new STLExporter().parse(contenu, { binary: true }), "modele.stl", "model/stl");
    new GLTFExporter().parse(contenu, (r) => download(r, "modele.glb", "model/gltf-binary"), (e) => toast("Export impossible : " + e.message, "danger"), { binary: true });
  };
  const photo = () => { choisir(null); requestAnimationFrame(() => renderer.domElement.toBlob((b) => download(b, "modele.png", "image/png"))); };
  bar.append(sel_forme, fileIn, btn("fas fa-file-import", "Importer", () => fileIn.click()), modeBtns.translate, modeBtns.rotate, modeBtns.scale, snapBtn,
    btn("fas fa-clone", "Dupliquer", dupliquer), btn("fas fa-trash", "Supprimer", supprimer), btn("fas fa-undo", "Annuler", () => undo(-1)), btn("fas fa-redo", "Refaire", () => undo(1)),
    h("span", { class: "dzw-sp" }), btn("fas fa-camera", "Image", photo), btn("fas fa-download", "GLB", () => exporter("glb")), btn("fas fa-cube", "STL (impression 3D)", () => exporter("stl")));
  setMode("translate");
  const init = c.get() || conf(el, "src", "");
  if (init && /^\s*\{/.test(init) && restaurer(init)) { /* scène reprise */ }
  else if (init) ajouterModele(init);
  else { ajouter("cube"); choisir(null); }
  history.length = 0; hIndex = -1; snapshot();
});
