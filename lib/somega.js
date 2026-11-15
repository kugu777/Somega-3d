// Acabado común de las máquinas SOMEGA: inox, aristas marcadas y sombras.
import * as THREE from 'three';

export const INOX = new THREE.MeshStandardMaterial({
  color: 0xc4c9d0, metalness: 0.9, roughness: 0.45, envMapIntensity: 0.95, vertexColors: true });

const EDGE = new THREE.LineBasicMaterial({ color: 0x1d2128, transparent: true, opacity: 0.55 });
const EDGE_DARK = new THREE.LineBasicMaterial({ color: 0x8a9099, transparent: true, opacity: 0.5 });

// Prepara un modelo recién cargado (una sola vez; los clones comparten geometrías)
export function finishModel(root) {
  const meshes = [];
  root.traverse(o => { if (o.isMesh) meshes.push(o); });
  for (const o of meshes) {
    const name = o.material && o.material.name;
    if (name === 'inox') o.material = INOX;
    else if (o.material) o.material.vertexColors = false;
    const glass = o.material && o.material.transparent;
    if (glass) o.material.depthWrite = false;
    o.castShadow = !glass; o.receiveShadow = !glass;
    // aristas: pliegues y cantos de más de 28°
    if (glass) continue;                 // el metacrilato sin aristas
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 28),
      name === 'negro' || name === 'azul_motor' ? EDGE_DARK : EDGE);
    edges.raycast = () => {};            // que no estorben al tocar
    o.add(edges);
  }
  return root;
}

// Luz con sombras ajustada a un tamaño de escena (metros)
export function addShadowLight(scene, size = 4) {
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(1.8, 4.5, 2.6); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  const c = sun.shadow.camera; c.left = c.bottom = -size; c.right = c.top = size; c.near = 0.5; c.far = 15;
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.015;
  scene.add(sun, sun.target);
  return sun;
}

// Suelo invisible que solo recibe sombra
export function shadowFloor(size = 12, opacity = 0.32) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.ShadowMaterial({ opacity }));
  m.rotation.x = -Math.PI / 2; m.receiveShadow = true; m.raycast = () => {};
  return m;
}
