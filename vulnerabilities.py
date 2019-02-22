import os, sys, glob, json
from os import path

def get_vulnerable_inst(f):
    trace = open(f, "r")

    lines = trace.readlines()
    for i, l in enumerate(lines):
        if "Stack:" in l:
            break

    if "Stack:" in lines[i]:
        top_line = lines[i+1]
    else:
        return None

    if "at" in top_line:
        file, lineno = top_line.split(" at ")[1].split(":")
        file = file.strip()
        lineno = lineno.strip()
        return (file, lineno)
    else:
        return None

def remove_duplicates(errfiles):
    vulns = []
    for f in errfiles:
        inst = get_vulnerable_inst(f)
        if inst and inst not in vulns:
            vulns.append(inst)

    return vulns

def get_afl_vulnerabilities(outdir, binary, options):
    if not path.isdir(path.join(outdir, "crashes_min")):
        cmin_command = "afl-cmin -i %s -o %s -- %s %s"%(path.join(outdir, "crashes"), path.join(outdir, "crashes_min"), binary, options)
        print(cmin_command)
        os.system(cmin_command)

    crashes = glob.glob(path.join(outdir, "crashes_min/*"))
    print("%d unique vulns found by AFL"%(len(crashes)))
    return len(crashes)

def get_klee_vulnerabilities(outdir):
    ptr_errs = glob.glob(path.join(outdir, "klee-out-*/*.ptr.err"))
    print("Found %d ptr.err files"%(len(ptr_errs)))
    print("Filtering by instruction")

    vulns = remove_duplicates(ptr_errs)
    print("%d unique vulns found by KLEE"%(len(vulns)))

    return len(vulns)

def main():
    outdir = sys.argv[1]
    afl_binary = sys.argv[2]
    if len(sys.argv)>3:
        afl_options = " ".join(sys.argv[3:])
    else:
        afl_options = ""

    if not (path.isdir(path.join(outdir, "afl_out")) and path.isdir(path.join(outdir, "klee_out"))):
        print("Hmm, that does not look like a Munch output dir: %s.\nEnding..."%(outdir))
        sys.exit(-1)
    klee_out = path.join(outdir, "klee_out")
    afl_out = path.join(outdir, "afl_out")

    total_unique_vulns = get_klee_vulnerabilities(klee_out) + get_afl_vulnerabilities(afl_out, afl_binary, afl_options)
    vulndict = {"vulninstcount": total_unique_vulns, "bytype": {"main": total_unique_vulns}}

    out_json = open(path.join(outdir, "vulninst.json"), "w")
    json.dump(vulndict, out_json)

if __name__=="__main__":
    main()
