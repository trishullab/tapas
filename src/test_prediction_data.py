
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from gen.production_instance import InstanceHandlers, match_instance

from lib import generic_tree

from lib.python_ast_from_generic_ast import from_generic_ast
from lib.python_ast_serialize import serialize_Module
from lib import python_instance
from lib.file import write_res, write_append_res, write_res_gen, write_append_res_gen

from lib.production_instance import instance
from lib import production_instance as prod_inst



import re

# prediction_data = r"[[grammar,Module,Module],[grammar,statements,SingleStmt],[grammar,stmt,DecFunctionDef],[grammar,decorators,NoDec],[grammar,function_def,FunctionDef],[vocab,identifier,check_RShift],[grammar,parameters,ParamsB],[grammar,parameters_b,SingleParam],[grammar,Param,Param],[vocab,identifier,str1],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,return_type,NoReturnType],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,string1],[grammar,expr,False_],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,char],[grammar,expr,False_],[grammar,statements,ConsStmt],[grammar,stmt,For],[grammar,expr,Name],[vocab,identifier,x],[grammar,expr,Name],[vocab,identifier,str1],[grammar,statements,SingleStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,char],[grammar,expr,List],[grammar,comma_exprs,SingleExpr],[grammar,expr,CallArgs],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,vowels],[vocab,identifier,search],[grammar,arguments,ConsArg],[grammar,expr,Name],[vocab,identifier,temp],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,list],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,e],[grammar,expr,Call],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,c_num_test_str],[vocab,statements,ConsStmt],[grammar,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,res],[grammar,expr,Call],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,temp],[vocab,identifier,split],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,res_num],[grammar,expr,Tuple],[grammar,comma_exprs,ConsExpr],[grammar,expr,Name],[vocab,identifier,K1x],[grammar,comma_exprs,SingleExpr],[grammar,expr,Name],[vocab,identifier,b],[grammar,comma_exprs,SingleExpr],[grammar,expr,Name],[vocab,identifier,temp],[grammar,statements,SingleStmt],[grammar,stmt,If],[grammar,expr,CallArgs],[grammar,expr,Name],[vocab,identifier,isinstance],[grammar,arguments,ConsArg],[grammar,expr,Name],[vocab,identifier,temp],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,match],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,Name],[vocab,identifier,res],[grammar,conditions,NoCond]]")
# prediction_data = r"[[grammar,Module,Module],[grammar,statements,SingleStmt],[grammar,stmt,DecFunctionDef],[grammar,decorators,NoDec],[grammar,function_def,FunctionDef],[vocab,identifier,sum_path],[grammar,parameters,ParamsB],[grammar,parameters_b,ConsParam],[grammar,Param,Param],[vocab,identifier,A],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,parameters_b,SingleParam],[grammar,Param,Param],[vocab,identifier,n],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,return_type,NoReturnType],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,BinOp],[grammar,expr,BinOp],[grammar,expr,Integer],[vocab,integer,2],[grammar,operator,Mult],[grammar,expr,CallArgs],[grammar,expr,Name],[vocab,identifier,isinstance],[grammar,arguments,ConsArg],[grammar,expr,Name],[vocab,identifier,n],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,m],[grammar,operator,Add],[grammar,expr,Integer],[vocab,integer,1]]"
prediction_data = r"[[grammar,Module,Module],[grammar,statements,ConsStmt],[grammar,stmt,Import],[grammar,sequence_ImportName,SingleImportName],[grammar,ImportName,ImportName],[vocab,module_identifier,re],[grammar,alias,NoAlias],[grammar,statements,SingleStmt],[grammar,stmt,DecFunctionDef],[grammar,decorators,NoDec],[grammar,function_def,FunctionDef],[vocab,identifier,freq_count],[grammar,parameters,ParamsB],[grammar,parameters_b,ParamsB],[grammar,parameters_b,SingleParam],[grammar,Param,Param],[vocab,identifier,text],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,return_type,NoReturnType],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,word],[grammar,expr,CallArgs],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,re],[vocab,identifier,arguments,ConsArg],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[grammar,string,'\w+'],[grammar,arguments,ConsArg],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[vocab,string,''],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,text],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,result],[grammar,expr,CallArgs],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,text],[vocab,identifier,compile],[grammar,arguments,SingleArg],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[vocab,string,'1'],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,Name],[vocab,identifier,result]]"
# prediction_data = r"[[grammar,Module,Module],[grammar,statements,ConsStmt],[grammar,stmt,Import],[grammar,sequence_ImportName,SingleImportName],[grammar,ImportName,ImportName],[vocab,module_identifier,re],[grammar,alias,NoAlias],[grammar,statements,SingleStmt],[grammar,stmt,DecFunctionDef],[grammar,decorators,NoDec],[grammar,function_def,FunctionDef],[vocab,identifier,text_match_word],[grammar,parameters,ParamsB],[grammar,parameters_b,SingleParam],[grammar,Param,Param],[vocab,identifier,text1],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,return_type,NoReturnType],[grammar,statements,ConsStmt],[grammar,stmt,Assign],[grammar,target_exprs,SingleTargetExpr],[grammar,expr,Name],[vocab,identifier,patterns],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[vocab,string,'ab{3$'],[grammar,statements,SingleStmt],[grammar,stmt,If],[grammar,expr,CallArgs],[grammar,expr,Attribute],[grammar,expr,Name],[vocab,identifier,re],[vocab,identifier,search],[grammar,arguments,ConsArg],[grammar,expr,Name],[vocab,identifier,patterns],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,string],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[vocab,string,'Found a match!'],[grammar,conditions,ElseCond],[grammar,ElseBlock,ElseBlock],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,ConcatString],[grammar,sequence_string,SingleStr],[vocab,string,'Not matched!']]"
# prediction_data = r"[[grammar,Module,Module],[grammar,statements,SingleStmt],[grammar,stmt,DecFunctionDef],[grammar,decorators,NoDec],[grammar,function_def,FunctionDef],[vocab,identifier,find_Even],[grammar,parameters,ParamsB],[grammar,parameters_b,ConsParam],[grammar,Param,Param],[vocab,identifier,arr],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,parameters_b,SingleParam],[grammar,Param,Param],[vocab,identifier,n],[grammar,param_type,NoParamType],[grammar,param_default,NoParamDefault],[grammar,return_type,NoReturnType],[grammar,statements,ConsStmt],[grammar,stmt,For],[grammar,expr,Name],[vocab,identifier,i],[grammar,expr,CallArgs],[grammar,expr,Name],[vocab,identifier,range],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,n],[grammar,statements,SingleStmt],[grammar,stmt,For],[grammar,expr,Name],[vocab,identifier,j],[grammar,expr,CallArgs],[grammar,expr,Name],[vocab,identifier,range],[grammar,arguments,ConsArg],[grammar,expr,Integer],[vocab,integer,0],[grammar,arguments,SingleArg],[grammar,expr,Name],[vocab,identifier,n],[grammar,statements,SingleStmt],[grammar,stmt,If],[grammar,expr,Compare],[grammar,expr,Subscript],[grammar,expr,Name],[vocab,identifier,arr],[grammar,expr,BinOp],[grammar,expr,Name],[vocab,identifier,i],[grammar,operator,Sub],[grammar,expr,Integer],[vocab,integer,1],[grammar,comparisons,SingleCompareRight],[grammar,CompareRight,CompareRight],[grammar,cmpop,Gt],[grammar,expr,Subscript],[grammar,expr,Name],[vocab,identifier,arr],[grammar,expr,Name],[vocab,identifier,j],[grammar,statements,SingleStmt],[grammar,stmt,AugAssign],[grammar,expr,Name],[vocab,identifier,count],[grammar,operator,Add],[grammar,expr,Integer],[vocab,integer,1],[grammar,conditions,NoCond],[grammar,statements,SingleStmt],[grammar,stmt,ReturnSomething],[grammar,expr,Name],[vocab,identifier,count]]"



