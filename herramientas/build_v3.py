"""v3: más realismo.
- Mismos colores que v2.
- Cada pieza (componente conectado) con un tono de su material ligeramente distinto
  (COLOR_0), para que las chapas solapadas se distingan.
- Normales suavizadas solo hasta 25° (aristas vivas en los pliegues/cantos).
GLB escrito a mano con pygltflib (posiciones, normales, colores, índices, material PBR)."""
import re, sys, numpy as np, trimesh, pygltflib as G
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from build_v2 import MATS, nodes, E, E_DROP, M_DROP, mesa_cls

rng = np.random.default_rng(7)
VAR = {"cristal":0.0, "inox":0.10, "negro":0.0, "azul_motor":0.05, "blanco":0.04, "azul":0.0, "gris_caja":0.04, "verde":0.0, "rojo":0.0, "gris_oscuro":0.03}

def build_group(meshes, var):
    m = trimesh.util.concatenate(meshes); m.merge_vertices(digits_vertex=5)
    parts = m.split(only_watertight=False) if var > 0 else [m]
    V, N, C, F, off = [], [], [], [], 0
    for p in parts:
        p = trimesh.graph.smooth_shade(p, angle=np.radians(25))
        f = 1.0 + (rng.random() * 2 - 1) * var
        V.append(p.vertices); N.append(p.vertex_normals); F.append(p.faces + off)
        C.append(np.full((len(p.vertices), 3), f)); off += len(p.vertices)
    return np.vstack(V), np.vstack(N), np.clip(np.vstack(C), 0, 1.0), np.vstack(F), len(parts)

def write_glb(groups, out, shift=None):
    allv = np.vstack([g[0] for g in groups.values()]); lo, hi = allv.min(0), allv.max(0)
    if shift is None: shift = np.array([-(lo[0]+hi[0])/2, -lo[1], -(lo[2]+hi[2])/2])
    gl = G.GLTF2(asset=G.Asset(version="2.0", generator="SOMEGA"), scene=0, scenes=[G.Scene(nodes=[])])
    blob = bytearray()
    def add(arr, target, comp, typ, minmax=False):
        nonlocal blob
        while len(blob) % 4: blob += b'\0'
        b = arr.tobytes(); bv = G.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(b), target=target)
        blob += b; gl.bufferViews.append(bv)
        acc = G.Accessor(bufferView=len(gl.bufferViews)-1, componentType=comp, count=len(arr), type=typ)
        if minmax: acc.min = arr.min(0).tolist(); acc.max = arr.max(0).tolist()
        gl.accessors.append(acc); return len(gl.accessors)-1
    for name, (V, N, C, F, _) in groups.items():
        base, met, rough = MATS[name]
        gl.materials.append(G.Material(name=name, alphaMode='BLEND' if base[3] < 1 else 'OPAQUE', doubleSided=base[3] < 1,
            pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorFactor=base, metallicFactor=met, roughnessFactor=rough)))
        p = add((V + shift).astype(np.float32), G.ARRAY_BUFFER, G.FLOAT, G.VEC3, True)
        n = add(N.astype(np.float32), G.ARRAY_BUFFER, G.FLOAT, G.VEC3)
        c = add(C.astype(np.float32), G.ARRAY_BUFFER, G.FLOAT, G.VEC3)
        i = add(F.reshape(-1).astype(np.uint32), G.ELEMENT_ARRAY_BUFFER, G.UNSIGNED_INT, G.SCALAR)
        gl.meshes.append(G.Mesh(primitives=[G.Primitive(attributes=G.Attributes(POSITION=p, NORMAL=n, COLOR_0=c),
            indices=i, material=len(gl.materials)-1)]))
        gl.nodes.append(G.Node(mesh=len(gl.meshes)-1)); gl.scenes[0].nodes.append(len(gl.nodes)-1)
    gl.buffers.append(G.Buffer(byteLength=len(blob))); gl.set_binary_blob(bytes(blob))
    gl.save_binary(out)
    print(out, "mm", np.round((hi-lo)*1000), {k: v[4] for k, v in groups.items()})

def run(src, cls, drop, out):
    raw = {}
    for name, col, mm in nodes(src):
        if drop(name, col): continue
        raw.setdefault(cls(name, col), []).append(mm)
    write_glb({k: build_group(v, VAR[k]) for k, v in raw.items()}, out)

if __name__ == '__main__':
  run('/home/claude/enc/raw.glb', lambda n, c: E.get(c, "inox"), lambda n, c: c in E_DROP, '/home/claude/encordadora_SOMEGA.glb')
  run('/home/claude/raw.glb', mesa_cls, lambda n, c: bool(M_DROP.match(n)), '/home/claude/mesa_vibradora_SOMEGA.glb')
