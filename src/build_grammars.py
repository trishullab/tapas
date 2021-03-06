from tree_sitter import Language

import os
import pathlib
# import logging

from tapas_base import util_system as us
# logging.basicConfig(level=logging.INFO)

Language.build_library(
    # Store the library in the `build` directory
    us.project_path('tapas_res/grammars.so'),

    # Include one or more languages
    [
        # 'vendor/tree-sitter-python'
        us.project_path('tapas_res/tree-sitter-python/')
    ]
)