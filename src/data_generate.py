from __future__ import annotations
import json

from lib import python_schema 
from lib.file import write_res_gen
from lib import apps_training_data
from lib import training_data

# write_res_gen('python_grammar.txt', python_schema.format())
write_res_gen('python_grammar.json', json.dumps(python_schema.grammar_dictionary, indent=4))

training_data.generate('mbpp')

# apps_training_data.compile()

# apps_0: update line 787 for python 3: change print statement to print call expression
# apps_0: update line 1310 and onwards to remove extra backslash escape characters for double quotes in block string 
# apps_0: update line 1362 to remove extra backslashes for newline continuation 
# training_data.generate('apps_0')
# training_data.generate('apps_1')
# training_data.generate('apps_2')
# training_data.generate('apps_3')
# training_data.generate('apps_4')
# training_data.generate('apps_5')
# training_data.generate('apps_6')
# training_data.generate('apps_7')
# training_data.generate('apps_8')
# training_data.generate('apps_9')