prediction_instances : list[instance] = [
    (
        prod_inst.make_Grammar(triple[1], triple[2])
        if triple[0] == "grammar" else

        prod_inst.make_Vocab(triple[1], triple[2])

    )
    for match in re.findall(r"\[[^,]+,[^,]+,[^,]+\]", prediction_data[1:-1])
    for triple in [match[1:-1].split(",")]
]


# print(f"-------------------------")
# print(f"generic tree:")
# print(generic_tree.dump(tree))

# print(f"-------------------------")
# print(f"production tree:")
# print(python_instance.dump(prediction_instances))

concrete_code = python_instance.concretize(prediction_instances)
print(f"-------------------------")
print(f"concretized:")
print(concrete_code)
print(f"-------------------------")
# for pi in prediction_instances:
#     print(pi)







# for pi in prediction_instances:
#     print(pi)


# def generate(name : str):
#     logging.basicConfig(level=logging.INFO)
#     base_path = pathlib.Path(__file__).parent.absolute()
#     dirpath = os.path.join(base_path, "../../res")
#     fpath = os.path.join(dirpath, f"{name}.jsonl")


#     vocab : dict[str, set[str]] = {}

#     write_res_gen(f'{name}_vocab.json', '')
#     write_res_gen(f'{name}_training.txt', '')

