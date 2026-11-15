"""USDZ para iPhone de cada configuración de la mesa (el visor de Apple no monta piezas sueltas).
Uso: python3 catalogo_usdz.py DIR_GLB DIR_SALIDA
Nombres: mesa-p22-t0-r0.usdz  (p = parrilla 22/16, t = tolva 0/1, r = rampa 0/1)"""
import os, sys, subprocess, itertools, tempfile, trimesh
src, out = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
for p, t, r in itertools.product(('22', '16'), (0, 1), (0, 1)):
    files = ['mesa-cuerpo', f'parrilla-{p}'] + (['tolva'] if t else []) + (['rampa'] if r else [])
    sc = trimesh.Scene()
    for f in files:
        s = trimesh.load(f'{src}/{f}.glb')
        for name, g in s.geometry.items():   # nodos sin transformación (build_v3)
            m = trimesh.Trimesh(g.vertices, g.faces, vertex_normals=g.vertex_normals, process=False)
            m.visual = trimesh.visual.TextureVisuals(material=g.visual.material)   # sin COLOR_0
            sc.add_geometry(m, geom_name=f'{f}_{name}')
    name = f'mesa-p{p}-t{t}-r{r}'
    with tempfile.TemporaryDirectory() as d:
        glb = f'{d}/{name}.glb'; open(glb, 'wb').write(trimesh.exchange.gltf.export_glb(sc, include_normals=True))
        subprocess.run([sys.executable, f'{here}/glb2usdz.py', glb, f'{d}/{name}.usdc', f'{out}/{name}.usdz'], check=True)
    print(name, os.path.getsize(f'{out}/{name}.usdz') // 1024, 'KB')
