#!/usr/bin/env python

from __future__ import print_function, division
import subprocess

def write_coverage(src_file, prefix, prog, lines):
        pure_code = prefix + prog + "/cov/" +  prog + "_pure_code.txt"
        file_to_write = open(pure_code, "w+")
        subprocess.call(["gcc", "-fpreprocessed", "-dD", "-E", "-P", src_file[0]], stdout=file_to_write)
        file_to_write.close()
        with open(pure_code, "r") as file_to_write:
                file_lines = sum(1 for line_num in file_to_write)
        coverage = '{0:,.2f}'.format((lines / file_lines) * 100)
        with open(prefix + prog + "/cov/" + prog + "_coverage.txt", "a+") as info:
                info.write(src_file[0] + ": " + str(coverage) + "%\n")
                info.close()

def main():

	files = ["basename", "df", "dirname", "echo" , "factor", "id", "ls", "nohup", "pinky", "printf", "shuf", "touch", "uptime", "who", "comm", "dir", "du", "expr", "ginstall", "join", "nice", "pathchk", "printenv", "seq", "test", "uname", "vdir", "yes", "base64", "cat", "cksum", "expand", "fmt", "fold", "head", "md5sum", "paste", "pr", "ptx", "sha1sum" "sha224sum", "sha256sum", "sha384sum", "sha512sum", "sort" "stat", "sum", "tac", "tail", "tsort", "unexpand", "uniq", "wc"]

	prefix = "/media/vdc/coreutils-6.10/obj-afl/test_afl/sync_dir/"
        for prog in files: 
                filename = prefix + prog + "/cov/id-delta-cov"
                f = open(filename, "r")
                next(f)
                lines = 0
                prev = ""
                for line in f:
                        words = line.split(" ")
                        if "src" in words[2]:
                                if "line" in words[3]:
                                        if prev == "":
                                                prev = words[2]
                                                lines += 1
                                        elif words[2] == prev:
                                                lines += 1
                                        else:   
                                                write_coverage(prev.split(","), prefix, prog, lines)
                                                prev = words[2]
                                                lines = 1
                if (lines > 0):
                        write_coverage(prev.split(","), prefix, prog, lines)

        return 1

if __name__ == '__main__':
    main()

