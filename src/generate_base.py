from __future__ import annotations

from base.util_system import write_code
from base import line_format_construct_def
from base import abstract_token_construct_def
from base import rule_construct_def

write_code('base', "rule_construct", rule_construct_def.generate_content())

write_code('base', "line_format_construct", line_format_construct_def.generate_content())

write_code('base', "abstract_token_construct", abstract_token_construct_def.generate_content())