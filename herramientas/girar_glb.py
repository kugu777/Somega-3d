"""Da la vuelta (180° en vertical) a un GLB ya hecho, sin volver al STEP.
Cambia de signo X y Z de posiciones y normales. Uso: python3 girar_glb.py modelo.glb"""
import sys, numpy as np
from pygltflib import GLTF2
path = sys.argv[1]
g = GLTF2().load(path); blob = bytearray(g.binary_blob()); done = set()
for mesh in g.meshes:
    for p in mesh.primitives:
        for attr in ('POSITION', 'NORMAL'):
            i = getattr(p.attributes, attr)
            if i is None or i in done: continue
            done.add(i); a = g.accessors[i]; v = g.bufferViews[a.bufferView]
            assert a.componentType == 5126 and a.type == 'VEC3'
            off = (v.byteOffset or 0) + (a.byteOffset or 0); stride = v.byteStride or 12
            assert stride % 4 == 0
            f = np.frombuffer(blob, dtype=np.float32, count=(a.count - 1) * stride // 4 + 3, offset=off)
            f = f.reshape(-1) ; s4 = stride // 4
            f[0::s4][:a.count] *= -1; f[2::s4][:a.count] *= -1
            if attr == 'POSITION' and a.min:
                mn, mx = a.min, a.max
                a.min = [-mx[0], mn[1], -mx[2]]; a.max = [-mn[0], mx[1], -mn[2]]
g.set_binary_blob(bytes(blob)); g.save(path)
print('girado', path, len(done), 'accesores')
