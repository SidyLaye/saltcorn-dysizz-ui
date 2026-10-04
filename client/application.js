/* Ergonomie d'application. Les sources, les formulaires et les actions restent natifs. */
(() => {
 "use strict";
 const plan=window.__dzApplication;
 if(!plan||!document.documentElement.classList.contains('dz-app-ui'))return;
 const store={get:k=>{try{return localStorage.getItem(k);}catch{return null;}},set:(k,v)=>{try{localStorage.setItem(k,v);}catch{}}};
 const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text!=null)el.textContent=text;return el;};
 const decode=s=>{const t=document.createElement('textarea');t.innerHTML=s||'';return t.value;};
 const tableState=new WeakMap();
 let content;
 function dialog(title){
  const origin=document.activeElement,overlay=node('div','ux-dialog'),panel=node('div','panel'),heading=node('h2','',title),close=node('button','','Fermer');
  heading.id='dz-app-dialog-title';close.type='button';panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');panel.setAttribute('aria-labelledby',heading.id);
  panel.append(heading,close);overlay.append(panel);document.body.append(overlay);
  const finish=()=>{overlay.remove();if(origin?.isConnected)origin.focus();};close.onclick=finish;overlay.onclick=e=>{if(e.target===overlay)finish();};close.focus();
  overlay.onkeydown=e=>{if(e.key==='Escape')finish();if(e.key==='Tab'){const controls=[...panel.querySelectorAll('button,input,a[href],select')].filter(x=>!x.disabled&&!x.hidden),i=controls.indexOf(document.activeElement);if(e.shiftKey&&i===0){e.preventDefault();controls.at(-1).focus();}else if(!e.shiftKey&&i===controls.length-1){e.preventDefault();controls[0].focus();}}};
  return {panel,close};
 }
 function arrange(){
  const widgets=[...document.querySelectorAll('[data-dz-widget="tableau"],[data-dz-widget="fiche"]')].filter(w=>!w.closest('.dz-builder,.navbar,.modal'));
  if(!widgets.length)return false;
  let original=widgets[0].parentElement;
  while(original!==document.body&&!widgets.every(w=>original.contains(w)))original=original.parentElement;
  if(original===document.body)original=document.getElementById('page-inner-content')||document.querySelector('main');
  if(!original||!widgets.every(w=>original.contains(w)))return false;
  const heading=[...original.querySelectorAll('h1')].find(h=>!h.closest('[data-dz-widget]'));
  const back=[...original.querySelectorAll('a[href]')].find(a=>!a.closest('[data-dz-widget]')&&/^\s*←/.test(a.textContent));
  content=node('div','dz-app-content');
  original.prepend(content);document.body.dataset.dzAppLayout=plan.layout;
  if(back){back.classList.add('ux-back');content.append(back);}
  const head=node('div','ux-screen-head'),kpis=node('div','ux-kpi-row'),filters=[],rest=[];
  const hasTitle=widgets.some(w=>w.dataset.vue==='titre');
  if(heading){const wrap=heading.closest('.dz-ecran-titre')||heading;if(hasTitle)wrap.hidden=true;else {if(plan.title)heading.textContent=plan.title;content.append(wrap);}}
  else if(!hasTitle&&plan.title)content.append(node('h1','dz-ecran-titre',plan.title));
  content.append(head);
  for(const w of widgets){
   if(plan.inline_sources.includes(w.dataset.source)){w.classList.add('dz-app-kpi-inline');content.append(w);}
   else if(w.dataset.vue==='titre')head.append(w);
   else if(w.dataset.vue==='filtres')filters.push(w);
   else if(w.dataset.vue==='kpi')kpis.append(w);
   else rest.push(w);
  }
  if(kpis.children.length){kpis.style.setProperty('--dz-app-kpis',Math.min(4,kpis.children.length));content.append(kpis);}
  content.append(...filters);
  if(plan.sections.length){
   const tabs=node('div','ux-screen-tabs');tabs.setAttribute('role','tablist');tabs.setAttribute('aria-label','Rubriques');content.append(tabs);
   const assigned=new Set(),panels=[];
   plan.sections.forEach((s,i)=>{
    const tab=node('button','',s.title),panel=node('section','ux-screen-panel'),grid=node('div','ux-screen-grid'+(plan.charts?' ux-charts-grid':''));tab.type='button';tab.id='dz-app-tab-'+i;panel.id='dz-app-panel-'+i;
    tab.setAttribute('role','tab');tab.setAttribute('aria-controls',panel.id);panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',tab.id);
    for(const w of rest)if(!assigned.has(w)&&s.sources.includes(w.dataset.source)){grid.append(w);assigned.add(w);}
    panel.append(grid);panels.push({tab,panel,grid});tabs.append(tab);content.append(panel);
   });
   rest.filter(w=>!assigned.has(w)).forEach(w=>panels[0].grid.append(w));
   const activate=(i,focus=false,write=true)=>{panels.forEach((p,j)=>{p.tab.setAttribute('aria-selected',String(i===j));p.tab.tabIndex=i===j?0:-1;p.panel.hidden=i!==j;});if(focus)panels[i].tab.focus();if(write){const u=new URL(location.href);u.searchParams.set('section',String(i));history.replaceState(null,'',u);}};
   const current=()=>{const i=Number(new URLSearchParams(location.search).get('section')||0);return Number.isInteger(i)&&i>=0&&i<panels.length?i:0;};
   panels.forEach((p,i)=>{p.tab.onclick=()=>activate(i);p.tab.onkeydown=e=>{const visible=panels.map((p,j)=>p.tab.hidden?null:j).filter(j=>j!=null),at=visible.indexOf(i),keys={ArrowRight:visible[(at+1)%visible.length],ArrowLeft:visible[(at+visible.length-1)%visible.length],Home:visible[0],End:visible.at(-1)};if(keys[e.key]!=null){e.preventDefault();activate(keys[e.key],true);}};});
   activate(current(),false,false);window.addEventListener('popstate',()=>activate(current(),false,false));
   content.dzAppPruneTabs=()=>{
    panels.forEach(p=>{p.tab.hidden=!!p.grid.children.length&&[...p.grid.children].every(w=>w.hidden);});
    const selected=panels.findIndex(p=>p.tab.getAttribute('aria-selected')==='true');
    if(panels[selected]?.tab.hidden){const first=panels.findIndex(p=>!p.tab.hidden);if(first>=0)activate(first,false,false);}
   };
  }else{const stack=node('div','dz-app-stack');stack.append(...rest);content.append(stack);}
  // Existing content other than the data widgets is retained, including native links/forms.
  for(const intro of [...original.querySelectorAll('.dz-ecran-intro,.dz-ecran-note')]){
   if(content.contains(intro)||intro.querySelector('[data-dz-widget],form,input,button,a'))continue;
   intro.classList.add('page-intro');
   if(/Cliquez une ligne|Cliquez une personne|Page réservée/.test(intro.textContent))intro.hidden=true;
   else if(intro.textContent.trim())head.append(intro);
  }
  for(const child of [...original.children])if(child!==content){child.dataset.dzAppPreserved='1';if(!child.textContent.trim()&&!child.querySelector('a[href],button,form,input,select,textarea,img,iframe'))child.hidden=true;}
  return true;
 }
 function refine(){
  const tones={'#047857':'success','#b45309':'warning','#b91c1c':'danger','#1d4ed8':'info','#6d28d9':'violet','#64748b':'neutral','#000000':'text'};
  content.querySelectorAll('[data-vue=titre] p').forEach(p=>{const next=p.textContent.replace(/\s*·\s*product_id\s+\S+/g,'').replace(/\s*·\s*\d{5,}\s*$/,'');if(next!==p.textContent)p.textContent=next;});
  content.querySelectorAll('[style]').forEach(el=>{const color=(el.getAttribute('style')||'').match(/(?:--c|(?:^|;)\s*color)\s*:\s*(#[\da-f]{6})/i)?.[1]?.toLowerCase();if(tones[color])el.dataset.tone=tones[color];});
  content.querySelectorAll('.dzw-tb-fiche dd').forEach(dd=>{const v=dd.textContent.trim();if(v==='true'||v==='false')dd.textContent=dd.previousElementSibling?.textContent.trim()==='Statut web'?(v==='true'?'Publié':'Non publié'):(v==='true'?'Oui':'Non');});
  content.querySelectorAll('.page-intro').forEach(text=>{if(text.dataset.dzAppConcise)return;text.dataset.dzAppConcise='1';if(text.textContent.length>170){const d=node('details','ux-context-help'),s=node('summary','',/Les taux suivent/.test(text.textContent)?'Comprendre les indicateurs':'Comment ça fonctionne ?');text.before(d);d.append(s,text);}});
  content.querySelectorAll('.dzw-tb-filtres').forEach(bar=>{
   if(bar.dataset.dzAppOrganised)return;bar.dataset.dzAppOrganised='1';
   const widget=bar.closest('[data-dz-widget]');let defs=[];try{defs=JSON.parse(widget?.dataset.champs||'[]');}catch{}
   if(!Array.isArray(defs))return;
   if(defs.some(c=>c.type==='boutons')){
    const group=bar.querySelector('[role="group"]');if(!group)return;bar.classList.add('ux-tabs');group.setAttribute('role','tablist');group.setAttribute('aria-label','Rubriques');
    [...group.children].forEach((b,i)=>{b.setAttribute('role','tab');b.setAttribute('aria-selected',String(b.classList.contains('on')));b.tabIndex=b.classList.contains('on')?0:-1;b.addEventListener('keydown',e=>{const keys={ArrowRight:(i+1)%group.children.length,ArrowLeft:(i+group.children.length-1)%group.children.length,Home:0,End:group.children.length-1};if(keys[e.key]!=null){e.preventDefault();group.children[keys[e.key]].focus();group.children[keys[e.key]].click();}});});return;
   }
   const fields=[...bar.children].filter(el=>el.tagName==='LABEL');if(fields.length<5)return;
   const primary=node('div','ux-filter-primary'),panel=node('details','ux-filter-panel'),summary=node('summary');panel.append(summary);
   const key='dz-app-filters:'+location.pathname+':'+(widget?.dataset.montrer||widget?.dataset.champs||'').slice(0,170);
   try{panel.open=sessionStorage.getItem(key)==='open';panel.ontoggle=()=>sessionStorage.setItem(key,panel.open?'open':'closed');}catch{}
   const groups=new Map(),groupFor=c=>{const t=decode(c.titre).toLowerCase();if(/date|reçu|^du$|^au$|période/.test(t))return 'Période';if(/agence|négociateur|commune|portail|groupe|assistant|rôle/.test(t))return 'Origine et rattachement';if(/statut|fiche|notification|extraction|bien|présent|manque|rythme/.test(t))return 'Situation';return 'Autres critères';};
   fields.forEach((label,i)=>{const c=defs[i]||{},t=decode(c.titre).toLowerCase();if((c.type==='texte'||/^(agence|statut|reçu depuis|période)$/.test(t))&&primary.children.length<4){primary.append(label);return;}const name=groupFor(c);if(!groups.has(name)){const fieldset=node('fieldset'),legend=node('legend','',name);fieldset.append(legend);groups.set(name,fieldset);panel.append(fieldset);}groups.get(name).append(label);});
   bar.prepend(primary,panel);
   const update=()=>{const q=new URLSearchParams(location.search),n=defs.filter(c=>c.type!=='boutons'&&!c.garder&&q.get(c.param)&&q.get(c.param)!=='tout').length;summary.textContent='Tous les filtres'+(n?' · '+n+' actif'+(n>1?'s':''):'');};update();window.addEventListener('dz:filtres',update);
  });
  content.querySelectorAll('.dzw-tb[data-vue="kpi"] .dzw-tb-sous').forEach(text=>{if(text.dataset.dzAppConcise)return;text.dataset.dzAppConcise='1';const help=node('details','ux-inline-help'),summary=node('summary','','i');summary.setAttribute('aria-label','Comment est calculé cet indicateur ?');text.before(help);help.append(summary,text);text.closest('.dzw-tb').querySelector('h3')?.append(help);});
  content.querySelectorAll('[data-vue="note"] .dzw-tb-note').forEach(text=>{
   if(text.dataset.dzAppConcise)return;text.dataset.dzAppConcise='1';const value=decode(text.textContent);
   const edits=[[/Recalculé à chaque/,'Les destinataires affichés tiennent compte des remplacements en cours.'],[/Modifier plusieurs personnes/,'Sélectionnez les personnes, puis choisissez « Modifier la sélection ».'],[/Jours : 1 = lundi/,''],[/Exemple : mi-temps/,'Les jours non travaillés utilisent le relais indiqué.'],[/Le relais peut être/,'À la fin du congé, les demandes reviennent automatiquement au titulaire.'],[/Un départ se prépare/,'Indiquez une date de départ et un remplaçant pour programmer le relais.']];
   const edit=edits.find(([pattern])=>pattern.test(value));if(edit){if(!edit[1]){text.hidden=true;return;}text.textContent=edit[1];}
   if(text.textContent.length>170){const d=node('details','ux-context-help'),s=node('summary','','Comment ça fonctionne ?');text.before(d);d.append(s,text);}
  });
  content.querySelectorAll('.dzw-tb-table th').forEach(th=>{if(decode(th.textContent).trim()==='Jours travaillés'){const i=[...th.parentNode.children].indexOf(th);th.closest('table').querySelectorAll('tbody tr').forEach(tr=>{const cell=tr.children[i];if(cell&&/^\s*[1-7](?:\s*,\s*[1-7])*\s*$/.test(cell.textContent))cell.textContent=cell.textContent.split(',').map(n=>['','Lun','Mar','Mer','Jeu','Ven','Sam','Dim'][+n.trim()]).join(' · ');});}});
 }
 const pagerClone=pager=>{const copy=pager.cloneNode(true);copy.className='ux-top-pager';copy.querySelectorAll('button').forEach((b,i)=>b.onclick=()=>pager.querySelectorAll('button')[i]?.click());return copy;};
 function enhance(){
  refine();
  content.dzAppPruneTabs?.();
  content.querySelectorAll('.dzw-tb-grille').forEach(grid=>{if(grid.dataset.dzAppDone)return;grid.dataset.dzAppDone='1';const pager=grid.parentElement.querySelector('.dzw-tb-pied');if(!pager)return;const top=node('div','ux-grid-pager');top.append(pagerClone(pager));grid.before(top);});
  content.querySelectorAll('.dzw-tb-table').forEach(table=>{
   if(table.dataset.dzAppDone)return;table.dataset.dzAppDone='1';
   const widget=table.closest('[data-dz-widget]'),wrap=table.parentElement,pager=wrap.querySelector('.dzw-tb-pied');
   const state=tableState.get(widget)||{x:0,y:0};tableState.set(widget,state);
   const scroll=node('div','ux-table-scroll');scroll.tabIndex=0;scroll.setAttribute('role','region');scroll.setAttribute('aria-label','Tableau avec défilement et en-têtes fixes');table.before(scroll);scroll.append(table);scroll.scrollLeft=state.x;scroll.scrollTop=state.y;scroll.addEventListener('scroll',()=>{state.x=scroll.scrollLeft;state.y=scroll.scrollTop;},{passive:true});
   const toolbar=node('div','ux-table-toolbar'),left=node('div','left'),right=node('div','right'),label=node('span','','Lignes'),count=node('select');count.setAttribute('aria-label','Nombre de lignes par page');
   for(const n of [25,50,100,200])count.add(new Option(String(n),String(n),false,Number(new URLSearchParams(location.search).get('par_page')||widget.dataset.dzPageSize||25)===n));
   count.onchange=()=>{const u=new URL(location.href);u.searchParams.set('par_page',count.value);u.searchParams.delete('page');history.replaceState(null,'',u);state.x=0;state.y=0;window.dispatchEvent(new Event('dz:filtres'));};left.append(label,count);
   const density=node('button','ux-density',document.body.classList.contains('compact')?'Confort':'Compact');density.type='button';density.setAttribute('aria-label','Changer la densité des lignes');density.onclick=()=>{document.body.classList.toggle('compact');const compact=document.body.classList.contains('compact');store.set('dz-app-density',compact?'compact':'confort');content.querySelectorAll('.ux-density').forEach(b=>b.textContent=compact?'Confort':'Compact');};
   const key='dz-app-columns:'+location.pathname+':'+(widget.dataset.source||'')+':'+(widget.dataset.colonnes||'').slice(0,160),headers=[...table.querySelectorAll('thead th')];
   let hidden=[];try{hidden=JSON.parse(store.get(key)||'[]');}catch{}if(!Array.isArray(hidden))hidden=[];
   const columnName=th=>th.textContent.replace(/[▲▼]/g,'').trim();
   const apply=()=>{const live=widget.querySelector('.dzw-tb-table');if(!live)return;const hs=[...live.querySelectorAll('thead th')];live.querySelectorAll('tr').forEach(tr=>[...tr.children].forEach((cell,i)=>cell.hidden=i>0&&hidden.includes(columnName(hs[i]||{textContent:''}))));};apply();
   const columns=node('button','','Colonnes');columns.type='button';columns.onclick=()=>{const d=dialog('Colonnes du tableau'),choices=node('div','ux-col-choices');d.close.before(choices);headers.forEach((th,i)=>{const label=node('label'),input=node('input');input.type='checkbox';input.checked=i===0||!hidden.includes(columnName(th));input.disabled=i===0;label.append(input,document.createTextNode(' '+(columnName(th)||'Sélection')));choices.append(label);input.onchange=()=>{const name=columnName(th);hidden=input.checked?hidden.filter(x=>x!==name):[...hidden,name];store.set(key,JSON.stringify(hidden));apply();};});};right.append(density,columns);if(pager)right.append(pagerClone(pager));toolbar.append(left,right);wrap.prepend(toolbar);
  });
 }
 function start(){
  if(!arrange())return;
  if(store.get('dz-app-density')==='compact')document.body.classList.add('compact');
  let queued=false;
  const observer=new MutationObserver(records=>{if(queued||!records.some(r=>r.type==='childList'||r.target.matches('[data-dz-widget]')))return;queued=true;requestAnimationFrame(()=>{queued=false;enhance();});});observer.observe(content,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']});enhance();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
