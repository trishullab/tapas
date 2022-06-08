# Tapas 
Texas program analyzer

## Download this repo
```bash
git clone https://github.com/resin-studio/texaslang.git
```

## Install Conda on MacOS
```bash
brew install --cask miniconda
```

## Install Conda environment
```bash
./install_env.sh
```
`install_env.sh` uses `conda` to create a a local environment called `env` from `environment.yml`.
It's simply the following command:
```bash
conda env create --prefix=env -f ./environment.yml
```

## Activate Conda environment
```bash
conda activate ./env
```
Activating the environment sets the variables of your shell and your Python to use the environment's specifications

## Download tree-sitter Python parser
```bash
git clonde https://github.com/resin-studio/tree-sitter-python
```
Download this repo next to this repo.

## Download tree-sitter Python parser
```bash
git clonde https://github.com/resin-studio/tree-sitter-python
```
Download the tree-sitter-python repo next to this repo.

## Download Typeshed
```bash
git clone https://github.com/python/typeshed
```
Download the typeshed repo next to this repo.

## Build parsers
```bash
src/build_grammars.py
```
run this script to create `build/grammars.so`

## Run tests
```bash
pytest -v src/test_python_analysis_system.py
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

## Analysis
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

## Semantic checks
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
