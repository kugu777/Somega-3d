import sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.RWMesh import RWMesh_CoordinateSystem_Zup, RWMesh_CoordinateSystem_glTF
from OCP.collections import IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString as IDM
from OCP.Message import Message_ProgressRange

src, out = sys.argv[1], sys.argv[2]
# opcional: tolerancia de malla en mm y ángulo en rad (de serie 0.3 / 0.3; máquinas grandes: 1.0 0.5)
defl = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
ang = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
r = STEPCAFControl_Reader(); r.SetColorMode(True); r.SetNameMode(True)
assert r.ReadFile(src) == 1
r.Transfer(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
BRepMesh_IncrementalMesh(st.GetOneShape(), defl, False, ang, True)
w = RWGltf_CafWriter(TCollection_AsciiString(out), True)
cs = w.ChangeCoordinateSystemConverter()
cs.SetInputLengthUnit(0.001)  # mm -> m
cs.SetInputCoordinateSystem(RWMesh_CoordinateSystem_Zup)
cs.SetOutputCoordinateSystem(RWMesh_CoordinateSystem_glTF)
ok = w.Perform(doc, IDM(), Message_ProgressRange())
print("ok", ok)
