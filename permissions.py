import clr
import sys

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import System


def username():
    return System.Environment.UserName


def details():
    print("Author: recs@premiertech.com")
    print("Last update: 2020-07-10")


def permissions(app):

    assert app.Value in [
        "Solid Edge ST7",
        "Solid Edge 2019",
    ], "Unvalid version of solidedge"

    user = username()
    print("User: %s" % user)
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
        print("Autorized user ID")
    else:
        print("user with no valid permissions.")
        sys.exit()
