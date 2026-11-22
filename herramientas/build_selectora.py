"""Selectora hidráulica (adelanto: STEP SS26-100-Chasis-conjunto-R29, solo chasis, parrillas y tolva).
Todo inox salvo lo que el dibujo trae en negro (2,2,2): bases de goma de las patas y ruedas.
Ya viene con el largo en Z y la tolva hacia +Z, como la encordadora: no se gira.
Uso: python3 build_selectora.py raw.glb salida.glb"""
import os, sys, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v3 as B3

src, out = sys.argv[1], sys.argv[2]
s = trimesh.load(src)
g = {}
for node in s.graph.nodes_geometry:
    T, geo = s.graph[node]; m = s.geometry[geo]
    col = tuple(int(x) for x in m.visual.material.baseColorFactor[:3]) if hasattr(m.visual, 'material') else None
    mm = trimesh.Trimesh(m.vertices, m.faces, process=False); mm.apply_transform(T)
    g.setdefault('negro' if col == (2, 2, 2) else 'inox', []).append(mm)
B3.write_glb({k: B3.build_group(v, B3.VAR[k]) for k, v in g.items()}, out)
