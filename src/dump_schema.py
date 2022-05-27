from __future__ import annotations
from lib import python_data_system
from base.util_system import write, project_path
from lib import python_schema_system
import os
import json

write(project_path('res'), 'python_grammar.json', json.dumps(python_schema_system.portable_schema, indent=4))
