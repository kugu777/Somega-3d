"""Pesadora ensacadora (STEP SOMEGA_pesadora_montaje_completo_v68 (2)): colores de Vicente.
Todo inox, salvo: pegatinas de peligro eléctrico con sus colores (interior amarillo, marco y rayo negros); pegatina del logo SOMEGA azul; metacrilato de la ventana del armario del visor transparente; botón del cierre de la tapa del armario negro; cristales del visor de peso (LCD) verdes; caja Schneider XALD02 gris oscuro con
pulsador_1 verde y pulsador_2 rojo; solo la banda de rodadura de las ruedas azul (el resto de la goma negro); rodamientos UCF204, sensor inductivo y sus tuercas M18 negros; bandas (cintas de
cangilones) azules; tacos de goma de las patas negros.
Uso: python3 build_pesadora.py raw.glb salida.glb"""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v3 as B3

def cls(name):
    if name.startswith('metacrilato'): return 'cristal'
    if name.startswith('cierre_pulsador_puerta_armario_visor_boton') or name.startswith('cierre_pulsador_puerta_armario_visor_cuerpo'): return 'negro'
    if name.startswith('pegatina_peligro') and '_amarillo_' in name: return 'amarillo'   # colores originales
    if name.startswith('pegatina_peligro'): return 'negro'                                # marco y rayo
    if name.startswith('pegatina_logo_SOMEGA_azul'): return 'azul'
    if name.startswith('visor_peso_lcd'): return 'verde'
    if name.startswith('caja_pulsadores_XALD0') and '_pulsador_1' in name: return 'verde'
    if name.startswith('caja_pulsadores_XALD0') and '_pulsador_2' in name: return 'rojo'
    if name.startswith('caja_pulsadores_XALD0'): return 'gris_oscuro'
    if name.startswith('rueda_ALEX') and '_goma_' in name: return 'goma'   # se parte: banda de rodadura azul, resto negro
    if name.startswith('UCF204'): return 'negro'                            # rodamientos
    if name.startswith('sensor_inductivo') or name.startswith('tuerca_M18_sensor'): return 'negro'
    if name.startswith('banda_azul'): return 'azul'
    if name.startswith('base_niveladora_goma'): return 'negro'
    return 'inox'

src, out = sys.argv[1], sys.argv[2]
# Girada -90° en vertical para que quede como la encordadora: largo en Z y la tolva de carga
# hacia el mismo lado que la tolva de la encordadora (+Z)
ROT = trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0])
s = trimesh.load(src)
g = {}; gomas = {}
for node in s.graph.nodes_geometry:
    T, geo = s.graph[node]; m = s.geometry[geo]
    name = s.graph.transforms.parents.get(node) or node
    mm = trimesh.Trimesh(m.vertices, m.faces, process=False); mm.apply_transform(T)
    mm.apply_transform(ROT)
    k = cls(name)
    if k == 'goma':
        gomas.setdefault(name.split('_goma_')[1].rstrip('_0123456789'), []).append(mm); continue
    g.setdefault(k, []).append(mm)
# ruedas: eje = lado más corto; banda de rodadura = caras en el borde exterior
for wheel, parts in gomas.items():
    mm = trimesh.util.concatenate(parts)
    lo, hi = mm.bounds; ext = hi - lo; ax = int(np.argmin(ext)); c = (lo + hi) / 2
    other = [i for i in range(3) if i != ax]; R = ext[other].max() / 2
    r = np.linalg.norm((mm.vertices - c)[:, other], axis=1)
    tread = (r[mm.faces] > R * 0.99).all(axis=1)   # solo la cara exterior plana
    print('rueda', wheel, 'R mm', round(R * 1000), 'caras banda', int(tread.sum()), 'de', len(tread))
    for part, sel in (('azul', tread), ('negro', ~tread)):
        if sel.any():
            sub = trimesh.Trimesh(mm.vertices, mm.faces[sel], process=False); sub.remove_unreferenced_vertices()
            g.setdefault(part, []).append(sub)
B3.write_glb({k: B3.build_group(v, B3.VAR[k]) for k, v in g.items()}, out)
