# Texas Language System

## Install environment
```bash
./install_env.sh
```
`install_env.sh` uses `conda` to create a a local environment called `env` from `environment.yml`.
It's simply the following command:
```bash
conda env create --prefix=env -f ./environment.yml
```

## Activate environment
```bash
conda activate ./env
```
Activating the environment sets the variables of your shell and your Python to use the environment's specifications

## Python schema
The Python schema is defined at `lib/python_schema.py`. This field `grammar` specifies the full grammar as a map from nonterminal keys to choices of nodes, which represent sequences of terminals and nonterminals. The field `node_map` maps the node names to nodes (i.e. sequence IDs to sequences).

## Code generation
`lib/def_type.py`, `lib/def_serialize.py`, and other `lib/def_` prefixed files define generation of well-typed Python code.
The script `code_generate.py` calls these definitions with the Python schema to generate well-typed constructors and procedures for Python ASTs.
The generate code is written to the `gen` directory.

## Serialized production instances
A list of production instances generated from a Python AST, is a linear leftward depth-first representation of a Python program.
The constructors and static types for production instances is generated and written to `gen/production_instance.py`.
Various processing tools for production instances, including concretizing to human-readable Python programs, are defined at `lib/production_instance.py`


