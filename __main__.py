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
from System import Console
from System.IO import Directory
from System.IO.Path import Combine
import SolidEdgeConstants

import permissions, helpers

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

# TODO: [1] develop function
def convertor_meter_to_inch(dim):
    pass

# TODO: [1] develop function
def convertor_radius_to_degres(dim):
    pass

# TODO: [1] develop function
def get_number_of_bend(part):
    # BendAngle
    # BendRadius
    # Flange Type = -1752010637
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == -1752010637])

# TODO: [1] develop function
def get_number_holes(part):
    # Hole Type = 462094722
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 462094722])

# TODO: [1] develop function
def get_number_of_cutouts(part):
    # Cutout Type = 462094714
    return len([bend.Name for bend in part.DesignEdgebarFeatures if bend.Type == 462094714])

def main():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")

        plate = application.ActiveDocument
        assert plate.Type == 4, "This macro only works on plate"

        permissions.details()
        permissions.permissions(application)

        print "\npart: %s" % plate.Name
        print "="*70

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

        print "[NUMBER FLANGES] {0:>20}: {1:>30} {2:>5}".format('NUMBER FLANGES' , get_number_of_bend(plate), "x")
        print "[NUMBER HOLES] {0:>20}: {1:>30} {2:>5}".format('NUMBER HOLES' , get_number_holes(plate) , "x")
        print "[NUMBER CUTOUT] {0:>20}: {1:>30} {2:>5}".format('NUMBER CUTOUT' , get_number_of_cutouts(plate) , "x")

        print "[BOM      ]: {0:<20}{1:.<40}{2:.>5}".format('DSC_A' , dsc_a, blank_field(dsc_a))
        print "[MANUALS  ]: {0:<20}{1:.<40}{2:.>5}".format('DSC_M_A' , dsc_m_a, blank_field(dsc_m_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('EQUIP_A' , equip_a, blank_field(equip_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('SERIE_A' , serie_a, blank_field(serie_a))
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('MODULE_A' , module_a, blank_field(module_a))
        print "[JDE      ]: {0:<20}{1:.<40}{2:.>5}".format('JDELITM' , jdelitm, blank_field(jdelitm))
        print "[MATERIAL ]: {0:<20}{1:.<40}{2:.>5}".format('Material'  ,material , blank_field())
        print "[CAD      ]: {0:<20}{1:.<40}{2:.>5}".format('Teamcenter'  , teamcenter, blank_field())
        print "[UNITS    ]: {0:<20}{1:.<40}{2:.>5}".format('CAD_UOM' , cad_uom, blank_field())
        print "[CATEGORY ]: {0:<20}{1:.<40}{2:.>5}".format('PartType' , parttype, blank_field())
        print "[CATEGORY ]: {0:<20}{1:.<40}{2:.>5}".format('CATEGORY_VB' , category_vb, blank_field())
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('Nom'  , part_name, blank_field())
        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>5}".format('DIM' , Dim, blank_field())
        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>5}".format('Dim1' , dim1, blank_field())
        print "[DIMENSION]: {0:<20}{1:.<40}{2:.>5}".format('Dim2' , dim2, blank_field())
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('JDEDSC1_A' , jdedsc1_a, blank_field())
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('JDEDSC2_A' , jdedsc2_a, blank_field())
        print "[CARTOUCHE]: {0:<20}{1:.<40}{2:.>5}".format('JDESTRX_A' , jdestrx_a, blank_field())
        print "[MODE     ]: {0:<20}{1:.<40}{2:.>5}".format('MODELING_MODE' , get_modeling_mode(plate), validate_modeling_mode(plate))
        print "[MODELING] {0:>20}: {1:>30} {2:>5}".format('FLATE_PATTERN' , "", flatpattern_exist(plate))
        print "[BEND     ]: {0:<20}{1:.<40}{2:.>5}".format('Bend'  , bend, blank_field())

        # VARIABLES:
        variables = plate.Variables
        variableList = variables.Query(
            pFindCriterium = "*",
            NamedBy = SolidEdgeConstants.VariableNameBy.seVariableNameByBoth,
            VarType = SolidEdgeConstants.VariableVarType.SeVariableVarTypeBoth,
        )
        if flatpattern_exist(plate) == "OK":
            print "[DIMENSION] {0:>20}: {1:>30} {2:>5}".format("flatten-dimension", variableList['Flat_Pattern_Model_CutSizeY'].Value, "OK")  # exist only with flate pattern
            print "[DIMENSION] {0:>20}: {1:>30} {2:>5}".format("flatten-dimension", variableList['Flat_Pattern_Model_CutSizeX'].Value, "OK")
        print "[VARIABLES] {0:>20}: {1:>30} {2:>5}".format('A' , variableList['A'].Value, "OK")
        print "[VARIABLES] {0:>20}: {1:>30} {2:>5}".format('N' , variableList['N'].Value, "OK")


        # check number of angles
        # check holes
        # check cutout

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
