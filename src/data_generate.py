from __future__ import annotations
from lib import training_data
import pathlib


base_path = pathlib.Path(__file__).parent.absolute()
# write(os.path.join(base_path, '../res'), 'python_grammar.json', json.dumps(python_schema.grammar, indent=4))

training_data.generate_dir('mbpp')

# apps_0: update line 787 for python 3: change print statement to print call expression
# apps_0: update line 1310 and onwards to remove extra backslash escape characters for double quotes in block string 
# apps_0: update line 1362 to remove extra backslashes for newline continuation 
training_data.generate_dir('apps')
# up to 6 so far