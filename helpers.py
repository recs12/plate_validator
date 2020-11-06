import sys
import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import SolidEdgeConstants
import SolidEdgeFramework
import System
import System.Runtime.InteropServices as SRI
from standards import PLIAGE
from System import Console
from debbug import loggingINFO
from standards import PLIAGE, thickness_mapping

def raw_input(message):
    Console.WriteLine(message)
    return Console.ReadLine()

def prompt_exit():
    raw_input("\nPress any key to exit...")
    sys.exit()

def userprofile():
    return System.Environment.GetEnvironmentVariable("USERPROFILE")


def null(content):
    if not content or content == "-" or content == ".":
        return "MISSING"
    else:
        return "OK"


def flatpattern_exist(part):
    if part.FlatPatternModels.item(1):
        return "OK"
    else:
        return "MISSING"


def get_modeling_mode(part):
    mode = part.ModelingMode
    if mode == 1:
        return "SYNCHRONOUS"
    elif mode == 2:
        return "ORDERED"
    elif mode == 3:
        return "SIMPLIFY"
    elif mode == 4:
        return "FLATTEN"
    else:
        return "Unknown"


def validate_modeling_mode(part):
    mode = part.ModelingMode
    if mode == 2:
        return "OK"
    else:
        return "WRONG MODE"


def to_inches(m):
    return m * 39.3700787


def convertor_radius_to_degres(angle_in_radians):
    return angle_in_radians * (180 / Math.PI)


def get_data_Flange(part):
    # BendAngle, BendRadius, Flange Type = -1752010637
    return [
        (bend.Name, convertor_radius_to_degres(bend.BendAngle))
        for bend in part.DesignEdgebarFeatures
        if bend.Type == -1752010637
    ]


def get_number_Flange(part):
    # Flange Type = -1752010637
    return len(
        [bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == -1752010637]
    )


def get_number_CoutourFlange(part):
    # Flange Type = 281089316
    return len(
        [bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 281089316]
    )


def get_data_ContourFlanges(part):
    # BendRadius, Flange Type = 281089316
    return [
        (contour.Name, "%.3f in" % to_inches(contour.BendRadius))
        for contour in part.DesignEdgebarFeatures
        if contour.Type == 281089316
    ]


def get_number_Hole(part):
    # Hole Type = 462094722
    return len(
        [hole.Name for hole in part.DesignEdgebarFeatures if hole.Type == 462094722]
    )


def get_number_ExtrudedCutout(part):
    # Cutout Type = 462094714
    return len(
        [
            cutout.Name
            for cutout in part.DesignEdgebarFeatures
            if cutout.Type == 462094714
        ]
    )


def get_number_NormalCutout(part):
    # Normal Cutout Type = -292547215
    return len(
        [
            ncutout.Name
            for ncutout in part.DesignEdgebarFeatures
            if ncutout.Type == -292547215
        ]
    )


def check_maximum(dim1, dim2):
    """ Check maximum size possible in sheetmetal. 10"x5"
    """
    ordered_dims = sorted([dim1, dim2])
    width, height = ordered_dims[0], ordered_dims[1]
    if width < 60 and height < 120:
        return "OK"
    else:
        return 'MAX.(10"X5") EXCEEDED'


def pli_exists(part):
    if get_number_Flange(part) or get_number_CoutourFlange(part):
        return True
    return False


def ln(parameters):
    print(
        "[{0:^12}]: {1:<20}{2:.<40}{3:.>25}".format(
            parameters[0], parameters[1], parameters[2], parameters[3]
        )
    )


def properties(part, property):
    return part.Properties.Item("Custom").Item(property).value


def variables(part, variable):
    variables = part.Variables
    variableList = variables.Query(
        pFindCriterium="*",
        NamedBy=SolidEdgeConstants.VariableNameBy.seVariableNameByBoth,
        VarType=SolidEdgeConstants.VariableVarType.SeVariableVarTypeBoth,
    )
    return to_inches(variableList[variable].Value)


def dimensions(X, Y):
    return "{0:.3f} X {1:.3f}".format(X, Y)


def isCopiedPart(part):
    # Copied Part Type = -1871757644
    return len(
        [copy.Name for copy in part.DesignEdgebarFeatures if copy.Type == -1871757644]
    )

def run_check_list(plate):
    """
    Validation of various points in the constuction of the CAD modele.
    """
    if plate.Type == 4:

        # plate.Active()
        print("")
        print("-" * 100)
        print("-> %s:" % plate.Name)
        print("=" * 100)

        # build a logger
        loggingINFO(
            "====================DEBUG MODE======================")
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

        loggingINFO(
            "====================END DEBUG MODE======================")

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
            ("VARIABLES", "A", A, null(A)),
            ("VARIABLES", "N", N, null(N)),
            ("MODE", "MODELING_MODE", mode, valide_mode),
            ("MODELING", "FLAT_PATTERN", "DESIGNED", isflatten),
            ("MANUALS", "DSC_M_A", DSC_M_A, null(DSC_M_A)),
            ("JDE", "JDELITM", JDELITM, null(JDELITM)),
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
            b_max = PLIAGE.get(epaisseur).get(
                "Bmax").get("STEEL PLATE", None)
            hors_tout = PLIAGE.get(epaisseur).get(
                "H").get("STEEL PLATE", None)
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
                ln(("DESIGN", "Angle Max",
                    "degrees (pli interieur B)", angle_max))

        else:
            ln(("STANDARDS", "standards unavailable", "", thickness))

        print("-" * 100)
