"""
html2layout — transforme un morceau de HTML en éléments NATIFS du builder
Saltcorn (conteneurs, textes, liens, images), pour que chaque bloc du kit
soit modifiable sans code : clic sur un texte pour l'écrire, clic sur un
conteneur pour changer ses classes / couleurs / marges dans le panneau.

Règles (dans l'ordre) :
  - balise « technique » (svg, video, iframe, form, input, select, table…)
    ou attribut sans équivalent en classe  → reste en bloc HTML (code) ;
  - <img> pleine largeur                  → élément Image ;
  - <a> au contenu simple                 → élément Lien (bouton, lien) ;
  - <a> au contenu riche (carte cliquable) → conteneur avec lien ;
  - h1…h6 au texte simple                 → élément Texte, style de titre ;
  - <span> au texte simple                → élément Texte (span + classes) ;
  - autre balise au texte simple          → conteneur (même balise) + Texte ;
  - le reste                              → conteneur (même balise, classes,
                                            id, style) + enfants convertis.
Les attributs data-dz-* sont traduits en classes équivalentes (voir
client/dz.js, section « classes sans code »).
"""
from html.parser import HTMLParser
from html import escape, unescape
import re

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
INLINE = {"a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn", "em", "i", "kbd", "mark", "q", "s",
          "samp", "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr", "del", "ins", "img"}
RAW_TAGS = {"svg", "video", "audio", "iframe", "canvas", "form", "input", "select", "textarea", "table", "picture",
            "script", "style", "template", "dialog", "object", "embed", "math", "noscript", "progress", "meter",
            "option", "optgroup", "datalist", "output", "map", "area", "source", "track"}
DROP_ATTRS = {"aria-hidden", "loading", "decoding", "type", "tabindex"}
FLAG_ATTRS = {
    "data-dz-theme-toggle": "dz-theme-toggle", "data-dz-dismiss": "dz-dismiss", "data-dz-confetti": "dz-confetti",
    "data-dz-tilt": "dz-tilt", "data-dz-menu-toggle": "dz-menu-toggle", "data-dz-cmdk-open": "dz-cmdk-open",
    "data-dz-autoplay": "dz-tabs-auto", "data-dz-hscroll": "dz-hscroll", "data-dz-slider": "dz-slider",
    "data-dz-close": "dz-close", "data-dz-lightbox": "dz-zoomable", "data-dz-words": "dz-words",
    "data-dz-split": "dz-letters", "data-dz-magnetic": "dz-magnetic",
}
FULL_WIDTH_IMG = {"w-100", "img-fluid", "dz-cover", "dz-img", "dz-media-img"}


class Node:
    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def cls(self):
        return (self.attrs.get("class") or "").split()


class _P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("#root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, [(k, v if v is not None else "") for k, v in attrs])
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, [(k, v if v is not None else "") for k, v in attrs]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, d):
        self.stack[-1].children.append(d)

    def handle_entityref(self, name):
        self.stack[-1].children.append(f"&{name};")

    def handle_charref(self, name):
        self.stack[-1].children.append(f"&#{name};")

    def handle_comment(self, data):
        pass


def parse(html):
    p = _P()
    p.feed(html)
    p.close()
    return p.root


def ser(n):
    if isinstance(n, str):
        return n
    a = "".join(f' {k}="{escape(v, quote=True)}"' for k, v in n.attrs.items())
    if n.tag in VOID:
        return f"<{n.tag}{a}>"
    return f"<{n.tag}{a}>{''.join(ser(c) for c in n.children)}</{n.tag}>"


def inner(n):
    return "".join(ser(c) for c in n.children)


def text_only(n):
    """vrai si tous les descendants sont du texte ou des balises en ligne simples"""
    for c in n.children:
        if isinstance(c, str):
            continue
        if c.tag not in INLINE or c.tag in RAW_TAGS:
            return False
        if c.tag == "img":
            return False
        if any(k.startswith("data-") for k in c.attrs):
            return False  # comportement à traduire en classe : l'enfant devient un élément à part
        if not text_only(c):
            return False
    return True


