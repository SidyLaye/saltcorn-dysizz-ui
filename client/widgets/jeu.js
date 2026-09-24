/* Mini moteur de jeux 2D (canvas) + jeux prêts à jouer : serpent, casse-briques,
   2048, mémoire, morpion, coureur, quiz. On peut aussi écrire son propre jeu :
   <script type="text/dz-jeu"> … </script> dans le bloc, avec l'objet `jeu`. */
import { register, css, h, conf, btn, tableSave, toast } from "./_commun.js";

css("jeu", `.dzw-jeu .dzw-jeu-zone{position:relative;background:#0f172a;display:grid;place-items:center;user-select:none;-webkit-user-select:none}
.dzw-jeu canvas{display:block;max-width:100%;height:auto;touch-action:none;image-rendering:auto}
.dzw-jeu .dzw-jeu-ov{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:rgba(15,23,42,.72);color:#fff;text-align:center;padding:16px}
.dzw-jeu .dzw-jeu-ov h3{margin:0;font-size:1.6rem;color:#fff}
.dzw-jeu .dzw-jeu-ov p{margin:0;opacity:.85;max-width:420px}
.dzw-jeu .dzw-jeu-ov .dzw-b{background:var(--dz-primary,#2563eb);color:#fff;border:0;padding:10px 18px;font-size:1rem}
.dzw-jeu .dzw-jeu-pad{display:none;gap:8px;justify-content:center;padding:8px;background:#0b1222}
.dzw-jeu .dzw-jeu-pad button{width:56px;height:48px;border-radius:12px;border:0;background:#1e293b;color:#fff;font-size:1.2rem}
@media (hover:none){.dzw-jeu .dzw-jeu-pad.on{display:flex}}
.dzw-jeu .dzw-jeu-score{font-variant-numeric:tabular-nums;font-weight:600}`);

