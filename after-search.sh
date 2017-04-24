#!/bin/bash

#targ="bc_new_num"




#klee="/home/saahil/repos/after-search/Release+Asserts/bin/klee"
#llvm_obj="/home/saahil/vdc/bc-1.06/obj-llvm/KLEE-1.3/bc.x.bc"
#arg1="--sym-args 1 3 50"
#arg2="--sym-files 1 100"
#arg3="--sym-stdin 100"

#options=( "-posix-runtime" "-libc=uclibc" "-only-output-states-covering-new" "-disable-inlining" "-optimize" "-max-solver-time=15" "-max-time=420" "-watchdog" "-search=after-call" )
#command=( "$klee" "${options[@]}" "$targ" "$llvm_obj" "$arg1" "$arg2" "$arg3" )

#echo $llvm_obj

# execute the command
#"${command[@]}"


#uncoveredFuncs="['free_args', 'bc_init_numbers', 'bc_new_num', 'out_of_memory', 'def_label', 'assign', 'bc_copy_num', 'bc_free_num', 'auto_var', 'bc_init_num', 'bc_add', '_bc_do_add', '_bc_rm_leading_zeros', '_bc_do_compare', '_bc_do_sub', 'bc_compare', 'bc_divide', '_one_mult', 'bc_is_zero', 'bc_int2num', 'bc_is_neg', 'bc_modulo', 'bc_divmod', 'bc_multiply', '_bc_rec_mul', '_bc_shift_addsub', '_bc_simp_mul', 'bc_sub', 'new_sub_num', 'bc_out_num', 'bc_num2long', 'bc_out_long', 'bc_raise', 'rt_error', 'rt_warn', 'bc_sqrt', 'bc_is_near_zero', 'byte', 'decr_array', 'get_array_num', 'decr_var', 'fpop', 'fpush', 'incr_array', 'incr_var', 'load_array', 'load_var', 'out_schar', 'pop_vars', 'free_a_tree', 'process_params', 'copy_array', 'copy_tree', 'push_constant', 'store_array', 'long_val', 'nextarg', 'lookup', 'find_id', 'insert_id_rec', 'warn', 'yyerror', 'new_yy_file', 'show_bc_version', 'usage', 'arg_str', 'make_arg_str', 'call_str', 'check_params', 'limits', 'warranty', 'welcome', 'input', 'yy_fatal_error', 'yy_flex_realloc', 'yy_flex_alloc', 'yy_load_buffer_state', 'yywrap', 'yy_try_NUL_trans']
uncoveredFuncs=("free_args" "bc_init_numbers" "bc_new_num" "out_of_memory" "def_label" "assign" "bc_copy_num" "bc_free_num" "auto_var" "bc_init_num"
"bc_add" "_bc_do_add" "_bc_rm_leading_zeros" "_bc_do_compare" "_bc_do_sub" "bc_compare" "bc_divide" "_one_mult" "bc_is_zero" "bc_int2num"
"bc_is_neg" "bc_modulo" "bc_divmod" "bc_multiply" "_bc_rec_mul" "_bc_shift_addsub" "_bc_simp_mul" "bc_sub" "new_sub_num" "bc_out_num"
"bc_num2long" "bc_out_long" "bc_raise" "rt_error" "rt_warn" "bc_sqrt" "bc_is_near_zero" "byte" "decr_array" "get_array_num" "decr_var"
"fpop" "fpush" "incr_array" "incr_var" "load_array" "load_var" "out_schar" "pop_vars" "free_a_tree" "process_params" "copy_array"
"copy_tree" "push_constant" "store_array" "long_val" "nextarg" "lookup" "find_id" "insert_id_rec" "warn" "yyerror" "new_yy_file"
"show_bc_version" "usage" "arg_str" "make_arg_str" "call_str" "check_params" "limits" "warranty" "welcome" "input" "yy_fatal_error"
"yy_flex_realloc" "yy_flex_alloc" "yy_load_buffer_state" "yywrap" "yy_try_NUL_trans")

for targ in "${uncoveredFuncs[@]}"
do
    lecommand="/home/saahil/repos/after-search/Release+Asserts/bin/klee -posix-runtime  -libc=uclibc
		-only-output-states-covering-new -disable-inlining -optimize -max-solver-time=15
		-max-time=420 -watchdog -output-dir=klee-out-$targ -search=after-call -after-function=$targ /home/saahil/vdc/bc-1.06/obj-llvm/KLEE-bash/bc.x.bc
		--sym-args 1 3 50 --sym-files 1 100 --sym-stdin 100"
    echo $lecommand
    echo "Func: $targ"
    eval $lecommand
done

#lecommand="/home/saahil/repos/after-search/Release+Asserts/bin/klee -posix-runtime 
#-libc=uclibc -only-output-states-covering-new -disable-inlining -optimize -max-solver-time=15 
#-max-time=420 -watchdog -search=after-call -after-function=$targ /home/saahil/vdc/bc-1.06/obj-llvm/KLEE-1.3/bc.x.bc --sym-args 1 3 50 
#--sym-files 1 100 --sym-stdin 100"
#echo $lecommand
#eval $lecommand
