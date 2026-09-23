"""Construit index.js (fichier unique du plugin) à partir de src/plugin.js et assets/.

Lancer après toute modification :
    python3 tools/build_packs.py   # si les blocs ont changé
    python3 tools/build_index.py
"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
A = os.path.join(ROOT, "assets")
embed = {}
import re, shutil, subprocess


def min_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)          # commentaires
    css = re.sub(r"\s+", " ", css)                           # espaces
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)             # autour des séparateurs
    css = re.sub(r";}", "}", css)
    return css.strip()


def min_js(path):
    """terser si disponible (npx), sinon le fichier tel quel."""
    try:
        if shutil.which("npx"):
            out = subprocess.run(["npx", "--yes", "terser", path, "-c", "-m"], capture_output=True, text=True, timeout=120)
            if out.returncode == 0 and len(out.stdout) > 1000:
                return out.stdout
    except Exception:
        pass
    return open(path, encoding="utf-8").read()


for f in ["dz-core.css", "dz-skin.css"]:
    embed[f] = min_css(open(os.path.join(A, f), encoding="utf-8").read())
embed["dz.js"] = min_js(os.path.join(A, "dz.js"))
for f in ["blocks.json", "demo-pages.json"]:
    embed[f] = json.load(open(os.path.join(A, f), encoding="utf-8"))
version = json.load(open(os.path.join(ROOT, "package.json")))["version"]
src = open(os.path.join(ROOT, "src", "plugin.js"), encoding="utf-8").read()
assert "/*__EMBED__*/ {}" in src and '/*__VERSION__*/ "0.0.0"' in src
out = src.replace("/*__EMBED__*/ {}", json.dumps(embed, ensure_ascii=False)).replace('/*__VERSION__*/ "0.0.0"', json.dumps(version))
out = "/* FICHIER GÉNÉRÉ par tools/build_index.py — modifier src/plugin.js et assets/ */\n" + out
open(os.path.join(ROOT, "index.js"), "w", encoding="utf-8").write(out)
print("index.js", len(out) // 1024, "Ko, version", version, "| css", len(embed["dz-core.css"]) // 1024, "+", len(embed["dz-skin.css"]) // 1024, "Ko, js", len(embed["dz.js"]) // 1024, "Ko")