/* ---------------- moteur ---------------- */
class Jeu {
  constructor(canvas, largeur, hauteur) {
    this.cv = canvas; this.W = largeur; this.H = hauteur;
    const r = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = largeur * r; canvas.height = hauteur * r; canvas.style.width = largeur + "px";
    this.ctx = canvas.getContext("2d"); this.ctx.scale(r, r);
    this.touches = new Set(); this.appuis = new Set(); this.souris = { x: 0, y: 0, bas: false, clic: false };
    this.score = 0; this.enCours = false; this.t = 0; this._scene = null; this._ecouteurs = [];
    this.audio = null;
    const kd = (e) => { if (!this.actif) return; const k = this.nomTouche(e.key); if (["haut", "bas", "gauche", "droite", "espace"].includes(k)) e.preventDefault(); if (!this.touches.has(k)) this.appuis.add(k); this.touches.add(k); };
    const ku = (e) => this.touches.delete(this.nomTouche(e.key));
    window.addEventListener("keydown", kd); window.addEventListener("keyup", ku);
    const pos = (e) => { const b = canvas.getBoundingClientRect(); this.souris.x = ((e.clientX - b.left) / b.width) * this.W; this.souris.y = ((e.clientY - b.top) / b.height) * this.H; };
    canvas.addEventListener("pointermove", pos);
    canvas.addEventListener("pointerdown", (e) => { pos(e); this.souris.bas = true; this.souris.clic = true; this.actif = true; this._sx = e.clientX; this._sy = e.clientY; });
    canvas.addEventListener("pointerup", (e) => { this.souris.bas = false; const dx = e.clientX - this._sx, dy = e.clientY - this._sy; if (Math.hypot(dx, dy) > 30) this.appuis.add(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "droite" : "gauche") : dy > 0 ? "bas" : "haut"); });
    document.addEventListener("pointerdown", (e) => { this.actif = canvas.parentElement.contains(e.target) || canvas.closest(".dzw").contains(e.target); });
    this.actif = false;
  }
  nomTouche(k) { return { ArrowUp: "haut", ArrowDown: "bas", ArrowLeft: "gauche", ArrowRight: "droite", " ": "espace", z: "haut", s: "bas", q: "gauche", d: "droite", w: "haut", a: "gauche", Enter: "entree" }[k] || String(k).toLowerCase(); }
  appui(k) { return this.appuis.has(k); }
  touche(k) { return this.touches.has(k); }
  scene(s) { this._scene = s; if (s.debut) s.debut(this); }
  demarrer() {
    if (this.enCours) return; this.enCours = true; let last = performance.now(), acc = 0; const pas = 1000 / 60;
    const loop = (now) => {
      if (!this.enCours) return;
      acc += Math.min(250, now - last); last = now;
      while (acc >= pas) { this.t += pas / 1000; if (this._scene && this._scene.maj) this._scene.maj(this, pas / 1000); this.appuis.clear(); this.souris.clic = false; acc -= pas; }
      if (this._scene && this._scene.dessin) this._scene.dessin(this, this.ctx);
      this._raf = requestAnimationFrame(loop);
    };
    this._raf = requestAnimationFrame(loop);
  }
  arreter() { this.enCours = false; cancelAnimationFrame(this._raf); }
  /* dessin */
  fond(c) { this.ctx.fillStyle = c; this.ctx.fillRect(0, 0, this.W, this.H); }
  rect(x, y, w, hh, c, r = 0) { const g = this.ctx; g.fillStyle = c; if (r) { g.beginPath(); g.roundRect(x, y, w, hh, r); g.fill(); } else g.fillRect(x, y, w, hh); }
  rond(x, y, r, c) { const g = this.ctx; g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); }
  texte(t, x, y, { taille = 20, couleur = "#fff", align = "center", gras = true } = {}) { const g = this.ctx; g.fillStyle = couleur; g.textAlign = align; g.textBaseline = "middle"; g.font = `${gras ? "700 " : ""}${taille}px system-ui,sans-serif`; g.fillText(t, x, y); }
  /* utilitaires */
  collision(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }
  hasard(a, b) { return a + Math.random() * (b - a); }
  entier(a, b) { return Math.floor(this.hasard(a, b + 1)); }
  son(freq = 440, duree = 0.08, type = "square", vol = 0.05) {
    try { this.audio = this.audio || new (window.AudioContext || window.webkitAudioContext)(); const o = this.audio.createOscillator(), g = this.audio.createGain(); o.type = type; o.frequency.value = freq; g.gain.value = vol; g.gain.exponentialRampToValueAtTime(0.0001, this.audio.currentTime + duree); o.connect(g).connect(this.audio.destination); o.start(); o.stop(this.audio.currentTime + duree); } catch (e) { /* pas de son */ }
  }
  points(n = 1) { this.score += n; this._ecouteurs.forEach((f) => f("score", this.score)); }
  fin(message) { this.arreter(); this._ecouteurs.forEach((f) => f("fin", this.score, message)); }
  gagne(message) { this.arreter(); this._ecouteurs.forEach((f) => f("gagne", this.score, message)); }
  on(f) { this._ecouteurs.push(f); }
}

