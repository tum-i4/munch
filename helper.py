from os.path import expanduser
import subprocess
import json

MYOPT = expanduser("~/build/llvm/Release/bin/opt")
MYLIBMACKEOPT = expanduser("~/git/macke-opt-llvm/bin/libMackeOpt.so")

"""
Reads a list of all functions in topological order
"""
def read_all_funcs(bcfilename):
    popenargs = [MYOPT, "-load", MYLIBMACKEOPT, bcfilename,
        "--listallfuncstopologic", "-disable-output"]
    output = subprocess.check_output(popenargs)
    outjson = json.loads(output.decode("utf-8"))
    return outjson

"""
Flattens nested lists into one single list
"""
def flatten_string_list(deepListOfStrings):
    flattened = []
    for elem in deepListOfStrings:
        if isinstance(elem, str):
            flattened.append(elem)
        else:
            flattened.extend(elem)
    return flattened

"""
Get a list of all functions inside the bitcodefile ordered topologically
from main level down to bottom. SCCs are not marked explicitly.
"""
def get_flat_topology(bcfilename):
    return flatten_string_list(read_all_funcs(bcfilename))

"""
Get a list of all functions inside the bitcodefile ordered topologically
from deep up to main level. SCCs are not marked explicitly.
"""
def get_flat_inversed_topology(bcfilename):
    return reversed(get_flat_topology(bcfilename))


def order_funcs_topologic(list_of_functions):
    print("TODO: order_funcs_topologic() should be replaced "
          "by get_flat_inversed_topology()")
    func = ""
    l = []
    for c in list_of_functions:
        if c not in "[],\n\"":
            if (c == ' ') and (func != ""):
                l.append(func)
                func = ""
            else:
                if c != ' ':
                    func += c
    if func != "":
        l.append(func)

    l.reverse()
    print(l)
    return l
