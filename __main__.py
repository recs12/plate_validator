# -*- coding: utf-8 -*-

"""
Check list for sheet plate.
"""

import sys
import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import System
import System.Runtime.InteropServices as SRI
from System import Console
import permissions, helpers

from standards import PLIAGE, thickness_mapping
from helpers import *
from debbug import loggingINFO

__VERSION__ = "0.0.4"


def main():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")
        plate = application.ActiveDocument
        assert plate.Type == 4, "This macro only works on plate"

        permissions.details()
        permissions.permissions(application)

        print("part: %s" % plate.Name)
        print("=" * 88)

        # build a logger
        loggingINFO("====================DEBUG MODE======================")
        DIM = properties(plate, "DIM")
        loggingINFO("DIM :")
        loggingINFO(str(DIM))
        loggingINFO("")

        dim1 = properties(plate, "dim1")
        loggingINFO("dim1 :")
        loggingINFO(str(dim1))
        loggingINFO("")

        dim2 = properties(plate, "dim2")
        loggingINFO("dim2 :")
        loggingINFO(str(dim2))
        loggingINFO("")

        JDEDSC1_A = properties(plate, "JDEDSC1_A")
        loggingINFO("JDEDSC1_A :")
        loggingINFO(str(JDEDSC1_A))
        loggingINFO("")

        DSC_A = properties(plate, "DSC_A")
        loggingINFO("DSC_A :")
        loggingINFO(str(DSC_A))
        loggingINFO("")

        EQUIP_A = properties(plate, "EQUIP_A")
        loggingINFO("EQUIP_A :")
        loggingINFO(str(EQUIP_A))
        loggingINFO("")

        SERIE_A = properties(plate, "SERIE_A")
        loggingINFO("SERIE_A :")
        loggingINFO(str(SERIE_A))
        loggingINFO("")

        MODULE_A = properties(plate, "MODULE_A")
        loggingINFO("MODULE_A :")
        loggingINFO(str(MODULE_A))
        loggingINFO("")

        NAME = properties(plate, "Nom de la piece")
        loggingINFO("Nom de la piece :")
        loggingINFO(str(NAME))
        loggingINFO("")

        A = variables(plate, "A")
        loggingINFO("A :")
        loggingINFO(str(A))
        loggingINFO("")

        N = variables(plate, "N")
        loggingINFO("N :")
        loggingINFO(str(N))
        loggingINFO("")

        DSC_M_A = properties(plate, "DSC_M_A")
        loggingINFO("DSC_M_A :")
        loggingINFO(str(DSC_M_A))
        loggingINFO("")

        JDELITM = properties(plate, "JDELITM")
        loggingINFO("JDELITM :")
        loggingINFO(str(JDELITM))
        loggingINFO("")

        CAD = properties(plate, "Teamcenter Item Type")
        loggingINFO("CAD :")
        loggingINFO(str(CAD))
        loggingINFO("")

        CATEGORY_VB = properties(plate, "CATEGORY_VB")
        loggingINFO("CATEGORY_VB :")
        loggingINFO(str(CATEGORY_VB))
        loggingINFO("")

        CAD_UOM = properties(plate, "CAD_UOM")
        loggingINFO("CAD_UOM :")
        loggingINFO(str(CAD_UOM))
        loggingINFO("")

        THICKNESS = properties(plate, "JDEDSC2_A")
        loggingINFO("THICKNESS :")
        loggingINFO(str(THICKNESS))
        loggingINFO("")

        mode = get_modeling_mode(plate)
        loggingINFO("mode :")
        loggingINFO(str(mode))
        loggingINFO("")

        valide_mode = validate_modeling_mode(plate)
        loggingINFO("valide_mode :")
        loggingINFO(str(valide_mode))
        loggingINFO("")

        isflatten = flatpattern_exist(plate)
        loggingINFO("isflatten :")
        loggingINFO(str(isflatten))
        loggingINFO("")

        loggingINFO("====================END DEBUG MODE======================")

        # add a condition according to mode select to display or not.

        parameters = [
            ("DESCRIPTION", "DIM", DIM, null(DIM)),
            ("DESCRIPTION", "Dim1", dim1, null(dim1)),
            ("DESCRIPTION", "Dim2", dim2, null(dim2)),
            ("DESCRIPTION", "JDEDSC1_A", JDEDSC1_A, null(JDEDSC1_A)),
            ("DESCRIPTION", "DSC_A", DSC_A, null(DSC_A)),
            ("CARTOUCHE", "EQUIP_A", EQUIP_A, null(EQUIP_A)),
            ("CARTOUCHE", "SERIE_A", SERIE_A, null(SERIE_A)),
            ("CARTOUCHE", "MODULE_A", MODULE_A, null(MODULE_A)),
            # (
            #     "CARTOUCHE",
            #     "NAME",
            #     NAME,
            #     null(NAME),
            # ),
            ("VARIABLES", "A", A, null(A)),
            ("VARIABLES", "N", N, null(N)),
            ("MODE", "MODELING_MODE", mode, valide_mode),
            ("MODELING", "FLAT_PATTERN", "DESIGNED", isflatten),
            ("MANUALS", "DSC_M_A", DSC_M_A, null(DSC_M_A)),
            ("JDE", "JDELITM", JDELITM, null(JDELITM)),
            # (
            #     "MATERIAL",
            #     "Material",
            #     MATERIAL,
            #     null(MATERIAL),
            # ),
            ("CAD", "Teamcenter", CAD, null(CAD)),
            ("CATEGORY", "CATEGORY_VB", CATEGORY_VB, null(CATEGORY_VB)),
            ("UNITS", "CAD_UOM", CAD_UOM, null(CAD_UOM)),
            ("THICKNESS", "JDEDSC2_A", THICKNESS, null(THICKNESS)),
        ]

        # -- VIEW -- :
        # ===========

        map(ln, parameters)

        # STANDARDS
        thickness_jde = properties(plate, "JDEDSC2_A")
        epaisseur = thickness_mapping.get(thickness_jde)
        if epaisseur in PLIAGE.keys():
            pli_min = PLIAGE.get(epaisseur).get("B", None)
            b_max = PLIAGE.get(epaisseur).get("Bmax").get("STEEL PLATE", None)
            hors_tout = PLIAGE.get(epaisseur).get("H").get("STEEL PLATE", None)
            angle_max = PLIAGE.get(epaisseur).get("A", None)

            # FEATURES:
            if flatpattern_exist(plate) == "OK":
                max_X = variables(plate, "Flat_Pattern_Model_CutSizeX")
                max_Y = variables(plate, "Flat_Pattern_Model_CutSizeY")
                d = dimensions(max_X, max_Y)
                c = check_maximum(dim1=max_X, dim2=max_Y)
                ln(("DIMENSION", "flatten-dimensions", d, c))

                # implementation
                # print(sorted([round(max_X, 2), round(max_Y, 2)]))
                # print(sorted([round(dim1, 2), round(dim2, 2)]))
                if sorted([round(max_X, 2), round(max_Y, 2)]) != sorted(
                    [round(dim1, 2), round(dim2, 2)]
                ):
                    ln(("DIMENSION", "dimensions", dim1, "DISCREPENCY"))
                    ln(("DIMENSION", "dimensions", dim2, "DISCREPENCY"))

            if isCopiedPart(plate):
                ln(("DESIGN", "Part Copy", "", "COPY"))
            if get_number_Flange(plate) or get_number_CoutourFlange(plate):
                ln(("DESIGN", "B pli-min", "in", pli_min))
            if get_number_Flange(plate) == 4:
                ln(("DESIGN", "B max (4 x plis)", "in", b_max))
            if get_number_Flange(plate) > 1 or get_number_CoutourFlange(plate):
                ln(("DESIGN", "H hors-tout", "in (pliage inverse)", hors_tout))
            if get_number_Flange(plate) or get_number_CoutourFlange(plate):
                ln(("DESIGN", "Angle Max", "degrees (pli interieur B)", angle_max))

        else:
            ln(("STANDARDS", "standards unavailable", "", thickness))

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

# TODO: create a batch version
