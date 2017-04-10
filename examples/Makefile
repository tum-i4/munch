CLANG ?= ~/build/llvm/Release/bin/clang
OPT   ?= ~/build/llvm/Release/bin/opt

callgraph: callgraph.png

callgraph.png: callgraph.dot
	dot $< -Tpng -o $@

callgraph.dot: tree.bc
	$(OPT) -dot-callgraph $< -disable-output

%.bc: %.c
	$(CLANG) -emit-llvm -O0 -g -c -o $@ $<

clean:
	@ rm -f callgraph.png callgraph.dot
	@ rm -rf klee-out-*
	@ rm -rf *.bc
