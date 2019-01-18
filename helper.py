from os.path import expanduser
import subprocess
import json
import essentials as es
import os

MYOPT = expanduser(os.environ['HOME'] + "/build/llvm/Release/bin/opt")
MYLIBMACKEOPT = expanduser(os.environ['HOME'] + "/build/macke-opt-llvm/bin/libMackeOpt.so")

MYKLEE = expanduser(os.environ['HOME'] + "/build/klee/Release+Asserts/bin/klee")

"""
Reads the local config file for the analyzed program
"""
def read_config(config_file):
    json_file = open(config_file, "r")
    conf = json.load(json_file)

    #global READ_FROM_FILE, AFL_BINARY, LLVM_OBJ, GCOV_DIR, LLVM_OPT, LIB_MACKEOPT, AFL_BINARY_ARGS, AFL_RESULTS_FOLDER
    global AFL_OBJ, WHICH_KLEE, LLVM_OBJ, TESTCASES, FUZZ_TIME, GCOV_DIR, LLVM_OPT, LIB_MACKEOPT, AFL_BINARY_ARGS, READ_FROM_FILE, OUTPUT_DIR, AFL_RESULTS_FOLDER, KLEE_RESULTS_FOLDER, FUZZ_TIME
    es.AFL_OBJ = conf["AFL_OBJ"]
    es.LLVM_OBJ = conf["LLVM_OBJ"]
    es.GCOV_OBJ = conf["GCOV_OBJ"]
    es.GCOV_DIR = conf["GCOV_DIR"]
    es.LLVM_OPT = conf["LLVM_OPT"]
    es.LIB_MACKEOPT = conf["LIB_MACKEOPT"]
    es.AFL_BINARY_ARGS = conf["AFL_BINARY_ARGS"]
    es.READ_FROM_FILE = conf["READ_FROM_FILE"]
    
    es.OUTPUT_DIR = conf["OUTPUT_DIR"]
    es.AFL_RESULTS_FOLDER = os.path.join(conf["OUTPUT_DIR"], "afl_out")
    es.KLEE_RESULTS_FOLDER = os.path.join(conf["OUTPUT_DIR"], "klee_out")

    es.TESTCASES = conf["TESTCASES"]
    es.FUZZ_TIME = conf["FUZZ_TIME"]
    
    es.WHICH_KLEE = conf["WHICH_KLEE"]

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
Returns a list with only called functions from the extracted call-graph of a program"
"""
def total_funcs_topologic(funcname, outjson, total_funcs):
    nested_dict = outjson.get(funcname)
    if not nested_dict.get("isexternal"):
        total_funcs.append(funcname)
        for call in nested_dict.get("calls"):
          #  print(call)
            if call not in total_funcs:
                total_funcs_topologic(call, outjson, total_funcs)
    return total_funcs

"""
Returns the list with all functions that are internal and called of a bitcode file. 
"""

def get_all_called_funcs(bcfilename):
    total_funcs = []
    popenargs = [es.LLVM_OPT, "-load", es.LIB_MACKEOPT, bcfilename,
    "--extractcallgraph", "-disable-output"]
    output = subprocess.check_output(popenargs)
    outjson = json.loads(output.decode("utf-8"))

    if outjson.get("main") != None:
        total_funcs = total_funcs_topologic("main", outjson, [])
    return total_funcs

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
