/* dysizz-ui — page /dysizz-ui/classes : référence des classes du kit,
   comportements, et éditeur de classes perso (visuel ou code). */
(function () {
  var D = JSON.parse(document.getElementById("dzc-data").textContent);
  var app = document.getElementById("dzc-app");
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function el(html) { var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; }
  function getJSON(u) { return fetch(u, { credentials: "same-origin" }).then(function (r) { return r.json(); }); }
  var famLoaded = {};
  function loadFam(f) { if (famLoaded[f]) return; famLoaded[f] = 1; var l = document.createElement("link"); l.rel = "stylesheet"; l.href = D.fam + f + ".css"; document.head.appendChild(l); }

  document.head.appendChild(el('<style>' +
    '.dzc-tabs{display:flex;gap:.3rem;flex-wrap:wrap;margin:1.2rem 0;border-bottom:1px solid var(--dz-border)}' +
    '.dzc-tabs button{border:0;background:none;color:var(--dz-text-soft);padding:.6rem 1rem;font-weight:600;border-bottom:2px solid transparent;margin-bottom:-1px}' +
    '.dzc-tabs button.on{color:var(--dz-text);border-color:var(--dz-primary)}' +
    '.dzc-layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:1.5rem;align-items:start}' +
    '.dzc-side{position:sticky;top:1rem;max-height:calc(100vh - 2rem);overflow:auto;display:grid;gap:.15rem}' +
    '.dzc-side input,.dzc-f input,.dzc-f select,.dzc-f textarea{width:100%;padding:.5rem .7rem;border:1px solid var(--dz-border);border-radius:8px;background:var(--dz-surface);color:var(--dz-text)}' +
    '.dzc-side a{display:flex;justify-content:space-between;gap:.5rem;padding:.35rem .6rem;border-radius:8px;color:var(--dz-text-soft);text-decoration:none;font-size:.88rem}' +
    '.dzc-side a:hover,.dzc-side a.on{background:var(--dz-surface-2);color:var(--dz-text)}' +
    '.dzc-side h6{margin:.8rem .6rem .2rem;font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dz-text-mute)}' +
    '.dzc-card{padding:1rem 1.1rem;border:1px solid var(--dz-border);border-radius:var(--dz-radius);background:var(--dz-surface);margin-bottom:.8rem}' +
    '.dzc-card header{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}.dzc-card code{font-size:.95rem;color:var(--dz-primary-ink);background:none;padding:0}' +
    '.dzc-card p{margin:.4rem 0;color:var(--dz-text-soft);font-size:.9rem}' +
    '.dzc-prev{position:relative;margin:.6rem 0;padding:1rem;border:1px dashed var(--dz-border);border-radius:8px;overflow:hidden;contain:layout paint;transform:translateZ(0);min-height:56px;max-height:340px;background:var(--dz-bg)}' +
    '.dzc-card pre{margin:.4rem 0 0;padding:.8rem;max-height:320px;overflow:auto;border-radius:8px;background:var(--dz-surface-2);font:12px/1.5 var(--dz-font-mono);white-space:pre}' +
    '.dzc-mini{font-size:.75rem;padding:.15rem .5rem;border:1px solid var(--dz-border);border-radius:6px;background:none;color:var(--dz-text-soft)}' +
    '.dzc-ed{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.5rem;align-items:start}' +
    '.dzc-f{display:grid;gap:.6rem}.dzc-f label{display:grid;gap:.2rem;font-size:.82rem;color:var(--dz-text-soft)}' +
    '.dzc-grp{border:1px solid var(--dz-border);border-radius:10px;padding:.2rem .8rem .8rem;background:var(--dz-surface)}' +
    '.dzc-grp summary{cursor:pointer;padding:.5rem 0;font-weight:650}' +
    '.dzc-row{display:grid;grid-template-columns:140px 1fr;gap:.6rem;align-items:center;margin-top:.35rem;font-size:.82rem}' +
    '.dzc-row .dzc-val{display:flex;gap:.4rem;align-items:center}.dzc-row input[type=range]{flex:1}.dzc-row input[type=color]{width:42px;height:32px;padding:2px}' +
    '.dzc-out{font:600 .75rem var(--dz-font-mono);min-width:4.2rem;text-align:right;color:var(--dz-text-mute)}' +
    '.dzc-stage{position:sticky;top:1rem;display:grid;gap:.6rem}.dzc-stagebox{padding:2rem;border:1px dashed var(--dz-border);border-radius:12px;min-height:220px;display:grid;place-items:center;background:var(--dz-bg);contain:layout paint;transform:translateZ(0)}' +
    '.dzc-mylist{display:grid;gap:.3rem;margin-bottom:1rem}.dzc-mylist a{display:flex;justify-content:space-between;padding:.45rem .7rem;border-radius:8px;border:1px solid var(--dz-border);text-decoration:none;color:var(--dz-text)}.dzc-mylist a.on{border-color:var(--dz-primary)}' +
    '@media (max-width:900px){.dzc-layout,.dzc-ed{grid-template-columns:1fr}.dzc-side,.dzc-stage{position:static;max-height:none}}' +
    '</style>'));

  if (D.ok) app.appendChild(el('<div class="dz-callout dz-callout-success mb-3"><div>' + esc(D.ok) + "</div></div>"));
  if (D.err) app.appendChild(el('<div class="dz-callout dz-callout-danger mb-3"><div>' + esc(D.err) + "</div></div>"));
  var tabs = el('<div class="dzc-tabs"><button data-t="kit">Classes du kit</button><button data-t="beh">Comportements (sans code)</button><button data-t="mine">Mes classes (' + D.mine.length + ")</button></div>");
  var body = el("<div></div>");
  app.appendChild(tabs); app.appendChild(body);
  function show(t) {
    tabs.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.dataset.t === t); });
    body.innerHTML = "";
    ({ kit: kitTab, beh: behTab, mine: mineTab })[t]();
    try { history.replaceState(null, "", "?tab=" + t); } catch (e) {}
  }
  tabs.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) show(b.dataset.t); });

  var IDX = null, DOCS = null;
  function data() {
    return Promise.all([IDX || getJSON(D.idx), DOCS || getJSON(D.docs)]).then(function (r) { IDX = r[0]; DOCS = r[1]; return r; });
  }
  function copyBtn(txt) { return '<button type="button" class="dzc-mini" data-copy="' + esc(txt) + '"><i class="far fa-copy"></i> copier</button>'; }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    (navigator.clipboard ? navigator.clipboard.writeText(b.dataset.copy) : Promise.reject()).then(function () { b.innerHTML = "✓ copié"; setTimeout(function () { b.innerHTML = '<i class="far fa-copy"></i> copier'; }, 1200); }, function () {});
  });

  /* ---------------- classes du kit ---------------- */
  function kitTab() {
    body.innerHTML = '<div class="dzc-layout"><nav class="dzc-side"><input type="search" placeholder="Chercher une classe…" id="dzc-q"><div id="dzc-groups"></div></nav><div id="dzc-main"><p class="dz-small">Chargement…</p></div></div>';
    data().then(function () {
      var g = body.querySelector("#dzc-groups"), main = body.querySelector("#dzc-main"), q = body.querySelector("#dzc-q");
      var keys = Object.keys(IDX);
      g.innerHTML = "<h6>Le kit</h6>" + keys.filter(function (k) { return k[0] === "c"; }).map(link).join("") + "<h6>Familles de blocs</h6>" + keys.filter(function (k) { return k[0] === "f"; }).map(link).join("");
      function link(k) { return '<a href="#" data-g="' + k + '"><span>' + esc(IDX[k].label) + '</span><span class="dz-small">' + IDX[k].names.length + "</span></a>"; }
      g.addEventListener("click", function (e) { var a = e.target.closest("[data-g]"); if (!a) return; e.preventDefault(); openGroup(a.dataset.g); });
      function openGroup(k, focus) {
        g.querySelectorAll("a").forEach(function (a) { a.classList.toggle("on", a.dataset.g === k); });
        main.innerHTML = '<p class="dz-small">Chargement…</p>';
        if (k[0] === "f") loadFam(k.slice(2));
        getJSON(D.group + k + ".json").then(function (cls) {
          var names = Object.keys(cls).sort(function (a, b) { return (DOCS.classes[b] ? 1 : 0) - (DOCS.classes[a] ? 1 : 0) || a.localeCompare(b); });
          main.innerHTML = '<h2 class="dz-h3" style="margin:0 0 1rem">' + esc(IDX[k].label) + ' <span class="dz-small">' + names.length + " classes</span></h2>";
          names.forEach(function (n) { main.appendChild(card(n, cls[n])); });
          if (focus) { var c = document.getElementById("c-" + focus); if (c) { c.scrollIntoView({ block: "start" }); c.style.outline = "2px solid var(--dz-primary)"; } }
        });
      }
      function card(n, info) {
        var doc = DOCS.classes[n] || [];
        var BASE = { "dz-btn-": '<a class="dz-btn X" href="#">Bouton</a>', "dz-card-": '<div class="dz-card X">Carte</div>', "dz-badge-": '<span class="dz-badge X">Badge</span>', "dz-icon-": '<span class="dz-icon X"><i class="fas fa-bolt"></i></span>', "dz-callout-": '<div class="dz-callout X"><div>Encadré</div></div>', "dz-grid-": '<div class="dz-grid X"><div class="dz-card">1</div><div class="dz-card">2</div><div class="dz-card">3</div><div class="dz-card">4</div></div>', "dz-section-": '<div class="X" style="padding:1rem">Section</div>', "dz-avatar-": '<span class="dz-avatar X">SD</span>' };
        var bk = Object.keys(BASE).filter(function (b) { return n.indexOf(b) === 0; })[0];
        var ex = doc[1] || (bk ? BASE[bk].replace("X", esc(n)) : '<div class="' + esc(n) + '">Exemple</div>');
        var c = el('<article class="dzc-card" id="c-' + esc(n) + '"><header><code>.' + esc(n) + "</code>" + copyBtn(n) + "</header>" + (doc[0] ? "<p>" + esc(doc[0]) + "</p>" : "") +
          '<div class="dzc-prev">' + ex + "</div>" +
          "<details><summary class=\"dz-small\">CSS derrière cette classe (" + info.rules.length + " règle" + (info.rules.length > 1 ? "s" : "") + ")</summary><pre>" + esc(info.rules.join("\n\n")) + "</pre></details></article>");
        return c;
      }
      q.addEventListener("input", function () {
        var v = q.value.trim().toLowerCase();
        if (v.length < 2) return;
        var hits = [];
        keys.forEach(function (k) { IDX[k].names.forEach(function (n) { if (n.indexOf(v) >= 0 || ((DOCS.classes[n] || [])[0] || "").toLowerCase().indexOf(v) >= 0) hits.push([n, k]); }); });
        main.innerHTML = '<h2 class="dz-h4">' + hits.length + " résultat(s)</h2>" + hits.slice(0, 300).map(function (h) { return '<a href="#" class="dz-chip" style="margin:.2rem" data-go="' + h[1] + '" data-n="' + esc(h[0]) + '">.' + esc(h[0]) + ' <span class="dz-small">' + esc(IDX[h[1]].label) + "</span></a>"; }).join("");
      });
      main.addEventListener("click", function (e) { var a = e.target.closest("[data-go]"); if (!a) return; e.preventDefault(); openGroup(a.dataset.go, a.dataset.n); });
      openGroup("c-05");
    });
  }

  /* ---------------- comportements ---------------- */
  function behTab() {
    data().then(function () {
      body.innerHTML = '<p class="dz-lead" style="font-size:1rem">Ces classes ajoutent un comportement (animation, clic…). Elles marchent dans le builder sans code : sélectionne l\'élément, champ Custom class.</p>';
      Object.keys(DOCS.behaviours).forEach(function (n) {
        var d = DOCS.behaviours[n];
        body.appendChild(el('<article class="dzc-card"><header><code>' + esc(n) + "</code>" + copyBtn(n) + "</header><p>" + esc(d[0]) + "</p>" + (d[1] ? '<div class="dzc-prev">' + d[1] + "</div>" : "") + "</article>"));
      });
      if (window.DZ && window.DZ.init) window.DZ.init(body);
    });
  }

  /* ---------------- mes classes : éditeur ---------------- */
  var TOK = [["", "—"], ["var(--dz-text)", "Texte"], ["var(--dz-text-soft)", "Texte doux"], ["var(--dz-text-mute)", "Texte discret"], ["var(--dz-bg)", "Fond de page"], ["var(--dz-surface)", "Surface"], ["var(--dz-surface-2)", "Surface 2"], ["var(--dz-primary)", "Principale"], ["var(--dz-primary-soft)", "Principale douce"], ["var(--dz-on-primary)", "Sur principale"], ["var(--dz-accent)", "Accent"], ["var(--dz-accent-2)", "Accent 2"], ["var(--dz-success)", "Succès"], ["var(--dz-warning)", "Attention"], ["var(--dz-danger)", "Danger"], ["var(--dz-info)", "Info"], ["var(--dz-border)", "Bordure"], ["transparent", "Transparent"], ["custom", "Autre couleur…"]];
  var BG = TOK.slice(0, -1).concat([["var(--dz-gradient)", "Dégradé du thème"], ["var(--dz-glass)", "Verre"], ["custom", "Autre couleur…"]]);
  var F = [
    ["Couleurs", [["color", "Couleur du texte", "tok", TOK], ["background", "Fond", "tok", BG], ["border-color", "Couleur de bordure", "tok", TOK]]],
    ["Texte", [["font-family", "Police", "sel", [["", "—"], ["var(--dz-font-heading)", "Titres"], ["var(--dz-font-body)", "Texte"], ["var(--dz-font-mono)", "Mono"]]], ["font-size", "Taille", "num", [0.6, 6, 0.05, "rem"]], ["font-weight", "Graisse", "sel", [["", "—"], ["300", "Fine"], ["400", "Normale"], ["500", "Moyenne"], ["600", "Demi-gras"], ["700", "Gras"], ["800", "Très gras"]]], ["line-height", "Interligne", "num", [0.8, 2.4, 0.05, ""]], ["letter-spacing", "Espacement lettres", "num", [-0.08, 0.3, 0.01, "em"]], ["text-transform", "Casse", "sel", [["", "—"], ["uppercase", "MAJUSCULES"], ["lowercase", "minuscules"], ["capitalize", "Initiales"]]], ["text-align", "Alignement", "sel", [["", "—"], ["left", "Gauche"], ["center", "Centre"], ["right", "Droite"]]]]],
    ["Espacements", [["padding", "Marge intérieure", "num", [0, 8, 0.25, "rem"]], ["margin", "Marge extérieure", "num", [-4, 8, 0.25, "rem"]], ["gap", "Espace entre enfants", "num", [0, 6, 0.25, "rem"]]]],
    ["Bordure et forme", [["border-width", "Épaisseur", "num", [0, 12, 1, "px"]], ["border-style", "Style", "sel", [["", "—"], ["solid", "Pleine"], ["dashed", "Tirets"], ["dotted", "Points"]]], ["border-radius", "Arrondi", "sel", [["", "—"], ["0", "Aucun"], ["var(--dz-radius-sm)", "Petit"], ["var(--dz-radius)", "Moyen"], ["var(--dz-radius-lg)", "Grand"], ["var(--dz-radius-pill)", "Pilule / cercle"]]], ["box-shadow", "Ombre", "sel", [["", "—"], ["none", "Aucune"], ["var(--dz-shadow-xs)", "Très légère"], ["var(--dz-shadow-sm)", "Légère"], ["var(--dz-shadow)", "Moyenne"], ["var(--dz-shadow-lg)", "Forte"], ["var(--dz-shadow-glow)", "Halo"]]], ["opacity", "Opacité", "num", [0, 1, 0.05, ""]]]],
    ["Disposition", [["display", "Affichage", "sel", [["", "—"], ["block", "Bloc"], ["flex", "En ligne (flex)"], ["grid", "Grille"], ["inline-flex", "En ligne, largeur du contenu"], ["inline-block", "Dans le texte"], ["none", "Caché"]]], ["flex-direction", "Sens (flex)", "sel", [["", "—"], ["row", "Horizontal"], ["column", "Vertical"]]], ["align-items", "Alignement vertical", "sel", [["", "—"], ["flex-start", "Haut"], ["center", "Centre"], ["flex-end", "Bas"], ["stretch", "Étiré"]]], ["justify-content", "Répartition", "sel", [["", "—"], ["flex-start", "Début"], ["center", "Centre"], ["flex-end", "Fin"], ["space-between", "Espacé"]]], ["flex-wrap", "Retour à la ligne", "sel", [["", "—"], ["wrap", "Oui"], ["nowrap", "Non"]]], ["grid-cols", "Colonnes (grille)", "num", [1, 8, 1, ""]]]],
    ["Taille", [["width", "Largeur", "sel", [["", "—"], ["100%", "Toute la largeur"], ["auto", "Automatique"], ["fit-content", "Celle du contenu"]]], ["max-width", "Largeur max", "num", [0, 1600, 10, "px"]], ["min-height", "Hauteur min", "num", [0, 1000, 10, "px"]]]],
    ["Effets et animations", [["hover", "Au survol", "sel", [["", "Rien"], ["lift", "Se soulève"], ["scale", "Grossit un peu"], ["glow", "Halo"], ["tint", "Se teinte"]]], ["enter", "Apparition au défilement", "sel", [["", "Aucune"], ["up", "Monte"], ["fade", "Fondu"], ["zoom", "Zoom"], ["blur", "Flou → net"], ["left", "Depuis la gauche"], ["right", "Depuis la droite"]]], ["loop", "En boucle", "sel", [["", "Aucune"], ["float", "Flotte"], ["pulse", "Pulse"], ["spin", "Tourne"], ["glow", "Halo qui respire"]]]]],
    ["Sur mobile", [["m-font-size", "Taille du texte", "num", [0.6, 5, 0.05, "rem"]], ["m-padding", "Marge intérieure", "num", [0, 6, 0.25, "rem"]], ["m-cols", "Colonnes (grille)", "num", [1, 4, 1, ""]], ["m-hide", "Cacher sur mobile", "chk"]]],
    ["En thème sombre", [["d-color", "Couleur du texte", "tok", TOK], ["d-background", "Fond", "tok", BG]]],
  ];
  function num(v, u) { return v === "" || v == null ? "" : v + u; }
  function gen(s) {
    var out = [], hov = [], mob = [], dark = [], anims = [], tl = [], rng = [];
    F.forEach(function (g) { g[1].forEach(function (f) {
      var k = f[0], v = s[k];
      if (v === "" || v == null || v === false) return;
      if (f[2] === "num") v = num(v, f[3][3]);
      if (/^(m-|d-)/.test(k) || /^(hover|enter|loop|grid-cols)$/.test(k)) return;
      out.push(k + ": " + v + ";");
    }); });
    if (s["grid-cols"]) out.push("grid-template-columns: repeat(" + s["grid-cols"] + ", minmax(0, 1fr));");
    if (s["border-width"] && !s["border-style"]) out.push("border-style: solid;");
    if (s.hover) {
      out.push("transition: transform .25s var(--dz-ease), box-shadow .25s var(--dz-ease), background .25s;");
      hov.push({ lift: "transform: translateY(-4px); box-shadow: var(--dz-shadow-lg);", scale: "transform: scale(1.03);", glow: "box-shadow: var(--dz-shadow-glow);", tint: "background: var(--dz-primary-soft);" }[s.hover]);
    }
    if (s.enter) { anims.push("dz-rv-" + s.enter + " linear both"); tl.push("view()"); rng.push("entry 0% cover 30%"); }
    if (s.loop) { anims.push({ float: "dz-k-float 4s ease-in-out infinite", pulse: "dz-k-pulse 2.4s ease-in-out infinite", spin: "dz-k-spin 8s linear infinite", glow: "dz-k-glow 2.4s ease-in-out infinite" }[s.loop]); tl.push("auto"); rng.push("normal"); }
    if (anims.length) { out.push("animation: " + anims.join(", ") + ";"); if (s.enter) out.push("animation-timeline: " + tl.join(", ") + ";", "animation-range: " + rng.join(", ") + ";"); }
    if (s["m-font-size"]) mob.push("font-size: " + s["m-font-size"] + "rem;");
    if (s["m-padding"] !== "" && s["m-padding"] != null) mob.push("padding: " + s["m-padding"] + "rem;");
    if (s["m-cols"]) mob.push("grid-template-columns: repeat(" + s["m-cols"] + ", minmax(0, 1fr));");
    if (s["m-hide"]) mob.push("display: none;");
    if (s["d-color"]) dark.push("color: " + s["d-color"] + ";");
    if (s["d-background"]) dark.push("background: " + s["d-background"] + ";");
    var css = out.join("\n");
    if (hov.length) css += "\n&:hover { " + hov.join(" ") + " }";
    if (mob.length) css += "\n@media (max-width: 767.98px) { " + mob.join(" ") + " }";
    if (dark.length) css += '\n[data-bs-theme="dark"] & { ' + dark.join(" ") + " }";
    return css;
  }
  var SAMPLES = {
    texte: '<p style="margin:0">Un texte d\'exemple pour juger la classe.</p>',
    titre: "Grand titre",
    bouton: "Bouton",
    carte: '<b>Carte</b><br><span class="dz-small">Un peu de contenu à l\'intérieur.</span>',
    grille: "<div class=\"dz-card\">1</div><div class=\"dz-card\">2</div><div class=\"dz-card\">3</div><div class=\"dz-card\">4</div>",
  };
  function mineTab() {
    var cur = D.mine.find(function (m) { return String(m.id) === String(D.edit); }) || { id: "", name: "", description: "", category: "", css: "", style: "" };
    var st = {};
    try { st = cur.style ? JSON.parse(cur.style) : {}; } catch (e) { st = {}; }
    var mode = cur.css && !cur.style ? "code" : "visual";
    body.innerHTML = '<div class="dzc-ed"><div>' +
      '<div class="dzc-mylist">' + D.mine.map(function (m) { return '<a href="?tab=mine&edit=' + m.id + '"' + (String(m.id) === String(cur.id) ? ' class="on"' : "") + "><code>." + esc(m.name) + '</code><span class="dz-small">' + esc(m.category) + "</span></a>"; }).join("") +
      '<a href="?tab=mine"><span><i class="fas fa-plus"></i> Nouvelle classe</span></a></div>' +
      '<form method="post" action="/dysizz-ui/classes/save" class="dzc-f" id="dzc-form"><input type="hidden" name="_csrf" value="' + esc(D.csrf) + '"><input type="hidden" name="id" value="' + esc(cur.id) + '"><input type="hidden" name="style_json"><input type="hidden" name="css">' +
      '<label>Nom de la classe (sans point)<input name="name" required pattern="[a-z][a-z0-9\\-]{1,40}" placeholder="ma-carte-promo" value="' + esc(cur.name) + '"></label>' +
      '<label>À quoi elle sert<input name="description" value="' + esc(cur.description) + '" placeholder="Carte de promotion avec fond dégradé"></label>' +
      '<label>Catégorie<input name="category" value="' + esc(cur.category) + '" placeholder="cartes, textes, boutons…"></label>' +
      '<div class="dz-cluster" style="--dz-gap:.4rem"><button type="button" class="dzc-mini" data-mode="visual">Visuel (sans code)</button><button type="button" class="dzc-mini" data-mode="code">Code CSS</button></div>' +
      '<div id="dzc-visual"></div><div id="dzc-code" hidden><label>CSS de la classe (imbrication permise : <code>&amp;:hover{…}</code>, <code>h2{…}</code>, <code>@media …{…}</code>)<textarea id="dzc-css" rows="14" spellcheck="false" style="font:13px/1.5 var(--dz-font-mono)"></textarea></label></div>' +
      '<div class="dz-cluster"><button class="dz-btn" type="submit"><i class="fas fa-save"></i> Enregistrer</button></div></form>' +
      (cur.id ? '<form method="post" action="/dysizz-ui/classes/delete" onsubmit="return confirm(\'Supprimer cette classe ? Les éléments qui l\\\'utilisent perdront ce style.\')" style="margin-top:.5rem"><input type="hidden" name="_csrf" value="' + esc(D.csrf) + '"><input type="hidden" name="id" value="' + esc(cur.id) + '"><button class="dzc-mini" type="submit"><i class="fas fa-trash"></i> Supprimer</button></form>' : "") +
      '<div class="dzc-grp" style="margin-top:1.5rem"><p style="margin:.6rem 0"><b>Partager</b> entre tenants</p><div class="dz-cluster"><a class="dzc-mini" href="/dysizz-ui/classes/export">Exporter mes classes</a></div>' +
      '<form method="post" action="/dysizz-ui/classes/import" class="dzc-f" style="margin-top:.6rem"><input type="hidden" name="_csrf" value="' + esc(D.csrf) + '"><textarea name="json" rows="3" placeholder="Colle ici un export de classes (JSON)" required></textarea><button class="dzc-mini" type="submit">Importer</button></form></div>' +
      '</div><div class="dzc-stage"><div class="dz-cluster" style="--dz-gap:.3rem">' + Object.keys(SAMPLES).map(function (k) { return '<button type="button" class="dzc-mini" data-sample="' + k + '">' + k + "</button>"; }).join("") + '</div><div class="dzc-stagebox"><div id="dzc-target"></div></div><pre class="dz-small" id="dzc-preview-css" style="white-space:pre-wrap;max-height:260px;overflow:auto;padding:.8rem;border-radius:8px;background:var(--dz-surface-2)"></pre><p class="dz-small">Dans le builder : sélectionne un élément → champ <b>Custom class</b> → tape le nom. Tu peux en mettre plusieurs, séparés par un espace.</p></div></div>';
    var form = body.querySelector("#dzc-form"), vis = body.querySelector("#dzc-visual"), code = body.querySelector("#dzc-code"), ta = body.querySelector("#dzc-css");
    var target = body.querySelector("#dzc-target"), pv = body.querySelector("#dzc-preview-css");
    var live = document.getElementById("dzc-live") || document.head.appendChild(el('<style id="dzc-live"></style>'));
    vis.innerHTML = F.map(function (g, gi) {
      return '<details class="dzc-grp"' + (gi < 2 ? " open" : "") + "><summary>" + g[0] + "</summary>" + g[1].map(function (f) {
        var k = f[0], v = st[k] == null ? "" : st[k], ctl;
        if (f[2] === "sel" || f[2] === "tok") {
          var isCustom = f[2] === "tok" && v && !f[3].some(function (o) { return o[0] === v; });
          ctl = '<select data-k="' + k + '">' + f[3].map(function (o) { return '<option value="' + esc(o[0]) + '"' + ((isCustom ? o[0] === "custom" : o[0] === v) ? " selected" : "") + ">" + esc(o[1]) + "</option>"; }).join("") + "</select>" + (f[2] === "tok" ? '<input type="color" data-c="' + k + '" value="' + (isCustom ? esc(v) : "#888888") + '"' + (isCustom ? "" : " hidden") + ">" : "");
        } else if (f[2] === "num") {
          ctl = '<input type="range" data-k="' + k + '" min="' + f[3][0] + '" max="' + f[3][1] + '" step="' + f[3][2] + '" value="' + (v === "" ? f[3][0] : v) + '" data-set="' + (v === "" ? "" : "1") + '"><span class="dzc-out">' + (v === "" ? "—" : v + f[3][3]) + '</span><button type="button" class="dzc-mini" data-clear="' + k + '" title="Effacer">×</button>';
        } else ctl = '<input type="checkbox" data-k="' + k + '"' + (v ? " checked" : "") + ">";
        return '<div class="dzc-row"><span>' + f[1] + '</span><span class="dzc-val">' + ctl + "</span></div>";
      }).join("") + "</details>";
    }).join("");
    function readVisual() {
      var s = {};
      vis.querySelectorAll("[data-k]").forEach(function (c) {
        var k = c.dataset.k;
        if (c.type === "checkbox") s[k] = c.checked;
        else if (c.type === "range") s[k] = c.dataset.set ? c.value : "";
        else if (c.value === "custom") s[k] = vis.querySelector('[data-c="' + k + '"]').value;
        else s[k] = c.value;
      });
      return s;
    }
    function name() { return (form.name.value || "ma-classe").replace(/[^a-z0-9-]/g, "") || "ma-classe"; }
    function css() { return mode === "visual" ? gen(readVisual()) : ta.value; }
    var sample = "carte";
    function draw() {
      var c = css();
      live.textContent = "." + name() + "{" + c + "}";
      pv.textContent = "." + name() + " {\n" + c.split("\n").map(function (l) { return "  " + l; }).join("\n") + "\n}";
      target.className = name() + (sample === "titre" ? " dz-h2" : sample === "bouton" ? " dz-btn" : sample === "carte" ? " dz-card" : "");
      target.style.cssText = sample === "grille" ? "width:100%" : "";
      target.innerHTML = SAMPLES[sample];
    }
    function setMode(m) {
      if (m === "code" && mode === "visual") ta.value = gen(readVisual());
      if (m === "visual" && mode === "code" && ta.value && ta.value !== gen(readVisual()) && !confirm("Revenir au visuel remplace le CSS écrit à la main par celui des réglages visuels. Continuer ?")) return;
      mode = m;
      vis.hidden = m !== "visual"; code.hidden = m !== "code";
      body.querySelectorAll("[data-mode]").forEach(function (b) { b.classList.toggle("dz-active", b.dataset.mode === m); b.style.borderColor = b.dataset.mode === m ? "var(--dz-primary)" : ""; });
      draw();
    }
    ta.value = cur.css || "";
    body.addEventListener("click", function (e) {
      var t = e.target.closest("[data-mode],[data-sample],[data-clear]");
      if (!t) return;
      if (t.dataset.mode) setMode(t.dataset.mode);
      if (t.dataset.sample) { sample = t.dataset.sample; draw(); }
      if (t.dataset.clear) { var r = vis.querySelector('[data-k="' + t.dataset.clear + '"]'); r.dataset.set = ""; r.nextElementSibling.textContent = "—"; draw(); }
    });
    vis.addEventListener("input", function (e) {
      var c = e.target;
      if (c.type === "range") { c.dataset.set = "1"; var f = null; F.forEach(function (g) { g[1].forEach(function (x) { if (x[0] === c.dataset.k) f = x; }); }); c.nextElementSibling.textContent = c.value + f[3][3]; }
      if (c.tagName === "SELECT" && c.nextElementSibling && c.nextElementSibling.dataset.c !== undefined) c.nextElementSibling.hidden = c.value !== "custom";
      draw();
    });
    vis.addEventListener("change", draw);
    ta.addEventListener("input", draw);
    form.name.addEventListener("input", draw);
    form.addEventListener("submit", function () { form.css.value = css(); form.style_json.value = mode === "visual" ? JSON.stringify(readVisual()) : ""; });
    setMode(mode);
  }

  show(["kit", "beh", "mine"].indexOf(D.tab) >= 0 ? D.tab : "kit");
})();
