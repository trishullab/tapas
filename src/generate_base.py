from __future__ import annotations

from tapas_base.util_system import write_code
from tapas_base import line_format_construct_def
from tapas_base import abstract_token_construct_def
from tapas_base import rule_construct_def

write_code('tapas_base', "rule_construct", rule_construct_def.generate_content())

write_code('tapas_base', "line_format_construct", line_format_construct_def.generate_content())

write_code('tapas_base', "abstract_token_construct", abstract_token_construct_def.generate_content())