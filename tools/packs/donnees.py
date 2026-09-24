"""Famille « Données » : visualisation de données sans bibliothèque JS.
Graphiques en CSS pur (barres, anneaux, jauges, cartes de chaleur) et en
petits SVG inline (courbes, aires, sparklines). Préfixe CSS : dz-dt-.
Les valeurs sont écrites en clair : --v (hauteur / largeur en %) sur le
conteneur, texte lisible dans les étiquettes."""
import random

FAMILY = "donnees"


# ------------------------------------------------------------------ outils
def _pts(vals, w, h, lo=None, hi=None, pad=2):
    lo = min(vals) if lo is None else lo
    hi = max(vals) if hi is None else hi
    n = len(vals)
    return [(i * w / (n - 1), pad + (h - 2 * pad) * (1 - (v - lo) / ((hi - lo) or 1))) for i, v in enumerate(vals)]


def _curve(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    n = len(pts)
    for i in range(n - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def spark(vals, gid, serie="s1", w=120, h=36):
    """petite courbe avec aire en dégradé"""
    d = _curve(_pts(vals, w, h, pad=3))
    return (f'<svg class="dz-dt-spark dz-dt-{serie}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="dz-dt-stop"/>'
            f'<stop offset="1" class="dz-dt-stop0"/></linearGradient></defs>'
            f'<path class="dz-dt-area" fill="url(#{gid})" d="{d}L{w} {h}L0 {h}Z"/>'
            f'<path class="dz-dt-ln" vector-effect="non-scaling-stroke" d="{d}"/></svg>')


def lines(series, gid, hi, w=600, h=200):
    """grand graphique : [(valeurs, série, aire?, pointillé?)] sur une échelle 0..hi"""
    out = [f'<svg class="dz-dt-svg" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><defs>']
    for k, (vals, serie, area, dashed) in enumerate(series):
        if area:
            out.append(f'<linearGradient id="{gid}{k}" x1="0" y1="0" x2="0" y2="1" class="dz-dt-{serie}">'
                       f'<stop offset="0" class="dz-dt-stop"/><stop offset="1" class="dz-dt-stop0"/></linearGradient>')
    out.append('</defs>')
    for k, (vals, serie, area, dashed) in enumerate(series):
        d = _curve(_pts(vals, w, h, lo=0, hi=hi, pad=0))
        g = f'<g class="dz-dt-{serie}">'
        if area:
            g += f'<path class="dz-dt-area" fill="url(#{gid}{k})" d="{d}L{w} {h}L0 {h}Z"/>'
        g += f'<path class="dz-dt-ln{" dz-dt-dash" if dashed else ""}" vector-effect="non-scaling-stroke" d="{d}"/></g>'
        out.append(g)
    out.append('</svg>')
    return "".join(out)


def yaxis(labels):
    return '<div class="dz-dt-y">' + "".join(f"<span>{l}</span>" for l in labels) + "</div>"


def fr(n, dec=0):
    s = f"{n:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s


# ------------------------------------------------------------------ blocs
BLOCKS = []

# 1. cartes KPI avec sparkline -------------------------------------------
_kpis = [
    ("fas fa-euro-sign", "Chiffre d'affaires", "48 250 €", "up", "12,4 %", "vs 42 920 € les 30 j précédents",
     [31, 34, 33, 38, 36, 41, 39, 44, 42, 47, 45, 52], "s1"),
    ("fas fa-user-plus", "Nouveaux clients", "1 284", "up", "8,1 %", "dont 312 via le parrainage",
     [80, 78, 90, 86, 95, 92, 104, 99, 110, 108, 115, 121], "s2"),
    ("fas fa-percentage", "Taux de conversion", "3,42 %", "down", "0,3 pt", "objectif du trimestre : 3,8 %",
     [3.9, 3.8, 3.85, 3.7, 3.72, 3.6, 3.65, 3.5, 3.55, 3.48, 3.45, 3.42], "s4"),
    ("fas fa-shopping-basket", "Panier moyen", "86,40 €", "up", "4,7 %", "sur 3 482 commandes payées",
     [78, 80, 79, 81, 83, 82, 84, 83, 85, 84, 86, 86.4], "s3"),
]
_k = []
for i, (ic, lab, val, tr, dv, sub, vals, s) in enumerate(_kpis):
    _k.append(f"""
  <article class="dz-dt-kpi dz-dt-{s}">
    <div class="dz-dt-kpi-top"><span class="dz-dt-kpi-ico"><i class="{ic}"></i></span><span class="dz-dt-kpi-label">{lab}</span><span class="dz-trend dz-trend-{tr}"><i class="fas fa-arrow-{tr}"></i> {dv}</span></div>
    <div class="dz-dt-kpi-val dz-counter">{val}</div>
    {spark(vals, f"dzdt-kpi{i}", s)}
    <p class="dz-dt-kpi-sub">{sub}</p>
  </article>""")
BLOCKS.append(dict(name="indicateurs clés", icon="fas fa-tachometer-alt", html=f"""
<div class="dz-dt dz-dt-kpis">{''.join(_k)}
</div>
"""))

# 2. histogramme -----------------------------------------------------------
_months = ["Oct", "Nov", "Déc", "Janv", "Févr", "Mars", "Avr", "Mai", "Juin", "Juil", "Août", "Sept"]
_ca = [31.2, 36.8, 52.4, 28.9, 30.5, 35.1, 38.7, 41.2, 44.9, 39.6, 33.8, 48.3]
_cols = []
for m, v in zip(_months, _ca):
    act = " dz-active" if m == "Sept" else ""
    _cols.append(f'<div class="dz-dt-col{act}" style="--v:{v / 60 * 100:.1f}%"><span class="dz-dt-tip">{fr(v, 1)} k€</span><i class="dz-dt-bar"></i><span class="dz-dt-xl">{m}</span></div>')
BLOCKS.append(dict(name="histogramme", icon="fas fa-chart-bar", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Chiffre d'affaires mensuel</h3>
      <div class="dz-dt-figure"><span class="dz-dt-big">461,4 k€</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 18,2 %</span></div>
      <p class="dz-dt-sub">12 derniers mois · hors taxes · mis à jour il y a 4 min</p>
    </div>
    <div class="dz-dt-seg"><a href="#">7 j</a><a href="#">30 j</a><a class="dz-active" href="#">12 mois</a></div>
  </div>
  <div class="dz-dt-chart">
    {yaxis(["60 k", "45 k", "30 k", "15 k", "0"])}
    <div class="dz-dt-plot"><div class="dz-dt-bars">{''.join(_cols)}</div></div>
  </div>
  <div class="dz-dt-foot"><span class="dz-dt-note"><i class="fas fa-bolt"></i> Meilleur mois : <b>décembre</b> (52,4 k€)</span><span class="dz-dt-note">Moyenne : <b>38,5 k€ / mois</b></span></div>
</div>
"""))

# 3. barres groupées -------------------------------------------------------
_q = [("T1", 118, 142), ("T2", 131, 164), ("T3", 126, 171), ("T4", 158, 0)]
_g = []
for q, a, b in _q:
    bb = (f'<div class="dz-dt-gbar dz-dt-s1" style="--v:{b / 200 * 100:.1f}%"><span class="dz-dt-gv">{b}</span></div>' if b
          else '<div class="dz-dt-gbar dz-dt-ghost" style="--v:92%"><span class="dz-dt-gv">prév. 184</span></div>')
    _g.append(f'<div class="dz-dt-group"><div class="dz-dt-gbar dz-dt-s0" style="--v:{a / 200 * 100:.1f}%"><span class="dz-dt-gv">{a}</span></div>{bb}<span class="dz-dt-xl">{q}</span></div>')
BLOCKS.append(dict(name="barres groupées", icon="fas fa-chart-bar", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Ventes par trimestre, 2025 et 2026</h3>
      <p class="dz-dt-sub">En milliers d'euros · T4 2026 : prévision</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s0">2025 <b>533 k€</b></span><span class="dz-dt-key dz-dt-s1">2026 <b>477 k€</b></span><span class="dz-dt-key dz-dt-ghostkey">Prévision</span></div>
  </div>
  <div class="dz-dt-chart">
    {yaxis(["200", "150", "100", "50", "0"])}
    <div class="dz-dt-plot"><div class="dz-dt-groups">{''.join(_g)}</div></div>
  </div>
  <div class="dz-dt-deltas">
    <div><span class="dz-dt-kpi-label">T1</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 20,3 %</span></div>
    <div><span class="dz-dt-kpi-label">T2</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 25,2 %</span></div>
    <div><span class="dz-dt-kpi-label">T3</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 35,7 %</span></div>
    <div><span class="dz-dt-kpi-label">T4</span><span class="dz-badge dz-badge-neutral">en cours</span></div>
  </div>
</div>
"""))

# 4. barres empilées -------------------------------------------------------
_st = [("Avr", 212, 96, 41), ("Mai", 238, 104, 52), ("Juin", 261, 121, 58), ("Juil", 228, 117, 49),
       ("Août", 196, 98, 44), ("Sept", 284, 139, 71)]
_s = []
for m, a, b, c in _st:
    tot = a + b + c
    act = " dz-active" if m == "Sept" else ""
    _s.append(f'<div class="dz-dt-scol{act}" style="--v:{tot / 500 * 100:.1f}%"><span class="dz-dt-tip">{tot} inscriptions</span>'
              f'<div class="dz-dt-stack"><i class="dz-dt-s1" style="flex:{a}"></i><i class="dz-dt-s2" style="flex:{b}"></i><i class="dz-dt-s3" style="flex:{c}"></i></div>'
              f'<span class="dz-dt-xl">{m}</span></div>')
BLOCKS.append(dict(name="barres empilées", icon="fas fa-layer-group", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Inscriptions par formule</h3>
      <p class="dz-dt-sub">6 derniers mois · 3 043 comptes créés</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">Essentiel <b>59 %</b></span><span class="dz-dt-key dz-dt-s2">Pro <b>29 %</b></span><span class="dz-dt-key dz-dt-s3">Équipe <b>12 %</b></span></div>
  </div>
  <div class="dz-dt-chart">
    {yaxis(["500", "375", "250", "125", "0"])}
    <div class="dz-dt-plot"><div class="dz-dt-bars">{''.join(_s)}</div></div>
  </div>
</div>
"""))

# 5. barres horizontales classées -----------------------------------------
_rk = [("/tarifs", "Tarifs", 18420, 100), ("/", "Accueil", 15870, 86), ("/blog/automatiser-sa-facturation", "Automatiser sa facturation", 9 * 1000 + 312, 51),
       ("/fonctionnalites/planning", "Planning d'équipe", 7640, 41), ("/cas-clients/atelier-lune", "Cas client : Atelier Lune", 5980, 32),
       ("/aide/demarrer", "Démarrer en 5 minutes", 4215, 23), ("/integrations", "Intégrations", 3102, 17)]
_r = []
for i, (u, t, n, v) in enumerate(_rk):
    _r.append(f'<div class="dz-dt-hrow"><span class="dz-dt-rank">{i + 1}</span><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>{t}</b><span class="dz-mono">{u}</span></div>'
              f'<div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:{v}%"></i></div></div><span class="dz-dt-hval">{fr(n)}</span></div>')
BLOCKS.append(dict(name="barres classées", icon="fas fa-sort-amount-down", html=f"""
<div class="dz-dt dz-dt-panel dz-dt-narrow">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Pages les plus vues</h3>
      <p class="dz-dt-sub">Septembre 2026 · 64 539 vues uniques</p>
    </div>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Tout voir <i class="fas fa-arrow-right"></i></a>
  </div>
  <div class="dz-dt-hhead"><span>Page</span><span>Vues</span></div>
  <div class="dz-dt-hlist">{''.join(_r)}</div>
</div>
"""))

# 6. courbe + aire ---------------------------------------------------------
_v26 = [4.2, 4.8, 4.5, 5.6, 6.1, 5.8, 6.9, 7.4, 7.1, 8.3, 8.0, 9.2]
_v25 = [3.6, 3.9, 4.1, 4.0, 4.6, 4.4, 5.0, 5.3, 5.1, 5.6, 5.9, 6.2]
_lab = ["1 sept", "", "", "10 sept", "", "", "", "20 sept", "", "", "", "30 sept"]
BLOCKS.append(dict(name="courbe et aire", icon="fas fa-chart-area", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Visiteurs uniques</h3>
      <div class="dz-dt-figure"><span class="dz-dt-big">184 360</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 38,6 %</span></div>
      <p class="dz-dt-sub">Septembre 2026 comparé à septembre 2025</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">2026</span><span class="dz-dt-key dz-dt-s0 dz-dt-dashkey">2025</span></div>
  </div>
  <div class="dz-dt-chart">
    {yaxis(["10 k", "7,5 k", "5 k", "2,5 k", "0"])}
    <div class="dz-dt-plot">
      {lines([(_v25, "s0", False, True), (_v26, "s1", True, False)], "dzdt-line", 10)}
      <div class="dz-dt-cross" style="left:72.7%"></div>
      <i class="dz-dt-pt dz-dt-s1" style="left:72.7%;bottom:80%"></i>
      <div class="dz-dt-card" style="left:72.7%;bottom:80%">
        <b>Mardi 22 septembre</b>
        <span class="dz-dt-key dz-dt-s1">2026 <b>8 012</b></span>
        <span class="dz-dt-key dz-dt-s0">2025 <b>5 596</b></span>
      </div>
      <div class="dz-dt-xaxis"><span>1 sept</span><span>8 sept</span><span>15 sept</span><span>22 sept</span><span>30 sept</span></div>
    </div>
  </div>
</div>
"""))

# 7. anneau (donut) --------------------------------------------------------
BLOCKS.append(dict(name="anneau", icon="fas fa-chart-pie", html="""
<div class="dz-dt dz-dt-panel dz-dt-narrow">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Sources de trafic</h3>
      <p class="dz-dt-sub">30 derniers jours · 48 200 sessions</p>
    </div>
    <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-download"></i> Exporter</a>
  </div>
  <div class="dz-dt-donutwrap">
    <div class="dz-dt-donut" style="--p1:38%;--p2:62%;--p3:79%;--p4:91%">
      <div class="dz-dt-donut-c"><b>48 200</b><span>sessions</span></div>
    </div>
    <div class="dz-dt-dlist">
      <div class="dz-dt-drow dz-dt-s1"><span class="dz-dt-key">Recherche naturelle</span><b>18 316</b><span class="dz-dt-pct">38 %</span></div>
      <div class="dz-dt-drow dz-dt-s2"><span class="dz-dt-key">Accès direct</span><b>11 568</b><span class="dz-dt-pct">24 %</span></div>
      <div class="dz-dt-drow dz-dt-s3"><span class="dz-dt-key">Réseaux sociaux</span><b>8 194</b><span class="dz-dt-pct">17 %</span></div>
      <div class="dz-dt-drow dz-dt-s4"><span class="dz-dt-key">Newsletter</span><b>5 784</b><span class="dz-dt-pct">12 %</span></div>
      <div class="dz-dt-drow dz-dt-s5"><span class="dz-dt-key">Sites partenaires</span><b>4 338</b><span class="dz-dt-pct">9 %</span></div>
    </div>
  </div>
</div>
"""))

# 8. jauge semi-circulaire -------------------------------------------------
BLOCKS.append(dict(name="jauge", icon="fas fa-tachometer-alt", html="""
<div class="dz-dt dz-dt-panel dz-dt-narrow">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Performance du site</h3>
      <p class="dz-dt-sub">Mesures réelles des visiteurs · mobile · 28 jours</p>
    </div>
    <span class="dz-badge dz-badge-success"><i class="fas fa-check"></i> Bon</span>
  </div>
  <div class="dz-dt-gauge" style="--v:78">
    <div class="dz-dt-gauge-arc"></div>
    <div class="dz-dt-needle"></div>
    <div class="dz-dt-gauge-c"><b>78</b><span>sur 100</span></div>
    <span class="dz-dt-gauge-min">0</span><span class="dz-dt-gauge-max">100</span>
  </div>
  <div class="dz-dt-vitals">
    <div class="dz-dt-vital"><span class="dz-dt-kpi-label">Affichage principal</span><b>1,8 s</b><span class="dz-dt-state dz-dt-ok">Bon</span></div>
    <div class="dz-dt-vital"><span class="dz-dt-kpi-label">Réactivité</span><b>212 ms</b><span class="dz-dt-state dz-dt-mid">À améliorer</span></div>
    <div class="dz-dt-vital"><span class="dz-dt-kpi-label">Stabilité visuelle</span><b>0,04</b><span class="dz-dt-state dz-dt-ok">Bon</span></div>
  </div>
</div>
"""))

# 9. carte de chaleur (calendrier) -----------------------------------------
_rng = random.Random(26)
_cells = []
_weeks = 30
for w in range(_weeks):
    for d in range(7):
        base = 1.4 + w / _weeks * 1.6
        if d >= 5:
            base *= .45
        x = base + _rng.uniform(-1.3, 1.5)
        lvl = max(0, min(4, int(round(x))))
        if w == 15 and d == 1:
            lvl = 4
        _cells.append(f'<i class="dz-dt-l{lvl}"></i>')
_mlabels = [("Mars", 1), ("Avr", 5), ("Mai", 9), ("Juin", 14), ("Juil", 18), ("Août", 22), ("Sept", 27)]
_ml = "".join(f'<span style="grid-column:{c + 1}">{m}</span>' for m, c in _mlabels)
BLOCKS.append(dict(name="carte de chaleur", icon="fas fa-th", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">3 482 commandes en 30 semaines</h3>
      <p class="dz-dt-sub">Record : 41 commandes le mardi 16 juin · série en cours : 23 jours</p>
    </div>
    <div class="dz-dt-seg"><a href="#">2025</a><a class="dz-active" href="#">2026</a></div>
  </div>
  <div class="dz-dt-heatscroll">
    <div class="dz-dt-heat">
      <div class="dz-dt-heat-m">{_ml}</div>
      <div class="dz-dt-heat-g"><span>Lun</span><span></span><span>Mer</span><span></span><span>Ven</span><span></span><span>Dim</span>{''.join(_cells)}</div>
    </div>
  </div>
  <div class="dz-dt-foot">
    <span class="dz-dt-note"><i class="fas fa-info-circle"></i> Les week-ends comptent 55 % de commandes en moins.</span>
    <div class="dz-dt-scale"><span>Moins</span><i class="dz-dt-l0"></i><i class="dz-dt-l1"></i><i class="dz-dt-l2"></i><i class="dz-dt-l3"></i><i class="dz-dt-l4"></i><span>Plus</span></div>
  </div>
</div>
"""))

# 10. entonnoir ------------------------------------------------------------
_fn = [("fas fa-eye", "Visites", "48 200", 100, None), ("fas fa-box-open", "Fiche produit vue", "21 540", 44.7, ("44,7 %", "26 660 sorties")),
       ("fas fa-cart-plus", "Ajout au panier", "6 820", 14.1, ("31,7 %", "14 720 sorties")),
       ("fas fa-credit-card", "Paiement commencé", "3 110", 6.5, ("45,6 %", "3 710 sorties")),
       ("fas fa-check-circle", "Commande payée", "2 486", 5.2, ("79,9 %", "624 sorties"))]
_f = []
for i, (ic, lab, n, v, drop) in enumerate(_fn):
    if drop:
        _f.append(f'<div class="dz-dt-fdrop"><i class="fas fa-arrow-down"></i><span><b>{drop[0]}</b> passent à l\'étape suivante</span><span class="dz-dt-fout">{drop[1]}</span></div>')
    _f.append(f'<div class="dz-dt-fstep" style="--v:{max(v, 3)}%;--o:{1 - i * .14:.2f}"><div class="dz-dt-flab"><span class="dz-dt-kpi-ico"><i class="{ic}"></i></span><div><b>{lab}</b><span>{n}</span></div></div>'
              f'<div class="dz-dt-ftrack"><i class="dz-dt-fbar"></i></div><span class="dz-dt-fpct">{fr(v, 1)} %</span></div>')
BLOCKS.append(dict(name="entonnoir", icon="fas fa-filter", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Tunnel de conversion</h3>
      <p class="dz-dt-sub">Boutique en ligne · 1er au 30 septembre 2026</p>
    </div>
    <div class="dz-dt-figure dz-dt-right"><span class="dz-dt-big">5,16 %</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 0,8 pt</span></div>
  </div>
  <div class="dz-dt-funnel">{''.join(_f)}</div>
</div>
"""))

# 11. cohortes -------------------------------------------------------------
_co = [("Mars 2026", 1240, [100, 58, 46, 41, 38, 36, 34]), ("Avril 2026", 1386, [100, 61, 49, 43, 40, 37]),
       ("Mai 2026", 1512, [100, 63, 52, 46, 42]), ("Juin 2026", 1470, [100, 66, 55, 48]),
       ("Juillet 2026", 1298, [100, 64, 53]), ("Août 2026", 1105, [100, 69]), ("Sept. 2026", 1622, [100])]
_rows = []
for lab, n, vals in _co:
    cells = "".join(f'<span class="dz-dt-cell{" dz-dt-hi" if v >= 70 else ""}" style="--v:{v}">{v} %</span>' for v in vals)
    cells += '<span class="dz-dt-cell dz-dt-empty"></span>' * (7 - len(vals))
    _rows.append(f'<div class="dz-dt-crow"><span class="dz-dt-clab"><b>{lab}</b><span>{fr(n)} clients</span></span>{cells}</div>')
BLOCKS.append(dict(name="cohortes", icon="fas fa-th-large", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Rétention par cohorte mensuelle</h3>
      <p class="dz-dt-sub">Part des clients qui repassent commande, par mois d'inscription</p>
    </div>
    <div class="dz-dt-seg"><a class="dz-active" href="#">Clients</a><a href="#">Revenu</a></div>
  </div>
  <div class="dz-dt-scroll">
    <div class="dz-dt-cohort">
      <div class="dz-dt-crow dz-dt-chead"><span>Cohorte</span><span>Mois 0</span><span>Mois 1</span><span>Mois 2</span><span>Mois 3</span><span>Mois 4</span><span>Mois 5</span><span>Mois 6</span></div>
      {''.join(_rows)}
      <div class="dz-dt-crow dz-dt-cavg"><span class="dz-dt-clab"><b>Moyenne</b><span>9 633 clients</span></span><span class="dz-dt-cell">100 %</span><span class="dz-dt-cell">63 %</span><span class="dz-dt-cell">51 %</span><span class="dz-dt-cell">45 %</span><span class="dz-dt-cell">40 %</span><span class="dz-dt-cell">37 %</span><span class="dz-dt-cell">34 %</span></div>
    </div>
  </div>
</div>
"""))

# 12. classement / leaderboard ---------------------------------------------
_lb = [("4", "Inès Morel", "IM", "Paris Est", "31 ventes", "84 200 €", 72, "up"), ("5", "Karim Belkacem", "KB", "Lille", "28 ventes", "79 650 €", 68, "down"),
       ("6", "Chloé Vasseur", "CV", "Nantes", "26 ventes", "71 300 €", 61, "up"), ("7", "Tom Guérin", "TG", "Bordeaux", "22 ventes", "63 980 €", 55, "up")]
_l = "".join(f'<div class="dz-dt-lrow"><span class="dz-dt-rank">{r}</span><span class="dz-avatar dz-avatar-sm">{ini}</span>'
             f'<div class="dz-dt-lname"><b>{n}</b><span>{city} · {ventes}</span></div><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:{v}%"></i></div>'
             f'<span class="dz-dt-hval">{amt}</span><i class="fas fa-caret-{tr} dz-dt-{tr}"></i></div>'
             for r, n, ini, city, ventes, amt, v, tr in _lb)
BLOCKS.append(dict(name="classement", icon="fas fa-trophy", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Meilleurs commerciaux · septembre</h3>
      <p class="dz-dt-sub">Chiffre signé · objectif mensuel 110 000 €</p>
    </div>
    <div class="dz-dt-seg"><a href="#">Semaine</a><a class="dz-active" href="#">Mois</a><a href="#">Année</a></div>
  </div>
  <div class="dz-dt-podium">
    <div class="dz-dt-pod dz-dt-p2"><span class="dz-avatar dz-avatar-lg">LF</span><b>Léa Fontaine</b><span class="dz-dt-podval">98 400 €</span><div class="dz-dt-step"><span>2</span></div></div>
    <div class="dz-dt-pod dz-dt-p1"><i class="fas fa-crown dz-dt-crown"></i><span class="dz-avatar dz-avatar-lg">NB</span><b>Nathan Brun</b><span class="dz-dt-podval">126 750 €</span><div class="dz-dt-step"><span>1</span></div></div>
    <div class="dz-dt-pod dz-dt-p3"><span class="dz-avatar dz-avatar-lg">SA</span><b>Sofia Amrani</b><span class="dz-dt-podval">91 120 €</span><div class="dz-dt-step"><span>3</span></div></div>
  </div>
  <div class="dz-dt-llist">{_l}</div>
</div>
"""))

# 13. avant / après --------------------------------------------------------
_ba = [("Taux de conversion", "2,31 %", "3,42 %", 46, 68, "up", "+48 %"), ("Abandon au paiement", "71 %", "52 %", 71, 52, "up", "−19 pts"),
       ("Temps pour payer", "3 min 40", "1 min 55", 73, 38, "up", "−48 %"), ("Panier moyen", "82,10 €", "86,40 €", 82, 86, "up", "+5,2 %")]
_b = "".join(f'<div class="dz-dt-barow"><div class="dz-dt-balab"><b>{lab}</b><span class="dz-trend dz-trend-{tr}">{d}</span></div>'
             f'<div class="dz-dt-bapair"><div class="dz-dt-baline dz-dt-s0"><i class="dz-dt-hbar" style="--v:{va}%"></i><span>{a}</span></div>'
             f'<div class="dz-dt-baline dz-dt-s1"><i class="dz-dt-hbar" style="--v:{vb}%"></i><span>{b}</span></div></div></div>'
             for lab, a, b, va, vb, tr, d in _ba)
BLOCKS.append(dict(name="avant après", icon="fas fa-exchange-alt", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Nouveau tunnel de paiement : l'effet en chiffres</h3>
      <p class="dz-dt-sub">4 semaines avant la mise en ligne du 17 août, comparées aux 4 semaines après</p>
    </div>
  </div>
  <div class="dz-dt-vs">
    <div class="dz-dt-vscard dz-dt-s0"><span class="dz-dt-kpi-label">Avant · 20 juil. → 16 août</span><b>31 870 €</b><span>1 184 commandes</span></div>
    <span class="dz-dt-vsmid">VS</span>
    <div class="dz-dt-vscard dz-dt-s1 dz-dt-vsnew"><span class="dz-dt-kpi-label">Après · 17 août → 13 sept.</span><b>44 610 €</b><span>1 612 commandes</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 40,0 %</span></div>
  </div>
  <div class="dz-dt-ba">{_b}</div>
  <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s0">Avant</span><span class="dz-dt-key dz-dt-s1">Après</span></div>
</div>
"""))

# 14. répartition 100 % ----------------------------------------------------
_rp = [("Recherche naturelle", 58, 36, 6), ("Réseaux sociaux", 81, 14, 5), ("Newsletter", 47, 45, 8), ("Accès direct", 39, 55, 6), ("Publicité", 72, 22, 6)]
_p = "".join(f'<div class="dz-dt-prow"><span class="dz-dt-plab">{lab}</span><div class="dz-dt-pbar">'
             f'<span class="dz-dt-s1" style="flex:{a}">{a} %</span><span class="dz-dt-s2" style="flex:{b}">{b} %</span><span class="dz-dt-s3 dz-dt-tiny" style="flex:{c}">{c} %</span></div></div>'
             for lab, a, b, c in _rp)
BLOCKS.append(dict(name="répartition 100 %", icon="fas fa-align-left", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Appareils utilisés, par canal d'acquisition</h3>
      <p class="dz-dt-sub">Part des sessions · septembre 2026</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">Mobile</span><span class="dz-dt-key dz-dt-s2">Ordinateur</span><span class="dz-dt-key dz-dt-s3">Tablette</span></div>
  </div>
  <div class="dz-dt-plist">{_p}</div>
  <div class="dz-dt-pscale"><span>0 %</span><span>25 %</span><span>50 %</span><span>75 %</span><span>100 %</span></div>
</div>
"""))

# 15. carte des pays (grille) ----------------------------------------------
_tiles = [("IS", 1, 1, 0), ("NO", 5, 1, 1), ("SE", 6, 1, 2), ("FI", 7, 1, 1),
          ("IE", 2, 2, 1), ("GB", 3, 2, 3), ("DK", 5, 2, 1), ("EE", 7, 2, 0),
          ("NL", 4, 3, 2), ("DE", 5, 3, 3), ("PL", 6, 3, 2), ("LV", 7, 3, 0),
          ("BE", 3, 4, 3), ("LU", 4, 4, 2), ("CZ", 5, 4, 1), ("SK", 6, 4, 1), ("LT", 7, 4, 0),
          ("FR", 3, 5, 4), ("CH", 4, 5, 3), ("AT", 5, 5, 1), ("HU", 6, 5, 1), ("RO", 7, 5, 1),
          ("PT", 1, 6, 2), ("ES", 2, 6, 3), ("IT", 4, 6, 3), ("SI", 5, 6, 0), ("HR", 6, 6, 1), ("RS", 7, 6, 0), ("BG", 8, 6, 0),
          ("MT", 4, 7, 0), ("GR", 7, 7, 1), ("CY", 9, 7, 0)]
_t = "".join(f'<span class="dz-dt-tile dz-dt-l{l}" style="grid-column:{c};grid-row:{r}">{code}</span>' for code, c, r, l in _tiles)
_top = [("France", "FR", "21 480", 100), ("Belgique", "BE", "6 912", 32), ("Suisse", "CH", "4 870", 23), ("Allemagne", "DE", "3 944", 18), ("Espagne", "ES", "2 716", 13)]
_tp = "".join(f'<div class="dz-dt-crow2"><span class="dz-dt-code">{c}</span><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>{n}</b><span class="dz-dt-hval">{v}</span></div>'
              f'<div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:{p}%"></i></div></div></div>' for n, c, v, p in _top)
BLOCKS.append(dict(name="carte des pays", icon="fas fa-globe-europe", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Audience par pays</h3>
      <p class="dz-dt-sub">Sessions · 30 derniers jours · 32 pays européens</p>
    </div>
    <div class="dz-dt-seg"><a class="dz-active" href="#">Europe</a><a href="#">Monde</a></div>
  </div>
  <div class="dz-dt-geo">
    <div class="dz-dt-tiles">{_t}</div>
    <div class="dz-dt-geoside">
      <div class="dz-dt-toplist">{_tp}</div>
      <div class="dz-dt-scale"><span>0</span><i class="dz-dt-l0"></i><i class="dz-dt-l1"></i><i class="dz-dt-l2"></i><i class="dz-dt-l3"></i><i class="dz-dt-l4"></i><span>20 k+</span></div>
      <p class="dz-dt-note"><i class="fas fa-globe"></i> Hors Europe : Canada 1 840 · Maroc 1 312 · Sénégal 968</p>
    </div>
  </div>
</div>
"""))

# 16. nuage de points --------------------------------------------------------
_sc = [(12, 18, 10, 1), (18, 22, 12, 1), (22, 35, 16, 1), (28, 30, 12, 2), (31, 52, 20, 1), (36, 44, 14, 2), (40, 61, 22, 1),
       (44, 38, 12, 3), (47, 70, 24, 1), (52, 56, 16, 2), (55, 34, 12, 3), (60, 77, 26, 1), (63, 48, 14, 3), (67, 66, 18, 2),
       (71, 40, 12, 3), (74, 84, 28, 1), (78, 58, 16, 2), (82, 30, 14, 3), (86, 72, 20, 2), (90, 46, 14, 3), (25, 12, 10, 3), (15, 40, 12, 2)]
_dots = "".join(f'<i class="dz-dt-dot dz-dt-s{s}" style="left:{x}%;bottom:{y}%;--s:{r}px"></i>' for x, y, r, s in _sc)
BLOCKS.append(dict(name="nuage de points", icon="fas fa-braille", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Campagnes : budget dépensé et ventes générées</h3>
      <p class="dz-dt-sub">22 campagnes actives · taille du point = nombre de clics</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">Recherche</span><span class="dz-dt-key dz-dt-s2">Réseaux sociaux</span><span class="dz-dt-key dz-dt-s3">Affichage</span></div>
  </div>
  <div class="dz-dt-chart">
    {yaxis(["120", "90", "60", "30", "0"])}
    <div class="dz-dt-plot dz-dt-scatter">
      <span class="dz-dt-quad dz-dt-q1">Rentables</span><span class="dz-dt-quad dz-dt-q2">À surveiller</span>
      <svg class="dz-dt-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path class="dz-dt-trend" vector-effect="non-scaling-stroke" d="M5 86 L95 22"/></svg>
      {_dots}
      <div class="dz-dt-card dz-dt-card-sm" style="left:74%;bottom:84%"><b>Rentrée · recherche</b><span>2 960 € dépensés · 101 ventes</span></div>
      <div class="dz-dt-xaxis"><span>0 €</span><span>1 000 €</span><span>2 000 €</span><span>3 000 €</span><span>4 000 €</span></div>
    </div>
  </div>
  <div class="dz-dt-axisname"><span>Axe vertical : ventes</span><span>Axe horizontal : budget dépensé</span></div>
</div>
"""))

# 17. tableau de données pro -----------------------------------------------
_tb = [("AL", "Atelier Lune", "contact@atelier-lune.fr", "success", "Actif", "Équipe", "1 240 €", 88, [3, 4, 4, 5, 6, 6, 7], "il y a 2 h"),
       ("NX", "Nexora", "finance@nexora.io", "success", "Actif", "Pro", "890 €", 63, [5, 5, 6, 5, 6, 7, 7], "il y a 5 h"),
       ("BV", "Boulangerie Vauclair", "bonjour@vauclair.fr", "warning", "Essai", "Essentiel", "0 €", 4, [0, 1, 1, 2, 2, 3, 4], "hier"),
       ("CM", "Cabinet Mercier", "admin@mercier-avocats.fr", "success", "Actif", "Pro", "640 €", 46, [6, 6, 5, 6, 6, 6, 6], "hier"),
       ("OR", "Orbis Conseil", "compta@orbis.eu", "danger", "Impayé", "Équipe", "1 080 €", 77, [7, 6, 6, 5, 4, 4, 3], "il y a 3 j"),
       ("VF", "Verger des Fontaines", "hello@vergerfontaines.fr", "neutral", "Résilié", "Essentiel", "0 €", 0, [4, 4, 3, 2, 1, 0, 0], "il y a 12 j")]
_trs = []
for i, (ini, name, mail, st, stl, plan, mrr, v, sp, last) in enumerate(_tb):
    sel = " dz-dt-sel" if i == 1 else ""
    chk = '<span class="dz-dt-check dz-on"><i class="fas fa-check"></i></span>' if i == 1 else '<span class="dz-dt-check"></span>'
    _trs.append(f'<div class="dz-dt-tr{sel}">{chk}<div class="dz-dt-who"><span class="dz-avatar dz-avatar-sm">{ini}</span><div><b>{name}</b><span>{mail}</span></div></div>'
                f'<span class="dz-badge dz-badge-{st}">{stl}</span><span class="dz-dt-plan">{plan}</span>'
                f'<div class="dz-dt-mrr"><span>{mrr}</span><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:{v}%"></i></div></div>'
                f'{spark(sp, f"dzdt-tb{i}", "s1" if sp[-1] >= sp[0] else "s4", 80, 24)}<span class="dz-dt-last">{last}</span>'
                f'<a class="dz-dt-more" href="#" aria-label="Actions"><i class="fas fa-ellipsis-h"></i></a></div>')
BLOCKS.append(dict(name="tableau de données", icon="fas fa-table", html=f"""
<div class="dz-dt dz-dt-panel dz-dt-tablepanel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Comptes clients <span class="dz-badge dz-badge-neutral">248</span></h3>
      <p class="dz-dt-sub">Revenu mensuel récurrent total : 96 420 €</p>
    </div>
    <div class="dz-dt-tools">
      <div class="dz-search"><i class="fas fa-search"></i><span>Rechercher un compte…</span><span class="dz-kbd">/</span></div>
      <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="fas fa-sliders-h"></i> Filtres</a>
      <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-plus"></i> Nouveau</a>
    </div>
  </div>
  <div class="dz-dt-selbar"><span><b>1 compte sélectionné</b></span><a href="#"><i class="fas fa-tag"></i> Étiqueter</a><a href="#"><i class="fas fa-envelope"></i> Écrire</a><a href="#"><i class="fas fa-file-export"></i> Exporter</a></div>
  <div class="dz-dt-scroll">
    <div class="dz-dt-table">
      <div class="dz-dt-tr dz-dt-th"><span class="dz-dt-check"></span><span>Client</span><span>Statut</span><span>Formule</span><span class="dz-dt-sorted">Revenu mensuel <i class="fas fa-arrow-down"></i></span><span>7 derniers jours</span><span>Activité</span><span></span></div>
      {''.join(_trs)}
    </div>
  </div>
  <div class="dz-dt-pager">
    <span class="dz-dt-sub">1 – 6 sur 248 comptes</span>
    <div class="dz-dt-pages"><a href="#" aria-label="Page précédente"><i class="fas fa-chevron-left"></i></a><a class="dz-active" href="#">1</a><a href="#">2</a><a href="#">3</a><span>…</span><a href="#">42</a><a href="#" aria-label="Page suivante"><i class="fas fa-chevron-right"></i></a></div>
  </div>
</div>
"""))

# 18. tableau de bord analytics complet ------------------------------------
_d26 = [22, 26, 24, 31, 29, 35, 33, 38, 41, 37, 44, 48, 46, 52]
_d25 = [20, 21, 23, 22, 25, 24, 27, 26, 29, 28, 30, 31, 30, 33]
_mini = [(38, "2,4 k"), (52, "3,1 k"), (47, "2,8 k"), (61, "3,7 k"), (58, "3,5 k"), (72, "4,3 k"), (86, "5,2 k")]
_mb = "".join(f'<div class="dz-dt-col{" dz-active" if i == 6 else ""}" style="--v:{v}%"><span class="dz-dt-tip">{t}</span><i class="dz-dt-bar"></i><span class="dz-dt-xl">{d}</span></div>'
              for i, ((v, t), d) in enumerate(zip(_mini, ["L", "M", "M", "J", "V", "S", "D"])))
BLOCKS.append(dict(name="tableau de bord", icon="fas fa-columns", html=f"""
<div class="dz-dt dz-dt-dash">
  <div class="dz-dt-dashhead">
    <div>
      <span class="dz-eyebrow">Analytique · boutique Maison Carmin</span>
      <h2 class="dz-h3">Vue d'ensemble</h2>
    </div>
    <div class="dz-dt-tools">
      <div class="dz-dt-seg"><a href="#">Aujourd'hui</a><a class="dz-active" href="#">14 jours</a><a href="#">Trimestre</a></div>
      <a class="dz-btn dz-btn-sm dz-btn-ghost" href="#"><i class="far fa-calendar"></i> 11 – 24 sept.</a>
      <a class="dz-btn dz-btn-sm" href="#"><i class="fas fa-share-alt"></i> Partager</a>
    </div>
  </div>
  <div class="dz-dt-kpis dz-dt-kpis-mini">
    <article class="dz-dt-kpi dz-dt-s1"><div class="dz-dt-kpi-top"><span class="dz-dt-kpi-label">Revenu</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 14 %</span></div><div class="dz-dt-kpi-val">22 870 €</div>{spark(_d26, "dzdt-dk1", "s1", 120, 30)}</article>
    <article class="dz-dt-kpi dz-dt-s2"><div class="dz-dt-kpi-top"><span class="dz-dt-kpi-label">Commandes</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 9 %</span></div><div class="dz-dt-kpi-val">264</div>{spark([12, 14, 13, 17, 16, 18, 17, 19, 21, 18, 22, 24, 23, 25], "dzdt-dk2", "s2", 120, 30)}</article>
    <article class="dz-dt-kpi dz-dt-s3"><div class="dz-dt-kpi-top"><span class="dz-dt-kpi-label">Visiteurs</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 21 %</span></div><div class="dz-dt-kpi-val">9 812</div>{spark([520, 610, 580, 640, 700, 660, 720, 690, 760, 740, 800, 780, 820, 870], "dzdt-dk3", "s3", 120, 30)}</article>
    <article class="dz-dt-kpi dz-dt-s4"><div class="dz-dt-kpi-top"><span class="dz-dt-kpi-label">Remboursements</span><span class="dz-trend dz-trend-down"><i class="fas fa-arrow-up"></i> 2 %</span></div><div class="dz-dt-kpi-val">1,8 %</div>{spark([1.2, 1.3, 1.5, 1.4, 1.6, 1.5, 1.7, 1.6, 1.8, 1.7, 1.9, 1.7, 1.8, 1.8], "dzdt-dk4", "s4", 120, 30)}</article>
  </div>
  <div class="dz-dt-dashgrid">
    <div class="dz-dt-panel dz-dt-span2">
      <div class="dz-dt-head"><div><h3 class="dz-dt-title">Revenu par jour</h3><p class="dz-dt-sub">Comparé aux 14 jours précédents</p></div><div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">Période</span><span class="dz-dt-key dz-dt-s0 dz-dt-dashkey">Précédente</span></div></div>
      <div class="dz-dt-chart dz-dt-h-sm">
        {yaxis(["2,4 k", "1,8 k", "1,2 k", "600", "0"])}
        <div class="dz-dt-plot">{lines([(_d25, "s0", False, True), (_d26, "s1", True, False)], "dzdt-dash", 60)}<div class="dz-dt-xaxis"><span>11 sept.</span><span>15 sept.</span><span>19 sept.</span><span>24 sept.</span></div></div>
      </div>
    </div>
    <div class="dz-dt-panel">
      <div class="dz-dt-head"><div><h3 class="dz-dt-title">Canaux de vente</h3><p class="dz-dt-sub">Part du revenu</p></div></div>
      <div class="dz-dt-donutwrap dz-dt-donut-sm">
        <div class="dz-dt-donut" style="--p1:54%;--p2:78%;--p3:92%;--p4:100%"><div class="dz-dt-donut-c"><b>22,9 k€</b><span>total</span></div></div>
        <div class="dz-dt-dlist">
          <div class="dz-dt-drow dz-dt-s1"><span class="dz-dt-key">Site web</span><span class="dz-dt-pct">54 %</span></div>
          <div class="dz-dt-drow dz-dt-s2"><span class="dz-dt-key">Boutique</span><span class="dz-dt-pct">24 %</span></div>
          <div class="dz-dt-drow dz-dt-s3"><span class="dz-dt-key">Marketplaces</span><span class="dz-dt-pct">14 %</span></div>
          <div class="dz-dt-drow dz-dt-s4"><span class="dz-dt-key">Revendeurs</span><span class="dz-dt-pct">8 %</span></div>
        </div>
      </div>
    </div>
    <div class="dz-dt-panel">
      <div class="dz-dt-head"><div><h3 class="dz-dt-title">Produits phares</h3><p class="dz-dt-sub">Unités vendues</p></div></div>
      <div class="dz-dt-hlist dz-dt-compact">
        <div class="dz-dt-hrow"><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>Bougie Figue noire</b><span class="dz-dt-hval">142</span></div><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:100%"></i></div></div></div>
        <div class="dz-dt-hrow"><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>Diffuseur Cèdre</b><span class="dz-dt-hval">97</span></div><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:68%"></i></div></div></div>
        <div class="dz-dt-hrow"><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>Coffret Découverte</b><span class="dz-dt-hval">74</span></div><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:52%"></i></div></div></div>
        <div class="dz-dt-hrow"><div class="dz-dt-hmain"><div class="dz-dt-hlab"><b>Savon Verveine</b><span class="dz-dt-hval">58</span></div><div class="dz-dt-htrack"><i class="dz-dt-hbar" style="--v:41%"></i></div></div></div>
      </div>
    </div>
    <div class="dz-dt-panel">
      <div class="dz-dt-head"><div><h3 class="dz-dt-title">Visiteurs cette semaine</h3><p class="dz-dt-sub">24 800 · record dimanche</p></div></div>
      <div class="dz-dt-chart dz-dt-h-xs dz-dt-noy"><div class="dz-dt-plot"><div class="dz-dt-bars">{_mb}</div></div></div>
    </div>
    <div class="dz-dt-panel">
      <div class="dz-dt-head"><div><h3 class="dz-dt-title">En direct</h3><p class="dz-dt-sub">Mis à jour chaque seconde</p></div><span class="dz-dt-live"><span class="dz-dot"></span> Live</span></div>
      <div class="dz-dt-livebig"><b>37</b><span>visiteurs en ce moment</span></div>
      <div class="dz-dt-feed">
        <div class="dz-dt-ev"><i class="fas fa-shopping-bag"></i><span><b>Commande n° 10482</b> · 64,00 € · Lyon</span><time>à l'instant</time></div>
        <div class="dz-dt-ev"><i class="fas fa-cart-plus"></i><span><b>Ajout au panier</b> · Diffuseur Cèdre</span><time>12 s</time></div>
        <div class="dz-dt-ev"><i class="fas fa-user-plus"></i><span><b>Nouveau compte</b> · Rennes</span><time>48 s</time></div>
      </div>
    </div>
  </div>
</div>
"""))

# 19. temps réel -------------------------------------------------------------
_rng2 = random.Random(7)
_live = "".join(f'<i style="--v:{max(12, min(100, int(38 + 22 * __import__("math").sin(i / 5) + _rng2.uniform(-14, 18) + i * .5)))}%"></i>' for i in range(40))
BLOCKS.append(dict(name="temps réel", icon="fas fa-broadcast-tower", html=f"""
<div class="dz-dt dz-dt-panel dz-dt-realtime">
  <div class="dz-dt-head">
    <div>
      <span class="dz-dt-live"><span class="dz-dot"></span> En direct</span>
      <h3 class="dz-dt-title">Activité en temps réel</h3>
    </div>
    <span class="dz-dt-sub">Dernière mise à jour : 14:32:08</span>
  </div>
  <div class="dz-dt-rtgrid">
    <div class="dz-dt-rtmain">
      <div class="dz-dt-livebig dz-dt-livexl"><b class="dz-counter">1 248</b><span>visiteurs actifs sur le site</span></div>
      <div class="dz-dt-rtsplit">
        <div><span class="dz-dt-kpi-label"><i class="fas fa-mobile-alt"></i> Mobile</span><b>812</b></div>
        <div><span class="dz-dt-kpi-label"><i class="fas fa-desktop"></i> Ordinateur</span><b>391</b></div>
        <div><span class="dz-dt-kpi-label"><i class="fas fa-tablet-alt"></i> Tablette</span><b>45</b></div>
      </div>
      <div class="dz-dt-pulsebars">{_live}</div>
      <div class="dz-dt-pulsex"><span>il y a 40 min</span><span>maintenant</span></div>
    </div>
    <div class="dz-dt-rtside">
      <p class="dz-dt-kpi-label">Pages actives</p>
      <div class="dz-dt-active">
        <div><span class="dz-mono">/soldes-automne</span><b>386</b></div>
        <div><span class="dz-mono">/produit/bougie-figue-noire</span><b>214</b></div>
        <div><span class="dz-mono">/panier</span><b>97</b></div>
        <div><span class="dz-mono">/</span><b>88</b></div>
      </div>
      <p class="dz-dt-kpi-label">Derniers événements</p>
      <div class="dz-dt-feed">
        <div class="dz-dt-ev dz-dt-evnew"><i class="fas fa-shopping-bag"></i><span><b>Achat</b> · 128,00 € · Nantes</span><time>maintenant</time></div>
        <div class="dz-dt-ev"><i class="fas fa-user-plus"></i><span><b>Inscription</b> · newsletter</span><time>8 s</time></div>
        <div class="dz-dt-ev"><i class="fas fa-shopping-bag"></i><span><b>Achat</b> · 42,50 € · Genève</span><time>21 s</time></div>
        <div class="dz-dt-ev"><i class="fas fa-search"></i><span><b>Recherche</b> · « coffret noël »</span><time>34 s</time></div>
      </div>
    </div>
  </div>
</div>
"""))

# 20. objectifs vs réel (bullet charts) ------------------------------------
_ob = [("Chiffre d'affaires", "412 k€", "480 k€", 86, 71, "warning", "86 %"), ("Nouveaux clients", "1 284", "1 100", 100, 85, "success", "117 %"),
       ("Rétention à 90 jours", "45 %", "50 %", 90, 75, "warning", "90 %"), ("Satisfaction", "4,6 / 5", "4,5 / 5", 100, 90, "success", "102 %"),
       ("Délai de livraison", "3,1 j", "2,5 j", 64, 81, "danger", "−24 %")]
_o = "".join(f'<div class="dz-dt-orow"><div class="dz-dt-olab"><b>{lab}</b><span>{real} <em>/ objectif {goal}</em></span></div>'
             f'<div class="dz-dt-bullet" style="--v:{min(v, 100) * .92:.0f}%;--t:{t}%"><i class="dz-dt-bullet-bar dz-dt-{st}"></i><i class="dz-dt-target"></i></div>'
             f'<span class="dz-badge dz-badge-{st}">{pct}</span></div>' for lab, real, goal, v, t, st, pct in _ob)
BLOCKS.append(dict(name="objectifs vs réel", icon="fas fa-bullseye", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Objectifs du 3e trimestre</h3>
      <p class="dz-dt-sub">Au 24 septembre · 92 % du trimestre écoulé</p>
    </div>
    <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-s1">Réalisé</span><span class="dz-dt-key dz-dt-tkey">Objectif</span><span class="dz-dt-key dz-dt-bandkey">Seuils 50 / 75 / 100 %</span></div>
  </div>
  <div class="dz-dt-objs">{_o}</div>
  <div class="dz-dt-foot"><span class="dz-dt-note"><i class="fas fa-flag-checkered"></i> <b>2 objectifs atteints</b> sur 5 · 1 en retard</span><a class="dz-btn dz-btn-sm dz-btn-ghost" href="#">Voir le plan d'action</a></div>
</div>
"""))

# 21. cascade (waterfall) --------------------------------------------------
_wf = [("Juillet", 82.4, "total"), ("Nouveaux", 18.6, "up"), ("Montées", 9.2, "up"),
       ("Retours", 3.9, "up"), ("Baisses", -5.1, "down"), ("Départs", -11.8, "down"), ("Sept.", 97.2, "total")]
_w, _run = [], 0.0
for lab, x, k in _wf:
    if k == "total":
        b, v, _run = 0, x, x
        val = f"{fr(x, 1)}"
    else:
        b, v = (_run, x) if x > 0 else (_run + x, -x)
        _run += x
        val = ("+" if x > 0 else "−") + f"{fr(abs(x), 1)}"
    _w.append(f'<div class="dz-dt-wcol dz-dt-w{k}" style="--b:{b / 1.2:.1f}%;--v:{v / 1.2:.1f}%"><span class="dz-dt-wval">{val}</span><i class="dz-dt-wbar"></i><span class="dz-dt-xl">{lab}</span></div>')
_w = "".join(_w)
BLOCKS.append(dict(name="cascade", icon="fas fa-stream", html=f"""
<div class="dz-dt dz-dt-panel">
  <div class="dz-dt-head">
    <div>
      <h3 class="dz-dt-title">Évolution du revenu récurrent</h3>
      <p class="dz-dt-sub">3e trimestre 2026 · revenu mensuel récurrent, en k€</p>
    </div>
    <div class="dz-dt-figure dz-dt-right"><span class="dz-dt-big">+14,8 k€</span><span class="dz-trend dz-trend-up"><i class="fas fa-arrow-up"></i> 18,0 %</span></div>
  </div>
  <div class="dz-dt-chart dz-dt-tallx">
    {yaxis(["120 k", "90 k", "60 k", "30 k", "0"])}
    <div class="dz-dt-plot"><div class="dz-dt-bars dz-dt-waterfall">{_w}</div></div>
  </div>
  <div class="dz-dt-legend"><span class="dz-dt-key dz-dt-wk-total">Solde</span><span class="dz-dt-key dz-dt-wk-up">Hausse</span><span class="dz-dt-key dz-dt-wk-down">Baisse</span></div>
</div>
"""))
