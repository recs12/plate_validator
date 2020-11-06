# -*- coding: utf-8 -*-

"""
Quick Check-list for sheetmetal plates.
"""

import sys
import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import System
import System.Runtime.InteropServices as SRI
from System import Console
import helpers

from standards import PLIAGE, thickness_mapping
from helpers import *
from debbug import loggingINFO

__project__ = "plate_validator"
__author__ = "recs"
__version__ = "0.0.2"
__update__ = "2020-11-06"


def main():


    try:
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")

        response = raw_input(
            """Would you like to validate this sheetmetal modeling? (Press y/[Y] to proceed.)\n(Option: Press '*' for processing documents in batch)""")

        if response.lower() in ["y", "yes"]:
            plate = application.ActiveDocument
            run_check_list(plate)

        elif response.lower() in ["*"]:
            # loop through all the plates
            documents = application.Documents
            for plate in documents:
                run_check_list(plate)
        else:
            pass

    except AssertionError as err:
        print(err.args)

    except Exception as ex:
        print(ex.args)

    finally:
        prompt_exit()


if __name__ == "__main__":
    print("%s\n--author:%s --version:%s --last-update :%s\n" %
        (__project__, __author__, __version__, __update__))
    main()