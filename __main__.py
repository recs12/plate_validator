# -*- coding: utf-8 -*-

"""
hide hardware and save the assembly as .jt or parasolid
"""

import sys
import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import jt
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


def validator():
    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")
        print "Author: recs@premiertech.com"
        print "Last update: 2020-06-29"
        print "version solidedge: %s" % application.Value

        assert application.Value in [
            "Solid Edge ST7",
            "Solid Edge 2019",
        ], "Unvalid version of solidedge"

        user = username()
        print "\nUser: %s" % user
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
            "gils2",
            "albp",
            "tres2",
        ]:
            print "Autorized user ID"
        else:
            print("user with no valid permissions.")
            sys.exit()

        plate = application.ActiveDocument
        print "part: %s\n" % plate.Name

        # asm.Type =>  plate :4 , assembly : 3, partdocument: 1
        assert plate.Type == 4, "This macro only works on plate"

        # CARTOUCHE

        print( "[CARTOUCHE] {0:<10}: {1:>20} {2:>10}".format('EQUIP_A' , plate.Properties.Item("Custom").Item('EQUIP_A').value, "OK"))
        print( "[CARTOUCHE] {0:<10}: {1:>20} {2:>10}".format('SERIE_A' , plate.Properties.Item("Custom").Item('SERIE_A').value, "OK"))
        print( "[CARTOUCHE] {0:<10}: {1:>20} {2:>10}".format('MODULE_A' , plate.Properties.Item("Custom").Item('MODULE_A').value, "OK"))
        print( " %s: %s, " % ( 'Teamcenter'  , plate.Properties.Item("Custom").Item('Teamcenter Item Type').value))
        print( " %s: %s, " % ( 'JDELITM' , plate.Properties.Item("Custom").Item('JDELITM').value))
        print( " %s: %s, " % ( 'CATEGORY_VB' , plate.Properties.Item("Custom").Item('CATEGORY_VB').value))
        print( " %s: %s, " % ( 'Material'  , plate.Properties.Item("Custom").Item('Material Thickness').value))
        print( " %s: %s, " % ( 'Bend'  , plate.Properties.Item("Custom").Item('Bend Radius').value))
        print( " %s: %s, " % ( 'Teamcenter'  , plate.Properties.Item("Custom").Item('Teamcenter Item Type').value))
        print( " %s: %s, " % ( 'PartType' , plate.Properties.Item("Custom").Item('PartType').value))
        print( " %s: %s, " % ( 'CATEGORY_VB' , plate.Properties.Item("Custom").Item('CATEGORY_VB').value))
        print( " %s: %s, " % ( 'Nom'  , plate.Properties.Item("Custom").Item('Nom de la piece').value))
        print( " %s: %s, " % ( 'DIM' , plate.Properties.Item("Custom").Item('DIM').value))
        print( " %s: %s, " % ( 'Dim1' , plate.Properties.Item("Custom").Item('Dim1').value))
        print( " %s: %s, " % ( 'Dim2' , plate.Properties.Item("Custom").Item('Dim2').value))
        print( " %s: %s, " % ( 'CAD_UOM' , plate.Properties.Item("Custom").Item('CAD_UOM').value))
        print( " %s: %s, " % ( 'DSC_A' , plate.Properties.Item("Custom").Item('DSC_A').value))
        print( " %s: %s, " % ( 'DSC_M_A' , plate.Properties.Item("Custom").Item('DSC_M_A').value))
        print( " %s: %s, " % ( 'JDEDSC1_A' , plate.Properties.Item("Custom").Item('JDEDSC1_A').value))
        print( " %s: %s, " % ( 'JDEDSC2_A' , plate.Properties.Item("Custom").Item('JDEDSC2_A').value))
        print( " %s: %s, " % ( 'JDESTRX_A' , plate.Properties.Item("Custom").Item('JDESTRX_A').value))

        # Get a reference to the Variables collection.
        variables = plate.Variables

        # // Get a reference to the variablelist.
        variableList = variables.Query(
            pFindCriterium = "*",
            NamedBy = SolidEdgeConstants.VariableNameBy.seVariableNameByBoth,
            VarType = SolidEdgeConstants.VariableVarType.SeVariableVarTypeBoth,
        )

        # // Process variables.
        # print(variableList['Flat_Pattern_Model_CutSizeY'].Value) # exist only with flate pattern
        # print(variableList['Flat_Pattern_Model_CutSizeX'].Value)
        print(variableList['A'].Value)
        print(variableList['N'].Value)
        # print("Dimension: {0} = {1} {2}".format(variable.Type , variable.DisplayName, variable.Value))

        print(plate.ModelingMode) #1 sync #2 ordered

        # flatten
        # if plate.FlatPatternModels.Count >= 1:
        #     print "flatten ok"
        # if plate.FlatPatternModels.Count == 0:
        #     print "flatten failed"

        # check number of angles
        # check if draft exist
        # check holes
        # check cutout

        for f in plate.DesignEdgebarFeatures:
            print(f.Name)

        for i in plate.Models:
            print(i.Name)

    except AssertionError as err:
        print(err.args)

    except Exception as ex:
        print(ex.args)

    finally:
        raw_input("\nPress any key to exit...")
        sys.exit()


def confirmation(func):
    response = raw_input("""Validate sheetmetal parameters ? (Press y/[Y] to proceed.)""")
    if response.lower() not in ["y", "yes", "oui"]:
        print("Process canceled")
        sys.exit()
    else:
        func()


if __name__ == "__main__":
    confirmation(validator)
