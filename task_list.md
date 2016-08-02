# My Tasks

Task list (02.08.2016)

- [x] Run script for all coreutils in LRZ for 1h for each binary
- [x] Check Sebastian's obfuscated files

Task list (29.07.2016)

- [x] Setup fresh system in LRZ
- [x] Install LLVM, afl, KLEE and download coreutils
- [x] Run script to fuzz coreutils for 5' each

Task list (07.07.2016)

- [x] Automate the whole process to test coreutils with afl-fuzz
	- [-] PROGRAM ABORT : Non-alphanumeric fuzzer ID specified via -S or -M
		- Location : fix_up_sync(), afl-fuzz.c:7226
 	
- [x] fuzz coreutils on multiple cores

Task list (30.06.2016)

- [x] Apply the common patch to all coreutils
- [x] Split coreutils into 2 categories:
	- reading from a file
	- reading from stdin
- [x] Write test cases for all coreutils and make sure they work with afl-fuzz
	- test cases missing for:
		-   chroot : ./chroot \$HOME echo \$PWD : ./chroot: cannot change root directory to /home/eirini: Operation not permitted

		-   groups
		-   runcon : ./runcon: runcon may be used only on a SELinux kernel
		-   setuidgid
		-   su
		-   test or [

Task list (23.06.2016)

- [x] Common patch applied to Coreutils
- [x] Test cases for Coreutils to run afl-fuzz
	-	basename.c
	-  dirname.c
	-  du.c 	
	-  echo.c
	-  expr.c
	-  cat.c
	-  printf.c
	-  md5sum.c 
	- id.c
	- link.c
	- ln.c
	- ls.c
	- mkdir.c
	- mkfifo.c
	- mv.c
	- nice.c
	- pathchk.c
	- pinky.c
	- printenv.c
	- vdir.c
	- seq.c
	- yes.c
	- sleep.c
	- factor.c
	- true.c
	- false.c
	- tac.c


Task list (17.06.2016)  

- [x] What common patch to be applied for Coreutils, to make afl-fuzz work with command line arguments?
	- *printf.c is modified	to read from stdin or file (needs more testing)* 
	- *common patch to read from stdin:*
		- *echo.c* 
		- *basename.c*
		- *dirname.c*
		- *du.c*
		- *env.c*
		- *expr.c*
		- *id.c*
		- *kill.c*
		- *link.c*
		- *ln.c*
		- *ls.c*
		- *mkdir.c*
		- *mkfifo.c*
		- *mknod.c*
		- *mktemp.c*
		- *mv.c*
		- *nice.txt*
		- *nohup.c*
		- *pathchk.c*
		- *pinky.c*
        - *printenv.c*
		- *readlink.c*
		- *rm.c*
		- *rmdir.c*
		- *runcon.c*
		- *seq.c*
		- *sleep.c*
		- *touch.c*
		- *unlink.c*
		- *vdir.c*
		- *yes.c*

	- *still to check:* 
		- *install.c*
		- *stat.c*
  
Task list (14.06.2016)

- [x] Change source of printf as shown in [this patch](https://bitbucket.org/jwilk/fuzzing/src/default/patches/coreutils/printf-args.diff?fileviewer=file-view-default)
- [x] Compile and run printf with afl-fuzz
	- [x] test different formats
	- [x] use one argument per text-file
	- [x] use one argument per line
- [x] Apply above to echo
- [x] Make list of all coreutils program that work with command line arguments

- [x] What common patch to be applied for Coreutils, to make afl-fuzz work with command line arguments?
		
- How to read output information from afl-fuzz?
	- [x] Read coverage information with afl-cov
	- [x] Is coverage information enough to know input to the program?
	- [x] If not, then what is the best way to get input to the program, from afl-fuzz? *// I haven't found something else yet..*

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

