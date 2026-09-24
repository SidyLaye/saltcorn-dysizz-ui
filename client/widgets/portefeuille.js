/* Portefeuille crypto : connexion (MetaMask, Rabby, Coinbase Wallet… via
   EIP-6963 / window.ethereum), adresse, solde, changement de réseau,
   signature d'un message (preuve de propriété) et envoi d'un paiement. */
import { register, css, h, conf, champ, btn, toast } from "./_commun.js";

css("portefeuille", `.dzw-wal .dzw-wal-body{padding:16px;display:grid;gap:12px}
.dzw-wal .dzw-wal-addr{font-family:ui-monospace,monospace;font-size:.9rem;word-break:break-all}
.dzw-wal .dzw-wal-bal{font-size:1.8rem;font-weight:700;font-variant-numeric:tabular-nums}
.dzw-wal .dzw-wal-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dzw-wal .dzw-wal-list{display:grid;gap:8px}
.dzw-wal .dzw-wal-list button{display:flex;align-items:center;gap:10px;justify-content:flex-start;width:100%;padding:10px 12px}
.dzw-wal .dzw-wal-list img{width:26px;height:26px;border-radius:6px}`);

const CHAINS = { 1: ["Ethereum", "ETH", "https://etherscan.io"], 137: ["Polygon", "POL", "https://polygonscan.com"], 8453: ["Base", "ETH", "https://basescan.org"], 42161: ["Arbitrum", "ETH", "https://arbiscan.io"], 10: ["Optimism", "ETH", "https://optimistic.etherscan.io"], 56: ["BNB Chain", "BNB", "https://bscscan.com"], 43114: ["Avalanche", "AVAX", "https://snowtrace.io"], 100: ["Gnosis", "xDAI", "https://gnosisscan.io"], 11155111: ["Sepolia (test)", "ETH", "https://sepolia.etherscan.io"] };
const fromWei = (hex, dec = 18) => { const b = BigInt(hex); const d = 10n ** BigInt(dec); const f = (b % d).toString().padStart(dec, "0").slice(0, 5).replace(/0+$/, ""); return (b / d).toString() + (f ? "," + f : ""); };
const toWeiHex = (v) => { const [i, f = ""] = String(v).replace(",", ".").split("."); return "0x" + (BigInt(i || "0") * 10n ** 18n + BigInt((f + "0".repeat(18)).slice(0, 18))).toString(16); };

/* portefeuilles annoncés par EIP-6963 (plusieurs extensions à la fois) */
const providers = [];
window.addEventListener("eip6963:announceProvider", (e) => { if (!providers.some((p) => p.info.uuid === e.detail.info.uuid)) providers.push(e.detail); });
window.dispatchEvent(new Event("eip6963:requestProvider"));

