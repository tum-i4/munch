#!/bin/bash

targ="--after-function=bc_new_num"
klee="/home/saahil/repos/after-search/Release+Asserts/bin/klee"
llvm_obj="/home/saahil/vdc/bc-1.06/obj-llvm/KLEE-1.3/bc.x.bc"
arg1="--sym-args 1 3 50"
arg2="--sym-files 1 100"
arg3="--sym-stdin 100"

options=( "-posix-runtime" "-libc=uclibc" "-only-output-states-covering-new" "-disable-inlining" "-optimize"
		"-max-solver-time=15" "-max-time=420" "-watchdog" "-search=after-call" )
command=( "$klee" "${options[@]}" "$targ" "$llvm_obj" "$arg1" "$arg2" "$arg3" )

# execute the command
"${command[@]}"
