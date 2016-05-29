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
 
 If all went well, you should now have in **src/** folder LLVM bitcode versions of Coreutils!
 
 