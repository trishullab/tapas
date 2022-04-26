from __future__ import annotations
from lib import data_system
from lib.util_system import write, project_path
import os
import json
from lib import python_schema_system

write(project_path('res'), 'python_grammar.json', json.dumps(python_schema_system.portable_schema, indent=4))
