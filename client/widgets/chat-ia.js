/* Chat IA : une fenêtre de discussion reliée à un point d'API dysizz-flow
   (modèle « Assistant IA pour tes pages ») ou à toute adresse qui renvoie
   { reponse }. En bulle flottante ou intégré dans la page. */
import { register, css, h, conf, esc } from "./_commun.js";

css("chat-ia", `.dzw-chat{display:flex;flex-direction:column;height:var(--h,460px)}
.dzw-chat .dzw-chat-log{flex:1;overflow:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:var(--dz-surface-2,#f8fafc)}
.dzw-chat .m{max-width:85%;padding:9px 12px;border-radius:14px;line-height:1.45;font-size:.93rem;white-space:normal;word-wrap:break-word}
.dzw-chat .m.moi{align-self:flex-end;background:var(--dz-primary,#2563eb);color:#fff;border-bottom-right-radius:4px}
.dzw-chat .m.ia{align-self:flex-start;background:var(--dz-surface,#fff);border:1px solid var(--dz-border,#e5e7eb);border-bottom-left-radius:4px}
.dzw-chat .m.err{border-color:#fca5a5;color:#b91c1c}
.dzw-chat .m p{margin:0 0 6px}.dzw-chat .m p:last-child{margin:0}
.dzw-chat .m code{background:rgba(0,0,0,.06);padding:1px 4px;border-radius:4px}
.dzw-chat .m ul{margin:4px 0;padding-left:18px}
.dzw-chat .dots span{display:inline-block;width:6px;height:6px;margin:0 2px;border-radius:50%;background:currentColor;opacity:.4;animation:dzwdot 1s infinite}
.dzw-chat .dots span:nth-child(2){animation-delay:.15s}.dzw-chat .dots span:nth-child(3){animation-delay:.3s}
@keyframes dzwdot{50%{opacity:1;transform:translateY(-3px)}}
.dzw-chat form{display:flex;gap:8px;padding:10px;border-top:1px solid var(--dz-border,#e5e7eb)}
.dzw-chat textarea{flex:1;resize:none;border:1px solid var(--dz-border,#e5e7eb);border-radius:10px;padding:8px 10px;font:inherit;max-height:120px;background:var(--dz-surface,#fff);color:inherit}
.dzw-chat .sugg{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px;background:var(--dz-surface-2,#f8fafc)}
.dzw-chat .sugg button{border:1px solid var(--dz-border,#e5e7eb);background:var(--dz-surface,#fff);border-radius:999px;padding:4px 10px;font-size:.82rem;cursor:pointer;color:inherit}
.dzw-chat-bulle{position:fixed;right:18px;bottom:18px;z-index:1040;width:56px;height:56px;border-radius:50%;border:0;background:var(--dz-primary,#2563eb);color:#fff;font-size:1.4rem;box-shadow:0 8px 24px rgba(0,0,0,.2);cursor:pointer}
.dzw-chat-pop{position:fixed;right:18px;bottom:86px;z-index:1040;width:min(380px,calc(100vw - 24px));box-shadow:0 18px 50px rgba(0,0,0,.22);display:none}
.dzw-chat-pop.on{display:flex}`);

/* Markdown très simple (gras, code, listes, liens), texte échappé d'abord */
const md = (t) => {
  const lines = esc(t).split("\n"); let html = "", list = false;
  for (const l of lines) {
    const m = l.match(/^\s*[-*•]\s+(.*)/);
    if (m) { if (!list) { html += "<ul>"; list = true; } html += `<li>${inl(m[1])}</li>`; continue; }
    if (list) { html += "</ul>"; list = false; }
    if (l.trim()) html += `<p>${inl(l)}</p>`;
  }
  return html + (list ? "</ul>" : "");
};
const inl = (s) => s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+|\/[^)\s]*)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

register("chat-ia", (el) => {
  const url = conf(el, "url", "/dzf/api/assistant");
  const flottant = conf(el, "flottant", false);
  el.innerHTML = "";
  const box = flottant ? h("div", { class: "dzw dzw-chat dzw-chat-pop" }) : el;
  box.classList.add("dzw", "dzw-chat");
  box.style.setProperty("--h", conf(el, "hauteur", 460) + "px");
  const log = h("div", { class: "dzw-chat-log", "aria-live": "polite" });
  const ta = h("textarea", { rows: 1, placeholder: conf(el, "placeholder", "Écris ta question…") });
  const send = h("button", { type: "submit", class: "dzw-b on", title: "Envoyer" }, h("i", { class: "fas fa-paper-plane" }));
  const form = h("form", {}, ta, send);
  const historique = [];
  const bulle = (txt, qui, err) => { const m = h("div", { class: `m ${qui}${err ? " err" : ""}` }); m.innerHTML = qui === "ia" ? md(txt) : esc(txt).replace(/\n/g, "<br>"); log.append(m); log.scrollTop = log.scrollHeight; return m; };
  const sugg = h("div", { class: "sugg" }, ...conf(el, "suggestions", []).map((s) => h("button", { type: "button", onclick: () => { ta.value = s; form.requestSubmit(); } }, s)));
  bulle(conf(el, "accueil", "Bonjour ! Pose-moi une question."), "ia");
  let busy = false;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = ta.value.trim(); if (!q || busy) return;
    busy = true; send.disabled = true; ta.value = ""; sugg.remove();
    bulle(q, "moi");
    const wait = h("div", { class: "m ia dots" }, h("span"), h("span"), h("span")); log.append(wait); log.scrollTop = log.scrollHeight;
    try {
      const r = await fetch(url, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-Requested-With": "dysizz" }, body: JSON.stringify({ message: q, historique: historique.slice(-10) }) });
      const j = await r.json().catch(() => null);
      wait.remove();
      if (!r.ok) throw new Error((j && j.erreur) || `erreur ${r.status}`);
      const rep = typeof j === "string" ? j : (j && (j.reponse || j.message || j.texte)) || JSON.stringify(j);
      bulle(rep, "ia");
      historique.push({ role: "user", content: q }, { role: "assistant", content: rep });
    } catch (err) { wait.remove(); bulle("Je n'ai pas pu répondre : " + err.message, "ia", true); }
    busy = false; send.disabled = false; ta.focus();
  });
  ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
  ta.addEventListener("input", () => { ta.style.height = "auto"; ta.style.height = Math.min(120, ta.scrollHeight) + "px"; });
  box.append(h("div", { class: "dzw-bar" }, h("i", { class: "fas fa-robot" }), h("b", {}, conf(el, "titre", "Assistant")), h("span", { class: "dzw-sp" }), flottant ? h("button", { type: "button", class: "dzw-b", title: "Fermer", onclick: () => box.classList.remove("on") }, h("i", { class: "fas fa-times" })) : null), log, sugg, form);
  if (flottant) {
    document.body.append(box, h("button", { type: "button", class: "dzw-chat-bulle", title: "Assistant", onclick: () => { box.classList.toggle("on"); if (box.classList.contains("on")) ta.focus(); } }, h("i", { class: "fas fa-comment-dots" })));
  }
});
