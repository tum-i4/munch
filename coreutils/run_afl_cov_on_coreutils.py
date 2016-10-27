#!/usr/bin/env python

from __future__ import print_function
import os, sys
import subprocess

def main():

	stdin = ["basename", "df", "dirname", "echo" , "factor", "id", "ls", "nohup", "pinky", "printf", "shuf", "touch",
	          "uptime", "who", "comm", "dir", "du", "expr", "ginstall", "join", "nice", "pathchk", "printenv", "seq", "test", "uname", "vdir", "yes"]

	file_progs = ["base64", "cat", "cksum", "expand", "fmt", "fold", "head", "md5sum", "paste", "pr", "ptx", "sha1sum" "sha224sum", "sha256sum", "sha384sum",
	        "sha512sum", "sort" "stat", "sum", "tac", "tail", "tsort", "unexpand", "uniq", "wc"]

	for prog in stdin:
		path_to_afl_results = "/media/vdc/coreutils-6.10/obj-afl/test_afl/sync_dir/" + prog
		command = "./src/" + prog + " AFL_FILE"
		code_dir = "."
		src_file = "media/vdc/coreutils-6.10/src/" + prog + ".c"
		output = prog + ".txt"
		args = ["afl-cov", "-d", path_to_afl_results, "-e", command, "-c", code_dir, "--coverage-include-lines", "--src-file", src_file, "-O"]
                file_to_write = open(output, "w+")
		subprocess.call(args, stdout=file_to_write)
		file_to_write.close()

	for prog in file_progs:
		path_to_afl_results = "/media/vdc/coreutils-6.10/obj-afl/test_afl/sync_dir/" + prog
		command = "\"./src/./" + prog + " AFL_FILE\""
		code_dir = "."
		src_file = "media/vdc/coreutils-6.10/src/" + prog + ".c"
		output = prog + ".txt"
		args = ["sudo", "afl-cov", "-d", path_to_afl_results, "-e", command, "-c", code_dir, "--coverage-include-lines", "--src-file", src_file, "-O"]
		file_to_write = open(output, "w+")
               	subprocess.call(args, stdout=file_to_write)
		file_to_write.close()

	return 1

if __name__ == '__main__':
    main()

