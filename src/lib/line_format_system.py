from __future__ import annotations
from typing import Iterator

from lib.line_format_construct_autogen import * 

def to_string(line_form : line_format) -> str:
    return match_line_format(line_form, LineFormatHandlers[str](
        case_InLine = lambda _ : "InLine",
        case_NewLine = lambda _ : "NewLine", 
        case_IndentLine = lambda _ : "IndentLine" 
    ))
