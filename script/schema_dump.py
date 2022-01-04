from __future__ import annotations
from lib import data
from lib.util import write, project_path
import os
import json
from lib import python_schema

write(project_path('res'), 'python_grammar.json', json.dumps(python_schema.portable, indent=4))
