from tree_sitter import Language

import os
import pathlib
# import logging

from lib import util_system as us
# logging.basicConfig(level=logging.INFO)

Language.build_library(
    # Store the library in the `build` directory
    us.project_path('build/grammars.so'),

    # Include one or more languages
    [
        # 'vendor/tree-sitter-python'
        us.project_path('../tree-sitter-python/')
    ]
)