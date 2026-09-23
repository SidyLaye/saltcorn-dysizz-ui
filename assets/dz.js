/* =====================================================================
   DYSIZZ UI — dz.js
   Petit moteur d'interactions sans dépendance. Tout se pilote par des
   classes ou attributs data-dz-* posés dans le builder Saltcorn : aucun
   code à écrire dans les pages.
   Se relance tout seul quand Saltcorn recharge un morceau de page en ajax.
   API publique : window.DZ.init(el), DZ.toast(msg, opts), DZ.confetti(),
                  DZ.setTheme("light"|"dark"|"auto")
   ===================================================================== */
(function () {
  "use strict";
  if (window.DZ && window.DZ.__loaded) return;

  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  /* réglage « Animations » : on (défaut) | system (suit le réglage du visiteur) | off */
  var motionOff = function () {
    var m = root.getAttribute("data-dz-motion");
    return m === "off" || (m === "system" && reduceMotion);
  };
  /* dans l'éditeur de pages Saltcorn : aucun moteur, tout reste visible et fixe */
  var inBuilder = root.classList.contains("dz-builder");

  root.classList.add("dz-js");
  /* apparitions gérées en CSS pur si le navigateur sait faire (pas de JS au défilement) */
  var cssReveal = !!(window.CSS && CSS.supports && CSS.supports("animation-timeline: view()"));
  var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 60); };

  /* ---------- outils ---------- */
  function $all(sel, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(sel)); }
  function once(el, key) {
    var k = "dz" + key;
    if (el.dataset[k]) return false;
    el.dataset[k] = "1";
    return true;
  }
  function withSelf(el, sel) {
    var list = $all(sel, el);
    if (el !== doc && el.matches && el.matches(sel)) list.unshift(el);
    return list;
  }
  var nf = function (decimals) {
    try { return new Intl.NumberFormat(root.lang && root.lang !== "en" ? root.lang : "fr-FR", { minimumFractionDigits: decimals, maximumFractionDigits: decimals }); }
    catch (e) { return { format: function (n) { return n.toFixed(decimals); } }; }
  };

  /* ---------- 1. apparition au défilement ---------- */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      el.classList.add("dz-in");
      if (el.hasAttribute("data-dz-count")) countUp(el);
      if (el.classList.contains("dz-progress")) {
        var bar = el.querySelector("span");
        if (bar && el.dataset.dzValue) bar.style.width = el.dataset.dzValue + "%";
      }
      if (!el.hasAttribute("data-dz-repeat")) io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }) : null;

  function initReveal(scope) {
    withSelf(scope, "[data-dz-reveal],.dz-reveal,.dz-stagger,.dz-highlight,.dz-clip,.dz-split-ready,[data-dz-count],.dz-progress[data-dz-value]").forEach(function (el) {
      if (!once(el, "Rev")) return;
      var pureReveal = !el.hasAttribute("data-dz-count") && !el.classList.contains("dz-progress") && !el.classList.contains("dz-split-ready") && !el.classList.contains("dz-highlight");
      if (el.classList.contains("dz-stagger")) Array.prototype.forEach.call(el.children, function (c, i) { c.style.setProperty("--dz-i", i); });
      if (cssReveal && pureReveal) return;
      if (el.dataset.dzDelay) el.style.setProperty("--dz-delay", (parseFloat(el.dataset.dzDelay) || 0) + "ms");
      if (el.classList.contains("dz-stagger")) {
        Array.prototype.forEach.call(el.children, function (c, i) { c.style.setProperty("--dz-i", i); });
      }
      if (el.classList.contains("dz-progress") && el.dataset.dzValue) {
        var bar = el.querySelector("span");
        if (bar) bar.style.width = "0%";
      }
      if (!io || motionOff()) {
        el.classList.add("dz-in");
        if (el.hasAttribute("data-dz-count")) countUp(el, true);
        if (el.classList.contains("dz-progress")) { var b = el.querySelector("span"); if (b) b.style.width = el.dataset.dzValue + "%"; }
      } else io.observe(el);
    });
  }

  /* ---------- 2. compteurs animés ---------- */
  function countUp(el, instant) {
    if (el.dataset.dzCounted) return;
    el.dataset.dzCounted = "1";
    var target = parseFloat(String(el.getAttribute("data-dz-count")).replace(",", "."));
    if (isNaN(target)) return;
    var decimals = parseInt(el.dataset.dzDecimals || (String(target).split(".")[1] || "").length, 10) || 0;
    var prefix = el.dataset.dzPrefix || "", suffix = el.dataset.dzSuffix || "";
    var fmt = nf(decimals);
    var dur = parseInt(el.dataset.dzDuration || "1800", 10);
    if (instant || motionOff()) { el.textContent = prefix + fmt.format(target) + suffix; return; }
    var start = performance.now();
    (function tick(now) {
      var p = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = prefix + fmt.format(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    })(start);
  }

  /* ---------- 3. texte qui s'écrit ---------- */
  function initTyped(scope) {
    withSelf(scope, "[data-dz-typed]").forEach(function (el) {
      if (!once(el, "Typed")) return;
      var words = el.getAttribute("data-dz-typed").split("|").map(function (s) { return s.trim(); }).filter(Boolean);
      if (!words.length) return;
      el.classList.add("dz-typed");
      if (motionOff()) { el.textContent = words[0]; return; }
      var w = 0, i = 0, deleting = false;
      var speed = parseInt(el.dataset.dzSpeed || "70", 10), pause = parseInt(el.dataset.dzPause || "1600", 10);
      (function step() {
        if (!doc.body.contains(el)) return;
        var word = words[w];
        el.textContent = word.slice(0, i);
        if (!deleting && i < word.length) { i++; setTimeout(step, speed); }
        else if (!deleting) { deleting = true; setTimeout(step, pause); }
        else if (i > 0) { i--; setTimeout(step, speed / 2); }
        else { deleting = false; w = (w + 1) % words.length; setTimeout(step, 300); }
      })();
    });
  }

  /* ---------- 4. halo qui suit la souris ---------- */
  function initSpotlight(scope) {
    withSelf(scope, "[data-dz-spotlight],.dz-spotlight,.dz-border-glow").forEach(function (el) {
      if (!once(el, "Spot")) return;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", (e.clientX - r.left) + "px");
        el.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  /* ---------- 5. inclinaison 3D ---------- */
  function initTilt(scope) {
    if (!finePointer) return;
    withSelf(scope, "[data-dz-tilt],.dz-tilt-on").forEach(function (el) {
      if (!once(el, "Tilt")) return;
      var max = parseFloat(el.getAttribute("data-dz-tilt")) || 8;
      el.classList.add("dz-tilt");
      el.addEventListener("pointermove", function (e) {
        if (motionOff()) return;
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(900px) rotateY(" + (x * max) + "deg) rotateX(" + (-y * max) + "deg) translateZ(0)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- 6. boutons magnétiques ---------- */
  function initMagnetic(scope) {
    if (!finePointer) return;
    withSelf(scope, ".dz-magnetic,[data-dz-magnetic]").forEach(function (el) {
      if (!once(el, "Mag")) return;
      var force = parseFloat(el.getAttribute("data-dz-magnetic")) || 0.3;
      el.addEventListener("pointermove", function (e) {
        if (motionOff()) return;
        var r = el.getBoundingClientRect();
        el.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * force) + "px," + ((e.clientY - r.top - r.height / 2) * force) + "px)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- 7. parallaxe + état de défilement ---------- */
  var parallaxEls = [];
  function initParallax(scope) {
    withSelf(scope, "[data-dz-parallax],.dz-parallax").forEach(function (el) {
      if (!once(el, "Par")) return;
      parallaxEls.push(el);
    });
  }
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset;
      root.classList.toggle("dz-scrolled", y > 12);
      /* bandeau d'annonce au-dessus de la barre fixe : la barre descend d'autant, puis remonte au défilement */
      var tb = doc.querySelector(".dz-topbar:not(.dz-dismissed)");
      root.style.setProperty("--dz-nav-top", tb ? Math.max(0, tb.getBoundingClientRect().bottom) + "px" : "0px");
      root.classList.toggle("dz-scrolled-far", y > 700);
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      root.style.setProperty("--dz-progress", h > 0 ? (y / h).toFixed(4) : 0);
      if (!motionOff()) {
        parallaxEls = parallaxEls.filter(function (el) { return doc.body.contains(el); });
        parallaxEls.forEach(function (el) {
          var speed = parseFloat(el.getAttribute("data-dz-parallax")) || 0.2;
          var r = el.getBoundingClientRect();
          var center = r.top + r.height / 2 - window.innerHeight / 2;
          el.style.transform = "translate3d(0," + (-center * speed).toFixed(1) + "px,0)";
        });
      }
      if (wordEls.length) updateWords();
      if (hscrolls.length) updateHScroll();
      ticking = false;
    });
  }

  /* ---------- 8. thème clair / sombre ---------- */
  function setTheme(mode) {
    try { localStorage.setItem("dz-theme", mode); } catch (e) {}
    var eff = mode === "auto" ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light") : mode;
    root.setAttribute("data-bs-theme", eff);
    $all("[data-dz-theme-toggle]").forEach(function (b) { b.setAttribute("aria-pressed", eff === "dark" ? "true" : "false"); if (b.type === "checkbox") b.checked = eff === "dark"; });
  }
  function initThemeToggle(scope) {
    withSelf(scope, "[data-dz-theme-toggle]").forEach(function (el) {
      if (!once(el, "Theme")) return;
      el.setAttribute("aria-pressed", root.getAttribute("data-bs-theme") === "dark" ? "true" : "false");
      if (el.type === "checkbox") el.checked = root.getAttribute("data-bs-theme") === "dark";
      el.addEventListener("click", function (e) {
        if (el.type !== "checkbox") e.preventDefault();
        setTheme(root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark");
      });
    });
  }

  /* ---------- 9. bascule de prix mensuel / annuel ---------- */
  function initPriceToggle(scope) {
    withSelf(scope, "[data-dz-price-toggle]").forEach(function (tg) {
      if (!once(tg, "Price")) return;
      var area = tg.closest("[data-dz-pricing]") || tg.closest(".dz-section") || doc;
      function apply(period) {
        $all("button[data-period]", tg).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.period === period ? "true" : "false"); });
        $all("[data-monthly][data-yearly]", area).forEach(function (el) {
          var v = el.getAttribute(period === "yearly" ? "data-yearly" : "data-monthly");
          if (el.textContent === v) return;
          el.animate ? el.animate([{ opacity: 0, transform: "translateY(-6px)" }, { opacity: 1, transform: "none" }], { duration: 300, easing: "ease-out" }) : null;
          el.textContent = v;
        });
        $all("[data-dz-show-period]", area).forEach(function (el) { el.hidden = el.getAttribute("data-dz-show-period") !== period; });
      }
      $all("button[data-period]", tg).forEach(function (b) {
        b.type = "button";
        b.addEventListener("click", function () { apply(b.dataset.period); });
      });
      apply(tg.getAttribute("data-dz-price-toggle") || "monthly");
    });
  }

  /* ---------- 10. onglets ---------- */
  function initTabs(scope) {
    withSelf(scope, ".dz-tabs").forEach(function (box) {
      if (!once(box, "Tabs")) return;
      var btns = $all(".dz-tabs-nav [data-tab]", box);
      var panels = $all(".dz-tab-panel[data-tab]", box);
      function show(id) {
        btns.forEach(function (b) { b.setAttribute("aria-selected", b.dataset.tab === id ? "true" : "false"); });
        panels.forEach(function (p) { p.hidden = p.dataset.tab !== id; });
      }
      btns.forEach(function (b) { b.type = "button"; b.setAttribute("role", "tab"); b.addEventListener("click", function () { show(b.dataset.tab); }); });
      if (btns[0]) show((btns.filter(function (b) { return b.getAttribute("aria-selected") === "true"; })[0] || btns[0]).dataset.tab);
    });
  }

  /* ---------- 11. défilement infini (logos) ---------- */
  function initMarquee(scope) {
    withSelf(scope, ".dz-marquee").forEach(function (m) {
      if (!once(m, "Mq")) return;
      var track = m.querySelector(".dz-marquee-track");
      if (!track) return;
      var clone = track.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      m.appendChild(clone);
      if (m.dataset.dzSpeed) m.style.setProperty("--dz-marquee-dur", m.dataset.dzSpeed + "s");
    });
  }

  /* ---------- 12. copier dans le presse-papier ---------- */
  function initCopy(scope) {
    withSelf(scope, "[data-dz-copy]").forEach(function (el) {
      if (!once(el, "Copy")) return;
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var v = el.getAttribute("data-dz-copy");
        var target = v && v.charAt(0) === "#" ? doc.querySelector(v) : null;
        var text = target ? (target.value || target.textContent) : v;
        (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject())
          .then(function () { toast(el.dataset.dzCopied || "Copié ✓"); })
          .catch(function () { toast("Copie impossible"); });
      });
    });
  }

  /* ---------- 13. menu mobile ---------- */
  function initMenus(scope) {
    withSelf(scope, "[data-dz-menu-toggle]").forEach(function (btn) {
      if (!once(btn, "Menu")) return;
      var target = doc.querySelector(btn.getAttribute("data-dz-menu-toggle"));
      if (!target) return;
      btn.setAttribute("aria-expanded", "false");
      btn.addEventListener("click", function () {
        var open = target.classList.toggle("dz-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
      $all("a", target).forEach(function (a) { a.addEventListener("click", function () { target.classList.remove("dz-open"); btn.setAttribute("aria-expanded", "false"); }); });
    });
  }

  /* ---------- 14. compte à rebours ---------- */
  function initCountdown(scope) {
    withSelf(scope, "[data-dz-countdown]").forEach(function (el) {
      if (!once(el, "Cd")) return;
      var end = new Date(el.getAttribute("data-dz-countdown")).getTime();
      if (isNaN(end)) return;
      var units = { days: 864e5, hours: 36e5, minutes: 6e4, seconds: 1e3 };
      function pad(n) { return n < 10 ? "0" + n : "" + n; }
      (function tick() {
        if (!doc.body.contains(el)) return;
        var left = Math.max(0, end - Date.now());
        var parts = { days: Math.floor(left / units.days), hours: Math.floor(left % units.days / units.hours), minutes: Math.floor(left % units.hours / units.minutes), seconds: Math.floor(left % units.minutes / units.seconds) };
        var slots = $all("[data-dz-unit]", el);
        if (slots.length) slots.forEach(function (s) { s.textContent = pad(parts[s.dataset.dzUnit] || 0); });
        else el.textContent = parts.days + "j " + pad(parts.hours) + ":" + pad(parts.minutes) + ":" + pad(parts.seconds);
        if (left > 0) setTimeout(tick, 1000);
        else if (el.dataset.dzDone) el.textContent = el.dataset.dzDone;
      })();
    });
  }

  /* ---------- 15. avant / après ---------- */
  function initCompare(scope) {
    withSelf(scope, ".dz-compare").forEach(function (box) {
      if (!once(box, "Cmp")) return;
      var input = doc.createElement("input");
      input.type = "range"; input.min = 0; input.max = 100; input.value = 50;
      input.setAttribute("aria-label", "Comparer avant et après");
      box.appendChild(input);
      var set = function () { box.style.setProperty("--pos", input.value + "%"); };
      input.addEventListener("input", set); set();
    });
  }

  /* ---------- 16. barre du bas : onglet actif ---------- */
  function initBottomNav(scope) {
    withSelf(scope, ".dz-bottom-nav a, .dz-nav-links a, [data-dz-active-link] a").forEach(function (a) {
      if (!once(a, "Act")) return;
      try {
        var u = new URL(a.href, location.href);
        var here = location.pathname.replace(/\/$/, "") || "/";
        var there = u.pathname.replace(/\/$/, "") || "/";
        if (u.origin === location.origin && (there === here || (there !== "/" && here.indexOf(there + "/") === 0 && !u.hash))) a.classList.add("dz-active");
      } catch (e) {}
    });
  }

  /* ---------- 17. retour en haut ---------- */
  function initToTop(scope) {
    withSelf(scope, ".dz-to-top").forEach(function (b) {
      if (!once(b, "Top")) return;
      b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: motionOff() ? "auto" : "smooth" }); });
    });
    if (root.getAttribute("data-dz-totop") === "on" && !doc.querySelector(".dz-to-top") && doc.body) {
      var btn = doc.createElement("button");
      btn.className = "dz-to-top"; btn.type = "button"; btn.setAttribute("aria-label", "Retour en haut");
      btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
      doc.body.appendChild(btn);
      initToTop(btn);
    }
  }

  /* ---------- 18. toasts ---------- */
  function toast(msg, opts) {
    opts = opts || {};
    var zone = doc.querySelector(".dz-toasts");
    if (!zone) { zone = doc.createElement("div"); zone.className = "dz-toasts"; zone.setAttribute("aria-live", "polite"); doc.body.appendChild(zone); }
    var t = doc.createElement("div");
    t.className = "dz-toast";
    if (opts.icon) { var i = doc.createElement("i"); i.className = opts.icon; t.appendChild(i); }
    var s = doc.createElement("span"); s.textContent = msg; t.appendChild(s);
    zone.appendChild(t);
    setTimeout(function () { t.classList.add("dz-out"); setTimeout(function () { t.remove(); }, 320); }, opts.timeout || 2800);
    return t;
  }

  /* ---------- 19. confettis (pour les succès) ---------- */
  function confetti(opts) {
    if (motionOff()) return;
    opts = opts || {};
    var c = doc.createElement("canvas");
    c.style.cssText = "position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:4000";
    doc.body.appendChild(c);
    var ctx = c.getContext("2d"), W = c.width = innerWidth * devicePixelRatio, H = c.height = innerHeight * devicePixelRatio;
    var cs = getComputedStyle(root);
    var colors = opts.colors || [cs.getPropertyValue("--dz-primary"), cs.getPropertyValue("--dz-accent"), cs.getPropertyValue("--dz-accent-2"), "#fbbf24"].map(function (s) { return s.trim() || "#6d5efc"; });
    var ox = (opts.x != null ? opts.x : 0.5) * W, oy = (opts.y != null ? opts.y : 0.35) * H;
    var ps = [];
    for (var k = 0; k < (opts.count || 140); k++) {
      var a = Math.random() * Math.PI * 2, v = (4 + Math.random() * 9) * devicePixelRatio;
      ps.push({ x: ox, y: oy, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 6 * devicePixelRatio, r: (4 + Math.random() * 5) * devicePixelRatio, c: colors[k % colors.length], rot: Math.random() * 6, vr: (Math.random() - .5) * .3, life: 0 });
    }
    var t0 = performance.now();
    (function frame(now) {
      ctx.clearRect(0, 0, W, H);
      ps.forEach(function (p) {
        p.vy += .25 * devicePixelRatio; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.rot += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.fillStyle = p.c;
        ctx.globalAlpha = Math.max(0, 1 - (now - t0) / 2600);
        ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2); ctx.restore();
      });
      if (now - t0 < 2600) requestAnimationFrame(frame); else c.remove();
    })(t0);
  }
  function initConfettiTriggers(scope) {
    withSelf(scope, "[data-dz-confetti]").forEach(function (el) {
      if (!once(el, "Conf")) return;
      el.addEventListener("click", function (e) {
        confetti({ x: e.clientX / innerWidth, y: e.clientY / innerHeight });
      });
    });
  }

  /* ---------- 20. liens d'ancre avec décalage de la barre fixe ---------- */
  function initAnchors(scope) {
    withSelf(scope, 'a[href^="#"]:not([href="#"]):not([data-bs-toggle])').forEach(function (a) {
      if (!once(a, "Anc")) return;
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href").slice(1);
        var t = id && doc.getElementById(id);
        if (!t) return;
        e.preventDefault();
        var nav = doc.querySelector(".dz-nav, .navbar.fixed-top, .navbar.sticky-top");
        var off = nav ? nav.getBoundingClientRect().height + 12 : 12;
        window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - off, behavior: motionOff() ? "auto" : "smooth" });
        history.replaceState(null, "", "#" + id);
      });
    });
  }


  /* ---------- 21. pause des animations hors écran ---------- */
  var offIO = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { en.target.classList.toggle("dz-offscreen", !en.isIntersecting); });
  }, { rootMargin: "120px 0px" }) : null;
  function initOffscreen(scope) {
    if (!offIO) return;
    withSelf(scope, ".dz-section,.dz-hero,.dz-marquee,.dz-orbit,.dz-cta,.dz-portrait-wrap,.dz-browser,.dz-footer").forEach(function (el) {
      if (!once(el, "Off")) return;
      offIO.observe(el);
    });
  }

  /* ---------- 22. bandeau à fermer ---------- */
  function initDismiss(scope) {
    withSelf(scope, "[data-dz-dismiss]").forEach(function (b) {
      if (!once(b, "Dis")) return;
      var box = b.closest(b.getAttribute("data-dz-dismiss") || ".dz-topbar") || b.parentElement;
      var key = "dz-dismiss-" + (box.id || (box.textContent || "").trim().slice(0, 40));
      try { if (localStorage.getItem(key)) box.classList.add("dz-dismissed"); } catch (e) {}
      b.addEventListener("click", function () { box.classList.add("dz-dismissed"); try { localStorage.setItem(key, "1"); } catch (e) {} onScroll(); });
    });
  }

  /* ---------- 23. texte qui s'éclaire mot par mot ---------- */
  var wordEls = [];
  function initWords(scope) {
    withSelf(scope, "[data-dz-words],.dz-words-reveal").forEach(function (el) {
      if (!once(el, "Wd")) return;
      el.classList.add("dz-words");
      splitTextNodes(el, function (word) { var s = doc.createElement("span"); s.className = "dz-w"; s.textContent = word; return s; });
      el._dzW = $all(".dz-w", el);
      wordEls.push(el);
    });
  }
  function splitTextNodes(el, make) {
    var walker = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (n) {
      var parts = n.nodeValue.split(/(\s+)/);
      var frag = doc.createDocumentFragment();
      parts.forEach(function (p) { if (!p) return; frag.appendChild(/\s+/.test(p) ? doc.createTextNode(p) : make(p)); });
      n.parentNode.replaceChild(frag, n);
    });
  }
  function updateWords() {
    wordEls = wordEls.filter(function (el) { return doc.body.contains(el); });
    wordEls.forEach(function (el) {
      var r = el.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      var n = el._dzW.length, lit = Math.round(p * n);
      for (var i = 0; i < n; i++) el._dzW[i].style.setProperty("--o", i < lit ? 1 : 0.15);
    });
  }

  /* ---------- 24. lettres qui montent (titre) ---------- */
  function initSplit(scope) {
    withSelf(scope, "[data-dz-split],.dz-split-text").forEach(function (el) {
      if (!once(el, "Spl")) return;
      var rr = el.getBoundingClientRect();
      if (rr.top < window.innerHeight && rr.bottom > 0 && !el.hasAttribute("data-dz-split-force")) return; /* déjà visible : pas d'effet (évite le clignotement) */
      var i = 0;
      splitTextNodes(el, function (word) {
        var w = doc.createElement("span"); w.className = "dz-wd";
        word.split("").forEach(function (ch) { var s = doc.createElement("span"); s.className = "dz-ch"; s.textContent = ch; s.style.setProperty("--i", i++); w.appendChild(s); });
        return w;
      });
      el.classList.add("dz-split-ready");
      if (motionOff()) el.classList.add("dz-in"); else initReveal(el);
    });
  }

  /* ---------- 25. défilement horizontal épinglé ---------- */
  var hscrolls = [];
  function initHScroll(scope) {
    withSelf(scope, "[data-dz-hscroll]").forEach(function (el) {
      if (!once(el, "Hs")) return;
      el.classList.add("dz-hscroll");
      hscrolls.push(el);
      sizeHScroll(el);
    });
  }
  function sizeHScroll(el) {
    var track = el.querySelector(".dz-hscroll-track");
    if (!track) return;
    if (window.innerWidth < 768 || motionOff()) { el.style.height = ""; track.style.transform = ""; return; }
    var dist = Math.max(0, track.scrollWidth - window.innerWidth);
    el._dzDist = dist;
    el.style.height = (window.innerHeight + dist) + "px";
  }
  function updateHScroll() {
    hscrolls = hscrolls.filter(function (el) { return doc.body.contains(el); });
    hscrolls.forEach(function (el) {
      var track = el.querySelector(".dz-hscroll-track");
      if (!track || !el._dzDist || window.innerWidth < 768) return;
      var r = el.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, -r.top / (r.height - window.innerHeight || 1)));
      track.style.transform = "translate3d(" + (-p * el._dzDist).toFixed(1) + "px,0,0)";
    });
  }

  /* ---------- 26. carrousel ---------- */
  function initSlider(scope) {
    withSelf(scope, "[data-dz-slider],.dz-slider-auto").forEach(function (box) {
      if (!once(box, "Sl")) return;
      box.classList.add("dz-slider");
      var track = box.querySelector(".dz-slider-track");
      if (!track) return;
      var slides = Array.prototype.slice.call(track.children);
      var ui = box.querySelector(".dz-slider-ui");
      if (!ui) {
        ui = doc.createElement("div"); ui.className = "dz-slider-ui";
        ui.innerHTML = '<div class="dz-slider-dots"></div><div class="dz-slider-arrows"><button type="button" class="dz-btn dz-btn-ghost dz-icon-btn" data-dir="-1" aria-label="Précédent">←</button><button type="button" class="dz-btn dz-btn-ghost dz-icon-btn" data-dir="1" aria-label="Suivant">→</button></div>';
        box.appendChild(ui);
      }
      var dots = ui.querySelector(".dz-slider-dots");
      dots.innerHTML = "";
      slides.forEach(function (s, i) { var d = doc.createElement("button"); d.type = "button"; d.setAttribute("aria-label", "Aller à " + (i + 1)); d.addEventListener("click", function () { go(i); }); dots.appendChild(d); });
      function current() { var x = track.scrollLeft, best = 0, bd = 1e9; slides.forEach(function (s, i) { var d = Math.abs(s.offsetLeft - track.offsetLeft - x); if (d < bd) { bd = d; best = i; } }); return best; }
      function go(i) { i = (i + slides.length) % slides.length; track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: motionOff() ? "auto" : "smooth" }); }
      function mark() { var c = current(); Array.prototype.forEach.call(dots.children, function (d, i) { d.setAttribute("aria-current", i === c ? "true" : "false"); }); }
      $all("[data-dir]", ui).forEach(function (b) { b.addEventListener("click", function () { go(current() + parseInt(b.dataset.dir, 10)); }); });
      track.addEventListener("scroll", function () { requestAnimationFrame(mark); }, { passive: true });
      mark();
      var delay = parseInt(box.getAttribute("data-dz-slider"), 10);
      if (delay > 0 && !motionOff()) {
        var paused = false;
        box.addEventListener("pointerenter", function () { paused = true; });
        box.addEventListener("pointerleave", function () { paused = false; });
        setInterval(function () { if (!paused && !box.classList.contains("dz-offscreen") && doc.body.contains(box) && !doc.hidden) go(current() + 1); }, delay * 1000);
      }
    });
  }

  /* ---------- 27. filtres (portfolio, listes) ---------- */
  function initFilter(scope) {
    withSelf(scope, "[data-dz-filter]").forEach(function (bar) {
      if (!once(bar, "Flt")) return;
      var target = doc.querySelector(bar.getAttribute("data-dz-filter"));
      if (!target) return;
      var btns = $all("[data-filter]", bar);
      btns.forEach(function (b) {
        b.type = "button";
        b.addEventListener("click", function () {
          var f = b.getAttribute("data-filter");
          btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          Array.prototype.forEach.call(target.children, function (it) {
            var tags = (it.getAttribute("data-tags") || "").split(/[\s,]+/);
            var show = f === "*" || tags.indexOf(f) >= 0;
            it.classList.toggle("dz-filtered-out", !show);
            if (show && it.animate && !motionOff()) it.animate([{ opacity: 0, transform: "scale(.97)" }, { opacity: 1, transform: "none" }], { duration: 350, easing: "ease-out" });
          });
        });
      });
      if (btns[0]) btns[0].setAttribute("aria-pressed", "true");
    });
  }

  /* ---------- 28. puces à bascule ---------- */
  function initChips(scope) {
    withSelf(scope, ".dz-chips[data-dz-toggle] .dz-chip, button.dz-chip").forEach(function (c) {
      if (!once(c, "Chp") || c.closest("[data-dz-filter]")) return;
      c.addEventListener("click", function () {
        var single = c.closest("[data-dz-single]");
        if (single) $all(".dz-chip", single).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") === "true" && !single ? "false" : "true");
      });
    });
  }

  /* ---------- 29. curseur personnalisé ---------- */
  function initCursor() {
    if (root.getAttribute("data-dz-cursor") !== "on" || !finePointer || motionOff() || doc.querySelector(".dz-cursor")) return;
    var ring = doc.createElement("div"); ring.className = "dz-cursor";
    var dot = doc.createElement("div"); dot.className = "dz-cursor-dot";
    doc.body.appendChild(ring); doc.body.appendChild(dot);
    var x = -100, y = -100, rx = -100, ry = -100;
    window.addEventListener("pointermove", function (e) { x = e.clientX; y = e.clientY; dot.style.transform = "translate(" + x + "px," + y + "px)"; }, { passive: true });
    doc.addEventListener("pointerover", function (e) { ring.classList.toggle("dz-hover", !!(e.target.closest && e.target.closest("a,button,[data-dz-lightbox],.dz-work,input,label"))); });
    (function loop() { rx += (x - rx) * 0.18; ry += (y - ry) * 0.18; ring.style.transform = "translate(" + rx.toFixed(1) + "px," + ry.toFixed(1) + "px)"; requestAnimationFrame(loop); })();
  }

  /* ---------- 30. lightbox ---------- */
  function initLightbox(scope) {
    withSelf(scope, "[data-dz-lightbox],.dz-lightbox-on img").forEach(function (el) {
      if (!once(el, "Lb")) return;
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var src = el.getAttribute("data-dz-lightbox") || el.getAttribute("href") || el.getAttribute("src") || (el.querySelector("img") || {}).src;
        if (!src) return;
        var box = doc.createElement("div"); box.className = "dz-lightbox";
        var yt = src.match(/(?:youtu\.be\/|v=|embed\/)([\w-]{11})/);
        box.innerHTML = yt ? '<iframe src="https://www.youtube-nocookie.com/embed/' + yt[1] + '?autoplay=1" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>' : '<img alt="">';
        if (!yt) box.querySelector("img").src = src;
        doc.body.appendChild(box);
        requestAnimationFrame(function () { box.classList.add("dz-open"); });
        function close() { box.classList.remove("dz-open"); setTimeout(function () { box.remove(); }, 300); doc.removeEventListener("keydown", esc); }
        function esc(ev) { if (ev.key === "Escape") close(); }
        box.addEventListener("click", close); doc.addEventListener("keydown", esc);
      });
    });
  }

  /* ---------- 31. bandeau cookies ---------- */
  function initCookie(scope) {
    withSelf(scope, "[data-dz-cookie]").forEach(function (box) {
      if (!once(box, "Ck")) return;
      var v = null; try { v = localStorage.getItem("dz-cookie"); } catch (e) {}
      if (v) { box.classList.add("dz-dismissed"); return; }
      $all("[data-accept],[data-refuse]", box).forEach(function (b) {
        b.addEventListener("click", function () {
          try { localStorage.setItem("dz-cookie", b.hasAttribute("data-accept") ? "ok" : "no"); } catch (e) {}
          box.classList.add("dz-dismissed");
          doc.dispatchEvent(new CustomEvent("dz:cookie", { detail: b.hasAttribute("data-accept") }));
        });
      });
    });
  }

  /* ---------- 32. feuilles, tiroirs, fenêtres : data-dz-open / data-dz-close ---------- */
  var overlay = null;
  function openPanel(p) {
    if (!overlay) { overlay = doc.createElement("div"); overlay.className = "dz-overlay"; doc.body.appendChild(overlay); overlay.addEventListener("click", closeAll); }
    closeAll();
    p.classList.add("dz-open"); overlay.classList.add("dz-open");
    doc.documentElement.style.overflow = "hidden";
  }
  function closeAll() {
    $all(".dz-sheet.dz-open,.dz-drawer.dz-open").forEach(function (x) { x.classList.remove("dz-open"); });
    if (overlay) overlay.classList.remove("dz-open");
    doc.documentElement.style.overflow = "";
  }
  function initPanels(scope) {
    withSelf(scope, "[data-dz-open]").forEach(function (b) {
      if (!once(b, "Op")) return;
      b.addEventListener("click", function (e) { var p = doc.querySelector(b.getAttribute("data-dz-open")); if (p) { e.preventDefault(); openPanel(p); } });
    });
    withSelf(scope, "[data-dz-close]").forEach(function (b) {
      if (!once(b, "Cl")) return;
      b.addEventListener("click", function (e) { e.preventDefault(); closeAll(); });
    });
  }

  /* ---------- 33. palette de commandes ⌘K / Ctrl+K ---------- */
  function initCmdk(scope) {
    withSelf(scope, "[data-dz-cmdk]").forEach(function (box) {
      if (!once(box, "Cmd")) return;
      box.classList.add("dz-cmdk");
      var input = box.querySelector("input"), list = box.querySelector(".dz-cmdk-list");
      if (!input || !list) return;
      var sel = 0;
      function items() { return $all("a", list).filter(function (a) { return !a.hidden; }); }
      function paint() { var it = items(); it.forEach(function (a, i) { a.classList.toggle("dz-sel", i === sel); }); if (it[sel]) it[sel].scrollIntoView({ block: "nearest" }); }
      function filter() {
        var q = input.value.trim().toLowerCase();
        $all("a", list).forEach(function (a) { a.hidden = q && a.textContent.toLowerCase().indexOf(q) < 0 && (a.dataset.keywords || "").toLowerCase().indexOf(q) < 0; });
        $all(".dz-cmdk-group", list).forEach(function (g) { var n = g.nextElementSibling, any = false; while (n && !n.classList.contains("dz-cmdk-group")) { if (n.tagName === "A" && !n.hidden) any = true; n = n.nextElementSibling; } g.hidden = !any; });
        var empty = list.querySelector(".dz-cmdk-empty"); if (empty) empty.hidden = items().length > 0;
        sel = 0; paint();
      }
      function open() { box.classList.add("dz-open"); input.value = ""; filter(); setTimeout(function () { input.focus(); }, 30); }
      function close() { box.classList.remove("dz-open"); }
      box.addEventListener("click", function (e) { if (e.target === box) close(); });
      input.addEventListener("input", filter);
      input.addEventListener("keydown", function (e) {
        var it = items();
        if (e.key === "ArrowDown") { sel = Math.min(it.length - 1, sel + 1); paint(); e.preventDefault(); }
        else if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); paint(); e.preventDefault(); }
        else if (e.key === "Enter" && it[sel]) { it[sel].click(); close(); }
        else if (e.key === "Escape") close();
      });
      doc.addEventListener("keydown", function (e) { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); box.classList.contains("dz-open") ? close() : open(); } });
      $all("[data-dz-cmdk-open]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); open(); }); });
    });
  }

  /* ---------- 34. onglets en lecture automatique ---------- */
  function initTabsAutoplay(scope) {
    withSelf(scope, ".dz-tabs[data-dz-autoplay]").forEach(function (box) {
      if (!once(box, "Ap") || motionOff()) return;
      var sec = parseFloat(box.getAttribute("data-dz-autoplay")) || 6;
      box.style.setProperty("--dz-autoplay", sec + "s");
      var btns = $all(".dz-tabs-nav [data-tab]", box), user = false;
      btns.forEach(function (b) { b.addEventListener("click", function (e) { if (e.isTrusted) user = true; }); });
      setInterval(function () {
        if (user || box.classList.contains("dz-offscreen") || doc.hidden || !doc.body.contains(box)) return;
        var i = btns.findIndex(function (b) { return b.getAttribute("aria-selected") === "true"; });
        var nb = btns[(i + 1) % btns.length]; if (nb) nb.click();
      }, sec * 1000);
    });
  }

  /* ---------- lancement ---------- */
  function pageFlags() {
    root.classList.toggle("dz-has-hero", !!doc.querySelector(".dz-hero"));
    root.classList.toggle("dz-has-nav", !!doc.querySelector(".dz-nav"));
    var bn = doc.querySelector(".dz-bottom-nav");
    root.classList.toggle("dz-has-bottomnav", !!bn);
    root.classList.toggle("dz-has-bottomnav-mobile", !!(bn && bn.classList.contains("dz-mobile-only")));
    $all(".page-section").forEach(function (ps) {
      var first = ps.firstElementChild && ps.firstElementChild.firstElementChild;
      if (ps.querySelector(".dz-nav") || (first && first.classList.contains("full-page-width"))) ps.classList.add("dz-flush");
    });
  }

  /* initialisation en deux temps : l'essentiel tout de suite, le reste quand
     le navigateur est libre (le chargement reste fluide) */
  function init(scope, deferRest) {
    scope = scope || doc;
    var critical = [initReveal, initSplit, initTyped, initThemeToggle, initMenus, initMarquee, initTabs, initPriceToggle, initAnchors, initDismiss, initOffscreen, initWords, initHScroll, initBottomNav, initToTop];
    var rest = [initSpotlight, initTilt, initMagnetic, initParallax, initCopy, initCountdown, initCompare, initConfettiTriggers, initSlider, initFilter, initChips, initLightbox, initCookie, initPanels, initCmdk, initTabsAutoplay];
    function run(list) { list.forEach(function (fn) { try { fn(scope); } catch (e) { if (window.console) console.warn("[dysizz-ui]", fn.name, e); } }); }
    run(critical);
    if (deferRest) idle(function () { run(rest); }, { timeout: 800 }); else run(rest);
  }

  window.DZ = { __loaded: true, init: init, toast: toast, confetti: confetti, setTheme: setTheme, version: "2.2.0" };

  function start() {
    if (inBuilder) { initThemeToggle(doc); return; }
    pageFlags();
    init(doc, true);
    initCursor();
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { hscrolls.forEach(sizeHScroll); onScroll(); }, { passive: true });
    window.addEventListener("load", function () { hscrolls.forEach(sizeHScroll); onScroll(); });
    /* Saltcorn recharge des vues en ajax : on initialise ce qui arrive (par lots) */
    if ("MutationObserver" in window) {
      var pending = [], timer = null;
      var mo = new MutationObserver(function (muts) {
        for (var k = 0; k < muts.length; k++) {
          var added = muts[k].addedNodes;
          for (var m = 0; m < added.length; m++) {
            var n = added[m];
            if (n.nodeType === 1 && !n.classList.contains("dz-w") && !n.classList.contains("dz-ch") && !n.classList.contains("dz-wd") && n.className !== "dz-toast") pending.push(n);
          }
        }
        if (pending.length && !timer) timer = setTimeout(function () {
          var batch = pending; pending = []; timer = null;
          batch.forEach(function (n) { if (doc.body.contains(n)) init(n, false); });
        }, 120);
      });
      mo.observe(doc.body, { childList: true, subtree: true });
    }
  }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", start);
  else start();
})();