def fmt_number(v, decimals=0):
    x = float(v)
    s = f"{x:,.{decimals}f}".replace(",", " ").replace(".", ",")
    return s


def map_attrs(n):
    """traduit les attributs en classes ; renvoie (classes, id, style, extra) ou None si impossible"""
    classes = n.cls()
    extra = {}
    style = n.attrs.get("style", "")
    nid = n.attrs.get("id")
    text_override = None
    for k, v in n.attrs.items():
        if k in ("class", "style", "id") or k in DROP_ATTRS:
            continue
        if k == "role" and v in ("presentation", "none"):
            continue
        if k in FLAG_ATTRS:
            classes.append(FLAG_ATTRS[k])
        elif k == "data-dz-copy" and v == "":
            classes.append("dz-copy")
        elif k == "data-dz-reveal":
            classes.append(f"dz-reveal-{v or 'up'}")
        elif k == "data-dz-open" and v.startswith("#") and re.match(r"^#[A-Za-z][\w-]*$", v):
            classes.append(f"dz-open-{v[1:]}")
        elif k == "data-dz-value" and "dz-progress" in classes and v.isdigit():
            classes.append(f"dz-progress-{v}")
        elif k == "data-dz-parallax":
            try:
                f = float(v or 0.2)
            except ValueError:
                return None
            classes.append("dz-parallax" if 0.15 <= f <= 0.25 else "dz-parallax-slow" if 0 < f < 0.15 else "dz-parallax-fast" if f > 0.25 else "dz-parallax-reverse")
        elif k == "data-dz-count":
            dec = int(n.attrs.get("data-dz-decimals", "0") or 0)
            text_override = n.attrs.get("data-dz-prefix", "") + fmt_number(v, dec) + n.attrs.get("data-dz-suffix", "")
            classes.append("dz-counter")
        elif k in ("data-dz-suffix", "data-dz-prefix", "data-dz-decimals") and "data-dz-count" in n.attrs:
            continue
        elif k == "data-dz-typed":
            text_override = " | ".join(w.strip() for w in v.split("|"))
            classes.append("dz-typewriter")
        elif k == "href" and n.tag == "a":
            extra["href"] = v
        elif k == "target" and n.tag == "a":
            extra["target"] = v
        elif k == "rel" and n.tag == "a":
            continue
        elif k == "alt" and n.tag == "img":
            extra["alt"] = v
        elif k == "src" and n.tag == "img":
            extra["src"] = v
        elif k == "title":
            extra["title"] = v
        elif k == "aria-label":
            extra["aria"] = v
        else:
            return None  # attribut sans équivalent : on garde le HTML
    seen = []
    for c in classes:
        if c not in seen:
            seen.append(c)
    return seen, nid, style, extra, text_override


def css_obj(style):
    out = {}
    for decl in style.split(";"):
        if ":" in decl:
            k, v = decl.split(":", 1)
            if k.strip():
                out[k.strip()] = v.strip()
    return out


def raw(n):
    return {"type": "blank", "isHTML": True, "contents": ser(n) if not isinstance(n, str) else n}


def txt(contents, cls=None, style=None, text_style=None, block=False):
    seg = {"type": "blank", "contents": contents}
    if cls:
        seg["customClass"] = cls
    if style:
        seg["style"] = css_obj(style)
    if text_style:
        seg["textStyle"] = text_style
    if block:
        seg["block"] = True
    return seg


def container(tag, classes, nid, style, contents, url=None):
    seg = {"type": "container", "contents": contents}
    if tag != "div":
        seg["htmlElement"] = tag
    if classes:
        seg["customClass"] = " ".join(classes)
    if nid:
        seg["customId"] = nid
    if style:
        seg["customCSS"] = style.strip().rstrip(";")
    if url:
        seg["url"] = url
    return seg


def sr(label):
    """texte lu par les lecteurs d'écran, invisible à l'écran (remplace aria-label)"""
    return f'<span class="visually-hidden">{escape(label)}</span>'


def pack(segs):
    segs = [s for s in segs if s is not None]
    if not segs:
        return ""
    return segs[0] if len(segs) == 1 else {"above": segs}


