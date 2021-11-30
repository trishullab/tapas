from __future__ import annotations

from lib import def_type
from lib import line_format_def_type
from lib import instance_def_type

import lib.rule
from lib import python_schema

from lib import def_serialize
# from lib import def_rename

from lib.file import write
import pathlib
import os


base_path = pathlib.Path(__file__).parent.absolute()

dirpath = os.path.join(base_path, '../src_souffle/gen')


def souffle_type_map(s):
    if s == 'str':
        return 'symbol'
    else:
        return s


write(dirpath, "python_ast.dl", (
    "\n\n".join([
        def_type.generate_souffle(type_name, [
            lib.rule.to_constructor(node)
            for node in nodes 
        ], souffle_type_map)
        for type_name, nodes in python_schema.nonterminal_map.items()
    ])
))

instance_list = f"{instance_def_type.type_name}_list"
write(dirpath, "instance.dl", (
    "\n\n".join([
        def_type.generate_souffle(instance_def_type.type_name, instance_def_type.constructors, souffle_type_map)
    ])
))