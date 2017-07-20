Munch
======

This tool performs a sequence of fuzzing and concolic execution on C programs (compiled into LLVM bitcode).

[__AFL__](http://lcamtuf.coredump.cx/afl/) is used for (blackbox) fuzzing. Ideally, this stage should cover most of the easy-to-reach functions in the programs. 

[__KLEE__](https://github.com/tum-i22/klee22/tree/sonar) is used for concolic execution. However, we use a custom fork of KLEE with a specialized implementation of targeted path search, called *sonar* search. Ideally, this stage should cover the (hard-to-reach) functions that were not discovered with fuzzing in the first step. Please use our [KLEE installation guide](https://github.com/tum-i22/klee-install). 

This project is in developmental stage, so do not expect it to work out of the box for you. 

In case of question, simply shoot me an email me at <ognawala@in.tum.de>. 