/* ---------------- jeux prêts ---------------- */
const JEUX = {
  serpent: { titre: "Serpent", aide: "Flèches, ZQSD ou glisser le doigt. Mange les pommes, ne te mords pas.", W: 400, H: 400, pad: true,
    scene: () => { const N = 20, S = 20; let sn, dir, next, pomme, tick, vitesse;
      const place = (j) => { do pomme = { x: j.entier(0, N - 1), y: j.entier(0, N - 1) }; while (sn.some((p) => p.x === pomme.x && p.y === pomme.y)); };
      return { debut(j) { sn = [{ x: 10, y: 10 }, { x: 9, y: 10 }, { x: 8, y: 10 }]; dir = { x: 1, y: 0 }; next = dir; tick = 0; vitesse = 0.13; place(j); },
        maj(j, dt) {
          const D = { haut: [0, -1], bas: [0, 1], gauche: [-1, 0], droite: [1, 0] };
          for (const k in D) if (j.appui(k) && (D[k][0] !== -dir.x || D[k][1] !== -dir.y)) next = { x: D[k][0], y: D[k][1] };
          if ((tick += dt) < vitesse) return; tick = 0; dir = next;
          const t = { x: (sn[0].x + dir.x + N) % N, y: (sn[0].y + dir.y + N) % N };
          if (sn.some((p) => p.x === t.x && p.y === t.y)) { j.son(110, 0.4, "sawtooth"); return j.fin("Le serpent s'est mordu !"); }
          sn.unshift(t);
          if (t.x === pomme.x && t.y === pomme.y) { j.points(10); j.son(880); vitesse = Math.max(0.05, vitesse - 0.004); place(j); } else sn.pop();
        },
        dessin(j) { j.fond("#0f172a"); for (let x = 0; x < N; x++) for (let y = 0; y < N; y++) if ((x + y) % 2) j.rect(x * S, y * S, S, S, "#111c33");
          j.rond(pomme.x * S + S / 2, pomme.y * S + S / 2, S / 2 - 2, "#ef4444");
          sn.forEach((p, i) => j.rect(p.x * S + 1, p.y * S + 1, S - 2, S - 2, i ? "#22c55e" : "#86efac", 5)); } }; } },

  "casse-briques": { titre: "Casse-briques", aide: "Souris, doigt ou flèches pour la raquette. Casse toutes les briques.", W: 480, H: 400,
    scene: () => { let pad, balle, briques, vies, colle;
      const COUL = ["#ef4444", "#f59e0b", "#eab308", "#22c55e", "#3b82f6", "#8b5cf6"];
      const niveau = () => { briques = []; for (let r = 0; r < 6; r++) for (let c = 0; c < 10; c++) briques.push({ x: 8 + c * 46.4, y: 40 + r * 20, w: 42, h: 15, c: COUL[r], pts: (6 - r) * 5 }); };
      return { debut() { pad = { x: 200, y: 370, w: 80, h: 10 }; balle = { x: 240, y: 355, vx: 180, vy: -260, r: 6 }; vies = 3; colle = true; niveau(); },
        maj(j, dt) {
          if (j.touche("gauche")) pad.x -= 420 * dt; if (j.touche("droite")) pad.x += 420 * dt;
          if (j.souris.x && (j.souris.bas || !j.touches.size)) pad.x += (j.souris.x - pad.w / 2 - pad.x) * 0.35;
          pad.x = Math.max(0, Math.min(j.W - pad.w, pad.x));
          if (colle) { balle.x = pad.x + pad.w / 2; balle.y = pad.y - 8; if (j.appui("espace") || j.souris.clic || j.appui("haut")) colle = false; return; }
          balle.x += balle.vx * dt; balle.y += balle.vy * dt;
          if (balle.x < balle.r || balle.x > j.W - balle.r) { balle.vx *= -1; balle.x = Math.max(balle.r, Math.min(j.W - balle.r, balle.x)); j.son(300, 0.03); }
          if (balle.y < balle.r) { balle.vy = Math.abs(balle.vy); j.son(300, 0.03); }
          const bb = { x: balle.x - balle.r, y: balle.y - balle.r, w: balle.r * 2, h: balle.r * 2 };
          if (balle.vy > 0 && j.collision(bb, pad)) { const k = (balle.x - (pad.x + pad.w / 2)) / (pad.w / 2); const v = Math.hypot(balle.vx, balle.vy) * 1.02; balle.vx = v * Math.sin(k * 1.05); balle.vy = -Math.abs(v * Math.cos(k * 1.05)); j.son(520, 0.04); }
          for (const b of briques) if (!b.mort && j.collision(bb, b)) { b.mort = true; j.points(b.pts); j.son(700 + b.pts * 10, 0.05); const ox = Math.min(bb.x + bb.w - b.x, b.x + b.w - bb.x), oy = Math.min(bb.y + bb.h - b.y, b.y + b.h - bb.y); if (ox < oy) balle.vx *= -1; else balle.vy *= -1; break; }
          if (briques.every((b) => b.mort)) return j.gagne("Toutes les briques sont cassées !");
          if (balle.y > j.H + 20) { vies--; j.son(120, 0.3, "sawtooth"); if (!vies) return j.fin("Plus de balles."); colle = true; }
        },
        dessin(j) { j.fond("#0f172a"); briques.forEach((b) => !b.mort && j.rect(b.x, b.y, b.w, b.h, b.c, 3)); j.rect(pad.x, pad.y, pad.w, pad.h, "#e2e8f0", 5); j.rond(balle.x, balle.y, balle.r, "#fff");
          for (let i = 0; i < vies; i++) j.rond(14 + i * 16, 16, 5, "#f472b6"); if (colle) j.texte("Clic ou espace pour lancer", j.W / 2, 250, { taille: 16, gras: false }); } }; } },

  "2048": { titre: "2048", aide: "Flèches ou glisser : les tuiles identiques fusionnent. Atteins 2048 !", W: 400, H: 400, pad: true,
    scene: () => { let g; const N = 4;
      const COUL = { 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e" };
      const ajoute = (j) => { const v = []; g.forEach((r, y) => r.forEach((c, x) => !c && v.push([x, y]))); if (!v.length) return; const [x, y] = v[j.entier(0, v.length - 1)]; g[y][x] = Math.random() < 0.9 ? 2 : 4; };
      const glisse = (j, dx, dy) => { let bouge = false, gagne = false;
        const ordre = [...Array(N).keys()]; const xs = dx > 0 ? ordre.slice().reverse() : ordre, ys = dy > 0 ? ordre.slice().reverse() : ordre; const fus = new Set();
        for (const y of ys) for (const x of xs) { if (!g[y][x]) continue; let cx = x, cy = y;
          while (true) { const nx = cx + dx, ny = cy + dy; if (nx < 0 || ny < 0 || nx >= N || ny >= N) break;
            if (!g[ny][nx]) { g[ny][nx] = g[cy][cx]; g[cy][cx] = 0; cx = nx; cy = ny; bouge = true; }
            else if (g[ny][nx] === g[cy][cx] && !fus.has(ny * N + nx)) { g[ny][nx] *= 2; g[cy][cx] = 0; fus.add(ny * N + nx); j.points(g[ny][nx]); if (g[ny][nx] === 2048) gagne = true; bouge = true; break; } else break; } }
        if (bouge) { ajoute(j); j.son(420, 0.04, "triangle"); } if (gagne) j.gagne("2048 atteint !");
        const bloque = g.every((r, y) => r.every((c, x) => c && (x === N - 1 || c !== r[x + 1]) && (y === N - 1 || c !== g[y + 1][x]))); if (bloque) j.fin("Plus aucun coup possible."); };
      return { debut(j) { g = [...Array(N)].map(() => Array(N).fill(0)); ajoute(j); ajoute(j); },
        maj(j) { if (j.appui("gauche")) glisse(j, -1, 0); else if (j.appui("droite")) glisse(j, 1, 0); else if (j.appui("haut")) glisse(j, 0, -1); else if (j.appui("bas")) glisse(j, 0, 1); },
        dessin(j) { j.fond("#bbada0"); const S = 90, M = 8; g.forEach((r, y) => r.forEach((c, x) => { j.rect(M + x * (S + M) + 4, M + y * (S + M) + 4, S, S, c ? COUL[c] || "#3c3a32" : "#cdc1b4", 8); if (c) j.texte(String(c), M + x * (S + M) + 4 + S / 2, M + y * (S + M) + 4 + S / 2, { taille: c > 512 ? 28 : 34, couleur: c > 4 ? "#fff" : "#776e65" }); })); } }; } },

  memoire: { titre: "Mémoire", aide: "Retourne les cartes deux par deux et retrouve toutes les paires.", W: 420, H: 420,
    scene: () => { let cartes, ouvertes, attente, coups; const E = ["🍎", "🚀", "🎸", "🐙", "🌵", "⚽", "🎲", "🦊"];
      return { debut(j) { cartes = [...E, ...E].map((e) => ({ e, ok: false, vue: false })).sort(() => Math.random() - 0.5); ouvertes = []; attente = 0; coups = 0; },
        maj(j, dt) { if (attente > 0) { attente -= dt; if (attente <= 0) { ouvertes.forEach((c) => (c.vue = false)); ouvertes = []; } return; }
          if (!j.souris.clic) return; const S = 100, i = Math.floor((j.souris.x - 10) / S) + 4 * Math.floor((j.souris.y - 10) / S); const c = cartes[i];
          if (!c || c.ok || c.vue || i < 0) return; c.vue = true; ouvertes.push(c); j.son(600, 0.04, "triangle");
          if (ouvertes.length === 2) { coups++; if (ouvertes[0].e === ouvertes[1].e) { ouvertes.forEach((x) => (x.ok = true)); ouvertes = []; j.points(Math.max(5, 30 - coups)); j.son(990, 0.1, "triangle"); if (cartes.every((x) => x.ok)) j.gagne(`Bravo, en ${coups} coups !`); } else attente = 0.8; } },
        dessin(j) { j.fond("#0f172a"); cartes.forEach((c, i) => { const x = 10 + (i % 4) * 100, y = 10 + Math.floor(i / 4) * 100; j.rect(x + 4, y + 4, 92, 92, c.ok ? "#14532d" : c.vue ? "#e2e8f0" : "#2563eb", 12); if (c.vue || c.ok) j.texte(c.e, x + 50, y + 52, { taille: 44 }); else j.texte("?", x + 50, y + 52, { taille: 34, couleur: "#bfdbfe" }); }); } }; } },

  morpion: { titre: "Morpion", aide: "Aligne 3 ✕ avant l'ordinateur. Clique sur une case.", W: 360, H: 360,
    scene: () => { let b, fini; const L = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
      const gagnant = (t) => { for (const [a, c, d] of L) if (t[a] && t[a] === t[c] && t[a] === t[d]) return t[a]; return t.every(Boolean) ? "nul" : null; };
      const mm = (t, joueur) => { const w = gagnant(t); if (w === "O") return { s: 1 }; if (w === "X") return { s: -1 }; if (w === "nul") return { s: 0 };
        let best = { s: joueur === "O" ? -2 : 2 }; t.forEach((v, i) => { if (v) return; t[i] = joueur; const r = mm(t, joueur === "O" ? "X" : "O"); t[i] = null; if (joueur === "O" ? r.s > best.s : r.s < best.s) best = { s: r.s, i }; }); return best; };
      return { debut() { b = Array(9).fill(null); fini = false; },
        maj(j) { if (fini || !j.souris.clic) return; const i = Math.floor(j.souris.x / 120) + 3 * Math.floor(j.souris.y / 120); if (b[i]) return; b[i] = "X"; j.son(500);
          let w = gagnant(b); if (!w) { const m = mm(b, "O"); if (m.i !== undefined && Math.random() > 0.15) b[m.i] = "O"; else { const libres = b.map((v, k) => (v ? null : k)).filter((k) => k !== null); b[libres[j.entier(0, libres.length - 1)]] = "O"; } w = gagnant(b); }
          if (w) { fini = true; if (w === "X") { j.points(100); setTimeout(() => j.gagne("Tu as battu l'ordinateur !"), 400); } else setTimeout(() => j.fin(w === "nul" ? "Match nul." : "L'ordinateur a gagné."), 400); } },
        dessin(j) { j.fond("#0f172a"); for (let k = 1; k < 3; k++) { j.rect(k * 120 - 2, 10, 4, 340, "#334155"); j.rect(10, k * 120 - 2, 340, 4, "#334155"); }
          b.forEach((v, i) => v && j.texte(v === "X" ? "✕" : "◯", (i % 3) * 120 + 60, Math.floor(i / 3) * 120 + 62, { taille: 70, couleur: v === "X" ? "#60a5fa" : "#f472b6" })); } }; } },

  coureur: { titre: "Coureur", aide: "Espace, flèche haut ou toucher pour sauter par-dessus les obstacles.", W: 520, H: 260,
    scene: () => { let p, obs, vitesse, dist, nuages;
      return { debut(j) { p = { x: 60, y: 200, w: 28, h: 36, vy: 0 }; obs = []; vitesse = 280; dist = 0; nuages = [...Array(4)].map(() => ({ x: j.hasard(0, 520), y: j.hasard(20, 90) })); },
        maj(j, dt) { const sol = 236 - p.h;
          if ((j.appui("espace") || j.appui("haut") || j.souris.clic) && p.y >= sol - 0.5) { p.vy = -560; j.son(660, 0.06, "triangle"); }
          p.vy += 1500 * dt; p.y = Math.min(sol, p.y + p.vy * dt);
          vitesse += 6 * dt; dist += vitesse * dt; if (Math.floor(dist / 100) > j.score) j.points(1);
          if (!obs.length || obs[obs.length - 1].x < j.W - j.hasard(220, 420)) { const hh = j.hasard(20, 46); obs.push({ x: j.W + 10, y: 236 - hh, w: j.hasard(16, 30), h: hh }); }
          obs.forEach((o) => (o.x -= vitesse * dt)); obs = obs.filter((o) => o.x > -40);
          nuages.forEach((n) => { n.x -= vitesse * 0.2 * dt; if (n.x < -60) n.x = j.W + 20; });
          if (obs.some((o) => j.collision({ x: p.x + 4, y: p.y + 2, w: p.w - 8, h: p.h - 4 }, o))) { j.son(100, 0.4, "sawtooth"); j.fin(`Distance : ${Math.floor(dist / 10)} m`); } },
        dessin(j) { j.fond("#e0f2fe"); nuages.forEach((n) => { j.rond(n.x, n.y, 14, "#fff"); j.rond(n.x + 16, n.y + 4, 12, "#fff"); j.rond(n.x - 14, n.y + 5, 10, "#fff"); });
          j.rect(0, 236, j.W, 24, "#a3e635"); j.rect(0, 236, j.W, 4, "#65a30d");
          obs.forEach((o) => j.rect(o.x, o.y, o.w, o.h, "#15803d", 4));
          j.rect(p.x, p.y, p.w, p.h, "#2563eb", 6); j.rect(p.x + 17, p.y + 8, 6, 6, "#fff", 2);
          j.texte(`${Math.floor(dist / 10)} m`, j.W - 14, 20, { taille: 16, couleur: "#0f172a", align: "right" }); } }; } },

  quiz: { titre: "Quiz", aide: "Réponds aux questions le plus vite possible.", W: 520, H: 380,
    scene: (el) => { let qs, i, choix, rep, t0, attente;
      const DEF = [{ q: "Capitale du Sénégal ?", r: ["Dakar", "Thiès", "Saint-Louis", "Ziguinchor"], ok: 0 }, { q: "2 + 2 × 3 = ?", r: ["12", "8", "10", "6"], ok: 1 }, { q: "Quel protocole sécurise le web ?", r: ["FTP", "HTTP", "TLS", "SMTP"], ok: 2 }];
      return { debut() { qs = conf(el, "questions", DEF); i = 0; rep = null; attente = 0; t0 = 0; },
        maj(j, dt) { t0 += dt; if (attente > 0) { attente -= dt; if (attente <= 0) { i++; rep = null; t0 = 0; if (i >= qs.length) j.gagne(`Score : ${j.score}`); } return; }
          if (!j.souris.clic) return; const k = Math.floor((j.souris.y - 150) / 54); if (k < 0 || k >= qs[i].r.length) return;
          rep = k; attente = 1.1; if (k === qs[i].ok) { j.points(Math.max(10, 100 - Math.floor(t0 * 10))); j.son(880, 0.12, "triangle"); } else j.son(160, 0.3, "sawtooth"); },
        dessin(j) { j.fond("#0f172a"); const q = qs[Math.min(i, qs.length - 1)];
          j.texte(`Question ${Math.min(i + 1, qs.length)} / ${qs.length}`, j.W / 2, 34, { taille: 14, couleur: "#94a3b8", gras: false });
          j.ctx.font = "700 22px system-ui"; const words = q.q.split(" "); let line = "", y = 80; for (const w of words) { if (j.ctx.measureText(line + w).width > 460) { j.texte(line, j.W / 2, y, { taille: 22 }); line = ""; y += 28; } line += w + " "; } j.texte(line, j.W / 2, y, { taille: 22 });
          q.r.forEach((r, k) => { const c = rep === null ? "#1e293b" : k === q.ok ? "#15803d" : k === rep ? "#b91c1c" : "#1e293b"; j.rect(40, 150 + k * 54, j.W - 80, 44, c, 10); j.texte(r, j.W / 2, 172 + k * 54, { taille: 18, gras: false }); }); } }; } },
};

register("jeu", (el) => {
  const nom = conf(el, "jeu", "serpent");
  const perso = el.querySelector('script[type="text/dz-jeu"]');
  const code = perso ? perso.textContent : null;
  const def = JEUX[nom] || (code ? { titre: conf(el, "titre", "Mon jeu"), aide: conf(el, "aide", ""), W: conf(el, "largeur", 480), H: conf(el, "hauteur", 360) } : JEUX.serpent);
  el.classList.add("dzw", "dzw-jeu");
  el.innerHTML = "";
  const zone = h("div", { class: "dzw-jeu-zone" });
  const cv = h("canvas", { tabindex: 0 });
  const score = h("span", { class: "dzw-jeu-score" }, "0");
  const cleRecord = "dzw-jeu-record-" + (nom || "perso");
  let record = 0; try { record = +localStorage.getItem(cleRecord) || 0; } catch (e) { /* rien */ }
  const rec = h("span", { class: "dzw-note" }, record ? `Record : ${record}` : "");
  const jeu = new Jeu(cv, def.W, def.H);
  const pad = h("div", { class: "dzw-jeu-pad" + (def.pad ? " on" : "") }, ...[["gauche", "◀"], ["haut", "▲"], ["bas", "▼"], ["droite", "▶"]].map(([k, t]) => h("button", { type: "button", onpointerdown: (e) => { e.preventDefault(); jeu.appuis.add(k); jeu.touches.add(k); jeu.actif = true; }, onpointerup: () => jeu.touches.delete(k) }, t)));
  const ov = h("div", { class: "dzw-jeu-ov" });
  const ecran = (titre, texte, bouton) => { ov.innerHTML = ""; ov.append(h("h3", {}, titre), texte ? h("p", {}, texte) : null, h("button", { type: "button", class: "dzw-b", onclick: lancer }, bouton)); ov.style.display = "flex"; };
  const makeScene = () => {
    if (JEUX[nom]) return JEUX[nom].scene(el);
    /* jeu écrit par l'utilisateur : le code reçoit `jeu` et renvoie une scène {debut, maj, dessin} */
    try { return new Function("jeu", code)(jeu) || {}; } catch (e) { ecran("Erreur dans le code du jeu", e.message, "Réessayer"); throw e; }
  };
  function lancer() { ov.style.display = "none"; jeu.score = 0; score.textContent = "0"; jeu.actif = true; cv.focus(); jeu.scene(makeScene()); jeu.demarrer(); }
  jeu.on(async (ev, s, msg) => {
    if (ev === "score") { score.textContent = s; return; }
    if (s > record) { record = s; rec.textContent = `Record : ${record}`; try { localStorage.setItem(cleRecord, record); } catch (e) { /* rien */ } }
    ecran(ev === "gagne" ? "Gagné ! 🎉" : "Perdu", `${msg || ""} Score : ${s}`, "Rejouer");
    if (ev === "gagne" && window.DZ && window.DZ.confetti) window.DZ.confetti();
    const t = conf(el, "table-scores", "");
    if (t && s > 0) { try { await tableSave(t, { jeu: def.titre, score: s, quand: new Date().toISOString() }); } catch (e) { toast("Score non enregistré : " + e.message, "warning"); } }
  });
  zone.append(cv, ov);
  el.append(h("div", { class: "dzw-bar" }, h("b", {}, def.titre), h("span", { class: "dzw-sp" }), rec, h("span", {}, "Score : ", score), btn("fas fa-expand", "Plein écran", () => (zone.requestFullscreen ? zone.requestFullscreen() : null))), zone, pad);
  ecran(def.titre, def.aide, "Jouer");
  /* écran d'accueil : on dessine la scène une fois pour donner envie */
  try { const s = makeScene(); if (s.debut) s.debut(jeu); if (s.dessin) s.dessin(jeu, jeu.ctx); } catch (e) { /* rien */ }
});
window.DZJeu = Jeu;
