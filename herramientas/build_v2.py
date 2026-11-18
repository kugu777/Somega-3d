"""v2: colores de Vicente.
Encordadora: todo inox; halador y tacos de pata negros; motores y reductora azules;
tuerca de nylon y brida motor blancas. Sin tornillería.
Mesa: inox; gomas y tacos negros; caja Schneider gris con pulsador verde y rojo;
pegatinas azules. Sin tornillería/interior.
Inox menos brillante (roughness 0.45)."""
import re, numpy as np, trimesh
from trimesh.visual.material import PBRMaterial

MATS = {"inox":([0.78,0.79,0.81,1],0.9,0.45), "negro":([0.03,0.03,0.03,1],0.0,0.85),
        "azul_motor":([0.05,0.20,0.58,1],0.3,0.45), "blanco":([0.93,0.93,0.91,1],0.0,0.6),
        "azul":([0.02,0.12,0.55,1],0.0,0.45), "gris_caja":([0.62,0.63,0.62,1],0.0,0.55),
        "verde":([0.05,0.55,0.12,1],0.0,0.4), "rojo":([0.75,0.05,0.04,1],0.0,0.4), "gris_oscuro":([0.16,0.17,0.18,1],0.0,0.55),
        "cristal":([0.86,0.93,0.97,0.22],0.0,0.05),
        "amarillo":([0.98,0.74,0.0,1],0.0,0.5)}   # metacrilato transparente / pegatinas de peligro

def finish(groups, out):
    meshes = {k: trimesh.util.concatenate(v) for k, v in groups.items()}
    allv = np.vstack([m.vertices for m in meshes.values()]); lo, hi = allv.min(0), allv.max(0)
    shift = np.array([-(lo[0]+hi[0])/2, -lo[1], -(lo[2]+hi[2])/2])
    sc = trimesh.Scene()
    for i, (k, m) in enumerate(meshes.items()):
        m.merge_vertices(digits_vertex=5); m.apply_translation(shift)
        m = trimesh.graph.smooth_shade(m, angle=np.radians(35))
        base, met, rough = MATS[k]
        m.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(name=k, baseColorFactor=base, metallicFactor=met, roughnessFactor=rough))
        sc.add_geometry(m, geom_name=f"m{i}", node_name=f"m{i}")
    open(out, 'wb').write(trimesh.exchange.gltf.export_glb(sc, include_normals=True))
    print(out, "mm", np.round((hi-lo)*1000), "mats", sorted(meshes))

def nodes(src):
    s = trimesh.load(src)
    for node in s.graph.nodes_geometry:
        T, g = s.graph[node]; m = s.geometry[g]
        col = tuple(int(x) for x in m.visual.material.baseColorFactor[:3])
        name = s.graph.transforms.parents.get(node) or node
        mm = trimesh.Trimesh(m.vertices, m.faces, process=False); mm.apply_transform(T)
        yield name, col, mm

E_DROP = set()   # tornillería incluida (inox)
E = {**{c:"negro" for c in [(3,3,3),(1,1,1),(139,147,156)]},
     **{c:"azul_motor" for c in [(3,13,50),(70,85,93)]},   # motores y reductora; protección, tubo y brazo de reacción -> inox
     **{c:"blanco" for c in [(220,206,171),(231,224,206),(226,210,175)]}}
M_DROP = re.compile(r'^$a')   # ya no se quita nada: tornillería completa
def mesa_cls(name, col):
    if name.startswith('SCHNEIDER_caja_pulsadores_XALD02_pulsador_1'): return "verde"
    if name.startswith('SCHNEIDER_caja_pulsadores_XALD02_pulsador_2'): return "rojo"
    if name.startswith('SCHNEIDER'): return "gris_oscuro"
    if name.startswith('PRENSAESTOPA') or name.startswith('MOTOR_'): return "gris_oscuro"
    if name.startswith('PEGATINA_RIESGO_AMARILLO'): return "amarillo"   # pegatina de peligro: colores originales
    if name.startswith('PEGATINA_RIESGO_NEGRO'): return "negro"
    if name.startswith('PEGATINA'): return "azul"
    if col == (2,2,2): return "negro"
    return "inox"

if __name__ == "__main__":
    g = {}
    for name, col, mm in nodes('/home/claude/enc/raw.glb'):
        if col in E_DROP: continue
        g.setdefault(E.get(col, "inox"), []).append(mm)
    finish(g, '/home/claude/encordadora_SOMEGA.glb')
    
    g = {}
    for name, col, mm in nodes('/home/claude/raw.glb'):
        if M_DROP.match(name): continue
        g.setdefault(mesa_cls(name, col), []).append(mm)
    finish(g, '/home/claude/mesa_vibradora_SOMEGA.glb')
