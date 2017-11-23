Munch
======

With two modes (FS and SF), this tool performs a sequence of fuzzing and concolic execution on C programs (compiled into LLVM bitcode). The goal is to increase function coverage and, hopefully, finding more (buffer-overflow) vulnerabilities than symbolic execution or fuzzing. 

[__AFL__](http://lcamtuf.coredump.cx/afl/) is used for (blackbox) fuzzing. Ideally, this stage should cover most of the easy-to-reach functions in the programs. 

[__KLEE22__](https://github.com/tum-i22/klee22/tree/sonar) is used for concolic execution. It is a custom fork of KLEE with a specialized implementation of targeted path search, called *sonar* search. Ideally, this stage should cover the (hard-to-reach) functions that were not discovered with fuzzing in the first step. Please use our [KLEE installation guide](https://github.com/tum-i22/klee-install). 

This project is in developmental stage, so please excuse us if it does not work out-of-the-box for you. 

In case of question, simply shoot me an email me at <ognawala@in.tum.de>. 

__N.B.__: You might be interested in our full compositional analysis framework, [__Macke__](https://github.com/tum-i22/macke), for a more vulnerabilities-focussed symbolic execution approach. 