def conv(n):
    if isinstance(n, str):
        return txt(n) if n.strip() else None
    if n.tag in RAW_TAGS:
        return raw(n)
    if n.tag in ("br", "wbr", "hr") and not n.attrs:
        return txt(f"<{n.tag}>")
    m = map_attrs(n)
    if m is None:
        return raw(n)
    classes, nid, style, extra, text_override = m
    cls = " ".join(classes)
    body = text_override if text_override is not None else None

    if n.tag == "img":
        if set(classes) & FULL_WIDTH_IMG or not classes:
            seg = {"type": "image", "srctype": "URL", "url": extra.get("src", ""), "alt": extra.get("alt", "")}
            if cls:
                seg["customClass"] = cls
            if style:
                seg["style"] = css_obj(style)
            return seg
        return raw(n)

    if n.tag == "a":
        href = extra.get("href", "#")
        kids = [c for c in n.children if not (isinstance(c, str) and not c.strip())]
        if text_only(n) and not nid and not style and not extra.get("aria"):
            icon = None
            label_nodes = list(n.children)
            first = next((c for c in label_nodes if not (isinstance(c, str) and not c.strip())), None)
            if isinstance(first, Node) and first.tag == "i" and not first.children and len(first.attrs) == 1:
                icon = first.attrs.get("class")
                label_nodes = label_nodes[label_nodes.index(first) + 1:]
            label = (body if body is not None else "".join(ser(c) for c in label_nodes)).strip()
            if "<" not in label and "<" not in unescape(label):
                label = unescape(label)
                # classes dans link_style : c'est ce que l'aperçu du builder affiche
                seg = {"type": "link", "text": label or " ", "url": href, "link_style": cls}
                if icon:
                    seg["link_icon"] = icon
                if extra.get("target") == "_blank":
                    seg["target_blank"] = True
                if extra.get("title"):
                    seg["link_title"] = extra["title"]
                return seg
        if extra.get("title"):
            return raw(n)
        pre = [txt(sr(extra["aria"]))] if extra.get("aria") else []
        return container("a", classes, nid, style, pack(pre + [conv(c) for c in kids]), url=href)

    if extra.get("title"):
        return raw(n)

    if text_only(n) or body is not None:
        content = body if body is not None else inner(n).strip()
        if extra.get("aria"):
            content = sr(extra["aria"]) + content
        if re.fullmatch(r"h[1-6]", n.tag) and not nid:
            return txt(content, cls, style, text_style=n.tag)
        if n.tag == "span" and not nid:
            if not cls and not style:
                return container("span", [], None, "", txt(content) if content else "")
            return txt(content, cls, style)
        return container(n.tag, classes, nid, style, txt(content) if content else "")

    kids = [c for c in n.children if not (isinstance(c, str) and not c.strip())]
    pre = [txt(sr(extra["aria"]))] if extra.get("aria") else []
    return container(n.tag, classes, nid, style, pack(pre + [conv(c) for c in kids]))


def html2layout(html):
    root = parse(html)
    kids = [c for c in root.children if not (isinstance(c, str) and not c.strip())]
    return pack([conv(c) for c in kids])


def convert_layout(layout):
    """remplace, dans une mise en page, chaque bloc HTML (isHTML) par des éléments natifs,
    sauf ceux marqués dz_raw"""
    if isinstance(layout, list):
        return [convert_layout(x) for x in layout]
    if not isinstance(layout, dict):
        return layout
    if layout.get("type") == "blank" and layout.get("isHTML") and not layout.get("dz_raw"):
        conv_ = html2layout(layout.get("contents", ""))
        return conv_ if conv_ != "" else layout
    out = dict(layout)
    if out.get("type") == "link" and out.get("link_class") and not out.get("link_style"):
        out["link_style"], out["link_class"] = out["link_class"], ""
    for k in ("contents", "above", "besides"):
        if k in out and not isinstance(out[k], str):
            out[k] = convert_layout(out[k])
    return out


if __name__ == "__main__":
    import json, sys
    print(json.dumps(html2layout(sys.stdin.read()), indent=1, ensure_ascii=False))
