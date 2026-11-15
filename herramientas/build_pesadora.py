"""Pesadora ensacadora (STEP SOMEGA_pesadora_montaje_completo_v68 (2)): colores de Vicente.
Todo inox, salvo: metacrilato de la ventana del armario del visor transparente; botón del cierre de la tapa del armario negro; cristales del visor de peso (LCD) verdes; caja Schneider XALD02 gris oscuro con
pulsador_1 verde y pulsador_2 rojo; bandas de rodadura de las ruedas azules; bandas (cintas de
cangilones) azules; tacos de goma de las patas negros.
Uso: python3 build_pesadora.py raw.glb salida.glb"""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v3 as B3

def cls(name):
    if name.startswith('metacrilato'): return 'cristal'
    if name.startswith('cierre_pulsador_puerta_armario_visor_boton') or name.startswith('cierre_pulsador_puerta_armario_visor_cuerpo'): return 'negro'
    if name.startswith('visor_peso_lcd'): return 'verde'
    if name.startswith('caja_pulsadores_XALD02_pulsador_1'): return 'verde'
    if name.startswith('caja_pulsadores_XALD02_pulsador_2'): return 'rojo'
    if name.startswith('caja_pulsadores_XALD02'): return 'gris_oscuro'
    if name.startswith('rueda_ALEX') and '_goma_' in name: return 'azul'
    if name.startswith('banda_azul'): return 'azul'
    if name.startswith('base_niveladora_goma'): return 'negro'
    return 'inox'

src, out = sys.argv[1], sys.argv[2]
# Girada -90° en vertical para que quede como la encordadora: largo en Z y la tolva de carga
# hacia el mismo lado que la tolva de la encordadora (+Z)
ROT = trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0])
s = trimesh.load(src)
g = {}
for node in s.graph.nodes_geometry:
    T, geo = s.graph[node]; m = s.geometry[geo]
    name = s.graph.transforms.parents.get(node) or node
    mm = trimesh.Trimesh(m.vertices, m.faces, process=False); mm.apply_transform(T)
    mm.apply_transform(ROT)
    g.setdefault(cls(name), []).append(mm)
B3.write_glb({k: B3.build_group(v, B3.VAR[k]) for k, v in g.items()}, out)
