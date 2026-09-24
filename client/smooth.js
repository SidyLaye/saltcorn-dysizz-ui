/* dysizz-ui — défilement doux (optionnel, chargé seulement si activé dans les réglages)
   Moteur : Lenis (MIT, darkroom.engineering). Réglages lus sur <html> :
   data-dz-smooth="light|strong", désactivé si le visiteur réduit les animations,
   dans le builder, sur les écrans tactiles (le natif y est déjà doux) et sur les
   pages d'application (.dz-app) sauf si la page demande le contraire. */
import Lenis from "lenis";

(function () {
  var h = document.documentElement;
  function wanted() {
    var mode = h.getAttribute("data-dz-smooth");
    var page = document.querySelector("[data-dz-page-smooth]");
    if (page) mode = page.getAttribute("data-dz-page-smooth");
    if (!mode || mode === "off") return null;
    if (h.classList.contains("dz-builder") || h.getAttribute("data-dz-motion") === "off") return null;
    if (h.getAttribute("data-dz-motion") === "system" && matchMedia("(prefers-reduced-motion: reduce)").matches) return null;
    if (matchMedia("(pointer: coarse)").matches) return null;
    if (!page && document.querySelector(".dz-app, .dz-app-shell")) return null;
    return mode;
  }
  function start() {
    var mode = wanted();
    if (!mode) return;
    var lenis = new Lenis({
      lerp: mode === "strong" ? 0.075 : 0.12,
      wheelMultiplier: 1,
      smoothWheel: true,
      anchors: { offset: -80 },
      /* on laisse défiler nativement les zones qui ont leur propre ascenseur */
      prevent: function (node) {
        return !!(node.closest && node.closest("[data-lenis-prevent],.modal,.dz-sheet,.dz-cmdk,.dz-scroller,textarea,select,.dropdown-menu,[data-dz-no-smooth]"));
      },
      autoRaf: true,
    });
    h.classList.add("dz-smooth-on");
    window.DZ = window.DZ || {};
    window.DZ.lenis = lenis;
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
