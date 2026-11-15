import sys, numpy as np, trimesh
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, UsdUtils, Vt

src, usda, usdz = sys.argv[1], sys.argv[2], sys.argv[3]
s = trimesh.load(src)
stage = Usd.Stage.CreateNew(usda)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)
root = UsdGeom.Xform.Define(stage, "/Mesa"); stage.SetDefaultPrim(root.GetPrim())
for i, (name, m) in enumerate(s.geometry.items()):
    mat = m.visual.material
    base = np.array(mat.baseColorFactor[:3]) / 255.0
    p = f"/Mesa/m{i}"
    mesh = UsdGeom.Mesh.Define(stage, p)
    mesh.CreatePointsAttr(Vt.Vec3fArray.FromNumpy(m.vertices.astype(np.float32)))
    mesh.CreateFaceVertexCountsAttr(Vt.IntArray([3]*len(m.faces)))
    mesh.CreateFaceVertexIndicesAttr(Vt.IntArray.FromNumpy(m.faces.reshape(-1).astype(np.int32)))
    mesh.CreateNormalsAttr(Vt.Vec3fArray.FromNumpy(m.vertex_normals.astype(np.float32)))
    mesh.SetNormalsInterpolation(UsdGeom.Tokens.vertex)
    mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)
    mesh.CreateDoubleSidedAttr(True)
    lo, hi = m.bounds
    mesh.CreateExtentAttr([Gf.Vec3f(*lo), Gf.Vec3f(*hi)])
    M = UsdShade.Material.Define(stage, p + "_mat")
    sh = UsdShade.Shader.Define(stage, p + "_mat/pbr")
    sh.CreateIdAttr("UsdPreviewSurface")
    sh.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*base))
    sh.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(float(mat.metallicFactor or 0))
    sh.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(float(mat.roughnessFactor or 0.5))
    M.CreateSurfaceOutput().ConnectToSource(sh.ConnectableAPI(), "surface")
    UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim()).Bind(M)
stage.GetRootLayer().Save()
print("usdz", UsdUtils.CreateNewUsdzPackage(usda, usdz))