register("portefeuille", (el) => {
  const c = champ(el);
  const reseau = conf(el, "reseau", 0);
  el.classList.add("dzw", "dzw-wal");
  el.innerHTML = "";
  const body = h("div", { class: "dzw-wal-body" });
  el.append(h("div", { class: "dzw-bar" }, h("i", { class: "fas fa-wallet" }), h("b", {}, conf(el, "titre", "Portefeuille")), h("span", { class: "dzw-sp" })), body);
  let prov = null, addr = null, chain = null;
  const req = (method, params = []) => prov.request({ method, params });
  const show = async () => {
    body.innerHTML = "";
    if (!addr) {
      const list = providers.length ? providers : window.ethereum ? [{ info: { name: "Portefeuille du navigateur", icon: "" }, provider: window.ethereum }] : [];
      if (!list.length) { body.append(h("p", {}, "Aucun portefeuille trouvé dans ce navigateur."), h("a", { href: "https://metamask.io/download/", target: "_blank", rel: "noopener", class: "dzw-b" }, "Installer MetaMask")); return; }
      body.append(h("p", { class: "dzw-note" }, "Choisis ton portefeuille :"), h("div", { class: "dzw-wal-list" }, ...list.map((p) => h("button", { type: "button", class: "dzw-b", onclick: () => connect(p.provider) }, p.info.icon ? h("img", { src: p.info.icon, alt: "" }) : h("i", { class: "fas fa-wallet" }), p.info.name))));
      return;
    }
    const [nom, sym, scan] = CHAINS[chain] || [`Réseau ${chain}`, "", ""];
    let bal = "…";
    try { bal = fromWei(await req("eth_getBalance", [addr, "latest"])); } catch (e) { bal = "?"; }
    const montant = h("input", { type: "text", placeholder: "Montant", style: { width: "110px" } });
    const vers = h("input", { type: "text", placeholder: "Adresse 0x… du destinataire", value: conf(el, "destinataire", ""), style: { flex: "1", minWidth: "200px" } });
    body.append(
      h("div", { class: "dzw-wal-row" }, h("span", { class: "badge text-bg-light" }, nom), h("span", { class: "dzw-note" }, "connecté")),
      h("div", { class: "dzw-wal-addr" }, scan ? h("a", { href: `${scan}/address/${addr}`, target: "_blank", rel: "noopener" }, addr) : addr),
      h("div", { class: "dzw-wal-bal" }, `${bal} ${sym}`),
      h("div", { class: "dzw-wal-row" }, btn("fas fa-copy", "Copier l'adresse", () => navigator.clipboard.writeText(addr).then(() => toast("Adresse copiée", "success"))), btn("fas fa-signature", "Prouver que c'est moi", signer), reseau && +reseau !== chain ? btn("fas fa-random", `Passer sur ${(CHAINS[reseau] || [reseau])[0]}`, () => changer(+reseau)) : null, btn("fas fa-sign-out-alt", "Déconnecter", () => { addr = null; show(); })),
      conf(el, "paiement", false) ? h("div", { class: "dzw-wal-row" }, vers, montant, h("span", {}, sym), btn("fas fa-paper-plane", "Envoyer", () => payer(vers.value.trim(), montant.value.trim()))) : null,
    );
  };
  const connect = async (p) => {
    prov = p;
    try {
      [addr] = await req("eth_requestAccounts");
      chain = Number(await req("eth_chainId"));
      p.on && p.on("accountsChanged", (a) => { addr = a[0] || null; show(); });
      p.on && p.on("chainChanged", (x) => { chain = Number(x); show(); });
      if (c.input && !conf(el, "signer-auto", false)) c.set(addr);
      if (conf(el, "signer-auto", false)) await signer();
      show();
    } catch (e) { toast("Connexion refusée : " + (e.message || e), "warning"); }
  };
  const changer = async (id) => { try { await req("wallet_switchEthereumChain", [{ chainId: "0x" + id.toString(16) }]); } catch (e) { toast("Changement de réseau refusé : " + e.message, "warning"); } };
  /* message signé : le serveur le vérifie avec le bloc flow « signer / vérifier un message » */
  const signer = async () => {
    const msg = `${location.host} te demande de prouver que tu possèdes cette adresse.\n\nAdresse : ${addr}\nDate : ${new Date().toISOString()}\nCode : ${Math.random().toString(36).slice(2, 10)}`;
    try { const sig = await req("personal_sign", [msg, addr]); if (c.input) c.set(JSON.stringify({ adresse: addr, message: msg, signature: sig })); toast("Message signé", "success"); el.dispatchEvent(new CustomEvent("dz-signature", { detail: { adresse: addr, message: msg, signature: sig }, bubbles: true })); }
    catch (e) { toast("Signature refusée", "warning"); }
  };
  const payer = async (to, v) => {
    if (!/^0x[0-9a-fA-F]{40}$/.test(to)) return toast("Adresse du destinataire invalide", "warning");
    if (!(+String(v).replace(",", ".") > 0)) return toast("Montant invalide", "warning");
    try { const hash = await req("eth_sendTransaction", [{ from: addr, to, value: toWeiHex(v) }]); const scan = (CHAINS[chain] || [])[2]; toast("Paiement envoyé", "success"); body.append(h("div", { class: "dzw-note" }, "Transaction : ", scan ? h("a", { href: `${scan}/tx/${hash}`, target: "_blank", rel: "noopener" }, hash.slice(0, 18) + "…") : hash)); el.dispatchEvent(new CustomEvent("dz-paiement", { detail: { hash, chain }, bubbles: true })); }
    catch (e) { toast("Paiement annulé : " + (e.message || e), "warning"); }
  };
  setTimeout(show, 150);
});
