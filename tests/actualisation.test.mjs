import assert from "node:assert/strict";
import {createRequire} from "node:module";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const require=createRequire(path.join(root,"tools/package.json"));
const {chromium}=require("playwright");
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || undefined});
try {
 const p=await browser.newPage();let demandes=0;
 await p.route("http://test.local/**",async route=>{
  if(route.request().url().includes("/dysizz/donnees/")) {
   demandes++;return route.fulfill({contentType:"application/json",body:JSON.stringify({type:"fiche",lignes:[{nom:String(demandes)}]})});
  }
  return route.fulfill({contentType:"text/html",body:'<div id="a" data-source="test" data-vue="fiche" data-champs="nom" data-rafraichir="15"></div><div id="b" data-source="test" data-vue="fiche" data-champs="nom" data-rafraichir="15"></div>'});
 });
 await p.goto("http://test.local/page/bien");
 await p.evaluate(()=>{window.handlers={};window.joins=0;window.get_shared_socket=()=>window.mockSocket||(window.mockSocket={connected:true,on:(k,fn)=>{window.handlers[k]=fn;},off:()=>{},emit:()=>{window.joins++;}});});
 await p.addScriptTag({path:path.join(root,"build/dz-w-tableau.js")});
 await p.evaluate(()=>{window.DZW.tableau(document.getElementById("a"));window.DZW.tableau(document.getElementById("b"));});
 await p.waitForFunction(()=>document.querySelectorAll(".dzw-tb-fiche").length===2);
 assert.equal(await p.evaluate(()=>window.joins),1,"une seule inscription socket pour les deux blocs");
 const before=demandes;
 await p.evaluate(()=>{for(let i=0;i<5;i++)window.handlers.dynamic_update({dzf_lecture:true});});
 await p.waitForFunction(()=>document.querySelector("#b").textContent.includes("4"));
 assert.equal(demandes,before+2,"une rafale relit chaque bloc une fois");
 const urls=[];p.on("request",r=>urls.push(r.url()));
 await p.evaluate(()=>{const i=document.createElement("input");i.id="saisie";document.getElementById("a").append(i);i.value="texte en cours";i.focus();window.dispatchEvent(new Event("dz:rafraichir"));});
 await p.waitForFunction(()=>document.querySelector("#b").textContent.includes("5"));
 assert.equal(await p.locator("#saisie").inputValue(),"texte en cours");
 assert.ok(urls.some(u=>u.includes("_dz_frais=1")),"lecture fraîche lors d'une invalidation");
 console.log("Actualisation : connexion partagée, rafale regroupée, sources fraîches, saisie conservée OK");
} finally {await browser.close();}
