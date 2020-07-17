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

from  standards import MAX, PLIAGE


def raw_input(message):
    Console.WriteLine(message)
    return Console.ReadLine()


def is_exist(path_to_check):
    return Directory.Exists(path_to_check)


def makedirs(path_to_make):
    Directory.CreateDirectory(path_to_make)


def userprofile():
    return System.Environment.GetEnvironmentVariable("USERPROFILE")

def combine(path1, path2):
    return Combine(path1, path2)

def null(content):
    if not content:
        return "MISSING"
    elif content is "-":
        return "MISSING"
    else:
        return "OK"


def flatpattern_exist(part):
    if part.FlatPatternModels.item(1):
        return "OK"
    return "MISSING"


def get_modeling_mode(part):
    mode = part.ModelingMode
    if  mode == 1:
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
    if  mode == 2:
        return "OK"
    else:
        return "WRONG MODE"


def to_inches(m):
    return m * 39.3700787


def convertor_radius_to_degres(angle_in_radians):
    return (angle_in_radians * (180/Math.PI))


def get_data_Flange(part):
    # BendAngle, BendRadius, Flange Type = -1752010637
    return [(
        bend.Name,
        convertor_radius_to_degres(bend.BendAngle),
        ) for bend in part.DesignEdgebarFeatures if bend.Type == -1752010637]

def variables(part, variable):
    variables = part.Variables
    variableList = variables.Query(
        pFindCriterium = "*",
        NamedBy = SolidEdgeConstants.VariableNameBy.seVariableNameByBoth,
        VarType = SolidEdgeConstants.VariableVarType.SeVariableVarTypeBoth,
    )
    return to_inches(variableList[variable].Value)

def get_number_Flange(part):
    # Flange Type = -1752010637
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == -1752010637])


def get_number_CoutourFlange(part):
    # Flange Type = 281089316
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 281089316])


def get_data_ContourFlanges(part):
    # BendRadius, Flange Type = 281089316
    return [(
        contour.Name ,
        "%.3f in" %to_inches(contour.BendRadius),
    ) for contour in part.DesignEdgebarFeatures if contour.Type == 281089316]


def get_number_Hole(part):
    # Hole Type = 462094722
    return len([hole.Name for hole in part.DesignEdgebarFeatures if hole.Type == 462094722])


def get_number_ExtrudedCutout(part):
    # Cutout Type = 462094714
    return len([cutout.Name for cutout in part.DesignEdgebarFeatures if cutout.Type == 462094714])


def get_number_NormalCutout(part):
    # Normal Cutout Type = -292547215
    return len([ncutout.Name for ncutout in part.DesignEdgebarFeatures if ncutout.Type == -292547215])


def check_maximum(*dims):
    """ Check maximum size possible in sheetmetal. 10"x5"
    """
    width, height  = sorted(list(dims))
    if  width < MAX.get('width') and height < MAX.get('height'):
        return "OK"
    else:
        return "max size exceeded"


def pli_exists(part):
    if get_number_Flange(part) or get_number_CoutourFlange(part):
        return True
    else:
        return False

def ln(desc, title, value, validation):
    print("[{0:^12}]: {1:<20}{2:.<40}{3:.>15}".format(desc, title, value, validation))

def properties(part, property):
    return part.Properties.Item("Custom").Item(property).value
