"""Construit index.js (fichier unique du plugin) à partir de src/plugin.js et assets/.

Lancer après toute modification :
    python3 tools/build_packs.py   # si les blocs ont changé
    python3 tools/build_index.py
"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
A = os.path.join(ROOT, "assets")
embed = {}
for f in ["dz-core.css", "dz-skin.css", "dz.js"]:
    embed[f] = open(os.path.join(A, f), encoding="utf-8").read()
for f in ["blocks.json", "demo-pages.json"]:
    embed[f] = json.load(open(os.path.join(A, f), encoding="utf-8"))
version = json.load(open(os.path.join(ROOT, "package.json")))["version"]
src = open(os.path.join(ROOT, "src", "plugin.js"), encoding="utf-8").read()
assert "/*__EMBED__*/ {}" in src and '/*__VERSION__*/ "0.0.0"' in src
out = src.replace("/*__EMBED__*/ {}", json.dumps(embed, ensure_ascii=False)).replace('/*__VERSION__*/ "0.0.0"', json.dumps(version))
out = "/* FICHIER GÉNÉRÉ par tools/build_index.py — modifier src/plugin.js et assets/ */\n" + out
open(os.path.join(ROOT, "index.js"), "w", encoding="utf-8").write(out)
print("index.js", len(out) // 1024, "Ko, version", version)
