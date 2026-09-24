/* Carte interactive (Leaflet + OpenStreetMap) : points d'une liste ou d'une table,
   choix d'une position pour un formulaire, recherche d'adresse, « où suis-je ». */
import L from "leaflet";
import leafletCss from "leaflet/dist/leaflet.css";
import { register, css, h, conf, champ, btn, tableRows, esc, toast } from "./_commun.js";

css("leaflet", leafletCss);
css("carte", `.dzw-carte .dzw-carte-map{width:100%;z-index:0}
.dzw-carte .dzw-carte-search{flex:1;min-width:160px}
.dzw-pin{width:26px;height:26px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.35)}
.dzw-pin i{transform:rotate(45deg);display:block;text-align:center;line-height:22px;color:#fff;font-size:11px}
.dzw-carte .leaflet-popup-content{margin:10px 12px;font:inherit}
.dzw-carte .leaflet-popup-content b{display:block;margin-bottom:2px}`);

const pin = (couleur = "#2563eb", icone = "") => L.divIcon({ className: "", html: `<div class="dzw-pin" style="background:${esc(couleur)}">${icone ? `<i class="${esc(icone)}"></i>` : ""}</div>`, iconSize: [26, 26], iconAnchor: [13, 26], popupAnchor: [0, -24] });
const parsePos = (v) => { const m = String(v || "").match(/(-?\d+(?:\.\d+)?)\s*[,; ]\s*(-?\d+(?:\.\d+)?)/); return m ? [+m[1], +m[2]] : null; };

register("carte", async (el) => {
  const H = conf(el, "hauteur", 380);
  const mode = conf(el, "mode", "afficher");
  const c = champ(el);
  el.classList.add("dzw", "dzw-carte");
  el.innerHTML = "";
  const bar = h("div", { class: "dzw-bar" });
  const mapEl = h("div", { class: "dzw-carte-map", style: { height: H + "px" } });
  el.append(bar, mapEl);
  const centre = parsePos(conf(el, "centre", "")) || [46.6, 2.4];
  const map = L.map(mapEl, { scrollWheelZoom: conf(el, "molette", false), zoomControl: true }).setView(centre, conf(el, "zoom", 5));
  L.tileLayer(conf(el, "tuiles", "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"), { maxZoom: 19, attribution: conf(el, "attribution", '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>') }).addTo(map);
  new ResizeObserver(() => map.invalidateSize()).observe(mapEl);
  const groupe = L.featureGroup().addTo(map);

  /* recherche d'adresse (France : BAN, sinon OpenStreetMap) */
  const q = h("input", { type: "text", class: "dzw-carte-search", placeholder: "Chercher une adresse ou un lieu…" });
  const chercher = async () => {
    const t = q.value.trim(); if (!t) return;
    try {
      let r = await fetch(`https://data.geopf.fr/geocodage/search?q=${encodeURIComponent(t)}&limit=1`).then((x) => x.json()).catch(() => null);
      let pos = r && r.features && r.features[0] ? [r.features[0].geometry.coordinates[1], r.features[0].geometry.coordinates[0]] : null;
      if (!pos) { r = await fetch(`https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(t)}`).then((x) => x.json()); pos = r[0] ? [+r[0].lat, +r[0].lon] : null; }
      if (!pos) return toast("Lieu introuvable", "warning");
      map.setView(pos, 16);
      if (mode === "choisir") poser(pos);
    } catch (e) { toast("Recherche impossible : " + e.message, "danger"); }
  };
  q.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); chercher(); } });
  bar.append(q, btn("fas fa-search", "Chercher", chercher), btn("fas fa-location-arrow", "Ma position", () => {
    if (!navigator.geolocation) return toast("Géolocalisation indisponible", "warning");
    navigator.geolocation.getCurrentPosition((p) => { const pos = [p.coords.latitude, p.coords.longitude]; map.setView(pos, 16); if (mode === "choisir") poser(pos); else L.circleMarker(pos, { radius: 8, color: "#fff", weight: 3, fillColor: "#2563eb", fillOpacity: 1 }).addTo(map); }, () => toast("Position refusée", "warning"), { enableHighAccuracy: true, timeout: 10000 });
  }));

  /* mode « choisir » : une épingle déplaçable, la position va dans le champ */
  let marqueur = null;
  const poser = (pos) => {
    if (!marqueur) { marqueur = L.marker(pos, { draggable: true, icon: pin(conf(el, "couleur", "#ef4444"), "fas fa-map-pin") }).addTo(map); marqueur.on("dragend", () => ecrire(marqueur.getLatLng())); }
    else marqueur.setLatLng(pos);
    ecrire(marqueur.getLatLng());
  };
  const ecrire = (ll) => c.set(`${ll.lat.toFixed(6)},${ll.lng.toFixed(6)}`);
  if (mode === "choisir") {
    const p0 = parsePos(c.get());
    if (p0) { poser(p0); map.setView(p0, 15); }
    map.on("click", (e) => poser([e.latlng.lat, e.latlng.lng]));
    bar.append(h("span", { class: "dzw-note" }, "Clique sur la carte pour placer l'épingle"));
    return;
  }

  /* mode « afficher » : points fournis ou lus dans une table */
  let points = conf(el, "points", []);
  const table = conf(el, "table", "");
  if (table) {
    try {
      const rows = await tableRows(table, conf(el, "filtre", {}));
      const fLat = conf(el, "champ-lat", ""), fLon = conf(el, "champ-lon", ""), fPos = conf(el, "champ-position", "position"), fT = conf(el, "champ-titre", "nom"), fTx = conf(el, "champ-texte", ""), fL = conf(el, "lien", "");
      points = rows.map((r) => { const pos = fLat ? [+r[fLat], +r[fLon]] : parsePos(r[fPos]); return pos && !isNaN(pos[0]) ? { lat: pos[0], lon: pos[1], titre: r[fT], texte: fTx ? r[fTx] : "", lien: fL ? fL.replace(/\{id\}/g, r.id) : "" } : null; }).filter(Boolean);
    } catch (e) { bar.append(h("span", { class: "dzw-note" }, "Table illisible : " + e.message)); }
  }
  for (const p of points) {
    const pos = p.lat !== undefined ? [+p.lat, +p.lon] : parsePos(p.position);
    if (!pos) continue;
    const m = L.marker(pos, { icon: pin(p.couleur || conf(el, "couleur", "#2563eb"), p.icone || "") }).addTo(groupe);
    if (p.titre || p.texte) m.bindPopup(`<b>${esc(p.titre || "")}</b>${p.texte ? esc(p.texte) : ""}${p.lien ? `<br><a href="${esc(p.lien)}">Ouvrir</a>` : ""}`);
  }
  if (groupe.getLayers().length) map.fitBounds(groupe.getBounds().pad(0.2), { maxZoom: 15 });
  bar.append(h("span", { class: "dzw-note" }, `${groupe.getLayers().length} point(s)`));
});
