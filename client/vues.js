/* dysizz-ui — vues de données et pages d'application (aucune dépendance).
   - puces de filtre : marque celle qui correspond à l'adresse ;
   - tableau (kanban) : glisser-déposer d'une colonne à l'autre ;
   - accueil : salutation et date du jour. */
(function () {
  "use strict";
  var doc = document;

  function params() {
    var o = {};
    new URLSearchParams(location.search).forEach(function (v, k) { o[k] = v; });
    return o;
  }

  function chips() {
    var cur = params();
    doc.querySelectorAll("[data-dzv-chips]").forEach(function (nav) {
      var links = nav.querySelectorAll("a[data-q]");
      var keys = {};
      links.forEach(function (a) { new URLSearchParams(a.getAttribute("data-q")).forEach(function (v, k) { keys[k] = 1; }); });
      links.forEach(function (a) {
        var q = new URLSearchParams(a.getAttribute("data-q"));
        var on = true, n = 0;
        q.forEach(function (v, k) { n++; if (cur[k] !== v) on = false; });
        if (!n) on = !Object.keys(keys).some(function (k) { return cur[k] !== undefined && cur[k] !== ""; });
        a.classList.toggle("dzv-on", on);
        if (on) a.setAttribute("aria-current", "true");
      });
    });
  }

  function csrf() {
    return window._sc_globalCsrf || (doc.querySelector("input[name=_csrf]") || {}).value || "";
  }

  function toast(msg, bad) {
    if (window.DZ && window.DZ.toast) return window.DZ.toast(msg, bad ? "danger" : "success");
    if (window.notifyAlert) return window.notifyAlert({ type: bad ? "danger" : "success", text: msg });
  }

  function boards() {
    doc.querySelectorAll("[data-dzv-board]").forEach(function (board) {
      if (board.__dzm || board.hasAttribute("data-readonly")) return;
      board.__dzm = 1;
      var view = board.getAttribute("data-dzv-board"), dragged = null, from = null;
      board.addEventListener("dragstart", function (e) {
        var c = e.target.closest(".dzv-card");
        if (!c) return;
        dragged = c; from = c.parentNode;
        c.classList.add("dzv-dragging");
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", c.getAttribute("data-id"));
      });
      board.addEventListener("dragend", function () {
        if (dragged) dragged.classList.remove("dzv-dragging");
        board.querySelectorAll(".dzv-drop").forEach(function (x) { x.classList.remove("dzv-drop"); });
      });
      board.addEventListener("dragover", function (e) {
        var col = e.target.closest(".dzv-col");
        if (!col || !dragged) return;
        e.preventDefault();
        board.querySelectorAll(".dzv-drop").forEach(function (x) { if (x !== col) x.classList.remove("dzv-drop"); });
        col.classList.add("dzv-drop");
      });
      board.addEventListener("drop", function (e) {
        var col = e.target.closest(".dzv-col");
        if (!col || !dragged) return;
        e.preventDefault();
        col.classList.remove("dzv-drop");
        var body = col.querySelector(".dzv-col-body");
        if (body === from) return;
        var card = dragged, prev = from;
        var empty = body.querySelector(".dzv-col-empty");
        if (empty) empty.remove();
        body.insertBefore(card, body.firstChild);
        count(board);
        fetch("/view/" + encodeURIComponent(view) + "/move", {
          method: "POST", credentials: "same-origin",
          headers: { "Content-Type": "application/json", "CSRF-Token": csrf(), "X-Requested-With": "XMLHttpRequest" },
          body: JSON.stringify({ id: card.getAttribute("data-id"), value: col.getAttribute("data-value") }),
        }).then(function (r) { return r.json(); }).then(function (j) {
          if (j && j.error) throw new Error(j.error);
          card.classList.toggle("dzv-card-done", col === board.lastElementChild);
        }).catch(function (err) {
          prev.insertBefore(card, prev.firstChild);
          count(board);
          toast("Déplacement impossible : " + err.message, true);
        });
      });
    });
  }

  function count(board) {
    board.querySelectorAll(".dzv-col").forEach(function (col) {
      var n = col.querySelectorAll(".dzv-card").length, c = col.querySelector(".dzv-col-count");
      if (c) c.textContent = n;
    });
  }

  function hello() {
    doc.querySelectorAll("[data-dzv-hello]").forEach(function (el) {
      var h = new Date().getHours();
      var w = h < 5 ? "Bonne nuit" : h < 12 ? "Bonjour" : h < 18 ? "Bon après-midi" : "Bonsoir";
      var name = el.getAttribute("data-dzv-hello");
      el.textContent = w + (name ? " " + name : "");
    });
    doc.querySelectorAll("[data-dzv-date]").forEach(function (el) {
      var s = new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
      el.textContent = s.charAt(0).toUpperCase() + s.slice(1);
    });
  }

  /* DZ Journal : filtre par niveau + recherche (délégation : un seul écouteur, même après rechargement) */
  function logApply(box) {
    var lvl = box.getAttribute("data-lvl") || "tout", q = (box.getAttribute("data-q") || "").toLowerCase();
    box.querySelectorAll(".dzv-log-row").forEach(function (r) {
      var ok = (lvl === "tout" || r.getAttribute("data-t") === lvl) && (!q || r.textContent.toLowerCase().indexOf(q) >= 0);
      r.style.display = ok ? "" : "none";
    });
    box.querySelectorAll(".dzv-log-day").forEach(function (d) {
      var any = Array.prototype.some.call(d.querySelectorAll(".dzv-log-row"), function (r) { return r.style.display !== "none"; });
      d.style.display = any ? "" : "none";
    });
  }
  doc.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-dzv-log]");
    if (!b) return;
    var box = b.closest("[data-dzv-logs]");
    box.querySelectorAll("[data-dzv-log]").forEach(function (x) { x.classList.toggle("on", x === b); });
    box.setAttribute("data-lvl", b.getAttribute("data-dzv-log"));
    logApply(box);
  });
  doc.addEventListener("input", function (e) {
    if (!e.target.matches || !e.target.matches("[data-dzv-log-q]")) return;
    var box = e.target.closest("[data-dzv-logs]");
    box.setAttribute("data-q", e.target.value);
    logApply(box);
  });

  function start() { chips(); boards(); hello(); }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", start); else start();
  /* le contenu chargé en fenêtre ou rechargé par Saltcorn */
  doc.addEventListener("shown.bs.modal", start);
  window.addEventListener("load", start);
})();
