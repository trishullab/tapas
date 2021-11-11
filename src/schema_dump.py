from __future__ import annotations
from lib import data
import pathlib
from lib.file import write
import os
import json
from lib import python_schema

base_path = pathlib.Path(__file__).parent.absolute()
write(os.path.join(base_path, '../res'), 'python_grammar.json', json.dumps(python_schema.grammar, indent=4))
