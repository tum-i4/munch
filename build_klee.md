# Build Klee  
#### on Ubuntu 14.04 LTS 64bit with LLVM 3.4

 1. First make sure you are all up to date:
 
 ```
 $ sudo apt-get update
 $ sudo apt-get upgrade
 ```
 
 2. Install dependencies:

 ```
 $ sudo apt-get install build-essential curl git bison flex bc libcap-dev git cmake libboost-all-dev libncurses5-dev python-minimal python-pip unzip ncurses-dev zlib1g-dev
 ```
  
 3. Set the following environment variables in a config file (like **.bashrc**):
 
 ```
export C_INCLUDE_PATH=/usr/include/x86_64-linux-gnu  
export CPLUS_INCLUDE_PATH=/usr/include/x86_64-linux-gnu
```

 4. Install LLVM 3.4. Add the following lines to your **/etc/apt/sources.list**:

 ```
deb http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.4 main  
deb-src http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.4 main
 ```

 Then add the repository key and install the 3.4 packages:
  
 ```
 $ wget -O - http://llvm.org/apt/llvm-snapshot.gpg.key|sudo apt-key add -  
 $ sudo apt-get update  
 $ sudo apt-get install clang-3.4 llvm-3.4 llvm-3.4-dev llvm-3.4-tools  
 ```

 Make sure llvm-config is in your path:
 
  ```
  $ sudo ln -sf /usr/bin/llvm-config-3.4 /usr/bin/llvm-config
  ```
   
 5. Build STP (Simple Theorem Prover):

 ```
 $ git clone https://github.com/stp/minisat.git
 $ cd minisat
 $ mkdir build
 $ cd build
 $ cmake -DCMAKE_INSTALL_PREFIX=/usr/ ../
 $ sudo make install
 $ cd ../../
 $ git clone https://github.com/stp/stp.git
 $ cd stp
 $ mkdir build && cd build
 $ cmake -G 'Unix Makefiles' $HOME/stp
 $ make
 $ sudo make install
 $ sudo ldconfig
 $ ulimit -s unlimited
 $ cd $HOME
 ``` 

6. Build KLEE-uclibc and the POSIX environment model:

 ```
 $ git clone --depth 1 --branch klee_0_9_29 https://github.com/klee/klee-uclibc.git
 $ cd klee-uclibc  
 $ ./configure --make-llvm-lib  
 $ make -j`nproc` 
 $ cd $HOME
 ```
<!--7. (Optional) Build libgtest:

 ```
$ curl -OL https://googletest.googlecode.com/files/gtest-1.7.0.zip  
$ unzip gtest-1.7.0.zip  
$ cd gtest-1.7.0  
$ cmake .  
$ make  
$ cd ..
 ```-->
 
8. Build KLEE:

 ```
 $ git clone https://github.com/klee/klee.git
 $ cd klee
 $ ./configure --with-stp=/full/path/to/stp/build/ --with-uclibc=/full/path/to/klee-uclibc/ --enable-posix-runtime 
 $ make ENABLE_OPTIMIZED=1
 $ sudo make install
 $ make test
 $ cd $HOME
 ```
 
 Add also the following line to your **.bashrc** file:
 
 ```
 export PATH=$PATH:/full/path/to/klee/Release+Asserts/bin
 ```
 
9. Check the [Tutorials](http://klee.github.io/tutorials/) page to try KLEE.

 Testing a small function (Tutorial 1):
 
 ```
 $ cd $HOME/klee/examples/get_sign
 $ clang-3.4 -emit-llvm -c -g get_sign.c
 $ klee get_sign.bc
 ```
 
 You should see the following output:
 
 ```
 KLEE: output directory is "/full/path/to/klee/examples/get_sign/klee-out-0"
 Using STP solver backend
 
 KLEE: done: total instructions = 31
 KLEE: done: completed paths = 3
 KLEE: done: generated tests = 3
 ```
 
 You might need to add the following (in case you see errors while running the example) to your **.bashrc** profile :

 ```
 export C_INCLUDE_PATH=/full/path/to/klee/include/:$C_INCLUDE_PATH
 export LD_LIBRARY_PATH=/full/path/to/klee/Release+Asserts/lib/:/usr/lib/x86_64-linux-gnu/:/full/path/to/stp/build/lib/:$LD_LIBRARY_PATH
 export LIBRARY_PATH=$LD_LIBRARY_PATH
 ```
 
