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


def raw_input(message):
    Console.WriteLine(message)
    return Console.ReadLine()


def is_exist(path_to_check):
    return Directory.Exists(path_to_check)


def makedirs(path_to_make):
    Directory.CreateDirectory(path_to_make)


def userprofile():
    return System.Environment.GetEnvironmentVariable("USERPROFILE")


def username():
    return System.Environment.UserName


def combine(path1, path2):
    return Combine(path1, path2)

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

def convertor_meter_to_inch(dim):
    pass

def convertor_radius_to_degres(dim):
    pass

def get_number_of_bend(part):
    pass

def get_number_holes(part):
    pass

def get_number_of_cutouts(part):
    pass

def main():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")
        print "Author: recs@premiertech.com"
        print "Last update: 2020-07-10"

        assert application.Value in [
            "Solid Edge ST7",
            "Solid Edge 2019",
        ], "Unvalid version of solidedge"

        user = username()
        print "User: %s" % user
        if user.lower() in [
            "alba",
            "bouc11",
            "lapc3",
            "peld6",
            "fouj3",
            "cotk2",
            "nunk",
            "beam",
            "boum3",
            "morm8",
            "benn2",
            "recs",
            "slimane",
            "gils2",
            "albp",
            "tres2",
        ]:
            print "Autorized user ID"
        else:
            print "user with no valid permissions."
            sys.exit()

        plate = application.ActiveDocument
        print "\npart: %s" % plate.Name
        print "="*70

        # Code for plate : 4
        assert plate.Type == 4, "This macro only works on plate"

        equipe_a = plate.Properties.Item("Custom").Item('EQUIP_A').value
        serie_a = plate.Properties.Item("Custom").Item('SERIE_A').value

        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('EQUIP_A' , equipe_a, blank_field(equipe_a))
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('SERIE_A' , serie_a, blank_field(serie_a))
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('MODULE_A' , plate.Properties.Item("Custom").Item('MODULE_A').value, "OK")
        print "[JDE      ] {0:>20}: {1:>30} {2:>5}".format('JDELITM' , plate.Properties.Item("Custom").Item('JDELITM').value, "OK")
        print "[MATERIAL ] {0:>20}: {1:>30} {2:>5}".format('Material'  , plate.Properties.Item("Custom").Item('Material Thickness').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('Bend'  , plate.Properties.Item("Custom").Item('Bend Radius').value, "OK")
        print "[CAD      ] {0:>20}: {1:>30} {2:>5}".format('Teamcenter'  , plate.Properties.Item("Custom").Item('Teamcenter Item Type').value, "OK")
        print "[CATEGORY ] {0:>20}: {1:>30} {2:>5}".format('PartType' , plate.Properties.Item("Custom").Item('PartType').value, "OK")
        print "[CATEGORY ] {0:>20}: {1:>30} {2:>5}".format('CATEGORY_VB' , plate.Properties.Item("Custom").Item('CATEGORY_VB').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('Nom'  , plate.Properties.Item("Custom").Item('Nom de la piece').value, "OK")
        print "[DIMENSION] {0:>20}: {1:>30} {2:>5}".format('DIM' , plate.Properties.Item("Custom").Item('DIM').value, "OK")
        print "[DIMENSION] {0:>20}: {1:>30} {2:>5}".format('Dim1' , plate.Properties.Item("Custom").Item('Dim1').value, "OK")
        print "[DIMENSION] {0:>20}: {1:>30} {2:>5}".format('Dim2' , plate.Properties.Item("Custom").Item('Dim2').value, "OK")
        print "[UNITS    ] {0:>20}: {1:>30} {2:>5}".format('CAD_UOM' , plate.Properties.Item("Custom").Item('CAD_UOM').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('DSC_A' , plate.Properties.Item("Custom").Item('DSC_A').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('DSC_M_A' , plate.Properties.Item("Custom").Item('DSC_M_A').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('JDEDSC1_A' , plate.Properties.Item("Custom").Item('JDEDSC1_A').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('JDEDSC2_A' , plate.Properties.Item("Custom").Item('JDEDSC2_A').value, "OK")
        print "[CARTOUCHE] {0:>20}: {1:>30} {2:>5}".format('JDESTRX_A' , plate.Properties.Item("Custom").Item('JDESTRX_A').value, "OK")
        print "[MODE     ] {0:>20}: {1:>30} {2:>5}".format('MODELING MODE' , get_modeling_mode(plate), validate_modeling_mode(plate))
        print "[MODELING] {0:>20}: {1:>30} {2:>5}".format('Flat-Pattern' , "", flatpattern_exist(plate))

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

        print "\n"
        print "Features (list):"
        for f in plate.DesignEdgebarFeatures:
            print(f.Name)

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
