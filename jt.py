import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import System

def save_as_jt(document, NewName):
    """Note: Some of the parameters are obvious by their name but we need to work on getting better descriptions for some
    """
    document.SaveAsJT(
        NewName,
        Include_PreciseGeom = 0,
        Prod_Structure_Option = 1,
        Export_PMI = 0,
        Export_CoordinateSystem = 0,
        Export_3DBodies = 0,
        NumberofLODs = 1,
        JTFileUnit = 0,
        Write_Which_Files = 1,
        Use_Simplified_TopAsm = 0,
        Use_Simplified_SubAsm = 0,
        Use_Simplified_Part = 0,
        EnableDefaultOutputPath = 0,
        IncludeSEProperties = 0,
        Export_VisiblePartsOnly = 1,
        Export_VisibleConstructionsOnly = 0,
        RemoveUnsafeCharacters = 0,
        ExportSEPartFileAsSingleJTFile = 0,
    )