#     from datetime import datetime

#     start = datetime.now()

#     with open(fpath, 'r') as f:
#         count = 1
#         line = f.readline()
#         while line: 

#             line_obj = json.loads(line)

#             source_code = line_obj['code']

#             tree = generic_tree.parse('python', source_code, 'utf8')


#             try:
#                 mod = from_generic_ast(tree)

#                 instances = []
#                 try:
#                     instances = serialize_Module(mod)
#                 except RecursionError:
#                     print(f"\n\n")

#                     print(f"""--Generic Tree--\n{
#                         generic_tree.dump(tree, 
#                             text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
#                         )
#                     }\n""")

#                     print(f"\n\n")
#                     print(f"---Source Code---")
#                     print(source_code)
#                     print(f"-------------------------")
#                     print(f"recursion error line number: {count}")
#                     print("RECURSION ERROR")
#                     return

#                 else:

#                     if count < 21:

#                         print(f"-------------------------")
#                         print(f"line number: {count}")
#                         print(f"-------------------------")

#                         concrete_code = python_instance.concretize(instances)

#                         # print(f"-------------------------")
#                         # print(f"generic tree:")
#                         # print(generic_tree.dump(tree))

#                         print(f"-------------------------")
#                         print(f"production tree:")
#                         print(python_instance.dump(instances))

#                         print(f"-------------------------")
#                         print(f"source:")
#                         print(source_code)

#                         print(f"-------------------------")
#                         print(f"concretized:")
#                         print(concrete_code)



#                     def triple_from_instance(inst : instance) -> tuple[str, str, str]:
#                         return match_instance(inst, InstanceHandlers[tuple[str, str, str]](
#                             case_Grammar=lambda o : (
#                                 ("grammar", o.nonterminal, o.sequence_id)
#                             ),
#                             case_Vocab=lambda o : (
#                                 ("vocab", o.choices_id, o.word)
#                             )
#                         )) 


#                     training_data = [
#                         f"[{t[0]},{t[1]},{t[2]}]"
#                         for i in instances
#                         for t in [triple_from_instance(i)] 
#                     ]


#                     # update vocabulary
#                     for inst in instances:
#                         def handle_Vocab(o):
#                             if o.choices_id in vocab.keys():
#                                 vocab[o.choices_id].add(o.word)
#                             else:
#                                 vocab[o.choices_id] = {o.word}

#                         match_instance(inst, InstanceHandlers(
#                             case_Grammar=lambda o : (),
#                             case_Vocab=handle_Vocab 
#                         )) 


#                     write_append_res_gen(f'{name}_training.txt', "[" + ",".join(training_data) + "]" + '\n\n<|endoftext|>\n\n')

#             except Exception as x:


#                 print(f"Another Exception {x}")
#                 print(f"\n\n")

#                 print(f"""--Generic Tree--\n{
#                     generic_tree.dump(tree, 
#                         text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
#                     )
#                 }\n""")

#                 print(f"\n\n")
#                 print(f"---Source Code---")
#                 print(source_code)
#                 print(f"-------------------------")
#                 print(f"line number: {count}")

#                 raise x

#             # update
#             line = f.readline()
#             count += 1
        
#         write_res_gen(f'{name}_vocab.json', json.dumps(
#             {
#                 k:list(v)
#                 for k,v in vocab.items()
#             },
#             indent=4
#         ))


#     end = datetime.now()
#     print(f"time: {end - start}")