/* dysizz-ui — ce qui est injecté dans chaque page */
"use strict";
const { pub } = require("./core");
const { EMBED } = require("./assets");
const { FONTS, FONT_AUTO, MONO, PRESETS, cfgOf } = require("./settings");

/* ---------------- ce qui est injecté dans chaque page ---------------- */
const fontUrl = (fams) => `https://fonts.googleapis.com/css2?${[...new Set(fams)].map((g) => "family=" + g).join("&")}&display=swap`;

const headers = (rawCfg) => {
  const c = cfgOf(rawCfg);
  const P = PRESETS[c.preset];
  const fHead = c.font_heading === FONT_AUTO ? P.heading : c.font_heading;
  const fBody = c.font_body === FONT_AUTO ? P.body : c.font_body;
  const fams = [...new Set([fBody, fHead])].map((f) => FONTS[f] && FONTS[f].g).filter(Boolean);
  if (P.mono) fams.push(MONO);
  if (P.accent) fams.push(P.accent);
  const out = [];
  if (fams.length)
    out.push({
      headerTag:
        /* polices chargées sans bloquer l'affichage (le texte apparaît tout de suite) */
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
        `<link rel="preload" as="style" href="${fontUrl(fams)}" onload="this.onload=null;this.rel='stylesheet'">` +
        `<noscript><link rel="stylesheet" href="${fontUrl(fams)}"></noscript>`,
    });
  out.push({ css: pub("dz-core.css") });
  if (c.skin) out.push({ css: pub("dz-skin.css") });
  /* familles de blocs utilisées par ce tenant (cochées sur /dysizz-ui) */
  for (const f of c.families) if (EMBED[`dz-f-${f}.css`]) out.push({ css: pub(`dz-f-${f}.css`) });
  const vars = [
    `--dz-font-body:${FONTS[fBody].stack}`,
    `--dz-font-heading:${FONTS[fHead].stack}`,
    `--dz-container:${c.container}px`,
  ];
  if (c.radius > 0) vars.push(`--dz-radius:${c.radius}px`);
  if (c.custom_colors) vars.push(`--dz-primary:${c.primary}`, `--dz-primary-ink:${c.primary}`, `--dz-accent:${c.accent}`, `--dz-accent-2:${c.accent_2}`);
  /* :root:root pour passer devant les univers ([data-dz-preset]) */
  out.push({ style: `:root:root{${vars.join(";")}}` + (c.classes_css ? "\n" + c.classes_css : "") + (c.custom_css ? "\n" + c.custom_css : "") });
  /* script de tête : pose les attributs avant l'affichage (pas de flash) */
  const flags = {
    preset: c.preset,
    style: c.style,
    skin: c.skin,
    glass: c.glass_nav,
    motion: c.motion === "toujours" ? "on" : c.motion === "désactivées" ? "off" : "system",
    cursor: c.cursor,
    top: c.to_top,
    remember: c.remember_theme,
    builderCss: pub("dz-builder.css"),
    fam: EMBED["family-prefixes.json"] || {},
    famUrl: pub("dz-f-"),
    tr: c.transition,
    snap: c.snap,
    smooth: c.smooth,
    morph: c.bg_morph,
  };
  out.push({
    headerTag:
      "<script>(function(f){var h=document.documentElement;" +
      "h.setAttribute('data-dz-preset',f.preset);h.setAttribute('data-dz-style',f.style);" +
      "if(f.skin)h.classList.add('dz-skin');if(f.glass)h.classList.add('dz-glass-nav');" +
      "var b=/^\\/(pageedit|viewedit)\\//.test(location.pathname);if(b){h.classList.add('dz-builder');var l=document.createElement('link');l.rel='stylesheet';l.href=f.builderCss;document.head.appendChild(l);}" +
      "h.setAttribute('data-dz-motion',b?'off':f.motion);if(f.cursor)h.setAttribute('data-dz-cursor','on');if(f.top)h.setAttribute('data-dz-totop','on');" +
      "if(f.tr!=='none')h.setAttribute('data-dz-tr',f.tr);if(f.snap!=='off')h.setAttribute('data-dz-snap',f.snap);if(f.smooth!=='off')h.setAttribute('data-dz-smooth',f.smooth);if(!f.morph)h.setAttribute('data-dz-bgmorph','off');" +
      "if(f.remember){try{var t=localStorage.getItem('dz-theme');if(t==='auto')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';if(t==='dark'||t==='light')h.setAttribute('data-bs-theme',t);}catch(e){}}" +
      "window.__dzFam={map:f.fam,url:f.famUrl};h.classList.add('dz-js');setTimeout(function(){if(!window.DZ)h.classList.remove('dz-js');},3000);" +
      "})(" + JSON.stringify(flags) + ");</script>",
  });
  out.push({ script: pub("dz.js"), defer: true });
  if (c.smooth !== "off") out.push({ script: pub("dz-smooth.js"), defer: true });
  return out;
};


module.exports = { headers };
