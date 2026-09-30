/* Vue « DZ Écran » : un bloc HTML <div data-dz-widget=…> devient un bloc de vue réglable dans l'éditeur,
   et le rendu redonne exactement les mêmes attributs (données fictives). */
"use strict";
const assert = require("assert");
const Module = require("module");
const orig = Module._load;
Module._load = function (req, ...rest) { if (req.startsWith("@saltcorn/")) return class {}; return orig.call(this, req, ...rest); };
const E = require("../src/views/ecran");
(async () => {
  const html = `<div class="dz-card" style="padding:0;max-width:760px"><div data-dz-widget="fiche" data-table="equipe" data-champs='["nom","email"]' data-apres="/page/gestion?t=equipe" data-caches='["x"]'></div></div>`;
  const layout = { above: [{ type: "blank", contents: "Titre", textStyle: "h1" }, { type: "blank", isHTML: true, contents: html }, { type: "blank", isHTML: true, contents: "<p>texte</p><div data-dz-widget=\"tableau\"></div>" }] };
  const { layout: L, convertis } = E.convertirLayout(layout);
  assert.strictEqual(convertis, 1, "seul le bloc qui ne contient que des widgets est converti");
  const carte = L.above[1];
  assert.strictEqual(carte.type, "container"); assert.strictEqual(carte.customClass, "dz-card"); assert.strictEqual(carte.style["max-width"], "760px");
  const v = carte.contents;
  assert.deepStrictEqual([v.type, v.view, v.state], ["view", "dz_ecran", "fixed"]);
  assert.strictEqual(v.configuration.table, "equipe"); assert.strictEqual(v.configuration.champs, '["nom","email"]');
  assert.deepStrictEqual(JSON.parse(v.configuration.autres), { caches: ["x"] });
  assert.strictEqual(L.above[2].isHTML, true, "bloc mêlé de texte : laissé tel quel");
  assert.strictEqual(layout.above[1].isHTML, true, "l'original n'est pas modifié");
  /* rendu : mêmes attributs, valeurs échappées */
  const r = E.balise(v.configuration);
  assert.match(r, /^<div data-dz-widget="fiche"/); assert.match(r, /data-table="equipe"/); assert.match(r, /data-champs="\[&quot;nom&quot;,&quot;email&quot;\]"/); assert.match(r, /data-caches=/);
  assert.match(E.balise({ widget: "tableau", titre: "A & <b>" }), /data-titre="A &amp; &lt;b&gt;"/);
  assert.match(E.balise({ widget: "<script>" }), /^<div data-dz-widget="tableau"/, "type de bloc inconnu : tableau");
  assert.match(E.balise({ autres: "{pas du json" }), /n'est pas un JSON valide/);
  assert.ok(!/onload/.test(E.balise({ autres: '{"x\\" onload=\\"alert(1)":"1"}' })), "clé d'attribut invalide ignorée");
  /* un autre widget (jeu, signature…) n'est pas un bloc d'écran : laissé en HTML */
  const jeu = E.convertirLayout({ type: "blank", isHTML: true, contents: '<div data-dz-widget="morpion"></div>' });
  assert.strictEqual(jeu.convertis, 0); assert.strictEqual(jeu.layout.isHTML, true);
  /* « Preset … » enregistrés par l'éditeur (IP à la place des réglages) : retirés, le reste gardé */
  const abime = { above: [{ type: "view", view: "dz_ecran", name: "a", state: "fixed", configuration: { widget: "tableau", source: "leads", preset_source: "IP", preset_titre: "IP" } }, { type: "view", view: "autre", configuration: { preset_x: "IP" } }] };
  const net = E.convertirLayout(abime);
  assert.strictEqual(net.nettoyes, 1); assert.strictEqual(net.convertis, 0);
  assert.deepStrictEqual(net.layout.above[0].configuration, { widget: "tableau", source: "leads" });
  assert.deepStrictEqual(net.layout.above[1].configuration, { preset_x: "IP" }, "autre vue : pas touchée");
  assert.strictEqual(abime.above[0].configuration.preset_source, "IP", "l'original n'est pas modifié");
  const fs = await E.get_state_fields();
  assert.ok(fs.find((f) => f.name === "source") && fs.find((f) => f.name === "autres").fieldview === "textarea");
  assert.strictEqual(E.widgetsHTML(layout), 2); assert.strictEqual(E.widgetsHTML(L), 1);
  console.log("DZ Écran OK : bloc HTML → vue réglable dans l'éditeur, rendu identique, valeurs échappées");
})().catch((e) => { console.error(e); process.exit(1); });
