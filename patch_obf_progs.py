#!/usr/bin/env python3

import os, sys

def main(argv):

    # run program as:
    # python <script> <obf_prog> <patch>

    try:
        obf_prog = sys.argv[1]    # name of the obfuscated program to patch
        afl_patch = sys.argv[2] # patch for afl in order main to read the args from stdin
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # 1. patch the obfuscated program with the patch
    f = open(obf_prog, "r+")
    lines = f.readlines()
    f.close()

    output_file = obf_prog[:-2] + "_afl.c"
    print("Output file: " + output_file)
    struct = 0
    main = 0
    output_lines = []
    output_lines.append("#include <getopt.h>\n")
    output_lines.append("#include <stdio.h>\n")
    output_lines.append("#include <stdlib.h>\n")
    output_lines.append("#include <sys/types.h>\n")
    output_lines.append("#include <assert.h>\n")
    output_lines.append("#define NDEBUG 1\n")
    output_lines.append("#define SIZE 99999\n")
    output_lines.append("#undef initialize_main\n")
    output_lines.append("void initialize_main(int *argc, char ***argv) ;\n")
    output_lines.append("int* a ;\n")
    
    for line in lines:
        #if "/*" in line:
        #    continue
        if struct > 0:
            struct -= 1
            continue
        if main == 1 and "{" in line:
            main = 0
            output_lines.append("int main(int argc , char *argv[] ) {\n")
            output_lines.append("  initialize_main (&argc, &argv);\n")
            output_lines.append("  int *a;\n")
            continue
        if line.startswith("extern int fclose"):
            continue
        elif line.startswith("extern void *fopen"):
            continue
        elif line.startswith("extern int fprintf(struct"):
            continue
        elif line.startswith("extern unsigned long strtoul(char"):
            continue
        elif line.startswith("extern double strtod(char"):
            continue
        elif line.startswith("extern long strtol(char"):
            continue
        elif line.startswith("struct timeval"):
            struct = 3
        #elif "int main(int argc , char *argv[] )" in line:
        #    if main == 0:
        #        main = 1
        elif "printf(\"You win!" in line:
            output_lines.append(line)
            output_lines.append("    printf(\"%d\", a[10]);\n")
        else:
            output_lines.append(line)

    f = open(afl_patch, "r+")
    lines = f.readlines()
    f.close()
    for line in lines:
        output_lines.append(line)

    f = open(output_file, "w")
    f.write("".join(output_lines))
    f.close()

if __name__ == '__main__':
    main(sys.argv[1:])

