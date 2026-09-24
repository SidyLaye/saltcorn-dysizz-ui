/* =====================================================================
   Parité builder : dans l'éditeur de Saltcorn, un conteneur est rendu
   .kontainer.<classes> > div > .canvas > enfants. Une classe qui met ses
   enfants en grille / flex doit donc reporter sa mise en page sur .canvas.
   Ce module lit le CSS et écrit ces règles automatiquement (préfixées
   html.dz-builder : aucun effet hors de l'éditeur).
   ===================================================================== */
import postcss from "postcss";

const LAYOUT_DISPLAY = /^(inline-)?(flex|grid)$/;
const LAYOUT_PROPS = new Set([
  "display", "grid-template-columns", "grid-template-rows", "grid-template-areas", "grid-template", "grid-auto-flow",
  "grid-auto-rows", "grid-auto-columns", "gap", "row-gap", "column-gap", "grid-gap", "align-items", "align-content",
  "justify-content", "justify-items", "place-items", "place-content", "flex-direction", "flex-wrap", "flex-flow",
  "counter-reset", "overflow-x", "scroll-snap-type",
]);
const COMPOUND = /^((?:\.[a-zA-Z][\w-]*)+)$/;
const CHILD = /^((?:\.[a-zA-Z][\w-]*)+)\s*>\s*(.+)$/;
const classesOf = (compound) => compound.split(".").filter(Boolean);
/* dans le builder, un <span> du kit devient div.is-text et un <a> devient .is-builder-link */
const TYPE_MAP = { span: ":is(span, .is-text)", a: ":is(a, .is-builder-link)" };
const builderTypes = (sel) => sel.replace(/(^|[\s>+~(,])(span|a)(?=[.:\[\s>+~),]|$)/g, (m, pre, tag) => pre + TYPE_MAP[tag]);
/* enfant direct d'un conteneur : dans le builder il y a deux div entre les deux */
const builderChild = (sel) => sel.replace(/((?:\.[a-zA-Z][\w-]*)+)\s*>\s*/g, (m, compound) => `.kontainer${compound} > div > .canvas > `);

export function builderParity(css, { prefix = "dz-" } = {}) {
  const root = postcss.parse(css);
  const layoutClasses = new Set();
  /* passe 1 : quelles classes mettent leurs enfants en grille / flex */
  root.walkRules((rule) => {
    const disp = rule.nodes.find((n) => n.type === "decl" && n.prop === "display" && LAYOUT_DISPLAY.test(n.value.replace(/\s*!important/, "").trim()));
    if (!disp) return;
    for (const sel of rule.selectors) {
      const m = sel.trim().match(COMPOUND);
      if (m) classesOf(m[1]).filter((c) => c.startsWith(prefix) || prefix === "").forEach((c) => layoutClasses.add(c));
    }
  });
  const isLayout = (compound) => classesOf(compound).some((c) => layoutClasses.has(c));
  const out = postcss.root();
  const clonePath = (rule, newRule) => {
    /* recopie le contexte @media / @supports */
    let node = newRule, parent = rule.parent;
    while (parent && parent.type === "atrule") {
      const at = postcss.atRule({ name: parent.name, params: parent.params });
      at.append(node);
      node = at;
      parent = parent.parent;
    }
    out.append(node);
  };
  /* passe 2 : règles reportées */
  root.walkRules((rule) => {
    if (rule.parent && rule.parent.type === "atrule" && /keyframes/.test(rule.parent.name)) return;
    const decls = rule.nodes.filter((n) => n.type === "decl");
    for (const selRaw of rule.selectors) {
      const sel = selRaw.trim();
      let m;
      if ((m = sel.match(COMPOUND)) && isLayout(m[1])) {
        const lay = decls.filter((d) => LAYOUT_PROPS.has(d.prop));
        if (!lay.length) continue;
        const r = postcss.rule({ selector: `html.dz-builder .kontainer${m[1]} > div > .canvas` });
        lay.forEach((d) => r.append(postcss.decl({ prop: d.prop, value: d.value.replace(/\s*!important/, ""), important: d.prop === "display" || d.important })));
        clonePath(rule, r);
        const disp = lay.find((d) => d.prop === "display");
        if (disp) {
          const k = postcss.rule({ selector: `html.dz-builder .kontainer${m[1]}` });
          k.append(postcss.decl({ prop: "display", value: /^inline/.test(disp.value) ? "inline-block" : "block", important: true }));
          clonePath(rule, k);
          const d2 = postcss.rule({ selector: `html.dz-builder .kontainer${m[1]} > div` });
          d2.append(postcss.decl({ prop: "display", value: "block", important: true }));
          d2.append(postcss.decl({ prop: "height", value: "100%" }));
          clonePath(rule, d2);
        }
      } else if (/\.dz-/.test(sel) && (/>/.test(sel) || /(^|[\s>+~(,])(span|a)(?=[.:\[\s>+~),]|$)/.test(sel))) {
        /* sélecteurs « parent > enfant » ou qui visent span / a : variante builder */
        const bsel = builderTypes(builderChild(sel));
        if (bsel === sel) continue;
        const r = postcss.rule({ selector: `html.dz-builder ${bsel}` });
        decls.forEach((d) => r.append(d.clone()));
        if (r.nodes.length) clonePath(rule, r);
      }
    }
  });
  return { css: out.toString(), layoutClasses: [...layoutClasses].sort() };
}
