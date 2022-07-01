from __future__ import annotations
from tapas_lib import python_data_system
from tapas_base.util_system import write, project_path
from tapas_lib import python_schema_system
import os
import json

write(project_path('tapas_res'), 'python_grammar.json', json.dumps(python_schema_system.portable_schema, indent=4))
