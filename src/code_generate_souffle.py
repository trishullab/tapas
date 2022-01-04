from __future__ import annotations

from lib import def_construct
from lib import def_line_format_construct
from lib import def_instance_construct

import lib.rule
from lib import python_schema

from lib import def_ast_serialize
# from lib import def_rename

from lib import util

from lib.util import write

dirpath = util.project_path('src_souffle/gen')

def souffle_construct_map(s):
    if s == 'str':
        return 'symbol'
    else:
        return s


write(dirpath, "python_ast.dl", (
    "\n\n".join([
        def_construct.generate_souffle(type_name, [
            lib.rule.to_constructor(node)
            for node in nodes 
        ], souffle_construct_map)
        for type_name, nodes in python_schema.nonterminal_map.items()
    ])
))

instance_list = f"{def_instance_construct.type_name}_list"
write(dirpath, "instance.dl", (
    "\n\n".join([
        def_construct.generate_souffle(def_instance_construct.type_name, def_instance_construct.constructors, souffle_construct_map)
    ])
))


from lib import def_reconsitute_souffle

write(dirpath, "reconstitute.dl", def_reconsitute_souffle.content)