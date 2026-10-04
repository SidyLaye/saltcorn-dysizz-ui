"use strict";
const assert=require("node:assert/strict"),Module=require("module"),vm=require("node:vm");
let writes=0,loads=0,broadcasts=0,assetRefreshes=0,config={custom_css:"existing",nav_menu:"thème",application_ui:""};
const backups={};
const page={name:"orders",layout:{above:[{view:"dz_ecran",configuration:{source:"orders-list",vue:"liste"}}]},min_role:40};
const state={getConfig:(k,d)=>backups[k]||d,setConfig:async(k,v)=>{backups[k]=v;},computeAssetsByRole:async()=>{assetRefreshes++;},processSend:()=>{broadcasts++;}};
const plugin={name:"dysizz-ui",get configuration(){return config;},set configuration(v){config=v;},upsert:async()=>{writes++;}};
const orig=Module._load;
Module._load=function(name,...args){
 if(name==="@saltcorn/data/models/plugin")return{find:async()=>[plugin],loadPlugin:async()=>{loads++;}};
 if(name==="@saltcorn/data/models/page")return{find:async()=>[page]};
 if(name==="@saltcorn/data/db/state")return{getState:()=>state};
 if(name==="@saltcorn/data/db")return{getTenantSchema:()=>"test"};
 if(name.startsWith("@saltcorn/"))return class{};
 return orig.call(this,name,...args);
};
const {clean,action}=require("../src/application"),{headers}=require("../src/headers");
const presentation={enabled:true,pages:{orders:{title:"Orders",sections:[{title:"Items",sources:["orders-list"]}]}}};
(async()=>{
 await assert.rejects(action.run({configuration:{operation:"activer",presentation},user:{role_id:40}}),/administrateur/);
 assert.equal(writes,0,"un rôle non admin ne modifie rien");
 const args={presentation,operation:"verifier"},user={role_id:1};
 const report=await action.run({configuration:args,user});assert.equal(report.pages[0].blocs,1);assert.equal(writes,0,"la vérification est sans écriture");
 await assert.rejects(action.run({configuration:{...args,presentation:{enabled:true,pages:{absent:{}}}},user}),/Page absente/);
 await action.run({configuration:{...args,operation:"activer"},user});assert.equal(writes,1);assert.equal(config.custom_css,"existing");assert.equal(config.nav_menu,"thème");assert.equal(page.min_role,40);
 const again=await action.run({configuration:{...args,operation:"activer"},user});assert.equal(again.deja_actif,true);assert.equal(writes,1,"relancer n'ajoute ni migration ni sauvegarde");
 assert.equal(backups.dz_application_sauvegardes.length,1);assert.equal(loads,2);
 assert.equal(broadcasts,2);assert.equal(assetRefreshes,2);assert.equal(again.cache_recharge,true,"une activation identique répare aussi les caches de présentation");
 await action.run({configuration:{operation:"restaurer"},user});assert.equal(config.application_ui,"");assert.equal(config.custom_css,"existing");
 assert.equal(clean({enabled:true,pages:JSON.parse('{"__proto__":{}}')}),null);
 const h=headers({application_ui:JSON.stringify(presentation)});assert(h.some(x=>x.css?.endsWith("dz-application.css")));assert(h.some(x=>x.script?.endsWith("dz-application.js")));
 assert(h.every(x=>!x.onlyViews&&!x.onlyFieldviews&&!x.only_if),"les fichiers et le plan de présentation sont injectés pour tous les rôles");
 assert(!headers({}).some(x=>x.css?.endsWith("dz-application.css")),"les autres tenants gardent leur présentation");
 const malicious=headers({application_ui:JSON.stringify({enabled:true,pages:{orders:{title:"</script><script>bad</script>"}}})});
 const init=malicious.find(x=>x.headerTag?.startsWith("<script>"));assert(!init.headerTag.includes("<script>bad"));
 function runAt(path){const classes=new Set(),document={documentElement:{classList:{add:k=>classes.add(k)},setAttribute:()=>{}},createElement:()=>({}),head:{appendChild:()=>{}}};const sandbox={document,location:{pathname:path},window:{},localStorage:{getItem:()=>null},setTimeout:()=>{}};vm.runInNewContext(h.find(x=>x.headerTag?.startsWith("<script>")).headerTag.slice(8,-9),sandbox);return classes;}
 assert(runAt("/page/orders").has("dz-app-ui"));assert(!runAt("/page/constructor").has("dz-app-ui"));assert(!runAt("/pageedit/orders").has("dz-app-ui"));
 console.log("Présentation : droits, validation, activation relançable, retour arrière, pages et injection sûre OK");
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(()=>{Module._load=orig;});
