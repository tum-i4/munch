# My Tasks

Task list (14.06.2016)

- [x] Change source of printf as shown in [this patch](https://bitbucket.org/jwilk/fuzzing/src/default/patches/coreutils/printf-args.diff?fileviewer=file-view-default)
- [x] Compile and run printf with afl-fuzz
	- [x] test different formats
	- [x] use one argument per text-file
	- [x] use one argument per line
- [x] Apply above to echo
- [x] Make list of all coreutils program that work with command line arguments
- [ ] What common patch to be applied for Coreutils, to make afl-fuzz work with command line arguments?
- How to read output information from afl-fuzz?
	- [x] Read coverage information with afl-cov
	- [ ] Is coverage information enough to know input to the program?
	- [ ] If not, then what is the best way to get input to the program, from afl-fuzz? *// I haven't found something else yet..*

Task list (7.06.2016)

- [x] Add information about making executables +x
- [x] Add information about running KLEE and analyzing results of KLEE
- [x] Read information about --search argument on KLEE
- [x] Read information about other important arguments for KLEE (at least all the ones used for coreutils and other experiments)
- [x] Record all experiments with AFL in a new file. Just like KLEE. 

- [x] Run Coreutils executables with AFL - time limit half hour, one hour, and overnight. 
    - [x] with a new directory
    - [x] with a new makefile
    - [x] with afl-gcc as new compiler.
    - [x] maybe linker has to be changed. Not sure. Check.
    - [ ] try with echo,
    - [x] try with cat,
    - [x] try with md5sum

Task list (31.05.2016)

- [x] Install KLEE locally
- [x] Run Coreutils Experiment
- [x] Change Makefiles - Make text description of changes
- [x] Make private github repo - add saahil
- [x] Track task items on Github
- [x] Install AFL

