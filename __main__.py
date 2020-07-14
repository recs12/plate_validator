# -*- coding: utf-8 -*-

"""
hide hardware and save the assembly as .jt or parasolid
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

from  standards import MAX

def blank_field(content):
    if not content:
        return "MISSING"
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

def convertor_meters_to_inches(m):
    return (m * 39.3700787)

def convertor_radius_to_degres(angle_in_radians):
    return (angle_in_radians * (180/Math.PI))

# TODO: [1] develop function
def get_number_Flange(part):
    #  BendAngle
    # BendRadius
    # Flange Type = -1752010637
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == -1752010637])

# TODO: [1] develop function
def get_number_CoutourFlange(part):
    #  BendAngle
    # BendRadius
    # Flange Type = 281089316
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 281089316])

# TODO: [1] develop function
def get_number_Hole(part):
    # Hole Type = 462094722
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 462094722])

def get_number_ExtrudedCutout(part):
    # Cutout Type = 462094714
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 462094714])

# TODO: [1] develop function
def get_number_NormalCutout(part):
    # Normal Cutout Type = -292547215
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == -292547215])

# TODO: [1] develop the concept
def check_maximum(*dims):
    """ Check maximum size possible in sheetmetal. 10"x5"
    """
    width, height  = sorted(list(dims))
    if  width < MAX.get('width') and height < MAX.get('height'):
        return "OK"
    else:
        return "max size exceeded"

def main():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")

        plate = application.ActiveDocument
        assert plate.Type == 4, "This macro only works on plate"

        permissions.details()
        permissions.permissions(application)

        print "\npart: %s" % plate.Name
        print "="*75

        equip_a = plate.Properties.Item("Custom").Item('EQUIP_A').value
        serie_a = plate.Properties.Item("Custom").Item('SERIE_A').value
        module_a = plate.Properties.Item("Custom").Item('MODULE_A').value
        jdelitm = plate.Properties.Item("Custom").Item('JDELITM').value
        material  = plate.Properties.Item("Custom").Item('Material Thickness').value
        bend  = plate.Properties.Item("Custom").Item('Bend Radius').value
        teamcenter  = plate.Properties.Item("Custom").Item('Teamcenter Item Type').value
        parttype = plate.Properties.Item("Custom").Item('PartType').value
        category_vb = plate.Properties.Item("Custom").Item('CATEGORY_VB').value
        part_name  = plate.Properties.Item("Custom").Item('Nom de la piece').value
        dim = plate.Properties.Item("Custom").Item('DIM').value
        dim1 = plate.Properties.Item("Custom").Item('Dim1').value
        dim2 = plate.Properties.Item("Custom").Item('Dim2').value
        cad_uom = plate.Properties.Item("Custom").Item('CAD_UOM').value
        dsc_a = plate.Properties.Item("Custom").Item('DSC_A').value
        dsc_m_a = plate.Properties.Item("Custom").Item('DSC_M_A').value
        jdedsc1_a = plate.Properties.Item("Custom").Item('JDEDSC1_A').value
        jdedsc2_a = plate.Properties.Item("Custom").Item('JDEDSC2_A').value
        jdestrx_a = plate.Properties.Item("Custom").Item('JDESTRX_A').value

        # VARIABLES:
        variables = plate.Variables
        variableList = variables.Query(
            pFindCriterium = "*",
            NamedBy = SolidEdgeConstants.VariableNameBy.seVariableNameByBoth,
            VarType = SolidEdgeConstants.VariableVarType.SeVariableVarTypeBoth,
        )

        # CHECK MAXIMUM DIMENSIONS

        max_Y = convertor_meters_to_inches(variableList['Flat_Pattern_Model_CutSizeY'].Value)
        max_X = convertor_meters_to_inches(variableList['Flat_Pattern_Model_CutSizeX'].Value)

        # DISPLAY:

        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>15}".format('DIM' , dim, blank_field(dim))
        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>15}".format('Dim1' , dim1, blank_field(dim1))
        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>15}".format('Dim2' , dim2, blank_field(dim2))
        if flatpattern_exist(plate) == "OK":
            print "[DIMENSION]: {0:<20}{1}X{2}{3:.>15}".format("flatten-dimension", max_X, max_Y, check_maximum(max_X, max_Y))  # exist only with flate pattern

        print "[VARIABLES]: {0:<20}{1:.<40}{2:.>15}".format('A' , convertor_meters_to_inches(variableList['A'].Value), "ok")
        print "[VARIABLES]: {0:<20}{1:.<40}{2:.>15}".format('N' , convertor_meters_to_inches(variableList['N'].Value), "ok")

        # MODELING:
        print "[MODE     ]: {0:<20}{1:.<40}{2:.>15}".format('MODELING_MODE' , get_modeling_mode(plate), validate_modeling_mode(plate))

        # FEATURES:
        print "[FLANGE   ]: {0:<20}{1:.<40}{2:.>15}".format('FLANGES' , get_number_Flange(plate), "x")
        print "[CTRFLANGE]: {0:<20}{1:.<40}{2:.>15}".format('CONTOUR FLANGES' , get_number_CoutourFlange(plate), "x")
        print "[HOLE     ]: {0:<20}{1:.<40}{2:.>15}".format('HOLES' , get_number_Hole(plate) , "x")
        print "[CUTOUT   ]: {0:<20}{1:.<40}{2:.>15}".format('CUTOUT' , get_number_ExtrudedCutout(plate) , "x")
        print "[CUTNORMAL]: {0:<20}{1:.<40}{2:.>15}".format('NORMAL_CUTOUT' , get_number_NormalCutout(plate) , "x")

        print "[BOM      ]: {0:<20}{1:.<40}{2:.>15}".format('DSC_A' , dsc_a, blank_field(dsc_a))
        print "[MANUALS  ]: {0:<20}{1:.<40}{2:.>15}".format('DSC_M_A' , dsc_m_a, blank_field(dsc_m_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('EQUIP_A' , equip_a, blank_field(equip_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('SERIE_A' , serie_a, blank_field(serie_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('MODULE_A' , module_a, blank_field(module_a))
        print "[JDE      ]: {0:<20}{1:.<40}{2:.>15}".format('JDELITM' , jdelitm, blank_field(jdelitm))
        print "[MATERIAL ]: {0:<20}{1:.<40}{2:.>15}".format('Material'  , material, blank_field(material))
        print "[CAD      ]: {0:<20}{1:.<40}{2:.>15}".format('Teamcenter', teamcenter, blank_field(teamcenter))
        print "[UNITS    ]: {0:<20}{1:.<40}{2:.>15}".format('CAD_UOM' , cad_uom, blank_field(cad_uom))
        print "[CATEGORY ]: {0:<20}{1:.<40}{2:.>15}".format('PartType' , parttype, blank_field(parttype))
        print "[CATEGORY ]: {0:<20}{1:.<40}{2:.>15}".format('CATEGORY_VB' , category_vb, blank_field(category_vb))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('Nom'  , part_name, blank_field(part_name))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('JDEDSC1_A' , jdedsc1_a, blank_field(jdedsc1_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('JDEDSC2_A' , jdedsc2_a, blank_field(jdedsc2_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>15}".format('JDESTRX_A' , jdestrx_a, blank_field(jdestrx_a))
        print "[MODELING ]: {0:<20}{1:.<40}{2:.>15}".format('FLATE_PATTERN' , "", flatpattern_exist(plate))
        print "[BEND     ]: {0:<20}{1:.<40}{2:.>15}".format('Bend'  , bend , "update")



        # CHECK THE HOLE OPTIONS

        # Implement first standards.py  then standards.yaml
        # refactor helpers.py standards.py
        # refactor permissions.py

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


# TODO: [2] check features under constrainted.
