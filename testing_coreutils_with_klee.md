# Testing GNU Coreutils with KLEE

#### on Ubuntu 14.04 LTS 64bit with LLVM 3.4


1. KLEE should be configured and built with uclibc and POSIX runtime support. You will also need to set the following enviromental variable:

 ```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
 ```

2. Build Coreutils with LLVM

 Download and unpack the source for [coreutils](http://www.gnu.org/software/coreutils/coreutils.html). Here we use the version 6.10.
 
 ```
 coreutils-6.10$ mkdir obj-llvm
 coreutils-6.10$ cd obj-llvm
 obj-llvm$ ../configure --disable-nls CFLAGS="-g"
 ```
 In order to compile properly the sources into LLVM bitcode files, we need to make some changes to the Makefiles (i.e. llvm-ld has been removed from LLVM 3.4, we can use llvm-link instead).
 
 In **obj-llvm/Makefile** modify the corresponding lines:
 
 ```
 CC = clang-3.4 -emit-llvm -c
 gl_LIBOBJS =  acl.o argmatch.o asnprintf.o asprintf.o backupfile.o basename.o c-strtod.o c-strtold.o canon-host.o canonicalize.o chdir-long.o cloexec.o close-stream.o closein.o closeout.o creat-safer.o cycle-check.o dirchownmod.o dirname.o dup-safer.o exclude.o exitfail.o fd-safer.o file-has-acl.o file-type.o filemode.o filenamecat.o fopen-safer.o fprintftime.o frexpl.o fsusage.o fts.o gethrxtime.o getndelim2.o getpass.o gettime.o getugroups.o hard-locale.o hash.o human.o i-ring.o idcache.o imaxtostr.o isapipe.o isnanl.o long-options.o md5.o memcasecmp.o memcoll.o mgetgroups.o mkancesdirs.o mkdir-p.o mkstemp-safer.o modechange.o mountlist.o mpsort.o nanosleep.o offtostr.o open-safer.o openat-proc.o physmem.o pipe-safer.o posixtm.o posixver.o printf-args.o printf-parse.o quote.o quotearg.o readtokens.o readutmp.o regex.o root-dev-ino.o safe-read.o safe-write.o same.o save-cwd.o savedir.o selinux-at.o settime.o sha1.o sig2str.o strftime.o stripslash.o tempname.o uinttostr.o umaxtostr.o unlinkdir.o userspec.o utimecmp.o utimens.o vasnprintf.o vasprintf.o vfprintf.o vprintf.o write-any-file.o xgetcwd.o xmalloc.o xnanosleep.o xstrtod.o xstrtol.o xstrtol-error.o xstrtold.o xstrtoul.o yesno.o
gl_LTLIBOBJS =  acl.lo argmatch.lo asnprintf.lo asprintf.lo backupfile.lo basename.lo c-strtod.lo c-strtold.lo canon-host.lo canonicalize.lo chdir-long.lo cloexec.lo close-stream.lo closein.lo closeout.lo creat-safer.lo cycle-check.lo dirchownmod.lo dirname.lo dup-safer.lo exclude.lo exitfail.lo fd-safer.lo file-has-acl.lo file-type.lo filemode.lo filenamecat.lo fopen-safer.lo fprintftime.lo frexpl.lo fsusage.lo fts.lo gethrxtime.lo getndelim2.lo getpass.lo gettime.lo getugroups.lo hard-locale.lo hash.lo human.lo i-ring.lo idcache.lo imaxtostr.lo isapipe.lo isnanl.lo long-options.lo md5.lo memcasecmp.lo memcoll.lo mgetgroups.lo mkancesdirs.lo mkdir-p.lo mkstemp-safer.lo modechange.lo mountlist.lo mpsort.lo nanosleep.lo offtostr.lo open-safer.lo openat-proc.lo physmem.lo pipe-safer.lo posixtm.lo posixver.lo printf-args.lo printf-parse.lo quote.lo quotearg.lo readtokens.lo readutmp.lo regex.lo root-dev-ino.lo safe-read.lo safe-write.lo same.lo save-cwd.lo savedir.lo selinux-at.lo settime.lo sha1.lo sig2str.lo strftime.lo stripslash.lo tempname.lo uinttostr.lo umaxtostr.lo unlinkdir.lo userspec.lo utimecmp.lo utimens.lo vasnprintf.lo vasprintf.lo vfprintf.lo vprintf.lo write-any-file.lo xgetcwd.lo xmalloc.lo xnanosleep.lo xstrtod.lo xstrtol.lo xstrtol-error.lo xstrtold.lo xstrtoul.lo yesno.lo
SUBDIRS = lib src doc po tests gnulib-tests
 ```
 
 In **obj-llvm/src/Makefile** modify the corresponding lines:
 
 ```
 CCLD = llvm-link-3.4
 LINK = $(CCLD) -o $@
 CC = clang-3.4 -emit-llvm -c
 gl_LIBOBJS =  acl.o argmatch.o asnprintf.o asprintf.o backupfile.o basename.o c-strtod.o c-strtold.o canon-host.o canonicalize.o chdir-long.o cloexec.o close-stream.o closein.o closeout.o creat-safer.o cycle-check.o dirchownmod.o dirname.o dup-safer.o exclude.o exitfail.o fd-safer.o file-has-acl.o file-type.o filemode.o filenamecat.o fopen-safer.o fprintftime.o frexpl.o fsusage.o fts.o gethrxtime.o getndelim2.o getpass.o gettime.o getugroups.o hard-locale.o hash.o human.o i-ring.o idcache.o imaxtostr.o isapipe.o isnanl.o long-options.o md5.o memcasecmp.o memcoll.o mgetgroups.o mkancesdirs.o mkdir-p.o mkstemp-safer.o modechange.o mountlist.o mpsort.o nanosleep.o offtostr.o open-safer.o openat-proc.o physmem.o pipe-safer.o posixtm.o posixver.o printf-args.o printf-parse.o quote.o quotearg.o readtokens.o readutmp.o regex.o root-dev-ino.o safe-read.o safe-write.o same.o save-cwd.o savedir.o selinux-at.o settime.o sha1.o sig2str.o strftime.o stripslash.o tempname.o uinttostr.o umaxtostr.o unlinkdir.o userspec.o utimecmp.o utimens.o vasnprintf.o vasprintf.o vfprintf.o vprintf.o write-any-file.o xgetcwd.o xmalloc.o xnanosleep.o xstrtod.o xstrtol.o xstrtol-error.o xstrtold.o xstrtoul.o yesno.o
gl_LTLIBOBJS =  acl.lo argmatch.lo asnprintf.lo asprintf.lo backupfile.lo basename.lo c-strtod.lo c-strtold.lo canon-host.lo canonicalize.lo chdir-long.lo cloexec.lo close-stream.lo closein.lo closeout.lo creat-safer.lo cycle-check.lo dirchownmod.lo dirname.lo dup-safer.lo exclude.lo exitfail.lo fd-safer.lo file-has-acl.lo file-type.lo filemode.lo filenamecat.lo fopen-safer.lo fprintftime.lo frexpl.lo fsusage.lo fts.lo gethrxtime.lo getndelim2.lo getpass.lo gettime.lo getugroups.lo hard-locale.lo hash.lo human.lo i-ring.lo idcache.lo imaxtostr.lo isapipe.lo isnanl.lo long-options.lo md5.lo memcasecmp.lo memcoll.lo mgetgroups.lo mkancesdirs.lo mkdir-p.lo mkstemp-safer.lo modechange.lo mountlist.lo mpsort.lo nanosleep.lo offtostr.lo open-safer.lo openat-proc.lo physmem.lo pipe-safer.lo posixtm.lo posixver.lo printf-args.lo printf-parse.lo quote.lo quotearg.lo readtokens.lo readutmp.lo regex.lo root-dev-ino.lo safe-read.lo safe-write.lo same.lo save-cwd.lo savedir.lo selinux-at.lo settime.lo sha1.lo sig2str.lo strftime.lo stripslash.lo tempname.lo uinttostr.lo umaxtostr.lo unlinkdir.lo userspec.lo utimecmp.lo utimens.lo vasnprintf.lo vasprintf.lo vfprintf.lo vprintf.lo write-any-file.lo xgetcwd.lo xmalloc.lo xnanosleep.lo xstrtod.lo xstrtol.lo xstrtol-error.lo xstrtold.lo xstrtoul.lo yesno.lo 
LDADD = ../lib/libcoreutils.a 
su_LDADD = $(LDADD)
stat_LDADD = $(LDADD)
csplit$(EXEEXT): $(csplit_OBJECTS) $(csplit_DEPENDENCIES) 
	    @rm -f csplit$(EXEEXT)
	    $(LINK) $(csplit_OBJECTS)
 ```
 
 In **obj-llvm/lib/Makefile** modify the corresponding lines:

 ```
 AR = llvm-link-3.4
 ARFLAGS = -o
 CC = clang-3.4 -emit-llvm -c
 gl_LIBOBJS =  acl.o argmatch.o asnprintf.o asprintf.o backupfile.o basename.o c-strtod.o c-strtold.o canon-host.o canonicalize.o chdir-long.o cloexec.o close-stream.o closein.o closeout.o creat-safer.o cycle-check.o dirchownmod.o dirname.o dup-safer.o exclude.o exitfail.o fd-safer.o file-has-acl.o file-type.o filemode.o filenamecat.o fopen-safer.o fprintftime.o frexpl.o fsusage.o fts.o gethrxtime.o getndelim2.o getpass.o gettime.o getugroups.o hard-locale.o hash.o human.o i-ring.o idcache.o imaxtostr.o isapipe.o isnanl.o long-options.o md5.o memcasecmp.o memcoll.o mgetgroups.o mkancesdirs.o mkdir-p.o mkstemp-safer.o modechange.o mountlist.o mpsort.o nanosleep.o offtostr.o open-safer.o openat-proc.o physmem.o pipe-safer.o posixtm.o posixver.o printf-args.o printf-parse.o quote.o quotearg.o readtokens.o readutmp.o regex.o root-dev-ino.o safe-read.o safe-write.o same.o save-cwd.o savedir.o selinux-at.o settime.o sha1.o sig2str.o strftime.o stripslash.o tempname.o uinttostr.o umaxtostr.o unlinkdir.o userspec.o utimecmp.o utimens.o vasnprintf.o vasprintf.o vfprintf.o vprintf.o write-any-file.o xgetcwd.o xmalloc.o xnanosleep.o xstrtod.o xstrtol.o xstrtol-error.o xstrtold.o xstrtoul.o yesno.o
gl_LTLIBOBJS =  acl.lo argmatch.lo asnprintf.lo asprintf.lo backupfile.lo basename.lo c-strtod.lo c-strtold.lo canon-host.lo canonicalize.lo chdir-long.lo cloexec.lo close-stream.lo closein.lo closeout.lo creat-safer.lo cycle-check.lo dirchownmod.lo dirname.lo dup-safer.lo exclude.lo exitfail.lo fd-safer.lo file-has-acl.lo file-type.lo filemode.lo filenamecat.lo fopen-safer.lo fprintftime.lo frexpl.lo fsusage.lo fts.lo gethrxtime.lo getndelim2.lo getpass.lo gettime.lo getugroups.lo hard-locale.lo hash.lo human.lo i-ring.lo idcache.lo imaxtostr.lo isapipe.lo isnanl.lo long-options.lo md5.lo memcasecmp.lo memcoll.lo mgetgroups.lo mkancesdirs.lo mkdir-p.lo mkstemp-safer.lo modechange.lo mountlist.lo mpsort.lo nanosleep.lo offtostr.lo open-safer.lo openat-proc.lo physmem.lo pipe-safer.lo posixtm.lo posixver.lo printf-args.lo printf-parse.lo quote.lo quotearg.lo readtokens.lo readutmp.lo regex.lo root-dev-ino.lo safe-read.lo safe-write.lo same.lo save-cwd.lo savedir.lo selinux-at.lo settime.lo sha1.lo sig2str.lo strftime.lo stripslash.lo tempname.lo uinttostr.lo umaxtostr.lo unlinkdir.lo userspec.lo utimecmp.lo utimens.lo vasnprintf.lo vasprintf.lo vfprintf.lo vprintf.lo write-any-file.lo xgetcwd.lo xmalloc.lo xnanosleep.lo xstrtod.lo xstrtol.lo xstrtol-error.lo xstrtold.lo xstrtoul.lo yesno.lo
libcoreutils.a: $(libcoreutils_a_OBJECTS) $(libcoreutils_a_DEPENDENCIES) 
	    -rm -f libcoreutils.a
	    $(libcoreutils_a_AR) libcoreutils.a $(libcoreutils_a_OBJECTS) $(libcoreutils_a_LIBADD)
 ```
 
 Now we can proceed:
 
 ``` 
 obj-llvm$ make
 obj-llvm$ make -C src arch hostname
 ```
 
 If all went well, you should now have in **src/** folder LLVM bitcode versions of Coreutils! Change also the permissions of all files in the folder in order to be able to run the executables.
 
 ```
 obj-llvm$ chmod 755 -R src/
 obj-llvm$ cd src
 src$ ls -l ls echo cat
 -rwxr-xr-x 1 eirini eirini 1488004 Mai 28 14:57 cat
 -rwxr-xr-x 1 eirini eirini 1478740 Mai 28 14:57 echo
 -rwxr-xr-x 1 eirini eirini 1644872 Mai 28 14:57 ls
 obj-llvm/src$ ./cat --version
 cat (GNU coreutils) 6.10
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
 
 0  libLLVM-3.4.so.1 0x00007f772b3fe042 llvm::sys::PrintStackTrace(_IO_FILE*) + 34
1  libLLVM-3.4.so.1 0x00007f772b3fde34
2  libpthread.so.0  0x00007f772a301330
3  libLLVM-3.4.so.1 0x00007f772b52267a
4  libLLVM-3.4.so.1 0x00007f772b522cba
5  libLLVM-3.4.so.1 0x00007f772adcda27 llvm::FPPassManager::runOnFunction(llvm::Function&) + 471
6  libLLVM-3.4.so.1 0x00007f772adcfa26 llvm::legacy::FunctionPassManagerImpl::run(llvm::Function&) + 102
7  libLLVM-3.4.so.1 0x00007f772adcfaf4 llvm::legacy::FunctionPassManager::run(llvm::Function&) + 84
8  libLLVM-3.4.so.1 0x00007f772af44044 llvm::JIT::jitTheFunction(llvm::Function*, llvm::MutexGuard const&) + 36
9  libLLVM-3.4.so.1 0x00007f772af4463f llvm::JIT::runJITOnFunctionUnlocked(llvm::Function*, llvm::MutexGuard const&) + 15
10 libLLVM-3.4.so.1 0x00007f772af44812 llvm::JIT::getPointerToFunction(llvm::Function*) + 210
11 libLLVM-3.4.so.1 0x00007f772af52ceb
12 libLLVM-3.4.so.1 0x00007f772b5c0c01
13 libLLVM-3.4.so.1 0x00007f772b5c06fa X86CompilationCallback + 74
Stack dump:
0.	Program arguments: /usr/bin/lli-3.4 ./cat --version 
1.	Running pass 'X86 Machine Code Emitter' on function '@rpl_vfprintf'
Segmentation fault (core dumped)
 ```
 
 
3. Using KLEE as an interpreter for LLVM bitcode

 ```
 src$ klee --libc=uclibc --posix-runtime ./cat --version
 KLEE: NOTE: Using klee-uclibc : /usr/local/lib/klee/runtime/klee-uclibc.bca
 KLEE: NOTE: Using model: /usr/local/lib/klee/runtime/libkleeRuntimePOSIX.bca
 KLEE: output directory is "/home/.../obj-llvm/src/./klee-out-0"
 Using STP solver backend
 KLEE: WARNING ONCE: function "socket" has inline asm
 KLEE: WARNING ONCE: function "__libc_connect" has inline asm
 KLEE: WARNING ONCE: function "__libc_recvfrom" has inline asm
 KLEE: WARNING ONCE: function "__libc_sendto" has inline asm
 KLEE: WARNING: undefined reference to function: __ctype_b_loc
 KLEE: WARNING: undefined reference to function: __signbitl
 KLEE: WARNING: undefined reference to function: creat
 KLEE: WARNING: undefined reference to function: fdopendir
 KLEE: WARNING: undefined reference to function: freelocale
 KLEE: WARNING: undefined reference to function: iconv
 KLEE: WARNING: undefined reference to function: iconv_open
 KLEE: WARNING: undefined reference to function: klee_posix_prefer_cex
 KLEE: WARNING: undefined reference to function: newlocale
 KLEE: WARNING: undefined reference to function: strtod_l
 KLEE: WARNING: undefined reference to function: strtold_l
 KLEE: WARNING: executable has module level assembly (ignoring)
 KLEE: WARNING ONCE: calling external: syscall(16, 0, 21505, 122921568)
 KLEE: WARNING ONCE: calling __user_main with extra arguments.
 KLEE: WARNING ONCE: calling external: getpagesize()
 KLEE: WARNING ONCE: calling external: vprintf(122363584, 123116928)
 cat (GNU coreutils) 6.10

 License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
 This is free software: you are free to change and redistribute it.
 There is NO WARRANTY, to the extent permitted by law.

 Written by Torbjorn Granlund and Richard M. Stallman.
 KLEE: WARNING ONCE: calling close_stdout with extra arguments.

 KLEE: done: total instructions = 31486
 KLEE: done: completed paths = 1
 KLEE: done: generated tests = 1
 ```
  
4. Introducing symbolic data to an application

   Run KLEE on the echo application.

 ```
 src$ klee --libc=uclibc --posix-runtime ./echo --help
 ...
 
 KLEE: ERROR: /full/path/to/klee/runtime/POSIX/klee_init_env.c:24: klee_init_env
 
 usage: (klee_init_env) [options] [program arguments]
  -sym-arg <N>              - Replace by a symbolic argument with length N
  -sym-args <MIN> <MAX> <N> - Replace by at least MIN arguments and at most
                              MAX arguments, each with maximum length N
  -sym-files <NUM> <N>      - Make stdin and up to NUM symbolic files, each
                              with maximum size N.
  -sym-stdout               - Make stdout symbolic.
  -max-fail <N>             - Allow up to <N> injected failures
  -fd-fail                  - Shortcut for '-max-fail 1'

 KLEE: NOTE: now ignoring this error at this location

 KLEE: done: total instructions = 5159
 KLEE: done: completed paths = 1
 KLEE: done: generated tests = 1
 ```
 Run echo with a symbolic argument of 3 characters:
 
  ```
  KLEE: NOTE: Using klee-uclibc : /usr/local/lib/klee/runtime/klee-uclibc.bca
 KLEE: NOTE: Using model: /usr/local/lib/klee/runtime/libkleeRuntimePOSIX.bca
KLEE: output directory is "/home/.../obj-llvm/src/./klee-out-17"
 Using STP solver backend
 KLEE: WARNING ONCE: function "socket" has inline asm
 KLEE: WARNING ONCE: function "__libc_connect" has inline asm
 KLEE: WARNING ONCE: function "__libc_recvfrom" has inline asm
 KLEE: WARNING ONCE: function "__libc_sendto" has inline asm
 KLEE: WARNING: undefined reference to function: __ctype_b_loc
 KLEE: WARNING: undefined reference to function: __signbitl
 KLEE: WARNING: undefined reference to function: creat
 KLEE: WARNING: undefined reference to function: fdopendir
 KLEE: WARNING: undefined reference to function: freelocale
 KLEE: WARNING: undefined reference to function: iconv
 KLEE: WARNING: undefined reference to function: iconv_open
 KLEE: WARNING: undefined reference to function: klee_posix_prefer_cex
 KLEE: WARNING: undefined reference to function: newlocale
 KLEE: WARNING: undefined reference to function: strtod_l
 KLEE: WARNING: undefined reference to function: strtold_l
 KLEE: WARNING: executable has module level assembly (ignoring)
 KLEE: WARNING ONCE: calling external: syscall(16, 0, 21505, 99101760)
 KLEE: WARNING ONCE: calling __user_main with extra arguments.

 KLEE: WARNING ONCE: calling close_stdout with extra arguments.

 KLEE: WARNING ONCE: calling external: printf(98396064, 34508368)
Usage: ./echo [OPTION]... [STRING]...


 KLEE: WARNING ONCE: calling external: vprintf(98548384, 99346608)
echo (GNU coreutils) 6.10

 Echo the STRING(s) to standard output.

  -n             do not output the trailing newline
  -e             enable interpretation of backslash escapes
  -E             disable interpretation of backslash escapes (default)
      --help     display this help and exit
      --version  output version information and exit
 Copyright (C) 2008 Free Software Foundation, Inc.
 If -e is in effect, the following sequences are recognized:

  \0NNN   the character whose ASCII code is NNN (octal)
  \\     backslash
  \a     alert (BEL)
  \b     backspace

 License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
 This is free software: you are free to change and redistribute it.
 There is NO WARRANTY, to the extent permitted by law.

  \c     suppress trailing newline
  \f     form feed
  \n     new line
  \r     carriage return
  \t     horizontal tab
  \v     vertical tab

 NOTE: your shell may have its own version of echo, which usually supersedes
the version described here.  Please refer to your shell's documentation
for details about the options it supports.

 Report bugs to <bug-coreutils@gnu.org>.
Written by FIXME unknown.

 KLEE: done: total instructions = 69436
 KLEE: done: completed paths = 25
 KLEE: done: generated tests = 25
```

 We can get a short summary of KLEE’s internal statistics by running klee-stats on the output directory (remember, KLEE always makes a symlink called klee-last to the most recent output directory).

 ```
  src$ klee-stats klee-last
------------------------------------------------------------------------
|  Path   |  Instrs|  Time(s)|  ICov(%)|  BCov(%)|  ICount|  TSolver(%)|
------------------------------------------------------------------------
|klee-last|   69436|     0.81|     3.48|     3.27|  125170|       58.44|
------------------------------------------------------------------------
 ```
 
 Run again the application with --optimze enabled. This will cause KLEE to run the LLVM optimization passes on the bitcode module before executing it; in particular they will remove any dead code. 
 
 ```
 src$ klee --optimize --libc=uclibc --posix-runtime ./echo --sym-arg 3
 ... 
 KLEE: done: total instructions = 36543
 KLEE: done: completed paths = 25
 KLEE: done: generated tests = 25
 
 src$ klee-stats klee-last
 ------------------------------------------------------------------------
 |  Path   |  Instrs|  Time(s)|  ICov(%)|  BCov(%)|  ICount|  TSolver(%)|
 ------------------------------------------------------------------------
 |klee-last|   36543|     0.54|    29.89|    21.80|    8344|       80.99|
 ------------------------------------------------------------------------
 ```
 
5. Replaying KLEE generated test cases

 ```
 src$ ls klee-last
 assembly.ll       test000003.ktest  test000010.ktest  test000017.ktest  test000024.ktest
info              test000004.ktest  test000011.ktest  test000018.ktest  test000025.ktest
messages.txt      test000005.ktest  test000012.ktest  test000019.ktest  warnings.txt
run.istats        test000006.ktest  test000013.ktest  test000020.ktest
run.stats         test000007.ktest  test000014.ktest  test000021.ktest
test000001.ktest  test000008.ktest  test000015.ktest  test000022.ktest
test000002.ktest  test000009.ktest  test000016.ktest  test000023.ktest
```

 These files contain the actual values to use for the symbolic data in order to reproduce the path that KLEE followed. They also contain additional metadata generated by the POSIX runtime in order to track what the values correspond to and the version of the runtime. We can look at the individual contents of one file using ktest-tool:
 
 ```
 src$ ktest-tool klee-last/test000001.ktest
 ktest file : 'klee-last/test000001.ktest'
 args       : ['./echo', '--sym-arg', '3']
 num objects: 2
 object    0: name: 'arg0'
 object    0: size: 4
 object    0: data: '\x00\x00\x00\x00'
 object    1: name: 'model_version'
 object    1: size: 4
 object    1: data: '\x01\x00\x00\x00'
 ```
 
 **.ktest** files generally aren’t really meant to be looked at directly. For the POSIX runtime, we provide a tool **klee-replay** which can be used to read the .ktest file and invoke the native application, automatically passing it the data necessary to reproduce the path that KLEE followed.
To see how it works, go back to the directory where we built the native executables:

 ```
src$ cd ..
obj-llvm$ cd ..
coreutils-6.10$ cd obj-gcov
obj-gcov$ cd src
src$ ls -l echo
-rwxrwxr-x 1 eirini eirini 133146 Mai 27 20:57 echo
 ```
 
 To use the **klee-replay** tool, we just tell it the executable to run and the .ktest file to use. The program arguments, input files, etc. will all be constructed from the data in the **.ktest** file.
 
 ```
 src$ klee-replay ./echo ../../obj-llvm/src/klee-last/test000001.ktest
 klee-replay: TEST CASE: ../../obj-llvm/src/klee-last/test000001.ktest
 klee-replay: ARGS: "./echo" "" 

 klee-replay: EXIT STATUS: NORMAL (0 seconds)
 ```
 
 We can also use the **klee-replay** tool to run a set of test cases at once, one after the other.
 
 ```
 src$ klee-replay ./echo ../../obj-llvm/src/klee-last/*.ktest
 klee-replay: TEST CASE: ../../obj-llvm/src/klee-last/test000001.ktest
 klee-replay: ARGS: "./echo" "" 

 klee-replay: EXIT STATUS: NORMAL (0 seconds)

 ...
 
 klee-replay: TEST CASE: ../../obj-llvm/src/klee-last/test000007.ktest
 klee-replay: ARGS: "./echo" "--=" 
 --=
 klee-replay: EXIT STATUS: NORMAL (0 seconds)
 
 ...
 
 klee-replay: EXIT STATUS: NORMAL (0 seconds)

 klee-replay: TEST CASE: ../../obj-llvm/src/klee-last/test000025.ktest
 klee-replay: ARGS: "./echo" "--v" 
 echo (GNU coreutils) 6.10
 Copyright (C) 2008 Free Software Foundation, Inc.
 License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
 This is free software: you are free to change and redistribute it.
 There is NO WARRANTY, to the extent permitted by law.

 Written by FIXME unknown.
 klee-replay: EXIT STATUS: NORMAL (0 seconds)
 ```
 
 Before moving on to testing more complex applications, lets make sure we can get decent coverage of the simple echo.c. The problem before was that we weren’t making enough data symbolic, providing echo with two symbolic arguments should be plenty to cover the entire program. We can use the POSIX runtime --sym-args option to pass multiple options. Here are the steps, after switching back to the obj-llvm/src directory:
 
 ```
 src$ cd ../../obj-llvm/src/
 src$ klee --only-output-states-covering-new --optimize --libc=uclibc --posix-runtime ./echo --sym-args 0 2 4
 ...
 KLEE: done: total instructions = 7625251
 KLEE: done: completed paths = 10179
 KLEE: done: generated tests = 61
 ```
 
 The format of the **--sym-args** option actually specifies a minimum and a maximum number of arguments to pass and the length to use for each argument. In this case **--sym-args 0 2 4** says to pass between 0 and 2 arguments (inclusive), each with a maximum length of four characters. The final lines of the output show that even though KLEE explored over ten thousand paths through the code, it only needed to write 61 test cases.