from tree_sitter import Language

import os
import pathlib
# import logging

# logging.basicConfig(level=logging.INFO)
base_path = pathlib.Path(__file__).parent.absolute()

def relative(rel_path : str) -> str:
    return os.path.join(base_path, rel_path)

Language.build_library(
    # Store the library in the `build` directory
    relative('../build/grammars.so'),

    # Include one or more languages
    [
        # 'vendor/tree-sitter-python'
        relative('../../tree-sitter-python/')
    ]
)