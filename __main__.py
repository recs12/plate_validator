# -*- coding: utf-8 -*-

"""
Check list for sheet plate.
"""

import sys
import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import SolidEdgeFramework
import SolidEdgeConstants
import System
import System.Runtime.InteropServices as SRI
from System import Console, Math
from System.IO import Directory
from System.IO.Path import Combine
import SolidEdgeConstants
import permissions, helpers

from  standards import MAX, PLIAGE
from helpers import *


def main():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")
        plate = application.ActiveDocument
        assert plate.Type == 4, "This macro only works on plate"

        permissions.details()
        permissions.permissions(application)

        print "part: %s" % plate.Name
        print "="*75

        # TODO: [1] try to work out a way to align display and debugging together so I can debug more easly.
        # example by creating func for each value, functional style maybe.

        equip_a     = properties( plate, 'EQUIP_A')
        serie_a     = properties( plate, 'SERIE_A')
        module_a    = properties( plate, 'MODULE_A')
        jdelitm     = properties( plate, 'JDELITM')
        material    = properties( plate, 'Material Thickness')
        bend        = properties( plate, 'Bend Radius')
        teamcenter  = properties( plate, 'Teamcenter Item Type')
        category_vb = properties( plate, 'CATEGORY_VB')
        part_name   = properties( plate, 'Nom de la piece')
        dim         = properties( plate, 'DIM')
        dim1        = properties( plate, 'Dim1')
        dim2        = properties( plate, 'Dim2')
        cad_uom     = properties( plate, 'CAD_UOM')
        dsc_a       = properties( plate, 'DSC_A')
        dsc_m_a     = properties( plate, 'DSC_M_A')
        jdedsc1_a   = properties( plate, 'JDEDSC1_A')
        jdedsc2_a   = properties( plate, 'JDEDSC2_A')
        jdestrx_a   = properties( plate, 'JDESTRX_A')

        # VARIABLES:
        A           = variables(plate, 'A')
        N           = variables(plate, 'N')
        max_Y       = variables(plate, 'Flat_Pattern_Model_CutSizeY') # max size flatten
        max_X       = variables(plate, 'Flat_Pattern_Model_CutSizeX') # max size flatten

        # PLI
        pli_min     = PLIAGE.get(jdedsc2_a).get("B")
        angle_max   = PLIAGE.get(jdedsc2_a).get("A")

        # DISPLAY:
        ln("DESCRIPTION", 'DIM', dim, null(dim))
        ln("DESCRIPTION", 'Dim1', dim1, null(dim1))
        ln("DESCRIPTION", 'Dim2', dim2, null(dim2))

        if flatpattern_exist(plate) == "OK":
            dims = "{0:.3f}X{1:.3f}".format(max_X, max_Y)
            ln("DIMENSION", "flatten-dimension", dims , check_maximum(max_X, max_Y))
        ln("VARIABLES", "A", A, null(A))
        ln("VARIABLES", "N", N, null(N))

        # MODELING
        ln("MODE",      "MODELING_MODE", get_modeling_mode(plate), validate_modeling_mode(plate))
        ln("BOM",       "DSC_A",    dsc_a, null(dsc_a))
        ln("MANUALS" ,  "DSC_M_A", dsc_m_a, null(dsc_m_a))
        ln("CARTOUCHE", "EQUIP_A", equip_a, null(equip_a))
        ln("CARTOUCHE", "SERIE_A", serie_a, null(serie_a))
        ln("CARTOUCHE", "MODULE_A", module_a, null(module_a))
        ln("JDE",       "JDELITM", jdelitm, null(jdelitm))
        ln("MATERIAL",  "Material", material, null(material))
        ln("CAD",       'Teamcenter', teamcenter, null(teamcenter))
        ln("UNITS",     'CAD_UOM' , cad_uom, null(cad_uom))
        ln("CATEGORY",  'CATEGORY_VB' , category_vb, null(category_vb))
        ln("CARTOUCHE", 'NAME'  , part_name, null(part_name))
        ln("DESCRIPTION",'JDEDSC1_A' , jdedsc1_a, null(jdedsc1_a))
        ln("THICKNESS", 'JDEDSC2_A' , jdedsc2_a, null(jdedsc2_a))
        ln("CARTOUCHE", 'JDESTRX_A' , jdestrx_a, null(jdestrx_a))
        ln("MODELING",  'FLATE_PATTERN' , "", flatpattern_exist(plate))
        # ln("BEND",      'Bend', bend , "x") # TODO


        # FEATURES:
        if get_number_Flange(plate): ln("FLANGE", 'B pli-min' , get_number_Flange(plate), pli_min) # TODO
        if get_number_CoutourFlange(plate): ln("CTRFLANGE", 'B pli-min' , "", pli_min) # TODO
        if get_number_Hole(plate) and pli_exists(plate): ln("HOLE", 'C pli-Trous' , "" , pli_min) # TODO
        if get_number_Flange(plate)>1 or get_number_CoutourFlange(plate): ln("HORS-TOUT", 'H hors-tout' , "", pli_min) # TODO
        if get_number_Flange(plate)==4: ln("FLANGES", 'B max (4 plis)', "", pli_min) # TODO
        if get_number_Flange(plate) or get_number_CoutourFlange(plate): ln("ANGLE", "Angle max" , "(degres)", angle_max) # TODO


    except AssertionError as err:
        print(err.args)

    except Exception as ex:
        print(ex.args)

    finally:
        raw_input("\nPress any key to exit...")
        sys.exit()


def confirmation(func):
    response = raw_input("""Validate sheetmetal modeling? (Press y/[Y] to proceed.)""")
    if response.lower() not in ["y", "yes", "oui"]:
        print("Process canceled")
        sys.exit()
    else:
        func()


if __name__ == "__main__":
    confirmation(main)