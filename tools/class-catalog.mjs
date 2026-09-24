/* Catalogue des classes : pour chaque classe du kit, les règles CSS qui la
   concernent (ce qu'il y a « derrière » la classe), groupées par fichier.
   Sert à la page /dysizz-ui/classes. */
import postcss from "postcss";

export function classCatalog(files) {
  /* files : [{ group, label, css }] */
  const out = {};
  for (const { group, label, css } of files) {
    const root = postcss.parse(css);
    const classes = {};
    root.walkRules((rule) => {
      if (rule.parent && rule.parent.type === "atrule" && /keyframes/.test(rule.parent.name)) return;
      const found = new Set((rule.selector.match(/\.dz-[a-zA-Z0-9_-]+/g) || []).map((c) => c.slice(1)));
      if (!found.size) return;
      let ctx = "", p = rule.parent;
      while (p && p.type === "atrule") { ctx = `@${p.name} ${p.params} › ` + ctx; p = p.parent; }
      const decls = rule.nodes.filter((n) => n.type === "decl").map((d) => `  ${d.prop}: ${d.value}${d.important ? " !important" : ""};`).join("\n");
      const text = `${ctx ? "/* " + ctx.replace(/ › $/, "") + " */\n" : ""}${rule.selector.replace(/\s+/g, " ")} {\n${decls}\n}`;
      for (const c of found) {
        const e = (classes[c] ||= { rules: [], main: false });
        if (e.rules.length < 14) e.rules.push(text);
        if (new RegExp(`^\\.${c.replace(/[-]/g, "\\-")}$`).test(rule.selector.trim())) e.main = true;
      }
    });
    /* on garde les classes qui ont au moins une règle propre (pas seulement citées) */
    for (const [c, e] of Object.entries(classes)) if (!e.main && e.rules.length < 2) delete classes[c];
    out[group] = { label, classes };
  }
  return out;
}
