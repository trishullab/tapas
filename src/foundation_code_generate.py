from __future__ import annotations

from lib.util import write_code

from lib import line_format_construct_def
from lib import abstract_token_construct_def
from lib import rule_construct_def

write_code("rule_construct", rule_construct_def.generate_content())

write_code("line_format_construct", line_format_construct_def.generate_content())

write_code("abstract_token_construct", abstract_token_construct_def.generate_content())