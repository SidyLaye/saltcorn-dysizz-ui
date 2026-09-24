/* dysizz-ui — atelier de blocs : éditeur visuel (sans code) + code, aperçu en direct */
(function () {
  var D = JSON.parse(document.getElementById("dza-data").textContent);
  var app = document.getElementById("dza-app");
  var cur = D.cur;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function el(h) { var t = document.createElement("template"); t.innerHTML = h.trim(); return t.content.firstChild; }
  function slug(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "bloc"; }

  document.head.appendChild(el("<style>" +
    ".dza{display:grid;grid-template-columns:380px minmax(0,1fr);gap:1rem;align-items:start;margin-top:1rem}" +
    ".dza-panel{position:sticky;top:.5rem;max-height:calc(100vh - 1rem);overflow:auto;display:grid;gap:.7rem;padding-right:.2rem}" +
    ".dza-box{border:1px solid var(--dz-border);border-radius:12px;background:var(--dz-surface);padding:.8rem}" +
    ".dza-box h4{margin:0 0 .5rem;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--dz-text-mute)}" +
    ".dza input,.dza select,.dza textarea{width:100%;padding:.45rem .6rem;border:1px solid var(--dz-border);border-radius:8px;background:var(--dz-bg);color:var(--dz-text);font-size:.85rem}" +
    ".dza textarea{font:12.5px/1.5 var(--dz-font-mono);tab-size:2}" +
    ".dza label{display:grid;gap:.2rem;font-size:.78rem;color:var(--dz-text-soft);margin-top:.45rem}" +
    ".dza-tabs{display:flex;gap:.25rem}.dza-tabs button,.dza-b{border:1px solid var(--dz-border);background:var(--dz-surface);color:var(--dz-text-soft);border-radius:8px;padding:.35rem .6rem;font-size:.8rem;cursor:pointer}" +
    ".dza-tabs button.on,.dza-b.on{border-color:var(--dz-primary);color:var(--dz-text)}.dza-b:hover{color:var(--dz-text)}" +
    ".dza-pal{display:grid;grid-template-columns:repeat(3,1fr);gap:.35rem}.dza-pal button{display:grid;justify-items:center;gap:.25rem;padding:.55rem .2rem;border:1px solid var(--dz-border);border-radius:8px;background:var(--dz-bg);color:var(--dz-text-soft);font-size:.7rem;cursor:grab}" +
    ".dza-pal button:hover{border-color:var(--dz-primary);color:var(--dz-text)}.dza-pal i{font-size:1rem}" +
    ".dza-path{display:flex;flex-wrap:wrap;gap:.2rem}.dza-path button{font:11px var(--dz-font-mono);padding:.15rem .4rem;border-radius:5px;border:1px solid var(--dz-border);background:none;color:var(--dz-text-soft)}" +
    ".dza-chips{display:flex;flex-wrap:wrap;gap:.25rem;margin:.3rem 0}.dza-chip{display:inline-flex;gap:.3rem;align-items:center;font:12px var(--dz-font-mono);padding:.15rem .45rem;border-radius:6px;background:var(--dz-surface-2)}.dza-chip button{border:0;background:none;color:var(--dz-text-mute);padding:0;cursor:pointer}" +
    ".dza-row{display:grid;grid-template-columns:1fr 1fr;gap:.4rem}.dza-acts{display:flex;flex-wrap:wrap;gap:.25rem}" +
    ".dza-stage{display:grid;gap:.5rem}.dza-bar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem;align-items:center}" +
    ".dza-frame{width:100%;height:calc(100vh - 7rem);min-height:520px;border:1px solid var(--dz-border);border-radius:12px;background:var(--dz-bg);transition:width .3s}" +
    ".dza-frame.m{width:390px;max-width:100%;margin-inline:auto;display:block}" +
    ".dza-hint{font-size:.78rem;color:var(--dz-text-mute);margin:.3rem 0 0}" +
    "@media (max-width:980px){.dza{grid-template-columns:1fr}.dza-panel{position:static;max-height:none}}" +
    "</style>"));

  if (D.ok) app.appendChild(el('<div class="dz-callout dz-callout-success"><div>' + esc(D.ok) + "</div></div>"));
  if (D.err) app.appendChild(el('<div class="dz-callout dz-callout-danger"><div>' + esc(D.err) + "</div></div>"));

  var wrapOpts = Object.keys(D.wraps).map(function (k) { return '<option value="' + k + '"' + (k === cur.wrap ? " selected" : "") + ">" + esc(D.wraps[k]) + "</option>"; }).join("");
  var root = el('<form class="dza" method="post" action="/dysizz-ui/blocks/save" id="dza-form">' +
    '<input type="hidden" name="_csrf" value="' + esc(D.csrf) + '"><input type="hidden" name="id" value="' + esc(cur.id) + '">' +
    '<div class="dza-panel">' +
    '<div class="dza-box"><div class="dza-row"><label>Nom du bloc<input name="name" required maxlength="80" value="' + esc(cur.name) + '" placeholder="Mon · Bandeau promo"></label><label>Icône<input name="icon" value="' + esc(cur.icon) + '"></label></div>' +
    '<label>Enveloppe<select name="wrap">' + wrapOpts + "</select></label>" +
    '<div class="dza-acts" style="margin-top:.6rem"><button class="dz-btn dz-btn-sm" type="submit"><i class="fas fa-save"></i> ' + (cur.id ? "Enregistrer" : "Ajouter à la Library") + "</button>" + (cur.id ? '<button class="dz-btn dz-btn-sm dz-btn-ghost" type="submit" name="as_new" value="1">Copie</button><a class="dz-btn dz-btn-sm dz-btn-ghost" href="/dysizz-ui/blocks">Nouveau</a>' : "") + "</div></div>" +
    '<div class="dza-tabs"><button type="button" data-tab="visual" class="on">Visuel</button><button type="button" data-tab="code">Code</button><button type="button" data-tab="blocks">Mes blocs</button></div>' +
    '<div data-pane="visual"><div class="dza-box" id="dza-insp"></div><div class="dza-box"><h4>Ajouter</h4><div class="dza-pal" id="dza-pal"></div><p class="dza-hint">Ajouté après l\'élément sélectionné (ou dedans s\'il est vide). Double-clic sur un texte de l\'aperçu pour l\'écrire directement.</p></div></div>' +
    '<div data-pane="code" hidden><div class="dza-box"><label>HTML<textarea name="html" rows="16" spellcheck="false"></textarea></label><label>CSS du bloc (limité au bloc ; <code>h2{…}</code>, <code>&amp;:hover{…}</code>)<textarea name="css" rows="8" spellcheck="false"></textarea></label><label>JS (optionnel, <code>el</code> = le bloc)<textarea name="js" rows="5" spellcheck="false"></textarea></label></div></div>' +
    '<div data-pane="blocks" hidden><div class="dza-box"><h4>Mes blocs</h4><div id="dza-mine"></div></div><div class="dza-box"><h4>Partir d\'un bloc du kit</h4><select id="dza-from"><option value="">— choisir —</option>' + D.kit.map(function (k) { return '<option value="' + k.id + '">' + esc(k.name) + "</option>"; }).join("") + '</select><p class="dza-hint">Copie le bloc dans l\'atelier ; l\'original ne change pas.</p></div>' +
    '<div class="dza-box"><h4>Partager</h4><div class="dza-acts"><a class="dza-b" href="/dysizz-ui/blocks/export">Exporter mes blocs</a><a class="dza-b" href="/dysizz-ui/blocks/export?all=1">Toute la Library</a></div></div></div>' +
    "</div>" +
    '<div class="dza-stage"><div class="dza-bar"><div class="dza-acts"><button type="button" class="dza-b" data-undo title="Annuler (Ctrl Z)"><i class="fas fa-undo"></i></button><button type="button" class="dza-b" data-redo title="Rétablir (Ctrl Y)"><i class="fas fa-redo"></i></button><button type="button" class="dza-b on" data-live="edit">Édition</button><button type="button" class="dza-b" data-live="play">Aperçu animé</button></div>' +
    '<div class="dza-acts"><button type="button" class="dza-b on" data-w="d"><i class="fas fa-desktop"></i></button><button type="button" class="dza-b" data-w="m"><i class="fas fa-mobile-alt"></i></button><button type="button" class="dza-b" data-theme><i class="fas fa-adjust"></i></button></div></div>' +
    '<iframe class="dza-frame" id="dza-frame" title="Aperçu du bloc"></iframe></div></form>');
  app.appendChild(root);
  var F = root, frame = root.querySelector("#dza-frame"), insp = root.querySelector("#dza-insp");
  F.html.value = cur.html || ""; F.css.value = cur.css || ""; F.js.value = cur.js || "";
  if (!F.html.value.trim()) F.html.value = '<div class="dz-section-head"><span class="dz-eyebrow">Sur-titre</span><h2 class="dz-h2">Ton titre ici</h2><p class="dz-lead">Clique sur un élément pour le modifier, ou ajoute des éléments depuis la palette.</p></div>';

  /* ------------- aperçu ------------- */
  var mode = "edit", dark = null, doc = null, sel = null, hist = [F.html.value], hi = 0;
  var head = [].slice.call(document.querySelectorAll('link[rel=stylesheet],head style')).filter(function (n) { return n.id !== "dzc-live"; }).map(function (n) { return n.outerHTML; }).join("") +
    '<link rel="stylesheet" href="' + D.dzjs.replace(/dz\.js$/, "dz-builder.css") + '">';
  var de = document.documentElement;
  function attrs() {
    var a = [].slice.call(de.attributes).filter(function (x) { return !/^(style|class|data-dz-motion|data-bs-theme)$/.test(x.name); }).map(function (x) { return x.name + '="' + esc(x.value) + '"'; });
    var theme = dark === null ? de.getAttribute("data-bs-theme") || "light" : dark ? "dark" : "light";
    a.push('data-bs-theme="' + theme + '"', 'data-dz-motion="' + (mode === "edit" ? "off" : "on") + '"', 'class="' + esc((de.className || "").replace(/\bdz-builder\b/, "")) + '"');
    return a.join(" ");
  }
  function draw() {
    var cls = "dzb-" + slug(F.name.value), w = F.wrap.value, inner = '<div class="' + cls + '" id="dza-root">' + F.html.value + "</div>";
    if (w === "section") inner = '<section class="dz-section"><div class="dz-container">' + inner + "</div></section>";
    if (w === "full") inner = '<section class="dz-section dz-flush">' + inner + "</section>";
    var css = F.css.value.trim() ? "<style>." + cls + "{" + F.css.value + "}</style>" : "";
    var edit = mode === "edit" ? "<style>[data-dza-hov]{outline:1px dashed #3b82f6!important;outline-offset:1px}[data-dza-sel]{outline:2px solid #3b82f6!important;outline-offset:2px}[contenteditable]{outline:2px solid #f59e0b!important;cursor:text}#dza-root{min-height:80px}#dza-root:empty::before{content:'Bloc vide : ajoute des éléments depuis la palette';display:block;padding:2rem;text-align:center;opacity:.6}</style>" : "";
    var js = mode === "play" ? '<script src="' + D.dzjs + '"><\/script>' + (F.js.value.trim() ? '<script>document.querySelectorAll(".' + cls + '").forEach(function(el){try{' + F.js.value + "\n}catch(e){console.error(e)}});<\/script>" : "") : "";
    frame.srcdoc = "<!doctype html><html " + attrs() + '><head><meta name="viewport" content="width=device-width,initial-scale=1">' + head + "<style>body{margin:0;padding:0}</style>" + edit + "</head><body>" + css + inner + js + "</body></html>";
  }
  frame.addEventListener("load", function () {
    doc = frame.contentDocument; sel = null; renderInsp();
    if (mode !== "edit") return;
    doc.addEventListener("mouseover", function (e) { var t = pick(e.target); clearAttr("data-dza-hov"); if (t) t.setAttribute("data-dza-hov", ""); });
    doc.addEventListener("mouseleave", function () { clearAttr("data-dza-hov"); });
    doc.addEventListener("click", function (e) { if (e.target.closest("[contenteditable]")) return; e.preventDefault(); select(pick(e.target)); }, true);
    doc.addEventListener("dblclick", function (e) { var t = pick(e.target); if (t && textLike(t)) editText(t); });
    doc.addEventListener("keydown", keys);
  });
  function rootEl() { return doc && doc.getElementById("dza-root"); }
  function pick(t) { var r = rootEl(); if (!r || !t || !r.contains(t) || t === r) return null; return t.nodeType === 1 ? t : t.parentElement; }
  function clearAttr(a) { if (doc) doc.querySelectorAll("[" + a + "]").forEach(function (n) { n.removeAttribute(a); }); }
  var INLINE = /^(A|ABBR|B|BR|CODE|EM|I|KBD|MARK|S|SMALL|SPAN|STRONG|SUB|SUP|TIME|U)$/;
  function textLike(n) { if (/^(IMG|SVG|VIDEO|IFRAME|INPUT|SELECT|TEXTAREA)$/.test(n.tagName)) return false; for (var c = n.firstElementChild; c; c = c.nextElementSibling) { if (!INLINE.test(c.tagName) || !textLike(c)) return false; } return /\S/.test(n.textContent); }

  /* ------------- synchronisation + historique ------------- */
  function serialize() {
    var c = rootEl().cloneNode(true);
    c.querySelectorAll("[data-dza-sel],[data-dza-hov],[contenteditable]").forEach(function (n) { n.removeAttribute("data-dza-sel"); n.removeAttribute("data-dza-hov"); n.removeAttribute("contenteditable"); n.removeAttribute("spellcheck"); if (!n.getAttribute("style")) n.removeAttribute("style"); });
    return c.innerHTML;
  }
  function commit() { if (!rootEl()) return; F.html.value = serialize(); if (hist[hi] !== F.html.value) { hist = hist.slice(0, hi + 1); hist.push(F.html.value); if (hist.length > 80) hist.shift(); hi = hist.length - 1; } }
  function travel(d) { var n = hi + d; if (n < 0 || n >= hist.length) return; hi = n; F.html.value = hist[hi]; draw(); }

  /* ------------- sélection + inspecteur ------------- */
  function select(n) { clearAttr("data-dza-sel"); sel = n; if (n) n.setAttribute("data-dza-sel", ""); renderInsp(); }
  var TOK = [["", "—"], ["var(--dz-text)", "Texte"], ["var(--dz-text-soft)", "Texte doux"], ["var(--dz-text-mute)", "Discret"], ["var(--dz-bg)", "Fond page"], ["var(--dz-surface)", "Surface"], ["var(--dz-surface-2)", "Surface 2"], ["var(--dz-primary)", "Principale"], ["var(--dz-primary-soft)", "Principale douce"], ["var(--dz-on-primary)", "Sur principale"], ["var(--dz-accent)", "Accent"], ["var(--dz-success)", "Succès"], ["var(--dz-warning)", "Attention"], ["var(--dz-danger)", "Danger"], ["var(--dz-gradient)", "Dégradé"], ["transparent", "Transparent"]];
  var ANIM = [["", "Aucune"], ["dz-reveal", "Monte"], ["dz-reveal-fade", "Fondu"], ["dz-reveal-zoom", "Zoom"], ["dz-reveal-blur", "Flou → net"], ["dz-reveal-left", "Depuis la gauche"], ["dz-reveal-right", "Depuis la droite"], ["dz-reveal-flip", "Bascule"]];
  function opts(list, v) { return list.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (o[0] === v ? " selected" : "") + ">" + esc(o[1]) + "</option>"; }).join(""); }
  function renderInsp() {
    if (!sel) { insp.innerHTML = '<h4>Élément</h4><p class="dza-hint">Clique sur un élément dans l\'aperçu' + (mode === "play" ? " (repasse en mode Édition)" : "") + ".</p>"; return; }
    var n = sel, path = [], p = n;
    while (p && p.id !== "dza-root") { path.unshift(p); p = p.parentElement; }
    var cls = [].slice.call(n.classList);
    var st = n.style;
    var anim = (cls.filter(function (c) { return /^dz-reveal(-|$)/.test(c); })[0]) || "";
    var h = "<h4>" + esc(n.tagName.toLowerCase()) + '</h4><div class="dza-path">' + path.map(function (x, i) { return '<button type="button" data-path="' + i + '">' + esc(x.tagName.toLowerCase() + (x.classList[0] ? "." + x.classList[0] : "")) + "</button>"; }).join("›") + "</div>";
    if (textLike(n)) h += '<label>Texte (le gras &lt;b&gt; et l\'italique &lt;em&gt; sont gardés)<textarea data-f="text" rows="3">' + esc(n.innerHTML) + "</textarea></label>";
    if (n.tagName === "A") h += '<label>Lien (adresse)<input data-f="href" value="' + esc(n.getAttribute("href") || "") + '" placeholder="/page/contact ou https://…"></label><label style="display:flex;gap:.4rem;align-items:center"><input type="checkbox" data-f="blank" style="width:auto"' + (n.target === "_blank" ? " checked" : "") + "> ouvrir dans un nouvel onglet</label>";
    if (n.tagName === "IMG") h += '<label>Image (adresse)<input data-f="src" value="' + esc(n.getAttribute("src") || "") + '"></label><label>Texte alternatif<input data-f="alt" value="' + esc(n.getAttribute("alt") || "") + '"></label><p class="dza-hint">Téléverse l\'image dans Saltcorn (Fichiers), puis colle son adresse /files/serve/…</p>';
    var icon = n.tagName === "I" ? n : n.querySelector(":scope > i[class*='fa-']");
    if (icon) h += '<label>Icône (Font Awesome 5, ex. fas fa-star)<input data-f="icon" value="' + esc(icon.className) + '"></label>';
    h += '<label>Classes</label><div class="dza-chips">' + cls.map(function (c) { return '<span class="dza-chip">' + esc(c) + '<button type="button" data-rmc="' + esc(c) + '">×</button></span>'; }).join("") + '</div><input data-f="addc" list="dza-classes" placeholder="+ ajouter une classe (Entrée)">';
    h += '<div class="dza-row"><label>Couleur du texte<select data-s="color">' + opts(TOK, st.color) + '</select></label><label>Fond<select data-s="background">' + opts(TOK, st.background) + "</select></label></div>";
    h += '<div class="dza-row"><label>Marge intérieure<select data-s="padding">' + opts([["", "—"], ["0", "0"], [".5rem", "Petite"], ["1rem", "Moyenne"], ["2rem", "Grande"], ["3rem", "Très grande"]], st.padding) + '</select></label><label>Espace dessous<select data-s="margin-bottom">' + opts([["", "—"], ["0", "0"], [".5rem", "Petit"], ["1rem", "Moyen"], ["2rem", "Grand"], ["4rem", "Très grand"]], st.marginBottom) + "</select></label></div>";
    h += '<div class="dza-row"><label>Alignement<select data-s="text-align">' + opts([["", "—"], ["left", "Gauche"], ["center", "Centre"], ["right", "Droite"]], st.textAlign) + '</select></label><label>Arrondi<select data-s="border-radius">' + opts([["", "—"], ["0", "Aucun"], ["var(--dz-radius-sm)", "Petit"], ["var(--dz-radius)", "Moyen"], ["var(--dz-radius-lg)", "Grand"], ["var(--dz-radius-pill)", "Rond"]], st.borderRadius) + "</select></label></div>";
    h += '<div class="dza-row"><label>Taille du texte<select data-s="font-size">' + opts([["", "—"], [".85rem", "Petite"], ["1rem", "Normale"], ["1.25rem", "Grande"], ["2rem", "Très grande"], ["3rem", "Énorme"]], st.fontSize) + '</select></label><label>Apparition<select data-f="anim">' + opts(ANIM, anim) + "</select></label></div>";
    h += '<div class="dza-acts" style="margin-top:.7rem"><button type="button" class="dza-b" data-act="up" title="Monter"><i class="fas fa-arrow-up"></i></button><button type="button" class="dza-b" data-act="down" title="Descendre"><i class="fas fa-arrow-down"></i></button><button type="button" class="dza-b" data-act="dup" title="Dupliquer (Ctrl D)"><i class="far fa-copy"></i></button><button type="button" class="dza-b" data-act="wrap" title="Mettre dans un conteneur"><i class="far fa-square"></i></button><button type="button" class="dza-b" data-act="parent" title="Sélectionner le parent"><i class="fas fa-level-up-alt"></i></button><button type="button" class="dza-b" data-act="del" title="Supprimer (Suppr)"><i class="fas fa-trash"></i></button></div>';
    insp.innerHTML = h;
    insp._path = path;
  }
  insp.addEventListener("click", function (e) {
    var b = e.target.closest("[data-path],[data-rmc],[data-act]");
    if (!b || !sel) return;
    if (b.dataset.path) return select(insp._path[+b.dataset.path]);
    if (b.dataset.rmc) { sel.classList.remove(b.dataset.rmc); commit(); return renderInsp(); }
    act(b.dataset.act);
  });
  function act(a) {
    if (!sel) return;
    var n = sel, r = rootEl();
    if (a === "up" && n.previousElementSibling) n.parentNode.insertBefore(n, n.previousElementSibling);
    if (a === "down" && n.nextElementSibling) n.parentNode.insertBefore(n.nextElementSibling, n);
    if (a === "dup") { var c = n.cloneNode(true); c.removeAttribute("data-dza-sel"); n.after(c); select(c); }
    if (a === "wrap") { var w = doc.createElement("div"); w.className = "dz-stack"; n.before(w); w.appendChild(n); select(w); }
    if (a === "parent") { if (n.parentElement && n.parentElement !== r) select(n.parentElement); return; }
    if (a === "del") { var nx = n.nextElementSibling || n.previousElementSibling || (n.parentElement !== r ? n.parentElement : null); n.remove(); select(nx); }
    commit(); renderInsp();
  }
  insp.addEventListener("input", function (e) {
    var f = e.target.dataset.f, s = e.target.dataset.s, v = e.target.value;
    if (!sel) return;
    if (f === "text") sel.innerHTML = v;
    if (f === "href") sel.setAttribute("href", v);
    if (f === "src") sel.setAttribute("src", v);
    if (f === "alt") sel.setAttribute("alt", v);
    if (f === "icon") { var ic = sel.tagName === "I" ? sel : sel.querySelector(":scope > i[class*='fa-']"); if (ic) ic.className = v; }
    if (f === "text" || f === "href" || f === "src" || f === "alt" || f === "icon") commit();
  });
  insp.addEventListener("change", function (e) {
    var f = e.target.dataset.f, s = e.target.dataset.s, v = e.target.value;
    if (!sel) return;
    if (s) { if (v) sel.style.setProperty(s, v); else sel.style.removeProperty(s); }
    if (f === "blank") { if (e.target.checked) sel.setAttribute("target", "_blank"); else sel.removeAttribute("target"); }
    if (f === "anim") { [].slice.call(sel.classList).forEach(function (c) { if (/^dz-reveal(-|$)/.test(c)) sel.classList.remove(c); }); if (v) sel.classList.add(v); }
    if (s || f === "blank" || f === "anim") commit();
  });
  insp.addEventListener("keydown", function (e) {
    if (e.target.dataset.f === "addc" && e.key === "Enter") {
      e.preventDefault();
      e.target.value.split(/\s+/).filter(Boolean).forEach(function (c) { if (/^[A-Za-z][\w-]*$/.test(c)) sel.classList.add(c); });
      commit(); renderInsp();
      var i = insp.querySelector('[data-f="addc"]'); if (i) i.focus();
    }
  });
  function editText(n) {
    select(n);
    n.setAttribute("contenteditable", "true"); n.setAttribute("spellcheck", "false"); n.focus();
    function done() { n.removeEventListener("blur", done); n.removeAttribute("contenteditable"); n.removeAttribute("spellcheck"); commit(); renderInsp(); }
    n.addEventListener("blur", done);
  }
  function keys(e) {
    var editing = e.target && e.target.isContentEditable;
    if ((e.ctrlKey || e.metaKey) && e.key === "z" && !editing) { e.preventDefault(); travel(-1); }
    else if ((e.ctrlKey || e.metaKey) && (e.key === "y" || (e.shiftKey && e.key === "Z")) && !editing) { e.preventDefault(); travel(1); }
    else if ((e.ctrlKey || e.metaKey) && e.key === "d" && sel) { e.preventDefault(); act("dup"); }
    else if ((e.key === "Delete" || e.key === "Backspace") && sel && !editing) { e.preventDefault(); act("del"); }
    else if (e.key === "Escape") { if (editing) e.target.blur(); else select(null); }
  }
  document.addEventListener("keydown", function (e) { if (e.target.closest && e.target.closest("input,textarea,select")) return; if (mode === "edit" && doc) keys(e); });

  /* ------------- palette ------------- */
  var P = [
    ["fas fa-heading", "Titre", '<h2 class="dz-h2">Nouveau titre</h2>'],
    ["fas fa-font", "Sous-titre", '<h3 class="dz-h4">Sous-titre</h3>'],
    ["fas fa-align-left", "Paragraphe", '<p class="dz-lead">Votre texte ici.</p>'],
    ["fas fa-tag", "Sur-titre", '<span class="dz-eyebrow">Sur-titre</span>'],
    ["fas fa-hand-pointer", "Bouton", '<a class="dz-btn" href="#">Bouton</a>'],
    ["fas fa-grip-lines", "2 boutons", '<div class="dz-cluster"><a class="dz-btn" href="#">Principal</a><a class="dz-btn dz-btn-ghost" href="#">Secondaire</a></div>'],
    ["far fa-image", "Image", '<img src="https://picsum.photos/seed/atelier/1200/800" alt="Image">'],
    ["fas fa-star", "Icône", '<span class="dz-icon"><i class="fas fa-star"></i></span>'],
    ["far fa-square", "Carte", '<div class="dz-card"><h3 class="dz-h4">Titre de la carte</h3><p>Texte de la carte.</p></div>'],
    ["fas fa-th", "Grille ×3", '<div class="dz-grid dz-grid-3"><div class="dz-card"><h3 class="dz-h4">Un</h3><p>Texte.</p></div><div class="dz-card"><h3 class="dz-h4">Deux</h3><p>Texte.</p></div><div class="dz-card"><h3 class="dz-h4">Trois</h3><p>Texte.</p></div></div>'],
    ["fas fa-columns", "2 colonnes", '<div class="dz-split"><div><h2 class="dz-h2">Texte</h2><p class="dz-lead">Explication.</p></div><div><img src="https://picsum.photos/seed/split/1000/800" alt=""></div></div>'],
    ["fas fa-certificate", "Badge", '<span class="dz-badge">Nouveau</span>'],
    ["fas fa-list", "Liste", '<ul class="dz-list"><li>Premier point</li><li>Deuxième point</li><li>Troisième point</li></ul>'],
    ["fas fa-quote-left", "Citation", '<blockquote class="dz-lead" style="border-left:3px solid var(--dz-primary);padding-left:1rem;margin:0">« Une citation marquante. »</blockquote>'],
    ["fas fa-sort-numeric-up", "Chiffre animé", '<div class="dz-h1 dz-counter">1 250</div>'],
    ["far fa-square", "Conteneur", '<div class="dz-stack"></div>'],
    ["fas fa-minus", "Séparateur", '<div class="dz-divider"></div>'],
    ["fas fa-arrows-alt-v", "Espace", '<div style="height:3rem"></div>'],
  ];
  var pal = root.querySelector("#dza-pal");
  pal.innerHTML = P.map(function (x, i) { return '<button type="button" data-p="' + i + '"><i class="' + x[0] + '"></i>' + esc(x[1]) + "</button>"; }).join("");
  pal.addEventListener("click", function (e) {
    var b = e.target.closest("[data-p]"); if (!b || !doc) return;
    if (mode !== "edit") setLive("edit");
    var node = doc.createRange().createContextualFragment(P[+b.dataset.p][2]).firstChild, r = rootEl();
    if (sel && !sel.children.length && !textLike(sel) && !/^(IMG|I)$/.test(sel.tagName)) sel.appendChild(node);
    else if (sel) sel.after(node); else r.appendChild(node);
    select(node); commit();
  });

  /* ------------- onglets, barre, formulaire ------------- */
  root.querySelector(".dza-tabs").addEventListener("click", function (e) {
    var b = e.target.closest("[data-tab]"); if (!b) return;
    var leavingCode = !root.querySelector('[data-pane="code"]').hidden;
    root.querySelectorAll(".dza-tabs button").forEach(function (x) { x.classList.toggle("on", x === b); });
    root.querySelectorAll("[data-pane]").forEach(function (p) { p.hidden = p.dataset.pane !== b.dataset.tab; });
    if (leavingCode) { commitCode(); draw(); }
  });
  function commitCode() { if (hist[hi] !== F.html.value) { hist = hist.slice(0, hi + 1); hist.push(F.html.value); hi = hist.length - 1; } }
  var t;
  ["css", "js"].forEach(function (k) { F[k].addEventListener("input", function () { clearTimeout(t); t = setTimeout(draw, 400); }); });
  F.html.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { commitCode(); draw(); }, 500); });
  F.name.addEventListener("change", function () { if (F.css.value.trim() || F.js.value.trim()) { commit(); draw(); } }); F.wrap.addEventListener("change", function () { commit(); draw(); });
  function setLive(m) { mode = m; root.querySelectorAll("[data-live]").forEach(function (b) { b.classList.toggle("on", b.dataset.live === m); }); draw(); }
  root.querySelector(".dza-bar").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.hasAttribute("data-undo")) travel(-1);
    if (b.hasAttribute("data-redo")) travel(1);
    if (b.dataset.live) setLive(b.dataset.live);
    if (b.dataset.w) { frame.classList.toggle("m", b.dataset.w === "m"); root.querySelectorAll("[data-w]").forEach(function (x) { x.classList.toggle("on", x === b); }); }
    if (b.hasAttribute("data-theme")) { dark = dark === null ? de.getAttribute("data-bs-theme") !== "dark" : !dark; draw(); }
  });
  F.addEventListener("submit", function () { if (rootEl() && mode === "edit") F.html.value = serialize(); });
  root.querySelector("#dza-from").addEventListener("change", function (e) { if (e.target.value) location.href = "/dysizz-ui/blocks?from=" + e.target.value; });
  root.querySelector("#dza-mine").innerHTML = D.mine.length ? D.mine.map(function (m) {
    return '<div style="display:flex;justify-content:space-between;gap:.4rem;align-items:center;padding:.3rem 0;border-bottom:1px solid var(--dz-border)"><a href="/dysizz-ui/blocks?edit=' + m.id + '"><i class="' + esc(m.icon || "fas fa-cube") + '"></i> ' + esc(m.name) + '</a><button type="button" class="dza-b" data-del="' + m.id + '" title="Supprimer"><i class="fas fa-trash"></i></button></div>';
  }).join("") : '<p class="dza-hint">Aucun bloc perso. Crée-en un, ou dans le builder : sélectionne un élément puis Library → Add.</p>';
  root.querySelector("#dza-mine").addEventListener("click", function (e) {
    var b = e.target.closest("[data-del]"); if (!b || !confirm("Supprimer ce bloc de la Library ? (les pages qui l'utilisent ne changent pas)")) return;
    var f = el('<form method="post" action="/dysizz-ui/blocks/delete"><input type="hidden" name="_csrf" value="' + esc(D.csrf) + '"><input type="hidden" name="id" value="' + b.dataset.del + '"></form>');
    document.body.appendChild(f); f.submit();
  });
  /* autocomplétion des classes (kit + perso) */
  fetch("/dysizz-ui/classes/names", { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (d) {
    var dl = document.createElement("datalist"); dl.id = "dza-classes";
    dl.innerHTML = d.mine.concat(d.kit).map(function (x) { return '<option value="' + esc(x[0]) + '">' + esc(x[1] + (x[2] ? " — " + x[2] : "")) + "</option>"; }).join("");
    document.body.appendChild(dl);
  }).catch(function () {});
  draw();
})();
