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
  var motionOff = function () { return reduceMotion || root.getAttribute("data-dz-motion") === "off"; };

  root.classList.add("dz-js");

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
    withSelf(scope, "[data-dz-reveal],.dz-reveal,.dz-stagger,.dz-highlight,[data-dz-count],.dz-progress[data-dz-value]").forEach(function (el) {
      if (!once(el, "Rev")) return;
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
    withSelf(scope, "[data-dz-tilt]").forEach(function (el) {
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
    withSelf(scope, "[data-dz-parallax]").forEach(function (el) {
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
      ticking = false;
    });
  }

  /* ---------- 8. thème clair / sombre ---------- */
  function setTheme(mode) {
    try { localStorage.setItem("dz-theme", mode); } catch (e) {}
    var eff = mode === "auto" ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light") : mode;
    root.setAttribute("data-bs-theme", eff);
    $all("[data-dz-theme-toggle]").forEach(function (b) { b.setAttribute("aria-pressed", eff === "dark" ? "true" : "false"); });
  }
  function initThemeToggle(scope) {
    withSelf(scope, "[data-dz-theme-toggle]").forEach(function (el) {
      if (!once(el, "Theme")) return;
      el.setAttribute("aria-pressed", root.getAttribute("data-bs-theme") === "dark" ? "true" : "false");
      el.addEventListener("click", function (e) {
        e.preventDefault();
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

  /* ---------- lancement ---------- */
  function init(scope) {
    scope = scope || doc;
    try {
      initReveal(scope); initTyped(scope); initSpotlight(scope); initTilt(scope); initMagnetic(scope);
      initParallax(scope); initThemeToggle(scope); initPriceToggle(scope); initTabs(scope); initMarquee(scope);
      initCopy(scope); initMenus(scope); initCountdown(scope); initCompare(scope); initBottomNav(scope);
      initToTop(scope); initConfettiTriggers(scope); initAnchors(scope);
    } catch (e) { if (window.console) console.warn("[dysizz-ui]", e); }
  }

  window.DZ = { __loaded: true, init: init, toast: toast, confetti: confetti, setTheme: setTheme, version: "1.0.0" };

  function start() {
    init(doc);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    /* Saltcorn recharge des vues en ajax : on initialise ce qui arrive */
    if ("MutationObserver" in window) {
      var pending = [];
      var mo = new MutationObserver(function (muts) {
        muts.forEach(function (m) { Array.prototype.forEach.call(m.addedNodes, function (n) { if (n.nodeType === 1) pending.push(n); }); });
        if (pending.length) {
          var batch = pending; pending = [];
          requestAnimationFrame(function () { batch.forEach(function (n) { if (doc.body.contains(n)) init(n); }); });
        }
      });
      mo.observe(doc.body, { childList: true, subtree: true });
    }
  }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", start);
  else start();
})();
