# Running GNU Coreutils with AFL

#### on Ubuntu 14.04 LTS 64bit with LLVM 3.4

1. Download and unpack [afl](http://lcamtuf.coredump.cx/afl/). Here we use the version 2.13b. You can then build it:

 ```
 afl-2.13b$ make
 afl-2.13b$ sudo make install 
 ```
 
2. Fast LLVM-based instrumentation for afl-fuzz

 In order to leverage this mechanism, you need to have **clang** installed on your system and make sure that the **llvm-config** tool is in your path. You will need to make also the following changes (to fix the errors while compiling):
 
 * add *CXX += -std=c++11* to the Makefile to remove all the warnings
 * modify the *llvm-afl-pass.c.so* file by replacing in the *GlobalVariable \*AFLPrevLoc* the argument *GlobalValue::GeneralDynamicTLSModel* with *GlobalVariable::GeneralDynamicTLSModel*.

  Then type:

  ```
  afl-2.13b$ cd llvm_mode
  llvm_mode$ make
  llvm_mode$ cd ..
  afl-2.13b$ sudo make install
  ``` 

  Now we can compile the Coreutils sources with the **afl-gcc**
 
  ```
  coreutils-6.10$ mkdir obj-afl
  coreutils-6.10$ cd obj-afl
  obj-afl$ CC=afl-gcc ../configure 
  obj-afl$ make clean all
  ```

  If all went well, we should now see in **src/** folder the binaries of Coreutils. 

3. Fuzzing binaries

 Give a directory with initial test cases, a separate place to
store its findings, plus a path to the binary to test.

 Try with **cat**
 
 ```
 obj-afl/coreutils_testcases$ afl-fuzz -i cat_tests/ -o cat_results ../src/cat @@
 afl-fuzz 2.13b by <lcamtuf@google.com>
 [+] You have 1 CPU cores and 5 runnable tasks (utilization: 500%).
 [*] Checking core_pattern...
 [*] Setting up output directories...
 [*] Scanning 'cat_tests/'...
 [+] No auto-generated dictionary tokens to reuse.
 [*] Creating hard links for all input files...
 [*] Validating target binary...
 [*] Attempting dry run with 'id:000000,orig:test1.txt'...
 [*] Spinning up the fork server...
 [+] All right - fork server is up.
    len = 700000, map size = 52, exec speed = 858 us
 [*] Attempting dry run with 'id:000001,orig:test2.txt'...
    len = 283545, map size = 52, exec speed = 1689 us
 [+] All test cases processed.

 [!] WARNING: Some test cases are huge (683 kB) - see /usr/local/share/doc/afl/perf_tips.txt!
 [+] Here are some useful stats:

    Test case count : 1 favored, 0 variable, 2 total
       Bitmap range : 52 to 52 bits (average: 52.00 bits)
        Exec timing : 858 to 1689 us (average: 1273 us)

 [*] No -t option specified, so I'll use exec timeout of 20 ms.
 [+] All set and ready to roll!
 ```
 
 After ~30 min:
 
 ```
                         american fuzzy lop 2.13b (cat)

 ┌─ process timing ─────────────────────────────────────┬─ overall results ─────┐
 │        run time : 0 days, 0 hrs, 35 min, 15 sec      │  cycles done : 0      │
 │   last new path : 0 days, 0 hrs, 10 min, 45 sec      │  total paths : 3      │
 │ last uniq crash : none seen yet                      │ uniq crashes : 0      │
 │  last uniq hang : 0 days, 0 hrs, 21 min, 0 sec       │   uniq hangs : 3      │
 ├─ cycle progress ────────────────────┬─ map coverage ─┴───────────────────────┤
 │  now processing : 2 (66.67%)        │    map density : 52 (0.08%)            │
 │ paths timed out : 0 (0.00%)         │ count coverage : 1.23 bits/tuple       │
 ├─ stage progress ────────────────────┼─ findings in depth ────────────────────┤
 │  now trying : bitflip 2/1           │ favored paths : 1 (33.33%)             │
 │ stage execs : 380k/1.02M (37.43%)   │  new edges on : 1 (33.33%)             │
 │ total execs : 4.69M                 │ total crashes : 0 (0 unique)           │
 │  exec speed : 2035/sec              │   total hangs : 17 (3 unique)          │
 ├─ fuzzing strategy yields ───────────┴───────────────┬─ path geometry ────────┤
 │   bit flips : 0/2.07M, 0/1.05M, 0/1.05M             │    levels : 2          │
 │  byte flips : 0/131k, 0/9, 0/9                      │   pending : 2          │
 │ arithmetics : 0/504, 0/337, 0/171                   │  pend fav : 1          │
 │  known ints : 0/42, 0/198, 0/326                    │ own finds : 1          │
 │  dictionary : 0/0, 0/0, 0/0                         │  imported : n/a        │
 │       havoc : 1/10.0k, 0/0                          │  variable : 0          │
 │        trim : 37.69%/3001, 99.99%                   ├────────────────────────┘
  ────────────────────────────────────────────────────┘             [cpu:312%]

 ```
 After ~1h:

 ```
                         american fuzzy lop 2.13b (cat)

 ┌─ process timing ─────────────────────────────────────┬─ overall results ─────┐
 │        run time : 0 days, 1 hrs, 0 min, 28 sec       │  cycles done : 0      │
 │   last new path : 0 days, 0 hrs, 9 min, 24 sec       │  total paths : 4      │
 │ last uniq crash : none seen yet                      │ uniq crashes : 0      │
 │  last uniq hang : 0 days, 0 hrs, 58 min, 55 sec      │   uniq hangs : 3      │
 ├─ cycle progress ────────────────────┬─ map coverage ─┴───────────────────────┤
 │  now processing : 3 (75.00%)        │    map density : 52 (0.08%)            │
 │ paths timed out : 0 (0.00%)         │ count coverage : 1.38 bits/tuple       │
 ├─ stage progress ────────────────────┼─ findings in depth ────────────────────┤
 │  now trying : bitflip 4/1           │ favored paths : 1 (25.00%)             │
 │ stage execs : 324k/524k (61.76%)    │  new edges on : 1 (25.00%)             │
 │ total execs : 7.86M                 │ total crashes : 0 (0 unique)           │
 │  exec speed : 2322/sec              │   total hangs : 46 (3 unique)          │
 ├─ fuzzing strategy yields ───────────┴───────────────┬─ path geometry ────────┤
 │   bit flips : 0/2.59M, 0/2.59M, 0/2.07M             │    levels : 3          │
 │  byte flips : 0/258k, 0/19, 0/19                    │   pending : 2          │
 │ arithmetics : 0/1064, 0/674, 0/342                  │  pend fav : 1          │
 │  known ints : 0/91, 0/424, 0/696                    │ own finds : 2          │
 │  dictionary : 0/0, 0/0, 0/0                         │  imported : n/a        │
 │       havoc : 2/20.0k, 0/0                          │  variable : 0          │
 │        trim : 40.19%/4029, 99.99%                   ├────────────────────────┘
 ─────────────────────────────────────────────────────┘             [cpu:323%]

 ```
  
 Try with **md5sum**
 
 ```
 obj-afl/coreutils_testcases$ afl-fuzz -i md5sum_tests/ -o md5sum_results ../src/md5sum @@
afl-fuzz 2.13b by <lcamtuf@google.com>
 [+] You have 1 CPU cores and 5 runnable tasks (utilization: 500%).
 [*] Checking core_pattern...
 [*] Setting up output directories...
 [+] Output directory exists but deemed OK to reuse.
 [*] Deleting old session data...
 [+] Output dir cleanup successful.
 [*] Scanning 'md5sum_tests/'...
 [+] No auto-generated dictionary tokens to reuse.
 [*] Creating hard links for all input files...
 [*] Validating target binary...
 [*] Attempting dry run with 'id:000000,orig:mkdir.o'...
 [*] Spinning up the fork server...
 [+] All right - fork server is up.
    len = 12460, map size = 81, exec speed = 312 us
 [*] Attempting dry run with 'id:000001,orig:test1.txt'...
    len = 700000, map size = 81, exec speed = 4388 us
 [+] All test cases processed.

 [!] WARNING: Some test cases are huge (683 kB) - see /usr/local/share/doc/afl/perf_tips.txt!
 [+] Here are some useful stats:

    Test case count : 1 favored, 0 variable, 2 total
       Bitmap range : 81 to 81 bits (average: 81.00 bits)
        Exec timing : 312 to 4388 us (average: 2350 us)

 [*] No -t option specified, so I'll use exec timeout of 20 ms. 
 ```
 
 After ~30 min
 
 ```
                        american fuzzy lop 2.13b (md5sum)

 ┌─ process timing ─────────────────────────────────────┬─ overall results ─────┐
 │        run time : 0 days, 0 hrs, 30 min, 6 sec       │  cycles done : 1      │
 │   last new path : 0 days, 0 hrs, 24 min, 50 sec      │  total paths : 7      │
 │ last uniq crash : none seen yet                      │ uniq crashes : 0      │
 │  last uniq hang : 0 days, 0 hrs, 29 min, 33 sec      │   uniq hangs : 3      │
 ├─ cycle progress ────────────────────┬─ map coverage ─┴───────────────────────┤
 │  now processing : 1* (14.29%)       │    map density : 87 (0.13%)            │
 │ paths timed out : 0 (0.00%)         │ count coverage : 1.11 bits/tuple       │
 ├─ stage progress ────────────────────┼─ findings in depth ────────────────────┤
 │  now trying : bitflip 1/1           │ favored paths : 4 (57.14%)             │
 │ stage execs : 449k/4.23M (10.61%)   │  new edges on : 4 (57.14%)             │
 │ total execs : 1.98M                 │ total crashes : 0 (0 unique)           │
 │  exec speed : 418.3/sec             │   total hangs : 94 (3 unique)          │
 ├─ fuzzing strategy yields ───────────┴───────────────┬─ path geometry ────────┤
 │   bit flips : 0/427k, 0/427k, 0/427k                │    levels : 3          │
 │  byte flips : 0/53.5k, 0/73, 0/73                   │   pending : 2          │
 │ arithmetics : 0/4078, 0/3199, 0/2610                │  pend fav : 0          │
 │  known ints : 0/236, 0/1103, 0/1916                 │ own finds : 5          │
 │  dictionary : 0/0, 0/0, 0/0                         │  imported : n/a        │
 │       havoc : 5/172k, 0/0                           │  variable : 0          │
 │        trim : 23.11%/7655, 99.85%                   ├────────────────────────┘
 ─────────────────────────────────────────────────────┘             [cpu:307%]

 ```

 After ~1h
 
 ```
                       american fuzzy lop 2.13b (md5sum)

 ┌─ process timing ─────────────────────────────────────┬─ overall results ─────┐
 │        run time : 0 days, 1 hrs, 0 min, 12 sec       │  cycles done : 1      │
 │   last new path : 0 days, 0 hrs, 57 min, 43 sec      │  total paths : 6      │
 │ last uniq crash : none seen yet                      │ uniq crashes : 0      │
 │  last uniq hang : 0 days, 0 hrs, 51 min, 4 sec       │   uniq hangs : 8      │
 ├─ cycle progress ────────────────────┬─ map coverage ─┴───────────────────────┤
 │  now processing : 1* (16.67%)       │    map density : 87 (0.13%)            │
 │ paths timed out : 0 (0.00%)         │ count coverage : 1.07 bits/tuple       │
 ├─ stage progress ────────────────────┼─ findings in depth ────────────────────┤
 │  now trying : bitflip 1/1           │ favored paths : 4 (66.67%)             │
 │ stage execs : 1.39M/4.23M (32.74%)  │  new edges on : 4 (66.67%)             │
 │ total execs : 2.80M                 │ total crashes : 0 (0 unique)           │
 │  exec speed : 380.0/sec             │   total hangs : 135 (8 unique)         │
 ├─ fuzzing strategy yields ───────────┴───────────────┬─ path geometry ────────┤
 │   bit flips : 0/394k, 0/394k, 0/394k                │    levels : 2          │
 │  byte flips : 0/49.3k, 0/86, 0/92                   │   pending : 2          │
 │ arithmetics : 0/4637, 0/3022, 0/2149                │  pend fav : 0          │
 │  known ints : 0/310, 0/1599, 0/2984                 │ own finds : 4          │
 │  dictionary : 0/0, 0/0, 0/0                         │  imported : n/a        │
 │       havoc : 4/157k, 0/0                           │  variable : 0          │
 │        trim : 22.83%/7134, 99.82%                   ├────────────────────────┘
 ──────────────────────────────────────────────────────┘             [cpu:310%]

 ```
 
 After ~8h
 
 ```
                        american fuzzy lop 2.13b (md5sum)

 ┌─ process timing ─────────────────────────────────────┬─ overall results ─────┐
 │        run time : 0 days, 8 hrs, 2 min, 29 sec       │  cycles done : 1      │
 │   last new path : 0 days, 7 hrs, 49 min, 10 sec      │  total paths : 10     │
 │  last uniq crash : none seen yet                      │ uniq crashes : 0     │
 │  last uniq hang : 0 days, 0 hrs, 33 min, 59 sec      │   uniq hangs : 5      │
 ├─ cycle progress ────────────────────┬─ map coverage ─┴───────────────────────┤
 │  now processing : 1* (10.00%)       │    map density : 88 (0.13%)            │
 │ paths timed out : 0 (0.00%)         │ count coverage : 1.20 bits/tuple       │
 ├─ stage progress ────────────────────┼─ findings in depth ────────────────────┤
 │  now trying : bitflip 4/1           │ favored paths : 4 (40.00%)             │
 │  stage execs : 521k/4.23M (12.33%)   │  new edges on : 5 (50.00%)            │
 │ total execs : 10.9M                 │ total crashes : 0 (0 unique)           │
 │  exec speed : 427.8/sec             │   total hangs : 183 (5 unique)         │
 ├─ fuzzing strategy yields ───────────┴───────────────┬─ path geometry ────────┤
 │   bit flips : 0/4.76M, 0/4.76M, 0/527k              │    levels : 5          │
 │  byte flips : 0/65.9k, 0/167, 0/163                 │   pending : 1          │
 │ arithmetics : 0/9439, 0/5901, 0/4081                │  pend fav : 0          │
 │  known ints : 0/648, 0/3074, 0/5187                 │ own finds : 8          │
 │  dictionary : 0/0, 0/0, 0/0                         │  imported : n/a        │
 │       havoc : 8/276k, 0/0                           │  variable : 0          │
 │        trim : 23.52%/10.3k, 99.71%                  ├────────────────────────┘
 ─────────────────────────────────────────────────────┘             [cpu:308%]
 ```
 
 




