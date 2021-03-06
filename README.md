# Tapas 
Texas program analyzer

## Getting started
### Download this repo
```bash
git clone https://github.com/resin-studio/texaslang.git
```

### Install Conda on MacOS
```bash
brew install --cask miniconda
```

### Install Conda environment
```bash
./install_env.sh
```
`install_env.sh` uses `conda` to create a local environment called `env` from `environment.yml`.
It's simply the following command:
```bash
conda env create --prefix=env -f ./environment.yml
```

### Activate Conda environment
```bash
conda activate ./env
```
Activating the environment sets the variables of your shell and your Python to use the environment's specifications

### Download tree-sitter Python parser
```bash
git clonde https://github.com/resin-studio/tree-sitter-python
```
Download this repo next to this repo.

### Download tree-sitter Python parser
```bash
git clonde https://github.com/resin-studio/tree-sitter-python
```
Download the tree-sitter-python repo next to this repo.

### Download Typeshed
```bash
git clone https://github.com/python/typeshed
```
Download the Typeshed repo next to this repo.

### Build parsers
```bash
src/build_grammars.py
```
run this script to create `build/grammars.so`

### Run tests
```bash
pytest -v src/test_python_analysis_system.py
```

### Create local distribution 
```bash
python setup.py install
```

### Install package locally 
```bash
pip install <local_path_to_repo>
```

## Transliteration
```python
from lib import python_generic_tree_system as pgs 
from lib import python_ast_system as pas
from lib import python_abstract_token_system as pats
from base import abstract_token_system as ats

code : str = ...
gnode = pgs.parse(code)
mod = pas.parse_from_generic_tree(gnode)
mod = pas.parse(code)
abstract_tokens = pas.serialize(mod)
abstract_str = pats.dump(abstract_tokens)
code_again = pats.concretize(abstract_tokens)
```

## Transliteration internals 

### Syntax data model
The syntax data model is located at `src/lib/python_schema_system`.

To generate an abstract syntax tree (AST) model (i.e. data type) run the script `src/generate_lib.py`, which writes the file `src/lib/python_ast_construct_autogen.py`

### Analysis
```python
from lib import python_aux_system as pals
from base import abstract_token_system as ats

package = pals.analyze_typeshed()
module_name = ...
client : pals.Client = pals.spawn_analysis(package, module_name)

from typing import Iterator
token_iter : Iterator[ats.abstract_token]

inher_aux : pals.InherAux = client.init
token = next(token_iter, None)
while token:
    inher_aux = client.next(token)
    token = next(token_iter, None)
    ...
...
```

### Semantic checks
```python
from pyrsistent import pset
from lib import python_aux_system as pals
...

client : pals.Client = pals.spawn_analysis(package, module_name,
    checks = pals.all_checks.remove(pals.DeclareCheck())
)
```
Control which semantic checks are turned on with the `checks` parameter in `spawn_analysis`

```python
from pyrsistent import pset
from lib import python_aux_system as pals
...

client : pals.Client = pals.spawn_analysis(package, module_name,
    checks = pset() 
)
```
Turn off all semantics checks by passing in an empty set into the `checks` parameter of `spawn_analysis`

## Analysis internals
The analysis consists of three parts: the semantic data model, the program crawl, and the recording of information

### Semantic data model
The semantic data model is located at `src/lib/python_aux_construct_def`. 

The `aux` in the name refers to auxiliary information (as opposed to syntactic information). The `construct` refers to the construction of data of this model. The `def` is short for 'definition' because this code represents the definition of the construction of aux data, rather than the construction itself. The aux data model includes `InherAux` to store data that is passed as the crawling of the program proceeds across the program from left to right; `SynthAux` to store data that is deduced from current and child syntactic nodes and passed back up; `type` to represent various approximate descriptions of expressions and other elements in the program; and various other useful representations.

To generate the data model constructors run the script `src/generate_lib.py`, which writes the file `src/lib/python_aux_construct_autogen.py`

### Program crawl 
The program crawl is located at `src/lib/python_aux_crawl_stream_def`. The `crawl` refers to inspecting each part of a program to gather and pass some information along, and the `stream` refers to the program as a stream of abstract tokens. The program crawl relies on a mixture of (open) recursion and stack machines.

After processing each abstract token, the crawler writes some information to the concurrent output queue and waits for the next abstract token on the concurrent input queue.

To generate the crawler, run the script `src/generate_lib.py`, which writes the file `src/lib/python_aux_crawl_stream_autogen.py`


### Information recording
The information recording is located at `src/lib/python_aux_system.py`. The `Server` class extends the server from the autogenerated program crawler. There are a few places to record information and specify how that information is passed along.

A method that starts with `traverse_` takes in the `InherAux` of the current node and a `SynthAux` for each sibling to the left of the child node under consideration, and it returns an `InherAux` for the child node. 

A method that starts with `synthesize_` takes in the `InherAux` of the current node and for each child node, an AST and a `SynthAux` associated with that child node, and it returns a `SynthAux` for the current node.

-default behavior of traversal in method `traverse_auxes`
-default behavior of synthesis in method `synthesize_auxes`
-bespoke behavior of traversal for choice nodes in method `traverse_<node_lhs>_<node_rhs>_<field>`
-bespoke behavior of synthesis for choice nodes in method `synthesize_for_<node_lhs>_<node_rhs>`
-bespoke behavior of traversal for single nodes in method `traverse_<node>_<field>`
-bespoke behavior of synthesis for single nodes in method `synthesize_for_<node>`
