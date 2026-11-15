"""Extra suelto (sin colores en el STEP: todo inox) -> GLB final con el acabado de build_v3.
Uso: python3 build_extra.py raw.glb salida.glb [dx dy dz]
Sin desplazamiento, la pieza queda centrada y apoyada en el suelo (para verla sola en 360°).
Con dx dy dz (metros) se usa ese desplazamiento: el mismo que el de su máquina, para montarla en su sitio."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v3 as B3

src, out = sys.argv[1], sys.argv[2]
shift = np.array([float(x) for x in sys.argv[3:6]]) if len(sys.argv) >= 6 else None
s = trimesh.load(src)
meshes = []
for node in s.graph.nodes_geometry:
    T, g = s.graph[node]
    m = trimesh.Trimesh(s.geometry[g].vertices, s.geometry[g].faces, process=False); m.apply_transform(T)
    meshes.append(m)
B3.write_glb({'inox': B3.build_group(meshes, B3.VAR['inox'])}, out, shift=shift)
