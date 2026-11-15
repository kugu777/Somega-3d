// Catálogo SOMEGA: máquinas, sus opciones/extras y cómo montarlas en 3D.
// Todas las piezas de una máquina comparten el mismo origen (ver herramientas/build_catalogo.py),
// así que un extra se monta en su sitio solo con añadirlo.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { finishModel } from './somega.js?v=20261115e';

// Subir esta versión cada vez que cambie un modelo (si no, el móvil usa el guardado)
export const V = '20261115e';
const u = p => p + '?v=' + V;

export const MACHINES = [
  {
    id: 'mesa', name: 'Mesa vibradora 220 V', short: 'Mesa vibradora',
    base: ['mesa/mesa-cuerpo.glb'],
    groups: [
      { title: 'Parrilla', one: true, items: [
        { id: 'p22', name: 'Parrilla de 22', tag: 'De serie', glb: 'mesa/parrilla-22.glb' },
        { id: 'p16', name: 'Parrilla de 16', glb: 'mesa/parrilla-16.glb' },
      ] },
      { title: 'Extras', items: [
        { id: 'tolva', name: 'Tolva de recogida', glb: 'mesa/tolva.glb' },
        { id: 'rampa', name: 'Rampa de salida', glb: 'mesa/rampa.glb' },
      ] },
    ],
    usdz: c => u(`mesa/usdz/mesa-p${c.includes('p16') ? 16 : 22}-t${+c.includes('tolva')}-r${+c.includes('rampa')}.usdz`),
  },
  {
    id: 'enc', name: 'Encordadora', short: 'Encordadora',
    base: ['encordadora/encordadora.glb'],
    groups: [
      { title: 'Extras', items: [
        // view: solo se ve suelta en 360° (falta su posición en la máquina para montarla)
        { id: 'cartucho', name: 'Cartucho para carga de red', glb: 'encordadora/cartucho-red.glb', view: true },
        // lay: en el STEP está de pie; para verlo suelto se tumba
        { id: 'sinfin', name: 'Sinfín Ø80 paso 80 (tubo 1/2")', glb: 'encordadora/sinfin.glb', view: true, lay: true },
      ] },
    ],
    usdz: () => u('encordadora/encordadora.usdz'),
  },
  {
    id: 'pes', name: 'Pesadora ensacadora', short: 'Pesadora',
    note: 'En desarrollo',
    base: ['pesadora/pesadora.glb'], groups: [],
    usdz: () => u('pesadora/pesadora.usdz'),
  },
];

export const items = m => m.groups.flatMap(g => g.items);
export const defaultCfg = m => m.groups.filter(g => g.one).map(g => g.items[0].id);

// "#mesa" o "#mesa:p16,tolva"  →  { m, cfg }
export function parseHash(h) {
  const [id, list] = decodeURIComponent((h || '').replace(/^#/, '')).split(':');
  const m = MACHINES.find(x => x.id === id);
  if (!m) return null;
  let cfg = defaultCfg(m);
  if (list) {
    const want = list.split(',');
    cfg = [];
    for (const g of m.groups) {
      const sel = g.items.filter(i => !i.view && want.includes(i.id)).map(i => i.id);
      if (g.one) cfg.push(sel[0] || g.items[0].id); else cfg.push(...sel);
    }
  }
  return { m, cfg };
}
export function hashOf(m, cfg) {
  const extra = cfg.join(',') === defaultCfg(m).join(',') ? '' : ':' + cfg.join(',');
  return '#' + m.id + extra;
}
// Elegir/quitar una opción respetando los grupos de "solo una"
export function toggle(m, cfg, id) {
  const g = m.groups.find(g => g.items.some(i => i.id === id));
  if (g.one) return cfg.filter(x => !g.items.some(i => i.id === x)).concat(id).sort(order(m));
  return (cfg.includes(id) ? cfg.filter(x => x !== id) : cfg.concat(id)).sort(order(m));
}
const order = m => (a, b) => items(m).findIndex(i => i.id === a) - items(m).findIndex(i => i.id === b);

export function label(m, cfg) {
  const extras = m.groups.filter(g => !g.one).flatMap(g => g.items).filter(i => cfg.includes(i.id)).map(i => i.name.toLowerCase());
  const par = m.groups.find(g => g.one);
  const p = par && par.items.find(i => cfg.includes(i.id));
  return m.name + (p ? ' con ' + p.name.toLowerCase() : '') + (extras.length ? ' + ' + extras.join(' + ') : '');
}

// ---- 3D ----
const loader = new GLTFLoader(), cache = {};
export function loadGLB(path) {
  return cache[path] ||= new Promise((ok, ko) => loader.load(u(path), g => ok(finishModel(g.scene)), undefined, ko));
}
export async function buildMachine(m, cfg) {
  const paths = m.base.concat(items(m).filter(i => cfg.includes(i.id)).map(i => i.glb));
  const parts = await Promise.all(paths.map(loadGLB));
  const g = new THREE.Group();
  parts.forEach(p => g.add(p.clone(true)));
  g.userData.machine = m.id;
  return g;
}
// Un extra suelto, centrado y apoyado en el suelo (para verlo en 360°)
export async function buildItem(item) {
  const o = (await loadGLB(item.glb)).clone(true), w = new THREE.Group();
  if (item.lay) { o.rotation.x = -Math.PI / 2; o.updateMatrixWorld(true); }
  const b = new THREE.Box3().setFromObject(o), c = b.getCenter(new THREE.Vector3());
  o.position.set(-c.x, -b.min.y, -c.z); w.add(o); return w;
}
// Medidas en mm: largo (lado mayor en planta) × ancho × alto
export function sizeMM(obj) {
  const s = new THREE.Box3().setFromObject(obj).getSize(new THREE.Vector3()).multiplyScalar(1000);
  return { L: Math.round(Math.max(s.x, s.z)), W: Math.round(Math.min(s.x, s.z)), H: Math.round(s.y) };
}
export async function itemSize(item) { return sizeMM(await buildItem(item)); }
