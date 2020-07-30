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


def raw_input(message):
    Console.WriteLine(message)
    return Console.ReadLine()


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
