# AFL Fuzzing Code Coverage (afl-cov)

### for GNU coreutils

**afl-cov** uses test case files produced by the [AFL fuzzer](http://lcamtuf.coredump.cx/afl/) afl-fuzz to generate gcov code coverage results for a targeted binary.

#### Prerequisites
* afl-fuzz
* python
* gcov, lcov, genhtml

#### Installation

```
git clone https://github.com/mrash/afl-cov.git
sudo ln -s path/to/afl-cov /usr/bin/afl-cov
```

#### Workflow

* Copy the project sources to a new directory, **/path/to/project-gcov/**. This directory should contain the project binaries compiled for gcov profiling support (gcc -fprofile-arcs -ftest-coverage).
* Start up afl-cov in **--live** mode before also starting the afl-fuzz fuzzing cycle. The command line arguments to **afl-cov** must specify the path to the output directory used by afl-fuzz, and the command to execute along with associated arguments. If there is already an existing directory of AFL fuzzing results, then just omit the **--live** argument to process the existing results.

Try with **cat** (without **--live** mode, so the existing results of afl-fuzz for cat will be processed).

* `/path/to/afl-fuzz-output/` is is the output directory of afl-fuzz.

* The `AFL_FILE` string above refers to the test case file that AFL will build in the **queue/** directory under `/path/to/afl-fuzz-output`.  afl-cov will automatically substitute it with each AFL queue/id:NNNNNN* in succession as it builds the code coverage reports.
* The example below handles the case where a file is read from the **filesystem**.

 ```
 $ cd /path/to/project-gcov/
 project-gcov$ afl-cov -d ../obj-afl/coreutils_testcases/cat_results_full/ -e "./src/./cat AFL_FILE" -c . -O
    
 *** Imported 12 new test cases from: ../obj-afl/coreutils_testcases/cat_results_full//queue

    [+] AFL test case: id:000000,orig:test1.txt (0 / 12), cycle: 0
        lines......: 0.7% (85 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    
    Coverage diff (init) id:000000,orig:test1.txt
    diff (init) -> id:000000,orig:test1.txt
    New src file: /home/eirini/coreutils-6.10/lib/safe-read.c
      New 'function' coverage: safe_read()
      New 'function' coverage: safe_write()
      New 'line' coverage: 56
      New 'line' coverage: 66
      New 'line' coverage: 68
      New 'line' coverage: 69
    New src file: /home/eirini/coreutils-6.10/src/cat.c
      New 'function' coverage: main()
      New 'function' coverage: simple_cat()
      New 'line' coverage: 156
      New 'line' coverage: 173
      New 'line' coverage: 174
      New 'line' coverage: 182
      New 'line' coverage: 183
      New 'line' coverage: 189
      New 'line' coverage: 190
      New 'line' coverage: 193
      New 'line' coverage: 506
      New 'line' coverage: 514
      New 'line' coverage: 522
      New 'line' coverage: 535
      New 'line' coverage: 538
      New 'line' coverage: 543
      New 'line' coverage: 544
      New 'line' coverage: 545
      New 'line' coverage: 546
      New 'line' coverage: 547
      New 'line' coverage: 548
      New 'line' coverage: 549
      New 'line' coverage: 566
      New 'line' coverage: 567
      New 'line' coverage: 575
      New 'line' coverage: 579
      New 'line' coverage: 640
      New 'line' coverage: 643
      New 'line' coverage: 650
      New 'line' coverage: 652
      New 'line' coverage: 653
      New 'line' coverage: 664
      New 'line' coverage: 666
      New 'line' coverage: 675
      New 'line' coverage: 676
      New 'line' coverage: 680
      New 'line' coverage: 681
      New 'line' coverage: 683
      New 'line' coverage: 692
      New 'line' coverage: 693
      New 'line' coverage: 701
      New 'line' coverage: 707
      New 'line' coverage: 714
      New 'line' coverage: 715
      New 'line' coverage: 726
      New 'line' coverage: 727
      New 'line' coverage: 729
      New 'line' coverage: 730
      New 'line' coverage: 732
      New 'line' coverage: 771
      New 'line' coverage: 774
      New 'line' coverage: 780
      New 'line' coverage: 782
      New 'line' coverage: 785
    New src file: /home/eirini/coreutils-6.10/lib/close-stream.c
      New 'function' coverage: close_stream()
      New 'line' coverage: 53
      New 'line' coverage: 55
      New 'line' coverage: 56
      New 'line' coverage: 57
      New 'line' coverage: 67
      New 'line' coverage: 74
    New src file: /home/eirini/coreutils-6.10/lib/xmalloc.c
      New 'function' coverage: xmalloc()
      New 'line' coverage: 47
      New 'line' coverage: 49
      New 'line' coverage: 50
      New 'line' coverage: 52
    New src file: /home/eirini/coreutils-6.10/lib/closeout.c
      New 'function' coverage: close_stdout()
      New 'line' coverage: 69
      New 'line' coverage: 71
      New 'line' coverage: 83
      New 'line' coverage: 85
    New src file: /home/eirini/coreutils-6.10/lib/full-write.c
      New 'function' coverage: full_write()
      New 'line' coverage: 59
      New 'line' coverage: 61
      New 'line' coverage: 62
      New 'line' coverage: 64
      New 'line' coverage: 66
      New 'line' coverage: 67
      New 'line' coverage: 69
      New 'line' coverage: 74
      New 'line' coverage: 75
      New 'line' coverage: 76
      New 'line' coverage: 79
    New src file: /home/eirini/coreutils-6.10/src/system.h
      New 'function' coverage: ptr_align()
      New 'line' coverage: 545
      New 'line' coverage: 547
      New 'line' coverage: 548
      New 'line' coverage: 549
    
    

 ++++++ BEGIN - first exec output for CMD: ./src/./cat ../obj-afl/coreutils_testcases/cat_results_full//queue/id:000000,orig:test1.txt
        The Project Gutenberg EBook of The Adventures of Sherlock Holmes
        by Sir Arthur Conan Doyle
        (#15 in our series by Sir Arthur Conan Doyle)
        
        Copyright laws are changing all over the world. Be sure to check the
        copyright laws for your country before downloading or redistributing
        this or any other Project Gutenberg eBook.
        
        This header should be the first thing seen when viewing this Project
        Gutenberg file.  Please do not remove it.  Do not change or edit the
        header without written permission.
        ...
        
 ++++++ END

    [+] AFL test case: id:000001,orig:test2.txt (1 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    
    Coverage diff id:000000,orig:test1.txt id:000001,orig:test2.txt
    diff id:000000,orig:test1.txt -> id:000001,orig:test2.txt
    Src file: /home/eirini/coreutils-6.10/src/cat.c
      New 'line' coverage: 657
    
    [+] AFL test case: id:000002,src:000001,op:havoc,rep:128 (2 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000003,src:000002,op:havoc,rep:128 (3 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000004,src:000003,op:havoc,rep:32 (4 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000005,src:000004,op:havoc,rep:8 (5 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000006,src:000005,op:havoc,rep:64 (6 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000007,src:000006,op:havoc,rep:128 (7 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000008,src:000007,op:havoc,rep:64 (8 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000009,src:000008,op:havoc,rep:8 (9 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000010,src:000009,op:havoc,rep:32 (10 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] AFL test case: id:000011,src:000005+000009,op:splice,rep:128 (11 / 12), cycle: 0
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
    [+] Processed 12 / 12 test cases.

    [+] Final zero coverage report: ../obj-afl/coreutils_testcases/cat_results_full//cov/zero-cov
    [+] Final positive coverage report: ../obj-afl/coreutils_testcases/cat_results_full//cov/pos-cov
        lines......: 0.7% (86 of 12014 lines)
        functions..: 1.4% (9 of 629 functions)
        Non-zero exit status '2' for CMD: /usr/bin/genhtml --output-directory ../obj-afl/coreutils_testcases/cat_results_full//cov/web ../obj-afl/coreutils_testcases/cat_results_full//cov/lcov/trace.lcov_info_final
    [+] Final lcov web report: ../obj-afl/coreutils_testcases/cat_results_full//cov/web/index.html        
 ```

* For the other style where the AFL fuzzing cycle is fuzzing the targeted binary via **stdin**, see the example below.
* Try with **echo:**

 ```
 $ cd /path/to/project-gcov/
 $ afl-cov -d ../obj-afl/test_afl/sync_dir/yes -e "./src/./echo < AFL_FILE" -c . --enable-branch-coverage --coverage-include-lines  
 
  *** Imported 186 new test cases from: ../obj-afl/test_afl/sync_dir/echo/echo4/queue

    [+] AFL test case: id:000000,orig:test1.txt (0 / 186), cycle: 0
        lines......: 0.2% (78 of 36764 lines)
        functions..: 0.3% (5 of 1727 functions)
        branches...: 3.1% (36 of 1169 branches)

    Coverage diff (init) id:000000,orig:test1.txt
    diff (init) -> id:000000,orig:test1.txt
    New src file: /media/vdc/coreutils-6.10/lib/closeout.c
      New 'function' coverage: close_stdout()
      New 'line' coverage: 69
      New 'line' coverage: 71
      New 'line' coverage: 83
      New 'line' coverage: 85
    New src file: /media/vdc/coreutils-6.10/lib/close-stream.c
      New 'function' coverage: close_stream()
      New 'line' coverage: 53
      New 'line' coverage: 55
      New 'line' coverage: 56
      New 'line' coverage: 57
      New 'line' coverage: 67
      New 'line' coverage: 74
    New src file: /media/vdc/coreutils-6.10/src/echo.c
      New 'function' coverage: initialize_main()
      New 'function' coverage: main()
      New 'line' coverage: 124
      New 'line' coverage: 129
      New 'line' coverage: 131
      New 'line' coverage: 132
      New 'line' coverage: 133
      New 'line' coverage: 134
      
      ...
      
        New src file: /media/vdc/coreutils-6.10/lib/long-options.c
      New 'function' coverage: parse_long_options()
      New 'line' coverage: 44
      New 'line' coverage: 55
      New 'line' coverage: 58
      New 'line' coverage: 60
      New 'line' coverage: 83
      New 'line' coverage: 87
      New 'line' coverage: 88



  ++++++ BEGIN - first exec output for CMD: ./src/./echo < ../obj-afl/test_afl/sync_dir/echo/echo4/queue/id:000000,orig:test1.txt
        ---
        ./src/./echo
        ---
        This
        ---
        is 
        ---
        test1
        ---
        for
        ---
        echo.
        This is test1 for echo.
     ++++++ END

    [+] AFL test case: id:000001,orig:test2.txt (1 / 186), cycle: 0
        lines......: 0.2% (78 of 36764 lines)
        functions..: 0.3% (5 of 1727 functions)
        branches...: 3.1% (36 of 1169 branches)
    [+] AFL test case: id:000002,orig:test3.txt (2 / 186), cycle: 0
        lines......: 0.2% (78 of 36764 lines)
        functions..: 0.3% (5 of 1727 functions)
        branches...: 3.1% (36 of 1169 branches)
    [+] AFL test case: id:000003,orig:test4.txt (3 / 186), cycle: 0
        lines......: 0.2% (78 of 36764 lines)
        functions..: 0.3% (5 of 1727 functions)
        branches...: 3.2% (37 of 1169 branches)
    [+] AFL test case: id:000004,orig:test5.txt (4 / 186), cycle: 0
        lines......: 0.2% (78 of 36764 lines)
     
     ...
    ```

