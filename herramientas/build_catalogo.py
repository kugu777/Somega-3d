"""Catálogo: mesa vibradora por piezas (cuerpo + parrilla + extras), todas con el MISMO origen,
para que en la web los extras se monten en su sitio exacto sobre la mesa.

Uso: python3 build_catalogo.py RAW_DIR OUT_DIR
RAW_DIR tiene los GLB de step2glb.py:
  1.glb = 1_MESA_VIBRADORA_CON_PARRILLA_22.step
  2.glb = 2_PARRILLA_16_COMPLETA.step
  3.glb = 3_TOLVA_RECOGIDA.step
  4.glb = 4_RAMPA_DE_SALIDA.step
El origen (centro en planta, suelo en Y=0) se calcula con la mesa (1.glb) y se aplica a todo.
"""
import os, re, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2 import nodes, mesa_cls
import build_v3 as B3   # build_group, write_glb (sin ejecutar: ver guarda en build_v3)

raw, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
PARRILLA = re.compile(r'^(PARRILLA_|PLETINA_40x6_[AB]$|TUBO_10x10x1_L800)')

def collect(src, keep=lambda n: True):
    g = {}
    for name, col, mm in nodes(src):
        if not keep(name): continue
        g.setdefault(mesa_cls(name, col), []).append(mm)
    return g

# origen común: el de la mesa completa
import trimesh
allv = np.vstack([mm.vertices for _, _, mm in nodes(f'{raw}/1.glb')])
lo, hi = allv.min(0), allv.max(0)
SHIFT = np.array([-(lo[0]+hi[0])/2, -lo[1], -(lo[2]+hi[2])/2])
print('mesa mm', np.round((hi-lo)*1000), 'shift', SHIFT)

parts = {
    'mesa-cuerpo':  collect(f'{raw}/1.glb', lambda n: not PARRILLA.match(n)),
    'parrilla-22':  collect(f'{raw}/1.glb', lambda n: bool(PARRILLA.match(n))),
    'parrilla-16':  collect(f'{raw}/2.glb'),
    'tolva':        collect(f'{raw}/3.glb'),
    'rampa':        collect(f'{raw}/4.glb'),
}
for k, g in parts.items():
    B3.write_glb({m: B3.build_group(v, B3.VAR[m]) for m, v in g.items()}, f'{out}/{k}.glb', shift=SHIFT)
